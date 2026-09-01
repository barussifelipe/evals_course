---
name: evals-course-builder
description: Build one approved Evals and LLM-as-Judge lesson and its cumulative offline notebook build-along from approved context, plan, and research.
---

# Evals Course Builder

Use `gpt-5.6-terra` with `medium` reasoning. Read `../../references/operating-contract.md` and `../../references/methodology.md` before building.

Build exactly one approved epic. Treat each user story as one 300-500 word, 2-3 minute section containing its assigned checkpoint. Create one build-along at the end of the lesson, under 20 learner minutes. Use a standard Jupyter notebook with Markdown instructions and learner-editable Python cells, similar to Colab but runnable offline under Python 3.12.

Each notebook step must add a small capability and print a visible check. Do not drop in the finished solution. The notebook must run from a fresh kernel in top-to-bottom order and save an explicit artifact consumed by the next epic. Use fixtures or cached model results so review requires no paid API call. Do not rely on hidden notebook state or a hosted service.

Use only approved claims and cite their `CLM`/`SRC` records accurately. Inline diagrams may use HTML or SVG, never Mermaid or raster images. Do not add quizzes, flashcards, video, or audio.

Run the supplied deterministic checks before handoff. On review, edit only builder-owned artifacts and address defects with evidence. Never edit a judge report or `CONTEXT.md`.
