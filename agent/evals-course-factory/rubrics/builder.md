# Builder rubric

| Aspect | Weight |
| --- | ---: |
| Technical correctness | 20 |
| Build-along execution and offline reproducibility | 20 |
| Capstone contribution or completion | 15 |
| Artifact compounding across lessons | 10 |
| Checkpoint and prerequisite alignment | 10 |
| Assignment shape and time compliance | 10 |
| Research and citation fidelity | 10 |
| Pedagogical clarity at breaking points | 5 |

## Approved deterministic checklist

| Check ID | Check | Pass condition |
| --- | --- | --- |
| `CHK-BUILD-001` | Command completion | Every documented canonical execution command exits successfully. |
| `CHK-BUILD-002` | Expected outputs | Every declared output and persisted lesson artifact exists after execution. |
| `CHK-BUILD-003` | Grader report | The completed grader prints TP, FP, FN, TN, precision, and recall. Before the final lesson, the current increment must print every metric it claims to implement. |
| `CHK-BUILD-004` | Independent metric verification | Printed precision and recall match values independently recomputed from the produced TP, FP, and FN counts, including defined zero-denominator behavior. |
| `CHK-BUILD-005` | Offline replay | The canonical review path completes from fixtures or cached responses with network access unavailable and no paid API call. |
| `CHK-BUILD-006` | Runtime and dependency pins | Python 3.12 is specified and every non-standard dependency is pinned in `requirements.txt`. |
| `CHK-BUILD-007` | Build-along count | Every completed lesson ends with exactly one incremental build-along. |
| `CHK-BUILD-008` | Course shape | Every completed lesson has at most five sections, and every section contains 300-500 words teaching one idea. |
| `CHK-BUILD-009` | Package size | The complete submission archive remains under 10 MB. Before packaging, report this check as not applicable rather than passing it without evidence. |

Hard failures include notebook execution failure from a fresh kernel, paid/network dependency during review, missing visible checks, failure to persist the promised artifact, broken input from the previous epic, or inability to progress toward the capstone.
