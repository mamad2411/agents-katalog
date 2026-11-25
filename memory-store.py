#!/usr/bin/env python3
"""memory-store.py — memori lintas sesi yang benar-benar tersimpan & terpanggil.

  save  (stdin JSON hook SessionEnd)  -> simpan digest sesi + mirror ke Obsidian
  recall [--project DIR] [--query T]  -> ringkas memori untuk konteks sesi baru
  add "fakta"                         -> tambah 1 fakta ke MEMORY.md global
  list                                -> daftar sesi tersimpan

Sumber fakta: transcript JSONL (Claude/Codex) — tidak menelepon API, 0 token.
"""
import hashlib
import json
import os
import re
import sys
import time

H = os.path.expanduser("~")
MEM_DIR = os.path.join(H, ".agents", "memory")
GLOBAL_MD = os.path.join(MEM_DIR, "MEMORY.md")
SESS_DIR = os.path.join(MEM_DIR, "sessions")
PROJ_DIR = os.path.join(MEM_DIR, "projects")
VAULT = os.path.join(H, "mamatXobsidian", "00 - Inbox", "agent-memory")
SEEN = os.path.join(MEM_DIR, ".seen-hashes.json")
MAX_BULLETS = 8


def slug(path):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()
    return s[:60] or "root"


def read_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def write_atomic(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                out.append(c.get("text", ""))
    return "\n".join(out)


def parse_transcript(path):
    """Ambil: cwd, permintaan user, file yang disentuh, ringkasan asisten terakhir."""
    cwd, asks, files, last_assistant = "", [], [], ""
    try:
        with open(path, errors="ignore") as f:
            lines = f.readlines()[-400:]
    except Exception:
        return None
    for line in lines:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        cwd = rec.get("cwd") or cwd
        msg = rec.get("message") or {}
        role = rec.get("type") or msg.get("role")
        content = msg.get("content")
        if role == "user":
            t = text_of(content).strip()
            if t and not t.startswith("<") and "tool_result" not in t[:40]:
                if len(t) > 12 and not t.startswith("Caveat:"):
                    asks.append(t)
        elif role == "assistant":
            t = text_of(content).strip()
            if t:
                last_assistant = t
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        inp = c.get("input") or {}
                        fp = inp.get("file_path") or inp.get("path")
                        if fp:
                            files.append(str(fp))
    return {"cwd": cwd, "asks": asks, "files": files, "last": last_assistant}


def one_line(s, n=220):
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s[:n]


def newest_transcript(max_age_s=1800):
    """Untuk CLI yang tidak mengirim transcript_path di hook (mis. codex)."""
    roots = [os.path.join(H, ".claude", "projects"), os.path.join(H, ".codex", "sessions")]
    best, best_t = "", 0.0
    now = time.time()
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if not fn.endswith(".jsonl"):
                    continue
                p = os.path.join(dirpath, fn)
                try:
                    m = os.path.getmtime(p)
                except OSError:
                    continue
                if m > best_t and now - m < max_age_s:
                    best, best_t = p, m
    return best


def cmd_save():
    payload = read_json("/dev/stdin", {})
    transcript = payload.get("transcript_path") or ""
    if not transcript and "--auto" in sys.argv:
        transcript = newest_transcript()
    session = str(payload.get("session_id") or "")
    data = parse_transcript(transcript) if transcript else None
    if not data:
        return 0
    ask = one_line(data["asks"][0] if data["asks"] else "", 200)
    if not ask:
        return 0
    digest_src = ask + "|" + data["cwd"] + "|" + (transcript or "")
    h = hashlib.sha1(digest_src.encode()).hexdigest()[:12]
    seen = read_json(SEEN, {})
    if h in seen:
        return 0
    seen[h] = int(time.time())
    if len(seen) > 4000:
        for k in sorted(seen, key=seen.get)[:1000]:
            seen.pop(k, None)
    write_atomic(SEEN, json.dumps(seen))

    project = os.path.basename(data["cwd"].rstrip("/")) or "root"
    ts = time.strftime("%Y-%m-%d %H:%M")
    uniq_files = []
    for f in data["files"]:
        if f not in uniq_files:
            uniq_files.append(f)
    body = [
        "---",
        "tags: [agent-memory, session]",
        "date: %s" % ts,
        "project: %s" % project,
        "---",
        "",
        "# %s — %s" % (project, one_line(ask, 90)),
        "",
        "- **Sesi**: %s" % ts,
        "- **Folder**: `%s`" % data["cwd"],
        "- **Permintaan**: %s" % one_line(ask, 400),
    ]
    if uniq_files:
        body.append("- **File disentuh**: " + ", ".join("`%s`" % os.path.basename(f) for f in uniq_files[:12]))
    if data["last"]:
        body.append("- **Hasil terakhir**: %s" % one_line(data["last"], 500))
    body.append("")
    text = "\n".join(body)

    name = "%s-%s.md" % (time.strftime("%Y-%m-%d-%H%M"), (session[:8] or h[:8]))
    write_atomic(os.path.join(SESS_DIR, name), text)
    write_atomic(os.path.join(VAULT, name), text)
    return 0


def cmd_save_prompt():
    """Untuk opencode (tidak punya transcript JSONL): simpan maksud user per sesi."""
    payload = read_json("/dev/stdin", {})
    prompt = one_line(payload.get("prompt"), 400)
    cwd = payload.get("cwd") or os.getcwd()
    session = str(payload.get("session_id") or "")
    if len(prompt) < 12:
        return 0
    h = hashlib.sha1((prompt + "|" + cwd + "|" + session).encode()).hexdigest()[:12]
    seen = read_json(SEEN, {})
    if h in seen:
        return 0
    seen[h] = int(time.time())
    write_atomic(SEEN, json.dumps(seen))
    project = os.path.basename(cwd.rstrip("/")) or "root"
    text = "\n".join([
        "---", "tags: [agent-memory, session]", "date: %s" % time.strftime("%Y-%m-%d %H:%M"),
        "project: %s" % project, "tool: opencode", "---", "",
        "# %s — %s" % (project, one_line(prompt, 90)), "",
        "- **Folder**: `%s`" % cwd,
        "- **Permintaan**: %s" % prompt, "",
    ])
    name = "%s-%s.md" % (time.strftime("%Y-%m-%d-%H%M"), (session[:8] or h[:8]))
    write_atomic(os.path.join(SESS_DIR, name), text)
    write_atomic(os.path.join(VAULT, name), text)
    return 0


def recent_bullets(path, n):
    try:
        with open(path) as f:
            lines = [l.rstrip() for l in f if l.strip().startswith("- ")]
    except Exception:
        return []
    return lines[-n:]


def cmd_recall():
    argv = sys.argv[1:]
    project = None
    if "--project" in argv:
        project = argv[argv.index("--project") + 1]
    project = project or os.getcwd()
    out = []

    glob = recent_bullets(GLOBAL_MD, MAX_BULLETS)
    if glob:
        out.append("[memori global] " + " ‖ ".join(g.lstrip("- ")[:150] for g in glob))

    proj_file = os.path.join(PROJ_DIR, slug(project) + ".md")
    proj = recent_bullets(proj_file, 5)
    if proj:
        out.append("[memori proyek %s] %s" % (os.path.basename(project), " ‖ ".join(p.lstrip("- ")[:150] for p in proj)))

    try:
        sess = sorted(os.listdir(SESS_DIR))[-3:]
    except Exception:
        sess = []
    for s in reversed(sess):
        try:
            head = [l.strip() for l in open(os.path.join(SESS_DIR, s), errors="ignore") if l.strip().startswith("# ")]
        except Exception:
            continue
        if head:
            out.append("[sesi] %s: %s" % (s[:16], head[0][2:120]))
    if not out:
        return 0
    print(("\n".join(out))[:1200])
    return 0


def cmd_add():
    fact = " ".join(sys.argv[2:]).strip()
    if not fact:
        return 1
    line = "- %s — %s\n" % (time.strftime("%Y-%m-%d"), fact)
    os.makedirs(MEM_DIR, exist_ok=True)
    if not os.path.exists(GLOBAL_MD):
        write_atomic(GLOBAL_MD, "# Memory — global\n\n")
    with open(GLOBAL_MD, "a") as f:
        f.write(line)
    print("tersimpan: " + line.strip())
    return 0


def cmd_list():
    try:
        files = sorted(os.listdir(SESS_DIR))[-15:]
    except Exception:
        files = []
    for f in files:
        print(f)
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "recall"
    try:
        sys.exit({"save": cmd_save, "save-prompt": cmd_save_prompt, "recall": cmd_recall,
                  "add": cmd_add, "list": cmd_list}.get(cmd, cmd_recall)())
    except KeyboardInterrupt:
        sys.exit(0)
