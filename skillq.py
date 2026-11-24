#!/usr/bin/env python3
"""skillq — cari skill di katalog lokal, output padat (0 tool MCP).
Pakai: skillq.py "kata kunci" [-n 5]   |   skillq.py -l <nama>   (cetak SKILL.md)
       skillq.py --repo "kata" [-n 8]  (cari REPO di ~/.agents/repos.db)
"""
import sqlite3, sys, os, re

DB = os.path.expanduser("~/.agents/skills-index.db")
REPO_DB = os.path.expanduser("~/.agents/repos.db")
READY_JSON = os.path.expanduser("~/.agents/skills-readiness.json")


def _ready_map():
    try:
        import json as _j
        return _j.load(open(READY_JSON))
    except Exception:
        return {}


def _badge(info):
    if not info:
        return ""
    if info.get("ready"):
        return " [siap]"
    miss = ",".join(info.get("missing") or [])[:24]
    return f" [butuh:{miss}]" if miss else ""
STOP = set("yang dan dengan untuk dari pada ini itu saya mau bikin buat tolong bisa gimana cara agar supaya the and for with using use add create make new how please want need into that this from a an of to in on".split())

# Token 2 huruf ambigu ("pt", "cv", "rt", "rw"): tidak masuk FTS dan tidak
# dapat bonus nama — sinonim & cakupan probe tetap jalan.
AMBIG2 = {"pt", "cv", "rt", "rw"}

