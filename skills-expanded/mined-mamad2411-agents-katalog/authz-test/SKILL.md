---
name: authz-test
description: Builds the attacker-perspective authorization test matrix (IDOR, broken object-level authorization, tenant leakage, Supabase RLS bypass) that ordinary unit tests never cover, and verifies it against the real running system. Use when a task touches per-user or per-tenant data, any endpoint with an id in the path/query, or a Supabase table with RLS. Specifies tests for `test-copilot` to author and runs live probes itself; never writes implementation code.
---

# authz-test — "başkasının verisini çekebiliyor muyum?" katmanı

## Kullanılacak destek skiller
- `caveman`, `ponytail` (full) — her zaman aktif.
- `supabase-check` — Supabase tablosu varsa migration/gerçek-istek doğrulaması onda.

## Neden var
Test piramidinde bu katman yoktu. Mevcut testler hep **doğru kullanıcının doğru
veriye eriştiğini** doğruluyor. Gerçek dünyada en sık açık bunun tersi:
**yanlış kullanıcının doğru veriye erişmesi** — IDOR / broken object-level
authorization. OWASP API Top 10'un bir numarası budur ve mock'lu birim testler
onu yapısal olarak göremez, çünkü mock zaten "izin var" der.

`supabase-check` bunun yarısını kapatıyordu: migration uygulandı mı, gerçek
istek çalışıyor mu. Ama "anon key ile başkasının satırını çekebiliyor muyum"
**saldırgan testini** atmıyordu. Bu skill onu ekler.

## Ne zaman çalışır
`threat-model` bir `AC-S` yetkilendirme kriteri ürettiyse, ya da değişiklik
şunlardan birine dokunuyorsa: yol/sorguda id taşıyan uç (`/users/{id}`),
kullanıcıya veya kiracıya ait tablo, rol/izin kontrolü, paylaşım-davet akışı,
RLS politikası.

## Test matrisi — her korunan kaynak için

En az iki **farklı** aktör gerekir. Tek kullanıcıyla yetkilendirme test edilemez.

| # | Aktör | Beklenen |
|---|---|---|
| 1 | Sahibi (A) | 200 + kendi verisi |
| 2 | **Başka kullanıcı (B)** | 403 veya 404 — gövdede A'nın **hiçbir alanı** olmamalı |
| 3 | Kimliksiz / anon key | 401/403 — boş liste değil |
| 4 | Süresi geçmiş / bozuk token | 401 |
| 5 | Rol yükseltme denemesi (istekte `role: admin`) | yok sayılır, sunucu kendi kaydına bakar |
| 6 | Başkasının id'siyle yazma/silme | 403/404 **ve** veri değişmemiş olmalı |

### İki kural
- **Boş liste geçmek değildir.** RLS'te en tehlikeli sonuç `200 + []`'dir:
  test "veri sızmadı" diye geçer, oysa sorgu yetkisizdi ve sessizce filtrelendi
  — politika değişince sızmaya başlar. Yetkisiz erişim **hata** dönmeli.
- **Yazma testinde son durumu doğrula.** `403` dönüp kaydı yine de değiştiren
  uçlar olur. Cevap kodu yetmez; kaydı tekrar oku.

## Nasıl yürütülür

1. **Testleri sen yazma.** Yukarıdaki matrisi `test-copilot`'a
   `extra_instructions` olarak ver — boru hattının kuralı: test dosyalarını
   yalnızca `test-copilot` yazar. Her satırı `AC-S<n>`'e bağla.

2. **Mock'a izin verme.** Yetkilendirme testi mock'lanırsa hiçbir şey
   kanıtlamaz. Bu testler gerçek istemciye/DB'ye gitmeli (test projesi, test
   kullanıcıları). Mock'lu bir authz testi gördüğünde FAIL raporla.

3. **Canlı sonda (senin işin).** İki gerçek test hesabı varsa, matrisin
   2. ve 3. satırını gerçek istekle kendin doğrula ve çıktıyı rapora koy.
   Bu doğrulamadır, kod yazımı değil — izin verilen iş.

> Canlı sonda gerçek bir sisteme istek atar. Yalnızca **kullanıcının kendi
> test/geliştirme ortamında** ve kullanıcı bu görevi onayladıysa çalıştır.
> Üretim ortamına, ya da kullanıcının sahibi olmadığı bir sisteme asla.

## Supabase'e özel
- RLS **açık mı** kontrol et: politikası olmayan tabloda RLS kapalıysa anon key
  her satırı okur. Tablo bazında doğrula.
- `service_role` anahtarı istemci tarafı koda **hiç** girmemeli —
  `security-scan`'in sızıntı gate'i bunu ayrıca arar.
- `anon` key ile 2. ve 3. satır sondasını gerçekten at: `200 + []` gördüysen
  bunu PASS sayma, politika filtreliyor mu yoksa veri mi yok ayırt et.

## Raporlama
`obss_project/artifacts/<task-slug>/authz_test.md`: matris tablosu, her satır
için PASS/FAIL/N-A + kanıt (durum kodu, gövde özeti), mock'lanan test varsa
ayrıca işaretle. Kapsanmayan satır varsa **eksik** de, "uygulanmadı" deme.

## Yapmayacakların
- Uygulama kodu veya test dosyası yazmaz (`code-copilot` / `test-copilot`).
- Bulduğu açığı kendi başına düzeltmez — raporlar.
- Üretim ortamına sonda atmaz.
