#!/usr/bin/env python3
"""skill-flow.py — mesin alur kerja + kategori skill (sumber: skill-flow.json).

  (stdin JSON {"prompt":...})  → teks hook UserPromptSubmit (Claude Code)
  --render                      → tulis ~/.agents/SKILL-FLOW.md (dibaca semua AI)
  --check                       → daftar skill di JSON yang tidak ada di skills-store
  --link                        → symlink semua skill flow ke tiap AI + ~/.agents/skills (Cline)
  --test "teks"                 → uji hasil routing tanpa stdin
  --stats                       → besar injeksi yang sudah dikeluarkan sesi ini

Hemat konteks (audit 2026-09-26): routing/skor TIDAK diubah (kualitas tetap),
tapi injeksi jadi (a) idempoten per sesi — kategori+skill sama tidak diulang,
dan (b) berbatas SKILL_FLOW_MAX_BYTES byte. Dulu tiap prompt ikut mendorong
pembacaan SKILL-FLOW.md (5,3 KB/sesi); sekarang diganti 1 baris muat-ringkas.
"""
import json, os, re, sys, subprocess, time

H = os.path.expanduser("~")
A = H + "/.agents"
STORE = A + "/skills-store"
CFG = json.load(open(A + "/skill-flow.json"))


def match(prompt):
    p = " " + re.sub(r"[^\w\s.#+-]", " ", prompt.lower()) + " "
    hits = []
    for name, c in CFG["categories"].items():
        for k in c["kw"]:
            k = k.lower()
            ok = re.search(r"(?<![\w])" + re.escape(k) + r"(?![\w])", p) if len(k) <= 4 else k in p
            if ok:
                hits.append(name)
                break
    return hits


PRIORITY = ["debug", "keamanan", "test", "performa", "review", "refactor", "database", "backend-api",
            "frontend", "react-next", "vue", "mobile", "devops", "riset", "data", "tulisan", "sosmed", "email",
            "marketing", "dokumentasi", "file-office", "gambar-video", "rencana", "kode"]


def route(prompt):
    cats = match(prompt)
    cats.sort(key=lambda c: PRIORITY.index(c) if c in PRIORITY else len(PRIORITY))
    skills = list(CFG["always"])
    cap = CFG.get("max_skills", 7) + len(CFG["always"])
    depth = max((len(CFG["categories"][c]["skills"]) for c in cats), default=0)
    for i in range(depth):                      # round-robin: skill ke-i tiap kategori
        for c in cats:
            lst = CFG["categories"][c]["skills"]
            if i < len(lst) and lst[i] not in skills and len(skills) < cap:
                skills.append(lst[i])
    return cats, skills


def task_candidates(prompt):
    try:
        out = subprocess.run(["python3", A + "/skill-rank.py", prompt], capture_output=True, text=True, timeout=3)
        return [x for x in out.stdout.strip().split(",") if x]
    except Exception:
        return []


MAX_BYTES = int(os.environ.get("SKILL_FLOW_MAX_BYTES", "400"))
STATE_DIR = os.environ.get("SKILL_FLOW_STATE_DIR", "/tmp/voralens-skill-flow")


def _state_path(sid):
    safe = "".join(c for c in (sid or "default") if c.isalnum() or c in "-_")[:64]
    return os.path.join(STATE_DIR, safe or "default") + ".json"


def _load_state(sid):
    """Baca state sesi. Ada TTL supaya tool yang tidak mengirim session_id
    (Codex/Gemini/Cursor: key jatuh ke 'default') tidak saling menekan injeksi
    di sesi berbeda — setelah kedaluwarsa, skill diumumkan ulang (kualitas aman)."""
    p = _state_path(sid)
    try:
        ttl = int(os.environ.get("SKILL_FLOW_STATE_TTL", "21600"))  # 6 jam
        if ttl > 0 and (time.time() - os.path.getmtime(p)) > ttl:
            return {}
        with open(p) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(sid, d):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        p = _state_path(sid)
        tmp = p + ".tmp%d" % os.getpid()
        with open(tmp, "w") as f:
            json.dump(d, f)
        os.replace(tmp, p)
    except Exception:
        pass  # state gagal ditulis: hook tetap jalan, cuma tidak hemat antar-prompt


