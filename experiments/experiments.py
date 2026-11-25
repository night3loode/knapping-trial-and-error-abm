"""All experiments for the SPL711 final report. Usage: python experiments.py <name>"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))

import sys, time, json, numpy as np
from run_v1 import run
OUT='results/'
import os; os.makedirs(OUT,exist_ok=True)
def summ(o):
    s,ts,rt,cp=o[:4]
    return dict(surv=s[-5:].mean(0).tolist(), surv_t=s.tolist(),
                route=float(np.nanmean(rt[-5:])), comp=float(np.nanmean(cp[-5:])))
def sweep(name, settings, seeds):
    fn=OUT+name+'.json'
    res=json.load(open(fn)) if os.path.exists(fn) else []
    done=[r['setting'] for r in res]
    t=time.time()
    for st in settings:
        if done.count(st)>=seeds: continue
        res=[r for r in res if r['setting']!=st]
        for sd in range(seeds):
            r=summ(run(seed=sd,**st)); r.update(setting=st,seed=sd); res.append(r)
        json.dump(res,open(OUT+name+'.json','w'))
        print(name,st,f'{time.time()-t:.0f}s',flush=True)
E=sys.argv[1]
if E=='main':      # E1: H1/H2 core: tolerance of the hard techniques x practice
    sweep(E,[dict(hard=h,practice=p) for p in (0,1) for h in (2.,3.,4.,5.,6.)],20)
if E=='noise':     # E2: motor noise x perception noise x practice
    sweep(E,[dict(W=w,sobs=o,practice=p) for p in (0,1) for w in (0.5,1.5,3.) for o in (1.,3.,6.)],10)
if E=='ofat':      # E3: one-factor-at-a-time sensitivity, both conditions
    base=[('eta_P',[.02,.05,.2,.5]),('n_att',[1,3,10]),('beta',[0.,2.,10.]),('K',[2,5]),
          ('N',[20,100]),('life',[5000,20000]),('net',['caveman']),('smat',[0.,2.]),
          ('crit_prac',[5000])]
    st=[{}]+[{k:v} for k,vs in base for v in vs]
    sweep(E,[dict(s,practice=p) for s in st for p in (0,1)],8)
if E=='robust':    # E4: robustness of the measure and run length
    sweep(E,[dict(phi_min=f,practice=p) for f in (.05,.2) for p in (0,1)]+
            [dict(iters=80000,practice=p) for p in (0,1)],10)
if E=='lhs':       # E5: global uncertainty analysis, Latin hypercube over uncertain parameters
    rng=np.random.default_rng(42); n=60
    rngs={'W':(.5,3.),'sobs':(1.,6.),'smat':(0.,2.),'eta_P':(.02,.5),'beta':(0.,10.),'hard':(2.,6.)}
    cols={k:(rng.permutation(n)+rng.uniform(size=n))/n for k in rngs}
    pts=[{k:float(lo+(hi-lo)*cols[k][i]) for k,(lo,hi) in rngs.items()} for i in range(n)]
    fn=OUT+'lhs.json'
    res=json.load(open(fn)) if os.path.exists(fn) else []
    t=time.time()
    for i,p in enumerate(pts):
        if i < len(res)//2: continue
        for pr in (0,1):
            r=summ(run(seed=1000+i,practice=pr,**p)); r.update(setting=dict(p,practice=pr),seed=1000+i); res.append(r)
        json.dump(res,open(OUT+'lhs.json','w'))
        if i%10==0: print('lhs',i,f'{time.time()-t:.0f}s',flush=True)
