#!/usr/bin/env python3
"""
Link Skills -> Repo Refs
========================
Kalau sebuah skill punya repo GitHub, dan repo itu ADA di repo-refs,
maka tulis REPO-REF.md di folder skill + catat di skills-repo-map.json.

Sumber repo per skill:
  1. ~/.agents/.skill-lock.json  (field "source" / "sourceUrl")
  2. frontmatter SKILL.md        (source:, repo:, sourceUrl:)
  3. nama skill "gh-user-repo-..."
  4. nama folder skill sendiri

Usage:
  python3 link-skills-repos.py            # laporan saja (dry-run)
  python3 link-skills-repos.py --apply    # tulis REPO-REF.md
"""

import os
import re
import sys
import json
from datetime import datetime

SKILLS = os.path.expanduser("~/.agents/skills-store")
REFS = os.path.expanduser("~/.agents/repo-refs")
LOCK = os.path.expanduser("~/.agents/.skill-lock.json")
MAP = os.path.expanduser("~/.agents/skills-repo-map.json")
APPLY = "--apply" in sys.argv
NORM = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def repo_index():
    """norm(name) -> nama folder repo-refs"""
    idx = {}
    if not os.path.isdir(REFS):
        return idx
    for n in os.listdir(REFS):
        if n.startswith(".") or not os.path.isdir(os.path.join(REFS, n)):
            continue
        idx[NORM(n)] = n
    return idx


def candidates(skill_name, lock_entry):
    c = []
    if lock_entry:
        for k in ("source", "sourceUrl", "repo"):
            v = lock_entry.get(k)
            if v:
                c.append(str(v))
        sp = lock_entry.get("skillPath")
        if sp:
            c.append(sp)
    if skill_name.startswith("gh-"):
        c.append(skill_name[3:])
    c.append(skill_name)
    out = []
    for v in c:
        v = v.replace("https://github.com/", "").replace(".git", "")
        v = v.split("/tree/")[0].split("/blob/")[0].strip("/")
        if v:
            out.append(v)
    return out


def frontmatter_sources(path):
    try:
        with open(path, errors="ignore") as f:
            head = f.read(1500)
    except OSError:
        return []
    res = []
    for m in re.finditer(r"https://github\.com/([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)",
                         head):
        res.append(m.group(1))
    for m in re.finditer(r"^(?:source|repo|sourceUrl):\s*[\"']?([^\s\"']+)",
                         head, re.M):
        res.append(m.group(1))
    return res


def main():
    idx = repo_index()
    lock = load_json(LOCK, {})
    lock_skills = lock.get("skills", {}) if isinstance(lock, dict) else {}
    print(f"repo-refs index: {len(idx)} | skill-lock: {len(lock_skills)}")

    hit, miss = {}, 0
    if not os.path.isdir(SKILLS):
        print("folder skills tidak ada")
        return
    names = sorted(n for n in os.listdir(SKILLS)
                   if not n.startswith(".") and os.path.isdir(os.path.join(SKILLS, n)))
    for sn in names:
        sp = os.path.join(SKILLS, sn)
        cands = candidates(sn, lock_skills.get(sn)) + frontmatter_sources(
            os.path.join(sp, "SKILL.md"))
        found = None
        for c in cands:
            n = NORM(c)
            if n in idx:
                found = idx[n]
                break
            # coba bentuk user_repo apa adanya
            alt = NORM(c.replace("/", "_"))
            if alt in idx:
                found = idx[alt]
                break
        if found:
            hit[sn] = found
        else:
            miss += 1

    print(f"skill punya repo di repo-refs: {len(hit)} | tanpa repo: {miss}")

    if APPLY:
        for sn, rn in hit.items():
            stub = os.path.join(REFS, rn, "STUB.md")
            body = ""
            try:
                with open(stub, errors="ignore") as f:
                    body = f.read()[:2500]
            except OSError:
                pass
            txt = (f"# Repo Referensi: {rn.replace('_', '/')}\n\n"
                   f"Repo: https://github.com/{rn.replace('_', '/')}\n"
                   f"Ref lokal: {os.path.join(REFS, rn)}\n"
                   f"API: curl \"localhost:27126/repos/readme?name={rn}\"\n"
                   f"Dibuat: {datetime.now().isoformat()[:10]}\n\n"
                   f"## Cuplikan README\n{body}\n")
            with open(os.path.join(SKILLS, sn, "REPO-REF.md"), "w") as f:
                f.write(txt)
        out = {"version": "1.0", "updated": datetime.now().isoformat(),
               "total_skills": len(names), "with_repo": len(hit),
               "map": hit}
        with open(MAP, "w") as f:
            json.dump(out, f, indent=2)
        print(f"DITULIS: {len(hit)} REPO-REF.md | map -> {MAP}")
    else:
        for sn, rn in list(hit.items())[:15]:
            print(f"  {sn}  ->  {rn}")
        print("\n(dry-run — tambahkan --apply untuk eksekusi)")


if __name__ == "__main__":
    main()