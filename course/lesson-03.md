# Lesson 03: Measure the grader

The first two lessons created ground-truth cases and replayable judge predictions. This lesson turns those records into an auditable binary grader. The positive class remains fixed throughout: `1` means the defined regression is present.

<svg viewBox="0 0 920 180" width="100%" role="img" aria-labelledby="grader-map-title grader-map-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="grader-map-title">Lesson progression from aligned evidence to an auditable grader report</title>
  <desc id="grader-map-desc">Four connected stages: join cases and predictions by identity, count the four outcomes, calculate precision and recall, then prove and persist the report.</desc>
  <defs><marker id="grader-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="30" width="190" height="105" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="115" y="67" font-size="17" font-weight="700" fill="#172554">Join by identity</text><text x="115" y="96" font-size="14" fill="#1e3a8a">Stable case IDs</text><text x="115" y="117" font-size="14" fill="#1e3a8a">Exact coverage</text>
    <path d="M214 82H249" stroke="#475569" stroke-width="2" marker-end="url(#grader-arrow)"/><rect x="255" y="30" width="190" height="105" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="350" y="67" font-size="17" font-weight="700" fill="#2e1065">Count outcomes</text><text x="350" y="96" font-size="14" fill="#4c1d95">TP · FP · FN · TN</text><text x="350" y="117" font-size="14" fill="#4c1d95">Case-level trace</text>
    <path d="M449 82H484" stroke="#475569" stroke-width="2" marker-end="url(#grader-arrow)"/><rect x="490" y="30" width="190" height="105" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="585" y="67" font-size="17" font-weight="700" fill="#022c22">Read the metrics</text><text x="585" y="96" font-size="14" fill="#064e3b">Precision = alarms</text><text x="585" y="117" font-size="14" fill="#064e3b">Recall = regressions</text>
    <path d="M684 82H719" stroke="#475569" stroke-width="2" marker-end="url(#grader-arrow)"/><rect x="725" y="30" width="175" height="105" rx="14" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="812" y="67" font-size="17" font-weight="700" fill="#431407">Prove the report</text><text x="812" y="96" font-size="14" fill="#7c2d12">Known oracle</text><text x="812" y="117" font-size="14" fill="#7c2d12">Write + read back</text>
  </g>
</svg>

By the end, you will have `grader_report.json`: a checked, machine-readable confusion matrix with precision and recall for the same ten cases used throughout the course.

## Join evidence by identity (about 3 minutes)

A grader must compare the prediction and human label for the **same case**. Row order cannot prove that. `case_id` can.

<svg viewBox="0 0 860 220" width="100%" role="img" aria-labelledby="join-title join-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="join-title">Join cases and predictions by stable identity</title>
  <desc id="join-desc">Human and judge evidence with the same case ID become one aligned scoring row. Row positions are ignored.</desc>
  <defs><marker id="join-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="30" width="235" height="135" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="137" y="61" font-size="16" font-weight="700" fill="#172554">Human evidence</text><text x="137" y="93" font-family="ui-monospace, monospace" font-size="14" fill="#1e3a8a">refund-window-003</text><text x="137" y="122" font-size="14" fill="#334155">human_label = 1</text><text x="137" y="146" font-size="13" fill="#475569">Position: irrelevant</text>
    <path d="M259 98H334" stroke="#475569" stroke-width="2" marker-end="url(#join-arrow)"/><rect x="340" y="58" width="180" height="80" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="430" y="91" font-size="16" font-weight="700" fill="#2e1065">Match case_id</text><text x="430" y="117" font-size="13" fill="#4c1d95">then verify labels</text>
    <path d="M524 98H599" stroke="#475569" stroke-width="2" marker-end="url(#join-arrow)"/><rect x="605" y="30" width="235" height="135" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="722" y="61" font-size="16" font-weight="700" fill="#064e3b">Judge evidence</text><text x="722" y="93" font-family="ui-monospace, monospace" font-size="14" fill="#065f46">refund-window-003</text><text x="722" y="122" font-size="14" fill="#334155">judge_label = 0</text><text x="722" y="146" font-size="13" fill="#475569">Aligned result: one FN</text>
    <text x="430" y="201" font-size="14" font-weight="600" fill="#334155">Same identity → safe comparison</text>
  </g>
</svg>

Before counting, enforce four rules:

- **Valid identity:** every `case_id` is a non-empty string.
- **No duplicates:** one ID appears once per artifact.
- **Exact coverage:** no prediction is missing or unknown.
- **Labels agree:** the copied `human_label` matches Lesson 01.

