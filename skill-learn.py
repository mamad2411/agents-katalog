#!/usr/bin/env python3
"""skill-learn.py — belajar dari pemakaian skill nyata (30 hari terakhir).

Sumber data:
  - Riwayat Claude Code (~/.claude/projects/**/*.jsonl): pemanggilan Skill tool + baca SKILL.md
  - MCP skill-catalog (~/.agents/skill-efficacy-log.json): skill_load
Aksi:
  - Skill dipakai >= MIN_USES kali → masuk "learned" di skill-core.json + di-link ke semua AI
  - Tulis laporan ~/.agents/skill-learn-report.md (paling sering dipakai, skill flow yang tak pernah dipakai)
Tidak pernah menghapus skill dari alur (skill-flow.json) — hanya melaporkan.
  --dry   hanya laporan, tanpa mengubah apa pun
"""
import collections, datetime, glob, json, os, re, sys, time

H = os.path.expanduser("~")
A = H + "/.agents"
STORE = A + "/skills-store"
MIN_USES = 3
DAYS = 30
DRY = "--dry" in sys.argv
cutoff = time.time() - DAYS * 86400
uses = collections.Counter()

skill_re = re.compile(r'"name":"Skill","input":\{"skill":"([^"]+)"')
read_re = re.compile(r'skills-store/([A-Za-z0-9_.-]+)/SKILL\.md')
for f in glob.glob(H + "/.claude/projects/**/*.jsonl", recursive=True):
    if os.path.getmtime(f) < cutoff:
        continue
    try:
        txt = open(f, errors="ignore").read()
    except OSError:
        continue
    for n in skill_re.findall(txt):
        uses[n.split(":")[-1]] += 1
    for n in set(read_re.findall(txt)):          # dihitung sekali per sesi
        uses[n] += 1

try:
    for e in json.load(open(A + "/skill-efficacy-log.json")):
        ts = datetime.datetime.fromisoformat(e["ts"]).timestamp()
        if ts >= cutoff:
            uses[e["skill"]] += 1
except Exception:
    pass

uses = collections.Counter({k: v for k, v in uses.items() if os.path.isdir(f"{STORE}/{k}")})
flow = json.load(open(A + "/skill-flow.json"))
flow_skills = set(flow["always"]) | {s for c in flow["categories"].values() for s in c["skills"]}
learned = sorted(n for n, c in uses.items() if c >= MIN_USES)
unused_flow = sorted(flow_skills - set(uses))

core_f = A + "/skill-core.json"
core = json.load(open(core_f))
new = [n for n in learned if n not in set(core.get("core", [])) | set(core.get("learned", []))]
linked = 0
if not DRY and new:
    core["learned"] = sorted(set(core.get("learned", [])) | set(new))
    core["core"] = sorted(set(core["core"]) | set(new))
    json.dump(core, open(core_f, "w"), indent=1)
    tools = [f"{H}/{d}/skills" for d in os.listdir(H) if d.startswith(".") and d != ".agents"
             and os.path.isdir(f"{H}/{d}/skills") and not os.path.islink(f"{H}/{d}/skills")]
    for t in tools:                               # Cline (~/.agents/skills) sengaja tidak ditambah
        for n in new:
            if not os.path.lexists(f"{t}/{n}"):
                os.symlink(f"{STORE}/{n}", f"{t}/{n}")
                linked += 1

R = ["# Laporan belajar skill", "", "Dibuat: %s · jendela %d hari · ambang naik kelas: %d pemakaian" %
     (time.strftime("%Y-%m-%d %H:%M"), DAYS, MIN_USES), "",
     "## Paling sering dipakai", ""]
R += ["- `%s` — %d×" % (n, c) for n, c in uses.most_common(25)] or ["- (belum ada data)"]
R += ["", "## Naik kelas (masuk skill aktif semua AI)", ""]
R += ["- `%s`" % n for n in new] or ["- (tidak ada yang baru)"]
R += ["", "## Skill alur yang belum pernah dipakai (%d) — kandidat ditinjau, tidak dihapus otomatis" % len(unused_flow), ""]
R += [", ".join("`%s`" % n for n in unused_flow) or "(semua terpakai)"]
R += ["", "## Sumber", "", "- `~/.claude/projects/**/*.jsonl`", "- `~/.agents/skill-efficacy-log.json`", ""]
open(A + "/skill-learn-report.md", "w").write("\n".join(R))
print("pemakaian tercatat: %d skill | naik kelas baru: %d | symlink: %d | laporan: ~/.agents/skill-learn-report.md%s"
      % (len(uses), len(new), linked, " (dry-run)" if DRY else ""))
