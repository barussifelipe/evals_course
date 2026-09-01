---
name: evals-course-orchestrator
description: Orchestrate exactly one lesson-generation iteration for the Evals and LLM-as-Judge course, including planning, delegated research/building, cold reviews, context updates, and human-controlled Git handoff.
---

# Evals Course Orchestrator

Use `gpt-5.6-sol` with `low` reasoning. Read `../../references/operating-contract.md`, `../../references/methodology.md`, `../../references/output-layout.md`, and `../../references/git-protocol.md` completely before acting.

## Scope

Generate at most one lesson per run. Do not predetermine the course epics: derive them later from the assignment's breaking points, checkpoints, capstone, prerequisites, and useful artifact boundaries. An epic is a lesson, a user story is a section, and checkpoints live inside user stories.

Own `CONTEXT.md`; all other agents treat it as read-only. Write the current plan to `../../output/lesson-XX/orchestrator/plan.json`. Only structured agent provenance belongs in the plugin output; lesson prose, notebooks, fixtures, and executed build output use the repository-level destinations defined in the output layout.

## Workflow

1. Read the assignment and existing `CONTEXT.md`. Initialize the context from `../../templates/CONTEXT.template.md` only if absent.
2. If course-level breaking points, checkpoints, backward design, or epic boundaries are undecided, plan them before lesson content. Stop for human approval when the choice would materially define the course.
3. Select exactly one unfinished epic. Create its plan with user stories, embedded checkpoints, acceptance criteria, prerequisites, time budget, and cumulative artifact contract.
4. Delegate a cold review to `orchestrator-judge` using `gpt-5.6-sol`, high. Give it only the assignment, current context revision, candidate plan, rubric, and deterministic results.
5. After plan approval, delegate bounded research to `evals-course-searcher` using `gpt-5.6-luna`, low; then delegate its cold review to `searcher-judge` using `gpt-5.6-terra`, medium.
6. After research approval, delegate the lesson and build-along to `evals-course-builder` using `gpt-5.6-terra`, medium; then delegate its cold review to `builder-judge` using `gpt-5.6-sol`, low.
7. Route review defects back to the judgee. Judges never edit judgee artifacts. Allow no more than two revision rounds per gate.
8. Update `CONTEXT.md` with approved decisions, scores, artifact contracts, unresolved weaknesses, and next state. End with a PR ready for human review when Git operations were authorized.

## Gates

Approve only at 85/100 or higher, with every aspect at least 3/5, no failed hard constraint, and no critical defect. Use `score = sum(weight * rating / 5) - penalties`.

Never merge, auto-merge, squash-merge, rebase-merge, or close a PR as merged. A passing review is not merge authorization. Only the human user may merge.
