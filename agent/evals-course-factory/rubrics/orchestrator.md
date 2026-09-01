# Orchestrator rubric

| Aspect | Weight |
| --- | ---: |
| Assignment constraint coverage and traceability | 20 |
| Breaking points and observable checkpoints | 20 |
| Backward design from the capstone | 20 |
| Prerequisite and artifact dependency correctness | 15 |
| Task briefs and agent interface clarity | 10 |
| Offline and reproducibility strategy | 10 |
| Context consistency and change tracking | 5 |

## Approved deterministic checklist

| Check ID | Check | Pass condition |
| --- | --- | --- |
| `CHK-ORCH-001` | Lesson limit | The course plan contains 2-3 lessons, and the current run plans no more than one lesson. |
| `CHK-ORCH-002` | Section limit | The current lesson contains 1-5 user stories/sections. |
| `CHK-ORCH-003` | Required artifact declarations | The lesson declares its input artifact, output artifact, offline replay method, and next-lesson interface. |
| `CHK-ORCH-004` | Checkpoint presence | The lesson contains 1-3 observable checkpoints, each assigned within a user story. |
| `CHK-ORCH-005` | Build-along count | The lesson ends with exactly one build-along whose estimated learner time is no more than 20 minutes. |
| `CHK-ORCH-006` | Capstone traceability | Every lesson checkpoint and output artifact traces to an explicit capstone acceptance criterion. |

Hard failures include planning more than one lesson for the run, generating content before breaking points/checkpoints, an untraceable capstone, an impossible dependency, or granting an agent merge authority.
