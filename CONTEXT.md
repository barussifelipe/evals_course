# Course generation context

Context revision: 4
Status: EP-01 complete and approved; awaiting authorization to begin EP-02

## Human control and Git safety

Only the human user may merge a pull request. No agent may merge, auto-merge, squash-and-merge, rebase-and-merge, close a PR as merged, or enable auto-merge. A passing judge score is not merge authorization. The final automated state is **PR ready for human review**.

Current branch: not assigned
Current pull request: not opened
Authorized Git actions: none recorded

## Assignment constraints

Authoritative assignment: `ref/instructions.md`

- Topic: Evals and LLM-as-Judge.
- Audience: someone who shipped an AI feature and cannot tell whether it is getting worse.
- Capstone: a working grader that prints real precision and recall.
- Proposed course: 3 lessons, no more than 5 sections and 1-3 checkpoints per lesson, about 90 minutes total.
- Each lesson ends with exactly one cumulative build-along under 20 minutes.
- Build-alongs use offline, top-to-bottom Jupyter notebooks with editable Python cells and visible checks.
- Python 3.12 and dependencies are pinned; review requires no paid API call; submission remains under 10 MB.
- Text only; inline HTML/SVG is allowed; Mermaid, raster images, quizzes, flashcards, video, and audio are excluded.

## Audience and prerequisites

The learner has shipped an AI feature and can read basic Python. No prior evaluation, statistics, or prompt-grading expertise is assumed.

## Breaking points

1. Teams collect plausible examples but lack explicit labels and a decision rule, so regressions cannot be measured consistently.
2. A model judge can sound authoritative while applying an underspecified rubric inconsistently or leaking irrelevant preferences into its verdict.
3. A high aggregate accuracy can hide the failure that matters: missed regressions or excessive false alarms.

## Course checkpoints

- `CP-L01-03-A`: Create a small, labeled evaluation set with an explicit positive class and validate its schema and class counts.
- `CP-L02-03-A`: Run an offline LLM-as-judge rubric over the evaluation set and inspect disagreements against human labels.
- `CP-L03-03-A`: Build a confusion matrix from judge predictions and print precision and recall with zero-division handling.

## Capstone contract

Given persisted records containing stable IDs, inputs, candidate outputs, human binary labels, and offline judge responses, the final grader validates alignment, converts judge responses to binary predictions, computes TP/FP/FN/TN, and visibly prints precision and recall. A deterministic fixture must prove the printed values against known expected results.

## Agile hierarchy and epic boundaries

Approved by the human user on 2026-09-02:

- `EP-01` — **Make regressions measurable**: define the failure, positive class, labeled cases, and dataset checks. Produces `eval_cases.jsonl`.
- `EP-02` — **Turn a rubric into judge predictions**: specify a bounded rubric, replay cached judge responses, parse verdicts, and inspect human/judge disagreements. Consumes `eval_cases.jsonl`; produces `judge_predictions.jsonl`.
- `EP-03` — **Measure the grader**: join labels and predictions, construct the confusion matrix, and print real precision and recall. Consumes both prior artifacts; produces `grader_report.json` and visible metrics.

## Completed epics

- `EP-01` — **Make regressions measurable**. Research revision 1.1 was approved at 95/100 after one targeted remediation round. Builder revision 1.0 was approved at 100/100 on its first review. The lesson, fresh-kernel notebook, persisted dataset, and executed notebook are complete.

## Current epic

None in progress. The next unfinished epic is `EP-02` — **Turn a rubric into judge predictions**. It must consume `build/lesson-01/eval_cases.jsonl` without changing `case_id` or `human_label` semantics. EP-02 planning and generation require a new authorized orchestrator iteration.

## Output routing

Agent provenance root: `agent/evals-course-factory/output/lesson-XX/`

- Orchestrator plan/reviews: `orchestrator/`
- Searcher sources/reviews: `searcher/`
- Builder reviews: `builder/`
- Lesson prose: `course/lesson-XX.md`
- Build code and learner artifacts: `build/lesson-XX/`
- Actual executed build output: repository-level `output/lesson-XX/`

