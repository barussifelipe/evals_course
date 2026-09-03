# Evals and LLM-as-Judge

A three-lesson, approximately 90-minute course for someone who has shipped an AI feature and cannot tell whether it is getting worse. Everything runs offline from committed fixtures; no API key or paid call is required.

## Checkpoints and capstone

1. Create and validate a labeled evaluation set with an explicit positive class.
2. Replay a bounded model judge and inspect its disagreements with human labels.
3. Join labels and predictions by stable ID, then calculate a confusion matrix, precision, and recall.

The final artifact is `build/lesson-03/grader_report.json`. For the included ten cases it reports TP=3, FP=1, FN=2, TN=4, precision=0.75, and recall=0.6.

## Setup

Use Python 3.12 from the repository root:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r build/lesson-01/requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## Follow the build-alongs

Read `course/lesson-01.md` through `course/lesson-03.md` in order. Open each matching notebook and replace its `TODO` values before running all cells from a fresh kernel:

```text
python -m jupyter notebook build/lesson-01/lesson-01.ipynb
python -m jupyter notebook build/lesson-02/lesson-02.ipynb
python -m jupyter notebook build/lesson-03/lesson-03.ipynb
```

Each notebook prints visible checks and persists the artifact consumed by the next lesson.

## Replay the submitted results

The completed notebooks in `output/` are the recorded offline run. Re-execute them from the repository root and write fresh notebook copies to `.replay/`:

```text
python -m jupyter nbconvert --to notebook --execute output/lesson-01/lesson-01.executed.ipynb --output lesson-01.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute output/lesson-02/lesson-02.executed.ipynb --output lesson-02.replayed.ipynb --output-dir .replay
python -m jupyter nbconvert --to notebook --execute output/lesson-03/lesson-03.executed.ipynb --output lesson-03.replayed.ipynb --output-dir .replay
```

The final run prints all four confusion-matrix counts, precision, recall, and `FINAL PASS`.