If any rule fails, stop. Guessing would change which cases are scored.

The notebook indexes both files by `case_id`, compares their ID sets, and builds aligned tuples. Reordering either file cannot change the result. This preserves the required pairing between ground truth and predictions ([CLM-L03-005](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)).

Think of the join as an evidence check before it is a data operation. The human file answers, “What happened in this case?” The prediction file answers, “What did the judge decide for this case?” A score is meaningful only when both answers refer to the same event. Matching by position assumes that two independently produced files stayed in the same order forever. Matching by `case_id` states the relationship directly and survives sorting, filtering, and serialization.

Three failures should stop scoring immediately. A duplicate ID makes one identity point to multiple records. A missing ID leaves a human label without a prediction, or a prediction without ground truth. A copied `human_label` that differs between files signals that the handoff changed the reference answer. Silently dropping, overwriting, or accepting any of these cases would change the population being measured and could still produce a plausible decimal. The notebook rejects them before constructing the confusion matrix.

This is why the prediction artifact preserves `human_label` even though Lesson 3 can also read it from the original cases. The duplicate value acts as a handoff checksum that is easy to inspect: for every ID, the copied label must equal the source label. After that check passes, the grader uses the source human label and the judge label to create one aligned scoring row. The reason text remains available for diagnosis, but it does not affect the numerical outcome.

Keep one meaning visible:

> `1` means **regression present** for both the human and the judge.

“Positive” names the condition being detected; it does not mean “good answer” ([CLM-L03-003](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)). The first check also requires at least ten records in both files. Ten is this course fixture's floor, not proof of statistical confidence.

## Count the four outcomes (about 3 minutes)

Once the two labels are aligned, every case belongs to exactly one of four outcomes. When the human label is `1` and the judge label is `1`, the judge correctly detected a regression: true positive, or TP. When the human label is `0` and the judge label is `1`, it raised a regression alarm where the reference says none exists: false positive, or FP. A human `1` with judge `0` is a missed regression: false negative, or FN. A human `0` with judge `0` is a correct non-alarm: true negative, or TN.

<svg viewBox="0 0 760 300" width="100%" role="img" aria-labelledby="matrix-title matrix-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="matrix-title">Binary confusion matrix for regression detection</title><desc id="matrix-desc">Human labels form the rows and judge labels form the columns. The four cells show true positive, false negative, false positive, and true negative outcomes.</desc>
  <g font-family="system-ui, sans-serif" text-anchor="middle"><text x="465" y="27" font-size="16" font-weight="700" fill="#334155">Judge prediction</text><text x="36" y="177" transform="rotate(-90 36 177)" font-size="16" font-weight="700" fill="#334155">Human label</text><text x="335" y="57" font-size="14" fill="#475569">1 · regression</text><text x="565" y="57" font-size="14" fill="#475569">0 · absent</text><text x="138" y="127" font-size="14" fill="#475569">1 · regression</text><text x="138" y="237" font-size="14" fill="#475569">0 · absent</text>
    <rect x="225" y="75" width="220" height="100" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="335" y="116" font-size="22" font-weight="700" fill="#064e3b">TP</text><text x="335" y="145" font-size="14" fill="#065f46">Correct alarm</text><rect x="455" y="75" width="220" height="100" rx="14" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="565" y="116" font-size="22" font-weight="700" fill="#7c2d12">FN</text><text x="565" y="145" font-size="14" fill="#9a3412">Missed regression</text><rect x="225" y="185" width="220" height="100" rx="14" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/><text x="335" y="226" font-size="22" font-weight="700" fill="#7f1d1d">FP</text><text x="335" y="255" font-size="14" fill="#991b1b">False alarm</text><rect x="455" y="185" width="220" height="100" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="565" y="226" font-size="22" font-weight="700" fill="#172554">TN</text><text x="565" y="255" font-size="14" fill="#1e3a8a">Correct non-alarm</text></g>
</svg>

Those outcomes are mutually exclusive and exhaustive for a binary decision. Fawcett's standard confusion-matrix framing describes the same four possibilities: positive and predicted positive, positive and predicted negative, negative and predicted positive, and negative and predicted negative ([CLM-L03-001](https://www.math.ucdavis.edu/~saito/data/roc/fawcett-roc.pdf)). The useful discipline here is case-level traceability. Instead of counting labels in two independent columns, assign an outcome to each `case_id` after the validated join. A maintainer can then ask, “Which examples created our false positives?” and receive concrete case IDs rather than a mysterious aggregate.

