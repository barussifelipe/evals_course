# Final implementation plan

## Objective

Provide a reusable Codex plugin that generates the Evals and LLM-as-Judge course one reviewed lesson at a time. This package defines orchestration; it does not contain course content or decide the epics in advance.

## Per-run sequence

1. The Sol-low orchestrator reads the assignment and `CONTEXT.md`, then plans exactly one approved epic using the agile mapping epic=lesson, user story=section, checkpoint=observable capability within a story.
2. The Sol-high orchestrator judge cold-reviews the plan and returns a 1-5 weighted score plus evidence-backed feedback.
3. The Luna-low searcher researches only that plan, prioritizing papers and claim-level traceability.
4. The Terra-medium searcher judge verifies sources, entailment, coverage, and citations.
5. The Terra-medium builder creates one lesson and one cumulative offline Jupyter build-along.
6. The Sol-low builder judge executes deterministic checks and cold-reviews correctness, learning structure, artifact compounding, and citation fidelity.
7. The judgee may remediate findings for at most two rounds. The orchestrator records results and leaves any authorized PR ready for human review.

## Acceptance model

Each rubric uses integer ratings from 1 to 5. `weighted_score = weight * rating / 5`; the total is the weighted sum minus fixed, evidence-backed agent-behavior penalties capped at 10 points. Approval requires at least 85/100, every aspect at least 3/5, all hard checks passing, and no critical defect.

## Git boundary

When separately authorized, agents may create a branch, commit one owned file per commit with `[actual_branch] - ["gpt-agent"]: description`, push, open a draft PR to `main`, and post the three required milestone comments. No agent ever merges or enables auto-merge. Only the human user may merge.

## Deferred decisions

The orchestrator will later derive the number and content of the epics, exact user stories, checkpoints, dataset format, research claims, notebook steps, and cumulative artifacts. Those decisions are intentionally absent from this plugin build.
