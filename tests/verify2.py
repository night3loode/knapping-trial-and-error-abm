import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))
import numpy as np, v1
from run_v1 import run
rng=np.random.default_rng(0)
def learner(target,sobs,tau,nmax=3000,K=3):
    mu=rng.uniform(0,100,(K,3)); sd=np.full((K,3),5.); phi=np.full(K,1/K)
    for n in range(1,nmax+1):
        x=target+rng.normal(0,sobs,3) if sobs>0 else target.copy()
        lp=np.log(phi)+(-np.log(sd)-0.5*((x-mu)/sd)**2).sum(1)
        p=np.exp(lp-lp.max()); p/=p.sum(); w=p.argmax()
        m0=mu.copy(); s0=sd.copy()
        mu=np.clip(m0+p[:,None]*(x-m0)/s0**2,0,100)
        sd=np.maximum(s0+p[:,None]*((x-m0)**2/s0**3-1/s0),1)
        phi[w]+=.001*p[w]; phi/=phi.sum()
        ok=(((mu-target)/tau)**2).sum(1)<=1
        if (ok&(phi>=.1)).any(): return n
    return np.nan
print("V10. Acquisition test: one naive learner sees ONLY strikes of one technique.")
print("     Observations needed until it holds that technique (median, % never within 3000):")
for tau in [10,6,4]:
    for so in [0,3]:
        r=np.array([learner(v1.MU[2],so,tau) for _ in range(200)])
        print(f"  tau={tau:>2} sigma_obs={so}: median {np.nanmedian(r):6.0f}   never {np.isnan(r).mean()*100:4.0f}%")
print("\nV11. Twin asymmetry: swap the targets of T0 and T1 (16 seeds, social only)")
S=np.array([run(seed=s)[0][-1] for s in range(16)])
v1.MU[[0,1]]=v1.MU[[1,0]]
S2=np.array([run(seed=s)[0][-1] for s in range(16)])
v1.MU[[0,1]]=v1.MU[[1,0]]
print(f"  original: T0 {S[:,0].mean():.2f}  T1 {S[:,1].mean():.2f}")
print(f"  swapped : T0 {S2[:,0].mean():.2f}  T1 {S2[:,1].mean():.2f}")
