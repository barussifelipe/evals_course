# Output ownership and directory layout

All paths are relative to the repository root. Agent-generation provenance belongs inside the plugin's `output/` directory:

```text
agent/evals-course-factory/output/
└── lesson-01/
    ├── orchestrator/
    │   ├── plan.json
    │   └── reviews/
    │       ├── review-01.json
    │       └── review-02.json
    ├── searcher/
    │   ├── sources.json
    │   └── reviews/
    │       ├── review-01.json
    │       └── review-02.json
    └── builder/
        └── reviews/
            ├── review-01.json
            └── review-02.json
```

Use zero-padded lesson directories (`lesson-01`, `lesson-02`, `lesson-03`) and review files in chronological order. Do not overwrite earlier reviews. Omit `review-02.json` when no second remediation round occurs.

## Agent ownership

- Orchestrator writes only `orchestrator/plan.json` and updates the shared `CONTEXT.md`. The orchestrator judge writes only the orchestrator review files.
- Searcher writes only `searcher/sources.json`. This file follows the research schema and contains both source records and their supported claims. The searcher judge writes only the searcher review files.
- Builder writes lesson/build artifacts to their repository-level destinations below. The builder judge writes only the builder review files under agent output.
- A judge never edits the judgee artifact. A judgee never edits a review.

## Course and learner artifact destinations

```text
course/
├── lesson-01.md
├── lesson-02.md
└── lesson-03.md              # only when a third lesson is approved

build/
├── lesson-01/                # notebook, fixtures, and persisted learner artifact
├── lesson-02/
└── lesson-03/                # only when approved

output/
├── lesson-01/                # executed notebook and actual printed/build output
├── lesson-02/
└── lesson-03/                # only when approved
```

`course/` contains exactly one Markdown file per approved lesson and no auxiliary files. Put executable notebooks, fixtures, cached responses, and learner-produced artifacts under the matching `build/lesson-XX/`. Put only the output actually produced by executing that lesson's build-along under the repository-level `output/lesson-XX/`.

Do not place lesson prose, notebooks, fixtures, cached responses, learner artifacts, or executed build output inside the plugin's agent-provenance output. Do not place plans, sources, or judge reviews in `course/`, `build/`, or the repository-level `output/`.
