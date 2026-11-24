#!/usr/bin/env python3
"""data-hub — katalog & pengambil dataset publik 0-token untuk AI.

Dataset disimpan di ~/.agents/datasets/<slug>/ (hanya saat diminta —
tidak membebani storage). Sumber: UCI Machine Learning Repository
(archive.ics.uci.edu, publik tanpa API key) + mirror GitHub `datasets`.

Pakai:
  data-hub list                     # semua dataset + status terunduh
  data-hub search <kata>            # cari dataset
  data-hub get <slug>               # unduh & ekstrak -> path CSV
  data-hub get <slug> --info        # metadata tanpa unduh
"""
import json
import os
import subprocess
import sys
import zipfile

ROOT = os.path.expanduser("~/.agents/datasets")

# slug -> (nama, domain, url, catatan)
UCI = "https://archive.ics.uci.edu/static/public/{id}/{file}.zip"
DATASETS = {
    # --- Teknik sipil / material / aero (relevan menara, struktur, angin) ---
    "concrete-strength": ("Concrete Compressive Strength", "sipil-material",
        UCI.format(id=165, file="concrete+compressive+strength"),
        "1030 sampel: semen, fly ash, air, agregat -> kuat tekan MPa. Untuk desain pondasi/menara."),
    "airfoil-noise": ("Airfoil Self-Noise", "aero-akustik",
        UCI.format(id=291, file="airfoil+self+noise"),
        "1503 sampel: frekuensi, angle attack, chord, velocity, suction -> noise dB. Untuk aerodinamika/angin menara."),
    "energy-efficiency": ("Energy Efficiency (heating/cooling load)", "energi-bangunan",
        UCI.format(id=242, file="energy+efficiency"),
        "768 sampel: orientasi, luas dinding, atap -> heating/cooling load. Untuk efisiensi energi gedung."),
    # --- Klasifikasi & regresi klasik ML ---
    "iris": ("Iris", "klasifikasi",
        UCI.format(id=53, file="iris"),
        "150 sampel klasik: sepal/petal -> spesies. Baseline klasifikasi."),
    "wine-quality": ("Wine Quality (red+white)", "klasifikasi-regresi",
        UCI.format(id=186, file="wine+quality"),
        "~6500 sampel: fisikokimia -> skor kualitas 0-10. Regresi ordinal."),
    "wine-italian": ("Wine (Italian cultivars)", "klasifikasi",
        UCI.format(id=109, file="wine"),
        "178 sampel kimia anggur -> 3 cultivar."),
    "diabetes": ("Diabetes 130-US", "klasifikasi-regresi",
        UCI.format(id=34, file="diabetes"),
        "442 sampel: readmission diabetes -> klasifikasi."),
    "bank-marketing": ("Bank Marketing", "klasifikasi-tidak-seimbang",
        UCI.format(id=222, file="bank+marketing"),
        "45k panggilan telemarketing bank -> deposit yes/no. Klasifikasi imbalanced."),
    "student-performance": ("Student Performance", "regresi-klasifikasi",
        UCI.format(id=320, file="student+performance"),
        "649 sampel: demografi, kebiasaan -> nilai akhir G1/G2/G3."),
    "breast-cancer": ("Breast Cancer Wisconsin (diagnostic)", "klasifikasi-medical",
        UCI.format(id=17, file="breast+cancer+wisconsin+diagnostic"),
        "569 sampel: fitur nukleus sel -> jinak/ganas."),
    "parkinsons": ("Parkinsons Telemonitoring", "regresi-medical",
        UCI.format(id=174, file="parkinsons"),
        "5875 sampel suara -> UPDRS parkinson."),
    # --- Mirror GitHub datasets (CSV mentah) ---
    "population-world": ("Population (World Bank, per negara/tahun)", "demografi",
        "https://raw.githubusercontent.com/datasets/population/master/data/population.csv",
        "Populasi tiap negara per tahun — untuk analisis tren/forecast."),
    # --- Teknik tambahan: material, getaran, lalu lintas, energi, RF ---
    "steel-plates-faults": ("Steel Plates Faults", "material-cacat",
        UCI.format(id=198, file="steel+plates+faults"),
        "1941 sampel: 27 fitur permukaan baja -> 7 jenis cacat. Untuk inspeksi baja menara/struktur."),
    "hydraulic-systems": ("Condition Monitoring of Hydraulic Systems", "maintenance-prediktif",
        UCI.format(id=447, file="condition+monitoring+of+hydraulic+systems"),
        "2205 sampel sensor -> cooler/valve/pump/motor stable/optimal/near-failure. Untuk monitoring peralatan."),
    "traffic-volume": ("Metro Interstate Traffic Volume", "lalu-lintas",
        UCI.format(id=492, file="metro+interstate+traffic+volume"),
        "48k sampel: cuaca/jam/hari -> volume lalu lintas. Untuk perencanaan jalan."),
    "appliances-energy": ("Appliances Energy Prediction", "energi-rumah",
        UCI.format(id=374, file="appliances+energy+prediction"),
        "19k sampel sensor rumah -> watt hour appliance. Untuk manajemen energi gedung."),
    "occupancy-detection": ("Occupancy Detection", "sensor-gedung",
        UCI.format(id=357, file="occupancy+detection"),
        "20k sampel: suhu/kelembaban/cahaya/CO2 -> ruangan terisi/tidak. Untuk smart building/BMS."),
    "yacht-hydrodynamics": ("Yacht Hydrodynamics", "hidrodinamika",
        UCI.format(id=243, file="yacht+hydrodynamics"),
        "308 sampel geometri lambung -> resistance/heel. Untuk desain lambung/struktur apung."),
    "auto-mpg": ("Auto MPG", "regresi-kendaraan",
        UCI.format(id=9, file="auto+mpg"),
        "398 sampel: berat, silinder, tenaga -> konsumsi bahan bakar mpg."),
    "secom": ("SECOM Semiconductor Manufacturing", "manufacturing",
        UCI.format(id=179, file="secom"),
        "1567 sampel, 590 fitur sensor -> hasil produksi baik/gagal. Untuk predictive maintenance industri."),
    "bankruptcy-poland": ("Polish Companies Bankruptcy", "finansial-risiko",
        UCI.format(id=365, file="polish+companies+bankruptcy+data"),
        "10k perusahaan, 64 fitur keuangan -> bangkrut/tidak. Untuk analisis risiko."),
    "student-eval": ("Higher Education Student Performance", "pendidikan",
        UCI.format(id=856, file="higher+education+students+performance+evaluation"),
        "145 sampel survei -> performa akademik. Untuk analisis pendidikan."),
    "steel-energy": ("Steel Industry Energy Consumption", "energi-industri",
        UCI.format(id=851, file="steel+industry+energy+consumption"),
        "350 sampel ->Consumption energi industri baja. Untuk efisiensi industri."),
}

