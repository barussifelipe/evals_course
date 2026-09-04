# Course generation context

Context revision: 16
Status: EP-03 complete; course ready for human review

## Human control and Git safety

Only the human user may merge a pull request. No agent may merge, auto-merge, squash-and-merge, rebase-and-merge, close a PR as merged, or enable auto-merge. A passing judge score is not merge authorization. The final automated state is **PR ready for human review**.

Current branch: `LESSON-02-builder`
Current pull request: `#3` — https://github.com/barussifelipe/evals_course/pull/3
Authorized Git actions: the human authorized lesson-02 commits, branch push, draft PR creation, and milestone comments on 2026-09-02

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
- `EP-02` — **Turn a rubric into judge predictions**. Research revision 1.2 was approved at 98/100 after two targeted remediation rounds. Builder revision 1.0 was approved at 100/100 on its first review. The lesson, cached-response fixture, fresh-kernel notebook, persisted predictions, and executed notebook are complete.
- `EP-03` — **Measure the grader**. Research revision 1.1 was approved at 100/100 after one targeted remediation round. Builder revision 1.0 was approved at 100/100 on its first review. The cumulative fixture chain now contains 10 stable case IDs, and the final grader report prints verified precision and recall.

## Current epic

`EP-03` — **Measure the grader**. On 2026-09-03 the human approved acting on the plan and required the cumulative fixture chain to contain at least 10 stable case IDs. This authorizes the research and build gates, including minimal updates to prior lesson data, notebooks, and executed outputs needed to keep the cumulative artifacts reproducible. Git mutation and hosting actions remain unauthorized. EP-03 must consume the expanded EP-01 and EP-02 artifacts and complete the capstone without changing their schemas, existing IDs, or label semantics.

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
| `DEC-L02-001` | 5 | Open the EP-02 planning iteration and select EP-02 as the current epic. | The human explicitly requested the second lesson plan for review on 2026-09-02; this authorizes planning only, not research, building, Git mutation, or hosting actions. |
| `DEC-L02-002` | 5 | Revise EP-02 plan from 1.0 to 1.1 after review 01. | Record the human authorization in context revision 5 and explicitly trace approved breaking point 2 through US-L02-01 to CP-L02-03-A without changing lesson structure. |
| `DEC-L02-003` | 6 | Accept EP-02 plan revision 1.1 at the orchestrator gate. | Final cold review scored the plan 100/100; all six deterministic checks passed, both prior defects closed, and no defects or penalties remained. Human approval is still required before research. |
| `DEC-L02-004` | 7 | Record human approval of EP-02 plan revision 1.1 and authorize bounded research. | The human explicitly requested that lesson 02 be built from the approved plan on 2026-09-02; the workflow proceeds through the research gate before builder generation. |
| `DEC-L02-005` | 8 | Approve EP-02 research revision 1.2 after two targeted remediation rounds. | Reviews 01 and 02 identified an incorrect JSON Schema `additionalProperties` locator; the final review verified Core §10.3.2.3, closed the defect, and scored the research 98/100. |
| `DEC-L02-006` | 9 | Complete EP-02 builder revision 1.0. | Builder review 01 scored 100/100 with no defects or penalties; an independent isolated fresh-kernel replay passed, reproduced the recorded output, preserved EP-01 identities and labels, and matched the persisted prediction artifact exactly. |
| `DEC-L02-007` | 10 | Revise EP-02 presentation and build-along progression at human request. | Builder revision 1.1 adds accessible inline SVG teaching diagrams and learner-owned rubric, verdict-map, and response-contract TODOs matching EP-01's learn-as-you-go pattern; the completed notebook replay passed all five checks and final PASS. |
| `DEC-L03-001` | 11 | Open the EP-03 planning iteration and select EP-03 as the current epic. | The human explicitly requested the last lesson plan on 2026-09-03; this authorizes planning only, not research, building, Git mutation, or hosting actions. |
| `DEC-L03-002` | 12 | Accept EP-03 plan revision 1.0 at the orchestrator gate. | The cold review scored the plan 100/100; all deterministic checks passed, every weighted aspect rated 5/5, and no defects or penalties were found. Human approval is still required before research. |
| `DEC-L03-003` | 13 | Revise EP-03 plan to 1.1 and authorize its research/build iteration. | The human approved acting on the plan and required at least 10 case IDs for more meaningful metrics. The revised builder contract minimally expands the cumulative EP-01/EP-02 fixture chain while preserving schemas, existing IDs, label semantics, and current user edits. |
| `DEC-L03-004` | 14 | Accept EP-03 plan revision 1.1 and open bounded research. | Cold review 02 scored the revised plan 100/100 with all hard checks passing and no defects or penalties; the human had already authorized the research/build iteration. |
| `DEC-L03-005` | 15 | Approve EP-03 research after one targeted remediation round. | Review 01 scored 77/100 and found missing recall-specific zero-division evidence plus inaccurate Fawcett locators. The searcher added official recall documentation and corrected the locators; review 02 closed both defects and scored 100/100. |
| `DEC-L03-006` | 16 | Complete EP-03 builder revision 1.0 and the course capstone. | Builder review 01 scored 100/100 with no defects or penalties. An isolated EP-01 through EP-03 replay exited successfully, reproduced all artifacts byte-for-byte, and verified 10 shared IDs plus TP=3, FP=1, FN=2, TN=4, precision=0.75, and recall=0.6. |

