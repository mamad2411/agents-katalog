---
name: entropia-regression-check
description: >
  Entropia'da CI'ın YAKALAYAMADIĞI regresyonlara karşı kontrol listesi: docs
  kayıt silme (üç kez oldu), üretilmiş dosya drift'i (openapi.json,
  repository_facts.md), ci.yml concurrency kusuru nedeniyle hiç koşmamış CI,
  bayat belge/summary güveni ve çift kullanılmış ADIM numaraları. Bir PR merge
  etmeden önce, docs değiştiren her işte, "landed mi" sorusunda ve oturum
  başında oku.
license: MIT
---

# Entropia regression check — CI'ın görmediği yerler

Bu skill, **hiçbir otomatik kapının korumadığı** regresyonlar içindir. Hepsi en
az bir kez gerçekten oldu.

## 1. Docs kayıt silme — ÜÇ KEZ oldu

**Hiçbir CI kapısı `docs/` okumaz.** Bayat base'li docs PR'ları
`docs/PROJECT_HISTORY.md`'den kayıt sildi:

- #590 (ADIM 18, **211 satır**)
- #604 (ADIM 22 + ADIM 16, **194 satır**; ayrıca CLAUDE.md §Current position'ı boşalttı)

**Docs PR'ı merge etmeden önce zorunlu:**

```bash
git show <sha> -- docs/ | grep '^-## ' || echo "kayit silinmemis"
```

Çıktı varsa merge **etme** — base'i tazele, kaydı geri koy.

Ayrıca docs PR'ı açmadan önce base'in güncelliğini doğrula:

```bash
git fetch && git log --oneline origin/main -6
```

## 2. Üretilmiş dosyalar — elle düzeltme

| Dosya | Üretici | Kapı |
|---|---|---|
| `docs/openapi.json` | `make openapi` (`entropia.apps.api.openapi_export`) | `--check` CI'da bloklayıcı |
| `docs/generated/repository_facts.md` | `scripts/generate_repository_facts.py` | `--check` CI'da bloklayıcı |

`repository_facts.md` **sayısal otoritedir** (alembic head/sayı, tablo & FK,
HTTP operation, frontend route, `ENGINE_VERSION`, capability, test collection).
`--check` bu blokla çelişen bir head / `ENGINE_VERSION` / `SHARED_ALLOCATION_STATUS`
iddiasını **kırmızıya çevirir**.

Kırmızıysa dosyayı elle düzeltme — üreticiyi koştur.

## 3. `ci.yml` concurrency kusuru — CI hiç koşmamış olabilir

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

