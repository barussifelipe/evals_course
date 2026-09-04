# Lesson 01: Make regressions measurable

You cannot measure “worse.” You can measure a named failure, consistently labeled examples, and a dataset that proves it is structurally sound.

<svg viewBox="0 0 920 180" width="100%" role="img" aria-labelledby="lesson-map-title lesson-map-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="lesson-map-title">Lesson progression from product concern to reusable evaluation set</title>
  <desc id="lesson-map-desc">Four connected stages: name one observable regression, define label one as regression present, store cases with stable identifiers, and validate then persist the dataset.</desc>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="30" width="190" height="105" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="115" y="67" font-size="17" font-weight="700" fill="#172554">Name the failure</text><text x="115" y="96" font-size="14" fill="#1e3a8a">Observable criterion</text><text x="115" y="117" font-size="14" fill="#1e3a8a">One product risk</text>
    <path d="M214 82H249" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="255" y="30" width="190" height="105" rx="14" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="350" y="67" font-size="17" font-weight="700" fill="#2e1065">Fix the labels</text><text x="350" y="96" font-size="14" fill="#4c1d95">1 = regression</text><text x="350" y="117" font-size="14" fill="#4c1d95">0 = absent</text>
    <path d="M449 82H484" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="490" y="30" width="190" height="105" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="585" y="67" font-size="17" font-weight="700" fill="#022c22">Build the records</text><text x="585" y="96" font-size="14" fill="#064e3b">Stable case IDs</text><text x="585" y="117" font-size="14" fill="#064e3b">Inspectable evidence</text>
    <path d="M684 82H719" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="725" y="30" width="175" height="105" rx="14" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="812" y="67" font-size="17" font-weight="700" fill="#431407">Prove the handoff</text><text x="812" y="96" font-size="14" fill="#7c2d12">Validate</text><text x="812" y="117" font-size="14" fill="#7c2d12">Write + read back</text>
  </g>
</svg>

By the end, you will have `eval_cases.jsonl`: ten reviewed cases that the next lesson can consume without guessing what any label means.

## Name the regression before measuring it (about 3 minutes)

An AI feature can feel worse long before a dashboard can prove it. A support agent may invent refund eligibility, a summarizer may omit a warning, or a retrieval assistant may answer beyond its sources. “The output seems bad” is a signal to investigate, but it is not an evaluation target.

Start with one rule that a reviewer can apply using only the stored input and candidate output:

> **Regression criterion:** The support reply states that a customer is eligible for a refund when the supplied policy says the request is outside the refund window.

The criterion is observable because the record contains both pieces of evidence: the policy and request in `input`, and the reply in `candidate_output`. It asks one narrow question. Friendliness, concision, and formatting remain product concerns, but they do not decide this label.

| Raw example | Labeled evaluation case |
| --- | --- |
| Gives the system something to answer | Preserves the input **and** candidate output |
| May look realistic | States the decision rule |
| Cannot establish pass or failure alone | Records a human decision against that rule |

