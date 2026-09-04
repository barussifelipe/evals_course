# Evals and LLM-as-Judge

This repository contains a complete, three-lesson course about detecting regressions in an AI feature. It is for developers who have already shipped an AI feature but do not yet have a reliable way to tell whether a new model, prompt, or release made it worse.

The course does more than explain evaluation concepts. Across three cumulative Jupyter build-alongs, the learner creates a small labeled evaluation set, replays an offline LLM judge, inspects where that judge disagrees with human labels, and measures the judge with a confusion matrix, precision, and recall.

Everything needed for the course is committed to the repository. The notebooks run offline and make no API calls, so no provider account, API key, model download, or paid service is required.

## What we built

The project has two connected parts:

1. **The course** — lesson text, editable notebooks, deterministic fixtures, generated artifacts, and completed notebook runs.
2. **The course factory** — a reusable Codex plugin that planned, researched, built, and cold-reviewed one lesson at a time while recording its decisions and evidence.

The learner-facing work forms one artifact pipeline:

```text
Lesson 01                    Lesson 02                         Lesson 03
label evaluation cases  ->  replay an offline judge      ->  measure the judge
eval_cases.jsonl             judge_predictions.jsonl          grader_report.json
```

The positive class is fixed throughout the course: `1` means the defined regression is present, and `0` means it is absent. Stable `case_id` values connect the files; the later notebooks join records by ID rather than assuming that rows remain in the same order.

The included ten-case run produces:

```text
TP=3  FP=1  FN=2  TN=4
precision=0.75
recall=0.6
```

### Lesson 01 — Make regressions measurable

The first lesson turns a vague quality concern into an explicit decision rule. The learner defines the regression and positive class, creates ten cases with stable IDs and human labels, validates their schema and class counts, and writes `build/lesson-01/eval_cases.jsonl`. The notebook creates or overwrites this file; it does not require the file to exist before Lesson 1 runs.

### Lesson 02 — Turn a rubric into judge predictions

The second lesson defines a bounded judge rubric and strict response contract. It replays committed responses instead of calling a live model, validates exact case coverage, aligns predictions by `case_id`, exposes human/judge disagreements, and writes `build/lesson-02/judge_predictions.jsonl`. The notebook creates or overwrites this prediction file; it requires the Lesson 1 cases and the cached judge responses, but it does not require `judge_predictions.jsonl` to exist before Lesson 2 runs.

### Lesson 03 — Measure the grader

The final lesson joins human labels and judge predictions, verifies that identities and copied labels agree, classifies every case as TP, FP, FN, or TN, and calculates precision and recall with an explicit zero-division policy. It persists the capstone as `build/lesson-03/grader_report.json`.

## Repository map

