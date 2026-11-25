import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))
import numpy as np, v1
from run_v1 import run
print("V11 again (targets equidistant from centre), 24 seeds:")
S=np.array([run(seed=s)[0][-1] for s in range(24)])
print(f"  T0 {S[:,0].mean():.2f}±{S[:,0].std()/np.sqrt(24):.2f}   T1 {S[:,1].mean():.2f}±{S[:,1].std()/np.sqrt(24):.2f}")
v1.MU[[0,1]]=v1.MU[[1,0]]
S2=np.array([run(seed=s)[0][-1] for s in range(24)]); v1.MU[[0,1]]=v1.MU[[1,0]]
print(f"  swapped: T0 {S2[:,0].mean():.2f}  T1 {S2[:,1].mean():.2f}")
print("V8 again, tau=40 everywhere:", np.round(np.mean([run(seed=k,easy=40,medium=40,hard=40)[0][-1] for k in range(8)],0),2))
print("V9 again, no noise:        ", np.round(np.mean([run(seed=k,W=0.,sobs=0.,smat=0.,delta=0.)[0][-1] for k in range(8)],0),2))
print("V12 naive start (nobody seeded), 8 seeds:", np.round(np.mean([run(seed=k,seeded=0)[0][-1] for k in range(8)],0),2))
