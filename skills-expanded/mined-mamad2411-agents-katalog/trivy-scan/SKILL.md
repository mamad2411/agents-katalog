---
name: trivy-scan
description: Trivy MCP (aquasecurity/trivy-mcp) araçlarını kullanma referansı — bağımlılık CVE'si, secret, yanlış yapılandırma (IaC), lisans taraması; yerel dizin, container image veya uzak GitHub reposu üzerinde. "açık bul", "güvenlik açığı tara", "bu repo'yu tara", "container image'ı tara", "bağımlılıklarda CVE var mı" gibi isteklerde kullan. Python'a özgü SAST/mantık hatası bulmaz — o iş `security-scan` (bandit) ve `red-team`'de.
---

# trivy-scan — Trivy MCP araçları

## Bu mu, yoksa `security-scan` mı?

Aynı işi yapan iki farklı skill yok — **kapsamları ayrık**, karıştırma:

| Soru | `trivy-scan` (bu skill) | `security-scan` (mevcut) |
|---|---|---|
| Bağımlılık CVE'si (pip/npm/cargo/go vb.) | ✅ çok dilli | ✅ sadece pip-audit/npm audit |
| Container image taraması | ✅ | ❌ yok |
| Uzak GitHub reposu (klonlamadan) | ✅ | ❌ yok |
| Secret/sızıntı taraması | ✅ | ✅ (detect-secrets) |
| IaC yanlış yapılandırma (Dockerfile, Terraform, K8s) | ✅ | ❌ yok |
| Lisans taraması | ✅ | ❌ yok |
| Python SAST (`shell=True`, SQL injection, MD5) | ❌ yok | ✅ (bandit) |
| İş mantığı açığı (IDOR, auth bypass) | ❌ yok | ❌ yok — `red-team`/`authz-test`'in işi |
| ATDD pipeline gate'i (PASS/FAIL) | ❌ hayır, serbest kullanım | ✅ evet, `verify` içinde |

**Kısa kural:** Kod mantığı hatası mı arıyorsun → `security-scan` (Python) veya
`red-team`. Bağımlılık/container/repo/secret/IaC/lisans mı → bu skill.
İkisi de kullanılabilir (birbirini geçersiz kılmaz), farklı katmanları kapsarlar.

## Kurulum (bir kere)

```bash
# 1. Trivy CLI (winget/brew/apt) — MCP plugin bunun üstüne kurulur
winget install --id AquaSecurity.Trivy -e

# 2. MCP plugin
trivy plugin install github.com/aquasecurity/trivy-mcp
```

Doğrulama: `trivy plugin list` çıktısında `mcp` görünmeli.

**Claude Code'a kalıcı MCP olarak eklemek istersen** (opsiyonel — bu skill
kaydı olmadan da `Bash` üzerinden `trivy mcp -t stdio` + JSON-RPC ile
kullanılabilir, test bu şekilde yapıldı):

```bash
claude mcp add trivy -- trivy mcp -t stdio
```

## ⚠️ Doğrulanmış tuzaklar (hepsi bu oturumda test edilerek bulundu)

1. **MCP kendi gömülü Trivy'yi kullanır, sistem CLI'sından FARKLI olabilir.**
   Bu makinede sistem `trivy --version` → `0.74.0`, ama MCP'nin
   `trivy_version` aracı → `0.68.2` döndürdü. `trivy mcp` başlatılırken
   `--trivy-binary <yol>` verilmezse gömülü/eski binary kullanılır. Versiyon
   farkı CVE veritabanı güncelliğini etkileyebilir — kritik bir taramada
   önce `trivy_version` ile hangi binary'nin çalıştığını doğrula.

2. **`findings_get`, `id` değil `i` alanını ister.** `findings_list`'in
   döndürdüğü her bulguda iki farklı kimlik var: `id` (CVE-2026-28684 gibi
   insan-okunur) ve `i` (`b754b76345aa9e9b` gibi deterministik hash).
   `findings_get`'e CVE numarasını verirsen **sessizce değil, açıkça**
   `"finding not found"` hatası alırsın — ama bu hatayı görüp "araç bozuk"
   sanma, doğru alan `i`'dir. (Doğrulandı: CVE ile denendi → hata; `i`
   hash'iyle denendi → doğru sonuç döndü.)

3. **`scan_*` araçları bulguyu DÖNMEZ, sadece `batch_id` döner.** Üçü de
   (`scan_filesystem`/`scan_image`/`scan_repository`) taramayı yapar ve
   `{"batch_id": "...", "counts": {...}, "next": {"tool": "findings_list", ...}}`
   döndürür — asıl bulgu listesi için ayrıca `findings_list(batchID=...)`
   çağırman gerekir. Tek çağrıda bitmez, iki adımlı akış.

4. **`requirements.txt` versiyon pinlemiyorsa (`paramiko` gibi, `==` yok)
   sessizce 0 sonuç döner — hata vermez, "temiz" ile ayırt edilemez.**
   Debug log'da `Supported files for scanner(s) not found` görülüyor ama
   normal modda bu görünmez, sadece boş rapor gelir. Gerçek CVE eşleştirmesi
   için pinlenmiş bir dosya (`pip freeze` ile üretilip proje bağımlılıklarına
   filtrelenmiş) gerekir — repo'nun asıl `requirements.txt`'ine dokunmadan
   `/tmp/<geçici-dizin>/requirements.txt` gibi bir kopyada dene.

