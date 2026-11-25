#!/usr/bin/env python3
"""skills-ready — cek skill mana yang benar-benar bisa dipakai di device ini.

Kenapa: katalog besar (304k) tapi banyak skill butuh CLI yang tidak terpasang
(wrangler, docker, jq, ...). Tanpa cek ini, AI memuat skill lalu gagal di tengah.

Pakai:
  python3 ~/.agents/skills-ready.py            # semua skills-store + agent-assets
  python3 ~/.agents/skills-ready.py --all      # + skills-expanded (lebih lama)
  python3 ~/.agents/skills-ready.py --report   # tulis ~/.agents/skills-readiness.md

Output: ~/.agents/skills-readiness.json  {nama: {"ready": bool, "missing": [..], "checks": [..]}}
"""
import json
import os
import re
import shutil
import sqlite3
import sys

HOME = os.path.expanduser("~")
DB = os.path.join(HOME, ".agents", "skills-index.db")
OUT_JSON = os.path.join(HOME, ".agents", "skills-readiness.json")
OUT_MD = os.path.join(HOME, ".agents", "skills-readiness.md")

# nama CLI yang dikenal (dicek lewat PATH, tanpa menjalankannya)
KNOWN_CLI = {
    "wrangler", "docker", "kubectl", "helm", "terraform", "ansible", "gh", "git",
    "node", "npx", "npm", "pnpm", "bun", "deno", "python3", "pip", "pip3", "uv",
    "ffmpeg", "ffprobe", "tesseract", "jq", "yq", "curl", "wget", "rg", "fd",
    "psql", "mysql", "sqlite3", "redis-cli", "mongosh", "aws", "gcloud", "az",
    "vercel", "netlify", "heroku", "fly", "flyctl", "supabase", "stripe",
    "playwright", "cypress", "pytest", "jest", "vitest", "eslint", "prettier",
    "cargo", "rustc", "go", "swift", "xcodebuild", "podman", "minikube",
    "ollama", "huggingface-cli", "openai", "anthropic", "pandoc", "magick",
    "convert", "sox", "yt-dlp", "aria2c", "exiftool", "openssl", "ssh", "scp",
    "rsync", "tar", "zip", "unzip", "make", "cmake", "gcc", "clang", "java",
    "mvn", "gradle", "php", "composer", "ruby", "bundle", "gem", "dotnet",
    "mcporter", "mamat", "opencode", "sk",
}


ALIAS = {"pip": "pip3", "convert": "magick", "fly": "flyctl", "sk": "skillq.py"}


# Tool yang memang hidup di level PROYEK (npm/pip lokal), bukan global.
# Tanpa ini, 200+ skill palsu diberi badge [butuh:pytest] padahal test runner
# selalu dipasang di repo masing-masing.
PROJECT_SCOPE = {"pytest", "vitest", "jest", "eslint", "prettier", "cypress",
                 "playwright", "anthropic", "supabase", "stripe", "npm", "pnpm",
                 "bun", "pip", "pip3", "uv", "cargo", "go", "mvn", "gradle",
                 "composer", "bundle", "gem", "dotnet", "podman", "mcporter"}


def build_cli_cache():
    available = {}
    for c in KNOWN_CLI:
        hit = shutil.which(c) or shutil.which(ALIAS.get(c, c))
        available[c] = bool(hit)
    return available


def extract_checks(text):
    """Ambil CLI yang benar-benar dipanggil / diminta skill (bukan sekadar disebut)."""
    found = set()
    # perintah di blok kode atau inline code: `wrangler deploy`, ```bash\nnpx ...
    for m in re.finditer(r"[`\n]\s*(?:sudo\s+)?([a-z][a-z0-9._-]{1,24})\s+(?:-[-\w]|\w)", text):
        c = m.group(1)
        if c in KNOWN_CLI:
            found.add(c)
    # deklarasi eksplisit
    for m in re.finditer(r"(?:requires?|prerequisite[s]?|install(?:ed)?|butuh|wajib)[^\n]{0,120}", text, re.I):
        for c in KNOWN_CLI:
            if re.search(rf"\b{re.escape(c)}\b", m.group(0)):
                found.add(c)
    return sorted(found)


def main():
    args = set(sys.argv[1:])
    scope = ["skills-store", "agent-assets"] + (["skills-expanded"] if ("--all" in args or "--active" in args) else [])
    cli = build_cli_cache()
    c = sqlite3.connect(DB, timeout=30)
    if "--active" in args:
        rows = c.execute("SELECT name, path FROM skills WHERE tier <> 'junk'").fetchall()
    else:
        rows = c.execute("SELECT name, path FROM skills").fetchall()
    result = {}
    scanned = 0
    for name, path in rows:
        if not path or "/" not in path:
            continue
        if "--active" not in args and not any(f"/.agents/{s}/" in path for s in scope):
            continue
        try:
            if os.path.getsize(path) > 200_000:
                continue
            text = open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        scanned += 1
        checks = extract_checks(text)
        missing = [x for x in checks if not cli.get(x) and x not in PROJECT_SCOPE]
        result.setdefault(name, {"ready": not missing, "missing": missing, "checks": checks})
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    ready = sum(1 for v in result.values() if v["ready"])
    print(f"[skills-ready] {scanned} skill diperiksa · siap={ready} · butuh-dependency={len(result) - ready}")
    if "--report" in args:
        need = [(n, v) for n, v in result.items() if not v["ready"]]
        need.sort(key=lambda x: len(x[1]["missing"]))
        with open(OUT_MD, "w", encoding="utf-8") as f:
            f.write("# Kesiapan skill di device ini\n\n")
            f.write(f"diperiksa: {scanned} · siap: {ready} · butuh dependency: {len(need)}\n\n")
            f.write("## Siap pakai (tanpa install tambahan)\n\n")
            for n, v in list((x for x in result.items() if x[1]["ready"]))[:80]:
                f.write(f"- `{n}` — {', '.join(v['checks']) or 'tanpa CLI khusus'}\n")
            f.write("\n## Butuh dependency\n\n")
            for n, v in need[:120]:
                f.write(f"- `{n}` — kurang: {', '.join(v['missing'])}\n")
        print(f"(laporan: {OUT_MD})")


if __name__ == "__main__":
    main()