The notebook uses a short explicit mapping from the two binary labels to `TP`, `FP`, `FN`, or `TN`. It prints every ID and its outcome, then produces the four totals. This is deliberately boring code: the number of cases is small and an if-expression is easier to audit than a metric library call that hides the mapping. More importantly, it checks conservation: `TP + FP + FN + TN` must equal the number of joined cases. If the totals do not add up, an input was skipped, classified twice, or classified outside the binary contract.

The fixture is designed to show every kind of event. It includes correct alarms, correct non-alarms, missed late-refund regressions, and one false alarm on an in-window request. That last case matters because a judge that calls every approval a regression might catch many bad replies while making noisy alerts. Conversely, a judge that rarely alarms can look calm while missing real regressions. The confusion matrix keeps those failures separate. Do not turn it into accuracy here: one aggregate proportion would conceal which kind of operational mistake occurred. The next section asks the two questions that separate them.

## Read precision and recall (about 3 minutes)

Precision starts with the alarms the judge actually raised. Its formula is `TP / (TP + FP)`: among predicted regression cases, what fraction really were regressions? In an operational review, false positives are false alarms. Low precision means people spend time opening cases that the human reference says are acceptable. Recall starts with the human-labeled regressions. Its formula is `TP / (TP + FN)`: among the regressions that existed in the fixture, what fraction did the judge catch? False negatives are missed regressions. Low recall means the system lets known failure cases pass unnoticed.

<svg viewBox="0 0 820 210" width="100%" role="img" aria-labelledby="metric-title metric-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="metric-title">Precision and recall answer different operational questions</title><desc id="metric-desc">Precision examines judge alarms and separates correct alarms from false alarms. Recall examines human-labeled regressions and separates caught regressions from missed regressions.</desc>
  <g font-family="system-ui, sans-serif" text-anchor="middle"><rect x="20" y="25" width="375" height="160" rx="16" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="207" y="58" font-size="20" font-weight="700" fill="#2e1065">Precision</text><text x="207" y="91" font-size="17" fill="#4c1d95">TP / (TP + FP)</text><text x="207" y="124" font-size="14" fill="#334155">Of the judge's alarms,</text><text x="207" y="147" font-size="14" fill="#334155">how many were correct?</text><rect x="425" y="25" width="375" height="160" rx="16" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="612" y="58" font-size="20" font-weight="700" fill="#064e3b">Recall</text><text x="612" y="91" font-size="17" fill="#065f46">TP / (TP + FN)</text><text x="612" y="124" font-size="14" fill="#334155">Of the real regressions,</text><text x="612" y="147" font-size="14" fill="#334155">how many did the judge catch?</text></g>
</svg>

