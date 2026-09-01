"""Recompute a cold-review score and enforce the fixed verdict gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def evaluate(review: dict) -> tuple[float, str, list[str]]:
    errors: list[str] = []
    aspects = review.get("aspects", [])
    weight_total = sum(float(item["weight"]) for item in aspects)
    if abs(weight_total - 100.0) > 1e-9:
        errors.append(f"aspect weights total {weight_total}, expected 100")

    calculated = 0.0
    for item in aspects:
        rating = int(item["rating"])
        if rating not in range(1, 6):
            errors.append(f"{item['name']}: rating {rating} is outside 1..5")
        expected = float(item["weight"]) * rating / 5
        calculated += expected
        if abs(float(item["weighted_score"]) - expected) > 0.01:
            errors.append(f"{item['name']}: weighted score should be {expected:.2f}")

    penalty_catalog = {
        "PEN-001": 2,
        "PEN-002": 3,
        "PEN-003": 4,
        "PEN-004": 2,
        "PEN-005": 2,
        "PEN-006": 3,
        "PEN-007": 5,
        "PEN-008": 5,
    }
    seen_penalties: set[str] = set()
    raw_penalty_total = 0.0
    for penalty in review.get("penalties", []):
        penalty_id = penalty.get("penalty_id")
        if penalty_id not in penalty_catalog:
            errors.append(f"unknown behavioral penalty {penalty_id}")
            continue
        if penalty_id in seen_penalties:
            errors.append(f"duplicate behavioral penalty {penalty_id}")
            continue
        seen_penalties.add(penalty_id)
        expected_points = penalty_catalog[penalty_id]
        if float(penalty.get("points", -1)) != expected_points:
            errors.append(f"{penalty_id}: points should be {expected_points}")
        if not penalty.get("evidence_ids"):
            errors.append(f"{penalty_id}: at least one evidence ID is required")
        raw_penalty_total += expected_points

    penalty_total = min(raw_penalty_total, 10.0)
    if abs(float(review.get("penalty_total", -1)) - penalty_total) > 0.01:
        errors.append(f"penalty total should be {penalty_total:.2f}")
    calculated -= penalty_total
    calculated = round(max(0.0, calculated), 2)
    if abs(float(review.get("total_score", -1)) - calculated) > 0.01:
        errors.append(f"total score should be {calculated:.2f}")

    critical = any(item.get("severity") == "critical" for item in review.get("defects", []))
    hard_failure = any(not item["passed"] and item["severity"] == "critical" for item in review.get("deterministic_checks", []))
    below_aspect_floor = any(int(item["rating"]) < 3 for item in aspects)
    if critical or hard_failure:
        verdict = "rejected"
    elif calculated >= 85 and not below_aspect_floor:
        verdict = "approved"
    elif calculated >= 70:
        verdict = "targeted_revision"
    elif calculated >= 50:
        verdict = "substantial_revision"
    else:
        verdict = "rejected"
    if review.get("verdict") != verdict:
        errors.append(f"verdict should be {verdict}")
    return calculated, verdict, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    score, verdict, errors = evaluate(review)
    print(json.dumps({"score": score, "verdict": verdict, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
