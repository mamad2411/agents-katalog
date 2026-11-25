---
name: gorsel-uret
description: "Ortak GPU makinesine sprite/gorsel uretim istegi birak, sirasini takip et, sonucu indir. Sadece HTTP — kurulum, repo ya da GPU gerekmez. Triggers: gorsel uret, resim uret, sprite uret, ikon uret, karakter gorseli, sahne gorseli, image generate, gorsel api, kuyruga ekle, anim_image_jobs."
user-invocable: true
---

# Görsel üret — ortak GPU kuyruğuna istek bırak

Sprite, karakter, sahne ya da ikon görseli üretmek için. Üretimi başka bir
makinedeki RTX 5080 yapıyor; sen sadece **istek bırakıyorsun**.

**Kurulum yok.** Repo klonlamak, model indirmek, GPU'n olması gerekmiyor.
Tek ihtiyaç `curl` (ya da herhangi bir HTTP istemcisi).

**Makine kapalıyken de istek bırakılabilir.** İstek kuyruğa yazılır, GPU
makinesi açılınca sırayla üretir. Beklemene gerek yok — işi aç, sonra
durumunu sor.

Web arayüzü tercih edersen: https://animation-review-phi.vercel.app →
**Görsel üret** sekmesi. Aynı kuyruğa yazıyor.

---

## Bağlantı

```bash
API=https://arngdwwjjopmggixakez.supabase.co/rest/v1
ANON=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFybmdkd3dqam9wbWdnaXhha2V6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM3MzM4MjUsImV4cCI6MjA5OTMwOTgyNX0.lLOjQed_JkZwWCSd7w-h6Ph5xbc9gBtnZsz_3XEN0mw
AUTH=(-H "apikey: $ANON" -H "Authorization: Bearer $ANON")
```

Anahtar herkese açık olacak şekilde tasarlandı (yayınlanan sayfanın içinde de
duruyor). Güvenlik satır bazlı izinlerde: dışarıdan yalnızca bekleyen iş
açılabilir ve iptal edilebilir. `status: "done"` göndermek **401** ile
reddedilir — üretimi yalnızca GPU makinesi bitirebilir.

## 1. İş aç

```bash
JID="ij_$(date +%s)_$RANDOM"
curl -X POST "$API/anim_image_jobs" "${AUTH[@]}" \
  -H "Content-Type: application/json" \
  -d "{\"id\":\"$JID\",\"ad\":\"kilic-ikonu\",\"sinif\":\"karakter\",
       \"prompt\":\"a knight sprite, side view, black background\",
       \"negative\":\"blurry, watermark, text\",
       \"params\":{\"adet\":2,\"genislik\":1024,\"yukseklik\":1024,\"tohum\":0},
       \"status\":\"pending\",\"requested_by\":\"$USER\"}"
```

**Prompt İngilizce yazılır.** Türkçe prompt çıktı kalitesini düşürüyor —
ölçüldü, bu ekosistemde tekrar eden bir hata.

`params.tohum` 0 ise rastgele seçilir ve **kullanılan tohum sonuca yazılır**.
Tohumsuz bir görsel yeniden üretilemez; "bunu tekrar yap" bu hattın en sık
isteği.

## 2. Takip et

```bash
curl "$API/anim_image_jobs?id=eq.$JID&select=status,error" "${AUTH[@]}"
```

`pending` → `claimed` → `done` / `failed`

**`failed` görünce `error` alanını oku.** Sebep oraya yazılıyor; tahmin etme,
log arama, kimseye sorma. Kapalı bir sınıfa istek açtıysan sebep orada yazar.

## 3. Sonucu al

```bash
curl "$API/anim_image_results?job_id=eq.$JID&select=url,tohum,genislik,model" "${AUTH[@]}"
```

`url` doğrudan indirilebilir:

```bash
curl -sO "$(curl -s "$API/anim_image_results?job_id=eq.$JID&select=url" "${AUTH[@]}" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["url"])')"
```

