import asyncio,csv,io,json,logging,os
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI,HTTPException,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field
import joblib
from sqlalchemy import select
from .engine import trace_for,simulate,choose,features,PROFILES,BITRATES,LABELS
from .database import SessionLocal,SessionRecord
ROOT=Path(__file__).resolve().parents[2]
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
logger=logging.getLogger('streamiq')
app=FastAPI(title='StreamIQ AI API',version='1.0.0')
origins=[x.strip() for x in os.getenv('CORS_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Content-Type'])
class Config(BaseModel):
    profile:str='variable'
    segments:int=Field(90,ge=10,le=500)
    seed:int=Field(42,ge=0,le=1000000)
    base_bandwidth_kbps:float=Field(4500,ge=200,le=30000)
    latency_ms:float=Field(40,ge=0,le=2000)
    packet_loss:float=Field(0,ge=0,le=.5)
    segment_seconds:float=Field(4,ge=2,le=6)
    buffer_capacity:float=Field(30,ge=8,le=120)
    strategy:str='ml'
class Prediction(BaseModel):
    history:list[float]=Field(min_length=1,max_length=20)
    buffer_seconds:float=Field(ge=0,le=120)
    last_bitrate_kbps:int=700
@lru_cache(maxsize=1)
def artifact():
    path=ROOT/'ml/models/bandwidth.joblib'
    if not path.exists():raise FileNotFoundError('Model not trained. Run python -m ml.train')
    return joblib.load(path)
def get_model():
    try:return artifact()['estimator']
    except (FileNotFoundError,ValueError,KeyError) as exc:raise HTTPException(503,str(exc)) from exc
def execute(cfg):
    if cfg.profile not in PROFILES:raise HTTPException(422,'Unknown network profile')
    if cfg.strategy not in ('ml','buffer','fixed','throughput'):raise HTTPException(422,'Unknown strategy')
    trace=trace_for(cfg.profile,cfg.segments,cfg.seed,cfg.base_bandwidth_kbps)
    model=get_model() if cfg.strategy=='ml' else None
    return simulate(trace,cfg.strategy,model,cfg.segment_seconds,cfg.buffer_capacity,cfg.latency_ms,cfg.packet_loss)
@app.get('/api/health')
def health():return {'status':'ok','model_ready':(ROOT/'ml/models/bandwidth.joblib').exists()}
@app.get('/api/scenarios')
def scenarios():return {'profiles':PROFILES,'bitrates_kbps':BITRATES,'qualities':LABELS,'strategies':['ml','buffer','fixed','throughput']}
@app.get('/api/model/info')
def model_info():
    data=artifact() if (ROOT/'ml/models/bandwidth.joblib').exists() else None
    return {'ready':data is not None,'metrics':data['metrics'] if data else None,'features':data['feature_names'] if data else None,'algorithm':data['metrics']['model'] if data else None}
@app.post('/api/ml/predict')
def predict(payload:Prediction):
    if any(x<=0 for x in payload.history):raise HTTPException(422,'History values must be positive')
    selected,estimate,reason,_=choose('ml',payload.history,payload.buffer_seconds,payload.last_bitrate_kbps,get_model())
    return {'bitrate_kbps':selected,'quality':LABELS[BITRATES.index(selected)],'estimated_next_bandwidth_kbps':estimate,'explanation':reason,'features':dict(zip(artifact()['feature_names'],features(payload.history,payload.buffer_seconds,payload.last_bitrate_kbps))),'confidence':None,'confidence_note':'Regression model does not produce calibrated classification probabilities'}
@app.post('/api/simulation/run')
def run(cfg:Config):
    result=execute(cfg)
    with SessionLocal() as db:
        record=SessionRecord(profile=cfg.profile,strategy=cfg.strategy,seed=cfg.seed,summary=json.dumps(result['summary']),timeline=json.dumps(result['timeline']))
        db.add(record);db.commit();db.refresh(record);result['session_id']=record.id
    logger.info('simulation completed profile=%s strategy=%s session=%s',cfg.profile,cfg.strategy,result['session_id'])
    return result
@app.post('/api/comparison/run')
def comparison(cfg:Config):
    results={}
    for strategy in ('ml','buffer','fixed','throughput'):
        item=cfg.model_copy(update={'strategy':strategy})
        results[strategy]=execute(item)
    return results
@app.get('/api/sessions')
def sessions(limit:int=20):
    if not 1<=limit<=100:raise HTTPException(422,'limit must be 1–100')
    with SessionLocal() as db:
        rows=db.scalars(select(SessionRecord).order_by(SessionRecord.id.desc()).limit(limit)).all()
        return [{'id':r.id,'profile':r.profile,'strategy':r.strategy,'created_at':r.created_at.isoformat(),'summary':json.loads(r.summary)} for r in rows]
@app.get('/api/sessions/{session_id}')
def session_detail(session_id:int):
    with SessionLocal() as db:
        row=db.get(SessionRecord,session_id)
        if not row:raise HTTPException(404,'Session not found')
        return {'id':row.id,'profile':row.profile,'strategy':row.strategy,'summary':json.loads(row.summary),'timeline':json.loads(row.timeline)}
@app.get('/api/sessions/{session_id}/export')
def export(session_id:int,format:str='json'):
    data=session_detail(session_id)
    if format=='json':return data
    if format!='csv':raise HTTPException(422,'format must be csv or json')
    out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(data['timeline'][0]));writer.writeheader();writer.writerows(data['timeline'])
    return StreamingResponse(iter([out.getvalue()]),media_type='text/csv',headers={'Content-Disposition':f'attachment; filename="streamiq-{session_id}.csv"'})
@app.websocket('/ws/simulation')
async def websocket(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            cfg=Config.model_validate_json(await websocket.receive_text())
            result=execute(cfg)
            for item in result['timeline']:
                await websocket.send_json({'type':'tick','data':item})
                await asyncio.sleep(.045)
            await websocket.send_json({'type':'complete','summary':result['summary']})
    except WebSocketDisconnect:pass
    except Exception as exc:
        logger.warning('websocket error %s',type(exc).__name__)
        await websocket.send_json({'type':'error','message':'Simulation failed; check parameters and model availability'})
        await websocket.close()
