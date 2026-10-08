"""Segment-based adaptive bitrate streaming simulator with transparent QoE proxy."""
from dataclasses import dataclass
from math import sin,pi
from random import Random
from statistics import mean,pstdev
BITRATES=(300,700,1200,2000,3500,5500,8000)
LABELS=('144p','240p','360p','480p','720p','1080p','1440p')
PROFILES=('stable','mobile','congested','variable','drop','recovery','extreme')

def trace_for(profile='variable',segments=90,seed=42,base=4500):
    if profile not in PROFILES:raise ValueError('Unknown profile')
    if not 10<=segments<=500:raise ValueError('Segments must be 10–500')
    rng=Random(seed);out=[]
    for i in range(segments):
        phase=i/max(1,segments-1)
        if profile=='stable': value=base+rng.gauss(0,base*.045)
        elif profile=='mobile':value=base*(.75+.40*sin(i*.25))+rng.gauss(0,base*.18)
        elif profile=='congested':value=base*(.30+.18*sin(i*.19))+rng.gauss(0,base*.08)
        elif profile=='drop':value=base*(1 if phase<.35 else .16 if phase<.72 else .8)+rng.gauss(0,base*.06)
        elif profile=='recovery':value=base*(.18 if phase<.35 else .45 if phase<.65 else 1.15)+rng.gauss(0,base*.06)
        elif profile=='extreme':value=base*(.25+1.4*rng.random())*(.20 if i%13 in (0,1,2) else 1)
        else:value=base*(.65+.38*sin(i*.20))+rng.gauss(0,base*.13)
        out.append(round(max(180,value),1))
    return out

def features(history,buffer,last_bitrate):
    recent=list(history[-5:]) or [1000.]
    return [recent[-1],mean(recent[-3:]),mean(recent),pstdev(recent) if len(recent)>1 else 0.,(recent[-1]-recent[0])/max(1,len(recent)-1),buffer,last_bitrate]

def choose(strategy,history,buffer,last_bitrate,model=None):
    if strategy=='fixed':return 3500,3500.,'Fixed 720p baseline',None
    if strategy=='buffer':
        idx=0 if buffer<4 else 1 if buffer<8 else 2 if buffer<12 else 3 if buffer<18 else 4 if buffer<24 else 5
        return BITRATES[idx],float(BITRATES[idx]),'Buffer-threshold baseline',None
    if strategy=='throughput':
        estimate=mean(history[-4:]) if history else 1000.
        reason='Recent throughput moving average'
    elif strategy=='ml':
        if model is None:raise RuntimeError('ML model missing: run python -m ml.train')
        estimate=max(180.,float(model.predict([features(history,buffer,last_bitrate)])[0]))
        reason='Trained gradient boosting predicts next-segment bandwidth from throughput history, trend, variance, buffer and previous quality'
    else:raise ValueError('Unknown strategy')
    safe=estimate*(.58 if buffer<6 else .72 if buffer<14 else .86)
    bitrate=max((b for b in BITRATES if b<=safe),default=BITRATES[0])
    return bitrate,round(estimate,1),reason,None

def simulate(trace,strategy='ml',model=None,segment_seconds=4.,buffer_capacity=30.,latency_ms=40.,packet_loss=0.):
    if not trace or any(x<=0 for x in trace):raise ValueError('Bandwidth must be positive')
    if not 2<=segment_seconds<=6 or not 8<=buffer_capacity<=120:raise ValueError('Invalid buffer or segment duration')
    if not 0<=packet_loss<=.5 or not 0<=latency_ms<=2000:raise ValueError('Invalid network parameters')
    buffer=0.; startup=0.; previous=700;history=[];rows=[];stall_total=0.;events=0;switches=0;played=0.;elapsed=0.
    for i,bandwidth in enumerate(trace):
        selected,estimate,reason,_=choose(strategy,history,buffer,previous,model)
        effective=max(100.,bandwidth*(1-packet_loss))
        download=segment_seconds*selected/effective+latency_ms/1000
        if i==0:
            startup=download;elapsed+=download;buffer=segment_seconds;stall=0.
        else:
            stall=max(0.,download-buffer);events+=int(stall>0);stall_total+=stall
            buffer=min(buffer_capacity,max(0.,buffer-download)+segment_seconds)
            elapsed+=download
        switches+=int(i>0 and selected!=previous)
        played+=segment_seconds
        quality_reward=selected/1000
        switching_cost=abs(selected-previous)/1000*.12 if i>0 else 0
        qoe_step=quality_reward-4.3*stall-switching_cost
        rows.append({'segment':i+1,'bandwidth_kbps':bandwidth,'throughput_kbps':round(effective,1),'bitrate_kbps':selected,'quality':LABELS[BITRATES.index(selected)],'buffer_seconds':round(buffer,2),'download_seconds':round(download,3),'stall_seconds':round(stall,3),'rebuffer_event':bool(stall>0),'playback_seconds':round(played,2),'elapsed_seconds':round(elapsed,2),'estimated_bandwidth_kbps':estimate,'reason':reason,'qoe_step':round(qoe_step,3)})
        history.append(effective);previous=selected
    avg=mean(r['bitrate_kbps'] for r in rows)
    qoe=mean(r['qoe_step'] for r in rows)-.1*startup
    summary={'strategy':strategy,'segments':len(rows),'average_bitrate_kbps':round(avg,1),'average_quality':round(mean(BITRATES.index(r['bitrate_kbps']) for r in rows),2),'rebuffer_events':events,'rebuffer_seconds':round(stall_total,2),'rebuffer_ratio':round(stall_total/(played+stall_total),4),'quality_switches':switches,'startup_seconds':round(startup,3),'qoe_score':round(qoe,3),'total_playback_seconds':round(played,1)}
    return {'summary':summary,'timeline':rows}
