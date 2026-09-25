#!/usr/bin/env python3
"""skill-eval.py — eval harness ringan untuk katalog skill.

Mengukur:
  1. Triggering accuracy: untuk tiap test-case (task bahasa natural + jawaban
     yang dianggap benar), jalankan search+rerank yang SAMA PERSIS dengan yang
     dipakai AI (import skill-mcp.py), lalu cek pass@1 & pass@3.
  2. Kesehatan katalog: nama rusak, deskripsi kosong di tier aktif, DB & katalog fresh.

Hasil: stdout + history ke ~/.agents/skill-eval-results.json (ringkas).
Jalankan: python3 ~/.agents/skill-eval.py
"""
import importlib.util
import json
import re
import sqlite3
import time
from pathlib import Path

AG = Path.home() / ".agents"
EVALS = AG / "skill-evals.json"
RESULTS = AG / "skill-eval-results.json"
DB = AG / "skills-index.db"
IDX = AG / "skills-index.json"

spec = importlib.util.spec_from_file_location("sm", AG / "skill-mcp.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


def rank_scored(task, top=8, pool=60):
    """Skor dari skill-mcp.py (SUMBER TUNGGAL logika) — biar hasil eval = perilaku nyata AI."""
    return [(s, n, t) for s, n, t, _c, _d in sm.rank_with_scores(task, top, pool)]


def recommend(task, k=60, top=3):
    """Sama persis dengan AI: rank_for_task dari skill-mcp.py (sumber tunggal logika)."""
    return [(n, t) for n, t, _c, _d in sm.rank_for_task(task, top=top)]


def catalog_health():
    issues = []
    if not DB.exists():
        return ["DB tidak ada — jalankan build_skills_index.py"]
    conn = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    try:
        mal = conn.execute(
            "SELECT COUNT(*) FROM skills WHERE name LIKE '-%' OR name LIKE '%--%'"
        ).fetchone()[0]
        if mal:
            issues.append("%d nama rusak" % mal)
        for tier in ("curated", "reference"):
            n = conn.execute(
                "SELECT COUNT(*) FROM skills WHERE tier=? AND (description='' OR name='')",
                (tier,)).fetchone()[0]
            if n:
                issues.append("%d skill %s tanpa nama/deskripsi" % (n, tier))
        src = conn.execute("SELECT COUNT(*) FROM skills WHERE source!=''").fetchone()[0]
        act = conn.execute("SELECT COUNT(*) FROM skills WHERE tier!='junk'").fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM skills WHERE tier='curated'").fetchone()[0]
    finally:
        conn.close()
    if IDX.exists():
        age_h = (time.time() - IDX.stat().st_mtime) / 3600
        if age_h > 24:
            issues.append("katalog basi (%.0f jam) — jalankan skills-router.py" % age_h)
    else:
        issues.append("skills-index.json tidak ada")
    return issues, {"aktif": act, "curated": cur, "dengan_source": src}


def main():
    cases = json.loads(EVALS.read_text()) if EVALS.exists() else []
    if not cases:
        print("evals kosong:", EVALS)
        return 1
    passed1 = passed3 = neg_ok = neg_total = 0
    details = []
    for c in cases:
        rec = recommend(c["task"])
        if c.get("expect_none"):
            # Kasus negatif: sistem harus JUJUR — skor rekomendasi rendah /
            # kosong lebih baik daripada maksa. Lulus bila top-1 skor < ambang.
            neg_total += 1
            scored = rank_scored(c["task"])
            top_score = scored[0][0] if scored else 0
            # ambang jujur: < 11 = belum pede (1 kata generik saja ≈ 10) = perilaku benar
            ok = top_score < 11
            neg_ok += ok
            details.append({"task": c["task"], "top": [n for n, _t in rec],
                            "neg_score": top_score, "hit1": ok, "hit3": ok,
                            "negatif": True})
            continue
        expect = set(c["expect_any"])
        top1 = rec[0][0] if rec else None
        hit1 = top1 in expect
        hit3 = any(n in expect for n, _t in rec)
        passed1 += hit1
        passed3 += hit3
        details.append({"task": c["task"], "top": [n for n, _t in rec],
                        "hit1": hit1, "hit3": hit3})
    pos = [c for c in cases if not c.get("expect_none")]
    n = len(pos)
    p1, p3 = (passed1 / n * 100, passed3 / n * 100) if n else (100, 100)
    pn = (neg_ok / neg_total * 100) if neg_total else 100

    issues, extra = catalog_health()
    print("=== SKILL EVAL (%d positif + %d negatif) ===" % (n, neg_total))
    for d in details:
        if d.get("negatif"):
            mark = "✓" if d["hit1"] else "✗"
            print("%s [NEG sk=%d] %-36s -> %s" % (mark, d.get("neg_score", 0), d["task"][:36], ", ".join(d["top"][:3])))
            continue
        mark = "✓" if d["hit1"] else ("~" if d["hit3"] else "✗")
        print("%s %-46s -> %s" % (mark, d["task"][:46], ", ".join(d["top"][:3])))
    print("-" * 60)
    print("pass@1: %d/%d (%.0f%%) · pass@3: %d/%d (%.0f%%) · jujur-negatif: %d/%d (%.0f%%)"
          % (passed1, n, p1, passed3, n, p3, neg_ok, neg_total, pn))
    print("katalog: %d entri siap-cari (curated %d layak-invoke + reference) · %d dengan provenance"
          % (extra["aktif"], extra.get("curated", 0), extra["dengan_source"]))
    if issues:
        print("HEALTH ISSUES:")
        for i in issues:
            print("  -", i)
    else:
        print("katalog: SEHAT ✓")

    hist = json.loads(RESULTS.read_text()) if RESULTS.exists() else []
    hist.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "n": n, "neg": neg_total,
                 "pass1": round(p1), "pass3": round(p3), "neg_honest": round(pn),
                 "aktif": extra["aktif"], "issues": issues})
    RESULTS.write_text(json.dumps(hist[-30:], indent=1))
    print("history:", RESULTS)
    return 0 if (p3 >= 70 and pn >= 60 and not issues) else 2


if __name__ == "__main__":
    raise SystemExit(main())