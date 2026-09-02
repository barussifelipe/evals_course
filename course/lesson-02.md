# Lesson 02: Turn a rubric into judge predictions

An automated judge is useful only when its decision boundary is as inspectable as the human labels it will later be compared with. This lesson turns the Lesson 01 cases into replayable, case-level judge predictions—not a score.

<svg viewBox="0 0 920 180" width="100%" role="img" aria-labelledby="judge-map-title judge-map-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="judge-map-title">Lesson progression from rubric to reusable judge predictions</title>
  <desc id="judge-map-desc">Four connected stages: bound the rubric, cache judge responses, validate and align by case identifier, then inspect disagreements and persist predictions.</desc>
  <defs><marker id="judge-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="30" width="190" height="105" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="115" y="67" font-size="17" font-weight="700" fill="#172554">Bound the rubric</text><text x="115" y="96" font-size="14" fill="#1e3a8a">One regression</text><text x="115" y="117" font-size="14" fill="#1e3a8a">No label leakage</text>
    <path d="M214 82H249" stroke="#475569" stroke-width="2" marker-end="url(#judge-arrow)"/><rect x="255" y="30" width="190" height="105" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="350" y="67" font-size="17" font-weight="700" fill="#2e1065">Cache responses</text><text x="350" y="96" font-size="14" fill="#4c1d95">Verdict + reason</text><text x="350" y="117" font-size="14" fill="#4c1d95">Offline replay</text>
    <path d="M449 82H484" stroke="#475569" stroke-width="2" marker-end="url(#judge-arrow)"/><rect x="490" y="30" width="190" height="105" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="585" y="67" font-size="17" font-weight="700" fill="#022c22">Validate + align</text><text x="585" y="96" font-size="14" fill="#064e3b">Strict contract</text><text x="585" y="117" font-size="14" fill="#064e3b">Stable case IDs</text>
    <path d="M684 82H719" stroke="#475569" stroke-width="2" marker-end="url(#judge-arrow)"/><rect x="725" y="30" width="175" height="105" rx="14" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="812" y="67" font-size="17" font-weight="700" fill="#431407">Inspect the gap</text><text x="812" y="96" font-size="14" fill="#7c2d12">Keep reasons</text><text x="812" y="117" font-size="14" fill="#7c2d12">Persist predictions</text>
  </g>
</svg>

By the end, you will have `judge_predictions.jsonl`: one validated judge prediction per Lesson 01 case, ready for the grader in Lesson 03.

## Bound the judge with one rubric (about 3 minutes)

The previous lesson made the human decision explicit: `human_label = 1` means a reply grants a refund when the policy says the request is outside the 30-day window. That label is reference evidence. It is not an instruction to hand to a model judge. If a prompt includes it, the model can echo the answer instead of evaluating the case, and any apparent agreement becomes meaningless.

Write one bounded rubric instead. Its task is narrow: decide whether the candidate reply commits this specific refund-window regression. Its positive mapping is equally narrow: `REGRESSION_PRESENT` maps to `judge_label = 1`; `REGRESSION_ABSENT` maps to `judge_label = 0`. The judge may use only the stored `input` and `candidate_output`. It must ignore tone, detail, formatting, general helpfulness, and every other quality that is not the rule.

<svg viewBox="0 0 760 230" width="100%" role="img" aria-labelledby="rubric-title rubric-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="rubric-title">Evidence boundary between the judge request and hidden reference label</title>
  <desc id="rubric-desc">Input and candidate output enter the bounded rubric. Human label stays outside the request and is used only later for comparison.</desc>
  <defs><marker id="rubric-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="35" width="180" height="70" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="110" y="63" font-size="15" font-weight="700" fill="#172554">Allowed evidence</text><text x="110" y="87" font-size="14" fill="#1e3a8a">input + candidate_output</text>
    <path d="M204 70H279" stroke="#475569" stroke-width="2" marker-end="url(#rubric-arrow)"/><rect x="285" y="35" width="190" height="70" rx="12" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="380" y="63" font-size="15" font-weight="700" fill="#2e1065">Bounded rubric</text><text x="380" y="87" font-size="14" fill="#4c1d95">Present or absent</text>
    <path d="M479 70H554" stroke="#475569" stroke-width="2" marker-end="url(#rubric-arrow)"/><rect x="560" y="35" width="180" height="70" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="650" y="63" font-size="15" font-weight="700" fill="#022c22">Judge response</text><text x="650" y="87" font-size="14" fill="#064e3b">verdict + reason</text>
    <rect x="250" y="145" width="260" height="58" rx="12" fill="#fff7ed" stroke="#ea580c" stroke-width="2" stroke-dasharray="7 5"/><text x="380" y="170" font-size="15" font-weight="700" fill="#7c2d12">human_label stays hidden</text><text x="380" y="190" font-size="13" fill="#9a3412">Reference evidence, never prompt input</text>
  </g>