# Istilah Indonesia -> istilah yang benar-benar dipakai di deskripsi skill (Inggris).
# Tanpa ini, "desain dashboard profesional" jatuh ke skill Spanyol hasil auto-forge.
SYN = {
    "desain": "design", "mendesain": "design", "tampilan": "ui interface", "antarmuka": "ui interface",
    "dasbor": "dashboard", "halaman": "page landing", "layar": "screen page", "tombol": "button",
    "warna": "color palette", "huruf": "typography font", "tipografi": "typography", "tata": "layout grid",
    "letak": "layout grid", "animasi": "animation motion", "gerak": "motion animation",
    "aksesibel": "accessibility", "aksesibilitas": "accessibility", "responsif": "responsive",
    "formulir": "form", "kartu": "card", "tabel": "table", "ikon": "icon", "komponen": "component",
    "profesional": "polished professional", "bagus": "better polished", "jelek": "generic ai slop",
    "generik": "generic ai slop", "pasaran": "generic ai slop", "gelap": "dark theme",
    "terang": "light theme", "konsisten": "design system consistency", "rapi": "polished clean",
    "murah": "cheap", "modern": "modern contemporary", "landing": "landing page",
    # --- tugas umum (ID -> EN) supaya skill berbahasa Inggris tetap ketemu ---
    "presentasi": "presentation powerpoint", "paparan": "presentation powerpoint",
    "slide": "slide powerpoint presentation", "dek": "deck presentation",
    "kirim": "send", "surat": "email", "email": "email smtp",
    "gambar": "image", "foto": "image", "ubah": "edit convert",
    "transkrip": "transcribe transcription", "audio": "audio whisper speech",
    "video": "video", "laporan": "report", "dokumen": "document", "berkas": "file",
    "uji": "test testing", "tes": "test testing", "pengujian": "test testing",
    "perbaiki": "fix", "benerin": "fix", "rapikan": "refactor clean",
    "cari": "search find", "pindai": "scan", "keamanan": "security",
    "backup": "backup restore", "cadangkan": "backup", "pulihkan": "restore",
    "pasang": "install setup", "instal": "install setup", "unggah": "upload",
    "unduh": "download", "otomatis": "automation automate", "otomasi": "automation",
    "jadwal": "schedule calendar", "harga": "price pricing", "jual": "sales ecommerce",
    "percepat": "performance optimize", "lambat": "performance slow optimize",
    "galat": "error debug", "kesalahan": "error debug", "situs": "website site",
    "basis": "database", "data": "data dataset", "grafik": "chart graph",
    "ringkasan": "summary summarize", "terjemah": "translate translation",
    "suara": "voice speech audio", "teks": "text ocr", "gambar": "image",
    "baca": "read parse", "tulis": "write create", "hapus": "delete remove",
    "ganti": "replace", "ambil": "fetch get", "simpan": "save store",
    "gabung": "merge combine", "pisah": "split", "kompres": "compress",
    "cetak": "print", "hitung": "calculate compute", "bandingkan": "compare diff",
    # Istilah campuran Indonesia/Inggris & istilah tech yang sering dipakai apa adanya.
    "foto": "photo image picture", "musik": "music audio song", "lagu": "music audio song",
    "video": "video", "dokumen": "document pdf docx file", "laporan": "report",
    "rencana": "plan", "arsitektur": "architecture", "jaringan": "network",
    "aplikasi": "app application", "program": "app application",
    "toko": "store shop ecommerce", "belanja": "shopping ecommerce", "pesan": "chat message",
    "chat": "chat message", "otomatisasi": "automation", "keuangan": "finance accounting",
    "gaji": "payroll salary", "karyawan": "employee hr", "wawancara": "interview",
    "belajar": "course learn tutorial", "kursus": "course learn tutorial",
    "olahraga": "fitness sport", "kesehatan": "health medical", "resep": "recipe cooking",
    "perjalanan": "travel", "sandi": "password credential secret", "rahasia": "secret credential",
    "infografis": "infographic", "saham": "stock trading market", "forex": "forex trading",
    "kripto": "crypto cryptocurrency", "presentasi": "presentation powerpoint slides slide",
    "slideshow": "presentation slides", "subtitle": "subtitle caption", "captions": "subtitle caption",
    "enkripsi": "encrypt encryption crypto", "forensik": "forensic", "malware": "malware virus",
    "celah": "vulnerability exploit", "bug": "bug error debug", "error": "error debug",
    "crash": "crash error debug", "lemot": "performance slow optimize", "panas": "overheat thermal",
    "cadangan": "backup", "arsip": "archive backup", "kirim": "send email message",
    "terima": "receive email",
    "fine-tune": "finetune fine-tuning lora qlora train", "finetune": "finetune fine-tuning lora qlora",
    "fine-tuning": "finetune fine-tuning lora qlora", "ci/cd": "ci cd pipeline github-actions deploy",
    "cicd": "ci cd pipeline github-actions deploy", "devops": "devops ci-cd deploy",
    "machine-learning": "machine-learning ml", "deep-learning": "deep-learning neural",
    "data-science": "data-science", "business-intelligence": "business-intelligence bi dashboard",
    "ui/ux": "ui ux design", "front-end": "frontend", "back-end": "backend",
    "full-stack": "fullstack", "tech-stack": "tech-stack", "no-code": "no-code",
    "low-code": "low-code", "open-source": "open-source", "self-hosted": "self-hosted",
    # Istilah Indonesia domain-spesifik (lowongan, zakat, pantun, dsb).
    "lowongan": "job vacancy hiring career", "kerja": "job work career",
    "pekerjaan": "job work career", "karir": "career job", "gaji": "salary payroll",
    "tunjangan": "allowance benefit", "lembur": "overtime", "cuti": "leave vacation",
    "absen": "attendance", "kehadiran": "attendance", "presensi": "attendance",
    "zakat": "zakat islamic charity finance", "sedekah": "charity donation",
    "wasiat": "will testament", "waris": "inheritance estate",
    "pantun": "poem poetry", "puisi": "poem poetry", "sajak": "poem poetry",
    "nulis": "write writing", "menulis": "write writing", "karangan": "writing essay",
    "resensi": "review book", "buku": "book", "novel": "novel book fiction",
    "cerita": "story narrative", "dongeng": "folktale story", "fabel": "fable story",
    "cek": "check verify", "periksa": "check inspect", "verifikasi": "verify verification",
    "keaslian": "authenticity verify", "berita": "news", "hoaks": "fake-news fact-check",
    "gosip": "gossip rumor", "isu": "issue topic", "topik": "topic",
    "makanan": "food recipe cooking", "masakan": "food recipe cooking", "resep": "recipe cooking",
    "minuman": "beverage drink", "kue": "cake pastry", "jajanan": "snack food",
    "belanja": "shopping ecommerce", "belanjaan": "shopping grocery", "warung": "shop store",
    "toko": "store shop", "restoran": "restaurant", "kafe": "cafe coffee",
    "sentimen": "sentiment analysis opinion", "analisis": "analysis analytics",
    "nego": "negotiation negotiate", "negosiasi": "negotiation", "deal": "deal negotiation",
    "kata": "word passphrase", "sandi": "password passphrase", "kuat": "strong secure random",
    "rahasia": "secret confidential", "privasi": "privacy", "anonim": "anonymous",
    "gitar": "guitar music", "piano": "piano music", "drum": "drum music",
    "lagu": "song music", "musik": "music", "nada": "tone pitch music",
    "mod": "mod minecraft game", "minecraft": "minecraft game", "roblox": "roblox game",
    "game": "game gaming", "main": "play game", "ngegame": "gaming",
    "belajar": "learn study course", "mengajar": "teach teaching", "les": "tutoring lesson",
    "ujian": "exam test", "ulangan": "exam quiz", "tugas": "assignment homework",
    "skripsi": "thesis dissertation", "jurnal": "journal paper", "abstrak": "abstract",
    "portfolio": "portfolio website showcase", "lamaran": "application cover-letter",
    "wawancara": "interview", "rekrutmen": "recruitment hiring", "lowongan": "vacancy job",
    "invoice": "invoice billing", "tagihan": "bill invoice payment", "pembayaran": "payment",
    "transfer": "transfer payment", "bank": "bank banking", "rekening": "account bank",
    "pinjaman": "loan credit", "hutang": "debt loan", "cicilan": "installment loan",
    "asuransi": "insurance", "bpjs": "bpjs insurance", "pajak": "tax",
    "sppt": "property-tax", "nikah": "marriage wedding", "kawin": "marriage wedding",
    "mempelai": "bride groom wedding", "undangan": "invitation wedding", "seserahan": "wedding-gift",
    "kelahiran": "birth newborn", "bayi": "baby infant", "parenting": "parenting",
    "sekolah": "school education", "kampus": "university campus", "mahasiswa": "student university",
    "ijazah": "diploma certificate", "sertifikat": "certificate", "pelatihan": "training workshop",
    "webinar": "webinar", "lokakarya": "workshop", "seminar": "seminar",
    "acara": "event", "rapat": "meeting", "notulen": "meeting-minutes",
    "surat": "letter document", "memo": "memo memorandum", "pengumuman": "announcement",
    "lowongan": "job vacancy", "pelamar": "applicant candidate", "wawancara": "interview",
    "kuesioner": "questionnaire survey", "survei": "survey", "angket": "questionnaire",
    "olahraga": "sport fitness", "lari": "running", "badminton": "badminton sport",
    "sepak": "football soccer", "bola": "ball sport", "renang": "swimming",
    "hobi": "hobby", "koleksi": "collection", "stiker": "sticker", "collector": "collector",
    "otomotif": "automotive car", "motor": "motorcycle", "mobil": "car automobile",
    "service": "car-service", "sparepart": "spare-part", "bengkel": "workshop garage",
    "hewan": "pet animal", "kucing": "cat pet", "anjing": "dog pet", "hamster": "hamster pet",
    "tanaman": "plant gardening", "kebun": "garden", "sawah": "rice-field farming",
    "panen": "harvest", "ternak": "livestock farming", "ikan": "fish",
    "ikan": "fish", "lele": "catfish", "lele": "catfish",
    "travel": "travel trip", "wisata": "tourism travel", "hotel": "hotel",
    "tiket": "ticket", "penerbangan": "flight", "kereta": "train",
    "bus": "bus", "ojek": "ride-hailing", "ojol": "ride-hailing", "gojek": "gojek",
    "shopee": "shopee marketplace", "tokopedia": "tokopedia marketplace",
    "bukalapak": "bukalapak marketplace", "lazada": "lazada marketplace",
    "tiktok": "tiktok", "instagram": "instagram", "facebook": "facebook",
    "youtube": "youtube", "twitter": "twitter x", "threads": "threads",
    "konten": "content", "viral": "viral", "fyp": "fyp tiktok", "trending": "trending",
    "engagement": "engagement", "follower": "follower", "subscriber": "subscriber",
    "monetisasi": "monetization", "cuan": "profit money", "untung": "profit",
    "rugi": "loss", "modal": "capital investment", "investasi": "investment",
    "saham": "stock trading", "crypto": "crypto", "bitcoin": "bitcoin btc",
    "nft": "nft", "web3": "web3", "dao": "dao", "defi": "defi",
    "freelance": "freelance", "proyek": "project", "klien": "client",
    "deadline": "deadline", "scope": "scope", "deliverable": "deliverable",
    "estimasi": "estimate", "offer": "offer proposal", "proposal": "proposal",
    "quotation": "quotation quote", "nego": "negotiate", "kontrak": "contract",
    # Ambiguitas nama diri & istilah lokal yang sering salah-match.
    "tanah": "land property certificate", "sertifikat": "certificate land",
    "balik": "transfer rename back", "perusahaan": "company business firm",
    "pt": "perseroan terbatas company", "cv": "cv resume surat lamaran curriculum vitae",
    "kip": "kip beasiswa scholarship", "kuliah": "college university student",
    "umroh": "umroh haji islamic travel", "haji": "hajj pilgrimage",
    "bali": "bali indonesia travel", "jogja": "yogyakarta travel",
    "bromo": "bromo volcano travel", "stnk": "stnk vehicle registration",
    "npwp": "npwp tax id", "nik": "nik identity ktp",
    "skck": "skck police certificate", "kartu": "card id",
    "rt": "rt rw neighborhood", "rw": "rw rt neighborhood",
    "paket": "package tour travel bundle", "tour": "tour travel trip",
    "biaya": "cost fee expense", "tarif": "fare tariff price",
    "diskon": "discount promo", "promo": "promotion discount",
    "ongkir": "shipping ongkir delivery", "resi": "tracking resi receipt",
    "stok": "stock inventory", "penjualan": "sales selling",
    "pembelian": "purchase buying", "belanja": "shopping purchase",
    "pengiriman": "shipping delivery", "pengembalian": "return refund",
    "garansi": "warranty guarantee", "servis": "service repair maintenance",
    "bengkel": "workshop repair garage", "oli": "oil lubricant",
    "sparepart": "spare-part sparepart", "velg": "wheel rim", "ban": "tire tyre",
    # Ambiguitas teknis: "utm" bisa marketing-tag (UTM parameter) atau
    # Universal Transverse Mercator (geodesi). Sinonim keduanya disertakan.
    "utm": "utm universal transverse mercator coordinate geodesi survey lintang bujur",
    "konversi": "convert conversion transform",
    "lintang": "latitude lintang bujur koordinat", "bujur": "longitude koordinat",
    "koordinat": "coordinate gps utm latlon",
    "angin": "wind direction speed meteorology angin",
    "fisika": "physics formula mechanics",
    "unduh": "download fetch pull", "simpan": "save store", "baca": "read parse",
    "dataset": "dataset data csv table records", "data": "data dataset",
}
# Kata yang menandakan tugas desain -> naikkan skill kategori designer + curated.
DESIGN_HINT = {
    "design", "ui", "ux", "dashboard", "landing", "component", "layout", "grid", "typography",
    "color", "palette", "animation", "motion", "accessibility", "responsive", "theme", "polished",
    "generic", "slop", "page", "screen", "button", "card", "form", "icon", "table", "dark", "light",
}


