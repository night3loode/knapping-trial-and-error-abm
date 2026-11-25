"""
V1 model, implemented from "Methods - Base Model V1" (Dhairya Yadav, 24 Sep 2026).
Section numbers in comments refer to that document.

States: 0 nodule, 1 platform prepared, 2 roughed-out, 3 thinned (FINISHED), 4 alt. roughed-out.
BROKEN = -1. Strikes are points x = (location, angle, force) in [0,100]^3.

Every Real technique j: from-state FROM[j], result RES[j], target MU[j,3], tolerance TAU[j]
(same on all three parameters in V1).
"""
import numpy as np
from numba import njit

S = 5          # number of state types
FIN = 3        # finished state
BROKEN = -1

# ---------------- the Real world (section 2) ----------------
# j : from -> result : target : tol : role
#  0 : 0 -> 1 : easy  : drift-control twin
#  1 : 0 -> 1 : easy  : drift-control twin
#  2 : 1 -> 2 : HARD  : main route, unavoidable on that route
#  3 : 2 -> 3 : easy  : competes with 4 (same result)
#  4 : 2 -> 3 : HARD  : competes with 3
#  5 : 1 -> 4 : medium: alternative route
#  6 : 4 -> 3 : medium: alternative route
FROM = np.array([0, 0, 1, 2, 2, 1, 4])
RES  = np.array([1, 1, 2, 3, 3, 4, 3])
# All targets sit 25 units from the centre (50,50,50), so no technique is easier to acquire just
# because of where it is (fixes the location artefact found in verification test V11).
MU = np.array([[75., 50, 50], [25, 50, 50], [50, 75, 50], [50, 50, 75],
               [50, 50, 25], [50, 25, 50], [64.43, 64.43, 64.43]])
def make_tau(easy=10., medium=6., hard=4.):
    return np.array([easy, easy, hard, easy, hard, medium, medium])

@njit(cache=True)
def physics(s, x, FROM, RES, MU, TAU, smat):
    """2.3: distance to each technique from s (with stone-to-stone shift xi), nearest within 1 wins."""
    best = 1e18; res = BROKEN
    for j in range(FROM.shape[0]):
        if FROM[j] != s:
            continue
        d2 = 0.0
        for k in range(3):
            xi = np.random.normal(0.0, smat) if smat > 0 else 0.0
            d2 += ((x[k]-MU[j, k]-xi)/TAU[j])**2
        if d2 <= 1.0 and d2 < best:
            best = d2; res = RES[j]
    return res

@njit(cache=True)
def new_agent(a, mu, sd, phi, ncount, rs, ra, stone, age, K, sd_init):
    """3.3 naive newborn."""
    for s in range(S):
        for t in range(S):
            ncount[a, s, t] = 0
            rs[a, s, t] = 0
            ra[a, s, t] = 0
            for c in range(K):
                phi[a, s, t, c] = 1.0/K
                for k in range(3):
                    mu[a, s, t, c, k] = np.random.rand()*100
                    sd[a, s, t, c, k] = sd_init
    stone[a] = 0
    age[a] = 0

@njit(cache=True)
def values(a, ncount, rs, ra):
    """3.1: V(s) = best product of own reliabilities along a route to FIN."""
    V = np.zeros(S); V[FIN] = 1.0
    for _ in range(S):
        for s in range(S):
            if s == FIN:
                continue
            best = 0.0
            for t in range(S):
                if ncount[a, s, t] > 0:
                    r = (rs[a, s, t]+1.0)/(ra[a, s, t]+2.0)
                    v = r*V[t]
                    if v > best:
                        best = v
            V[s] = best
    return V

