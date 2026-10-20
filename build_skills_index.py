#!/usr/bin/env python3
"""Build one fast, deduplicated SQLite FTS5 index dari ~/.agents/skills-store (curated)
dan ~/.agents/skills-expanded (scraped reference).

v2 (2026-09-18) - P0 ringan:
  * nama kanonik dari frontmatter `name:` (bukan nama folder hasil flatten path)
  * tier 3 tingkat: curated | reference | docs  (tanpa description => docs)
  * kolom tambahan: category (role) + source (repo dari .skill-lock.json)
  * baca hanya HEAD_BYTES pertama tiap SKILL.md (jauh lebih ringan)
  * tulis skills-junk.txt (daftar tier docs) untuk pembersihan P1
"""
import json
import os
import re
import sqlite3
from pathlib import Path

HOME = Path.home()
AGENTS = HOME / ".agents"
# sumber curated HARUS skills-store (katalog lengkap), BUKAN skills/ (folder symlink
# flow hanya berisi ~79 skill aktif). memakai skills/ = rebuild Licensed curated
# 3.176 -> 79 dan membanjiri tier reference.
CURATED_DIR = AGENTS / "skills-store"
REF_DIR = AGENTS / "skills-expanded"
DB_PATH = AGENTS / "skills-index.db"
LOCK_FILE = AGENTS / ".skill-lock.json"
ROLE_FILE = AGENTS / "role-skill-map.json"
JUNK_FILE = AGENTS / "skills-junk.txt"

HEAD_BYTES = 4096
FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
NAME_RE = re.compile(r"^name:\s*[\"']?([^\"'\n]+)", re.M)
DESC_RE = re.compile(r"^description:\s*[\"']?(.*?)[\"']?\s*(?:\n\S|$)", re.S | re.M)
FOLD_RE = re.compile(r"""^description:\s*["']?[>|][-+]?["']?\s*$""")
HEAD_RE = re.compile(r"^#\s+([A-Za-z][^\n#]*)$", re.M)
SKIP_HEAD = {"basic information", "categorization", "table of contents"}
H1_RE = re.compile(r"^#\s+(.+)$", re.M)
JUNK_TITLES = {"readme", "license", "changelog", "contributing", "code of conduct",
               "table of contents", "index", "summary", "overview of the api"}
API_DOC_RE = re.compile(r"^(class:|function|method|type:|interface|enum|module|api reference)", re.I)


def slug(text):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (text or "").strip().lower())
    return re.sub(r"-{2,}", "-", s).strip("-")


def first_h1(body):
    for m in H1_RE.finditer(body):
        t = re.sub(r"[*_`#]", "", m.group(1)).strip()
        if t and t.lower() not in JUNK_TITLES and 3 <= len(t) <= 60 and not API_DOC_RE.match(t):
            return t
    return ""


def first_paragraph(body, skip_title=""):
    """Paragraf pertama yang cukup informatif → dipakai sebagai deskripsi."""
    for blk in re.split(r"\n\s*\n", body):
        b = blk.strip()
        if not b or b.startswith(("#", "```", "|", "-", "*", ">", "<", "<!--")):
            continue
        b = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", b)          # link → teks
        b = re.sub(r"[*_`]", "", b)
        b = re.sub(r"\s+", " ", b).strip()
        if re.search(r"[;{}]", b) and len(b.split()) < 25:      # blok kode, bukan prosa
            continue
        if b.lower().rstrip(":") == (skip_title or "").lower():
            continue
        if len(b.split()) >= 8:
            return b[:240]
    return ""


def looks_like_skill(body, title):
    """Filter sampah: dokumen API/HTML/license/changelog, body terlalu pendek."""
    if not title:
        return False
    if len(body.split()) < 40:
        return False
    low = body[:400].lower()
    if low.lstrip().startswith("<"):
        return False
    if any(k in low for k in ("api reference", "class:", "extends:", "npm install undici")):
        return False
    return True
CAMEL_DOC_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")


def read_head(p):
    """Baca secukupnya: 4 KB cukup untuk mayoritas; fallback 64 KB bila frontmatter
    belum tertutup (skill dengan frontmatter panjang) — tetap jauh lebih ringan
    daripada membaca seluruh file."""
    text = ""
    for size in (HEAD_BYTES, 65536):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read(size)
        except Exception:
            return ""
        if FM_RE.match(text):
            return text
    return text


