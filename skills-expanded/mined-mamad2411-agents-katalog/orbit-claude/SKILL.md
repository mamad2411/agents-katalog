# AGENT.md — Orbit

> **İsim kesinleşti: `orbit`.** (Portlar/process'ler yörüngede, tema kozmik.)
> npm'de müsaitlik yayından önce doğrulanmalı.

macOS'ta aynı anda çalışan birden fazla lokal geliştirme projesini tek yerden görmek,
durdurmak ve yeniden başlatmak için bir araç.

Çözdüğü problem: birden fazla proje açıkken "8080'de ne var, bu node process'i hangi
projeye ait, bunu kapatsam ne kırılır" belirsizliği.

---

## Kesinleşmiş kararlar

Bunlar tartışıldı ve karara bağlandı. Yeniden gündeme getirme, aksini önerme.

| Karar | Seçim |
|---|---|
| Hedef platform | **Sadece macOS** (v1'de Linux/Windows yok) |
| Arayüzler | v1: **CLI/TUI + web paneli**. v2: menu bar |
| Yetki | İzleme **+ durdurma + başlatma/restart** |
| Proje tanıma | **Otomatik** (process'in cwd/komutundan). Zorunlu config dosyası yok |
| Kapsam | Dev sunucuları, Docker container'ları, DB/servisler, port dinlemeyen proje process'leri |
| Dil | **Node.js + TypeScript** (ESM) |
| Çalışma modu | Tek seferlik komutlar **ve** opsiyonel arka plan daemon'ı |
| Görsel tema | **Midnight Galaxy** (theme-factory), dev-tool için uyarlanmış |
| UI kütüphanesi | **shadcn/ui** + Tailwind v4 |

---

## Mimari

Tek bir çekirdek kütüphane tüm işi yapar; arayüzler onun üstünde ince katmanlardır.
**Hiçbir arayüz doğrudan `lsof`/`ps`/`docker` çağırmaz** — her şey `core` üzerinden geçer.

```
lsof ─┐
ps   ─┼─→ core: tarayıcılar → proje çözümleyici → registry → aksiyonlar
docker┘                              │
                                     ├─→ cli    (komutlar + Ink TUI)
                                     ├─→ server (Fastify + SSE) → web (React)
                                     └─→ menubar (v2, aynı core)
```

### Paketler (pnpm workspace)

```
packages/core     tarayıcılar, proje çözümleyici, registry, aksiyonlar
packages/cli      commander + @clack/prompts + Ink TUI
packages/server   Fastify, SSE akışı, web build'ini serve eder
packages/daemon   launchd plist kurulumu/kaldırılması
apps/web          React + Vite + Tailwind + shadcn/ui
```

---

## Tech stack

**Ortak**
- Node.js 22 LTS, TypeScript, ESM
- pnpm workspaces (Turborepo bu ölçekte gereksiz)
- `tsx` (dev), `tsup` (build)
- **execa** — tüm alt process çağrıları. `child_process` kullanma; timeout ve
  process-group sinyalleri execa'da çok daha temiz
- **zod** — registry şeması ve API tipleri tek kaynaktan türer

**CLI**
- commander (argümanlar), @clack/prompts (interaktif seçim), **Ink** (TUI)

**Sunucu**
- Fastify + `@fastify/static`
- **SSE** (`text/event-stream`). WebSocket kullanma — akış tek yönlü, `EventSource`
  tarayıcıda hazır ve otomatik yeniden bağlanıyor

**Web**
- React + Vite + TypeScript
- Tailwind v4 + shadcn/ui
- Veri: SSE'den gelen tam durum snapshot'ı + `useState`. TanStack Query v1'de gereksiz

**Araçlar**
- **Vitest** — ağırlık parser testlerinde (aşağıya bak)
- **Biome** — lint + format (eslint/prettier yerine)

**Dağıtım**
- npm'e yayınla, `npx orbit` ile çalışsın
- Daemon: elle yazılmış launchd plist'i → `~/Library/LaunchAgents/`

---

## Veri toplama

Kullanılan komutlar:

```bash
lsof -nP -iTCP -sTCP:LISTEN        # port ↔ PID. -n -P şart, yoksa DNS/port çözümlemesi yavaşlatır
ps -o pid,ppid,pgid,lstart,etime,args -p <pid>   # tam komut satırı + uptime
lsof -a -p <pid> -d cwd            # process'in çalışma klasörü — proje algılamanın temeli
docker ps --format json            # container adı, imaj, port eşlemeleri
```

### Bilinen tuzaklar

- **IPv4/IPv6 çifte kayıt.** Aynı port iki satır döner. `port + pid` ile tekilleştir.
- **Docker Desktop.** Host'ta portu `com.docker.backend` dinliyor görünür. Bu kayıtları
  `docker ps` çıktısıyla eşleştir ve container olarak göster, ham process olarak değil.
- **Yetki.** `lsof` root'a ait process'lerin detayını vermez. Sessizce boş geçme;
  kullanıcıya "bu process'e erişilemedi" olarak göster.
- **Performans.** `lsof` çağrısı ~50–150ms. Panel açıkken 2sn, daemon modunda 5sn'de bir tara.

---

## Proje algılama

Her PID için:

1. `cwd`'yi al
2. Yukarı doğru `.git` ara → **repo kökü = proje kimliği**
3. İsim: `package.json`'daki `name`, yoksa klasör adı
4. Framework: komut satırı + bağımlılıklardan çıkar (next / vite / nest / django ...)
5. Aynı repo köküne düşen process'leri `pgid` ile grupla

Bir kart = bir proje. `pnpm dev → node → esbuild` zinciri tek kart altında toplanır;
kartta **en üstteki** komut gösterilir (`pnpm dev`), yaprak process değil.

---

## Registry

`~/.config/orbit/registry.json`. Atomik yaz: temp dosya → `rename`. lowdb gibi bir
bağımlılık ekleme.

```jsonc
{
  "projects": [{
    "id": "hash(repoRoot)",
    "name": "my-app",
    "path": "/Users/x/dev/my-app",
    "lastCommand": "pnpm dev",
    "lastPort": 5173,
    "lastSeen": "2026-08-03T10:00:00Z"
  }]
}
```

**Bu dosya "başlatma" özelliğinin tek dayanağı.** Otomatik algılama bir projeyi bir kez
gördüğünde komutunu ve klasörünü kaydeder; proje kapandığında listede
**"durduruldu"** olarak kalır ve tek tuşla ayağa kaldırılabilir. Hiç görülmemiş bir proje
başlatılamaz — bu bilinçli bir sınır, kullanıcıya da böyle anlat.

---

## Aksiyonlar

**Durdur** — process grubuna `SIGTERM` (`kill -TERM -<pgid>`), 5sn bekle, hâlâ ayaktaysa
`SIGKILL`. Sahibi başka kullanıcı/root ise sessizce başarısız olma, açıkça uyar.

**Başlat** — registry'deki komutu doğru `cwd` ve login shell env'i ile
`detached: true` spawn et. Çıktı → `~/.local/state/orbit/logs/<proje>.log`.
Detached olması kritik: CLI veya daemon kapanınca process ölmemeli.

**Restart** — durdur → portun serbest kalmasını bekle → başlat.

**Docker kartları** — yukarıdakiler `docker stop/start/restart <container>`'a düşer.

---

## Çalışma modları

- `orbit ls` gibi tek seferlik komutlar → `core`'u doğrudan çağırır, arka plan servisi gerekmez
- `orbit web` → sunucuyu ön planda açar
- `orbit daemon install` → launchd plist'i yazar; daemon 5sn'de bir tarar, uptime ve
  "bugün hangi portlar kullanıldı" geçmişini tutar

CLI önce daemon'ın unix socket'ini yoklar. Varsa oradan okur (tutarlı geçmiş için),
yoksa kendisi tarar. Bu fallback her komutta çalışmalı.

---

## Tasarım sistemi

Temel: theme-factory → **Midnight Galaxy**. Tema sunum desteleri için yazılmış, bu yüzden
palet korunup roller yeniden tanımlandı.

```css
@theme {
  --color-bg:      #2b1e3e;  /* Deep Purple — sayfa zemini */
  --color-surface: #4a4e8f;  /* Cosmic Blue — YALNIZCA yüzey/kenarlık */
  --color-muted:   #a490c2;  /* Lavender — ikincil metin, etiket, focus halkası */
  --color-fg:      #e6e6fa;  /* Silver — birincil metin */

  --status-running: #5ecfa8;  /* nane — ayakta */
  --status-stopped: #6b6280;  /* soluk mor — kapalı */
  --status-warn:    #e8b04b;  /* amber — port çakışması */
  --status-error:   #e05c78;  /* gül — çöktü / exit ≠ 0 */
}
```

**`--color-surface` metin rengi olarak kullanılamaz** — zemin üstünde kontrastı ~1.9:1.
Sadece yüzey ve hairline kenarlık. `--color-muted` ~5:1, `--color-fg` ~12:1 (ikisi de geçer).

Semantik renkler temada yoktu, eklendi: panel baştan sona durum gösteriyor. Kırmızı-yeşil
yerine nane-gül; mor zeminde titremiyorlar ve parlaklıkları farklı olduğu için renk
körlüğünde de ayırt edilebiliyorlar.

### Tipografi

- Başlıklar: **Familjen Grotesk**
- Arayüz metni: **Geist Sans**
- Veri: **Geist Mono** — port, PID, yol, komut satırı, uptime sayacı

Mono kullanımı pazarlık konusu değil; ekrandaki verinin çoğu hizalanmak zorunda.

### İmza öğesi: port spektrumu

Panelin üstünde 1024–65535 aralığını temsil eden yatay şerit; dolu her port bir ışık
noktası. Yoğun bölgeler (3000-3010, 5173, 8080) doğal olarak kümeleniyor, çakışan portlar
amber yanıyor. Dekoratif değil — bir bakışta hangi aralıkların dolu olduğunu gösteriyor.

**Cesaret tek burada harcanır.** Proje kartları düz, hairline kenarlıklı, gradyansız kalsın.

### Uygulama kuralları

- shadcn/ui'nin varsayılan nötr token'larını yukarıdaki değerlerle ez, yoksa iki palet çakışır
- **Sadece koyu tema.** Açık mod yok; midnight teması kendisiyle kavga eder
- Durum geçişlerinde 150ms renk animasyonu yeter. `prefers-reduced-motion` altında kapat
- Port spektrumundaki noktalar nabız atmasın — sürekli hareket eden panelin yanında çalışılamaz
- Focus halkası lavanta, 2px, her interaktif öğede görünür. Kill/restart klavyeyle erişilebilir

---

## Kod konvansiyonları

- Tüm alt process çağrıları `core`'da, `execa` ile, timeout'lu
- Ham komut çıktısını ayrıştıran her fonksiyon saf (pure) olmalı: string girer, tiplenmiş
  nesne çıkar. Bu sayede gerçek çıktı fixture'larıyla test edilebilir
- Tipler zod şemalarından türetilir (`z.infer`), elle interface yazma
- Kullanıcıya görünen metinler: sade fiil, cümle düzeni, aktif çatı. Buton "Durdur" diyorsa
  sonuç bildirimi de "Durduruldu" der. Hata mesajları özür dilemez, ne olduğunu ve ne
  yapılacağını söyler

## Test stratejisi

Ağırlık **parser testlerinde**. Gerçek `lsof`, `ps`, `docker ps` çıktılarını fixture olarak
kaydet ve ayrıştırıcıları bunlara karşı çalıştır. Bu projede en çok kıymeti görecek testler
bunlardır — asıl kırılganlık komut çıktı formatlarında.

---

## Yol haritası

**v1** — tarayıcılar, proje algılama, registry, stop/start/restart, `ls`/`kill`/`open`
komutları, tek ekranlık web paneli

**v1.5** — Ink TUI (canlı liste, ok tuşlarıyla gezinme), log tailing, daemon + geçmiş

**v2** — menu bar, port çakışması uyarıları, proje grupları (birlikte başlat/durdur)

**Başlangıç sırası:** önce `core`'un tarama katmanı, çıktısı JSON olarak doğrulanana kadar.
Gerisi onun üstüne oturur.

---

## Karara bağlanmamış konular

- **Bun vs Node.** v1 Node ile. Kod ESM ve standart API'lerde kalırsa sonradan taşımak
  birkaç saatlik iş. Uzun ömürlü launchd daemon'ında Node daha oturmuş.
- **Docker: CLI mi dockerode mu.** v1'de `docker ps --format json` ayrıştırma yeterli.
  Canlı container logu gerekince dockerode'a geç.
- **Menu bar: Tauri vs Electron.** v2'ye kadar ertelendi; mimari ikisini de destekliyor.
  Electron sürtünmesiz ama ~100MB; Tauri hafif ama Node çekirdeğini sidecar olarak
  paketlemeyi gerektirir.
- ~~Proje adı.~~ **Karara bağlandı: `orbit`.**
