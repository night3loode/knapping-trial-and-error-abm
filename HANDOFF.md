# Handoff: publish this repository to GitHub

**For:** Dhairya's coding agent (e.g. Claude Code) · **Owner:** Dhairya Yadav

## Goal

Put this folder on GitHub as a new repository so the SPL711 report can cite it and the examiner
can reproduce the results. Do not change the model, experiment or analysis code: the report's
numbers come from exactly this code. If something seems broken, stop and report it to Dhairya.

## Steps

1. **Ask Dhairya** which GitHub account to use and whether the repo should be **private** (default) or public.
   Suggested name: `knapping-trial-and-error-abm`.
2. Unzip the archive and `cd` into the folder.
3. Check nothing large or private is included:
   `find . -size +5M` should print nothing. There are no credentials, data files or HPC paths in the code.
4. Sanity check that the code runs (about 1 minute):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python tests/verify.py
   ```
   All lines should say PASS or print numbers; compare against `tests/verification_log.txt`.
5. Create and push:
   ```bash
   git init -b main
   git add .
   git commit -m "V1 knapping ABM: model, verification, experiments, results, figures"
   gh repo create <name> --private --source=. --push      # or --public if Dhairya says so
   ```
   Without the `gh` CLI: create an empty repo on github.com, then
   `git remote add origin https://github.com/<user>/<name>.git && git push -u origin main`.
6. Send Dhairya the repo URL. He will put it in the report's Method section and appendix.

## Optional (only if Dhairya asks)

- Add a licence (MIT is common for academic code).
- Add a GitHub Release / Zenodo DOI for a citable snapshot.
- Re-run all experiments (~1.5 h on one core): see README "Reproduce".

## What's in the repo

See README.md. In short: `model/` (the model), `tests/` (verification), `experiments/`
(all report experiments), `analysis/` (figures and tables), `results/` (raw JSON outputs),
`figures/`, `legacy/` (earlier F&S replication and Part D thesis code, for provenance).
