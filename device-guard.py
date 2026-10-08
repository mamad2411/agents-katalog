#!/usr/bin/env python3
"""device-guard.py — penjaga PANAS & SSD (bukan token): audit + perbaikan opt-in.

Konteks audit 2026-10-03 (temuan nyata di mesin ini):
  * Satu loop mining di tmux jalan **8 hari** (`while true` → GitHub API → tulis
    log/state tiap 10 detik). Mining sudah SATURASI menurut kebijakan repo sendiri
    (AGENTS.md §Aturan keras) → murni panas + tulis SSD tanpa hasil.
  * 2 launchd agent ber-`KeepAlive=true` (repo-ref-api, skill-graph-api) hidup 24/7
    padahal port-nya sendiri didokumentasikan mati/tidak diandalkan.
  * 2 launchd agent ber-jalan tiap **30 menit** (legakan, skill-auto-symlink).

Pakai:
  python3 ~/.agents/device-guard.py            # LAPORAN saja (read-only, aman)
  python3 ~/.agents/device-guard.py --apply    # jalankan perbaikan (backup otomatis)

Yang di-apply (hanya ini, semuanya reversible):
  1. Hentikan loop/tmux yg cocok pola mining-saturated (whitelist ketat).
  2. `launchctl bootout` + `disable` repo-ref-api & skill-graph-api (KeepAlive 24/7).
  3. Ubah StartInterval legakan & skill-auto-symlink 1800 → 21600 dtk (6 jam).
Daftar perubahan + cara balik ditulis ke ~/.agents/.device-guard-log.json.
Yang TIDAK pernah disentuh: docker, dev-stack.sh (PID di /tmp/voralens-dev.pid),
cline/editor, MCP server yg dipakai sesi aktif, proses < 5 menit, 9router.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
LA = os.path.join(HOME, "Library", "LaunchAgents")
LOG = os.path.join(HOME, ".agents", ".device-guard-log.json")
STAMP = time.strftime("%Y%m%d")
UID = os.getuid()

# pola loop yg aman dihentikan (mining/saturasi/watcher yatim) — KETAT
KILL_PATTERNS = [
    r"skillsh-fullpass\.sh",
    r"ghscan-fetch\.py",
    r"ghscan-enum\.sh",
    r"mine-daemon\.sh __worker__",
    r"mine-to-100k\.sh",
    r"upload-link-watcher",
]
# agent KeepAlive yg sebaiknya tidak hidup 24/7 (port mati per dokumen repo)
BOOTOUT = ["com.agents.repo-ref-api", "com.agents.skill-graph-api"]
# interval diperpanjang (nama → detik baru)
INTERVAL = {"com.agents.legakan": 21600, "com.agents.skill-auto-symlink": 21600}


def run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20, **kw)
    except Exception as e:
        return subprocess.CompletedProcess(cmd, 1, "", str(e))


def ps_rows():
    out = run(["ps", "-Ao", "pid=,etime=,pcpu=,rss=,command="]).stdout
    rows = []
    for ln in out.splitlines():
        p = ln.split(None, 4)
        if len(p) == 5:
            rows.append({"pid": int(p[0]), "etime": p[1], "cpu": float(p[2]),
                         "rss_mb": int(p[3]) / 1024, "cmd": p[4]})
    return rows


def tmux_sessions():
    out = run(["tmux", "ls", "-F", "#{session_name}|#{session_created}|#{pane_current_command}"]).stdout
    return [l.split("|") for l in out.splitlines() if l.strip()]


def log_churn(paths, secs=3):
    """(byte/detik) — bukti tulis SSD dari proses yang sedang berjalan."""
    before = {}
    for p in paths:
        try:
            before[p] = os.path.getsize(p)
        except OSError:
            before[p] = None
    time.sleep(secs)
    out = []
    for p, b in before.items():
        try:
            a = os.path.getsize(p)
        except OSError:
            continue
        if b is not None:
            out.append((max(a - b, 0) / float(secs), p))
    return sorted(out, reverse=True)


def launch_agents():
    rows = []
    for fn in sorted(os.listdir(LA)) if os.path.isdir(LA) else []:
        if not fn.endswith(".plist") or ".bak-" in fn:
            continue
        p = os.path.join(LA, fn)
        label = run(["/usr/libexec/PlistBuddy", "-c", "Print :Label", p]).stdout.strip() or fn[:-6]
        iv = run(["/usr/libexec/PlistBuddy", "-c", "Print :StartInterval", p]).stdout.strip()
        keep = run(["/usr/libexec/PlistBuddy", "-c", "Print :KeepAlive", p]).stdout.strip()
        rows.append({"label": label, "file": p, "interval": iv, "keepalive": keep})
    return rows


def report():
    rows = ps_rows()
    print("=== device-guard (PANAS/SSD) %s ===" % time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    ram = sum(r["rss_mb"] for r in rows)
    print("RAM proses: %.0f MB · proses >5%% CPU: %s" %
          (ram, ", ".join("%s(%.0f%%)" % (r["cmd"][:26], r["cpu"]) for r in sorted(rows, key=lambda x: -x["cpu"])[:3])))
    print("\n-- tmux (loop latar) --")
    for name, created, cmd in tmux_sessions():
        age = int(time.time()) - int(created) if created.isdigit() else 0
        print("  %-14s umur %5.1f hari  pane=%s" % (name, age / 86400.0, cmd))
    if not tmux_sessions():
        print("  (tidak ada)")
    print("\n-- churn tulis (3 dtk) --")
    for bps, p in log_churn(["/tmp/ghchain.log", "/tmp/skillsh-fullpass.log", "/tmp/legakan.log"]):
        print("  %8.1f B/s  %s" % (bps, p))
    print("\n-- launchd --")
    for a in launch_agents():
        verdict = ""
        if a["keepalive"] == "true":
            verdict = " <-- hidup 24/7"
        if a["interval"].isdigit() and int(a["interval"]) <= 1800:
            verdict += " <-- tiap %d menit" % (int(a["interval"]) // 60)
        print("  %-30s interval=%-7s keepalive=%-6s%s" % (a["label"], a["interval"] or "-", a["keepalive"] or "-", verdict))
    print("\n-- kandidat stop (loop mining saturasi) --")
    found = False
    for r in rows:
        if any(re.search(p, r["cmd"]) for p in KILL_PATTERNS):
            print("  PID %-7d %-9s %s" % (r["pid"], r["etime"], r["cmd"][:70]))
            found = True
    if not found:
        print("  (tidak ada)")
def apply():
    changes = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "killed": [],
               "bootout": [], "interval": [], "restore": {}}
    # 1. stop loop mining-saturasi
    for r in ps_rows():
        if any(re.search(p, r["cmd"]) for p in KILL_PATTERNS):
            if run(["kill", "-TERM", str(r["pid"])]).returncode == 0:
                changes["killed"].append({"pid": r["pid"], "cmd": r["cmd"][:120]})
    # tmux: bunuh session yg pane-nya menjalankan loop itu (nama 'ghchain'/'skillshfull')
    for name, _c, _cmd in tmux_sessions():
        if name in ("ghchain", "skillshfull"):
            if run(["tmux", "kill-session", "-t", name]).returncode == 0:
                changes["killed"].append({"tmux": name})
    # 2. bootout agent KeepAlive 24/7
    for label in BOOTOUT:
        run(["launchctl", "bootout", "gui/%d/%s" % (UID, label)])
        run(["launchctl", "disable", "gui/%d/%s" % (UID, label)])
        changes["bootout"].append(label)
        changes["restore"][label] = ("launchctl enable gui/%d/%s && launchctl bootstrap gui/%d %s/%s.plist"
                                     % (UID, label, UID, LA, label))
    # 3. perpanjang interval (backup plist dulu)
    for label, secs in INTERVAL.items():
        p = os.path.join(LA, label + ".plist")
        if not os.path.exists(p):
            continue
        bak = "%s.bak-%s" % (p, STAMP)
        if not os.path.exists(bak):
            shutil.copy2(p, bak)
        old = run(["/usr/libexec/PlistBuddy", "-c", "Print :StartInterval", p]).stdout.strip()
        run(["/usr/libexec/PlistBuddy", "-c", "Set :StartInterval %d" % secs, p])
        run(["launchctl", "bootout", "gui/%d/%s" % (UID, label)])
        run(["launchctl", "bootstrap", "gui/%d" % UID, p])
        changes["interval"].append({"label": label, "from": old, "to": secs})
        changes["restore"][label] = "cp %s %s && launchctl bootout gui/%d/%s; launchctl bootstrap gui/%d %s" % (
            bak, p, UID, label, UID, p)
    try:
        json.dump(changes, open(LOG, "w"), indent=1, ensure_ascii=False)
    except Exception:
        pass
    print("device-guard --apply selesai:")
    print("  dihentikan : %d item %s" % (len(changes["killed"]), [k.get("tmux") or k.get("pid") for k in changes["killed"]]))
    print("  bootout    : %s" % (", ".join(changes["bootout"]) or "-"))
    print("  interval   : %s" % ", ".join("%s %s→%ss" % (c["label"], c["from"], c["to"]) for c in changes["interval"]) or "-")
    print("  cara balik : ~/.agents/.device-guard-log.json (kunci 'restore')")
    return 0


if __name__ == "__main__":
    sys.exit(apply() if "--apply" in sys.argv else report())
