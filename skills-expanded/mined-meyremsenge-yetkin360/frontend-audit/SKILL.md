---
name: frontend-audit
description: Çalışan bir frontend URL'sini uçtan uca değerlendiren 3 aşamalı pipeline — Playwright MCP (kullanıcı akışı, formlar, responsive, console hataları, ekran görüntüsü) → Lighthouse MCP (performans, erişilebilirlik, SEO, Core Web Vitals) → OWASP ZAP MCP (DAST/dışarıdan güvenlik taraması) → önceliklendirilmiş rapor. "Bu siteyi/frontend'i değerlendir", "UX+performans+güvenlik raporu çıkar", "canlı URL'yi denetle" isteklerinde kullan. Backend/API güvenliği veya statik kod analizi için değil — o iş `trivy-scan`/`security-scan`/`authz-test`'te.
---

# frontend-audit — Playwright → Lighthouse → ZAP → rapor

## Bu mu, yoksa diğer güvenlik/kalite skilleri mi?

| Soru | `frontend-audit` (bu skill) | `trivy-scan` | `security-scan` | `authz-test` |
|---|---|---|---|---|
| Çalışan bir URL'yi tarayıcıda gezmek gerekiyor mu | ✅ evet, ön koşul | ❌ hayır | ❌ hayır | ✅ (canlı endpoint) |
| Performans/Core Web Vitals/SEO | ✅ | ❌ | ❌ | ❌ |
| Dışarıdan (kara kutu) web güvenlik taraması (DAST) | ✅ (ZAP) | ❌ | ❌ | ❌ (IDOR/yetki odaklı, DAST değil) |
| Statik kod/bağımlılık CVE'si | ❌ | ✅ | ✅ (Python) | ❌ |
| Kaynak kod erişimi gerekir mi | ❌ hayır (kara kutu) | ✅ evet | ✅ evet | kısmen |

**Kısa kural:** Elinde çalışan bir frontend URL'si varsa ve "genel olarak nasıl"
diye soruluyorsa → bu skill. Kaynak kod/repo/bağımlılık taranacaksa →
`trivy-scan`/`security-scan`. Belirli bir yetki/tenant açığı araştırılıyorsa
→ `authz-test`.

## ATDD/verify zincirindeki yeri

Bu skill zincirin (`atdd→...→commit`) parçası **değil** — `postmortem` gibi
bağımsız, isteğe bağlı bir araç. Ama araçları zincire şöyle bağlanır:

- **`atdd`**: Araç çağırmaz, sadece ölçülebilir hedef yazar — görev bir web
  UI içeriyorsa `Benchmark` bölümüne performans/erişilebilirlik hedefi
  ("LCP < 2.5s", "erişilebilirlik skoru ≥ 90" gibi) girilmeli. Güvenlik
  tarafı `threat-model`'in ürettiği `AC-S<n>` kriterleridir, bu skill değil.
- **`verify`**: Gerçek tetikleyici burası. Gate 7 (e2e — Playwright),
  gate 8/9 (Lighthouse — performans/erişilebilirlik), gate 13 (DAST — ZAP,
  sadece `threat-model` bir `AC-S<n>` ürettiyse) bu skill'in araç
  referansını kullanır. Bkz. `verify/SKILL.md`.
- Bağımsız/ad-hoc kullanım (zincire bağlı olmadan): kullanıcı doğrudan
  "şu canlı siteyi değerlendir" derse, bu skill tek başına çağrılır.

## Pipeline

```
Çalışan frontend URL'si
        ↓
Playwright MCP     — kullanıcı akışı, butonlar, formlar, responsive, console hataları, bozuk linkler, ekran görüntüsü
        ↓
Lighthouse MCP     — performans, erişilebilirlik, SEO, Core Web Vitals, kaynak analizi
        ↓
OWASP ZAP MCP      — dışarıdan web güvenliği / DAST taraması
        ↓
AI ajanı           — önceliklendirilmiş frontend değerlendirme raporu
```

Aşamalar bağımsızdır — biri kurulu değilse/çalışmıyorsa diğerleri atlanmaz,
raporda o aşama açıkça "N/A — sebep" olarak işaretlenir.

