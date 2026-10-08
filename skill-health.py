#!/usr/bin/env python3
"""skill-health.py — cek kesehatan sistem skill (mingguan via launchd, atau manual).

Cek: symlink rusak · jumlah skill Cline · skill alur hilang · tes routing · MCP skill-catalog
· hook terpasang di Claude/Cline/Codex/Gemini · MCP terdaftar di tiap AI · lalu jalankan skill-learn.
Hasil: ~/.agents/skill-health-report.md + notifikasi macOS bila ada masalah.
  --fix   hapus symlink rusak (hanya yang menunjuk ke ~/.agents)
"""
import json, os, subprocess, sys, time

H = os.path.expanduser("~")
A = H + "/.agents"
FIX = "--fix" in sys.argv
CLINE_MAX = 150
ok, bad = [], []


def run(cmd, inp=None, t=30):
    try:
        r = subprocess.run(cmd, input=inp, capture_output=True, text=True, timeout=t)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:
        return 1, str(e)


# 1. symlink rusak
tools = [A + "/skills"] + [f"{H}/{d}/skills" for d in os.listdir(H) if d.startswith(".") and d != ".agents"
                           and os.path.isdir(f"{H}/{d}/skills") and not os.path.islink(f"{H}/{d}/skills")]
broken = []
for t in tools:
    for e in os.scandir(t):
        if e.is_symlink() and not os.path.exists(e.path):
            broken.append(e.path)
            if FIX and os.readlink(e.path).startswith(A):
                os.unlink(e.path)
(bad if broken and not FIX else ok).append("symlink rusak: %d%s" % (len(broken), " (dihapus)" if FIX and broken else ""))

# 2. Cline tetap ringan
n = len(os.listdir(A + "/skills"))
(ok if n <= CLINE_MAX else bad).append("skill Cline (~/.agents/skills): %d (batas %d)" % (n, CLINE_MAX))

# 3. skill alur + tes routing
rc, out = run(["python3", A + "/skill-flow.py", "--check"])
(ok if "hilang: tidak ada" in out else bad).append("skill alur: " + out.strip().splitlines()[-1])
rc, out = run(["python3", A + "/skill-flow.py", "--eval"])
(ok if rc == 0 else bad).append("tes routing: " + out.strip().splitlines()[-1])

# 4. MCP skill-catalog merespons
req = ('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"health","version":"1"}}}\n'
       '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"skill_for_task","arguments":{"task":"write unit tests"}}}\n')
rc, out = run(["python3", A + "/skill-mcp.py"], req, 15)
(ok if '"id": 2' in out and "Rekomendasi" in out else bad).append("MCP skill-catalog: " + ("merespons" if "Rekomendasi" in out else "TIDAK merespons"))


# 5. hook terpasang
def has(path, needle):
    try:
        return needle in open(os.path.expanduser(path)).read()
    except OSError:
        return False


hooks = {"Claude Code": has("~/.claude/settings.json", "skill-inject.sh"),
         "Codex": has("~/.codex/hooks.json", "skill-inject.sh"),
         "Gemini": has("~/.gemini/settings.json", "skill-inject-gemini.py"),
         "Cline": os.path.exists(H + "/.cline/hooks/UserPromptSubmit.py")}
miss = [k for k, v in hooks.items() if not v]
(bad if miss else ok).append("hook: " + ("semua terpasang" if not miss else "hilang di " + ", ".join(miss)))

# 6. MCP terdaftar
cfgs = ["~/.claude.json", "~/.gemini/settings.json", "~/.cursor/mcp.json", "~/.cline/mcp.json", "~/.continue/mcp.json",
        "~/.kiro/mcp.json", "~/.codeium/mcp.json", "~/.config/opencode/opencode.json", "~/.qwen/settings.json",
        "~/.codebuddy/mcp.json", "~/.codex/config.toml"]
miss = [c for c in cfgs if os.path.exists(os.path.expanduser(c)) and not has(c, "skill-mcp.py")]
(bad if miss else ok).append("MCP terdaftar: " + ("semua" if not miss else "hilang di " + ", ".join(miss)))

# 7. belajar dari pemakaian
rc, out = run(["python3", A + "/skill-learn.py"], t=120)
(ok if rc == 0 else bad).append("belajar pemakaian: " + (out.strip().splitlines() or ["?"])[-1])

R = ["# Laporan kesehatan skill", "", "Dibuat: " + time.strftime("%Y-%m-%d %H:%M"), "",
     "## Masalah (%d)" % len(bad), ""] + ["- ❌ " + x for x in bad] + ["", "## OK (%d)" % len(ok), ""] + ["- ✅ " + x for x in ok]
if broken[:20]:
    R += ["", "## Contoh symlink rusak", ""] + ["- `%s`" % b.replace(H, "~") for b in broken[:20]]
R += ["", "## Sumber", "", "- `~/.agents/skill-health.py`", ""]
open(A + "/skill-health-report.md", "w").write("\n".join(R))
print("\n".join(R[4:4 + len(bad) + len(ok) + 4]))
if bad:
    run(["osascript", "-e", 'display notification "%d masalah — buka ~/.agents/skill-health-report.md" with title "Skill health"' % len(bad)])
sys.exit(1 if bad else 0)