| Path | What is there | Who it is for |
| --- | --- | --- |
| `course/lesson-01.md` to `lesson-03.md` | The three lessons, including concepts, diagrams, checkpoints, and build-along guidance | Learners |
| `build/lesson-XX/lesson-XX.ipynb` | Editable, cumulative notebooks intended to run top-to-bottom | Learners and reviewers |
| `build/lesson-01/eval_cases.jsonl` | Ten labeled regression cases produced by Lesson 01 | Input to Lesson 02 |
| `build/lesson-02/cached_judge_responses.jsonl` | Deterministic stand-in for responses from a live LLM judge | Offline fixture for Lesson 02 |
| `build/lesson-02/judge_predictions.jsonl` | Parsed and aligned judge labels, human labels, and reasons | Input to Lesson 03 |
| `build/lesson-03/grader_report.json` | Final confusion-matrix counts, policies, precision, and recall | Course capstone |
| `build/lesson-XX/requirements.txt` | Python version note and pinned notebook dependencies | Setup |
| `output/lesson-XX/*.executed.ipynb` | Completed notebook runs with saved cell output | Reviewers who want to inspect results without executing code |
| `agent/evals-course-factory/` | Root of the reusable course-generation plugin | Developers inspecting or reusing the generation system |
| `agent/evals-course-factory/.codex-plugin/` | Plugin manifest: identity, version, capabilities, skill location, and interface metadata | Codex plugin loader |
| `agent/evals-course-factory/.codex/` | Local Codex hook configuration | Plugin/tooling configuration |
| `agent/evals-course-factory/.impeccable/` | Local configuration for the optional Impeccable UI-review hook | Local development tooling |
| `agent/evals-course-factory/config/` | Agent-to-skill, model, and reasoning-effort assignments | Orchestrator and maintainers |
| `agent/evals-course-factory/plugins/` | Personal marketplace entry used to expose the local plugin | Plugin installation/discovery |
| `agent/evals-course-factory/skills/` | Instructions for the orchestrator, searcher, builder, and their three independent judges | Codex agents |
| `agent/evals-course-factory/schemas/` | JSON Schemas for lesson plans, research handoffs, and review reports | Producers, judges, and validators |
| `agent/evals-course-factory/rubrics/` | Weighted criteria, deterministic checks, hard failures, and fixed behavioral penalties | Judge agents and reviewers |
| `agent/evals-course-factory/references/` | Operating contract, evaluation methodology, output ownership, and Git protocol | All plugin roles |
| `agent/evals-course-factory/templates/` | Initial shared-context template, including human-only merge control | Orchestrator |
| `agent/evals-course-factory/scripts/` | Standard-library package validator | Developers and CI |
| `agent/evals-course-factory/output/lesson-XX/` | Structured plans, source/claim records, and chronological judge reviews for each lesson | Audit and generation provenance |
| `agent/evals-course-factory/CONTEXT.md` | Course decisions, artifact contracts, review scores, revision history, and current state | Cross-run source of truth |
| `ref/instructions.md` | Original assignment and delivery constraints | Reviewers |
| `writeup.md` | What was deliberately cut and where the course is weakest | Reviewers |

There are two directories named `output`, and they have different jobs:

- Repository-level `output/` contains the notebooks that were actually executed.
- `agent/evals-course-factory/output/` contains generation provenance: lesson plans, research sources, and cold-review reports. It does not contain learner output.

## Requirements

- Python 3.12
- A terminal opened at the repository root

Create an isolated environment and install the pinned dependencies:

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r build/lesson-03/requirements.txt
```

### macOS (Bash or Zsh)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r build/lesson-03/requirements.txt
```

### Linux (Bash)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r build/lesson-03/requirements.txt
```

The Lesson 03 requirements are the superset needed for the whole course: Jupyter plus Matplotlib. Notebook logic otherwise uses Python's standard library.

## Take the course

Work through the lessons in order because every build-along consumes artifacts from the previous one.

For each lesson:

1. Read the matching file in `course/`.
2. Start its notebook from the repository root.
3. Complete the editable `TODO` values as directed.
4. Run every cell from a fresh kernel, top to bottom.
5. Confirm that each visible `CHECK` passes and the notebook ends with `FINAL PASS`.

Start Jupyter from PowerShell:

```powershell
python -m jupyter notebook
```

Or from Bash/Zsh on macOS or Linux:

```bash
python -m jupyter notebook
```

Then open these notebooks in order:

```text
build/lesson-01/lesson-01.ipynb
build/lesson-02/lesson-02.ipynb
build/lesson-03/lesson-03.ipynb
```

Run Jupyter from the repository root. The notebooks use repository-relative paths, and Lessons 02 and 03 need the earlier artifacts under `build/`.

The `build/` notebooks contain the learner exercises and their `TODO` prompts. Their generated JSON/JSONL outputs are committed as reference artifacts so reviewers can inspect the result and later lessons have their required inputs. Lesson 1 must regenerate `eval_cases.jsonl`, and Lesson 2 must regenerate `judge_predictions.jsonl`; neither notebook may depend on its own output file already existing. Each notebook writes its artifact from in-memory records, reloads it, and verifies the contents. A committed output's existing presence is never treated as evidence that its lesson passed. The completed notebook executions live separately under `output/`.

## Inspect the completed result

If you only want to review what was built, open the notebooks under `output/`. Their cell outputs are already saved, so Jupyter is not needed just to read them; GitHub and most notebook viewers can render them directly.

The final machine-readable result is `build/lesson-03/grader_report.json`.

## Reproduce the submitted run

To reproduce the submitted result without completing the learner TODOs again, execute the completed notebooks from `output/` in dependency order.

The replayed notebooks are written to `.replay/` at the **repository root**, beside `build/` and `output/`. They are not created inside `output/`. The notebooks also refresh the generated JSON/JSONL artifacts under `build/`.

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force .replay | Out-Null
$env:JUPYTER_CONFIG_DIR = (Join-Path $PWD '.jupyter-config')
$env:IPYTHONDIR = (Join-Path $PWD '.ipython')
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-01/lesson-01.executed.ipynb --output lesson-01.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-02/lesson-02.executed.ipynb --output lesson-02.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-03/lesson-03.executed.ipynb --output lesson-03.replayed.ipynb --output-dir .replay
```

