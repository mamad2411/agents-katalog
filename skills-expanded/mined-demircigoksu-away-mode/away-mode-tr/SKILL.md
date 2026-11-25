---
name: away-mode-tr
description: Kullanıcı klavye başında değilken (uyurken, toplantıdayken, seyahatteyken) bir görev dosyasındaki işleri baştan sona, soru sormadan, doğrulayarak tamamlar. Use when the user says they will be away/asleep/offline and hands over a task file (gorev.md, tasks.md, todo.md, backlog.md ...) to be finished autonomously. Tetikleyiciler "ben uyuyorum", "sana tüm yetkiyi veriyorum", "ben yokken hallet", "bana sorma", "otomatik tamamla", "klavyeden uzaktayım", "work while I'm asleep", "autonomous run", "don't ask me anything".
---

# Away Mode: Kullanıcı yokken işi bitiren otonom akış

## Amaç

Kullanıcı klavyeden uzaktayken, bir görev dosyasındaki tüm işleri sırayla
tamamlamak, her adımı **doğrulamak** ve dönüşünde tek bir devir raporu
bırakmak. Soru sormak yasaktır; karar vermek zorunludur.

## Değişkenler (her çalıştırmada yeniden çözülür)

Bunları kullanıcının mesajından ve görev dosyasından çıkar. Hiçbiri sabit
değildir; hiçbirini sormak için durma.

| Değişken | Ne demek | Bulunamazsa varsayılan |
|---|---|---|
| `TASK_FILE` | Görev dosyası (gorev.md, tasks.md, todo.md, sprint.md, bir Notion/Drive sayfası, hatta mesajın kendisi) | Bağlı klasörlerde `gorev*.md`, `task*.md`, `todo*.md`, `backlog*.md` ara; tek aday varsa onu kullan |
| `TASK_COUNT` | Kaç iş var (7, 3, 12, "hepsi") | Dosyadan sayılan madde sayısı |
| `AWAY_MODE` | Kullanıcının durumu: uyuyor / toplantıda / seyahatte / sadece "yok" | `away` (etkileşimsiz kabul et) |
| `AWAY_WINDOW` | Ne kadar süre yok (gece boyu, 2 saat, belirsiz) | Belirsiz: akışı süresiz sürdürülebilir kur |
| `PROJECT_ROOT` | İşin yapılacağı kod/dosya kökü | Görev dosyasının bulunduğu klasör |
| `VERIFY_TARGETS` | Neyin doğrulanacağı: sunucu, veritabanı, API, build, test, canlı sayfa | Görev dosyasından çıkar; en az bir uçtan uca kontrol zorunlu |
| `RESUME_POLICY` | Oturum kesilirse ne olacak | Zamanlanmış görev ile kaldığı yerden devam |

`TASK_COUNT` bir hedef değil, bir **kontrol toplamıdır**. Dosyadan çıkan iş
sayısı kullanıcının söylediğinden farklıysa, farkı raporda yaz ve dosyadaki
sayıyla devam et.

## Akış

### 0. Bağlam topla (soru sorma)

1. `TASK_FILE`'ı bul ve tamamını oku. Bulamazsan: bağlı klasörleri, cihaz
   köprüsünü (`device_bash` / Desktop Commander) ve yüklenen dosyaları tara.
   Yine yoksa `references/degisken-cozumleme.md` içindeki "dosya yok"
   protokolünü uygula: kullanıcının mesajındaki işleri bir görev dosyasına
   sen yaz, öyle devam et.
2. Proje bağlamını oku: `README`, `CLAUDE.md`, `AGENTS.md`, `docker-compose.yml`,
   `.env.example`, migration klasörü, deploy scriptleri.
3. Kalıcı hafızayı oku (`memory_list` + ilgili dosyalar). Kullanıcının stack'i,
   sunucuları, alışkanlıkları burada olabilir.
4. Önceki oturumdan kalan `ilerleme.json` varsa oku ve **kaldığı yerden** devam et.

### 1. Durum dosyasını kur

`PROJECT_ROOT/.away-mode/ilerleme.json` oluştur (şema: `assets/ilerleme.schema.json`).
Her iş için: `id, baslik, durum, dogrulama, kanit, varsayimlar, notlar`.
Bu dosya tek gerçek kaynaktır. Her iş bittiğinde **hemen** güncelle; oturum
düşerse buradan devam edilir.

Aynı anda `TaskCreate` ile görünür bir görev listesi aç: her iş bir madde,
artı sondaki "uçtan uca doğrulama" ve "devir raporu" maddeleri.

### 2. Her iş için tek tip döngü

`references/calisma-dongusu.md` ayrıntılı hali. Özet:

```
OKU  ->  PLANLA  ->  UYGULA  ->  DOĞRULA  ->  KANIT KAYDET  ->  DURUMU YAZ
                        ^                          |
                        +------- düzelt <----------+   (en fazla 3 tur)
```

