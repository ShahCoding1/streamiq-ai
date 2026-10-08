import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.engine import trace_for,simulate,features
from ml.train import dataset
client=TestClient(app)
def test_scenarios():assert len(client.get('/api/scenarios').json()['profiles'])==7
def test_model_ready():assert client.get('/api/model/info').json()['ready']
def test_prediction():
 r=client.post('/api/ml/predict',json={'history':[1200,1300,1500,1800,2200],'buffer_seconds':15});assert r.status_code==200;assert r.json()['bitrate_kbps']>0
def test_simulation_persists():
 r=client.post('/api/simulation/run',json={'segments':20,'seed':111});assert r.status_code==200;sid=r.json()['session_id'];assert client.get(f'/api/sessions/{sid}').status_code==200;assert 'segment' in client.get(f'/api/sessions/{sid}/export?format=csv').text
def test_comparison_same_trace():
 r=client.post('/api/comparison/run',json={'segments':25});assert r.status_code==200
 data=r.json();assert len(data)==4
 for strategy in data:assert len(data[strategy]['timeline'])==25
 assert len({tuple(x['bandwidth_kbps'] for x in data[k]['timeline']) for k in data})==1
def test_stalls_when_network_drops():
 result=simulate([9000]*5+[200]*15,'fixed');assert result['summary']['rebuffer_events']>0
 assert result['summary']['rebuffer_seconds']>0
def test_repeatability():assert trace_for('variable',20,8)==trace_for('variable',20,8)
def test_invalid_profile():assert client.post('/api/simulation/run',json={'profile':'bad'}).status_code==422
def test_validation():assert client.post('/api/simulation/run',json={'packet_loss':3}).status_code==422
def test_no_untrained_claim():assert client.post('/api/ml/predict',json={'history':[500,700,900],'buffer_seconds':4}).json()['confidence'] is None