## Scores and review history

| Review ID | Agent | Artifact revision | Score | Verdict |
| --- | --- | --- | ---: | --- |
| `REV-ORCH-L01-01` | orchestrator-judge | 1.0 | 84 | targeted revision |
| `REV-ORCH-L01-02` | orchestrator-judge | 1.1 | 100 | approved |
| `REV-SEARCH-L01-01` | searcher-judge | 1.0 | 84 | targeted revision |
| `REV-SEARCH-L01-02` | searcher-judge | 1.1 | 95 | approved |
| `REV-BUILDER-L01-01` | builder-judge | 1.0 | 100 | approved |
| `REV-ORCH-L02-01` | orchestrator-judge | 1.0 | 90 | targeted revision |
| `REV-ORCH-L02-02` | orchestrator-judge | 1.1 | 100 | approved |
| `REV-ORCH-L03-01` | orchestrator-judge | 1.0 | 100 | approved |
| `REV-ORCH-L03-02` | orchestrator-judge | 1.1 | 100 | approved |
| `REV-SEARCH-L03-01` | searcher-judge | 1.0 | 77 | targeted revision |
| `REV-SEARCH-L03-02` | searcher-judge | 1.1 | 100 | approved |
| `REV-BUILDER-L03-01` | builder-judge | 1.0 | 100 | approved |
| `REV-SEARCH-L02-01` | searcher-judge | 1.0 | 80 | targeted revision |
| `REV-SEARCH-L02-02` | searcher-judge | 1.1 | 77 | targeted revision |
| `REV-SEARCH-L02-03` | searcher-judge | 1.2 | 98 | approved |
| `REV-BUILDER-L02-01` | builder-judge | 1.0 | 100 | approved |

## EP-01 approved artifact contract

- Lesson: `course/lesson-01.md` — four sections and one embedded checkpoint.
- Canonical build-along: `build/lesson-01/lesson-01.ipynb` — Python 3.12, offline, five visible checks, one 18-minute build-along.
- Persisted handoff: `build/lesson-01/eval_cases.jsonl` — 10 records with stable unique IDs and fields `case_id`, `input`, `candidate_output`, and `human_label`.
- Recorded execution: `output/lesson-01/lesson-01.executed.ipynb` — fresh-kernel execution with checks 1-5 and final PASS.
- EP-02 must preserve `case_id` and the invariant `human_label = 1` meaning regression present.

## EP-02 approved artifact contract

- Lesson: `course/lesson-02.md` — four sections and one embedded checkpoint.
- Canonical build-along: `build/lesson-02/lesson-02.ipynb` — Python 3.12, offline, five visible checks, one 18-minute build-along.
- Cached fixture: `build/lesson-02/cached_judge_responses.jsonl` — exactly one strict response per EP-01 case.
- Persisted handoff: `build/lesson-02/judge_predictions.jsonl` — stable `case_id`, unchanged `human_label`, binary `judge_label`, and non-empty `judge_reason`.
- Recorded execution: `output/lesson-02/lesson-02.executed.ipynb` — fresh-kernel execution with checks 1-5 and final PASS.
- EP-03 must join EP-01 cases and EP-02 predictions by `case_id`, verify copied labels, compute metrics without relying on row order, and enforce a minimum of 10 cases.

## EP-03 approved artifact contract

- Lesson: `course/lesson-03.md` — four sections and one embedded checkpoint.
- Canonical build-along: `build/lesson-03/lesson-03.ipynb` — Python 3.12, offline, four visible checks, one 18-minute build-along.
- Persisted capstone: `build/lesson-03/grader_report.json` — 10 cases, positive-class and zero-division policies, TP=3, FP=1, FN=2, TN=4, precision=0.75, and recall=0.6.
- Recorded execution: `output/lesson-03/lesson-03.executed.ipynb` — fresh-kernel execution with all checks and final PASS.

## Unresolved risks and weaknesses

- Three lessons can become thin; section counts and time budgets must keep the total near 90 minutes.
- Binary labels make precision and recall concrete but intentionally defer multiclass and ranking evaluation.
- Cached judge responses enable offline replay but do not demonstrate live-provider variance.
- The EP-01 both-class presence check is an approved course-specific guard for this small binary fixture, not a universal class-balance rule.
- Ten cases make the demonstration less brittle than four but are not a statistically sufficient universal sample-size threshold.

## Next authorized action

The complete three-lesson course is ready for human review. Git mutation and hosting actions remain unauthorized; no Lesson 03 branch, commits, push, or PR were created. Draft PR #3 remains unchanged, and only the human may merge it.