These formulas and their binary positive-class interpretation are standard ([CLM-L03-002](https://www.math.ucdavis.edu/~saito/data/roc/fawcett-roc.pdf); [CLM-L03-002](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)). The names are easy to reverse if you forget their denominators, so read them literally. Precision asks whether an alarm is correct; its denominator contains predicted positives. Recall asks whether a real regression was found; its denominator contains actual positives. Neither metric is “the score,” and neither treats true negatives as an answer to one of those questions.

The grader must also define what happens when a denominator is zero. If there are no judge alarms, `TP + FP` is zero and precision is mathematically undefined. If the fixture has no human-positive regressions, `TP + FN` is zero and recall is undefined. The official metric interfaces document those two situations and expose a configurable zero-division behavior ([CLM-L03-004](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html); [CLM-L03-004](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)). This course chooses a simple explicit policy: return `0.0` for either zero denominator and persist that policy in the report.

The policy is not a claim that `0.0` is the only possible interpretation. It is a deterministic course decision that prevents a runtime error or a quietly missing field. In a production system, choose and document a policy appropriate to the audience; warnings can be useful too. For this fixed fixture, the denominators are nonzero. The notebook still implements the branch, prints the policy, and asserts exact known values: `precision = 0.75` and `recall = 0.6`. The difference is informative: three of four alarms are correct, while the judge catches three of five human-labeled regressions.

## Prove and persist the grader report (about 3 minutes)

Metric code deserves a known-answer test because a plausible-looking decimal can hide swapped labels, a dropped record, or a copied-label error. The notebook's fixture contains ten stable IDs and declares its oracle before persistence: `TP = 3`, `FP = 1`, `FN = 2`, `TN = 4`, precision `0.75`, and recall `0.6`. It asserts the four count values, then asserts the two exact floating-point values. Because `3/4` and `3/5` are deterministic Python values here, direct equality makes the intended teaching check easy to inspect.

The check is not evidence that ten cases are statistically sufficient. Larger samples generally reduce sampling variation and narrow confidence intervals, but no universal threshold follows from that fact ([CLM-L03-006](https://online.stat.psu.edu/stat200/lesson/4/4.7)). The ten-case minimum is a human-required fixture floor that makes all four outcomes visible. A biased or unrepresentative collection remains biased even when it grows. Treat this report as a reproducible snapshot of these cases, not a universal verdict on a live model.

After the assertions pass, write one compact `grader_report.json`. It records the positive-class sentence, the `0.0` zero-division policy, case count, all four outcomes, precision, and recall. This avoids making a future consumer scrape notebook output to discover a number or infer a policy. The report is useful on its own: a dashboard, change review, or later lesson can load one machine-readable object and still see what “positive” meant.

Persistence has one last trap. A successful `write_text` call does not prove that the next reader will receive the intended structure. Reload the JSON file immediately and compare it with the in-memory report. The final visible `PASS` appears only after that round trip. This small check catches path mistakes, serialization changes, and accidental changes to the declared fields while they are still local and cheap to fix.

The complete artifact chain is now explicit: `eval_cases.jsonl` supplies human labels, `judge_predictions.jsonl` supplies aligned judge decisions, and `grader_report.json` supplies auditable metrics. The notebook never calls a provider or needs a key, so another person can replay the same results offline. For live model evaluation later, keep the identity, validation, and report contracts; replace only the cached fixture with deliberately collected new evidence.

<svg viewBox="0 0 860 170" width="100%" role="img" aria-labelledby="capstone-title capstone-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="capstone-title">The cumulative course artifact chain</title><desc id="capstone-desc">Evaluation cases flow into judge predictions, which flow into a grader report containing the confusion matrix, precision, and recall.</desc><defs><marker id="capstone-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle"><rect x="20" y="35" width="235" height="100" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="137" y="68" font-size="16" font-weight="700" fill="#172554">eval_cases.jsonl</text><text x="137" y="96" font-size="14" fill="#1e3a8a">Human labels · 10 IDs</text><path d="M259 85H309" stroke="#475569" stroke-width="2" marker-end="url(#capstone-arrow)"/><rect x="315" y="35" width="235" height="100" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="432" y="68" font-size="16" font-weight="700" fill="#2e1065">judge_predictions.jsonl</text><text x="432" y="96" font-size="14" fill="#4c1d95">Judge labels · reasons</text><path d="M554 85H604" stroke="#475569" stroke-width="2" marker-end="url(#capstone-arrow)"/><rect x="610" y="35" width="230" height="100" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="725" y="68" font-size="16" font-weight="700" fill="#064e3b">grader_report.json</text><text x="725" y="96" font-size="14" fill="#065f46">Counts · precision · recall</text></g>
</svg>

### Checkpoint: Produce an auditable grader

Run the notebook from a fresh kernel. You pass when it validates and joins at least ten records by `case_id`, prints case-level outcomes and the exact oracle, writes and reloads `grader_report.json`, and ends with `FINAL PASS`.

## Build-along — Measure the grader (18 minutes)

Open `build/lesson-03/lesson-03.ipynb`. Complete `TODO 1` by implementing the identity index and joining only after the two ID sets and copied labels agree. Complete `TODO 2A` by mapping the four human/judge label pairs to TP, FP, FN, and TN, then complete `TODO 2B` by classifying every case and writing the code that counts each outcome. Complete `TODO 3` by translating `TP / (TP + FP)` and `TP / (TP + FN)` directly into Python, including a `0.0` branch for each zero denominator. Run each cell after its TODO; the visible checks isolate mistakes before the report is written.

| You consume | You produce | Visible final result |
| --- | --- | --- |
| `eval_cases.jsonl` and `judge_predictions.jsonl` | `build/lesson-03/grader_report.json` | TP=3, FP=1, FN=2, TN=4, precision=0.75, recall=0.6, PASS |

The notebook uses only Python's standard library; the optional notebook runner is pinned in `build/lesson-03/requirements.txt`. Finish only when the final visible result is `FINAL PASS`.
