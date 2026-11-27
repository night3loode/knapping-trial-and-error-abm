# Narration script, V3

**Talk:** 7:57 planned, about 998 spoken words. You are the voice; the screen is the picture.

## How to read it

- **▶** press the clicker; the line after it belongs to that press.
- **/** short pause (half a second); **//** long pause (1–2 seconds).
- ***word*** lean on it.
- **(…)** what to wait for on screen, or how to deliver it. Don't read it aloud.
- **Tone changes:** stay silent through each light/dark dissolve (about 2 seconds). Breathe, and arrive in the new voice.

- **Campfire:** Low, slow (about 110 words a minute), close and intimate, present tense. Read each on-screen line with the type as it appears. Let silence work.
- **Daylight:** Brighter and brisker (about 150 words a minute), a warm museum guide. Say each number once, slowly, and let the screen carry the rest.

## 1. Cold open  ·  Campfire  ·  0:55 (ends at 0:55)

(Dark. Let the stone glow and the first flake fly before you speak.) Three point three million years ago, someone struck one stone with another. //

▶ (The clock fills.) Fold all of that time into a single day, and for ninety-nine point six percent of it, this was our technology; farming arrives at six minutes to midnight.

▶ A tool like this takes a handful of strikes, each in the right place and in the right order.

▶ It has goals inside goals: prepare a platform, rough out the shape, then thin it, so the tool is built from nested parts, much like a sentence.

▶ We shaped stone, and stone may well have shaped us in return: our hands, our brains, perhaps even language.

▶ (The Elder, the Apprentice, the Child.) None of this is in our genes, so every generation has had to learn it again. // (Let the stone pass from hand to hand.) And some of its steps are far harder to learn than others.

> If asked: The hedges are part of the science, so keep “may have” and “perhaps”. Greenfield 1991; Stout 2011; Arbib et al. 2023 (the link to language is still debated); Stout & Chaminade 2012. 99.6%: the Palaeolithic ends about 12,000 years ago, which is 0.36% of 3.3 million years. On the 24-hour clock, farming arrives at 23:54 and writing at 23:57.

## 2. Title  ·  Daylight  ·  0:12 (ends at 1:07)

(Let the morning come up. Then, warmly:) Good morning. At mid-sem I ended on one line, now, try it yourself, and today I'll show you what happened when I built that idea into a model and ran it.

> If asked: AI use is on the slide. If asked: the question, the model design, the analysis and the interpretation are mine; Claude helped with coding, editing text, refining content and building this presentation. I use it deliberately, as an AI-native researcher: it let me build and present this at this quality and speed.

## 3. The question  ·  Daylight  ·  0:27 (ends at 1:34)

A stone tool is made through a chain of strikes, and some links in that chain leave far less room for error than others.

▶ So my first question is this: if a skill like this is passed on only by watching other people, are the hardest steps the first to disappear?

▶ And my second question follows from it: can practice, meaning trial and error on your own, rescue those steps before they are lost?

## 4. Work done  ·  Daylight  ·  0:32 (ends at 2:06)

In September, my plan was to build the model by November and run the experiments in the spring.

▶ (The timeline.) As you can see, everything up to and including those experiments is now done.

▶ That is the full model, with fifty agents, seven techniques and a world that judges every strike; twelve verification tests, one of which caught a real artefact; and nearly nine hundred seeded runs.

> If asked: This slide carries the Work Done marks, so do not rush it. Padum ran the F&S replication; the V1 runs took about 1.5 hours on one CPU core.

## 5. Interlude · Inside one tick  ·  Campfire  ·  1:30 (ends at 3:36)

(Silence through the dissolve. Read each line as it types out, then carry on.) Let's go inside the model and slow one tick right down. Agent A, call him the Elder, holds a prepared stone.

▶ First, the Elder chooses where to aim. The hard route has served him well so far, so there is about a sixty percent chance that he takes it.

▶ Then he practises, and the stone judges every try: of five attempts only one lands inside the window, so his belief moves ten percent towards it.

▶ Now he strikes for real, with his belief plus a little motor noise.

▶ And the stone decides. // The strike falls inside the window, so the stone moves on to the next stage.

▶ A neighbour, the Apprentice, is watching, but he sees the strike blurred, and never what the Elder meant to do, only what happened.

▶ (His own stone, his own hands.) So he asks which of his own beliefs that strike was an example of: about eighty-two percent the first, eighteen percent the second.

▶ And he learns from it, but only a little, nudging both beliefs towards what he saw.

▶ (The Elder sets the handaxe down.) Finally, the Elder may die, and a newcomer takes his place with nothing. // That is one tick, and the model runs fifty agents through forty thousand of them.

> If asked: Why only successes: people copy success far more than failure (Nakawake & Kobayashi 2022). δ = √(W² + σ_obs²), matched to copying noise (Truskanov & Prat 2018). The learning rule is Falandays & Smaldino's, unchanged.

## 6. Analysis · from runs to numbers  ·  Daylight  ·  0:50 (ends at 4:26)

(Lights up. A breath, then as a guide:) So what did I measure? Every thousand ticks I count how many agents still hold each technique, and at the end of this run, twenty-three of fifty do.

▶ That gives forty-one records per run, and since one record is noisy, I average the last five, which here is point five two.

▶ Each setting runs with twenty seeds: copying alone ends at point one two, and with practice, at point five three.

▶ And the number I care about is the gap, plus point four one: the benefit of practice.

> If asked: “Holds” = a belief within τ of the real target with weight ≥ 0.1. 95% CI = 1.96·SD/√20. τ = 4, real data; the run shown is the one closest to the mean. Last five records = ticks 36,000 to 40,000; E4 doubles the run length to check the steady state.

## 7. Analysis · five experiments  ·  Daylight  ·  0:25 (ends at 4:51)

Eight hundred and ninety-six runs across five experiments, each asking one question: does the hard step die and does practice save it, does noise change that, can any one assumption flip it, is it an artefact, and when everything varies at once, what drives the gain?

> If asked: E1 200, E2 180, E3 336, E4 60, E5 120. PRCC = rank correlation of one input with the output after removing the others' ranked effects. No significance tests: in a simulation n is a free choice, so I report effect sizes with confidence intervals. E3 uses 8 seeds, so its intervals are wider (about ±0.08); read it for direction, not size.

## 8. Result 1 · H1  ·  Daylight  ·  0:42 (ends at 5:33)

Here is the first hypothesis, with copying alone, over roughly four lifetimes.

▶ (Let it play, and speak over the second half.) Watch the hard step thin out: it ends at point one two at our default difficulty, and at only point zero two when the window is at its narrowest.

▶ And look at T3: it's easy, yet it dies too, because almost no stone gets past T2 for anyone to show it. That's a cascade, and fewer than one tool in a hundred is ever finished.

> If asked: Two mechanisms: fewer successful demonstrations, and blurred copying drifts beliefs out of a narrow window sooner. With immortal agents, T2 still falls to 0.74 from copying drift alone (test V7).

## 9. Result 2 · H2  ·  Daylight  ·  0:36 (ends at 6:09)

Now let us add practice.

▶ (Let it play.) The decline stops: the hard step settles at point five three instead of point one two, and finished tools rise from half a percent to eight percent, so the second hypothesis holds.

▶ But look at the top row, because at the narrowest window, practice achieves almost nothing.

> If asked: In 80,000-tick runs practice holds T2 at 0.73 while copying alone falls to 0.01.

## 10. Interlude · Why practice fails  ·  Campfire  ·  1:02 (ends at 7:11)

(Silence through the dissolve. The Apprentice, alone at the fire. Low.) Look at the ground around him: every one of those fragments is a strike that failed. // So why can practice not save the hardest steps?

▶ (He strikes in time with the chart; speak with him, not over him.) Practice can only learn from a strike that works. Strike, and it shatters; strike again, and it shatters. // (The flake.) There: one clean flake, about one try in five, and that single flake is the only thing he can learn from.

▶ Now narrow the window. // Strike, shatter, strike, shatter. Only three and a half percent of attempts succeed, so he could practise all night and still have nothing to learn from.

▶ And practice cannot make anyone choose the hard way. It makes you better at a technique, but which one you pick depends on what you've seen succeed, and the easy rival succeeds more often, so the hard way is rarely chosen, rarely practised, and slowly fades.

> If asked: The strike sequence is illustrative; the rates are the model's (χ² from W, σ_mat, δ). “Isn't limit 2 a design choice?” Yes: in this version practice does not touch the weights, and that is the next extension.

## 11. How sure, and what it means  ·  Daylight  ·  0:36 (ends at 7:47)

(Lights up. Measured and confident.) How sure can we be? Practice helped in all twenty one-factor variations and in ninety-eight percent of sixty random parameter sets, and what decides how much it helps is how difficult the step is.

▶ So the answer is that practice protects hard skills, but not the very hardest ones, and not those that have an easier substitute.

▶ Next, I'll add teaching, let practice shape which technique people choose, and calibrate against real knapping data.

> If asked: Contribution: a boundary condition on Truskanov & Prat 2018. Prediction: in a declining craft, the steps lost despite practice are the most precise ones.

## 12. Thank you  ·  Daylight  ·  0:10 (ends at 7:57)

(Morning again: the Elder's hands around the Child's. Slow, almost quiet.) So watch, and then try it yourself. // But for the hardest steps, someone first has to help you succeed. // Thank you.

> If asked: Backup slides follow (→): the live strike window, sensitivity and noise, verification, limitations.