## 4. Referanslı üretim — "buna benzesin"

Önce referansı yükle:

```bash
YOL="sources/$(date +%s)_ref.png"
curl -X POST "https://arngdwwjjopmggixakez.supabase.co/storage/v1/object/animations/$YOL" \
  "${AUTH[@]}" -H "Content-Type: image/png" --data-binary @ref.png
```

Sonra işi açarken `"referanslar": ["'$YOL'"]` ekle.

En fazla 3 referans, yol **`sources/` ile başlamak zorunda**. Referanslı kipte
stil o görsellerden alınır (Qwen-Image-Edit kullanılır).

> **Boş bıraktığın her şey referanstan kopyalanır.** Neyin değişmesini
> istiyorsan açıkça yaz; genel bir prompt referansı yeniden üretir.

## 5. Bekleyen işi iptal et

```bash
curl -X DELETE "$API/anim_image_jobs?id=eq.$JID" "${AUTH[@]}"
curl "$API/anim_image_jobs?id=eq.$JID&select=id" "${AUTH[@]}"   # boş dönmeli
```

Yalnızca `pending` iş silinebilir. **Başarı kodu (204) silindiği anlamına
gelmez** — izin verilmeyen bir silme isteği hata yerine "0 satır etkilendi"
döndürüyor, yani yine 204 alırsın. Bu ekosistemde ölçüldü: 82 silme denemesi
başarılı göründü ve hiçbiri silmedi. İkinci satırdaki doğrulama sorgusu bu
yüzden var — boş dizi dönmeliyse gerçekten silinmiştir.

---

## Sınıflar

| sınıf | varsayılan boyut | durum |
|---|---|---|
| `karakter` | 1024×1024 | ✅ çalışıyor |
| `sahne` | 720×960 | ✅ çalışıyor |
| `ikon` | 1024×1024 | ⛔ kapalı |
| `yazili` | 1024×1024 | ⛔ kapalı |

Kapalı sınıf bir arıza değil: hangi modelin o işi iyi yaptığı ölçülmeden
üretime açılmıyor. İstek açarsan `failed` döner ve sebebi `error`'da yazar.
İhtiyacın varsa **hat sahibine söyle**, ölçüm yapılıp açılır.

## Süre — ne beklemeli

RTX 5080'de ölçüldü, 1024×1024 `karakter`:

```
ilk görsel (model yükleme dahil)   23.7 sn
sonraki her görsel                  8.4 sn   (9 üretimde sapma yok)
10 görsellik parti                 99.4 sn
```

Ama **sıra video üretimiyle paylaşımlı** ve ikisi aynı anda karta sığmıyor.
Bu yüzden işler öbek hâlinde çalışıyor:

- resim üretiliyorsa → resim kuyruğu **boşalana kadar** devam
- video üretiliyorsa → **10 resim birikmeden** kesilmez
- video kuyruğu boşsa → tek resim için bile resme geçilir

Yani tek bir acil resim isteğin çalışan video kuyruğunu kesmez; sırada
bekleyebilir. Acilse hat sahibinden elle "resme geç" demesini iste.

## Kurallar

- **Prompt İngilizce.**
- **`status` her zaman `"pending"`.** Başka değer 401.
- **`adet` en fazla 10.** Fazlası için birden çok iş aç.
- **Kendi `id`'ni üret, benzersiz olsun** (`ij_` öneki). Çakışırsa reddedilir.
- **Referans yolu `sources/` altında.**
- **Üretilen dosyalar herkese açık bağlantıda.** Gizli içerik gönderme.

## Sorun bildirme

İş kimliği, sınıf, prompt ve `error` metnini yaz. Aynı bilgiler web
arayüzündeki kuyruk listesinde de görünüyor.

## İlgili

- **[/animate](../animate/SKILL.md)** — üretilen görseli sprite animasyonuna çevir
- **[/reference-style](../reference-style/SKILL.md)** — referanstan stil aktarımı kuralı