ORIG_TERMS = []

_ID_WORDS = set("yang dan di ke dari untuk dengan pada dalam adalah ini itu atau tidak ada "
                "akan juga bisa perlu harus cara agar supaya telah sudah hanya lebih paling "
                "bikin buat dong aja kok nih tuh gimana kenapa apakah saya kamu kami kita "
                "mereka apa siapa kapan dimana mengapa berapa jadi kalau ketika karena "
                # Istilah domain yang khas Indonesia — query berisi ini hampir pasti
                # Bahasa Indonesia walau tanpa stopword ("perpanjang stnk", "hitung zakat").
                "stnk bpkb pkb bpjs zakat infak sedekah pnpm ppat snpmb kip lpdp beasiswa "
                "umroh haji umrah ojol gojek grab shopee tokopedia lazada bukalapak "
                "warung umkm rt rw kelurahan kecamatan provinsi kabupaten jakarta".split())

# Satu kata domain saja cukup untuk menandai query Indonesia.
_ID_DOMAIN = set("stnk bpkb pkb bpjs zakat infak sedekah snpmb kip lpdp beasiswa umroh "
                 "haji umrah ojol gojek grab shopee tokopedia lazada bukalapak warung umkm "
                 "kelurahan kecamatan provinsi kabupaten perusahaan usaha bisnis gaji nego "
                 "resensi pendidikan sekolah mahasiswa kesehatan dokter rumah belanja cicilan "
                 "utang tabungan penghasilan pekerjaan karir nikah pernikahan".split())


