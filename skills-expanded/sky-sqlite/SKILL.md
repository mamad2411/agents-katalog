---
name: sky-sqlite
description: >-
  SQLite'ı üretimde ve uygulamalarda kullanma: ne zaman yeterli (çoğu zaman sanıldığından
  fazla), WAL modu ve doğru PRAGMA ayarları, tek yazıcı modeli ve eşzamanlılık, Turso/libSQL ve
  Cloudflare D1 ile dağıtık SQLite, Litestream ile sürekli yedek, Drizzle/better-sqlite3/
  bun:sqlite kullanımı, FTS5 tam metin arama, JSON fonksiyonları, gömülü uygulamalar
  (masaüstü, mobil, tarayıcı — OPFS/WASM) ve sınırlar. SQLite kullanırken kullan.
disable-model-invocation: true
---

# Sky · SQLite

## Ne zaman yeterli?

Tek sunuculu web uygulaması, okuma ağırlıklı, saniyede yüzlerce (hatta binlerce) yazma — SQLite rahatça taşır; ağ gecikmesi yok, işletme yükü yok.
Yetmediği yerler: birden çok uygulama sunucusunun aynı DB'ye **yazması**, çok yüksek eşzamanlı yazma, DB'ye doğrudan dış erişim gereksinimi.

## Doğru ayarlar (en önemli kısım)

```sql
PRAGMA journal_mode = WAL;          -- okuyucular yazıcıyı bloklamaz
PRAGMA synchronous = NORMAL;        -- WAL ile güvenli ve hızlı
PRAGMA busy_timeout = 5000;         -- kilit beklerken hemen "database is locked" hatası verme
PRAGMA foreign_keys = ON;           -- varsayılan KAPALI!
PRAGMA cache_size = -64000;         -- ~64MB önbellek
PRAGMA temp_store = MEMORY;
```
Her bağlantı açılışında uygula (journal_mode kalıcıdır, diğerleri bağlantı başına).
Yazma işlemlerini `BEGIN IMMEDIATE` ile başlat (deadlock yerine bekleme). Uzun işlem tutma; yazmaları kısa ve toplu yap.

## Kütüphaneler

- Node: **better-sqlite3** (senkron, çok hızlı) veya Node 22+ yerleşik `node:sqlite`; Bun: `bun:sqlite`.
- ORM: **Drizzle** (`drizzle-orm/better-sqlite3`, `drizzle-orm/libsql`, `drizzle-orm/d1`).
- Python: `sqlite3` stdlib / SQLAlchemy; Go: `modernc.org/sqlite` (CGO'suz) veya `mattn/go-sqlite3`.

## Dağıtık / sunucusuz SQLite

- **Turso / libSQL**: SQLite uyumlu, uzaktan erişim, gömülü replikalar (uygulama içinde yerel kopya, okumalar mikro saniye), çoklu DB (kiracı başına bir DB).
- **Cloudflare D1**: Workers ile (bkz. `sky-cloudflare`).
- **LiteFS** (Fly): birden çok sunucuya replikasyon, tek birincil yazıcı.

## Yedek

**Litestream**: WAL'ı sürekli S3/R2'ye akıtır, saniyeler mertebesinde kayıp, tek komutla geri yükleme — tek sunuculu SQLite'ı üretime güvenle taşımanın anahtarı.
Anlık kopya: `sqlite3 app.db ".backup backup.db"` veya `VACUUM INTO 'backup.db'` (çalışan DB'yi `cp` ile kopyalama — tutarsız olabilir).

## Özellikler

- **FTS5** tam metin arama: `create virtual table posts_fts using fts5(title, body, content='posts', content_rowid='id', tokenize='unicode61 remove_diacritics 2');`
  (`remove_diacritics` → "cagri" ile "Çağrı" eşleşir — Türkçe için faydalı, ı/İ için ek normalizasyon gerekebilir, bkz. `sky-search`).
- JSON: `json_extract(data, '$.plan')`, `->>` operatörü, JSON sütunlarına generated column + indeks.
- `STRICT` tablolar (tip zorlaması), `WITHOUT ROWID` (bileşik anahtarlı tablolar), `RETURNING`.
- Tarih: ISO 8601 TEXT olarak sakla (UTC); `datetime('now')`.

## Gömülü uygulamalar

- Masaüstü (Tauri sql eklentisi, Electron better-sqlite3), mobil (expo-sqlite, drift, SwiftData altında da SQLite).
- Tarayıcı: SQLite WASM + **OPFS** (kalıcı, hızlı) — çevrimdışı-önce uygulamalar; senkron için ElectricSQL / PowerSync / cr-sqlite gibi çözümler.

## Migration

Drizzle Kit / sqlx / Alembic çalışır; SQLite `ALTER TABLE` sınırlı (sütun silme/yeniden adlandırma yeni sürümlerde var, tip değişikliği yok) →
araçlar tabloyu yeniden oluşturarak yapar; büyük tablolarda zamanla. Testlerde `:memory:` veritabanı çok hızlıdır.