### macOS (Bash or Zsh)

```bash
mkdir -p .replay
export JUPYTER_CONFIG_DIR="$PWD/.jupyter-config"
export IPYTHONDIR="$PWD/.ipython"
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-01/lesson-01.executed.ipynb --output lesson-01.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-02/lesson-02.executed.ipynb --output lesson-02.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-03/lesson-03.executed.ipynb --output lesson-03.replayed.ipynb --output-dir .replay
```

### Linux (Bash)

```bash
mkdir -p .replay
export JUPYTER_CONFIG_DIR="$PWD/.jupyter-config"
export IPYTHONDIR="$PWD/.ipython"
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-01/lesson-01.executed.ipynb --output lesson-01.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-02/lesson-02.executed.ipynb --output lesson-02.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 output/lesson-03/lesson-03.executed.ipynb --output lesson-03.replayed.ipynb --output-dir .replay
```

A successful replay ends each notebook with `FINAL PASS`. Lesson 03 prints all four confusion-matrix counts, `precision=0.75`, and `recall=0.6`.

## How the course factory works

`agent/evals-course-factory/` is the reusable generation system, not another copy of the course. It was built as a local Codex plugin so the generation method is inspectable and reusable rather than hidden in one long prompt. The package records what each agent was asked to do, which evidence it used, how its output was evaluated, what failed, and what changed during remediation.

### Agile planning and backward design

The factory adapts an agile hierarchy to course development:

| Agile concept | Meaning in this project |
| --- | --- |
| Product increment | The complete course |
| Epic (`EP`) | One lesson produced in one orchestrator run |
| User story (`US`) | One lesson section that teaches a single idea |
| Checkpoint (`CP`) | An observable learner capability inside a section |
| Integrated increment | The lesson's build-along and persisted artifact |

The internal `EP`, `US`, and `CP` identifiers remain in the agent provenance for traceability; the learner-facing lessons use ordinary lesson language.

Planning started from the required capstone—a grader that prints real precision and recall—and worked backward. The orchestrator first identified where the audience would get stuck, converted those breaking points into observable checkpoints, and divided the capstone into independently useful artifacts. This produced the cumulative boundary `eval_cases.jsonl` → `judge_predictions.jsonl` → `grader_report.json` instead of three disconnected exercises.

The shared `CONTEXT.md` acts as the project's evolving source of truth. It records approved decisions, prerequisites, terminology, artifact interfaces, review scores, known weaknesses, and the next authorized action. Each run handles at most one lesson so changes remain bounded and later lessons inherit explicit contracts rather than relying on conversational memory.

### Role separation and gated workflow

Six skills divide production from evaluation:

| Role | Responsibility |
| --- | --- |
| Orchestrator | Selects and plans one unfinished lesson, maintains shared context, and coordinates gates |
| Orchestrator judge | Cold-reviews lesson scope, prerequisites, checkpoints, and capstone traceability |
| Searcher | Researches only the approved lesson plan and maps sources to individual claims |
| Searcher judge | Verifies source authority, claim entailment, coverage, locators, and disclosed evidence gaps |
| Builder | Produces the lesson, learner notebook, fixtures, persisted artifacts, and recorded execution |
| Builder judge | Executes deterministic checks and reviews correctness, pedagogy, reproducibility, and artifact handoffs |

One lesson passes through the following pipeline:

```text
plan -> cold review -> research -> cold review -> build -> execute and cold review
```

This separation prevents an agent from approving or silently repairing its own work. Producers own their artifacts; judges own only their review reports. When a judge finds a defect, it provides a concrete remediation criterion and routes the work back to the responsible producer. Earlier reviews are retained, and each gate permits at most two remediation rounds.

