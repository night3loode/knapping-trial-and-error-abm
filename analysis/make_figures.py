"""Make every figure and summary table in the report from results/*.json. Usage: python make_figures.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))

import json, os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import rankdata
R = 'results/'; F = 'figures/'; os.makedirs(F, exist_ok=True)
NAMES = ['T0 0→1 easy (twin)', 'T1 0→1 easy (twin)', 'T2 1→2 HARD, unavoidable', 'T3 2→3 easy',
         'T4 2→3 HARD, has easy rival', 'T5 1→4 medium (alt. route)', 'T6 4→3 medium (alt. route)']
COL = {0: '#888888', 1: '#1f77b4'}; LAB = {0: 'Social learning only', 1: 'Social + practice'}
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
out = open(F+'summary_tables.md', 'w')
def load(n):
    p = R+n+'.json'
    return json.load(open(p)) if os.path.exists(p) else None
def pick(res, **kw):
    return [r for r in res if all(r['setting'].get(k) == v for k, v in kw.items())]
def ci(a):
    a = np.asarray(a, float); return a.mean(), 1.96*a.std(ddof=1)/np.sqrt(len(a)) if len(a) > 1 else 0

# ---------- Fig 1: the Real map ----------
fig, ax = plt.subplots(figsize=(7, 3.2))
pos = {0: (0, 0), 1: (1.4, 0), 2: (2.8, .6), 4: (2.8, -.6), 3: (4.2, 0)}
lab = {0: 's0\nnodule', 1: 's1\nplatform', 2: 's2\nroughed-out', 4: 's4\nalt. rough-out', 3: 's3\nFINISHED'}
for s, (x, y) in pos.items():
    ax.add_patch(plt.Circle((x, y), .33, fc='#f2f2f2' if s != 3 else '#d9f0d3', ec='k'))
    ax.text(x, y, lab[s], ha='center', va='center', fontsize=8)
edges = [(0, 1, 'T0 easy τ=10\nT1 easy τ=10', 0), (1, 2, 'T2 HARD τ=4', 0), (2, 3, 'T3 easy τ=10\nT4 HARD τ=4', 0),
         (1, 4, 'T5 medium τ=6', 0), (4, 3, 'T6 medium τ=6', 0)]
for a, b, t, _ in edges:
    (x0, y0), (x1, y1) = pos[a], pos[b]
    d = np.hypot(x1-x0, y1-y0); ux, uy = (x1-x0)/d, (y1-y0)/d
    ax.annotate('', xy=(x1-ux*.35, y1-uy*.35), xytext=(x0+ux*.35, y0+uy*.35), arrowprops=dict(arrowstyle='->'))
    ax.text((x0+x1)/2, (y0+y1)/2+(.28 if y1 >= y0 else -.28), t, ha='center', va='center', fontsize=7.5, color='#333')
ax.set_xlim(-.5, 4.7); ax.set_ylim(-1.2, 1.2); ax.axis('off')
ax.set_title('Fig. 1. The Real map: states, techniques and tolerances (defaults)', fontsize=10)
fig.tight_layout(); fig.savefig(F+'fig1_real_map.png', dpi=200); plt.close()

# ---------- Fig 2 + 3: main experiment ----------
main = load('main')
if main:
    fig, axs = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    t = np.arange(len(main[0]['surv_t']))*1000
    for ax, (js, ttl) in zip(axs, [([0, 1], 'Easy twins T0/T1 (mean)'), ([2], 'T2 hard, unavoidable'),
                                  ([3], 'T3 easy, last step'), ([4], 'T4 hard, has easy rival')]):
        for p in (0, 1):
            rs = pick(main, hard=4.0, practice=p)
            if not rs: continue
            Y = np.array([np.array(r['surv_t'])[:, js].mean(1) for r in rs])
            m = Y.mean(0); e = 1.96*Y.std(0, ddof=1)/np.sqrt(len(Y))
            ax.plot(t, m, color=COL[p], label=LAB[p]); ax.fill_between(t, m-e, m+e, color=COL[p], alpha=.2)
        ax.set_title(ttl, fontsize=9); ax.set_xlabel('time step')
    axs[0].set_ylabel('share of agents holding technique'); axs[0].legend(fontsize=8)
    fig.suptitle('Fig. 2. Technique survival over time (hard τ = 4, 20 runs, mean ± 95% CI)', fontsize=10)
    fig.tight_layout(); fig.savefig(F+'fig2_survival_time.png', dpi=200); plt.close()

    hs = sorted({r['setting']['hard'] for r in main})
    fig, axs = plt.subplots(1, 4, figsize=(12, 3))
    out.write('## E1 main experiment: end survival (mean of last 5 records), 20 runs, mean ± 95% CI\n\n')
    out.write('| hard τ | condition | ' + ' | '.join(f'T{j}' for j in range(7)) + ' | completion | route via hard |\n|' + '---|'*11 + '\n')
    for ax, (key, ttl) in zip(axs, [(2, 'T2 hard, unavoidable'), (4, 'T4 hard, has easy rival'), (3, 'T3 easy, last step'), ('comp', 'Stones finished')]):
        for p in (0, 1):
            m, e = [], []
            for h in hs:
                rs = pick(main, hard=h, practice=p)
                if not rs: m.append(np.nan); e.append(0); continue
                v = [r['comp'] for r in rs] if key == 'comp' else [r['surv'][key] for r in rs]
                a, b = ci(v); m.append(a); e.append(b)
            ax.errorbar(hs, m, yerr=e, color=COL[p], marker='o', capsize=3, label=LAB[p])
        ax.set_title(ttl, fontsize=9); ax.set_xlabel('tolerance of hard techniques (τ)')
    axs[0].set_ylabel('end survival'); axs[3].set_ylabel('completion rate'); axs[0].legend(fontsize=8)
    fig.suptitle('Fig. 3. H1 and H2: survival against difficulty, with and without practice', fontsize=10)
    fig.tight_layout(); fig.savefig(F+'fig3_tolerance.png', dpi=200); plt.close()
    for h in hs:
        for p in (0, 1):
            rs = pick(main, hard=h, practice=p)
            if not rs: continue
            S = np.array([r['surv'] for r in rs])
            cells = [f'{S[:,j].mean():.2f}±{1.96*S[:,j].std(ddof=1)/np.sqrt(len(S)):.2f}' for j in range(7)]
            out.write(f'| {h} | {LAB[p]} | ' + ' | '.join(cells) + f" | {np.mean([r['comp'] for r in rs]):.3f} | {np.nanmean([r['route'] for r in rs]):.2f} |\n")
    out.write('\n')

# ---------- Fig 4: noise ----------
noise = load('noise')
if noise:
    Ws = sorted({r['setting']['W'] for r in noise}); Os = sorted({r['setting']['sobs'] for r in noise})
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.2))
    mats = []
    for p in (0, 1):
        M = np.full((len(Ws), len(Os)), np.nan)
        for i, w in enumerate(Ws):
            for k, o in enumerate(Os):
                rs = pick(noise, W=w, sobs=o, practice=p)
                if rs: M[i, k] = np.mean([r['surv'][2] for r in rs])
        mats.append(M)
    for ax, M, ttl, cm, vr in zip(axs, [mats[0], mats[1], mats[1]-mats[0]],
                                  ['T2 survival: social only', 'T2 survival: + practice', 'Practice benefit (difference)'],
                                  ['viridis', 'viridis', 'RdBu'], [(0, 1), (0, 1), (-1, 1)]):
        im = ax.imshow(M, origin='lower', cmap=cm, vmin=vr[0], vmax=vr[1])
        ax.set_xticks(range(len(Os))); ax.set_xticklabels(Os); ax.set_yticks(range(len(Ws))); ax.set_yticklabels(Ws)
        ax.set_xlabel('perception noise σ_obs'); ax.set_ylabel('motor noise W'); ax.set_title(ttl, fontsize=9)
        for i in range(len(Ws)):
            for k in range(len(Os)):
                if not np.isnan(M[i, k]): ax.text(k, i, f'{M[i,k]:.2f}', ha='center', va='center', fontsize=8, color='w' if cm == 'viridis' and M[i, k] < .5 else 'k')
        plt.colorbar(im, ax=ax, fraction=.046)
    fig.suptitle('Fig. 4. Where does practice help the unavoidable hard step? (10 runs per cell)', fontsize=10)
    fig.tight_layout(); fig.savefig(F+'fig4_noise.png', dpi=200); plt.close()
    out.write('## E2 noise sweep: T2 survival (social | practice), 10 runs\n\n| W \\ σ_obs | ' + ' | '.join(map(str, Os)) + ' |\n|' + '---|'*(len(Os)+1) + '\n')
    for i, w in enumerate(Ws):
        out.write(f'| {w} | ' + ' | '.join(f'{mats[0][i,k]:.2f} → {mats[1][i,k]:.2f}' for k in range(len(Os))) + ' |\n')
    out.write('\n')

# ---------- Fig 5: OFAT sensitivity ----------
ofat = load('ofat')
if ofat:
    keys = []
    for r in ofat:
        k = {a: b for a, b in r['setting'].items() if a != 'practice'}
        if k not in keys: keys.append(k)
    rows = []
    for k in keys:
        v = []
        for p in (0, 1):
            rs = [r for r in ofat if {a: b for a, b in r['setting'].items() if a != 'practice'} == k and r['setting']['practice'] == p]
            v.append((np.mean([r['surv'][2] for r in rs]), np.mean([r['surv'][4] for r in rs]), np.mean([r['comp'] for r in rs]), len(rs)))
        lab = 'baseline' if not k else ', '.join(f'{a}={b}' for a, b in k.items())
        rows.append((lab, v))
    fig, axs = plt.subplots(1, 2, figsize=(10, .32*len(rows)+1.2), sharey=True)
    y = np.arange(len(rows))
    for ax, idx, ttl in [(axs[0], 0, 'T2 (hard, unavoidable)'), (axs[1], 1, 'T4 (hard, has easy rival)')]:
        ax.barh(y-.2, [r[1][0][idx] for r in rows], .4, color=COL[0], label=LAB[0])
        ax.barh(y+.2, [r[1][1][idx] for r in rows], .4, color=COL[1], label=LAB[1])
        ax.axvline(rows[0][1][0][idx], color=COL[0], ls=':'); ax.axvline(rows[0][1][1][idx], color=COL[1], ls=':')
        ax.set_title(ttl, fontsize=9); ax.set_xlabel('end survival'); ax.set_xlim(0, 1)
    axs[0].set_yticks(y); axs[0].set_yticklabels([r[0] for r in rows], fontsize=8); axs[0].invert_yaxis(); axs[0].legend(fontsize=8, loc='lower right')
    fig.suptitle('Fig. 5. One-factor-at-a-time sensitivity (8 runs each; dotted = baseline)', fontsize=10)
    fig.tight_layout(); fig.savefig(F+'fig5_ofat.png', dpi=200); plt.close()
    out.write('## E3 OFAT sensitivity (8 runs): T2 social→practice | T4 social→practice | completion social→practice\n\n| setting | T2 | T4 | completion |\n|---|---|---|---|\n')
    for lab, v in rows:
        out.write(f'| {lab} | {v[0][0]:.2f} → {v[1][0]:.2f} | {v[0][1]:.2f} → {v[1][1]:.2f} | {v[0][2]:.3f} → {v[1][2]:.3f} |\n')
    out.write('\n')

# ---------- robustness ----------
rob = load('robust')
if rob:
    out.write('## E4 robustness (10 runs): end survival T0..T6\n\n| setting | ' + ' | '.join(f'T{j}' for j in range(7)) + ' |\n|' + '---|'*8 + '\n')
    seen = []
    for r in rob:
        if r['setting'] in seen: continue
        seen.append(r['setting']); rs = [q for q in rob if q['setting'] == r['setting']]
        S = np.array([q['surv'] for q in rs])
        out.write(f"| {r['setting']} | " + ' | '.join(f'{S[:,j].mean():.2f}' for j in range(7)) + ' |\n')
    out.write('\n')

# ---------- Fig 6: global uncertainty (LHS) ----------
lhs = load('lhs')
if lhs and len(lhs) >= 20:
    pars = ['W', 'sobs', 'smat', 'eta_P', 'beta', 'hard']
    pts = {}
    for r in lhs:
        key = tuple(round(r['setting'][p], 6) for p in pars)
        pts.setdefault(key, {})[r['setting']['practice']] = r
    pts = [(k, v) for k, v in pts.items() if 0 in v and 1 in v]
    X = np.array([k for k, _ in pts]); d2 = np.array([v[1]['surv'][2]-v[0]['surv'][2] for _, v in pts])
    s0 = np.array([v[0]['surv'][2] for _, v in pts])
    def prcc(X, y):
        Xr = np.column_stack([rankdata(c) for c in X.T]); yr = rankdata(y); res = []
        for i in range(X.shape[1]):
            o = np.column_stack([np.ones(len(y)), np.delete(Xr, i, 1)])
            ex = Xr[:, i]-o@np.linalg.lstsq(o, Xr[:, i], rcond=None)[0]; ey = yr-o@np.linalg.lstsq(o, yr, rcond=None)[0]
            res.append(np.corrcoef(ex, ey)[0, 1])
        return res
    pc_d = prcc(X, d2); pc_s = prcc(X, s0)
    fig, axs = plt.subplots(1, len(pars), figsize=(13, 2.8), sharey=True)
    for i, (ax, p) in enumerate(zip(axs, pars)):
        ax.scatter(X[:, i], d2, s=12, color=COL[1]); ax.axhline(0, color='k', lw=.6)
        ax.set_xlabel(p); ax.set_title(f'PRCC = {pc_d[i]:+.2f}', fontsize=8)
    axs[0].set_ylabel('practice benefit\non T2 survival')
    fig.suptitle(f'Fig. 6. Global uncertainty: practice benefit on T2 across {len(d2)} Latin-hypercube parameter sets', fontsize=10)
    fig.tight_layout(); fig.savefig(F+'fig6_lhs.png', dpi=200); plt.close()
    out.write(f'## E5 Latin hypercube ({len(d2)} parameter sets)\n\nPractice benefit on T2: mean {d2.mean():.2f}, positive in {(d2>0).mean()*100:.0f}% of sets, '
              f'5th–95th percentile [{np.percentile(d2,5):.2f}, {np.percentile(d2,95):.2f}]\n\n| parameter | PRCC with practice benefit | PRCC with social-only T2 survival |\n|---|---|---|\n')
    for p, a, b in zip(pars, pc_d, pc_s):
        out.write(f'| {p} | {a:+.2f} | {b:+.2f} |\n')
out.close()
print(open(F+'summary_tables.md').read())