## Cross-epic artifact interfaces

`eval_cases.jsonl` -> `judge_predictions.jsonl` -> `grader_report.json`; stable case IDs and binary-label semantics must remain unchanged across lessons.

## Approved terminology and evidence

Approved course-level terminology: an epic is one lesson; a user story is one section; a checkpoint is an observable learner capability embedded in a section; the positive class is `human_label = 1`, meaning the defined regression is present. Lesson claims still require later research review.

## Decisions and revision history

| ID | Revision | Decision | Rationale |
| --- | ---: | --- | --- |
| `DEC-COURSE-001` | 1 | Propose three epics and their artifact interfaces; do not begin `EP-01` planning yet. | The user requested three epics, and each boundary yields a useful standalone artifact while decomposing the capstone backward. |
| `DEC-COURSE-002` | 2 | Approve the three-epic course design. | The human user approved EP-01 through EP-03, their checkpoints, capstone contract, and cumulative artifact chain on 2026-09-02. |
| `DEC-L01-001` | 2 | Select EP-01 for the current run. | EP-01 is the first unfinished epic and produces the human-labeled ground truth required by all later work. |
| `DEC-L01-002` | 2 | Revise EP-01 plan from 1.0 to 1.1 after review 01. | Move CP-L01-03-A after all required validation instruction and encode bounded searcher/builder handoffs without expanding the one-lesson scope. |
| `DEC-L01-003` | 3 | Approve EP-01 plan revision 1.1. | Final cold review scored the plan 100/100; every weighted aspect rated 5/5, all critical checks passed, and no defects or penalties remained. |
| `DEC-L01-004` | 4 | Approve EP-01 research after one remediation round. | Review 01 scored 84/100; the searcher repaired a mixed-source locator and explicitly bounded the both-class check as a course decision. Review 02 scored revision 1.1 at 95/100 with both defects closed. |
| `DEC-L01-005` | 4 | Complete EP-01 builder revision 1.0. | Builder review 01 scored 100/100 with no defects or penalties; an independent isolated fresh-kernel replay passed and reproduced the persisted JSONL exactly. |

## Scores and review history

| Review ID | Agent | Artifact revision | Score | Verdict |
| --- | --- | --- | ---: | --- |
| `REV-ORCH-L01-01` | orchestrator-judge | 1.0 | 84 | targeted revision |
| `REV-ORCH-L01-02` | orchestrator-judge | 1.1 | 100 | approved |
| `REV-SEARCH-L01-01` | searcher-judge | 1.0 | 84 | targeted revision |
| `REV-SEARCH-L01-02` | searcher-judge | 1.1 | 95 | approved |
| `REV-BUILDER-L01-01` | builder-judge | 1.0 | 100 | approved |

## EP-01 approved artifact contract

- Lesson: `course/lesson-01.md` — four sections and one embedded checkpoint.
- Canonical build-along: `build/lesson-01/lesson-01.ipynb` — Python 3.12, offline, five visible checks, one 18-minute build-along.
- Persisted handoff: `build/lesson-01/eval_cases.jsonl` — four records, stable unique IDs, fields `case_id`, `input`, `candidate_output`, and `human_label`, with two records per class.
- Recorded execution: `output/lesson-01/lesson-01.executed.ipynb` — fresh-kernel execution with checks 1-5 and final PASS.
- EP-02 must preserve `case_id` and the invariant `human_label = 1` meaning regression present.

## Unresolved risks and weaknesses

- Three lessons can become thin; section counts and time budgets must keep the total near 90 minutes.
- Binary labels make precision and recall concrete but intentionally defer multiclass and ranking evaluation.
- Cached judge responses enable offline replay but do not demonstrate live-provider variance.
- The EP-01 both-class presence check is an approved course-specific guard for this small binary fixture, not a universal class-balance rule.

## Next authorized action

Await human authorization for a new EP-02 orchestrator iteration. Do not generate EP-02 or EP-03 in this completed EP-01 run, and do not perform Git or hosting mutations without explicit authorization.