## Durum özeti (bu makinede doğrulandı — 2026-08-31)

| Aşama | Kurulum | Test durumu |
|---|---|---|
| Playwright | Zaten bağlı (`mcp__playwright__*`), kurulum gerekmedi | ✅ 5 araç gerçekten çağrıldı (`browser_navigate`, `browser_snapshot`, `browser_console_messages`, `browser_network_requests`, `browser_close`) — hepsi çalıştı |
| Lighthouse | `npm install -g @danielsogl/lighthouse-mcp@latest` | ✅ **11/11 araç** gerçekten çağrıldı (`https://example.com` üzerinde), hepsi geçerli sonuç döndürdü |
| OWASP ZAP | `winget install ZAP.ZAP` + `mcp` add-on (v0.4.0) kuruldu | ✅ **17/17 araç** kullanıcının kendi (sandbox dışı) terminalinde GUI ile başlattığı ZAP'a bu oturumdan HTTPS ile bağlanılarak test edildi (bkz. tuzak #3 — sandbox JVM subprocess açmayı engelliyor ama HTTP/HTTPS ile dışarıdan çalışan bir sunucuya erişim engellenmiyor) |

## Araçlar

### 1. Playwright MCP (`mcp__playwright__*`)

Zaten bu ortamda bağlı, ayrı kurulum gerekmiyor. ~24 araç var, en sık kullanılanlar:

| Araç | Ne zaman kullan |
|---|---|
| `browser_navigate` | URL'ye git |
| `browser_snapshot` | Sayfanın erişilebilirlik ağacını al (DOM okuma, buton/link/form tespiti) — ekran görüntüsünden daha güvenilir |
| `browser_click` / `browser_type` / `browser_fill_form` / `browser_select_option` | Kullanıcı akışını simüle et (form doldurma, buton tıklama) |
| `browser_console_messages` | JS hatalarını/uyarılarını yakala |
| `browser_network_requests` | Bozuk link/404/başarısız istek tespiti |
| `browser_take_screenshot` | Görsel kanıt (rapora eklenecek ekran görüntüsü) |
| `browser_resize` | Responsive test (mobile/tablet/desktop viewport) |
| `browser_wait_for` | Async içerik yüklenmesini bekle |

### 2. Lighthouse MCP (`lighthouse-mcp-server`, gömülü v2.0.1)

