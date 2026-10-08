#!/usr/bin/env python3
"""loop-guard.py — penghitung & pemberi sinyal loop agentic PER SESI (SEMUA tool AI).

Masalah nyata yang ditemukan audit 2026-10-03: limit habis bukan karena pesan
panjang, tapi karena LOOP — 1.223 pesan dalam 1 hari (02 Okt), ~500 jt token
(10× di atas rata-rata harian). Pola loop: spawn agent → baca → edit → gagal →
validasi → ulangi. Satu loop tak berujung = ratusan pesan/ratusan juta token.

Cara kerja: hook ini dipanggil di SETIAP tool call (PreToolUse di Claude Code,
dan disambungkan ke UserPromptSubmit Cline). Ia menghitung tool call per sesi
di file state kecil (/tmp, SEDIKIT sekali, bukan token), dan:
  - < 80 tool call/sesi   : 0 byte (sunyi)
  - 80–200/sesi            : 1 baris ("sesi ini sudah N tool call — pertimbangkan STOP/rangkum")
  - > 200/sesi ATAU pesan >500     : peringatan KERAS ("kemungkinan loop; hentikan agen, tulis
                       status ke file, lanjut sesi BARU membaca file status itu")

Biaya: 0 token saat normal. State dihapus otomatis (>24 jam).

Env: LOOP_WARN_N (80), LOOP_HARD_N (200), LOOP_MSG_N (500).
Hook Claude: stdin JSON berisi session_id + tool_name (+ transcript_path opsional).
Hook Cline : stdin JSON sembarang (state pakai sesi aktif yang terdeteksi dari disk).
"""
import glob
import json
import os
import sys
import time

HOME = os.path.expanduser("~")
STATE = os.path.join(HOME, ".agents", ".loop-guard.json")
CLAUDE_SESS = os.path.join(HOME, ".claude", "projects", "*", "*.jsonl")
CLINE_SESS = os.path.join(HOME, ".cline", "data", "sessions", "*", "*.messages.json")

WARN_N = int(os.environ.get("LOOP_WARN_N", "80"))
HARD_N = int(os.environ.get("LOOP_HARD_N", "200"))
MSG_N = int(os.environ.get("LOOP_MSG_N", "500"))


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}


def save_state(st):
    try:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        tmp = STATE + ".tmp"
        json.dump(st, open(tmp, "w"))
        os.replace(tmp, STATE)
    except Exception:
        pass


def newest_live_session():
    """Deteksi sesi yang sedang aktif: transcript yang ditulis <10 menit terakhir."""
    now = time.time()
    best, best_t = None, 0
    for pat in (CLAUDE_SESS, CLINE_SESS):
        for p in glob.glob(pat):
            try:
                mt = os.path.getmtime(p)
            except OSError:
                continue
            if now - mt < 600 and mt > best_t:
                best, best_t = p, mt
    return best


def transcript_msgs(path):
    """Hitung jumlah pesan riwayat (murah: tanpa parse dalam)."""
    if not path or not os.path.isfile(path):
        return 0
    try:
        if path.endswith(".jsonl"):
            # user/assistant = 2 baris per turn + system
            n = 0
            with open(path, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if '"role"' in line or '"type":"user"' in line or '"type":"assistant"' in line:
                        n += 1
            return n
        if path.endswith(".messages.json"):
            with open(path, encoding="utf-8", errors="ignore") as f:
                head = f.read(4000)
            return head.count('"role"') or 1
    except Exception:
        pass
    return 0


def _live_key():
    """Kunci fallback = transcript aktif (<10 menit). Bedakan sesi Cline yang
    payload hook-nya tanpa session_id; None kalau tidak ada sesi live."""
    live = newest_live_session()
    if not live:
        return None
    base = os.path.basename(live)
    for suffix in (".messages.json", ".jsonl"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    return "live:" + base[:40]


def check(payload):
    """Inti logika — bisa dipanggil hook wrapper lain (Cline) dengan dict payload.
    Mengembalikan teks peringatan ('' kalau sunyi)."""
    if not isinstance(payload, dict):
        payload = {}
    sid = str(payload.get("session_id") or payload.get("sessionId") or "")
    if not sid or sid == "live":
        sid = _live_key() or "live"
    st = load_state()
    now = time.time()
    # reset harian + buang sesi tak aktif >24 jam
    for k in [k for k in st if now - st[k].get("t", 0) > 86400]:
        del st[k]
    e = st.get(sid) or {"n": 0, "t": now, "warned": 0}
    e["n"] += 1
    e["t"] = now
    st[sid] = e
    save_state(st)

    n = e["n"]
    if n < WARN_N:
        return ""
    live = newest_live_session()
    msgs = transcript_msgs(live) if live else 0
    if n >= HARD_N or msgs >= MSG_N:
        return ("[loop-guard] KEMUNGKINAN LOOP: sesi ini sudah %d tool call%s. "
                "HENTIKAN agen/spawn sekarang: tulis STATUS + LANGKAH SELANJUTNYA ke file, "
                "tutup sesi, lanjut di sesi BARU yang membaca file itu. Jangan biarkan "
                "agen berjalan tanpa batas — tiap putaran membakar jutaan token."
                % (n, " (riwayat %d pesan)" % msgs if msgs else ""))
    step = n // WARN_N
    if e.get("warned", 0) < step:
        e["warned"] = step
        save_state(st)
        return ("[loop-guard] Sesi ini sudah %d tool call%s — kalau tugas selesai, STOP dan "
                "rangkum. Kalau macet di masalah yang sama, hentikan dan pecah tugasnya, "
                "jangan biarkan agen mengulang." % (n, " (%d pesan)" % msgs if msgs else ""))
    return ""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    out = check(payload)
    if out:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