5. **`target` için `.` verme, mutlak yol ver.** `scan_filesystem`'in şema
   açıklaması bunu zaten söylüyor ("use the absolute path rather than `.`")
   — göreli yolla tutarsız/boş sonuç riski var.

6. **Kendi stdio probe script'i yazıyorsan `PYTHONUTF8=1` + `encoding="utf-8"`
   zorunlu (Windows).** Bu, Claude Code'un kendi MCP client'ını kullanırken
   geçerli değil (o zaten UTF-8 hallediyor) — sadece elle `subprocess.Popen`
   ile JSON-RPC konuşan bir test/debug script'i yazarsan işine yarar. cp1254
   ortamında `UnicodeDecodeError`/`UnicodeEncodeError` ile sessizce patlar.

## Araçlar (6 tanesi de test edildi)

| Araç | Zorunlu parametreler | Ne döner | Ne zaman kullan |
|---|---|---|---|
| `scan_filesystem` | `target` (mutlak yol), `scanType` (`vuln`\|`misconfig`\|`license`\|`secret` dizisi), `outputFormat`, `targetType="filesystem"` | `batch_id` + kategori bazlı sayaç | Yerel bir proje dizinini/dosyayı taramak |
| `scan_image` | aynı + `targetType="image"`, `target`=image adı (örn. `alpine:3.19`) | `batch_id` + sayaç | Bir container image'ın CVE'lerini kontrol etmek (Docker daemon gerekir) |
| `scan_repository` | aynı + `targetType="repository"`, `target`=git URL | `batch_id` + sayaç | **Repo'yu klonlamadan** uzaktan GitHub/GitLab reposu taramak — "şu repo'yu tara" isteğinde ilk tercih |
| `findings_list` | `batchID`, `minSeverity`, `categories` (dizi) | Bulgu listesi (kısaltılmış alan adlarıyla: `i`,`c`,`s`,`id`,`at`,`an`,`av`,`ap`,`fx`,`fv`) + `token` (sayfalama) | Bir `scan_*` çağrısından sonra asıl bulguları görmek — **zorunlu ikinci adım** |
| `findings_get` | `batchID`, `id` (ama gerçekte `i` alanı — bkz. tuzak #2) | Tek bulgunun tam detayı | Belirli bir bulgunun (CVSS, açıklama, fix komutu gibi) ayrıntısını almak |
| `trivy_version` | yok | Çalışan gömülü Trivy'nin versiyonu | Taramaya başlamadan önce hangi Trivy motorunun aktif olduğunu doğrulamak (bkz. tuzak #1) |

### Ortak parametreler (`scan_*` üçü için)
- `scanType`: `["vuln"]`, `["secret"]`, `["misconfig"]`, `["license"]` veya
  birden fazlası — gereksiz kategori isteme, tarama süresini uzatır.
- `severities`: `["CRITICAL","HIGH","MEDIUM","LOW","UNKNOWN"]` alt kümesi —
  varsayılan sadece `CRITICAL`, genelde `HIGH`+`MEDIUM`'u da eklemek gerekir.
- `fixedOnly`: `true` → fix'i olmayan bulgular rapordan düşer (gürültü azaltır).
- `outputFormat`: `json` (varsayılan, programatik kullanım için), SBOM
  isteniyorsa `cyclonedx` (tercih edilen) veya `spdx`/`spdx-json`.

## Tipik akış

```
1. trivy_version                                    → hangi Trivy çalışıyor, doğrula
2. scan_filesystem / scan_image / scan_repository    → batch_id al
3. findings_list(batchID, minSeverity, categories)   → bulguları listele
4. (opsiyonel) findings_get(batchID, i=<hash>)        → tek bulguyu derinlemesine incele
```

Bulgular kullanıcıya raporlanırken CVE numarası (`id` alanı) gösterilir,
`i` alanı sadece `findings_get` çağrısı için dahili kullanılır.

## Bu görevde (maviLojistik) doğrulanmış gerçek sonuç

`scan_filesystem` ile pinlenmiş bağımlılıklar tarandı: `python-dotenv 1.2.1`
→ CVE-2026-28684 (MEDIUM, fix: 1.2.2) ve `paramiko 4.0.0` → CVE-2026-44405
(LOW, fix yok). Secret taraması tüm repo ağacında 0 bulgu verdi.
`scan_repository` ile `aquasecurity/trivy-ci-test` (klonlamadan) tarandı,
gerçek cargo/pipenv CVE'leri bulundu. `scan_image` ile `alpine:3.19`
taranıp 2 HIGH bulundu. Detaylar: Saga task #342 yorumları.

## Yapmayacakların
- Kod yazmaz/düzeltmez — bulguyu raporlar, düzeltme kararı ve uygulaması
  kullanıcının/`code-copilot`'ın işi.
- Bulunan bir CVE'yi kendi başına "önemsiz" diye eleme — severity/fix
  bilgisini olduğu gibi raporla, karar kullanıcının.
- `security-scan`'in yerini almaz (ATDD pipeline gate'i değil, serbest
  kullanım) — ikisini birbirine karıştırıp tek bir "güvenlik taraması"
  adımı sanma.