main'de kuyruğa giren koşu bir öncekini iptal etti → `e8d1d48` (#633) ve
`bc59dae` (#634) **0 job ile cancelled**, CI'ları **hiç koşmadı**.

"CI yeşil" demeden önce **job sayısını** kontrol et:

```bash
gh run list --branch main --limit 5
gh run view <id>   # 0 job => koşmadı, "yesil" DEĞİL
```

> **`gh` HER ORTAMDA YOK — ölçüldü (2026-08-25, remote container: `command -v gh` boş).**
> Aşağıdaki `gh` komutları **yerel** oturumun yoludur. `gh` yoksa aynı bilgiyi GitHub
> MCP araçlarından al (bunlar `.claude/settings.json` `permissions.allow`'da salt-okur
> olarak zaten kayıtlı): PR listesi `mcp__github__list_pull_requests` · PR ayrıntısı,
> diff'i ve check'leri `mcp__github__pull_request_read` · koşu listesi
> `mcp__github__actions_list` · koşu ayrıntısı `mcp__github__actions_get` · job log'u
> `mcp__github__get_job_logs` · PR açma `mcp__github__create_pull_request`.
> **Kanıt sorusu değişmez, aracı değişir.**

## 3b. Sır taraması YERELDE koşturulabilir (Docker gerekmez)

`Secret scan (gitleaks)` CI'da Docker imajıyla koşar ve bu container'da **Docker
daemon yoktur** — ama bu "yerelde doğrulanamaz" demek DEĞİLDİR: gitleaks statik tek
bir binary olarak yayımlanır.

```bash
curl -sSL -o gl.tar.gz https://github.com/gitleaks/gitleaks/releases/download/v8.28.0/gitleaks_8.28.0_linux_x64.tar.gz
tar xzf gl.tar.gz && ./gitleaks detect --source . --no-git --config .gitleaks.toml --redact -v
```

**Allowlist eklerken iki tuzak, ikisi de yaşandı:**

1. **`regexTarget = "line"` yazmayı unutma.** Allowlist regex'leri öntanımlı olarak
   **secret**'a bakar, satıra değil; satır şekli tarif eden bir desen sessizce
   etkisiz kalır ve kapı aynı bulguyla kırmızı kalmaya devam eder.
2. **Negatif kontrolü PRISTINE config ile karşılaştır.** Sahte bir kimlik satırı
   ekleyip "yakalanmadı" görmek tek başına *allowlist çok geniş* demek değildir —
   kural o şekli hiç tanımıyor da olabilir. Aynı probe'u eski konfigle koştur:
   fark yoksa probe kusurlu, fark varsa allowlist geniş.

## 4. Belgeler bayat-varsayılandır

- **Handoff / önceki oturum özeti / yerel branch güvenilmez.** Oturum başında:
  `git fetch`, `git log --oneline origin/main -6`, `gh pr list --state all`
  (`gh` yoksa `mcp__github__list_pull_requests`).
- `CLAUDE.md` §Current position **elle** yazılır; içindeki **HEAD sha'sı yapısal
  olarak bayattır** (kapanış commit'inin kendisi onu değiştirir).
- Bir belgenin güncel mi tarihsel mi olduğunu ilk satırındaki
  `<!-- doc-status: … -->` işareti söyler.
- `docs/audit/current_main_ground_truth_2026-08-03.md` §18'in 2/3/4/6 kalemleri
  ADIM 5–8 ile kapandı ama **o belge güncellenmedi** — güvenmeden önce doğrula.

## 5. Çift kullanılmış ADIM numaraları — ek ZORUNLU

Numaralar bilerek yeniden atanmadı (merge edilmiş PR başlıkları ve commit
mesajları değiştirilemez). Ayrım **başlık ekiyle** yapılır — yeni kayıt yazarken
bu ekleri **aynen** kullan:

- `ADIM 16 (sevk edilen)` = item intent katmanı (#571/#572)
- `ADIM 16 (ADR §12)` = `run_engine` resumable stepper (#602)
- `ADIM 21 (worker delivery)` = at-least-once delivery guard (#587)
- planlı `ADIM 21` = `ItemParticipant`

Eksiz "ADIM 16" **tek anlamlı değildir**. main'de iki rakip ADIM 16 kickoff
dosyası yan yana durur; hangisinin otorite olduğu **insan kararıdır**.

## 6. Dürüst sınır dili — "kapalı" demeden önce

Bir işi `Complete` / `PASS` / `Done` göstermeden önce **kanıt** iste. Repo'da
kanıtsız kapatma geçmişi var:

- **A-08 denetimi YAPILMADI** — defter boş, dört çıkış kriteri de ☐; izleme
  issue #514 kanıtsız kapatıldı, yeniden açıldı, yine kanıtsız kapatıldı.
  **Hiçbir belge A-08'i Complete gösteremez.** Kapatma yetkisi **insandadır**;
  agent kapatamaz.
- Ekran okuyucu (NVDA/VoiceOver) denetimi hâlâ yapılmadı — ADIM 28 yalnız
  **iskeleyi** kurdu.
- `scripts/e2e-acceptance.sh flows` bir **CI kapısı değil** → sunucu katmanı
  regresyonu sessizce dönebilir.
- Kalan 45 düğüm imza-mavisi **D-10 (2026-07-30) imzalı kalıcı sapmadır**;
  WCAG 2.2 AA 1.4.3 **karşılanmıyor**.

İşaretlenmemiş kestirme = gizli borç. Bilinçli sadeleştirmeyi kod içinde
`# ponytail:` yorumu ile **ve** `PROJECT_HISTORY.md`'de *honest boundary* olarak
işaretle.

## Merge öncesi kısa liste

```
[ ] git fetch + origin/main taze mi
[ ] docs PR ise: git show <sha> -- docs/ | grep '^-## '  → bos
[ ] openapi --check ve repository_facts --check yesil
[ ] gh run view <id> (gh yoksa mcp__github__actions_get) → job sayisi > 0
[ ] "landed/closed" iddialarinin kaniti var
```
