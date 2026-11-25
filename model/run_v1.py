import numpy as np, networkx as nx, time
import v1
def adj(g):
    ptr=[0]; idx=[]
    for a in range(g.number_of_nodes()):
        idx+=sorted(g.neighbors(a)); ptr.append(len(idx))
    return np.array(ptr,np.int64),np.array(idx,np.int64)
DEF=dict(N=50,iters=40000,life=10000,crit=40000,crit_prac=40000,K=3,sd_init=5.,alpha=1.,
         W=1.5,sobs=3.,smat=1.,beta=5.,eta_mu=1.,eta_sd=1.,eta_phi=.001,practice=0,n_att=5,
         delta=None,eta_P=.1,seeded=1,net='full',rec=1000,phi_min=.1,easy=10.,medium=6.,hard=4.)
def run(seed=0,**kw):
    p=dict(DEF); p.update(kw)
    if p['delta'] is None: p['delta']=float(np.sqrt(p['W']**2+p['sobs']**2))
    g=nx.complete_graph(p['N']) if p['net']=='full' else nx.connected_caveman_graph(p['N']//10,10)
    ptr,idx=adj(g)
    TAU=v1.make_tau(p['easy'],p['medium'],p['hard'])
    return v1.simulate(seed,p['N'],p['iters'],p['life'],p['crit'],p['crit_prac'],p['K'],p['sd_init'],
        p['alpha'],p['W'],p['sobs'],p['smat'],p['beta'],p['eta_mu'],p['eta_sd'],p['eta_phi'],
        p['practice'],p['n_att'],p['delta'],p['eta_P'],p['seeded'],
        v1.FROM,v1.RES,v1.MU,TAU,ptr,idx,p['rec'],p['phi_min'])
if __name__=='__main__':
    t=time.time(); run(iters=100); print('compile',round(time.time()-t,1))
    for pr in [0,1]:
        t=time.time(); s,ts,rt,cp=run(practice=pr)
        print(f'practice={pr} {time.time()-t:.1f}s')
        for r in [0,5,10,20,40]:
            print(' t=%5d surv'%(r*1000),np.round(s[r],2),' route->hard %.2f comp %.2f'%(rt[r],cp[r]))
