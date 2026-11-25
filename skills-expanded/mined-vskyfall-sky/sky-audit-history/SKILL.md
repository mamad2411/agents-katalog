---
name: sky-audit-history
description: >-
  Değişiklik geçmişi ve denetim: audit log tasarımı (kim, ne, ne zaman, nereden), alan bazlı
  önce/sonra farkı, kayıt versiyonlama ve "eski sürüme dön", geri al (undo) kalıpları, etkinlik
  akışı (activity feed) UI, Postgres trigger ile otomatik geçmiş, event sourcing ne zaman,
  saklama ve performans. "Kim değiştirdi", "geçmiş", "eski haline getir", "aktivite akışı",
  "audit log" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Geçmiş & Denetim

## Üç farklı ihtiyaç

| İhtiyaç | Çözüm |
|---|---|
| Güvenlik/uyum: "kim neyi ne zaman yaptı?" | **Audit log** (append-only) |
| Kullanıcı: "bu kaydın geçmişi", "eski sürüme dön" | **Kayıt versiyonlama** |
| Kullanıcı: "az önce yanlışlıkla sildim" | **Geri al (undo)** — toast + soft delete |
| Ekip: "bugün neler oldu?" | **Etkinlik akışı** (audit'ten türetilmiş, okunabilir) |

## Audit log

```
audit_logs  id, org_id, actor_type (user|api_key|system|ai_agent), actor_id, action, target_type, target_id,
            changes jsonb, ip_trunc, user_agent, request_id, created_at
```
- `action`: `booking.cancelled`, `member.role_changed`, `export.created`, `api_key.created`.
- `changes`: `{ "status": ["confirmed", "cancelled"], "note": ["…", "…"] }` (yalnızca değişen alanlar).
- **Append-only**: uygulama rolünün UPDATE/DELETE izni yok; saklama süresi politikası (bkz. `sky-privacy-engineering`).
- Servis katmanında tek `audit()` çağrısı; ya da kritik tablolarda Postgres trigger ile otomatik.

```sql
create function audit_trigger() returns trigger language plpgsql as $$
begin
  insert into audit_logs(org_id, actor_id, action, target_type, target_id, changes, created_at)
  values (coalesce(new.org_id, old.org_id), nullif(current_setting('app.user_id', true), '')::uuid,
          tg_table_name || '.' || lower(tg_op), tg_table_name, coalesce(new.id, old.id),
          jsonb_build_object('old', to_jsonb(old), 'new', to_jsonb(new)), now());
  return coalesce(new, old);
end $$;
```
İstek başında `set local app.user_id = '…'` ile aktör bilgisi trigger'a taşınır.

## Kayıt versiyonlama

```
document_versions  id, document_id, version int, data jsonb, author_id, summary, created_at
```
- Her kayıtta yeni sürüm satırı (veya her N dakikada birleştir — otomatik kayıtta her tuşa sürüm olmasın).
- UI: sağda "Sürüm geçmişi" paneli — tarih, yazar avatarı, "Bu sürüme dön", **diff görünümü**
  (eklenen yeşil, silinen kırmızı; `diff` / `jsondiffpatch`). Google Docs hissi — insanlar bayılır.
- "Geri dön" yeni bir sürüm oluşturur (geçmiş silinmez).
- Sürümlere isim verme ("Müşteriye gönderilen hali").

## Geri al (undo)

- Silme/arşivleme/toplu işlem → hemen uygula + toast "3 randevu silindi · **Geri al**" (6–8 sn).
- Arka planda soft delete (`deleted_at`); geri al = `deleted_at = null`. Kalıcı silme 30 gün sonra iş ile.
- Onay diyaloğundan çok daha iyi UX (bkz. `sky-ux-writing`). Geri alınamayan işlemler (gönderilen SMS) için onay.
- Klavye: `⌘Z` uygulama içi son işlemi geri alır (editör dışında).

## Etkinlik akışı (activity feed)

- Audit kayıtlarından insan diline: "**Ayşe** randevuyu iptal etti · Mehmet Yılmaz, 5 Kas 14:30 · 2 dk önce".
- Kayıt detay sayfasında zaman çizelgesi (oluşturuldu → düzenlendi → ödeme alındı → tamamlandı), yorumlarla karışık.
- Gruplama: "Ayşe 12 randevu ekledi" (aynı aktör, aynı işlem, kısa sürede).
- Filtre: kişi, işlem türü, tarih.
- Gerçek zamanlı güncelleme isteğe bağlı (bkz. `sky-realtime`).

## Event sourcing ne zaman?

Durumun tamamen olaylardan türetildiği sistemler (muhasebe defteri, cüzdan bakiyesi, stok hareketleri) —
"bakiye = tüm hareketlerin toplamı". Çoğu CRUD uygulaması için gereksiz karmaşıklık; audit log + versiyonlama yeter.
Para/stok için yine de **hareket tablosu** (ledger) tut, bakiyeyi türet veya senkron tut.

## Performans

- Audit tablosu hızla büyür: `(org_id, created_at desc)` ve `(target_type, target_id)` indeksleri; aylık partition.
- Eski kayıtları soğuk depolamaya (S3'e parquet/JSON) taşı.
- Okuma yolunda audit yazımı istek süresini uzatmasın — kritik değilse kuyruğa at.