def _format(cats, skills, extra):
    """Susun 1 baris pendek. Daftar skill wajib dilindungi; kandidat dipotong dulu."""
    must = ", ".join(skills)
    base = "Skill wajib: %s. Muat ringkas: bash ~/.agents/skill-load-lite.sh <nama>." % must
    if len(base) > MAX_BYTES:
        # masih kelebihan: buang skill opsional paling akhir, selalu simpan CFG["always"]
        keep = list(CFG["always"])
        for s in skills:
            if s in keep:
                continue
            cand = keep + [s]
            if len("Skill wajib: %s." % ", ".join(cand)) <= MAX_BYTES:
                keep.append(s)
        base = "Skill wajib: %s. Muat ringkas: skill-load-lite.sh <nama>." % ", ".join(keep)
    if extra:
        tail = " Kandidat: %s." % ", ".join(extra)
        if len(base) + len(tail) <= MAX_BYTES:
            base += tail
    return base


def hook(prompt, session_id="default"):
    prompt = (prompt or "")[:300]
    if len(prompt.split()) < 3:
        sig = "short"
        if _load_state(session_id).get("sig") == sig:
            return ""                                  # diulang: 0 token
        txt = "Gaya: caveman-token-optimizer (ringkas)."
        _save_state(session_id, {"sig": sig, "skills": [], "extra": [], "bytes": len(txt)})
        return txt
    cats, skills = route(prompt)
    extra = [s for s in task_candidates(prompt) if s not in skills][:2]
    # Signature SENGAJA hanya cats+skills: kandidat berubah tiap prompt dan tidak
    # boleh memaksa injeksi ulang (itu penyebab pemborosan sebelum 2026-09-26).
    sig = "|".join(cats) + "::" + ",".join(skills)
    st = _load_state(session_id)
    if st.get("sig") == sig:
        baru = [s for s in extra if s not in (st.get("extra") or [])]
        if not baru:
            return ""            # kategori & skill sama, kandidat sama → 0 token
        tail = "Kandidat baru: %s." % ", ".join(baru)   # ±40 B, bukan baris penuh
        st["extra"] = (st.get("extra") or []) + baru
        st["bytes"] = int(st.get("bytes", 0)) + len(tail)
        _save_state(session_id, st)
        return tail
    txt = _format(cats, skills, extra)
    _save_state(session_id, {"sig": sig, "skills": skills, "cats": cats,
                             "extra": extra, "bytes": len(txt)})
    return txt


def stats():
    if not os.path.isdir(STATE_DIR):
        print("belum ada injeksi tercatat (%s kosong)" % STATE_DIR)
        return
    n = tot = 0
    for fn in sorted(os.listdir(STATE_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(STATE_DIR, fn)))
        except Exception:
            continue
        n += 1
        tot += int(d.get("bytes", 0))
        print("  %-40s %4d B  %s" % (fn[:40], int(d.get("bytes", 0)), ", ".join(d.get("cats", []))))
    print("sesi tercatat: %d | byte state terakhir/sesi: %d B | batas %d B/prompt"
          % (n, tot, MAX_BYTES))
    print("(angka = injeksi terakhir per sesi, BUKAN akumulasi seluruh sesi)")



