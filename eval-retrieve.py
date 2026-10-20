#!/usr/bin/env python3
"""eval-retrieve.py — ukur kualitas retrieve.py sebelum/sesudah diubah.

Pakai:  python3 eval-retrieve.py            (default: modul sekarang)
        python3 eval-retrieve.py file.py    (bandingkan implementasi lain)

Metrik: recall@5 (ada jawaban benar di 5 hasil?) dan top1 (jawaban benar di #1).
Ground truth = potongan nama skill yang seharusnya muncul.
"""
import importlib.util, sys, time
from pathlib import Path

Q = [
    ("code review", "code-review"), ("anti slop desain ui", "anti-ui-slop"),
    ("hemat token konteks", "token"), ("fine tuning lora", "lora"),
    ("optimasi query postgres", "postgres"), ("docker compose production", "docker-compose"),
    ("react hooks patterns", "react-hooks"), ("menulis unit test", "unit-test"),
    ("seo audit website", "seo"), ("git commit message", "commit"),
    ("screenshot testing visual regression", "visual-regression"),
    ("kubernetes helm deploy", "kubernetes"), ("stripe payment integration", "stripe"),
    ("rust async tokio", "rust"), ("review kode", "code-review"),
    ("perbaiki bug", "debug"), ("uji otomatis", "test"), ("keamanan aplikasi", "security"),
    ("rapikan struktur kode", "refactor"), ("desain tampilan", "design"),
]


def load(path):
    spec = importlib.util.spec_from_file_location("r", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(mod, k=5):
    r5 = r1 = 0
    t0 = time.time()
    for q, stem in Q:
        names = [x["name"].lower() for x in mod.search(q, k)]
        ok5 = any(stem in n for n in names)
        r5 += ok5
        r1 += bool(names) and stem in names[0]
    ms = round((time.time() - t0) * 1000 / len(Q))
    return r5, r1, ms


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name("retrieve.py"))
    r5, r1, ms = run(load(path))
    print("%s: recall@5=%d/%d  top1=%d/%d  %dms/query" % (path, r5, len(Q), r1, len(Q), ms))