The agent configuration is also cost-conscious. `config/agents.json` assigns stronger reasoning to review roles where scrutiny has the most value and uses lower-cost configurations for bounded planning or research tasks. This is an explicit engineering tradeoff rather than using the most expensive model and reasoning level for every step.

### Structured schemas instead of informal handoffs

The factory uses JSON Schemas to make agent outputs machine-checkable:

- `lesson-plan.schema.json` requires the epic and context revisions, purpose, prerequisites, user stories, build-along contract, and capstone trace.
- `research.schema.json` requires source records, claim-level support, coverage reporting, and explicit evidence gaps.
- `review.schema.json` requires the judge and judgee, artifact revision, verdict, calculated score, penalties, aspect ratings, deterministic checks, evidence, strengths, defects, and qualitative feedback.

Stable identifiers connect evidence across those files. For example, `CLM` identifies a researched claim, `SRC` its source, `CHK` a deterministic check, `EV` review evidence, `DEF` a defect, `REV` a review record, and `DEC` an accepted decision. An ID is only a locator: every cited item must still resolve to a specific file, field, section, command, URL, or observed output. This makes the provenance auditable without exposing or depending on private model reasoning.

### Evidence-backed reviews

Each judge uses a committed rubric rather than an overall impression. Aspects receive integer ratings from 1 to 5 and contribute according to fixed weights. Approval requires all of the following:

- A final score of at least 85/100.
- Every scored aspect rated at least 3/5.
- Every hard deterministic check passing.
- No critical defect.

The score is calculated, not chosen: each contribution is `weight × rating / 5`, the contributions are summed, and evidenced behavioral penalties are subtracted. The three role-specific rubrics total 100 points each.

#### Orchestrator judge rubric

The orchestrator judge scores whether the proposed lesson is the right increment before research or writing begins:

| Criterion | Weight |
| --- | ---: |
| Assignment constraint coverage and traceability | 20 |
| Breaking points and observable checkpoints | 20 |
| Backward design from the capstone | 20 |
| Prerequisite and artifact dependency correctness | 15 |
| Task briefs and agent interface clarity | 10 |
| Offline and reproducibility strategy | 10 |
| Context consistency and change tracking | 5 |

Its deterministic checks enforce a two-to-three-lesson course, no more than one lesson planned per run, one to five sections, one to three checkpoints embedded in sections, exactly one build-along of at most 20 minutes, declared input/output interfaces, an offline replay method, and direct traceability from every checkpoint and artifact to a capstone requirement. Planning multiple lessons in one run, generating content before identifying breaking points, impossible dependencies, an untraceable capstone, or granting merge authority are hard failures regardless of the numerical score.

#### Searcher judge rubric

The searcher judge scores the evidence package that the builder will be allowed to use:

| Criterion | Weight |
| --- | ---: |
| Primary-source and paper quality | 20 |
| Claim-to-source entailment | 25 |
| Coverage of planned concepts and failure modes | 15 |
| Citation completeness and resolvability | 15 |
| Technical accuracy and appropriate qualifications | 15 |
| Balance of seminal and recent sources | 5 |
| Builder-ready structured handoff | 5 |

The heaviest criterion is entailment: a reputable source earns no credit if it does not support the exact claim attached to it. Deterministic checks report the percentage of material claims with resolvable sources, the percentage of central claims backed by primary or authoritative evidence (target: at least 80%), duplicate-source rate, missing source metadata, and coverage of every concept in the approved plan. There is deliberately no paper-count quota. Fabricated sources, sources that contradict central claims, or missing evidence for a concept necessary to build the lesson safely are hard failures.

#### Builder judge rubric

The builder judge scores the lesson and its executable artifact together:

| Criterion | Weight |
| --- | ---: |
| Technical correctness | 20 |
| Build-along execution and offline reproducibility | 20 |
| Capstone contribution or completion | 15 |
| Artifact compounding across lessons | 10 |
| Checkpoint and prerequisite alignment | 10 |
| Assignment shape and time compliance | 10 |
| Research and citation fidelity | 10 |
| Pedagogical clarity at breaking points | 5 |

