#!/usr/bin/env python3
"""concept-flow-map.py — 2 dimensi baru di atas kategori role yg ada (non-invasif).

Kenapa: kategori sekarang = 1 dimensi datar (role: backend, designer, ...).
Skill yg sama bisa beda KONSEP (generator vs reviewer vs automator) dan beda
tahap ALUR (plan vs build vs test vs deploy vs observe). Tanpa 2 dimensi ini,
router cuma bisa numpuk skill per role — alurnya nggak kelihatan.

Desain: TIDAK ubah skema DB (worker mining lagi jalan). Mapping keyword
name+description -> concept + flow, output 2 file generated:
  SKILLS-CONCEPTS.md : skill per konsep (apa perannya)
  SKILLS-FLOWS.md    : skill per tahap alur (kapan dipakai)

Pakai: python3 ~/.agents/concept-flow-map.py
"""
import sqlite3
from datetime import datetime
from pathlib import Path

AGENTS = Path.home() / ".agents"
DB = AGENTS / "skills-index.db"

# KONSEP: apa peran skill ini (satu skill = satu konsep dominan, first-match)
CONCEPTS = [
    ("generator", ["generate", "generator", "create", "creator", "builder", "scaffold",
                   "generasi", "buat", "template"]),
    ("reviewer", ["review", "audit", "critique", "inspect", "evaluat", "assess",
                  "checker", "validator", "linter"]),
    ("automator", ["automat", "workflow", "pipeline", "scheduler", "cron", "bot",
                   "otomatis", "bulk", "batch"]),
    ("advisor", ["advisor", "recommend", "suggest", "consult", "mentor", "guide",
                 "best-practice", "pattern", "saran"]),
    ("integrator", ["integrat", "connect", "bridge", "sync", "webhook", "api-",
                    "mcp", "plugin", "extension"]),
    ("analyzer", ["analy", "insight", "metric", "dashboard", "report", "forecast",
                  "predict", "detect", "scanner"]),
    ("transformer", ["convert", "migrat", "translat", "transcode", "refactor",
                     "optimiz", "compress", "format"]),
    ("assistant", ["assistant", "chat", "helper", "copilot", "agent", "ask",
                   "asisten", "bantu"]),
]

# ALUR: kapan skill dipakai (software lifecycle + AI workflow)
FLOWS = [
    ("plan", ["plan", "design", "architect", "spec", "requirement", "prd",
              "roadmap", "rencana", "perencana"]),
    ("build", ["build", "develop", "implement", "code", "scaffold", "create",
               "bangun", "kembang"]),
    ("test", ["test", "qa", "quality", "benchmark", "eval", "uji", "coba"]),
    ("review", ["review", "audit", "approve", "critique", "inspect", "refactor",
                "debugging", "debug", "fix"]),
    ("deploy", ["deploy", "release", "publish", "ship", "ci-cd", "cicd",
                "docker", "kubernetes", "terraform", "rilis"]),
    ("observe", ["monitor", "observ", "alert", "log", "trace", "metric",
                 "dashboard", "pantau", "analyt"]),
    ("secure", ["secur", "auth", "compliance", "governance", "policy", "aman",
                "vulnerab", "pentest", "encrypt"]),
    ("document", ["doc", "write", "tutorial", "guide", "explain", "summar",
                  "tulis", "dokumentasi", "readme"]),
]


def match(text, groups):
    low = (text or "").lower()
    for name, kws in groups:
        for k in kws:
            if k in low:
                return name
    return "lainnya"


def main():
    if not DB.exists():
        print("ERROR: DB belum ada")
        return 1
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = conn.execute(
        "SELECT name, COALESCE(description,''), COALESCE(category,''), tier "
        "FROM skills WHERE tier != 'junk'").fetchall()
    conn.close()

    by_concept, by_flow = {}, {}
    for name, desc, cat, tier in rows:
        text = f"{name} {desc}"
        c = match(text, CONCEPTS)
        f = match(text, FLOWS)
        by_concept.setdefault(c, []).append((name, cat, tier))
        by_flow.setdefault(f, []).append((name, cat, tier))

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    cc = AGENTS / "SKILLS-CONCEPTS.md"
    with open(cc, "w") as fh:
        fh.write(f"# SKILLS CONCEPTS — peran skill (generated {ts})\n\n")
        fh.write("Dimensi **apa** peran skill, melengkapi kategori role. "
                 "Curated = terawat, reference = cek dulu.\n\n")
        fh.write("| Konsep | Jumlah | Contoh |\n|---|---|---|\n")
        for c, _ in CONCEPTS + [("lainnya", [])]:
            items = by_concept.get(c, [])
            ex = ", ".join(f"`{n}`" for n, _, _ in items[:6]) or "-"
            fh.write(f"| {c} | {len(items)} | {ex} |\n")

    fl = AGENTS / "SKILLS-FLOWS.md"
    with open(fl, "w") as fh:
        fh.write(f"# SKILLS FLOWS — tahap alur (generated {ts})\n\n")
        fh.write("Dimensi **kapan** skill dipakai (lifecycle). "
                 "Alur cakep: `plan → build → test → review → deploy → observe` "
                 "(+ `secure` & `document` di semua tahap).\n\n")
        fh.write("## Rekomendasi alur\n\n")
        fh.write("1. Mulai dari `plan` (spec, arsitektur) → `build` (implementasi).\n")
        fh.write("2. `test` + `review` sebelum `deploy` — jangan loncat.\n")
        fh.write("3. `observe` terus jalan pasca-deploy; `secure` & `document` di tiap tahap.\n")
        fh.write("4. Pilih konsep per tahap: plan=advisor · build=generator · "
                 "test/reviewer=reviewer · deploy=automator · observe=analyzer.\n")
        fh.write("5. Role agent baru: `agent-orchestrator` (multi-agent/swarm/subagent-patterns) · "
                 "`agent-memory` (recall/konteks/Letta) · `agent-ux` (slash-command/hooks/IDE-rules).\n")
        fh.write("   Wire khusus agent: `bash ~/.agents/wire-skills-role.sh agent <repo> --apply`.\n\n")
        fh.write("| Tahap | Jumlah | Contoh |\n|---|---|---|\n")
        for f, _ in FLOWS + [("lainnya", [])]:
            items = by_flow.get(f, [])
            ex = ", ".join(f"`{n}`" for n, _, _ in items[:6]) or "-"
            fh.write(f"| {f} | {len(items)} | {ex} |\n")

    print(f"ditulis: {cc.name} ({len(rows)} skill) + {fl.name}")
    for f, _ in FLOWS:
        print(f"  flow/{f}: {len(by_flow.get(f, []))}")
    for c, _ in CONCEPTS:
        print(f"  concept/{c}: {len(by_concept.get(c, []))}")
    print(f"  lainnya: {len(by_concept.get('lainnya', []))} konsep / "
          f"{len(by_flow.get('lainnya', []))} flow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
