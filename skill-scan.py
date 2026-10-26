#!/usr/bin/env python3
"""skill-scan.py — pindai pola berbahaya di skill (read-only, tidak menghapus).

Cari di semua file teks (SKILL.md, scripts/) pola yang bisa merusak mesin,
mencuri kredensial, atau menarik kode dari internet saat skill dijalankan.

Pakai:
  python3 skill-scan.py                # ringkasan + temuan HIGH
  python3 skill-scan.py --all          # termasuk MEDIUM
  python3 skill-scan.py --json
  python3 skill-scan.py --path DIR     # scan folder lain
Exit: 0 aman, 1 ada HIGH.
"""
import json
import os
import re
import sys

AG = os.path.expanduser("~/.agents")
DEFAULT = f"{AG}/skills-store"
TEXT_EXT = {".md", ".sh", ".py", ".js", ".ts", ".tsx", ".json", ".yaml", ".yml", ".toml", ""}
SKIP = {".git", "node_modules", ".dupes", "__pycache__"}

RULES = [
    # (severity, label, regex)
    ("HIGH", "pipe ke shell", r"(curl|wget)[^\n|]{0,120}\|\s*(sudo\s+)?(ba)?sh\b"),
    ("HIGH", "rm -rf root/home", r"rm\s+-[rf]{1,2}\s+(/|~|\$HOME)(\s|\*|$)"),
    ("HIGH", "hapus filesystem", r"\b(mkfs|dd\s+if=|shred\s+|diskutil\s+erase)"),
    ("HIGH", "exfil kredensial", r"(AWS_SECRET|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC|SSH_AUTHORIZED|id_rsa)[^\n]{0,80}(curl|wget|nc\s|base64)"),
    ("HIGH", "kirim file ke URL", r"(curl|wget)[^\n]{0,120}(-F|--data-binary|--upload-file)\s"),
    ("HIGH", "base64 | shell", r"base64\s+(-d|--decode)[^\n]{0,60}\|\s*(ba)?sh"),
    ("HIGH", "eval unduhan", r"eval\s*[\(\"']?\s*\$\("),
    ("HIGH", "kunci SSH diedit", r"(>>|tee|sed\s+-i)[^\n]{0,60}(\.ssh/|authorized_keys)"),
    ("HIGH", "crontab/launchd persist", r"(crontab\s+-|launchctl\s+load|/Library/LaunchDaemons)"),
    ("HIGH", "sudo minta tanpa izin", r"(^|\s)sudo\s+(-S|sh|bash|rm|chmod|chown)"),
    ("MED", "chmod 777", r"chmod\s+(-R\s+)?777"),
    ("MED", "npm/gem publish", r"\b(npm\s+publish|gem\s+push|twine\s+upload)"),
    ("MED", "git force push", r"git\s+push[^\n]{0,40}(--force|-f)\b"),
    ("MED", "matikan proteksi mac", r"(csrutil\s+disable|spctl\s+--master-disable)"),
    ("MED", "baca seluruh home", r"(tar|zip)[^\n]{0,40}(~\s|/Users/[^\s]+|/etc/)"),
    ("MED", "token di-hardcode", r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})"),
]

COMPILED = [(sev, label, re.compile(rx, re.M)) for sev, label, rx in RULES]


def severity_for(path, sev):
    """Markdown = referensi (AI baca lalu putuskan); script = bisa langsung dieksekusi."""
    ext = os.path.splitext(path)[1].lower()
    executable = ext in (".sh", ".py", ".js", ".ts") or "/scripts/" in path.replace("\\", "/")
    if sev == "HIGH" and not executable:
        return "MED"
    return sev


def scan_file(p, root=""):
    hits = []
    try:
        text = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return hits
    rel = os.path.relpath(p, root) if root else p
    for sev, label, rx in COMPILED:
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            lines = text.splitlines()
            cur = lines[line - 1] if line - 1 < len(lines) else ""
            prev = lines[line - 2] if line >= 2 else ""
            stripped = cur.lstrip()
            if stripped.startswith(("#", "//", "*", "--")):
                continue                      # komentar, bukan perintah
            if "skill-scan: allow" in cur or "skill-scan: allow" in prev:
                continue                      # dianotasi manual sebagai by-design
            snippet = " ".join(m.group(0).split())[:90]
            hits.append({"sev": severity_for(rel, sev), "label": label,
                         "line": line, "code": snippet})
    return hits


def main():
    show_all = "--all" in sys.argv
    as_json = "--json" in sys.argv
    root = DEFAULT
    if "--path" in sys.argv:
        try:
            root = os.path.expanduser(sys.argv[sys.argv.index("--path") + 1])
        except IndexError:
            pass

    findings = {}
    files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for f in filenames:
            if os.path.splitext(f)[1].lower() not in TEXT_EXT:
                continue
            p = os.path.join(dirpath, f)
            if os.path.getsize(p) > 2_000_000:
                continue
            files += 1
            hits = scan_file(p, root)
            hits = [h for h in hits if show_all or h["sev"] == "HIGH"]
            if hits:
                findings[os.path.relpath(p, root)] = hits

    high = sum(1 for v in findings.values() for h in v if h["sev"] == "HIGH")
    med = sum(1 for v in findings.values() for h in v if h["sev"] == "MED")
    if as_json:
        json.dump({"files": files, "files_terdampak": len(findings),
                   "high": high, "med": med, "detail": findings},
                  sys.stdout, indent=1, ensure_ascii=False)
        print()
    else:
        print(f"file dipindai : {files}")
        print(f"file terdampak: {len(findings)}")
        print(f"HIGH: {high} · MED: {med}")
        for p, hits in list(findings.items())[:15]:
            print(f"\n{p}")
            for h in hits[:3]:
                print(f"  [{h['sev']}] {h['label']} (baris {h['line']}): {h['code']}")
        if findings:
            print("\nTindakan: review manual. Skill katalog hanya dibaca (tidak ada yang dijalankan "
                  "otomatis), jadi ini risiko saat skill dipanggil — bukan infeksi aktif.")
    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())
