# Searcher rubric

| Aspect | Weight |
| --- | ---: |
| Primary-source and paper quality | 20 |
| Claim-to-source entailment | 25 |
| Coverage of planned concepts and failure modes | 15 |
| Citation completeness and resolvability | 15 |
| Technical accuracy and appropriate qualifications | 15 |
| Seminal/recent source balance | 5 |
| Builder-ready structured handoff | 5 |

## Approved deterministic checklist

| Check ID | Measure | Required output |
| --- | --- | --- |
| `CHK-SEARCH-001` | Resolvable-claim percentage | Report `claims with at least one resolvable source / all material claims × 100`. |
| `CHK-SEARCH-002` | Central-claim primary-source percentage | Report `central claims supported by a primary or authoritative source / all central claims × 100`; target at least 80%. |
| `CHK-SEARCH-003` | Duplicate-source rate | Report duplicate source records divided by all source records, with duplicates identified. |
| `CHK-SEARCH-004` | Missing metadata count | Count sources missing required title, authors, year, source type, URL, or authority note. |
| `CHK-SEARCH-005` | Planned-topic coverage | Report approved plan concepts with adequate evidence divided by all approved plan concepts, with gaps identified. |

The checklist measures evidence quality and coverage; it does not impose a paper-count quota. Relevance and claim support take precedence over volume.

Hard failures include fabricated sources, central claims contradicted by their sources, or missing support for a concept necessary to build the lesson safely.