# HuggingFace datasets-server: ribuan dataset publik tanpa API key.
# Pakai: data-hub get hf:<owner>/<nama>  (contoh: data-hub get hf:cornell-movie-review-data/rotten_tomatoes)
HF_API = "https://datasets-server.huggingface.co"

def downloaded(slug):
    d = os.path.join(ROOT, slug)
    return d if os.path.isdir(d) and any(f.endswith((".csv", ".dat", ".xls", ".xlsx", ".data", ".jsonl", ".gz", ".arff", ".parquet", ".npz")) for f in os.listdir(d)) else None

def get_hf(spec, rows=1000):
    """Ambil dataset HuggingFace via datasets-server (tanpa API key).
    spec = owner/nama. Simpan JSONL + ringkasan kolom."""
    import json as _json
    import urllib.parse, urllib.request
    ds = urllib.parse.quote(spec, safe="")
    out = os.path.join(ROOT, "hf-" + spec.replace("/", "__"))
    os.makedirs(out, exist_ok=True)
    target = os.path.join(out, "rows.jsonl")
    if os.path.exists(target):
        print(f"sudah ada: {target}"); return
    def api(path):
        with urllib.request.urlopen(f"{HF_API}{path}", timeout=30) as r:
            return _json.loads(r.read())
    # Temukan config+split pertama yang punya rows
    cfgs = api(f"/splits?dataset={ds}").get("splits", [])
    if not cfgs:
        sys.exit(f"dataset {spec} tidak punya split publik (atau nama salah)")
    s = cfgs[0]
    cfg, split = s["config"], s["split"]
    got, offset = [], 0
    while len(got) < rows:
        n = min(100, rows - len(got))
        try:
            d = api(f"/rows?dataset={ds}&config={urllib.parse.quote(cfg)}&split={urllib.parse.quote(split)}&offset={offset}&length={n}")
        except Exception as e:
            print(f"henti di offset {offset}: {e}"); break
        batch = d.get("rows", [])
        if not batch:
            break
        got += [r["row"] for r in batch]
        offset += len(batch)
        if len(batch) < n:
            break
    with open(target, "w", encoding="utf-8") as f:
        for r in got:
            f.write(_json.dumps(r, ensure_ascii=False) + "\n")
    cols = list(got[0].keys()) if got else []
    print(f"tersimpan: {target}  ({len(got)} baris, config={cfg}, split={split})")
    print(f"  kolom ({len(cols)}): {', '.join(cols[:15])}{' ...' if len(cols)>15 else ''}")