Kurulum: `npm install -g @danielsogl/lighthouse-mcp@latest`
Çalıştırma (Claude Code'a MCP olarak eklemek için):
```bash
claude mcp add lighthouse -- node "$(npm root -g)/@danielsogl/lighthouse-mcp/dist/index.js"
```

11 araç (hepsi test edildi):

| Araç | Ne döner |
|---|---|
| `run_audit` | Tam Lighthouse denetimi (performance+accessibility+best-practices+seo+agentic-browsing kategorileri) — en yavaş, en kapsamlı |
| `get_performance_score` | Sadece performans skoru + metrikler (FCP, LCP, TBT, CLS) |
| `get_accessibility_score` | Erişilebilirlik skoru + öneri listesi |
| `get_seo_analysis` | SEO skoru + öneri listesi |
| `get_core_web_vitals` | LCP/FCP/CLS/INP/TBT tek tek |
| `get_security_audit` | HTTPS/CSP gibi temel güvenlik header kontrolleri (ZAP'ın yerini TUTMAZ — sadece Lighthouse'un statik header kontrolü) |
| `analyze_resources` | Görsel/JS/CSS/font boyutu ve optimizasyon fırsatları |
| `find_unused_javascript` | Kullanılmayan JS tespiti (bundle boyutu azaltma) |
| `get_lcp_opportunities` | LCP'yi iyileştirecek somut öneriler |
| `check_performance_budget` | Verilen eşiklere göre PASS/FAIL (bkz. tuzak #2) |
| `compare_mobile_desktop` | Mobil/masaüstü skor farkı |

Ortak parametre: `url` (zorunlu). Çoğu araç `device: "mobile"\|"desktop"` de kabul eder.

### 3. OWASP ZAP MCP (`mcp` add-on, v0.4.0-alpha) — 17/17 araç test edildi

**Kurulum (bu makinede tamamlandı):**
```bash
winget install --id ZAP.ZAP -e          # ZAP 2.17.0 + Java 17 (Temurin) bağımlılığı
# ZAP kurulum dizininden, Java 17 ile:
java -jar zap-2.17.0.jar -cmd -addoninstall mcp -addonupdate
```

**Bu ortamda (Claude Code sandbox'ı) ZAP daemon'ı doğrudan başlatılamıyor**
(bkz. tuzak #3) — ama kullanıcı ZAP'ı **kendi masaüstünde GUI ile** açıp
MCP sunucusunu aktif ettiğinde, bu oturumdan `https://localhost:8282`'ye
düz HTTP isteğiyle (JVM subprocess açmadan) sorunsuz bağlanılabiliyor.
Bu şekilde **17 aracın tamamı gerçekten çağrılıp doğrulandı**
(hedef: `https://demo.owasp-juice.shop` — OWASP'ın kendi güvenlik testi
pratiği için sunduğu resmi demo hedefi).

**Bağlantı formatı (tuzak #6'ya bakmadan asla tahmin etme):**
```
POST https://localhost:8282/
Header: Authorization: <security-key>      ← "Bearer" ÖNEKİ YOK
Header: Content-Type: application/json
Body: {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"...","arguments":{...}}}
```

| Araç | Zorunlu parametre(ler) | Ne yapar | Not |
|---|---|---|---|
| `zap_version` | yok | ZAP versiyonunu döner | |
| `zap_info` | yok | Temel ZAP bilgisi | |
| `zap_create_context` | `name`, `url` | Tarama bağlamı oluşturur | param adı `contextName` DEĞİL `name` |
| `zap_start_spider` | `target` | Klasik (statik link) spider başlatır, `scan_id` döner | |
| `zap_get_spider_status` | `scan_id` | İlerleme yüzdesi | `target` değil `scan_id` ister |
| `zap_stop_spider` | `scan_id` | Spider'ı durdurur | |
| `zap_start_ajax_spider` | `target` | JS-render edilen SPA'lar için spider, `scan_id` döner | |
| `zap_get_ajax_spider_status` | `scan_id` | İlerleme (0/50/100 gibi kaba adımlar) | |
| `zap_stop_ajax_spider` | `scan_id` | AJAX spider'ı durdurur | |
| `zap_get_passive_scan_status` | yok | Pasif tarama kuyruğu durumu | Spider gezdikçe otomatik pasif taranır |
| `zap_start_active_scan` | `target` | **Gerçek saldırı payload'ları gönderir** (DAST) — `scan_id` döner | Sadece yetkili/authorized hedefte kullan |
| `zap_get_active_scan_status` | `scan_id` | İlerleme yüzdesi | |
| `zap_stop_active_scan` | `scan_id` | Active scan'i durdurur | |
| `zap_list_resources` | yok | Okunabilir resource URI'lerini listeler (`zap://alerts`, `zap://contexts`, `zap://history/{id}` vb.) | |
| `zap_read_resource` | `uri` | Bir resource'u okur (örn. `zap://alerts` → bulunan tüm alert'ler) | Bazı yanıtlarda kontrol karakteri JSON'u bozabilir, bkz. tuzak #7 |
| `zap_get_history` | `id` | Tek bir HTTP isteğinin tam request/response header'larını döner | |
| `zap_generate_report` | `template`, `file_path` | Rapor dosyası üretir (örn. `traditional-html`) | `file_path` zorunlu, vermezsen "required" hatası |

**Gerçek akış (doğrulanmış sıra):**
```
zap_create_context(name, url)
  → zap_start_spider(target) → scan_id → zap_get_spider_status(scan_id) → zap_stop_spider(scan_id)
  → zap_start_ajax_spider(target) → scan_id → zap_get_ajax_spider_status(scan_id) → zap_stop_ajax_spider(scan_id)
  → zap_get_passive_scan_status()
  → zap_start_active_scan(target) → scan_id → zap_get_active_scan_status(scan_id) → zap_stop_active_scan(scan_id)
  → zap_read_resource(uri="zap://alerts")   ← asıl bulgular burada
  → zap_generate_report(template, file_path)
```

**Kullanıcının kendi terminalinde ZAP'ı başlatma — GUI modu, adım adım:**

1. **ZAP'ı GUI ile aç:**
   ```powershell
   & "C:\Program Files\ZAP\Zed Attack Proxy\ZAP.exe"
   ```
   İlk açılışta "Persist Session?" sorarsa test amaçlıysa
   **"No, I do not want to persist this session"** seçilebilir.

2. **MCP Integration ayarlarını aç:** Menüden `Tools → Options → MCP Integration`.
   - **Enable MCP Server** — işaretle
   - **Port** — varsayılan `8282`
   - **Secure Only** — açık bırak (sadece HTTPS)
   - **Security Key** — üretilen anahtarı kopyala

3. **Bu ortamdan (Claude Code) doğrudan bağlan — MCP olarak eklemene bile gerek yok:**
   Claude, `curl -sk https://localhost:8282/ -H "Authorization: <key>" -d '{...JSON-RPC...}'`
   ile veya Python `urllib`/`requests` ile doğrudan çağırabilir (bu skill'in
   test scripti bu yöntemi kullandı). MCP client'a (`claude mcp add`) resmi
   olarak eklemek istersen:
   ```bash
   claude mcp add --transport http zap https://localhost:8282 --header "Authorization: <key>"
   ```
   (Not: `Authorization: Bearer <key>` DEĞİL, sadece `Authorization: <key>` —
   bkz. tuzak #6.)

**Not:** ZAP GUI'si kapanırsa MCP sunucusu da durur. Sürekli/otomasyon
senaryosu için GUI yerine headless daemon istenirse:
```powershell
& "C:\Program Files\Eclipse Adoptium\jre-17.0.20.101-hotspot\bin\java.exe" -jar "C:\Program Files\ZAP\Zed Attack Proxy\zap-2.17.0.jar" -daemon -port 8090 -config api.disablekey=true
```
(Bu makinede Java 8 varsayılan `PATH`'te — mutlaka Java 17'nin tam yolunu
kullan, aksi halde `UnsupportedClassVersionError` alınır, bkz. tuzak #5.)

## ⚠️ Doğrulanmış tuzaklar

1. **Windows'ta `npx -y <paket>` MCP server'ı ilk çalıştırmada interaktif
   onay istediği için stdio JSON-RPC probe'u ile DEADLOCK olur** — hem npx
   onay bekliyor hem senin script'in JSON-RPC cevabı bekliyor, ikisi de
   stdin/stdout'u paylaşıyor. Çözüm: önce `npm install -g <paket>` ile
   global kur, sonra `node <global-yol>/dist/index.js` ile doğrudan çalıştır
   (npx'i tamamen atla).

2. **Lighthouse'un `check_performance_budget` aracı, beklenmedik şekilde
   `results: {}` (boş) döndürebilir** — `budget` parametresinin şeması bu
   oturumda tam doğrulanamadı (`{"performance": 80}` gönderildi, "passed"
   geldi ama `results` boştu). Kritik bir budget kontrolü için önce
   `run_audit`'in ham skorlarıyla manuel karşılaştır, sadece bu aracın
   PASS'ine güvenme.

3. **ZAP (ve muhtemelen her Netty/Apache-HttpCore5 tabanlı Java ağ
   sunucusu) bazı sandbox'lı Claude Code ortamlarında JVM'in loopback
   soket AÇMASI engellenir, ama bu ortamdan var olan bir sunucuya HTTP
   isteği GÖNDERMEK engellenmez — ikisi farklı kısıtlamalar.** Belirti:
   `java.io.IOException: Unable to establish loopback connection` +
   `SocketException: Invalid argument: connect` — bu sadece Bash/PowerShell
   tool'uyla bu oturumdan yeni bir JVM süreci başlatmaya çalışınca çıkar.
   **Çözüm (doğrulandı, çalışıyor):** ZAP'ı kullanıcı kendi masaüstünde GUI
   ile başlatsın (bu, sandbox dışında bir süreçtir), sonra bu oturum ona
   `curl`/`urllib` ile düz HTTPS isteğiyle bağlansın — subprocess açmıyor,
   sadece var olan bir porta konuşuyor, bu engellenmiyor.

4. **`trivy-scan` skill'indeki UTF-8 tuzağı burada da geçerli** — kendi
   stdio probe script'ini yazarsan `PYTHONUTF8=1` + `encoding="utf-8"`
   zorunlu (Windows, kullanıcı adında `Ç` olan bu makinede doğrulandı).

5. **ZAP 2.17.0, Java 17 gerektirir ama bu makinede `PATH`'teki varsayılan
   Java 8'dir.** `zap.bat`/`java -jar zap-2.17.0.jar` çalıştırılırken PATH'teki
   Java kullanılırsa `UnsupportedClassVersionError: ... class file version
   61.0 ... this version only recognizes up to 52.0` hatası alınır — mesaj
   Java versiyon uyumsuzluğunu doğrudan söylüyor ama ZAP'ın kendisi
   hatalıymış gibi yanıltabilir. Çözüm: winget'in kurduğu Temurin 17'nin tam
   yolunu kullan (`C:\Program Files\Eclipse Adoptium\jre-17.0.20.101-hotspot\bin\java.exe`),
   PATH'e güvenme.

6. **ZAP MCP'nin `Authorization` header'ı `Bearer <key>` DEĞİL, çıplak
   `<key>` bekliyor.** `Authorization: Bearer <key>` gönderirsen
   `{"error":{"code":-32000,"message":"Invalid or missing security key"}}`
   alırsın — hata mesajı anahtarın yanlış olduğunu düşündürür ama aslında
   format yanlış. Doğrulanmış doğru header: `Authorization: <key>` (öneksiz).
   Ayrıca `Secure Only=true` varsayılan olduğu için `http://` ile denersen
   (443/8282 fark etmez) `{"error":{"message":"HTTPS required"}}` alırsın —
   `https://` kullan, kendinden imzalı sertifika olduğu için `curl -k`
   (veya Python'da `ssl.CERT_NONE`) gerekir.

7. **Araç parametre adları tool açıklamasında yazmıyor, deneme-yanılmayla
   çıkar** — `zap_create_context` `contextName` değil `name` ister;
   `zap_get_spider_status`/`zap_stop_spider`/`zap_get_ajax_spider_status`/
   `zap_stop_ajax_spider`/`zap_get_active_scan_status`/`zap_stop_active_scan`
   `target` değil, ilgili `zap_start_*` çağrısının döndürdüğü `scan_id`
   (örn. `spider-1`, `ajaxspider-1`, `ascan-1`) ister; `zap_generate_report`
   `file_path` olmadan "required" hatası verir. Ayrıca `zap_read_resource`
   ile `zap://alerts` okurken bazı alert başlıklarında (örn. Türkçe/özel
   karakterli bir alert adı) yanıt JSON'u sıkı bir `json.loads` ile
   parse edilemeyebilir — ham metni de yakalayan bir fallback yaz, sert
   parse hatasında bulguyu kaybetme.

## Rapor formatı

Üç aşamadan gelen bulguları tek bir önceliklendirilmiş rapora indir:

```markdown
## Frontend Değerlendirme — <URL>

### 🔴 Kritik (hemen düzelt)
- [ZAP] ... / [Lighthouse] performans <50 / [Playwright] kırık kullanıcı akışı

### 🟠 Yüksek
...

### 🟡 Orta / iyileştirme fırsatı
...

### ℹ️ Bilgi / N/A
- [ZAP] Bu ortamda taranamadı — <sebep>
```

Her bulgu hangi araçtan geldiğini (`[Playwright]`/`[Lighthouse]`/`[ZAP]`)
etiketiyle taşımalı — kaynağı belirsiz bir bulgu, doğrulanamaz bir bulgudur.

## Yapmayacakların
- ZAP çalışmıyorken "güvenlik açığı yok" sonucuna varmaz — N/A der.
- Bulunan bir performans/erişilebilirlik sorununu kendi başına "önemsiz"
  diye eleme, skoru ve öneriyi olduğu gibi raporla.
- Kod yazmaz/düzeltmez — bulguyu raporlar.
