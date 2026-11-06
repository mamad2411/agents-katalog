#!/usr/bin/env python3
"""Tambah katalog skill dari repo SKILL.md nyata sampai mendekati 300k."""
import importlib.util
import os
import sqlite3
import subprocess
import sys
import time

AG = os.path.expanduser("~/.agents")
MINER = os.path.join(AG, "skill-miner.py")
BUILD = os.path.join(AG, "build_skills_index.py")
DB = os.path.join(AG, "skills-index.db")

SOURCES = [
    ("derkeyser/LegalSkillsKlotzkette", "main"),
    ("NeuralBlitz/ncx", "main"),
    ("brycewang-stanford/Auto-Empirical-Research-Skills", "main"),
    ("wonecosystem/2300-skills", "main"),
    ("Lord1Egypt/awesome-skill-forge", "master"),
    ("sickn33/agentic-awesome-skills", "main"),
]

spec = importlib.util.spec_from_file_location("sm", MINER)
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)

print("=== MULAI TAMBANG ===", flush=True)
print("sumber:", len(SOURCES), flush=True)
conn = sqlite3.connect(DB)
seen = set()
stats = {"new": 0, "exists": 0, "dup": 0, "err": 0}
t0 = time.time()
sm.mine_tarball(SOURCES, conn, seen, stats)
conn.close()
print("=== TAMBANG SELESAI ===", stats, "waktu=%.0fs" % (time.time() - t0), flush=True)

print("=== REBUILD INDEX ===", flush=True)
r = subprocess.run([sys.executable, BUILD], text=True)
print("build exit:", r.returncode, flush=True)

conn = sqlite3.connect(DB)
n = conn.execute("SELECT count(*) FROM skills").fetchone()[0]
conn.close()
print("=== TOTAL AKHIR:", n, "===", flush=True)