def first_heading(body):
    """Fallback deskripsi: heading pertama yang masuk akal (khusus tier curated)."""
    for m in HEAD_RE.finditer(body):
        t = m.group(1).strip()
        if t.lower() not in SKIP_HEAD:
            return t
    return ""


def parse_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return "", "", text
    fm = m.group(1)
    nm = NAME_RE.search(fm)
    name = nm.group(1).strip() if nm else ""
    desc = ""
    dm = DESC_RE.search(fm)
    if dm:
        desc = re.sub(r"\s+", " ", dm.group(1).replace("\\n", " ")).strip()
    if desc in (">", "|", ">-", "|-", ">+", "|+") or FOLD_RE.match("description: %s" % desc):
        parts, grab = [], False
        for ln in fm.splitlines():
            if FOLD_RE.match(ln):
                grab = True
                continue
            if grab:
                if ln.startswith((" ", "\t")) and ln.strip():
                    parts.append(ln.strip())
                elif ln.strip():
                    break
        desc = re.sub(r"\s+", " ", " ".join(parts)).strip()
    return name, desc, text[m.end():]


def canonical(raw, fm_name):
    """Frontmatter name kalau ada; kalau tidak, sanitasi nama folder hasil flatten.
    `--` juga dinormalkan supaya varian dari repo berbeda bisa ter-collapse."""
    n = (fm_name or "").strip()
    if not n:
        n = raw
    n = re.sub(r"^-+", "", n)
    n = n.replace("---", "-").replace("--", "-")
    n = re.sub(r"-skill$", "", n) if not fm_name else n
    n = re.sub(r"[-_]{2,}", "-", n).strip("- ")
    return n.lower() or raw


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def build_role_lookup():
    data = load_json(ROLE_FILE)
    lut = {}
    for role, val in (data.get("roles") or {}).items():
        for s in (val.get("skills") or []):
            lut.setdefault(s, role)
    for s in ((data.get("uncategorized") or {}).get("skills") or []):
        lut.setdefault(s, "uncategorized")
    return lut


def build_source_lookup():
    """Provenance berlapis: .skill-lock.json → skills-repo-map.json → heuristik
    prefix nama dir (gh-<owner>-<repo>, mined-<owner>-<repo>, repo-map owner_repo)."""
    lut = {}
    data = load_json(LOCK_FILE)
    for name, meta in (data.get("skills") or {}).items():
        if isinstance(meta, dict):
            src = meta.get("source") or meta.get("sourceUrl") or ""
            if src:
                lut[name] = src
    # skills-repo-map.json: map raw-dir → "owner_repo"
    repomap = load_json(AGENTS / "skills-repo-map.json")
    for raw, owner_repo in ((repomap.get("map") or {}).items()):
        if isinstance(owner_repo, str) and "_" in owner_repo:
            owner, repo = owner_repo.split("_", 1)
            lut.setdefault(raw, f"https://github.com/{owner}/{repo}")
    return lut


GH_RE = re.compile(r"^(?:gh|mined)-(.+)$")


def _split_owner_repo(rest):
    """Pisahkan 'owner-repo' jadi (owner, repo) dengan verifikasi bukti.

    Coba tiap posisi pisah dari KIRI (owner pendek dulu: 'nexu-io' sebelum
    'nexu'), kembalikan pasangan pertama yang TERBUKTI ADA. Tanpa bukti -> ('','').
    """
    parts = (rest or "").split("-")
    for i in range(1, len(parts)):
        owner, repo = "-".join(parts[:i]), "-".join(parts[i:])
        if owner and repo and _find_proven(owner, repo):
            hit = _find_proven(owner, repo)
            return hit[1], hit[2]
    return "", ""


def gh_source(dirname):
    """gh-<owner>-<repo> / mined-<owner>-<repo> → URL GitHub (hanya bila terbukti ada)."""
    m = GH_RE.match(dirname or "")
    if not m:
        return ""
    owner, repo = _split_owner_repo(m.group(1))
    if owner:
        return f"https://github.com/{owner}/{repo}"
    return ""

# Pola nama-dir hasil scrape komunitas: token sumber di tengah/akhir nama
# (mis. ---roo-skills-claude-api-... -> sumber roo/skills, claude-api, ...)
# Urutan = prioritas; first match wins. Hanya repo yang TERBUKTI ADA di
# repo-refs/ atau registry yang dipakai (lihat _PROVEN_SOURCES).
SCRAPE_SRC_PATTERNS = (
    (re.compile(r"github-copilot[_-]?skills?", re.I), None),  # owner bervariasi -> heuristik gh_
    (re.compile(r"obra[_-]?superpowers", re.I), ("obra", "superpowers")),
    (re.compile(r"anthropics[_-]?skills", re.I), ("anthropics", "skills")),
    (re.compile(r"awesome[_-]?copilot", re.I), ("github", "awesome-copilot")),
    (re.compile(r"composio", re.I), ("ComposioHQ", "awesome-claude-skills")),
    (re.compile(r"claude[_-]?code", re.I), ("hesreallyhim", "awesome-claude-code")),
)


