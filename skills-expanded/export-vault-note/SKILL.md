---
name: export-vault-note
description: >
  Exports a single Obsidian vault note and all its linked images into a portable zip or
  tar.gz archive, preserving vault-root-relative paths so the archive unpacks correctly
  anywhere. Use only when the user explicitly invokes /export-vault-note.
user-invocable: true
allowed-tools: Bash
argument-hint: "<vault-relative-path-to-note> [zip|tar] [output-dir]"
compatibility: Python 3 required (standard library only — zipfile, tarfile, pathlib, re). Must be invoked from within or near an Obsidian vault directory.
---

# Export Vault Note

This skill runs inside an **Obsidian vault**. It bundles a single Markdown note and every image it links into a portable archive placed at a location of the user's choosing (defaulting to one directory above the vault root).

Handles two image link styles:
- Wiki-style: `![[image.png]]` or `![[subfolder/image.png]]`
- Inline Markdown: `![alt text](path/to/image.png)`

**Example:**
```
/export-vault-note projects/blog/my-post.md zip ~/Desktop
```

---

## Step 1 — Parse Arguments

Read `$ARGUMENTS`. Extract:
- `note_path` — vault-relative path to the Markdown file (e.g. `ai/notes/my-note.md`)
- `format` — `zip` or `tar`
- `output_dir` — absolute or relative path where the archive should be saved

If `note_path` is missing, ask: *"Which note do you want to export? Provide the vault-relative path, e.g. `ai/notes/my-note.md`."*

If `format` is not provided, ask: *"Do you want a `zip` or `tar` archive?"*

If `output_dir` is not provided, tell the user: *"The archive will be saved to one directory above the vault root by default. Is that OK, or do you want a different location?"* Wait for confirmation or a new path before continuing.

---

## Step 2 — Locate the Vault Root

Walk up the directory tree from the current working directory looking for a `.obsidian` folder. If the note path given is absolute, also try walking up from its parent directory.

```bash
python3 -c "
import sys
from pathlib import Path
for start in sys.argv[1:]:
    p = Path(start).resolve()
    for candidate in [p] + list(p.parents):
        if (candidate / '.obsidian').is_dir():
            print(candidate)
            raise SystemExit(0)
print('')
" "." "<absolute-note-parent-if-known>"
```

If the output is empty (no `.obsidian` found), ask: *"I couldn't detect the vault root automatically. What is the absolute path to your vault root?"*

---

## Step 3 — Run the Export

Write the script below to `/tmp/export_vault_note.py` and run it. The script is embedded directly so the skill works regardless of install location.

```bash
cat > /tmp/export_vault_note.py << 'PYEOF'
import sys
import re
import zipfile
import tarfile
from pathlib import Path


def find_vault_wide(vault_root, name):
    for p in vault_root.rglob(name):
        return p
    return None


def collect_images(vault_root, note_path):
    content = note_path.read_text(encoding="utf-8")
    note_dir = note_path.parent
    images = []
    warnings = []
    seen = set()

    wiki = re.findall(r"!\[\[([^\]|#]+)", content)
    inline = re.findall(r"!\[[^\]]*\]\(([^)#\s]+)", content)

    for ref in wiki + inline:
        ref = ref.strip()
        if not ref or ref in seen:
            continue
        seen.add(ref)

        if re.match(r"https?://", ref):
            warnings.append(f"Skipping external image: {ref}")
            continue

        abs_path = None
        if "/" in ref or "\\" in ref:
            for candidate in [vault_root / ref, note_dir / ref]:
                if candidate.exists():
                    abs_path = candidate
                    break
        else:
            found = find_vault_wide(vault_root, ref)
            if found:
                abs_path = found
                print(f"Resolved bare link '{ref}' -> {abs_path.relative_to(vault_root)}")

        if abs_path is None:
            warnings.append(f"Warning: image not found, skipping: {ref}")
            continue

        try:
            vault_rel = str(abs_path.relative_to(vault_root))
            images.append((abs_path, vault_rel))
        except ValueError:
            warnings.append(f"Warning: image outside vault, skipping: {abs_path}")

    return images, warnings


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <vault_root> <note_rel_path> [zip|tar] [output_dir]", file=sys.stderr)
        sys.exit(1)

    vault_root = Path(sys.argv[1]).resolve()
    note_rel = sys.argv[2]
    fmt = sys.argv[3] if len(sys.argv) > 3 else "zip"
    output_dir = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else vault_root.parent

    if fmt not in ("zip", "tar"):
        print(f"Error: format must be 'zip' or 'tar', got '{fmt}'", file=sys.stderr)
        sys.exit(1)

    if not vault_root.is_dir():
        print(f"Error: vault root not found: {vault_root}", file=sys.stderr)
        sys.exit(1)

    note_path = vault_root / note_rel
    if not note_path.exists():
        print(f"Error: note not found: {note_path}", file=sys.stderr)
        sys.exit(1)

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    images, warnings = collect_images(vault_root, note_path)
    stem = note_path.stem

    if fmt == "tar":
        archive_path = output_dir / f"{stem}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(note_path, arcname=note_rel)
            for abs_path, vault_rel in images:
                tar.add(abs_path, arcname=vault_rel)
    else:
        archive_path = output_dir / f"{stem}.zip"
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(note_path, note_rel)
            for abs_path, vault_rel in images:
                zf.write(abs_path, vault_rel)

    print(f"Archive: {archive_path}")
    print(f"Note: {note_rel}")
    for _, vault_rel in images:
        print(f"Image: {vault_rel}")
    for w in warnings:
        print(w)


if __name__ == "__main__":
    main()
PYEOF
python3 /tmp/export_vault_note.py "<vault_root>" "<note_rel_path>" "<format>" "<output_dir>"
```

Substitute all four values. If the user accepted the default output location, resolve and pass `vault_root.parent` explicitly.

---

## Step 4 — Report Results

Parse the script output and report:

- **Archive created:** full path
- **Note inside archive:** vault-relative path
- **Images included:** one line each
- **Warnings:** skipped images, resolved bare links — display each prominently so the user can investigate if needed
