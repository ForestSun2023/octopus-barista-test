# Octopus Barista Test

[中文](README.md) · [English](README.en.md)

A single-prompt benchmark that probes an AI coding agent's **spatial reasoning, multi-constraint execution and code generation**. Inspired by the Pelican Test (asking a model to draw a pelican riding a bicycle).

> Same model, same prompt, different agent tools — see who actually gets all eight tentacles to do their job.

## What makes it harder than the Pelican Test

The Pelican Test mainly checks whether two objects (bird, bicycle) are put together correctly. This one concentrates the pressure on four things:

| Aspect | What it probes |
| --- | --- |
| Visual structure | Can it represent eight tentacles and several independent objects at once? |
| Spatial reasoning | Do contact, support, direction and occlusion actually make sense? |
| Multi-constraint execution | Does it satisfy every requirement, not just the most obvious one? |
| Code generation | Is the output valid, self-contained, renderable SVG? |

Drawing eight tentacles is not the hard part. The hard part is **giving every tentacle a different job while keeping the whole scene spatially coherent**.

## The prompt

The full prompt is in [prompt.md](prompt.md) (currently v2). Paste it verbatim; no extra tool instructions are needed.

The 2026-10-13 run in this repository used [prompts/v1.md](prompts/v1.md). v2 only adds a constraint forbidding labels or arrows in place of actual drawing.

## Scoring

Two steps: compute the total from the **four weighted categories** below, then verify item by item against the **10-point checklist**.

| Category | Max | Covers |
| --- | --- | --- |
| Instruction completion | 5 | Eight tentacles, the four specified actions, remaining limbs present |
| Space and interaction | 2 | Grips, pouring, button contact, cup and scale relationships |
| Composition and visual expression | 2 | Occlusion, perspective, proportion, legibility, detail |
| SVG engineering | 1 | Valid XML, self-contained, renders correctly |

> The total is *not* the sum of the 10 checklist items — a binary checklist can only produce integers, while this run's 9.5 / 8.3 / 7.8 come from the weighting above.
> Where the checklist and the weighting disagree, and which criteria the checklist is missing, are documented in [results/EVIDENCE.md](results/EVIDENCE.md).

### The 10-point checklist

Only "SVG engineering" can be judged automatically; the other nine are human judgement. Human items must be backed by evidence found **in the rendered image**, not by the model's own description.

| # | Item | Judged | Passes when |
| --- | --- | --- | --- |
| 1 | SVG engineering | 🤖 auto | Valid, has a viewBox, self-contained, no raster/base64/external assets |
| 2 | Tentacle count | 👁 human | Exactly eight, clearly distinguishable |
| 3 | Object grip | 👁 human | Tentacle-to-portafilter-handle contact is plausible |
| 4 | Liquid flow | 👁 human | Milk flows continuously into the cup, not into mid-air or outside |
| 5 | Button interaction | 👁 human | A tentacle actually touches the espresso machine button |
| 6 | Pointing | 👁 human | A tentacle clearly points at the wall clock |
| 7 | Cup and scale | 👁 human | The cup sits directly on the digital scale |
| 8 | Scene support | 👁 human | Machine and scale both rest on the countertop |
| 9 | Limb connection | 👁 human | The remaining four tentacles are visible and connected to the body |
| 10 | Spatial relations | 👁 human | Occlusion is consistent, objects do not visibly interpenetrate |

Item 1 is enforced by CI on every push. Run it locally before submitting (see [CONTRIBUTING.md](CONTRIBUTING.md)):

```bash
node scripts/check-svg.mjs
```

### Evidence rules for the human items

All nine must be checked against the rendered image. "Looks about right" does not count:

| Item | Passes when |
| --- | --- |
| Tentacle count | You can number all 8 tentacles starting from the body without ever hesitating over whether something is one tentacle or two |
| Object grip | The handle shape and the tentacle tip are touching; "near" does not count |
| Liquid flow | The milk stream is one continuous path ending inside the cup rim; a break, or landing outside the cup, fails |
| Button interaction | The tentacle tip is on the button shape, not beside it |
| Pointing | The tentacle's axis extended passes through the clock face |
| Cup and scale | The cup base meets the scale platform with no countertop visible between them |
| Scene support | The bottom edges of the machine and scale coincide with the countertop line |
| Limb connection | The four remaining tentacles start at the body, not from off-screen |
| Spatial relations | Occlusion is consistent: one tentacle cannot be both in front of and behind the machine |