def query_lang(q):
    """Tebak bahasa query: zh (CJK), id (stopword/istilah Indonesia), default en.
    id diperlakukan kompatibel dengan en — mayoritas skill berkonten Inggris."""
    if re.search(r"[一-鿿぀-ヿ가-힯]", q):
        return "zh"
    words = set(re.findall(r"[a-z]+", q.lower()))
    if len(words & _ID_WORDS) >= 2 or words & _ID_DOMAIN:
        return "id"
    return "en"


def terms(q):
    global ORIG_TERMS
    ORIG_TERMS = [t for t in re.findall(r"[\w./+-]+", q.lower())
                  if t not in STOP and len(t) > 1]
    out = []
    for t in re.findall(r"[\w./+-]+", q.lower()):
        if t in STOP or len(t) <= 1:
            continue
        # Selalu sertakan token asli + ekspansi sinonim: skill yang NAMANYA
        # memakai kata asli (mis. "analisis-*") tidak boleh hilang hanya karena
        # sinonimnya bahasa Inggris.
        if not (len(t) == 2 and t in AMBIG2):
            out.append(t)
        out.extend(SYN.get(t, t).split())
    # buang duplikat, jaga urutan
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    # Token majemuk ("fine-tune", "ci/cd", "ui/ux"): sertakan juga bagian-bagiannya
    # supaya "fine-tuning"/"github-actions" tetap cocok lewat "fine"/"cd".
    for t in list(uniq):
        parts = [p for p in re.split(r"[-/_.]+", t) if len(p) > 2]
        if len(parts) > 1:
            for p in parts:
                if p not in seen:
                    seen.add(p)
                    uniq.append(p)
    return uniq or [q.lower()]