def _norm_repo_key(s):
    """Normalisasi owner/repo: buang '-' dan '_', lowercase."""
    return re.sub(r"[-_]+", "", (s or "").lower())


def _build_proven_index():
    """Bangun indeks lookup O(1) dari repo-refs/ + repo-registry.json.

    Hasil IDENTIK dengan versi linear lama, tapi dibangun SEKALI (~14k entri)
    alih-alih memindai 14k entri per panggilan. Ini memperbaiki hot loop:
    _split_owner_repo() memanggil _find_proven() 2x per posisi split, untuk
    puluhan ribu skill -> sebelumnya ~1,7 miliar perbandingan string.

    Bentuk: {norm_key: (sumber, owner_asli, repo_asli)} dengan norm_key =
    norm(owner)+"/"+norm(repo). Ditambah varian singular (tanpa 's' di ujung)
    hanya bila belum ada, supaya perilaku `have.rstrip("s") == want_sing` tetap.
    """
    idx = {}

    def put(key, entry):
        if key and key not in idx:
            idx[key] = entry

    # repo-refs/ : prioritas utama (sumber lokal), ditimpa tidak boleh.
    try:
        listing = os.listdir(AGENTS / "repo-refs")
    except Exception:
        listing = []
    for d in listing:
        if "_" in d:
            o, r = d.split("_", 1)
            key = _norm_repo_key(o) + "/" + _norm_repo_key(r)
        else:
            o, r = d, ""
            key = _norm_repo_key(d) + "/"
        put(key, ("repo-refs", o, r))
        # varian singular (mis. owner/repos -> owner/repo) TIDAK boleh
        # menimpa entri asli; hanya diisi bila key belum ada.
        if key.endswith("s") and not key.endswith("ss"):
            put(key[:-1], ("repo-refs", o, r))

    # repo-registry.json : pelengkap, hanya bila belum ada di repo-refs.
    try:
        reg = load_json(AGENTS / "repo-registry.json").get("repos") or {}
    except Exception:
        reg = {}
    if isinstance(reg, dict):
        for k in reg:
            if "/" not in k:
                continue
            o, r = k.split("/", 1)
            key = _norm_repo_key(o) + "/" + _norm_repo_key(r)
            put(key, ("registry", o, r))
            if key.endswith("s") and not key.endswith("ss"):
                put(key[:-1], ("registry", o, r))
    return idx


def _find_proven(owner, repo):
    """Cari repo yang TERBUKTI ADA, kembalikan (sumber, owner_asli, repo_asli).

    Sumber = 'repo-refs' (dir lokal) atau 'registry' (repo-registry.json).
    Owner/repo ASLI dipakai supaya URL canonical benar
    (mis. 'Obra' bukan 'obra', 'ComposioHQ' bukan 'composiohq').
    Return None bila tidak ada bukti — pemanggil JANGAN mengarang URL.
    """
    # Cache: indeks dibangun SEKALI (lihat _build_proven_index), lalu O(1).
    global _PROVEN_IDX
    if "_PROVEN_IDX" not in globals() or _PROVEN_IDX is None:
        _PROVEN_IDX = _build_proven_index()
    want = _norm_repo_key(owner) + "/" + _norm_repo_key(repo)
    hit = _PROVEN_IDX.get(want)
    if hit is not None:
        return hit
    # fallback singular: 'owner/repos' pada query -> coba 'owner/repo'
    if want.endswith("s") and not want.endswith("ss"):
        hit = _PROVEN_IDX.get(want[:-1])
        if hit is not None:
            return hit
    return None


def _repo_ref_exists(owner, repo):
    """Cek repo terbukti ada: dir repo-refs/ lokal ATAU registry komunitas."""
    return _find_proven(owner, repo) is not None


def proven_source(owner, repo):
    """URL GitHub canonical dari repo yang TERBUKTI ADA (pakai owner/repo asli
    dari repo-refs/registry, bukan ejaan mentah dari nama dir)."""
    hit = _find_proven(owner, repo)
    if hit:
        return f"https://github.com/{hit[1]}/{hit[2]}"
    return ""


