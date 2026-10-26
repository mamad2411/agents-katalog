#!/usr/bin/env python3
"""fix-skill-name-canonical.py — selaraskan `name:` frontmatter dengan nama folder.

Aturan katalog (`AGENTS.md`): "Nama file = kanonik" -> `name:` di frontmatter
HARUS sama dengan nama folder (kebab-case). Skrip ini menyapu skill curated
yang `name:`-nya beda dari folder dan menulis ulang HANYA baris `name:` itu.

Aman & idempotent:
  - backup per-file: <folder>/SKILL.md.bak-YYYYMMDD (hanya sekali/hari)
  - hanya mengubah baris `name:` di blok frontmatter (di antara '---' pertama)
  - kalau sudah sama -> dilewati (jalan 2x = tidak ada perubahan)
  - tanpa argumen = dry-run (tidak menulis apa pun)

Pakai:
  python3 ~/.agents/fix-skill-name-canonical.py            # dry-run (lihat rencana)
  python3 ~/.agents/fix-skill-name-canonical.py --apply    # tulis + backup
"""
import re
import argparse
from datetime import datetime
from pathlib import Path

AGENTS = Path.home() / ".agents"
SKILLS = AGENTS / "skills"
if not SKILLS.is_dir():
    # katalog yang benar sejak 2026-09: skills-store (skills/ cuma folder symlink flow)
    SKILLS = AGENTS / "skills-store"
STAMP = datetime.now().strftime("%Y%m%d")

NAME_RE = re.compile(r"^([ \t]*name[ \t]*:[ \t]*)(.*?)([ \t]*)$")


def frontmatter_span(lines):
    """Kembalikan (start, end) index baris di dalam blok frontmatter, atau None.

    Frontmatter = blok di antara '---' pertama dan '---' berikutnya.
    """
    if not lines:
        return None
    if lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (1, i)
    return None


def patch_file(path, folder_name, apply=False, log=None):
    """Selaraskan satu SKILL.md. Return 'changed' | 'ok' | 'skip:<alasan>'."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"skip:read-error({e})"
    lines = text.split("\n")
    span = frontmatter_span(lines)
    if not span:
        return "skip:no-frontmatter"
    start, end = span

    hit = None
    for i in range(start, end):
        m = NAME_RE.match(lines[i])
        if m:
            hit = (i, m)
            break
    if hit is None:
        return "skip:no-name-key"
    i, m = hit
    old_val = m.group(2).strip().strip('"').strip("'")
    if old_val == folder_name:
        return "ok"

    if apply:
        bak = path.with_name(path.name + f".bak-{STAMP}")
        if not bak.exists():
            bak.write_text(text, encoding="utf-8")
        lines[i] = f"{m.group(1)}{folder_name}{m.group(3)}"
        path.write_text("\n".join(lines), encoding="utf-8")
    if log is not None:
        log.append((folder_name, old_val, str(path)))
    return "changed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="tulis perubahan (default dry-run)")
    ap.add_argument("--limit", type=int, default=0, help="batasi jumlah file (uji coba)")
    args = ap.parse_args()

    if not SKILLS.is_dir():
        print(f"ERROR: {SKILLS} tidak ada")
        return 1

    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    changes, ok, skipped = [], 0, []

    for d in dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            skipped.append((d.name, "no-SKILL.md"))
            continue
        res = patch_file(skill_md, d.name, apply=args.apply, log=changes)
        if res == "changed":
            if args.limit and len(changes) >= args.limit:
                break
        elif res == "ok":
            ok += 1
        else:
            skipped.append((d.name, res.split(":", 1)[1]))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] folder diperiksa : {len(dirs)}")
    print(f"[{mode}] sudah sinkron    : {ok}")
    print(f"[{mode}] akan diubah      : {len(changes)}")
    print(f"[{mode}] dilewati         : {len(skipped)}")
    if skipped:
        for n, r in skipped[:10]:
            print(f"    skip  {n}  ({r})")
    if changes:
        print(f"\ncontoh {'perubahan' if args.apply else 'rencana'} (folder | name lama):")
        for folder, old, _p in changes[:15]:
            print(f"  {folder:<42} <- {old!r}")
        if len(changes) > 15:
            print(f"  ... +{len(changes) - 15} lagi")
    if not args.apply and changes:
        print("\nJalankan ulang dengan --apply untuk menulis (backup otomatis).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
