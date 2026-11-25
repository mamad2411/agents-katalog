#!/usr/bin/env python3
"""repo-map.py — peta cepat sebuah repo/proyek: bahasa, struktur, fitur, cara pakai.

  repo-map.py [DIR] [--json] [--depth N]

Output ≤ 22 baris (~400 token): cukup untuk AI paham struktur proyek sebelum
membaca file satu per satu. Tanpa dependensi, tanpa jaringan.
"""
import json
import os
import subprocess
import sys

SKIP = {"node_modules", ".git", "dist", "build", "out", "target", ".next", ".nuxt", "coverage",
        "__pycache__", ".venv", "venv", "env", ".idea", ".vscode", "vendor", ".turbo",
        ".cache", "Pods", "DerivedData", ".gradle", "bin", "obj", ".terraform"}
LANG = {".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript",
        ".py": "Python", ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
        ".swift": "Swift", ".dart": "Dart", ".rb": "Ruby", ".php": "PHP", ".cs": "C#",
        ".c": "C", ".h": "C", ".cpp": "C++", ".sh": "Shell", ".sql": "SQL",
        ".vue": "Vue", ".svelte": "Svelte", ".html": "HTML", ".css": "CSS", ".scss": "SCSS"}
FRAMEWORKS = {
    "next": "Next.js", "react": "React", "vue": "Vue", "svelte": "Svelte", "@angular/core": "Angular",
    "express": "Express", "fastify": "Fastify", "nestjs": "NestJS", "@nestjs/core": "NestJS",
    "tailwindcss": "Tailwind", "vite": "Vite", "electron": "Electron", "react-native": "React Native",
    "expo": "Expo", "prisma": "Prisma", "@prisma/client": "Prisma", "drizzle-orm": "Drizzle",
    "fastapi": "FastAPI", "flask": "Flask", "django": "Django", "sqlalchemy": "SQLAlchemy",
    "torch": "PyTorch", "tensorflow": "TensorFlow", "pandas": "pandas", "streamlit": "Streamlit",
}
MANIFESTS = ["package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml",
             "pubspec.yaml", "composer.json", "Gemfile", "pom.xml", "build.gradle", "Makefile"]


def run(cmd, cwd):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=4).stdout.strip()
    except Exception:
        return ""


def scan(root, max_files=60000):
    files = []          # (relpath, size)
    loc = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            files.append((rel, size))
            ext = os.path.splitext(fn)[1].lower()
            if ext in LANG:
                lang = LANG[ext]
                cur = loc.setdefault(lang, [0, 0])
                cur[0] += 1
                try:
                    with open(p, errors="ignore") as f:
                        cur[1] += sum(1 for _ in f)
                except Exception:
                    pass
            if len(files) >= max_files:
                return files, loc
    return files, loc


def deps(root):
    names, scripts = set(), {}
    pj = os.path.join(root, "package.json")
    if os.path.exists(pj):
        try:
            d = json.load(open(pj))
            names |= set((d.get("dependencies") or {}).keys())
            names |= set((d.get("devDependencies") or {}).keys())
            scripts = d.get("scripts") or {}
        except Exception:
            pass
    for f in ("pyproject.toml", "requirements.txt"):
        p = os.path.join(root, f)
        if os.path.exists(p):
            try:
                txt = open(p, errors="ignore").read().lower()
            except Exception:
                continue
            for k in FRAMEWORKS:
                if k in txt:
                    names.add(k)
    if os.path.exists(os.path.join(root, "go.mod")):
        try:
            names |= {l.split()[0] for l in open(os.path.join(root, "go.mod")) if "/" in l.split(" ")[0]}
        except Exception:
            pass
    return names, scripts


def has(root, *paths):
    return any(os.path.exists(os.path.join(root, p)) for p in paths)


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = os.path.abspath(argv[0] if argv else ".")
    as_json = "--json" in sys.argv
    if not os.path.isdir(root):
        print("bukan folder: " + root)
        return 1

    files, loc = scan(root)
    total = len(files)
    langs = sorted(loc.items(), key=lambda kv: -kv[1][1])[:5]
    names, scripts = deps(root)

    top = {}
    for rel, _ in files:
        head = rel.split(os.sep)[0]
        if os.sep not in rel:
            continue
        top[head] = top.get(head, 0) + 1
    top_dirs = sorted(top.items(), key=lambda kv: -kv[1])[:8]

    fw = sorted({v for k, v in FRAMEWORKS.items() if k in names})
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    last = run(["git", "log", "-1", "--date=short", "--pretty=%cd %s"], root)[:90]
    remote = run(["git", "remote", "get-url", "origin"], root)[:80]
    dirty = bool(run(["git", "status", "--porcelain"], root))
    manifests = [m for m in MANIFESTS if os.path.exists(os.path.join(root, m))]
    entries = []
    for cand in ("src/index.ts", "src/main.ts", "src/app", "src/App.tsx", "app/page.tsx", "pages/index.tsx",
                 "main.py", "app.py", "src/main.py", "manage.py", "cmd", "main.go", "src/main.rs", "index.js"):
        if os.path.exists(os.path.join(root, cand)):
            entries.append(cand)
    tests = has(root, "tests", "test", "__tests__", "spec", "src/__tests__")
    ci = os.path.isdir(os.path.join(root, ".github", "workflows")) or os.path.exists(os.path.join(root, ".gitlab-ci.yml"))

    if as_json:
        print(json.dumps({"root": root, "files": total, "languages": langs, "dirs": top_dirs,
                          "frameworks": fw, "manifests": manifests, "entries": entries,
                          "tests": tests, "ci": ci, "branch": branch, "last_commit": last,
                          "remote": remote, "dirty": dirty, "scripts": list(scripts)[:8]}, indent=1))
        return 0

    print("repo: %s" % root)
    if branch:
        print("git: %s%s · commit %s%s" % (branch, " (dirty)" if dirty else "", last,
                                           (" · " + remote) if remote else ""))
    else:
        print("git: bukan repo git")
    if fw:
        print("stack: %s" % ", ".join(fw[:6]))
    print("ukuran: %d file · %s" % (total, " · ".join("%s %d fil/%d LOC" % (l, c, n) for l, (c, n) in langs) or "-"))
    if top_dirs:
        print("struktur: " + " | ".join("%s/ %df" % (d, c) for d, c in top_dirs))
    if manifests:
        print("manifest: " + ", ".join(manifests))
    if entries:
        print("entry: " + ", ".join(entries[:6]))
    if scripts:
        print("scripts: " + ", ".join(list(scripts)[:8]))
    marks = []
    marks.append("tests ✓" if tests else "tests ✗")
    marks.append("CI ✓" if ci else "CI ✗")
    marks.append("Docker ✓" if has(root, "Dockerfile", "docker-compose.yml", "compose.yaml") else "Docker ✗")
    marks.append("env ✓" if has(root, ".env.example", ".env.sample") else "env ✗")
    marks.append("README ✓" if has(root, "README.md", "readme.md") else "README ✗")
    print("kesehatan: " + " · ".join(marks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