def gh_source_legacy(dirname):
    """Versi lama (regex kaku) — disimpan sbg fallback, jangan dipakai langsung."""
    m = GH_RE.match(dirname or "")
    if m and _repo_ref_exists(m.group(1), m.group(2)):
        return f"https://github.com/{m.group(1)}/{m.group(2)}"
    return ""


def scrape_source(dirname):
    """Nama-dir scrape komunitas → sumber yang TERBUKTI ADA (repo-refs/registry).

    Return '' bila tidak ada bukti — jangan mengarang URL.
    """
    low = (dirname or "").lower()
    for pat, fixed in SCRAPE_SRC_PATTERNS:
        if not pat.search(low):
            continue
        if fixed:
            owner, repo = fixed
            return proven_source(owner, repo)
            continue
        # pola tanpa owner tetap: mis. github-copilot-skills-<owner>-<repo>-skill
        m = re.search(r"github[-_]?copilot[-_]?skills?[-_]([a-z0-9_.]+)-(.+?)(?:-skill)?$",
                      dirname or "", re.I)
        if m:
            return proven_source(m.group(1), m.group(2))
    return ""


_FALLBACK_ROLES = None


def _load_role_keywords():
    """Ambil dict role {role: {keywords: [...]}} dari _categorize_roles.py tanpa
    menghardcode ulang daftar keyword (sumber tunggal tetap file itu)."""
    try:
        import importlib.util as _iu
        spec = _iu.spec_from_file_location("_cr", AGENTS / "_categorize_roles.py")
        mod = _iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for attr in vars(mod).values():
            if (isinstance(attr, dict) and attr and
                    all(isinstance(v, dict) and "keywords" in v
                        for v in list(attr.values())[:3])):
                return list(attr.items())
    except Exception:
        pass
    return []


def role_fallback_text(text):
    """Kategori dari nama+deskripsi (fallback kalau role-skill-map tidak mencakup).
    Priority order = urutan dict _categorize_roles (first match wins),
    TAPI 'productivity-automator' selalu dicek duluan untuk token gws-*/google-*
    yang sangat spesifik (mencegah 'chat'/'send' nyasar ke role generik)."""
    global _FALLBACK_ROLES
    if _FALLBACK_ROLES is None:
        _FALLBACK_ROLES = [(r, tuple(k.lower() for k in (s.get("keywords") or []) if k),
                            (s.get("maps_to") or r))
                           for r, s in _load_role_keywords()]
    low = (text or "").lower()
    if not low:
        return ""
    prio = [p for p in _FALLBACK_ROLES if p[0] == "productivity-automator"] + \
           [p for p in _FALLBACK_ROLES if p[0] != "productivity-automator"]
    # Nama skill sangat prediktif: equality dulu (nama persis) sebelum substring.
    # Mencegah 'lark-attendance' kalah oleh keyword generik ('audit'/'scan' di
    # deskripsi Cina) — nama yang mengandung token spesifik role menang.
    for role, kws, maps in prio:
        if role == "productivity-automator":
            if re.search(r"\bgws[\w-]*|google[-_ ]?(workspace|drive|sheets|docs|slides|forms|calendar|meet|keep|tasks|mail)|gmail\b|lark|feishu", low):
                return role
            continue
        for k in kws:
            if k in low:
                # OVERRIDE: _override-* pindah ke kamar asli (maps_to)
                if isinstance(maps, dict):
                    return maps.get(k, role)
                return maps
    return ""