def render():
    L = ["# SKILL FLOW — alur kerja WAJIB semua AI", "",
         "> Dibuat otomatis dari `~/.agents/skill-flow.json` (edit di sana, lalu `python3 ~/.agents/skill-flow.py --render`).", "",
         "## Selalu", "", "- " + ", ".join("`%s`" % s for s in CFG["always"]), "",
         "## Alur (urut, jangan dilompati)", ""]
    L += [f for f in CFG["flow"]]
    L += ["", "## Kategori → skill", "", "| Kategori | Pemicu (contoh) | Skill |", "|---|---|---|"]
    for n, c in CFG["categories"].items():
        L.append("| %s | %s | %s |" % (n, ", ".join(c["kw"][:6]), ", ".join("`%s`" % s for s in c["skills"])))
    L += ["", "## Cara memuat skill", "",
          "- MCP `skill-catalog`: `skill_for_task(\"<tugas>\")` → `skill_load(\"<nama>\")`.",
          "- Tanpa MCP: `~/.agents/skill-search.sh \"<kata kunci>\"` lalu baca `~/.agents/skills-store/<nama>/SKILL.md`.",
          "- Muat hanya skill yang cocok (maks ±7). Tugas campuran → gabungkan kategori.", "",
          "## Sumber", "", "- `~/.agents/skill-flow.json`", "- `~/.agents/skills-store/<nama>/SKILL.md`", ""]
    open(A + "/SKILL-FLOW.md", "w").write("\n".join(L))
    print("ditulis: ~/.agents/SKILL-FLOW.md")


def all_skills():
    s = set(CFG["always"])
    for c in CFG["categories"].values():
        s |= set(c["skills"])
    return sorted(s)


def check():
    miss = [s for s in all_skills() if not os.path.isdir(STORE + "/" + s)]
    print("total skill flow:", len(all_skills()), "| hilang:", miss or "tidak ada")
    return miss


def link():
    tools = [A + "/skills"] + [f"{H}/{d}/skills" for d in os.listdir(H)
             if d.startswith(".") and d != ".agents" and os.path.isdir(f"{H}/{d}/skills") and not os.path.islink(f"{H}/{d}/skills")]
    n = 0
    for t in tools:
        for s in all_skills():
            if os.path.isdir(STORE + "/" + s) and not os.path.lexists(f"{t}/{s}"):
                os.symlink(f"{STORE}/{s}", f"{t}/{s}")
                n += 1
    core_f = A + "/skill-core.json"
    d = json.load(open(core_f))
    d["core"] = sorted(set(d["core"]) | set(all_skills()))
    json.dump(d, open(core_f, "w"), indent=1)
    print("symlink baru:", n, "| tool:", len(tools), "| Cline (~/.agents/skills):", len(os.listdir(A + "/skills")))


def evaluate():
    tests = json.load(open(A + "/skill-flow-tests.json"))
    fail = 0
    for t in tests:
        cats, skills = route(t["p"])
        miss_c = [c for c in t["cats"] if c not in cats]
        miss_s = [x for x in t["skills"] if x not in skills]
        extra = [] if t["cats"] else cats          # prompt umum tidak boleh kena kategori
        if miss_c or miss_s or extra:
            fail += 1
            print("GAGAL:", t["p"], "| dapat:", cats, "| kurang kategori:", miss_c, "| kurang skill:", miss_s, "| salah:", extra)
    print("hasil: %d/%d lulus" % (len(tests) - fail, len(tests)))
    return fail


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--render"]:
        render()
    elif a[:1] == ["--check"]:
        check()
    elif a[:1] == ["--eval"]:
        sys.exit(1 if evaluate() else 0)
    elif a[:1] == ["--link"]:
        link()
    elif a[:1] == ["--stats"]:
        stats()
    elif a[:1] == ["--test"]:
        # sesi sekali-pakai supaya dedupe tidak menyembunyikan hasil routing
        print(hook(" ".join(a[1:]), "cli-test-%d" % os.getpid()))
    else:
        try:
            payload = json.load(sys.stdin)
            sid = payload.get("session_id") or payload.get("transcript_path") or "default"
            out = hook(payload.get("prompt", ""), str(sid))
            if out:                       # kosong = sudah diumumkan sesi ini → 0 token
                print(out)
        except Exception:
            pass

