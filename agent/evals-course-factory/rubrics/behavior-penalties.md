# Agent behavior penalty rubric

Penalties measure observable workflow violations by the judgee. They do not measure the quality of a plan, research artifact, lesson, notebook, or other content; content quality belongs in the weighted aspects. A hard-gate failure remains a hard gate and must not be converted into a penalty.

## Fixed catalog

| Penalty ID | Points | Observable behavior |
| --- | ---: | --- |
| `PEN-001` | 2 | Used a `CONTEXT.md`, plan, research, or artifact revision different from the revision assigned in the task brief. |
| `PEN-002` | 3 | Started a gated phase before the preceding judge approval or required human decision was recorded. |
| `PEN-003` | 4 | Modified an artifact owned by another agent instead of returning feedback or editing only the judgee's owned artifact. |
| `PEN-004` | 2 | Performed work outside the explicitly assigned phase or lesson scope, even though the extra work did not itself trigger a hard failure. |
| `PEN-005` | 2 | Continued remediation after the maximum two revision rounds without a new human authorization. |
| `PEN-006` | 3 | Omitted or falsified a required workflow/provenance record, such as the artifact revision, context revision, executed command, or handoff status. |
| `PEN-007` | 5 | Performed a Git or external-state mutation that was not authorized for that run, excluding merges, which are prohibited hard failures. |
| `PEN-008` | 5 | Failed to disclose an observed tool/check failure or represented a failed/not-run check as passing. |

## Application rules

1. Apply a penalty only when a `PEV` record in the separate penalty-evidence registry shows the behavior occurred. Do not infer behavior from weak content and do not use quality evidence (`EV`) to support a penalty.
2. Apply each penalty ID at most once per reviewed artifact, even when the same behavior occurred repeatedly. Describe repeated occurrences in the evidence.
3. Use the fixed point value. Judges cannot invent IDs, change values, or create discretionary deductions.
4. List every evidenced penalty, calculate the raw sum, and set `penalty_total = min(raw sum, 10)`.
5. Calculate `total_score = max(0, sum(weight * rating / 5) - penalty_total)`.
6. Never penalize a problem already expressed only as content quality. For example, weak citations reduce the citation aspect; they do not receive a behavioral penalty.
7. A behavior may affect both a gate and a penalty only when the rules explicitly distinguish them. The merge prohibition is always a hard failure and never a penalty.

When no behavioral violation is evidenced, return empty `penalties` and `penalty_evidence` arrays and `penalty_total: 0`.