def main():
    import fcntl
    lock_fh = open(AGENTS / ".index-build.lock", "w")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("build lain sedang jalan — skip (lock: .index-build.lock)")
        return
    role_lut = build_role_lookup()
    src_lut = build_source_lookup()
    entries = {}
    junk = []
    stats = {"dup": 0, "rescued": 0, "junk": 0}

    def add(raw_dir, default_tier, parent=""):
        skill_md = raw_dir / "SKILL.md"
        if not skill_md.is_file():
            return
        fm_name, desc, body = parse_frontmatter(read_head(skill_md))
        title = first_h1(body)
        # Nama kanonik: frontmatter > slug H1 (entri scraping) > nama folder
        alt = slug(title) if (default_tier != "curated" and title) else ""
        name = canonical(raw_dir.name, fm_name or alt)
        if name in entries:
            stats["dup"] += 1
            return
        if not desc:
            desc = first_paragraph(body, title) or first_heading(body)
        if default_tier == "curated":
            tier = "curated"
        elif desc and looks_like_skill(body, title):
            tier = "reference"                      # di-RESCUE: isinya nyata, layak dipakai
            stats["rescued"] += 1
        else:
            tier = "junk"                           # sampah asli (API doc/HTML/license/terlalu pendek)
            stats["junk"] += 1
            junk.append(name)
        # Kategori: role-skill-map → fallback keyword (nama+deskripsi).
        # 'uncategorized' eksplisit di map TIDAK final — beri kesempatan fallback.
        # Nama 1 huruf (artefak scrape) TIDAK diberi kategori tebakan — biar
        # tetap uncategorized & gampang diidentifikasi, bukan salah kamar.
        cat = (role_lut.get(raw_dir.name) or role_lut.get(name) or "")
        if cat in ("", "uncategorized") and not re.match(r"^[a-z]$", name or ""):
            cat = role_fallback_text(f"{name} {desc}") or cat
        # Provenance: lock → repo-map → heuristik prefix (incl. parent mined-*)
        src = (src_lut.get(raw_dir.name) or src_lut.get(name)
               or gh_source(raw_dir.name) or gh_source(parent)
               or scrape_source(raw_dir.name) or scrape_source(parent))
        entries[name] = (
            desc,
            tier,
            cat,
            str(skill_md),
            src,
        )

    for d in sorted(CURATED_DIR.iterdir()):
        if d.is_dir():
            add(d, "curated")
    curated_count = len(entries)
    for d in sorted(REF_DIR.iterdir()):
        if not d.is_dir():
            continue
        if (d / "SKILL.md").exists():
            add(d, "reference")
        else:
            # nested (mis. skills-expanded/mined-<repo>/<nama>/SKILL.md)
            # + nested-2 (mis. skills-expanded/mined-<repo>/<grup>/<nama>/SKILL.md,
            # hasil tarball awesome-list seperti mined-ComposioHQ-awesome-claude-skills)
            for sub in sorted(d.iterdir()):
                if not sub.is_dir():
                    continue
                if (sub / "SKILL.md").exists():
                    add(sub, "reference", parent=d.name)
                else:
                    for sub2 in sorted(sub.iterdir()):
                        if sub2.is_dir() and (sub2 / "SKILL.md").exists():
                            add(sub2, "reference", parent=d.name)

    # --- aset agent lintas tool: AGENTS.md, .cursor/rules/*.mdc, prompt, copilot ---
    assets_dir = AGENTS / "agent-assets"
    asset_count = 0
    if assets_dir.exists():
        for f in sorted(list(assets_dir.rglob("*.md")) + list(assets_dir.rglob("*.mdc"))):
            try:
                head = read_head(f)
            except Exception:
                continue
            fm_name, desc, body = parse_frontmatter(head)
            title = first_h1(body)
            name = canonical(f.stem, fm_name or (slug(title) if title else ""))
            if not name or name in entries:
                stats["dup"] += 1
                continue
            if not desc:
                desc = first_paragraph(body, title) or first_heading(body)
            if not desc or len(desc) < 20:
                continue
            cat = role_fallback_text(f"{name} {desc}") or "agent-asset"
            src = (gh_source(f.parent.name) or gh_source(f.parent.parent.name)
                   or scrape_source(f.parent.name) or "")
            entries[name] = (desc, "reference", cat, str(f), src)
            asset_count += 1

    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE VIRTUAL TABLE skills USING fts5(name, description, tier, category, path, source)")
    conn.executemany(
        "INSERT INTO skills (name, description, tier, category, path, source) VALUES (?,?,?,?,?,?)",
        [(n, d, t, c, p, s) for n, (d, t, c, p, s) in entries.items()],
    )
    conn.commit()
    conn.close()

    JUNK_FILE.write_text("\n".join(sorted(junk)) + "\n", encoding="utf-8")
    by_tier = {}
    for (_d, t, _c, _p, _s) in entries.values():
        by_tier[t] = by_tier.get(t, 0) + 1
    print(f"curated={curated_count} total={len(entries)} dup_skipped={stats['dup']} rescued={stats['rescued']}")
    for t in ("curated", "reference", "junk"):
        print(f"  {t}: {by_tier.get(t, 0)}")
    print(f"Siap dipakai (curated+reference): {by_tier.get('curated',0) + by_tier.get('reference',0)}")
    print(f"junk list : {JUNK_FILE} ({len(junk)} entri)")
    print(f"DB        : {DB_PATH} ({DB_PATH.stat().st_size/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
