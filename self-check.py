#!/usr/bin/env python3
"""self-check.py — kritik-diri deterministik (anti-slop, struktur, boros token).

Pakai:  python3 self-check.py draft.txt        (atau)  echo "..." | python3 self-check.py
        python3 self-check.py --json draft.txt

Tanpa LLM: murni pola. Tujuan: AI mengecek jawabannya SENDIRI sebelum kirim
(anti-slop + tidak boros + terstruktur) tanpa user perlu ketik /antislop.
"""
import json, re, sys
from pathlib import Path

SLOP = {
    r"\bas an ai\b": 3, r"\bai language model\b": 3,
    r"\bin conclusion\b": 2, r"\bit'?s worth noting\b": 2,
    r"\bit is important to note\b": 2, r"\bdelve into\b": 3,
    r"\btapestry\b": 3, r"\bin today'?s fast-paced\b": 3,
    r"\bnavigating the (landscape|world)\b": 3, r"\bunlock the (potential|power)\b": 3,
    r"\bgame[- ]changer\b": 3, r"\brevolutioniz": 2, r"\bseamless": 2,
    r"\bcutting[- ]edge\b": 2, r"\bstate[- ]of[- ]the[- ]art\b": 2,
    r"\bfurthermore\b": 1, r"\bmoreover\b": 1, r"\bin summary\b": 1,
    r"\brest assured\b": 2, r"\bi hope this helps\b": 2,
    r"\blet me know if you\b": 2, r"\bplease note that\b": 1,
    r"\bas we can see\b": 1, r"\bat the end of the day\b": 2,
    r"\bthe fact of the matter\b": 2, r"\bwhen it comes to\b": 1,
}
HEDGE = {"very", "really", "just", "actually", "basically", "simply",
         "quite", "extremely", "literally", "definitely", "certainly",
         "somewhat", "rather", "fairly", "pretty much"}


def _pretty(pat):
    s = pat.replace("\\b", "").replace("?", "").replace("[- ]", "-")
    s = s.replace("(landscape|world)", "landscape/world")
    s = s.replace("(potential|power)", "potential/power")
    s = s.replace("revolutioniz", "revolutionize")
    return s.strip()


def check(text):
    t = text or ""
    low = t.lower()
    issues = []
    score = 100

    slop_hits = []
    for pat, w in SLOP.items():
        m = re.findall(pat, low)
        if m:
            slop_hits.append((_pretty(pat), len(m), w * len(m)))
    for pat, n, pen in slop_hits:
        score -= pen
        issues.append(("slop", "frasa klise '%s' x%d" % (pat, n), pen))

    hedges = [w for w in HEDGE if re.search(r"\b%s\b" % re.escape(w), low)]
    if hedges:
        pen = min(6, len(hedges))
        score -= pen
        issues.append(("filler", "kata pengisi: " + ", ".join(hedges[:8]), pen))

    emdash = t.count("—")
    words = len(re.findall(r"\S+", t))
    if words > 80 and emdash > max(3, words // 120):
        pen = 3
        score -= pen
        issues.append(("style", "em-dash berlebihan (%d)" % emdash, pen))

    sents = [s for s in re.split(r"[.!?]+", t) if s.strip()]
    long_s = [s for s in sents if len(s.split()) > 40]
    if long_s:
        pen = min(4, len(long_s))
        score -= pen
        issues.append(("struktur", "%d kalimat terlalu panjang (>40 kata)" % len(long_s), pen))

    has_struct = bool(re.search(r"(?m)^\s*([-*]|\d+\.|#|\|)", t))
    if words > 120 and not has_struct:
        score -= 5
        issues.append(("struktur", "teks panjang tanpa heading/bullet/tabel", 5))

    # repetisi kalimat
    norm = [re.sub(r"\W+", " ", s.lower()).strip() for s in sents if len(s.split()) > 4]
    dup = len(norm) - len(set(norm))
    if dup > 0:
        pen = min(6, dup * 2)
        score -= pen
        issues.append(("repetisi", "%d kalimat berulang" % dup, pen))

    # boros: kata banyak tapi sedikit angka/entitas konkret
    if words > 200:
        concrete = len(re.findall(r"[A-Za-z0-9_./-]+\.(py|js|ts|json|md|db|sh)\b", t)) \
                   + len(re.findall(r"\b\d+\b", t))
        if concrete < words / 120:
            score -= 5
            issues.append(("boros", "teks panjang, sedikit detail konkret (file/angka)", 5))

    score = max(0, min(100, score))
    verdict = ("bagus" if score >= 85 else "perlu poles" if score >= 65 else "banyak masalah")
    return {"score": score, "verdict": verdict, "words": words,
            "issues": [{"type": a, "detail": b, "penalty": c} for a, b, c in issues]}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if args:
        text = Path(args[0]).read_text(encoding="utf-8", errors="ignore")
    else:
        text = sys.stdin.read()
    r = check(text)
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    print("SELF-CHECK: %d/100 (%s), %d kata" % (r["score"], r["verdict"], r["words"]))
    if not r["issues"]:
        print("  tidak ada masalah terdeteksi.")
    for it in r["issues"]:
        print("  - [%s] %s (-%d)" % (it["type"], it["detail"], it["penalty"]))


if __name__ == "__main__":
    main()