def main():
    a = sys.argv[1:]
    if not a:
        sys.exit('pakai: skillq.py "kata" [-n 5] | skillq.py -l <nama>')
    if a[0] == "--design":
        # Koleksi desain terkurasi — supaya skill UI/UX selalu muncul paling depan.
        import json
        cur = os.path.expanduser("~/.agents/design-skills.json")
        names = json.load(open(cur))["core"]
        if len(a) > 2 and a[1] in ("-l", "--load"):
            a = a[1:]  # lanjut ke mode load di bawah
        else:
            if "-n" in a:
                names = names[: int(a[a.index("-n") + 1])]
            c = sqlite3.connect(DB)
            for name in names:
                r = c.execute(
                    "SELECT COALESCE(category,''), COALESCE(description,''), path FROM skills WHERE name=? LIMIT 1",
                    (name,)).fetchone()
                if not r:
                    continue
                cat, desc, path = r
                print(f"- {name} [{cat or '-'}] {(desc or '')[:60]} — {path.replace(os.path.expanduser('~'), '~')}")
            return
    if "--repo" in a or "-r" in a:
        a = [x for x in a if x not in ("--repo", "-r")]
        # Cari repo (bukan skill). Pakai: skillq.py --repo "whatsapp api" -n 5
        rest = a
        n = 5
        if "-n" in rest:
            i = rest.index("-n"); n = int(rest[i + 1]); rest = rest[:i] + rest[i + 2:]
        q = " ".join(rest).strip()
        if not q:
            sys.exit("pakai: skillq.py --repo \"kata\" -n 5")
        c = sqlite3.connect(REPO_DB)
        ts = [t for t in q.split() if len(t) > 1]
        rows = []
        # AND dulu (semua kata cocok) supaya relevan, baru OR kalau kosong.
        for joiner in (" AND ", " OR "):
            try:
                rows = c.execute(
                    "SELECT r.slug, r.stars, r.state, r.has_skill, substr(r.desc,1,70) FROM repos r "
                    "WHERE r.slug IN (SELECT slug FROM repos_fts WHERE repos_fts MATCH ?) "
                    "ORDER BY r.stars DESC LIMIT ?", (joiner.join(ts), n)).fetchall()
            except Exception:
                rows = []
            if rows:
                break
        if not rows:
            like = f"%{q}%"
            rows = c.execute(
                "SELECT slug, stars, state, has_skill, substr(desc,1,70) FROM repos "
                "WHERE slug LIKE ? OR desc LIKE ? ORDER BY stars DESC LIMIT ?",
                (like, like, n)).fetchall()
        total = c.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
        if not rows:
            print(f"tidak ada repo cocok (total {total} repo di indeks)")
            return
        for slug, stars, state, hs, desc in rows:
            tag = f"{state}{'+skill' if hs else ''}"
            print(f"- {slug} \u2b50{stars} [{tag}] {desc}")
        print(f"({total} repo terindeks; clone saat perlu: "
              f"python3 ~/.agents/repo-hub.py get <owner/name>)")
        return
    if a[0] in ("-l", "--load"):
        name = a[1]
        c = sqlite3.connect(DB, timeout=30)
        # feedback loop: catat skill yang benar-benar di-load -> ranking naik tipis
        try:
            c.execute("CREATE TABLE IF NOT EXISTS skusage(name TEXT PRIMARY KEY, cnt INTEGER)")
            c.execute("INSERT INTO skusage(name,cnt) VALUES(?,1) "
                      "ON CONFLICT(name) DO UPDATE SET cnt=cnt+1", (name,))
            c.commit()
        except Exception:
            pass
        r = c.execute("SELECT path FROM skills WHERE name=? LIMIT 1", (name,)).fetchone()
        if not r:
            r = c.execute("SELECT path FROM skills WHERE name LIKE ? LIMIT 1", (f"%{name}%",)).fetchone()
        if not r:
            sys.exit(f"tidak ada skill '{name}'")
        with open(r[0], encoding="utf-8", errors="ignore") as f:
            print("".join(f.readlines()[:90]))
        return
    n = 5
    if "-n" in a:
        i = a.index("-n"); n = int(a[i+1]); a = a[:i] + a[i+2:]
    q = " ".join(a).strip()
    if not q:
        sys.exit('pakai: skillq.py "kata" [-n 5] | skillq.py -l <nama> | skillq.py --repo "kata"')
    c = sqlite3.connect(DB, timeout=30)
    try:
        c.execute("CREATE TABLE IF NOT EXISTS skusage(name TEXT PRIMARY KEY, cnt INTEGER)")
        c.commit()
    except Exception:
        pass
    rows = []
    q_terms = terms(q)
    design_task = any(t in DESIGN_HINT for t in q_terms)
    # Kolom: name, description, tier, category, path, source.
    # Nama diberi bobot 8: kalau query menyebut "logo", skill yang NAMANYA logo
    # harus menang atas skill yang cuma menyebut logo di deskripsi. Tanpa bobot,
    # bm25 memilih deskripsi terpendek — bukan yang paling relevan.
    # IDF: kata langka ("vue", "cloudflare") jauh lebih menentukan daripada kata
    # umum ("setup", "hosting"). Tanpa ini "vue 3 setup" jatuh ke skill setup-*.
    try:
        total_rows = c.execute("SELECT count(*) FROM skills").fetchone()[0] or 1
    except Exception:
        total_rows = 1
    df_cache = {}

    def idf(t):
        if t not in df_cache:
            try:
                k = c.execute("SELECT count(*) FROM skills WHERE skills MATCH ?", (f'"{t}"',)).fetchone()[0]
            except Exception:
                k = 1
            df_cache[t] = max(0.35, min(3.0, __import__("math").log((total_rows + 1) / (k + 1)) / 3.0))
        return df_cache[t]

    order = "bm25(skills, 8.0, 1.0, 0.0, 0.0, 0.0, 0.0) + (CASE WHEN skills.tier = 'curated' THEN 0.0 ELSE 2.5 END)"
    # Nama yang PERSIS atau berawalan salah satu kata query naik ke atas:
    # "bikin logo" → logo-studio, bukan frame-logo-outro yang cuma memuat
    # kata "logo" di tengah nama.
    order += " + (CASE WHEN skills.name = :q THEN -100.0 ELSE 0 END)"
    params = {"q": q.strip().lower(), "n": n}
    nname = "replace(name, '-', ' ')"
    # Bonus nama HANYA untuk token asli query — sinonim ("stnk"→"vehicle")
    # jangan sampai membuat skill Inggris bernama "vehicle-*" mengalahkan
    # skill Indonesia yang deskripsinya memang relevan.
    for i, t in enumerate(ORIG_TERMS):
        if t in AMBIG2:
            continue
        params[f"t{i}"] = t
        w = idf(t)
        order += (f" + (CASE WHEN replace(skills.name, '-', ' ') = :t{i} OR replace(skills.name, '-', ' ') LIKE :t{i} || ' %'"
                 f" THEN {-14.0 * w:.2f} ELSE 0 END)")
    # Nama yang MEMUAT kata query (batas kata, "marketplace" != "market") harus
    # mengalahkan skill yang hanya menyebut kata itu di deskripsi.
    for i, t in enumerate(ORIG_TERMS):
        if len(t) >= 3 and t not in AMBIG2:
            order += (f" + (CASE WHEN instr(' ' || replace(skills.name, '-', ' ') || ' ', ' ' || :t{i} || ' ') > 0"
                     f" THEN {-10.0 * idf(t):.2f} ELSE 0 END)")
    # Cakupan kata: skill yang tidak memuat salah satu kata query didenda ringan.
    # Probe = token asli + sinonimnya: "saham" harus dianggap ter-cover oleh skill
    # "stock-trading" (memuat "stock"), bukan dihukum karena tak ada literal "saham".
    # Dulu query pakai AND (semua kata wajib) sehingga "deploy cloudflare hosting"
    # membuang cloudflare-deploy hanya karena kata "hosting" tidak ada di deskripsinya.
    for i, t in enumerate(ORIG_TERMS):
        probes = []
        for p in [t] + SYN.get(t, "").split():
            for pp in re.split(r"[^a-z0-9]+", p):
                if len(pp) >= 3 and pp not in probes:
                    probes.append(pp)
        probes = probes[:6] or [t]
        # Batas kata (bukan substring): "marketplace" tidak boleh dianggap
        # mencakup "market". Nama di-normalisasi '-' -> ' ' dulu.
        hay = "lower(replace(skills.name, '-', ' ') || ' ' || skills.description)"
        conds = " AND ".join(
            f"instr(' ' || {hay} || ' ', ' ' || :o{i}_{j} || ' ') = 0"
            for j in range(len(probes)))
        for j, p in enumerate(probes):
            params[f"o{i}_{j}"] = p
        try:
            k = c.execute("SELECT count(*) FROM skills WHERE skills MATCH ?", (f'"{t}"',)).fetchone()[0]
        except Exception:
            k = 1
        w = max(0.0, min(3.0, __import__("math").log((total_rows + 1) / (k + 1)) / 3.0))
        # Diperkuat: skill yang kehilangan 2+ kata asli ("kirim" tapi tanpa
        # "email"/"otomatis") harus kalah dari skill yang mencakup hampir semua.
        order += (f" + (CASE WHEN {conds}"
                  f" THEN {3.0 + 3.0 * w:.2f} ELSE 0 END)")
    # Skill auto-doc berbahasa asing (template massal "Wenn es um...", "Eres el
    # motor...") sering menang hanya karena nama slug cocok — dendakan ringan.
    order += (" + (CASE WHEN skills.description LIKE 'Wenn es um%'"
                " OR skills.description LIKE 'Eres el motor%'"
                " OR skills.description LIKE 'Für %' THEN 3.0 ELSE 0 END)")
    # Penalti bahasa: query id/en tidak boleh dimenangkan skill Jerman/Spanyol/
    # Portugis/Prancis/Cina yang namanya kebetulan mirip ("foto-*", "analisis-*").
    qlang = query_lang(q)
    params["qlang"] = qlang
    if qlang in ("en", "id"):
        # Penalti besar: boost nama bisa mencapai -100, jadi skill asing harus
        # benar-benar jauh lebih cocok untuk menangi query Indonesia/Inggris.
        order += (" + (CASE WHEN sklang.lang IN ('de','es','pt','fr','tr','it','nl','pl','cs','uk','vi','th','ja','ko') THEN 35.0"
                    " WHEN sklang.lang = 'zh' THEN 20.0 ELSE 0 END)")
        if qlang == "id":
            # Query Indonesia: skill berbahasa Indonesia menang tipis — deskripsi
            # lokal ("STNK", "zakat") memang tidak mungkin cocok di skill Inggris.
            order += " + (CASE WHEN sklang.lang = 'id' THEN -4.0 ELSE 0 END)"
    elif qlang == "zh":
        order += (" + (CASE WHEN sklang.lang NOT IN ('zh','??') THEN 20.0 ELSE 0 END)")
    # Feedback loop: skill yang sering di-load (`sk -l`) naik tipis — maks -4.8.
    # COALESCE wajib: tanpa itu NULL meracuni total skor baris tanpa pemakaian.
    order += (" + COALESCE((SELECT -0.4 * MIN(u.cnt, 12) FROM skusage u"
             " WHERE u.name = skills.name), 0)")
    if design_task:
        # Tugas UI/UX: skill designer naik, sisanya tidak dihapus.
        order += " + (CASE WHEN skills.category = 'designer' THEN -1.5 ELSE 0 END)"
    # Buang artefak auto-forge (isi kosong/duplikat) yang dulu membanjiri hasil,
    # dan tier 'junk' yang memang tidak masuk hitungan "siap dipakai".
    junk = (" AND skills.tier <> 'junk'"
            " AND skills.name NOT LIKE 'auto-%' AND skills.name NOT LIKE 'revision-%'"
            " AND skills.path NOT LIKE '%skill-forger%'")
    try:
        # Quote tiap term: token berisi '-'/'/' ("fine-tune", "ci/cd") bikin
        # FTS5 MATCH syntax error -> query gagal total -> fallback LIKE kosong.
        params["fts"] = " OR ".join('"' + t.replace('"', "") + '"' for t in q_terms)
        rows = c.execute(
            "SELECT skills.name, COALESCE(skills.category,''), COALESCE(skills.description,''), skills.path FROM skills "
            "LEFT JOIN sklang ON sklang.name = skills.name "
            f"WHERE skills MATCH :fts{junk} ORDER BY {order} LIMIT :n", params).fetchall()
    except Exception:
        rows = []
    if not rows:
        like = f"%{q}%"
        rows = c.execute(
            "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
            "WHERE name LIKE ? OR description LIKE ? LIMIT ?", (like, like, n)).fetchall()
    if not rows:
        print("tidak ada hasil")
        return
    ready = _ready_map()
    for name, cat, desc, path in rows:
        d = (desc or "").replace("\n", " ").strip()[:60]
        short = path.replace(os.path.expanduser("~"), "~")
        print(f"- {name} [{cat or '-'}] {d} — {short}{_badge(ready.get(name))}")

main()