def get_zenodo(rid):
    """Ambil file pertama dataset Zenodo via API publik -> ~/.agents/datasets/zenodo-<id>/."""
    import json as _json
    import urllib.request
    out = os.path.join(ROOT, f"zenodo-{rid}")
    os.makedirs(out, exist_ok=True)
    with urllib.request.urlopen(f"https://zenodo.org/api/records/{rid}", timeout=30) as r:
        rec = _json.loads(r.read())
    files = rec.get("files", [])
    if not files:
        sys.exit("record tidak punya file")
    # pilih file kecil dulu, maks ~50MB
    files.sort(key=lambda f: f.get("size", 0))
    f = files[0]
    if f.get("size", 0) > 50_000_000:
        sys.exit(f"file terlalu besar: {f['size']/1e6:.0f} MB")
    dest = os.path.join(out, f["key"])
    if os.path.exists(dest):
        print(f"sudah ada: {dest}"); return
    url = f["links"]["self"]
    subprocess.run(["curl", "-fsSL", "--max-time", "300", "-o", dest, url], check=True)
    print(f"tersimpan: {dest} ({f['size']/1024:.0f} KB) — {f['key']}")
    if len(files) > 1:
        print(f"  ({len(files)-1} file lain; edit data-hub.py untuk fetch manual)")

def get_openml(did):
    """Unduh dataset OpenML (ARFF/zip) -> ~/.agents/datasets/openml-<did>/."""
    out = os.path.join(ROOT, f"openml-{did}")
    os.makedirs(out, exist_ok=True)
    if os.listdir(out):
        print(f"sudah ada: {out}"); return
    url = f"https://www.openml.org/data/v1/download/{did}"
    dest = os.path.join(out, f"{did}.zip")
    try:
        subprocess.run(["curl", "-fsSL", "--max-time", "120", "-o", dest, url], check=True)
    except subprocess.CalledProcessError:
        sys.exit(f"gagal unduh OpenML {did}")
    import zipfile
    try:
        with zipfile.ZipFile(dest) as z:
            z.extractall(out)
        os.remove(dest)
    except zipfile.BadZipFile:
        # OpenML sering mengembalikan ARFF mentah, bukan zip
        os.rename(dest, os.path.join(out, f"{did}.arff"))
    print(f"tersimpan: {out}")

def get(slug, info_only=False):
    if slug.startswith("hf:"):
        return get_hf(slug[3:])
    if slug.startswith("zenodo:"):
        return get_zenodo(slug[7:])
    if slug.startswith("openml:"):
        return get_openml(slug[7:])
    if slug not in DATASETS:
        sys.exit(f"slug tidak dikenal: {slug} — coba: data-hub list")
    name, domain, url, note = DATASETS[slug]
    if info_only:
        print(f"{slug}: {name}\n  domain : {domain}\n  url    : {url}\n  catatan: {note}")
        return
    d = downloaded(slug)
    if d:
        print(f"sudah ada: {d}")
        return
    out = os.path.join(ROOT, slug)
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_dl.zip" if url.endswith(".zip") else "_dl.csv")
    try:
        subprocess.run(["curl", "-fsSL", "--max-time", "120", "-o", tmp, url], check=True)
    except subprocess.CalledProcessError:
        sys.exit(f"gagal unduh {url}")
    files = []
    if url.endswith(".zip"):
        with zipfile.ZipFile(tmp) as z:
            z.extractall(out)
        os.remove(tmp)
        for dp, _, fns in os.walk(out):
            files += [os.path.join(dp, f) for f in fns]
    else:
        os.rename(tmp, os.path.join(out, os.path.basename(url.split("?")[0]) or "data.csv"))
        files = [os.path.join(out, f) for f in os.listdir(out)]
    print(f"tersimpan: {out}")
    for f in files[:8]:
        sz = os.path.getsize(f)
        print(f"  {f}  ({sz/1024:.0f} KB)")