This distinction prevents a common dead end: collecting plausible prompts that cannot reveal whether a response passed. NIST’s Measure guidance calls for documented test sets and performance or assurance criteria under relevant conditions; the course inference is that each stored case needs enough evidence to apply the criterion ([See more here](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

Keep the first criterion small. If harmful tone or a missing citation also matters, give it a separate criterion rather than quietly mixing preferences into this label. Validation is evidence against requirements for a specific intended use, and outputs require interpretation in context ([See more here](https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/)). The notebook prints the criterion first so the dataset’s meaning stays visible.

A useful test is to imagine two reviewers working separately. Give each reviewer the policy, request, reply, and criterion—but no extra explanation. Could they point to the same sentence in the reply and reach the same label? If one reviewer is judging helpfulness while the other is judging refund eligibility, the criterion is still too broad. Rewrite it until the disagreement is about evidence, not about which quality dimension was intended. That small discipline pays off later: when the automated judge disagrees with a human label, you can inspect one boundary instead of debating whether “good” secretly meant safe, polite, accurate, or all three.

## Define the positive class (about 3 minutes)

Binary labels become useful only after their meaning is fixed. In this course, the positive class is the behavior we want to catch:

<svg viewBox="0 0 760 240" width="100%" role="img" aria-labelledby="labels-title labels-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="labels-title">Decision boundary for human labels</title>
  <desc id="labels-desc">A candidate reply is labeled one when it grants an out-of-window refund and zero when that regression is absent. Tone does not cross this decision boundary.</desc>
  <rect x="20" y="25" width="720" height="190" rx="16" fill="#f8fafc" stroke="#cbd5e1"/>
  <line x1="380" y1="48" x2="380" y2="150" stroke="#64748b" stroke-width="2" stroke-dasharray="7 7"/>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <text x="200" y="65" font-size="20" font-weight="700" fill="#166534">human_label = 0</text><text x="200" y="102" font-size="15" fill="#14532d">Regression absent</text><text x="200" y="132" font-size="14" fill="#334155">“The 30-day window has passed.”</text>
    <text x="560" y="65" font-size="20" font-weight="700" fill="#991b1b">human_label = 1</text><text x="560" y="102" font-size="15" fill="#7f1d1d">Regression present</text><text x="560" y="132" font-size="14" fill="#334155">“You are eligible for a refund.”</text>
    <path d="M113 171H647" stroke="#7c3aed" stroke-width="3"/><text x="380" y="198" font-size="14" font-weight="600" fill="#4c1d95">Tone may vary here; it does not determine this label.</text>
  </g>
</svg>

| Label | Exact meaning | What it does **not** mean |
| ---: | --- | --- |
| `1` | The reply grants a refund outside the stated window | The prose is rude or imperfect |
| `0` | That specific regression is absent | The answer is flawless in every respect |

A warm, polished reply that promises the prohibited refund is still `1`. A terse reply that correctly denies eligibility is `0`. Reviewers need this same decision boundary or the labels will encode personal preferences instead of the regression the team intends to detect.

NIST connects valid evaluation to stated requirements and intended use, while its Measure function calls for criteria measured in relevant conditions ([See more here](https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/)). The `1`/`0` polarity is an approved course convention, not a universal standard. Later, precision and recall will measure how well a grader detects cases labeled `1`. For now, every label should be explainable in one sentence. If it is not, revise the criterion or case before adding rows.

Use the criterion as a yes-or-no question: “Does this reply grant an out-of-window refund?” If yes, record `1`; if no, record `0`. Do not ask whether the reply is generally satisfactory. For example, “The normal window has passed, but I have approved a refund anyway” is still `1` because it grants the refund. “I cannot approve a refund, but I can escalate the request” is `0` because escalation is not eligibility. These near-boundary examples are more valuable than obviously good and obviously bad replies because they expose whether the rule is precise enough to apply.

Write the positive-class sentence beside the data, not only in your head. A future reader seeing `human_label: 1` should not need to infer whether `1` means success, failure, customer satisfaction, or regression. This course deliberately makes the unwanted behavior positive because the grader’s job is to detect it. That choice will make Lesson 3’s language natural: a true positive is a regression correctly caught, while a false negative is a regression the judge missed.

## Create cases with stable identities (about 3 minutes)

Turn each decision into a record that can survive sorting, filtering, and joins. The course uses four fields:

| Field | Purpose | Required invariant |
| --- | --- | --- |
| `case_id` | Joins the same case across lesson artifacts | Non-empty, unique string |
| `input` | Stores the policy fact and customer request | String with evidence needed to judge |
| `candidate_output` | Stores the reply under evaluation | String a reviewer can inspect |
| `human_label` | Preserves human ground truth | Integer `0` or `1` |

<svg viewBox="0 0 860 170" width="100%" role="img" aria-labelledby="identity-title identity-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="identity-title">Stable case identity across lesson artifacts</title>
  <desc id="identity-desc">The case identifier refund-window-001 links the evaluation case in lesson one to judge predictions in lesson two and grader metrics in lesson three.</desc>
  <defs><marker id="identity-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" text-anchor="middle">
    <rect x="20" y="40" width="220" height="90" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/><text x="130" y="72" font-size="15" font-weight="700" fill="#064e3b">Lesson 1 · ground truth</text><text x="130" y="103" font-family="ui-monospace, monospace" font-size="14" fill="#065f46">refund-window-001</text>
    <path d="M244 85H314" stroke="#475569" stroke-width="2" marker-end="url(#identity-arrow)"/>
    <rect x="320" y="40" width="220" height="90" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="430" y="72" font-size="15" font-weight="700" fill="#1e3a8a">Lesson 2 · prediction</text><text x="430" y="103" font-family="ui-monospace, monospace" font-size="14" fill="#1e40af">refund-window-001</text>
    <path d="M544 85H614" stroke="#475569" stroke-width="2" marker-end="url(#identity-arrow)"/>
    <rect x="620" y="40" width="220" height="90" rx="12" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/><text x="730" y="72" font-size="15" font-weight="700" fill="#7c2d12">Lesson 3 · metrics</text><text x="730" y="103" font-family="ui-monospace, monospace" font-size="14" fill="#9a3412">refund-window-001</text>
  </g>
</svg>

Readable identifiers such as `refund-window-001` are enough for this small local dataset. UUIDs are useful when identifiers must be generated independently at larger scale, but they are not required. RFC 9562 supports the broader identity goal by defining persistent, decentralized identifiers ([See more here](https://www.rfc-editor.org/rfc/rfc9562.html)).

The notebook creates ten cases: five regression cases and five acceptable cases. Ten is large enough to make the later confusion matrix less brittle than a four-case toy, but it is only a course fixture—not a claim of statistical sufficiency. The cases vary request timing and reply wording while keeping one decision boundary. That variation gives the judge realistic opportunities to disagree without changing what the label means.

Treat `case_id` as identity, not decoration. If you correct wording in `candidate_output`, keep the ID only when it remains the same evaluation case; create a new ID when the underlying scenario or intended judgment changes. Never recycle an ID for unrelated evidence. Later lessons copy these IDs into prediction records and join on them, so a duplicated or repurposed ID can silently compare a prediction with the wrong human label. Row numbers cannot provide that guarantee because sorting or filtering changes them.

The notebook writes the records as JSON Lines (JSONL), one valid JSON value per UTF-8 line ([See more here](https://jsonlines.org/)). One-record-per-line storage keeps the small artifact easy to inspect and process incrementally. The four-field schema is a course interface decision, not a source-mandated standard ([See more here](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)). Resist adding speculative fields now: the next lesson needs only stable identity, the evidence shown to the judge, and the human reference label.

## Validate before automating (about 3 minutes)

Writing a file is not proof that it is an evaluation set. Validate at the shared boundary, while malformed ground truth is still easy to diagnose.

| Check | Failure prevented |
| --- | --- |
| Required fields and string types | Missing evidence for a later judgment |
| Non-empty, unique `case_id` values | Ambiguous joins between artifacts |
| Exact integer label domain `{0, 1}` | Schema drift such as `"1"` or `true` |
| At least one case from each class | A demo that cannot exercise both outcomes |
| Write, read back, compare | A persisted artifact that differs from memory |

<svg viewBox="0 0 900 155" width="100%" role="img" aria-labelledby="validation-title validation-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="validation-title">Validation and persistence pipeline</title>
  <desc id="validation-desc">In-memory records pass schema, identity, and class checks before being written to JSONL, read back, and compared for equality.</desc>
  <defs><marker id="validation-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#475569"/></marker></defs>
  <g font-family="system-ui, sans-serif" font-size="14" text-anchor="middle">
    <rect x="15" y="45" width="135" height="60" rx="12" fill="#f8fafc" stroke="#64748b"/><text x="82" y="80" fill="#0f172a">Records</text><path d="M154 75H189" stroke="#475569" stroke-width="2" marker-end="url(#validation-arrow)"/>
    <rect x="195" y="45" width="135" height="60" rx="12" fill="#eff6ff" stroke="#2563eb"/><text x="262" y="72" fill="#1e3a8a">Schema +</text><text x="262" y="91" fill="#1e3a8a">identity</text><path d="M334 75H369" stroke="#475569" stroke-width="2" marker-end="url(#validation-arrow)"/>
    <rect x="375" y="45" width="135" height="60" rx="12" fill="#f5f3ff" stroke="#7c3aed"/><text x="442" y="72" fill="#4c1d95">Class</text><text x="442" y="91" fill="#4c1d95">presence</text><path d="M514 75H549" stroke="#475569" stroke-width="2" marker-end="url(#validation-arrow)"/>
    <rect x="555" y="45" width="135" height="60" rx="12" fill="#ecfdf5" stroke="#059669"/><text x="622" y="80" fill="#064e3b">Write JSONL</text><path d="M694 75H729" stroke="#475569" stroke-width="2" marker-end="url(#validation-arrow)"/>
    <rect x="735" y="45" width="150" height="60" rx="12" fill="#fff7ed" stroke="#ea580c"/><text x="810" y="72" fill="#7c2d12">Read back</text><text x="810" y="91" fill="#7c2d12">= PASS</text>
  </g>
</svg>

Requiring both classes is a bounded course decision for this tiny fixture, not a universal balance rule or proof of statistical representativeness. It ensures the learner sees an acceptable case beside a regression and prepares later lessons to exercise both sides of the binary interface.

JSONL defines the record-per-line representation but does not enforce schema or uniqueness; explicit validation and read-back comparison provide those safeguards ([See more here](https://jsonlines.org/)). Lesson 2 will consume the resulting file while preserving `case_id` and `human_label`, even when an automated judge disagrees.

Pay attention to Python’s edge cases while validating. Because `bool` is a subclass of `int`, a loose integer check can accidentally accept `true` as label `1`; the notebook therefore checks the exact allowed values and types. Empty IDs deserve their own failure even if they are technically strings, and uniqueness must be checked across the whole collection rather than one row at a time. Each error message should identify the broken condition early, before Lesson 2 turns a malformed row into a misleading judge prediction.

The final read-back check tests a different boundary. In-memory records can be correct while the persisted file is truncated, encoded unexpectedly, or written in a different shape. Reloading every JSONL line and comparing the result with the original records proves that the artifact handed to Lesson 2 is the artifact you inspected. It does not prove the labels are objectively perfect; it proves the file preserved the reviewed decisions exactly. That narrower promise is both testable and useful.

### Checkpoint: Validate the dataset

Run the notebook from a fresh kernel. You pass when it creates `eval_cases.jsonl`, reports no missing fields, invalid labels, or duplicate IDs, prints counts for both `0` and `1`, and ends with a read-back `PASS`. If a check fails, fix the named record before continuing.

## Build-along — Build a validated regression set (18 minutes)

Open `build/lesson-01/lesson-01.ipynb` in Jupyter. Complete `TODO 1` by writing the observable regression criterion. Then complete `TODO 2`: write each candidate reply and assign its `human_label`. Run each cell after completing its TODO; the supplied checks explain what remains incomplete before the final JSONL write.

| What you use | What you produce | What the next lesson inherits |
| --- | --- | --- |
| Python 3.12, standard library, ten case prompts | `build/lesson-01/eval_cases.jsonl` | Stable `case_id` values and fixed human-label semantics |

The optional notebook runner is pinned in `build/lesson-01/requirements.txt`. Finish only when the notebook’s last visible result is `PASS`.
