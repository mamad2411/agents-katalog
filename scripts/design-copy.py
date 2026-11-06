#!/usr/bin/env python3
"""design-copy.py — gerbang copy Bahasa Indonesia: buang bahasa pemasaran kosong
dan "AI tells" sebelum teks dipakai di UI.

Pakai:
  dcopy teks.md                 # file .md/.txt/.html
  dcopy https://situs/halaman   # ambil teks terlihat (Playwright)
  cat teks.txt | dcopy -        # stdin
  dcopy teks.md --json          # keluaran mesin

Yang dianggap pelanggaran keras (exit 1):
  - klaim pujian diri tanpa bukti ("solusi terbaik", "nomor satu", "revolusioner")
  - buzzword kosong ("seamless", "cutting-edge", "world-class", "tanpa hambatan")
  - pola AI ("tidak hanya ... tetapi juga", "di era digital", "mari kita")
  - tanda seru berlebihan (>=3) atau emoji bertebaran (>=3)

Peringatan (tidak menggagalkan): kalimat kepanjangan, kata pengisi, kalimat pasif
berlebihan, HURUF KAPITAL, elipsis.

Exit: 0 bersih · 1 ada pelanggaran keras · 2 gagal baca input.
"""
import json
import os
import re
import sys

HARD = [
    (r"\bsolusi terbaik\b", "klaim tanpa bukti", "sebutkan angka/fakta, atau hapus"),
    (r"\bnomor satu\b|\bnomor 1\b|\bno\.? ?1\b", "klaim tanpa bukti", "ganti dengan bukti terukur"),
    (r"\bterbaik di (industri|dunia|indonesia|kelasnya)\b", "klaim tanpa bukti", "hapus atau beri data"),
    (r"\brevolusioner\b|\brevolusioner\b", "buzzword", "jelaskan perubahan konkretnya"),
    (r"\bterdepan\b|\bterkemuka\b|\bterpercaya\b", "klaim tanpa bukti", "ganti dengan fakta yang bisa dicek"),
    (r"\bseamless\b|\bmulus tanpa hambatan\b|\btanpa hambatan\b", "buzzword", "sebut langkah konkretnya"),
    (r"\bcutting[- ]edge\b|\bworld[- ]class\b|\bbest[- ]in[- ]class\b|\bgame[- ]changer\b", "buzzword", "ganti istilah teknis nyata"),
    (r"\bdi era digital\b|\bdi era modern\b|\bseiring perkembangan teknologi\b", "pembuka klise", "mulai dari masalah pengguna"),
    (r"tidak hanya .{0,60}? tetapi juga", "pola AI", "pecah jadi dua kalimat"),
    (r"bukan hanya .{0,60}? melainkan", "pola AI", "pecah jadi dua kalimat"),
    (r"\bmari kita\b|\byuk kita\b|\bmari bersama\b", "ajakan klise", "pakai kalimat perintah langsung"),
    (r"\bmemberdayakan\b|\bmentransformasi\b|\bmengoptimalkan\b", "kata kosong", "sebut hasil yang terukur"),
]

SOFT = [
    (r"\bsangat\b|\bsekali\b|\bamat\b", "kata pengisi", "buang; kekuatan datang dari fakta"),
    (r"\bbenar-benar\b|\bsesungguhnya\b|\bsejatinya\b", "kata pengisi", "buang"),
    (r"\bberbagai\b|\bberagam\b", "kata pengisi", "sebut jumlah atau contoh"),
    (r"\bdapat dilakukan\b|\bdilakukan oleh\b|\boleh karena itu\b", "kalimat pasif", "pakai subjek aktif"),
]


def extract_text(src):
    if src == "-":
        return sys.stdin.read()
    if src.startswith(("http://", "https://")):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto(src, wait_until="domcontentloaded", timeout=45_000)
            pg.wait_for_timeout(1500)
            text = pg.evaluate(
                """() => {
                  const el = document.querySelector('main') || document.body;
                  return el.innerText || '';
                }"""
            )
            b.close()
        return text
    path = os.path.expanduser(src)
    if not os.path.exists(path):
        sys.exit(f"file tidak ada: {src}")
    raw = open(path, encoding="utf-8", errors="ignore").read()
    if path.endswith((".html", ".htm")):
        raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = re.sub(r"&[a-z]+;", " ", raw)
    return raw


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = sys.argv[1:]
    if not args:
        sys.exit("pakai: design-copy.py <file|url|-> [--json]")

    try:
        text = extract_text(args[0])
    except SystemExit:
        raise
    except Exception as exc:
        print(f"gagal membaca input: {exc}", file=sys.stderr)
        return 2

    lines = text.splitlines()
    hard, soft = [], []
    for i, line in enumerate(lines, 1):
        low = line.lower()
        for pattern, kind, fix in HARD:
            for m in re.finditer(pattern, low):
                hard.append({"line": i, "kind": kind, "match": m.group(0), "fix": fix,
                             "text": line.strip()[:90]})
        for pattern, kind, fix in SOFT:
            for m in re.finditer(pattern, low):
                soft.append({"line": i, "kind": kind, "match": m.group(0), "fix": fix,
                             "text": line.strip()[:90]})

    body = re.sub(r"\s+", " ", text).strip()
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", body) if len(s.split()) > 2]
    avg_words = round(sum(len(s.split()) for s in sentences) / len(sentences), 1) if sentences else 0
    bangs = text.count("!")
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", text))
    caps = len([w for w in re.findall(r"\b[A-Z]{4,}\b", text)])

    if bangs >= 3:
        hard.append({"line": 0, "kind": "tanda seru berlebihan", "match": f"{bangs}×",
                     "fix": "maksimal 1 untuk seluruh halaman", "text": ""})
    if emoji >= 3:
        hard.append({"line": 0, "kind": "emoji bertebaran", "match": f"{emoji}×",
                     "fix": "emoji bukan ikon; pakai icon set", "text": ""})
    if avg_words > 25:
        soft.append({"line": 0, "kind": "kalimat kepanjangan", "match": f"{avg_words} kata/kalimat",
                     "fix": "pecah jadi ≤20 kata", "text": ""})
    if caps >= 3:
        soft.append({"line": 0, "kind": "HURUF KAPITAL", "match": f"{caps}×",
                     "fix": "pakai kapitalisasi normal", "text": ""})

    score = max(0, 100 - 15 * len(hard) - 3 * len(soft))
    report = {
        "source": args[0], "score": score,
        "chars": len(body), "sentences": len(sentences), "avgWordsPerSentence": avg_words,
        "hard": hard, "soft": soft,
    }

    if "--json" in flags:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"copy  {args[0]} · {len(body)} karakter · {len(sentences)} kalimat · rata2 {avg_words} kata")
        if not hard and not soft:
            print("  bersih — tidak ada pola pemasaran kosong")
        for h in hard:
            loc = f"L{h['line']}" if h["line"] else "global"
            print(f"  FAIL {loc:6s} [{h['kind']}] \"{h['match']}\" → {h['fix']}")
        for s in soft[:6]:
            loc = f"L{s['line']}" if s["line"] else "global"
            print(f"  WARN {loc:6s} [{s['kind']}] \"{s['match']}\" → {s['fix']}")
        print(f"skor {score}/100 · {'LULUS' if not hard else 'GAGAL (' + str(len(hard)) + ' pelanggaran keras)'}")
    return 0 if not hard else 1


if __name__ == "__main__":
    sys.exit(main())
