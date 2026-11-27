# Narration script, V2

**Talk:** 7:45 planned, about 775 spoken words. You are the voice; the screen is the picture.

## How to read it

- **▶** press the clicker; the line after it belongs to that press.
- **/** short pause (half a second); **//** long pause (1–2 seconds).
- ***word*** lean on it.
- **(…)** what to wait for on screen, or how to deliver it. Don't read it aloud.
- **Tone changes:** stay silent through each light/dark dissolve (about 2 seconds). Breathe, and arrive in the new voice.

- **Campfire:** Low, slow (about 110 words a minute), close and intimate, present tense. Read each on-screen line with the type as it appears. Let silence work.
- **Daylight:** Brighter and brisker (about 150 words a minute), a warm museum guide. Say each number once, slowly, and let the screen carry the rest.

## 1. Cold open  ·  Campfire  ·  0:55 (ends at 0:55)

(Dark. Wait until the stone glows and the first flake flies.) **3.3 million years ago** / someone struck a stone. //

▶ (The clock fills.) Fold all of it / into a single day. // For *ninety-nine point six percent* of that day / this was our technology. / Farming arrives at six minutes to midnight.

▶ A handful of strikes / in the *right order*.

▶ Goals inside goals. / Prepare a platform. Rough out. Thin. / A tool / like a sentence / is built from nested parts.

▶ We shaped stone. // And stone *may have* shaped us. / Our hands. Our brains. Perhaps even language.

▶ None of it is in our genes. / (The Elder. The Apprentice. The Child.) Every generation had to learn it *again*. // (Let the stone pass hand to hand.) And some steps / are far harder to learn than others.

> If asked: Hedges are part of the science: “may have”, “perhaps”. Greenfield 1991; Stout 2011; Arbib et al. 2023 (the language link is debated); Stout & Chaminade 2012. 99.6%: the Palaeolithic ends about 12,000 years ago, which is 0.36% of 3.3 million years. Farming at 23:54, writing at 23:57.

## 2. Title  ·  Daylight  ·  0:10 (ends at 1:05)

(Let the morning come up: the chalk cliff, three people at a flint scatter. Then, warmly:) Good morning. / At mid-sem I ended on this line: / *now, try it yourself*. / Today / I built that idea / and ran it.

> If asked: The AI-use line now matches Appendix E of the report word for word in substance. If asked: I designed the questions and the V1 model; Claude helped implement, test, run, plot and draft from my design; I checked everything and can walk through any part of the code.

## 3. The question  ·  Daylight  ·  0:25 (ends at 1:30)

A stone tool is a *chain* of strikes. / And some links leave a much narrower window for error.

▶ So, two questions. / One: if a skill is passed on *only by watching*, / are the hard steps lost first?

▶ Two: / can *practice* / trial and error on your own / rescue them?

## 4. Work done  ·  Daylight  ·  0:30 (ends at 2:00)

In September I planned to build the model by November / and run it in the spring.

▶ (The timeline.) Everything up to and including the experiments / is *done*.

▶ The full model: fifty agents, seven techniques, and a physical world that judges every strike. / Twelve verification tests, / one of which caught a real artefact. / And nine hundred seeded runs.

> If asked: This slide carries the Work Done marks: do not rush it. Padum ran the F&S replication; confirm before the talk whether V1 itself ran there.

## 5. Interlude · Inside one tick  ·  Campfire  ·  1:30 (ends at 3:30)

(Silence through the dissolve. Read each line with the type as it appears.) *Inside the model.* / One tick / slowed right down. / Agent A / call him the Elder / holds a prepared stone.

▶ First, the agent chooses where to aim. / The hard route has served it well, / so it has a sixty percent chance of taking it.

▶ It practises. / The stone judges every try. / Five attempts. / Only *one* lands inside the window. / The belief moves ten percent towards it.

▶ Then it strikes / for real.

▶ The stone decides. // Inside the window / it moves on.

▶ A neighbour watches. / The Apprentice. / But sees it *blurred*. / He never sees what the Elder *meant* to do / only what happened.

▶ (His own stone, his own hands.) *Which of my beliefs was that?* / Eighty-two percent the first. / Eighteen, the second.

▶ And it learns. / A little.

▶ (The Elder sets the handaxe down.) Then he may die, / and a newcomer starts with nothing. // That is one tick. / Fifty agents. / Forty thousand ticks.

> If asked: Why only successes: people copy success far more than failure (Nakawake & Kobayashi 2022). δ = √(W² + σ_obs²), matched to copying noise (Truskanov & Prat 2018). The learning rule is Falandays & Smaldino's, unchanged.

## 6. Analysis · from runs to numbers  ·  Daylight  ·  0:50 (ends at 4:20)

(Lights up. A breath. Then brisker, a guide:) So what did I measure? / Every thousand ticks / I count who still *holds* each technique. / Here, at the end of one run: / twenty-three of fifty.

▶ Forty-one records make one run. / I summarise a run by its last five: / point five two.

▶ Twenty seeds per setting. / Copying alone: *point one two*. / With practice: *point five three*.

▶ And the number I care about / is the gap. // *Plus point four one.* / The practice benefit.

> If asked: “Holds” = a belief within τ of the real target with weight ≥ 0.1. 95% CI = 1.96·SD/√20. τ = 4, real data; the run shown is the one closest to the mean. Last five records = ticks 36,000–40,000; E4 doubles the run length to check the steady state.

## 7. Analysis · five experiments  ·  Daylight  ·  0:25 (ends at 4:45)

Eight hundred and ninety-six runs / five questions. / Does the hard step die, and does practice save it? / Does noise change that? / Can any single assumption flip it? / Is it an artefact? / And when *everything* varies at once / what drives the gain?

> If asked: E1 200, E2 180, E3 336, E4 60, E5 120. PRCC = rank correlation of one input with the output after removing the others' ranked effects. No significance tests: in a simulation n is a free choice, so I report effect sizes with CIs. E3 uses 8 seeds, so its CIs are wider (about ±0.08); it is read for direction, not size.

## 8. Result 1 · H1  ·  Daylight  ·  0:40 (ends at 5:25)

Hypothesis one. / Copying alone, / over about four lifetimes.

▶ (Let it play. Speak over the second half.) Watch the hard step thin. / *Point one two* at our default difficulty. / Point zero two at the narrowest.

▶ And look at T3. / It's easy / but it dies too, / because almost no stone gets past T2 to show it. / A *cascade*. / Fewer than one in a hundred tools / ever finished.

> If asked: Two mechanisms: fewer successful demonstrations, and blurred copying drifts out of a narrow window sooner. With immortal agents, T2 still falls to 0.74 from copying drift alone (test V7).

## 9. Result 2 · H2  ·  Daylight  ·  0:35 (ends at 6:00)

Now / add practice.

▶ (Let it play.) The decline *stops*. / Point one two becomes point five three. / Finished tools: from half a percent / to eight. / Hypothesis two / holds.

▶ But the top row. // At the narrowest window: / almost nothing.

> If asked: In 80,000-tick runs practice holds T2 at 0.73 while copying alone falls to 0.01.

## 10. Interlude · Why practice fails  ·  Campfire  ·  1:00 (ends at 7:00)

(Silence through the dissolve. The Apprentice, alone at the fire. Low, almost to yourself.) Look at the ground around him. // Every one of those / is a strike that failed. // *Why can practice not save the hardest steps?*

▶ (He strikes in time with the chart. Speak with him, not over him.) Practice only learns / from a strike that *works*. // Strike. Shatter. / Strike. Shatter. // (The flake.) *There.* / One clean flake. / About one try in five. / That flake / is the only thing he learns from.

▶ Now narrow the window. // Strike. / Shatter. / Strike. / Shatter. // Three and a half percent. / He can practise all night / and have nothing to learn from.

▶ And practice cannot make anyone *choose* the hard way. / Practice makes you *better* at a technique. / But what you *pick* follows what you've seen *succeed*, / and the easy rival succeeds more often. / So the hard way is rarely chosen, / rarely practised, / and it fades.

> If asked: The strike sequence is illustrative; the rates are the model's (χ² from W, σ_mat, δ). “Isn't limit 2 a design choice?” Yes: practice doesn't touch weights. That is the next extension.

## 11. How sure, and what it means  ·  Daylight  ·  0:35 (ends at 7:35)

(Lights up. Measured, confident.) How sure am I? / Practice helped in *all twenty* one-factor variations / and in ninety-eight percent of sixty randomly drawn parameter sets. / What decides how much it helps? / The step's difficulty.

▶ So: / practice protects hard skills. / But not the *hardest*, / and not those with an easy substitute.

▶ Next: / teaching, / practice that changes choice, / and real knapping data.

> If asked: Contribution: a boundary condition on Truskanov & Prat 2018. Prediction: in a declining craft, the steps lost despite practice are the most precise ones.

## 12. Thank you  ·  Daylight  ·  0:10 (ends at 7:45)

(Morning again: the Elder's hands around the Child's. Slow, almost quiet.) Watch. / Then try it yourself. // But for the hardest steps, / someone has to help you *succeed first*. // Thank you.

> If asked: Backup slides follow (→): the live strike window, sensitivity and noise, verification, limitations.
