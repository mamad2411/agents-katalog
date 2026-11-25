# 16 — Data, database, migrasi, dan ML

## 1. Migrasi database
Wajib sebelum merge:
- [ ] Migrasi **up dari database kosong** berhasil (bukan hanya dari DB dev yang sudah ada).
- [ ] Migrasi **down/rollback** berhasil, atau dinyatakan irreversible + rencana restore.
- [ ] Data lama tetap terbaca (backfill/dual-write bila perlu).
- [ ] Migrasi tidak mengunci tabel besar (`ALTER TABLE ... ADD COLUMN DEFAULT` hati-hati).
- [ ] Idempoten: dijalankan 2× tidak gagal.
- [ ] Uji waktu: estimasi durasi pada ukuran data produksi.
- [ ] Setelah migrasi: constraint/FK/unique benar-benar menolak data salah.

```bash
# postgres: ukur dampak sebelum produksi
psql "$URL" -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ...;"
# uji up-down-up pada DB bersih (pakai container)
docker run --rm -e POSTGRES_PASSWORD=dev -p 55432:5432 -d postgres:16-alpine
```

## 2. Integritas data
| Uji | Caranya |
|---|---|
| Constraint | insert duplikat/invalid → harus gagal (bukan diam-diam) |
| Transaksi | gagal di langkah 3 dari 5 → tidak ada data separuh |
| Konkurensi | 2 transaksi ubah baris sama → 1 menang / serialization error, bukan lost update |
| Isolasi level | uji `READ COMMITTED` vs `REPEATABLE READ` sesuai kebutuhan |
| Soft delete | filter default konsisten di semua query |
| Orphan | hapus parent → child ikut (cascade) atau ditolak |
| Encoding | emoji & unicode tersimpan utuh (utf8mb4) |
| Timezone | simpan UTC, tampilkan lokal; uji DST |
| Backup/restore | restore ke DB baru, bandingkan jumlah baris + checksum kolom kunci |

```bash
pg_dump "$URL" -Fc -f bak.dump && createdb uji && pg_restore -d uji bak.dump
psql uji -c "select count(*) from items;"    # bandingkan dengan sumber
```

## 3. ETL / pipeline data
- Schema contract: nama/tipe/nullable kolom; tolak perubahan tak terduga.
- Data quality: nol/duplikat/outlier/rentang tanggal/data hilang → metrik per run.
- Idempoten: jalankan ulang partisi yang sama → tidak menggandakan.
- Incremental vs full: hasil akhir harus identik (bandingkan checksum).
- Late/duplicate event, zona waktu, backfill, skema berubah di tengah jalan.
- Alat: `pandera`/`great_expectations`/`dbt tests`/`soda` (pilih yang tersedia).

## 4. ML / model
| Aspek | Uji minimum |
|---|---|
| Holdout | metrik pada data uji yang tidak pernah dilihat (bukan train) |
| Baseline | bandingkan dengan baseline naif (mayoritas/last value) |
| Robustness | input kosong, ekstrem, bahasa lain, teks panjang, gambar rusak |
| Fairness | metrik per segmen (gender/wilayah/usia) tidak jauh berbeda |
| Kalibrasi | probabilitas masuk akal (reliability curve) |
| Drift | distribusi fitur & output dibanding data pelatihan (PSI/KL) |
| Reproducible | seed, versi data & dependency tercatat; training ulang → hasil sama |
| Latensi | p95 inferensi sesuai anggaran; batch vs realtime |
| Regresi | prompt/model version baru tidak menurunkan metrik (golden set kecil) |
| Keselamatan | prompt injection, output berbahaya, PII bocor di jawaban |

Aturan: jangan pernah mengevaluasi model pada data latih; jangan laporkan akurasi tanpa
ukuran sampel dan interval kepercayaan.

## 5. Data uji & privasi
- Generator + seed (Faker) untuk volume; anonimisasi untuk bentuk realistis.
- Subset produksi hanya setelah PII dihapus/hash — catat prosesnya.
- Ukuran uji: 0 baris, 1 baris, 1 juta baris (pagination & performa).
- Unicode, emoji, RTL, newline di field teks; NULL vs string kosong.

## 6. Definition of Done data
- [ ] Migrasi up/down diuji pada DB bersih (log terlampir).
- [ ] Ada test integritas (constraint + transaksi + konkurensi).
- [ ] Backup & restore dibuktikan (bukan diasumsikan).
- [ ] Query baru punya `EXPLAIN` dan tidak `Seq Scan` pada tabel besar.
- [ ] Untuk ML: metrik holdout + baseline + segmen + drift tercatat.