- **UYGULA**: değişiklikleri kaynağın yanında yap. Kullanıcının dosyalarını
  yerinde düzenle (`sed -i`, kısa script), tool çıktısından yeniden yazma.
- **DOĞRULA**: iddia etme, kanıtla. Kod çalıştı demek yetmez; sonucu okuyan
  bir sorgu/istek çalıştır.
- 3 turda düzelmeyen iş `bloke` işaretlenir, sebebi ve denenenler yazılır,
  **diğer işlere geçilir**. Bir iş yüzünden akış durmaz.

### 3. Sunucu ve veritabanı doğrulaması (zorunlu)

Bir iş "yapıldı" sayılmaz; **sunucu tarafındaki kalıcı durum** değişmedikçe.
Her iş için uygun olanı çalıştır ve çıktısını kanıt olarak sakla:

- Şema değişikliği: migration gerçekten koştu mu (`alembic current`,
  `prisma migrate status`, `\d tablo`, `information_schema` sorgusu).
- Veri değişikliği: `SELECT` ile satır sayısı / örnek satır, öncesi ve sonrası.
- API: canlı endpoint'e istek at, dönen gövdeyi kaydet (200 yetmez, içerik bak).
- Uygulama: container ayakta mı, log'da hata var mı (`docker compose ps`, `logs --tail`).
- Cache/CDN: değişiklik gerçekten yayında mı.

Ayrıntı ve hazır komutlar: `references/dogrulama.md`.
Yazma işleminden önce yedek al: `references/dogrulama.md#yedekleme`.

### 4. Soru sorma, karar ver ve kaydet

`AWAY_MODE` etkinken `AskUserQuestion` kullanılmaz. Belirsizlikte:

1. Görev dosyasındaki ifadeyi birebir esas al.
2. Projedeki mevcut örüntüyü taklit et (aynı isimlendirme, aynı katman).
3. Geri alınabilir olanı seç.
4. Seçimi `ilerleme.json` -> `varsayimlar` alanına tek cümle yaz ve raporda göster.

**Tek istisna, geri alınamaz işler.** Görev dosyası açıkça izin vermiyorsa
şunlar yapılmaz, hazırlanır ve raporda onaya bırakılır: prod veri silme,
`DROP`/`TRUNCATE`, geri dönüşü olmayan migration, dış dünyaya e-posta/mesaj
gönderme, ödeme, DNS/domain değişikliği, force push, yedeksiz üzerine yazma.
Bunların yerine script'i yaz, dry-run çıktısını üret, raporda "onayınla tek
komut" olarak sun.

### 5. Akışı sürdür (kullanıcı hâlâ yokken)

Oturum uzun sürecekse veya kesilebilecekse akışı kendi kendine devam ettir:

- Uzun işlerde `send_later` / `ScheduleWakeup` ile kendine dönüş planla.
- Oturum tamamen kapanabiliyorsa `create_trigger` ile **kaldığı yerden devam
  eden** bir zamanlanmış görev kur; prompt'u tek başına anlaşılır yaz ve
  `ilerleme.json` yolunu içine göm. Yerel cron araçlarını kullanma.
- Tüm işler bitince zamanlanmış görevi `delete_trigger` ile kapat.

Şablon prompt: `references/devam-tetikleyici.md`.

### 6. Devir raporu

Bitince (veya kullanıcı döndüğünde) tek bir rapor bırak:
`PROJECT_ROOT/DEVIR-RAPORU.md`, şablon `assets/devir-raporu-sablonu.md`.

İçinde: iş iş durum tablosu, her iş için **kanıt** (komut + çıktı özeti),
verilen kararlar/varsayımlar, bloke kalanlar ve sebebi, onay bekleyen geri
alınamaz işler, ve "sen uyanınca yapılacak 3 şey" listesi.

Raporu hem dosya olarak teslim et (`SendUserFile` + bağlı klasöre yaz) hem de
sohbette 5 satırlık özetini ver. Uzun anlatım yok, tablo ve kanıt.

## Bitiş ölçütü

Her iş için: `durum = tamam` **ve** `kanit` dolu **ve** doğrulama sunucu
tarafında koşmuş. Bunlardan biri eksikse iş `tamam` yazılmaz.

## Referanslar

- `references/degisken-cozumleme.md` - değişkenleri bulma ve dosya yoksa ne yapılacağı
- `references/calisma-dongusu.md` - iş başına döngü, hata ve bloke yönetimi
- `references/dogrulama.md` - sunucu/DB/API doğrulama komutları ve yedekleme
- `references/devam-tetikleyici.md` - oturum kesilirse akışı sürdürme
- `assets/gorev-sablonu.md` - kullanıcıya verilecek görev dosyası şablonu
- `assets/ilerleme.schema.json` - durum dosyası şeması
- `assets/devir-raporu-sablonu.md` - rapor şablonu
