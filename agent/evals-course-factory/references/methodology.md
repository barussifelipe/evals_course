# Evaluation methodology

## Identifier glossary

| Prefix | Meaning | Example |
| --- | --- | --- |
| `EP` | Epic/lesson | `EP-01` |
| `US` | User story/section | `US-L01-02` |
| `CP` | Observable checkpoint | `CP-L01-02-A` |
| `CLM` | Research-supported claim | `CLM-L01-004` |
| `SRC` | Source | `SRC-L01-003` |
| `EV` | Evidence used by a judge | `EV-BJ-L01-007` |
| `CHK` | Deterministic check | `CHK-BUILD-012` |
| `DEF` | Review defect | `DEF-BJ-L01-003` |
| `REV` | Review record | `REV-BUILDER-L01-02` |
| `DEC` | Orchestrator decision | `DEC-L01-005` |

IDs are locators, not proof. Each ID must resolve within its artifact to a description and a precise file, URL, field, section, cell, command, or output location.

## Ratings and weights

Every rubric aspect receives an integer rating:

| Rating | Anchor |
| ---: | --- |
| 1 | Invalid, absent, or unusable |
| 2 | Major deficiencies |
| 3 | Partially meets requirements |
| 4 | Meets requirements |
| 5 | Exceeds requirements with strong evidence |

Calculate each aspect and total as:

```text
weighted_score = weight * rating / 5
raw_penalty_total = sum(fixed behavioral penalties)
penalty_total = min(raw_penalty_total, 10)
total_score = max(0, sum(weighted_score) - penalty_total)
```

The unpenalized scale therefore ranges from 20 to 100. Report weights, ratings, weighted scores, behavioral penalty IDs and evidence, the capped penalty total, and the recomputed final score. Do not use an overall impression to override the calculation.

## Behavioral penalties

Use only the fixed catalog in `../rubrics/behavior-penalties.md`. Penalties track the agent's workflow behavior outside content quality and are capped at 10 points. Each penalty requires observable `EV` evidence, has a fixed value, and may appear at most once per reviewed artifact. Unknown IDs, discretionary values, duplicate IDs, or unsupported penalties invalidate the review.

Do not double-count content defects. Weak research, unclear writing, incorrect code, or incomplete planning affect their weighted aspects. Unauthorized actions, stale assigned inputs, gate bypasses, ownership violations, excess revision rounds, missing or falsified provenance, and concealed failures are behavioral candidates only when they match the catalog exactly.

## Verdict gates

- Approved: at least 85, every aspect at least 3, all hard checks pass, no critical defect.
- Targeted revision: 70-84.99 when no critical failure exists.
- Substantial revision: 50-69.99.
- Rejected: below 50 or any critical hard-constraint failure.

Numerical score never overrides a hard gate. Maximum two remediation rounds per agent artifact.

## Cold-review protocol

The judge receives the assignment, applicable context revision, candidate artifact, fixed rubric, and deterministic outputs. Withhold private reasoning, intended answer, target score, and earlier reviews. The judge must provide evidence-backed strengths, defects, and testable remediation criteria. Qualitative feedback must explain consequences, not merely restate the score.

## Deterministic checks

Each `CHK` record specifies its command or method, expected condition, actual observation, pass/fail state, and failure severity. Typical hard checks cover file presence, limits, notebook clean execution, output equality, offline replay, artifact handoff, Python version, dependency pins, and package size. Judges may add qualitative findings, but must not relabel a failed hard check as passing.
