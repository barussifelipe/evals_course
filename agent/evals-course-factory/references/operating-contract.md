# Operating contract

## Assignment invariants

- Topic: Evals and LLM-as-Judge, for someone who shipped an AI feature and cannot tell whether it is getting worse.
- Capstone: a working grader that prints real precision and recall.
- Generate the course and build-alongs with AI; preserve the reusable agent setup.
- Identify at least three breaking points before generating content, convert them into observable checkpoints, and design backward from the capstone.
- The course has 2-3 lessons, no more than 5 sections per lesson, and 1-3 checkpoints per lesson.
- A section teaches one idea in 300-500 words and about 2-3 minutes.
- Every lesson ends with exactly one incremental build-along under 20 minutes. Its artifact must be useful alone and consumed by the next lesson.
- Total learner time is about 90 minutes. Prefer two strong lessons over three thin ones.
- Text only. Inline HTML/SVG is allowed; Mermaid, raster images, quizzes, flashcards, video, and audio are prohibited.
- The canonical build-along is a Jupyter notebook with Markdown and editable Python cells. It must run offline, top-to-bottom from a fresh kernel, print a visible check at every step, and persist its output artifact.
- Pin Python 3.12 and dependencies. Review must not require a paid API call. Do not ship dependencies, model weights, or more than 10 MB.

## Agile hierarchy

- Course: product increment.
- Epic (`EP`): one lesson, planned and generated in one orchestrator run.
- User story (`US`): one lesson section.
- Checkpoint (`CP`): an observable learner capability embedded within a user story.
- Build-along: the epic's integrated increment, not a separate assessment.

Do not decide epic boundaries in this reusable plugin. The orchestrator derives them from breaking points, checkpoints, prerequisite order, capstone decomposition, and artifact interfaces, then seeks human approval when the decision materially defines the course.

## Ownership

- Orchestrator: `CONTEXT.md`, plans, task briefs, state transitions, PR comments.
- Searcher: lesson-scoped research artifacts only.
- Builder: lesson, notebook, fixtures, recorded output, and learner artifacts.
- Judges: their own review artifacts only.

No agent edits its judge's report. No judge edits its judgee's artifacts. Course deliverables stay outside the plugin directory; only structured agent provenance uses the plugin-local output tree.

## Output routing

Read `output-layout.md` before writing any artifact. The plugin-local `output/lesson-XX/` stores only agent provenance: the orchestrator plan and review, searcher sources and review, and builder review. Course prose remains one file per lesson in `course/`; build code remains under `build/lesson-XX/`; actual executed build results remain under the repository-level `output/lesson-XX/`.
