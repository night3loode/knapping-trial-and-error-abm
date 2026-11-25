import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))
import numpy as np, v1
from run_v1 import run
from numba import njit
from scipy.stats import chi2
P=lambda *a: print(*a, flush=True)
TAU=v1.make_tau()

P("== V1. Physics unit tests (no material noise) ==")
@njit
def phys(s,x,F,R,M,T,sm): return v1.physics(s,x,F,R,M,T,sm)
ok=True
for j in range(7):
    r=phys(v1.FROM[j],v1.MU[j].copy(),v1.FROM,v1.RES,v1.MU,TAU,0.0); ok&= r==v1.RES[j]
    x=v1.MU[j].copy(); x[0]+=TAU[j]*1.01
    r2=phys(v1.FROM[j],x,v1.FROM,v1.RES,v1.MU,TAU,0.0); ok&= r2==-1
    x=v1.MU[j].copy(); x[0]+=TAU[j]*0.99
    r3=phys(v1.FROM[j],x,v1.FROM,v1.RES,v1.MU,TAU,0.0); ok&= r3==v1.RES[j]
P(" on-target -> result, just inside -> result, just outside -> broken:", "PASS" if ok else "FAIL")
r=phys(1,v1.MU[2].copy(),v1.FROM,v1.RES,v1.MU,TAU,0.0)
P(" a state-1 strike on T2's target gives state 2 (only techniques from current state count):","PASS" if r==2 else "FAIL")
r=phys(0,v1.MU[2].copy(),v1.FROM,v1.RES,v1.MU,TAU,0.0)
P(" the same strike on a nodule (state 0) breaks it:","PASS" if r==-1 else "FAIL")

P("\n== V2. Success probability vs theory (strikes centred on target, motor noise W=1.5, sigma_mat=1) ==")
@njit
def mc(j,W,sm,n,F,R,M,T):
    h=0
    for i in range(n):
        x=np.empty(3)
        for k in range(3): x[k]=M[j,k]+np.random.normal(0,W)
        if v1.physics(F[j],x,F,R,M,T,sm)==R[j]: h+=1
    return h/n
for j,lab in [(0,'easy tau=10'),(5,'medium tau=6'),(2,'hard tau=4')]:
    sim=mc(j,1.5,1.0,200000,v1.FROM,v1.RES,v1.MU,TAU)
    th=chi2.cdf(TAU[j]**2/(1.5**2+1.0**2),3)
    P(f" {lab}: simulated {sim:.3f}  theory {th:.3f}")

P("\n== V3. Learning update identical to F&S / Part D code ==")
# Part D's per-dimension functions with corr=0
lr=1.0
def d_mean(x,m,s,p): return lr*p*((x-m)/s**2)
def d_sd(x,m,s,p): return lr*p*(((x-m)**2)/(s**3)-1/s)
rng=np.random.default_rng(1); maxdiff=0
for _ in range(1000):
    x,m=rng.uniform(0,100,2); s=rng.uniform(1,10); p=rng.uniform()
    mine_m=min(max(m+lr*p*(x-m)/s**2,0),100); ref_m=min(max(m+d_mean(x,m,s,p),0),100)
    mine_s=max(s+lr*p*((x-m)**2/s**3-1/s),1); ref_s=max(s+d_sd(x,m,s,p),1)
    maxdiff=max(maxdiff,abs(mine_m-ref_m),abs(mine_s-ref_s))
P(f" max difference over 1000 random cases: {maxdiff:.2e}","PASS" if maxdiff<1e-9 else "FAIL")

P("\n== V4. Practice off => practice parameters have no effect (same seed) ==")
a=run(seed=3,iters=5000,practice=0,n_att=5,eta_P=.1)[0]; b=run(seed=3,iters=5000,practice=0,n_att=50,eta_P=.9)[0]
P(" identical output:","PASS" if np.array_equal(a,b) else "FAIL")

P("\n== V5. Determinism: same seed -> same run ==")
a=run(seed=7,iters=5000,practice=1); b=run(seed=7,iters=5000,practice=1)
P(" identical:","PASS" if all(np.array_equal(x,y,equal_nan=True) for x,y in zip(a,b)) else "FAIL")

P("\n== V6. No death, no learning (crit=0, practice off): seeded knowledge must stay at 1.0 ==")
s=run(seed=0,iters=20000,life=10**12,crit=0,practice=0)[0]
P(" min survival over run:",s.min(),"PASS" if s.min()==1.0 else "FAIL")

P("\n== V7. No death but learning on: loss only from copying drift ==")
s=run(seed=0,iters=40000,life=10**12)[0]
P(" survival at end:",np.round(s[-1],2))

P("\n== V8. Extreme: all tolerances huge (tau=40) -> nothing should be lost ==")
S=np.array([run(seed=k,easy=40,medium=40,hard=40)[0][-1] for k in range(8)])
P(" mean survival:",np.round(S.mean(0),2))

P("\n== V9. Extreme: no noise anywhere (W=0, sigma_obs=0, sigma_mat=0) ==")
S=np.array([run(seed=k,W=0.,sobs=0.,smat=0.,delta=0.)[0][-1] for k in range(8)])
P(" mean survival:",np.round(S.mean(0),2))
