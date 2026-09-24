#!/usr/bin/env python3
"""
Skill Auto-Symlink Daemon (Manifest-Diff v3)
=============================================
Uses a manifest to track symlinked skills. Only processes NEW skills.
O(new_skills) instead of O(1.5M entries) per run.

Triggers:
  - launchd: every 30 minutes (dikunci MIN_INTERVAL via .symlink-run.lock — anti-loop)
  - manual:  python3 ~/.agents/skill-auto-symlink.py [--verbose] [--force]
  - load:    python3 ~/.agents/skill-auto-symlink.py load <skill-name>
"""
import os, sys, gzip, json, time
from datetime import datetime

HOME = os.path.expanduser("~")
AGENTS = os.path.join(HOME, ".agents")
SKILLS_DIR = os.path.join(AGENTS, "skills")
CATALOG_DIR = os.path.join(AGENTS, "skills-catalog")
EXPANDED_DIR = os.path.join(AGENTS, "skills-expanded")
MANIFEST_FILE = os.path.join(AGENTS, ".symlink-manifest.json")
LOG_FILE = os.path.join(AGENTS, "skill-auto-symlink.log")
LOG_FILE = os.path.join(AGENTS, "skill-auto-symlink.log")
LOCK_FILE = os.path.join(AGENTS, ".symlink-run.lock")   # kunci anti-loop
MIN_INTERVAL = 1800                                     # detik (30 menit) antar-run otomatis

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    if VERBOSE:
        print(line, file=sys.stderr)


def get_tool_skill_dirs():
    tools = []
    for d in os.listdir(HOME):
        if not d.startswith(".") or d.startswith(".."):
            continue
        if d == ".agents":
            continue
        sp = os.path.join(HOME, d, "skills")
        if os.path.isdir(sp) and not os.path.islink(sp):
            tools.append(sp)
    return tools


def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE) as f:
                return set(json.load(f).get("skills", []))
        except Exception:
            pass
    return set()


def save_manifest(skill_set):
    with open(MANIFEST_FILE, "w") as f:
        json.dump({"skills": sorted(skill_set), "count": len(skill_set)}, f, separators=(",", ":"))


def symlink_to_all(skill_name, src_dir, tools):
    created = 0
    for tool_dir in tools:
        dst = os.path.join(tool_dir, skill_name)
        if os.path.exists(dst) or os.path.islink(dst):
            continue
        try:
            os.symlink(src_dir, dst)
            created += 1
        except OSError:
            pass
    return created


def load_skill_on_demand(skill_name):
    """Load a catalog skill on-demand: decompress .gz into skills-expanded/, symlink."""
    gz_path = os.path.join(CATALOG_DIR, f"{skill_name}.md.gz")
    if not os.path.exists(gz_path):
        custom = os.path.join(SKILLS_DIR, skill_name)
        if os.path.isdir(custom):
            tools = get_tool_skill_dirs()
            n = symlink_to_all(skill_name, custom, tools)
            log(f"  LOAD custom {skill_name} -> {n} tools")
            return True
        log(f"  LOAD ERR: {skill_name} not found")
        return False
    dst_dir = os.path.join(EXPANDED_DIR, skill_name)
    dst_md = os.path.join(dst_dir, "SKILL.md")
    if not os.path.exists(dst_md):
        try:
            os.makedirs(dst_dir, exist_ok=True)
            with gzip.open(gz_path, "rt", encoding="utf-8", errors="ignore") as f_in:
                content = f_in.read()
            with open(dst_md, "w", encoding="utf-8") as f_out:
                f_out.write(content)
        except Exception as e:
            log(f"  EXPAND ERR: {skill_name} -> {e}")
            return False
    tools = get_tool_skill_dirs()
    n = symlink_to_all(skill_name, dst_dir, tools)
    log(f"  LOAD catalog {skill_name} -> {n} tools")
    return True


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "load":
        ok = load_skill_on_demand(sys.argv[2])
        sys.exit(0 if ok else 1)

    # ==== KUNCI ANTI-LOOP (laptop panas) ====
    # launchd bisa me-restart agent jauh lebih sering dari StartInterval
    # (kombinasi KeepAlive+StartInterval). Kunci ini memastikan body tidak
    # jalan lebih cepat dari MIN_INTERVAL, KECUALI dipanggil manual --force.
    force = "--force" in sys.argv
    try:
        last = os.path.getmtime(LOCK_FILE)
        if not force and (time.time() - last) < MIN_INTERVAL:
            if VERBOSE:
                log("Skip: baru jalan %.0fs lalu (kunci anti-loop; pakai --force)"
                    % (time.time() - last))
            return
    except OSError:
        pass
    open(LOCK_FILE, "w").write(time.strftime("%Y-%m-%dT%H:%M:%S"))

    t0 = time.time()
    tools = get_tool_skill_dirs()

    # Load manifest — only process skills NOT in manifest
    manifest = load_manifest()

    # Collect current skill names from skills/ and skills-expanded/
    # TIERED (biar AI tidak berat): hanya skill CORE yang di-auto-link.
    # Sisanya diakses via MCP skill-catalog. --full untuk perilaku lama.
    core_names = None
    if "--full" not in sys.argv:
        try:
            core_f = os.path.join(AGENTS, "skill-core.json")
            d = json.load(open(core_f))
            core_names = set(d.get("core") or []) | set(d.get("full_native") or [])
        except Exception:
            core_names = set()

    current = set()
    if os.path.isdir(SKILLS_DIR):
        for s in os.listdir(SKILLS_DIR):
            if not s.startswith(".") and os.path.isdir(os.path.join(SKILLS_DIR, s)):
                if core_names is None or s in core_names:
                    current.add(("custom", s))
    if os.path.isdir(EXPANDED_DIR):
        for s in os.listdir(EXPANDED_DIR):
            if not s.startswith(".") and os.path.isdir(os.path.join(EXPANDED_DIR, s)):
                if core_names is None or s in core_names:
                    current.add(("expanded", s))

    # Diff: only process skills not in manifest
    new_skills = [(typ, name) for typ, name in current if name not in manifest]

    if not new_skills:
        elapsed = time.time() - t0
        log(f"Idle: 0 new skills ({len(manifest)} tracked, {elapsed:.1f}s)")
        return

    total_linked = 0
    for typ, skill in new_skills:
        src = os.path.join(SKILLS_DIR if typ == "custom" else EXPANDED_DIR, skill)
        n = symlink_to_all(skill, src, tools)
        if n:
            total_linked += n
            log(f"  +{typ[:3].upper()} {skill} -> {n} tools")
        manifest.add(skill)

    save_manifest(manifest)
    elapsed = time.time() - t0
    log(f"Done: {len(new_skills)} new, {total_linked} symlinks ({len(manifest)} tracked, {elapsed:.1f}s)")


if __name__ == "__main__":
    main()