Its deterministic checks execute the documented commands, confirm every promised artifact exists, independently recompute the reported metrics, replay from a fresh kernel without network access or paid calls, verify Python and dependency pins, enforce one incremental build-along per lesson, enforce the section and word-count limits, and check the final archive size. A notebook execution failure, missing visible checks, a missing persisted artifact, a broken input from the preceding lesson, a network requirement during review, or failure to advance the capstone is a hard failure.

#### Behavioral penalty metrics

| ID | Deduction | Measured workflow violation |
| --- | ---: | --- |
| `PEN-001` | −2 | Used a stale or unassigned context, plan, research, or artifact revision |
| `PEN-002` | −3 | Started a phase before its required judge or human approval |
| `PEN-003` | −4 | Modified an artifact owned by another role |
| `PEN-004` | −2 | Worked outside the assigned phase or lesson scope |
| `PEN-005` | −2 | Continued after the maximum two remediation rounds |
| `PEN-006` | −3 | Omitted or falsified required provenance |
| `PEN-007` | −5 | Made an unauthorized Git or external-state change |
| `PEN-008` | −5 | Hid a failed/not-run check or reported it as passing |

```text
raw penalty = sum(applicable deductions)
penalty total = min(raw penalty, 10)
final score = max(0, weighted rubric score - penalty total)
```

Each penalty requires its own `PEV` evidence record and can be applied only once per reviewed artifact. Content defects reduce the relevant weighted criterion instead of receiving a second behavioral deduction.

Qualitative findings complement rather than replace these calculations. They explain consequences, identify strengths and defects with precise `EV` locators, and give the producer a testable remediation target. The final review JSON preserves the individual ratings, weighted contributions, checks, evidence, penalties, defects, verdict, and recomputed total.

Cold review means the judge receives the assignment, relevant context revision, candidate artifact, rubric, and deterministic results—but not the producer's private reasoning, intended answer, desired score, or prior review conclusions. This reduces anchoring and makes the written evidence carry the decision.

### Reproducibility and human control

The learner artifacts, executed notebooks, and agent provenance are deliberately separated:

- `course/` and `build/` contain the material learners read and execute.
- Repository-level `output/` contains the recorded notebook runs used for reproduction.
- Plugin-level `agent/evals-course-factory/output/` contains plans, research, and review history.

The notebooks use committed fixtures so reviewers can reproduce the full course without network access, API keys, paid calls, or model downloads. Outputs are validated at each lesson boundary, and later lessons join records by stable ID rather than relying on row order.

Git actions are a separate authorization boundary. The plugin documents branch, commit, and pull-request conventions, but a passing score never authorizes a merge. Agents may prepare a reviewed pull request only when authorized; only the human user may approve and merge it.

### What this implementation demonstrates

This repository is a hiring exercise, so the agent package is part of the deliverable rather than incidental scaffolding. It demonstrates the ability to turn an ambiguous content request into explicit requirements, decompose a capstone into cumulative interfaces, coordinate specialized AI roles, control usage costs, validate structured outputs, test executable work, trace claims to sources, preserve human oversight, and document known limitations. The course is the product; the plugin and its provenance show the engineering process used to produce and verify that product.

### Plugin layout and validation

Important factory locations:

- `.codex-plugin/plugin.json` declares the local Codex plugin.
- `plugins/marketplace.json` exposes the local package through its personal marketplace metadata.
- `skills/` contains the six role instructions.
- `config/agents.json` maps each role to its model and reasoning effort.
- `schemas/` defines the plan, research, and review JSON formats.
- `rubrics/` defines scoring and behavioral penalties.
- `references/` defines the operating contract, evaluation method, output ownership, and Git safety rules.
- `output/lesson-XX/` preserves every plan, source record, score, defect, and remediation result.

Validate the plugin package without installing third-party Python packages:

```powershell
python agent/evals-course-factory/scripts/validate_agent_package.py
```

The expected result is:

```text
PASS: agent plugin package invariants
```

## Deliberate scope limits

Cached judge responses make the course free, offline, and deterministic, but they do not demonstrate variation across repeated live-model calls. The course also stays with binary classification and a ten-case teaching fixture; it does not cover multiclass evaluation, threshold tuning, ranking metrics, or statistical sample-size selection. See `writeup.md` for the reasoning and the most important extension that was left out.