**Principle**: a pretty drawing does not earn points. Gorgeous artwork with only six tentacles, or milk pouring outside the cup, still loses points.

## Results of this run

Model **DeepSeek-V4.1-Flash**, five different agent tools, one generation each, same prompt.

| Rank | Agent tool | Work | Score | One-line note |
| --- | --- | --- | --- | --- |
| 1 | ZCode | [zcode.svg](results/zcode.svg) | **9.5** | Richest detail, complete spatial structure, eight tentacles clearly differentiated |
| 2 | ChatGPT | [chatgpt.svg](results/chatgpt.svg) | **9.4** | Balanced composition, natural depth, high task completion |
| 3 | WorkBuddy | [workbuddy.svg](results/workbuddy.svg) | **9.2** | Excellent instruction following, clear action relationships, but diagram-like |
| 4 | DeepSeek Harness | [deepseek-harness.svg](results/deepseek-harness.svg) | **8.3** | Main structure complete, but some tentacles overlap and depth is weak |
| 5 | Claude | [claude.svg](results/claude.svg) | **7.8** | Clean composition, but no clear grip between the milk pitcher and the tentacle |

Blind review (works anonymised A–E, the evaluator did not know the mapping): [results/BLIND.md](results/BLIND.md) — **all five scored 10/10**, so this checklist is saturated on this batch and cannot rank them.

Full commentary and per-item evidence: [results/SCORES.md](results/SCORES.md) and [results/EVIDENCE.md](results/EVIDENCE.md).
Run environment and artefact sizes: [results/MANIFEST.md](results/MANIFEST.md).

### Preview

| **#1 ZCode · 9.5** | **#2 ChatGPT · 9.4** |
| --- | --- |
| ![ZCode](results/zcode.webp) | ![ChatGPT](results/chatgpt.webp) |
| **#3 WorkBuddy · 9.2** | **#4 DeepSeek Harness · 8.3** |
| ![WorkBuddy](results/workbuddy.webp) | ![DeepSeek Harness](results/deepseek-harness.webp) |
| **#5 Claude · 7.8** | |
| ![Claude](results/claude.webp) | |

Open [index.html](index.html) in a browser for the gallery — static, no build step, works as-is on GitHub Pages.

## Repository layout

```
prompt.md                The prompt, v2 — copy and paste
prompts/v1.md            Frozen v1, the version this run used
README.en.md             English
CONTRIBUTING.md          Submission requirements and blind review method
results/*.svg            Each agent tool's output (the only artefact that is scored)
results/MANIFEST.md      Run record: environment, artefact sizes, known gaps
results/SCORES.md        Scoring basis and per-work commentary
results/EVIDENCE.md      Per-item evidence and review findings
results/BLIND.md         Blind review result and rank comparison
scripts/check-svg.mjs    Self-containment check, run by CI and before submitting
scripts/render.mjs       SVG to PNG, for previews
scripts/<agent>/         Scripts the agents left behind; reference only
index.html               Gallery
```

## Running it yourself

1. Start a fresh agent session and paste the prompt from [prompt.md](prompt.md) verbatim.
2. Save the returned SVG, render it, and check it item by item against the checklist above — **structure first, beauty second**.
3. Prefer three independent runs per agent tool and compare the mean and minimum, not a single result.

## Notes

- This repository includes results from five agent tools only.
- A single run does not represent the overall ability of an agent tool or a model, and cannot be used to conclude that an API has been "nerfed". Model output is stochastic; prompt, reasoning effort and runtime all matter.
- CI runs `node scripts/check-svg.mjs` on every push; any invalid SVG, or one containing raster data, fails the build.
- The scripts under `scripts/<agent>/` were left behind during generation. Their style and quality vary widely; they are not part of the test and are not scored. `scripts/check-svg.mjs` and `scripts/render.mjs` are the exception — they are tooling, not outputs.

## License

MIT — see [LICENSE](LICENSE). Author: [@ForestSun2023](https://github.com/ForestSun2023).