@njit(cache=True)
def choose(a, s, beta, ncount, rs, ra, phi, K):
    """Section 4 steps 1-2: choose target state s'* and technique Belief c. Returns (t, c, random?)."""
    V = values(a, ncount, rs, ra)
    w = np.zeros(S); tot = 0.0
    for t in range(S):
        if t != s and ncount[a, s, t] > 0 and V[t] > 0:
            w[t] = np.exp(beta*V[t]); tot += w[t]
    if tot == 0.0:   # empty map: strike at random with any Belief from s
        while True:
            t = 1 + np.random.randint(S-1)
            if t != s:
                break
        return t, np.random.randint(K), True
    r = np.random.rand()*tot; acc = 0.0; t = 0
    for u in range(S):
        acc += w[u]
        if w[u] > 0 and r < acc:
            t = u; break
    r = np.random.rand(); acc = 0.0; c = K-1
    for cc in range(K):
        acc += phi[a, s, t, cc]
        if r < acc:
            c = cc; break
    return t, c, False

@njit(cache=True)
def simulate(seed, N, iters, life, crit, crit_prac, K, sd_init, alpha, W, sobs, smat,
             beta, eta_mu, eta_sd, eta_phi, practice, n_att, delta, eta_P, seeded,
             FROM, RES, MU, TAU, nbr_ptr, nbr_idx, rec, phi_min):
    np.random.seed(seed)
    J = FROM.shape[0]
    mu = np.zeros((N, S, S, K, 3)); sd = np.zeros((N, S, S, K, 3)); phi = np.zeros((N, S, S, K))
    ncount = np.zeros((N, S, S), np.int64)
    rs = np.zeros((N, S, S)); ra = np.zeros((N, S, S))
    stone = np.zeros(N, np.int64); age = np.zeros(N, np.int64)
    for a in range(N):
        new_agent(a, mu, sd, phi, ncount, rs, ra, stone, age, K, sd_init)
        if seeded:       # 3.3 seeded start: Beliefs near Real targets, Real transitions on the map
            slot = np.zeros((S, S), np.int64)
            for j in range(J):
                f = FROM[j]; t = RES[j]; c = slot[f, t]; slot[f, t] += 1
                for k in range(3):
                    mu[a, f, t, c, k] = MU[j, k] + np.random.normal(0, 0.5)
                ncount[a, f, t] = 1
    nrec = iters//rec + 1
    surv = np.zeros((nrec, J))         # share of agents holding Real technique j
    tsucc = np.zeros((nrec, J))        # share of attempts AIMED at technique j's result... per technique: strikes that landed in j
    route = np.zeros(nrec)             # share of choices at state 1 aimed at state 2 (hard route)
    comp = np.zeros(nrec)              # finished / (finished + broken)
    hits = np.zeros(J); n_strk_from = np.zeros(S)
    r12 = 0.0; r1all = 0.0; nfin = 0.0; nbrk = 0.0
    x = np.zeros(3); xo = np.zeros(3); xsum = np.zeros(3)
    dead = np.zeros(N, np.int64)
    R = 0
    for it in range(iters+1):
        if it % rec == 0:
            for j in range(J):
                f = FROM[j]; t = RES[j]; cnt = 0
                for a in range(N):
                    for c in range(K):
                        d2 = 0.0
                        for k in range(3):
                            d2 += ((mu[a, f, t, c, k]-MU[j, k])/TAU[j])**2
                        if d2 <= 1.0 and phi[a, f, t, c] >= phi_min:
                            cnt += 1; break
                surv[R, j] = cnt/N
                tsucc[R, j] = hits[j]/n_strk_from[f] if n_strk_from[f] > 0 else np.nan
            route[R] = r12/r1all if r1all > 0 else np.nan
            comp[R] = nfin/(nfin+nbrk) if nfin+nbrk > 0 else np.nan
            hits[:] = 0; n_strk_from[:] = 0; r12 = 0; r1all = 0; nfin = 0; nbrk = 0
            R += 1
        if it == iters:
            break
        for a in range(N):
            age[a] += 1
        # ---- section 6: practice (before striking) ----
        if practice:
            for a in range(N):
                if age[a] > crit_prac:
                    continue
                s = stone[a]
                t, c, rnd = choose(a, s, beta, ncount, rs, ra, phi, K)
                ns = 0; xsum[:] = 0
                for h in range(n_att):
                    for k in range(3):
                        x[k] = mu[a, s, t, c, k] + np.random.normal(0, delta) + np.random.normal(0, W)
                        x[k] = min(max(x[k], 0.0), 100.0)
                    out = physics(s, x, FROM, RES, MU, TAU, smat)
                    ra[a, s, t] += 1
                    if out == t:
                        rs[a, s, t] += 1; ns += 1
                        for k in range(3):
                            xsum[k] += x[k]
                if ns > 0:
                    for k in range(3):
                        mu[a, s, t, c, k] += eta_P*(xsum[k]/ns - mu[a, s, t, c, k])
        # ---- section 4 + 5: each agent strikes once, one neighbour watches ----
        nd = 0
        for a in range(N):
            s = stone[a]
            t, c, rnd = choose(a, s, beta, ncount, rs, ra, phi, K)
            if s == 1:
                r1all += 1
                if t == 2:
                    r12 += 1
            for k in range(3):
                xi_ = mu[a, s, t, c, k]
                if alpha < 1.0:
                    xi_ = np.random.normal(xi_, sd[a, s, t, c, k]*(1-alpha))
                x[k] = min(max(xi_ + np.random.normal(0, W), 0.0), 100.0)
            out = physics(s, x, FROM, RES, MU, TAU, smat)
            n_strk_from[s] += 1
            if out != BROKEN:
                for j in range(FROM.shape[0]):   # which Real technique did it land in (for logging)
                    if FROM[j] == s and RES[j] == out:
                        d2 = 0.0
                        for k in range(3):
                            d2 += ((x[k]-MU[j, k])/TAU[j])**2
                        if d2 <= 1.5:
                            hits[j] += 1; break
            ra[a, s, t] += 1          # own reliability bookkeeping
            if out == t:
                rs[a, s, t] += 1
            # ---- observer ----
            deg = nbr_ptr[a+1]-nbr_ptr[a]
            b = nbr_idx[nbr_ptr[a]+np.random.randint(deg)]
            if out != BROKEN and age[b] <= crit:
                for k in range(3):
                    xo[k] = x[k] + np.random.normal(0, sobs)
                # 5.2 classify among b's Beliefs for (s, out)
                lp = np.zeros(K); mx = -1e300
                for cc in range(K):
                    v = np.log(phi[b, s, out, cc])
                    for k in range(3):
                        sdk = sd[b, s, out, cc, k]
                        v += -0.5*np.log(2*np.pi) - np.log(sdk) - 0.5*((xo[k]-mu[b, s, out, cc, k])/sdk)**2
                    lp[cc] = v
                    if v > mx:
                        mx = v
                tot = 0.0
                for cc in range(K):
                    lp[cc] = np.exp(lp[cc]-mx); tot += lp[cc]
                win = 0; bp = -1.0
                for cc in range(K):
                    lp[cc] /= tot
                    if lp[cc] > bp:
                        bp = lp[cc]; win = cc
                # 5.3 F&S gradient updates
                for cc in range(K):
                    p = lp[cc]
                    for k in range(3):
                        m0 = mu[b, s, out, cc, k]; s0 = sd[b, s, out, cc, k]
                        mu[b, s, out, cc, k] = min(max(m0 + eta_mu*p*(xo[k]-m0)/s0**2, 0.0), 100.0)
                        sd[b, s, out, cc, k] = max(s0 + eta_sd*p*((xo[k]-m0)**2/s0**3 - 1/s0), 1.0)
                phi[b, s, out, win] += eta_phi*bp
                phi[b, s, out, :] /= phi[b, s, out, :].sum()
                ncount[b, s, out] += 1
            # stone update
            if out == BROKEN:
                nbrk += 1; stone[a] = 0
            elif out == FIN:
                nfin += 1; stone[a] = 0
            else:
                stone[a] = out
            if np.random.rand() < 1.0/life:
                dead[nd] = a; nd += 1
        for i in range(nd):
            new_agent(dead[i], mu, sd, phi, ncount, rs, ra, stone, age, K, sd_init)
    return surv, tsucc, route, comp, mu, sd, phi, age, ncount
