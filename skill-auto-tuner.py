#!/usr/bin/env python3
"""
Skill Auto-Tune Router
======================
After 20+ runs, analyze efficacy log + quality scores + combinations
to produce an optimized routing table.

Output: ~/.agents/skill-tuned-routes.json
- Top 50 skills by quality × usage → priority routing
- Top 10 golden combinations → auto-suggest
- Bottom 20% skills → quarantine (don't suggest proactively)

Usage:
  python3 skill-auto-tuner.py          # Run analysis
  python3 skill-auto-tuner.py report    # Show human-readable report
"""

import json
import os
import math
from datetime import datetime, timedelta
from collections import Counter

AGENTS_DIR = os.path.expanduser("~/.agents")
EFFICACY_LOG = os.path.join(AGENTS_DIR, "skill-efficacy-log.json")
QUALITY_SCORES = os.path.join(AGENTS_DIR, "skill-quality-scores.json")
COMBINATIONS = os.path.join(AGENTS_DIR, "skill-combinations.json")
MASTER_INDEX = os.path.join(AGENTS_DIR, "skills-catalog", "skill_master_index.json")
TUNED_ROUTES = os.path.join(AGENTS_DIR, "skill-tuned-routes.json")

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def calculate_skill_score(skill_name, quality, efficacy_runs):
    """Calculate composite score: quality × usage × efficacy × recency."""
    q = quality.get("scores", {}).get(skill_name, {})
    rating = q.get("rating", 3)
    uses = q.get("uses", 0)
    success_rate = q.get("success_rate", 0.5)
    
    # Efficacy from runs
    skill_runs = [r for r in efficacy_runs if r.get("skill") == skill_name]
    avg_efficacy = 50
    if skill_runs:
        avg_efficacy = sum(r.get("score", 50) for r in skill_runs) / len(skill_runs)
    
    # Composite: weighted formula
    usage_factor = math.log(uses + 1) / math.log(100) if uses > 0 else 0.1
    quality_factor = rating / 5.0
    efficacy_factor = avg_efficacy / 100.0
    
    composite = quality_factor * 0.3 + efficacy_factor * 0.4 + usage_factor * 0.3
    return {
        "skill": skill_name,
        "composite": round(composite, 3),
        "rating": rating,
        "uses": uses,
        "success_rate": round(success_rate, 2),
        "avg_efficacy": round(avg_efficacy, 1),
    }

def find_golden_combinations(combos_data):
    """Find top 10 skill pairs by success_rate × log(count)."""
    pairs = combos_data.get("pairs", {})
    scored = []
    for pair_key, data in pairs.items():
        count = data.get("count", 0)
        rate = data.get("success_rate", 0.5)
        if count < 2:
            continue
        score = rate * math.log(count + 1)
        scored.append({"pair": pair_key, "score": round(score, 3), "count": count, "success_rate": rate})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:10]

def find_quarantined_skills(all_skills, quality_data, efficacy_runs):
    """Skills with low quality + low efficacy → quarantine."""
    quarantined = []
    for skill in all_skills:
        q = quality_data.get("scores", {}).get(skill, {})
        uses = q.get("uses", 0)
        if uses == 0:
            continue  # Only quarantine skills that were tried and failed
        rating = q.get("rating", 3)
        success_rate = q.get("success_rate", 0.5)
        if rating <= 2 and success_rate < 0.3:
            quarantined.append(skill)
    return quarantined[:20]

def run_analysis():
    efficacy = load_json(EFFICACY_LOG, {"runs": []})
    quality = load_json(QUALITY_SCORES, {"scores": {}})
    combos = load_json(COMBINATIONS, {"pairs": {}})
    master = load_json(MASTER_INDEX, {"skills": []})
    
    all_skills = master.get("skills", [])
    efficacy_runs = efficacy.get("runs", [])
    total_runs = len(efficacy_runs)
    
    if total_runs < 20:
        return {"status": "insufficient_data", "runs": total_runs, "needed": 20}
    
    # Score all skills that have usage data
    used_skills = [s for s in all_skills if s in quality.get("scores", {})]
    scored = [calculate_skill_score(s, quality, efficacy_runs) for s in used_skills]
    scored.sort(key=lambda x: x["composite"], reverse=True)
    
    top_skills = scored[:50]
    golden = find_golden_combinations(combos)
    quarantined = find_quarantined_skills(all_skills, quality, efficacy_runs)
    
    result = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "total_runs_analyzed": total_runs,
        "top_50_skills": top_skills,
        "golden_combinations": golden,
        "quarantined_skills": quarantined,
        "routing_priority": {
            "high": [s["skill"] for s in top_skills[:10] if s["composite"] > 0.5],
            "medium": [s["skill"] for s in top_skills[10:30] if 0.3 < s["composite"] <= 0.5],
            "low": [s["skill"] for s in top_skills[30:] if s["composite"] <= 0.3],
            "blocked": quarantined,
        },
        "auto_suggest_threshold": 0.6,
        "golden_combo_cache": [{"pair": g["pair"], "score": g["score"]} for g in golden if g["score"] > 0.6],
    }
    
    save_json(TUNED_ROUTES, result)
    return result

def print_report():
    data = load_json(TUNED_ROUTES, {})
    if not data:
        print("No tuned routes found. Run 'python3 skill-auto-tuner.py' first.")
        return
    
    print(f"=== SKILL AUTO-TUNE REPORT ===")
    print(f"Generated: {data.get('generated_at', 'unknown')[:19]}")
    print(f"Runs analyzed: {data.get('total_runs_analyzed', 0)}")
    print()
    
    priority = data.get("routing_priority", {})
    print(f"HIGH priority ({len(priority.get('high', []))} skills):")
    for s in priority.get("high", [])[:5]:
        print(f"  - {s}")
    
    print(f"\nMEDIUM priority ({len(priority.get('medium', []))} skills)")
    print(f"LOW priority ({len(priority.get('low', []))} skills)")
    print(f"QUARANTINED ({len(priority.get('blocked', []))} skills):")
    for s in priority.get("blocked", [])[:5]:
        print(f"  - {s}")
    
    print(f"\nGolden combinations ({len(data.get('golden_combinations', []))}):")
    for g in data.get("golden_combinations", [])[:5]:
        print(f"  - {g['pair']}: {g['success_rate']:.0%} success, {g['count']} runs, score={g['score']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        print_report()
    else:
        result = run_analysis()
        if result.get("status") == "insufficient_data":
            print(f"Need {result['needed']} runs, have {result['runs']}. Keep using skills!")
        else:
            print(f"Auto-tune complete. Routes saved to {TUNED_ROUTES}")
            print_report()