</svg>

This is more than prompt tidiness. Criteria-driven judging asks the evaluator to receive an evaluation task and explicit criteria, then return a constrained form-like result instead of an unconstrained quality impression ([CLM-L02-RUBRIC-001](https://aclanthology.org/2023.emnlp-main.153/)). Here, the form is deliberately small: one verdict and one evidence-based reason. It gives a reviewer a concrete thing to inspect when the output seems surprising.

Keep the wording tied to evidence visible in each record. For a day-45 request, a reply that says “eligible for a full refund” is present. A reply that says the 30-day window has passed is absent. For a day-12 request, a refund may be appropriate, so the same word “refund” is not enough by itself. The policy, request date, and claim in the reply must be read together.

Do not let a polished answer drift the verdict. Research on LLM judges reports useful agreement with human preferences alongside position, verbosity, and self-enhancement biases ([CLM-L02-BIAS-001](https://arxiv.org/abs/2306.05685)). A bounded rubric reduces irrelevant room for preference; it does not make the judge authoritative. The notebook therefore renders a request without `human_label` and keeps human labels separate until disagreement inspection.

## Make responses replayable (about 3 minutes)

Calling a provider during every review creates a moving target: the model, service, prompt handling, and bill can all change. For this lesson, cache one response per stable `case_id`. Each line contains exactly `case_id`, `verdict`, and `reason`. The response is a fixture, not a claim that a particular live model will always produce it.

| Field | Purpose | Required invariant |
| --- | --- | --- |
| `case_id` | Links the response to a Lesson 01 case | Non-empty, unique, known ID |
| `verdict` | Carries the rubric decision | Exactly one declared verdict |
| `reason` | Preserves inspectable judge evidence | Non-empty string |

<svg viewBox="0 0 860 160" width="100%" role="img" aria-labelledby="replay-title replay-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="replay-title">Cached response replay path</title>
  <desc id="replay-desc">A versioned rubric and stored cases produce cached responses once; repeated offline runs replay the same responses without a provider call.</desc>
  <defs><marker id="replay-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="42" width="180" height="72" rx="12" fill="#f8fafc" stroke="#64748b"/><text x="110" y="70" font-size="15" font-weight="700" fill="#0f172a">Cases + rubric v1</text><text x="110" y="94" font-size="13" fill="#334155">Recorded inputs</text>
    <path d="M204 78H299" stroke="#475569" stroke-width="2" marker-end="url(#replay-arrow)"/><rect x="305" y="42" width="220" height="72" rx="12" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="415" y="70" font-size="15" font-weight="700" fill="#2e1065">Cached responses</text><text x="415" y="94" font-size="13" fill="#4c1d95">Stable lesson fixture</text>
    <path d="M529 78H624" stroke="#475569" stroke-width="2" marker-end="url(#replay-arrow)"/><rect x="630" y="42" width="210" height="72" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="735" y="70" font-size="15" font-weight="700" fill="#022c22">Offline rerun</text><text x="735" y="94" font-size="13" fill="#064e3b">No key · no network · no bill</text>
  </g>
</svg>

The cache’s contract is intentionally strict. `case_id` says which Lesson 01 case the response belongs to. `verdict` may be only `REGRESSION_PRESENT` or `REGRESSION_ABSENT`. `reason` must be a non-empty, evidence-based explanation. No score, confidence, alternate label, or extra field is needed for this binary pipeline. Fewer fields leave fewer opportunities for a later step to invent a meaning it cannot justify.

Named fields and required fields are useful boundary checks: JSON Schema defines type and required assertions, and its object-property rules can reject properties not covered by the declared contract ([CLM-L02-CONTRACT-001](https://json-schema.org/draft/2020-12/json-schema-core.html)). The notebook uses small standard-library checks rather than a new schema dependency, then adds cross-record checks that a field schema cannot provide: every case must appear once and only once.

Cached replay makes the teaching path reproducible. It needs no network, API key, model weights, or paid call, so a learner can rerun parsing and alignment while inspecting exactly the same evidence. It also lets a reviewer audit why a stored prediction was produced rather than receiving a fresh opaque answer. Version the rubric text beside the code if you later change its decision rule; a response produced under a different rubric is a different evaluation input.

There is an important ceiling: cached results exercise this pipeline, not a live provider. They cannot measure current model behavior, provider changes, or response variance ([CLM-L02-CACHE-001](https://arxiv.org/abs/2306.05685)). That is acceptable here because the next lesson needs stable prediction records before it can teach measurement. Add controlled live sampling only when you are ready to study that separate question.

## Parse and align predictions (about 3 minutes)

Raw model-shaped text is not yet evaluation data. First parse each cached JSON line. Then reject a response if its keys differ from the three-field contract, its `case_id` is not a non-empty string, its verdict is outside the two declared values, or its reason is blank. An error should name the offending `case_id` when possible, so the maintainer can repair the fixture or upstream response rather than debug a downstream number.

Field validation is necessary but incomplete. A perfectly shaped response for an unknown case is still unusable. Likewise, two valid responses for one case create an ambiguous prediction, and a missing response quietly changes the evaluation population. Gather response IDs, reject duplicates, compare them with the IDs from `eval_cases.jsonl`, and stop for unknown or missing IDs. Never align by row position: sorting either file would silently pair the wrong prediction with the wrong human decision.

<svg viewBox="0 0 860 190" width="100%" role="img" aria-labelledby="alignment-title alignment-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="alignment-title">Identity-based alignment instead of row-position matching</title>
  <desc id="alignment-desc">Evaluation cases and cached responses can appear in different row orders. Both connect through matching case identifiers to produce aligned prediction records.</desc>
  <defs><marker id="alignment-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="25" width="235" height="140" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="137" y="53" font-size="15" font-weight="700" fill="#172554">Lesson 01 cases</text><text x="137" y="84" font-family="ui-monospace, monospace" font-size="13" fill="#1e3a8a">refund-window-001</text><text x="137" y="110" font-family="ui-monospace, monospace" font-size="13" fill="#1e3a8a">refund-window-002</text><text x="137" y="136" font-size="13" fill="#334155">human_label preserved</text>
    <path d="M259 95H359" stroke="#475569" stroke-width="2" marker-end="url(#alignment-arrow)"/><rect x="365" y="45" width="130" height="100" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="430" y="78" font-size="15" font-weight="700" fill="#2e1065">Join by</text><text x="430" y="107" font-family="ui-monospace, monospace" font-size="14" fill="#4c1d95">case_id</text>
    <path d="M499 95H599" stroke="#475569" stroke-width="2" marker-end="url(#alignment-arrow)"/><rect x="605" y="25" width="235" height="140" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="722" y="53" font-size="15" font-weight="700" fill="#022c22">Cached responses</text><text x="722" y="84" font-family="ui-monospace, monospace" font-size="13" fill="#065f46">refund-window-002</text><text x="722" y="110" font-family="ui-monospace, monospace" font-size="13" fill="#065f46">refund-window-001</text><text x="722" y="136" font-size="13" fill="#334155">row order may differ</text>
  </g>
</svg>

Stable identity is the shared interface across this course. The one-to-one join is an explicit course invariant built on a field-level contract, rather than a behavior the JSON Schema standard supplies by itself ([CLM-L02-ALIGN-001](https://json-schema.org/draft/2020-12/json-schema-core.html)). In practical terms, build a dictionary keyed by `case_id`, then traverse the original evaluation cases. That preserves their order for readable output while making the lookup identity-based.

The output record has four fields: `case_id`, `human_label`, `judge_label`, and `judge_reason`. Copy the first two unchanged from Lesson 01. Convert only the validated verdict: present becomes `1`; absent becomes `0`. The reason comes from the cached response unchanged so a later reviewer can see the judge’s stated evidence. The notebook asserts the copied `(case_id, human_label)` pairs match the input exactly before it writes anything.

Notice what this section does not do. It does not count correct predictions, create a confusion matrix, or calculate precision or recall. Those are EP-03 questions. This boundary protects against a tempting shortcut: scoring records before you know whether every case was represented correctly.

## Inspect disagreements before scoring (about 3 minutes)

After alignment, compare `human_label` and `judge_label` one record at a time. A disagreement row needs four columns: `case_id`, `human_label`, `judge_label`, and `judge_reason`. That compact display is the point of the artifact. It turns “the judge disagreed” into an inspectable event: find the exact policy, request, reply, and stated reason before deciding what to revise.

| Result | Human | Judge | What happens next |
| --- | ---: | ---: | --- |
| Agreement | `1` | `1` | Preserve the evidence trail |
| Disagreement | `1` | `0` | Re-read the criterion, reply, and reason |

<svg viewBox="0 0 880 175" width="100%" role="img" aria-labelledby="disagreement-title disagreement-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="disagreement-title">A disagreement becomes a review target rather than an automatic relabel</title>
  <desc id="disagreement-desc">Human and judge labels feed a comparison. A disagreement opens review of the case, rubric, and reason without silently changing either label.</desc>
  <defs><marker id="disagreement-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="50" width="165" height="70" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="102" y="78" font-size="15" font-weight="700" fill="#172554">human_label</text><text x="102" y="102" font-size="13" fill="#1e3a8a">Reference decision</text>
    <path d="M189 85H309" stroke="#475569" stroke-width="2" marker-end="url(#disagreement-arrow)"/><rect x="315" y="50" width="170" height="70" rx="12" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="400" y="78" font-size="15" font-weight="700" fill="#2e1065">Compare labels</text><text x="400" y="102" font-size="13" fill="#4c1d95">Keep both unchanged</text>
    <path d="M489 85H609" stroke="#475569" stroke-width="2" marker-end="url(#disagreement-arrow)"/><rect x="615" y="25" width="245" height="120" rx="14" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="737" y="57" font-size="15" font-weight="700" fill="#431407">If they disagree</text><text x="737" y="85" font-size="13" fill="#7c2d12">Inspect case + rubric + reason</text><text x="737" y="111" font-size="13" font-weight="700" fill="#9a3412">Do not auto-relabel</text>
  </g>
</svg>

Treat neither side as automatic truth. The human label may reflect a mistaken reading of the criterion; the cached judge may have misread the policy, imported an irrelevant preference, or applied the rubric inconsistently. LLM-as-judge studies document systematic biases even where judges show substantial agreement with human preferences ([CLM-L02-BIAS-001](https://arxiv.org/abs/2306.05685)). Do not change `human_label` just to make the table look better, and do not relabel the judge output to make it agree. Preserve the evidence and review the underlying case.

In this fixture, one disagreement is intentional. Its reason claims that a day-33 reply does not explicitly say “eligible,” although the reply says “we will process your refund.” The row gives the team a concrete rubric-review target. Perhaps the rubric needs an example clarifying that an implied approval counts; perhaps the human label or candidate text needs review. The notebook does not decide. It makes the conflict visible.

Finally, persist the records as `build/lesson-02/judge_predictions.jsonl`, reload the file, and compare it to the in-memory records. That read-back check proves the next lesson receives the same case-level evidence you inspected. Cached replay makes this artifact repeatable offline, but it does not measure live-provider variance ([CLM-L02-CACHE-001](https://aclanthology.org/2023.emnlp-main.153/)). Keep the fixture and prediction file together: a reviewer should be able to trace every stored label back to its replayed verdict without reconstructing hidden state. EP-03 will consume these exact records, verify the shared IDs and human labels again, and then compute metrics. For now, stop with a trustworthy disagreement report.

### Checkpoint: Inspect aligned judge predictions

Run the notebook from a fresh kernel. You pass when it loads every Lesson 01 case, renders a request without `human_label`, validates one cached response per case, prints the disagreement table, writes and reloads `judge_predictions.jsonl`, and ends with `PASS`.

## Build-along — Replay a bounded judge (18 minutes)

Open `build/lesson-02/lesson-02.ipynb` in Jupyter. Complete `TODO 1` by writing the bounded rubric and its two verdict mappings. Then complete `TODO 2` by declaring the cached-response contract. Run each cell after its TODO; the supplied checks explain what remains incomplete before alignment and the final JSONL write. No API key or provider is involved.

| What you use | What you produce | What EP-03 inherits |
| --- | --- | --- |
| Python 3.12, `eval_cases.jsonl`, cached responses | `build/lesson-02/judge_predictions.jsonl` | stable IDs, unchanged human labels, judge labels, reasons |

The optional notebook runner is pinned in `build/lesson-02/requirements.txt`. Finish only when the final visible result is `PASS`; do not calculate metrics in this lesson.