def peek(slug):
    """EDA instan: temukan file utama dataset lalu jalankan data-eda.py (test-venv)."""
    # slug bisa: nama dataset, "hf:<owner>/<nama>", "zenodo:<id>", atau path file
    if os.path.exists(slug):
        venv_py = os.path.expanduser("~/.agents/test-venv/bin/python3")
        subprocess.run([venv_py, os.path.expanduser("~/.agents/data-eda.py"), slug])
        return
    if slug.startswith("hf:"):
        slug = "hf-" + slug[3:].replace("/", "__")
    elif slug.startswith("zenodo:"):
        get_zenodo(slug[7:])
        slug = f"zenodo-{slug[7:]}"
    elif slug.startswith("openml:"):
        get_openml(slug[7:])
        slug = f"openml-{slug[7:]}"
    d = downloaded(slug)
    if not d:
        get(slug)
        d = downloaded(slug)
    if not d:
        sys.exit(f"tidak ada file untuk {slug}")
    # pilih file data: prioritas ekstensi data, hindari readme/license/dokumen
    cands = []
    pri = {".csv": 5, ".jsonl": 5, ".xlsx": 4, ".xls": 4, ".dat": 3,
           ".data": 3, ".txt": 2, ".arff": 2}
    for dp, _, fns in os.walk(d):
        for f in fns:
            low = f.lower()
            if any(k in low for k in ("readme", "license", "changelog", "metadata")):
                continue
            p = os.path.join(dp, f)
            ext = os.path.splitext(low)[1]
            if ext in pri or low.endswith(".csv.gz"):
                cands.append((pri.get(ext, 1), os.path.getsize(p), p))
    if not cands:
        sys.exit("tidak ada file data yang didukung")
    cands.sort(key=lambda x: (x[0], x[1]), reverse=True)
    path = cands[0][2]
    venv_py = os.path.expanduser("~/.agents/test-venv/bin/python3")
    eda = os.path.expanduser("~/.agents/data-eda.py")
    subprocess.run([venv_py, eda, path])

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    cmd = a[0]
    if cmd == "list":
        for slug, (name, domain, url, note) in DATASETS.items():
            mark = "OK " if downloaded(slug) else "  "
            print(f"{mark}{slug:<22} [{domain}] {name}")
        print(f"\n{len(DATASETS)} dataset; unduh: data-hub get <slug>")
    elif cmd == "search":
        q = " ".join(a[1:]).lower()
        for slug, (name, domain, url, note) in DATASETS.items():
            if q in slug or q in name.lower() or q in note.lower() or q in domain:
                print(f"- {slug} [{domain}] {note[:70]}")
        # Cari juga di indeks besar (HF/OpenML/Zenodo — metadata saja)
        idb = os.path.expanduser("~/.agents/datasets-index.db")
        if os.path.exists(idb):
            import sqlite3
            try:
                ic = sqlite3.connect(idb)
                rows = ic.execute(
                    "SELECT d.source,d.slug,d.name,d.downloads FROM ds d "
                    "JOIN ds_fts f ON d.rowid=f.rowid "
                    "WHERE ds_fts MATCH ? ORDER BY d.downloads DESC LIMIT 8",
                    ('"' + '" OR "'.join(q.split()) + '"',)).fetchall()
                if rows:
                    print("\n-- indeks besar (metadata; fetch: data-hub get hf:<slug> / zenodo:<id> / openml:<id>) --")
                    for src, slug, name, dl in rows:
                        print(f"- {src}:{slug} ⬇{dl} {name[:60]}")
            except Exception:
                pass
    elif cmd in ("peek", "eda"):
        rest = [x for x in a[1:] if x != "--info"]
        peek(rest[0])
    elif cmd == "get":
        rest = [x for x in a[1:] if x != "--info"]
        get(rest[0], "--info" in a)
    else:
        sys.exit(f"perintah tidak dikenal: {cmd}")

if __name__ == "__main__":
    main()
