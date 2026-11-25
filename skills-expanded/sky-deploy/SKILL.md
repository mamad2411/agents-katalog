---
name: sky-deploy
description: >-
  Web uygulaması dağıtımı ve CI/CD: Vercel / Cloudflare / Docker+VPS (Coolify, Dokploy) /
  Fly / Railway seçimi, ortam değişkeni ve sır yönetimi, GitHub Actions pipeline (typecheck,
  lint, test, build, E2E), PR önizleme ortamları, veritabanı migration stratejisi, Next.js
  Dockerfile (standalone, çok aşamalı), reverse proxy ve TLS (Caddy), sıfır kesinti ve geri
  alma, alan adı/DNS, yedekleme, yayın kontrol listesi. "Deploy et", "canlıya al", "CI kur",
  "Dockerize", "VPS'e kur" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Dağıtım

## Hedef seçimi

| Durum | Öneri | Not |
|---|---|---|
| Next.js, hızlı, önizleme ortamı istiyorum | **Vercel** | ISR, edge, preview URL hazır; maliyet trafikle büyür; uzun süreli bağlantı (WS) yok |
| Statik/edge ağırlıklı, düşük maliyet | **Cloudflare Pages/Workers** (`@opennextjs/cloudflare`) | Node API kısıtları; R2/D1/KV ekosistemi |
| Tam kontrol, sabit maliyet, WS/arka plan iş | **VPS + Docker** (Hetzner/DigitalOcean) + **Coolify/Dokploy** | Sen yönetirsin: güvenlik güncellemeleri, yedek |
| Konteyner ama yönetilen | **Fly.io / Railway / Render** | Docker ver, ölçek/log/TLS onların |
| Veritabanı | **Neon / Supabase** (Postgres, serverless dostu) veya VPS'te Postgres + yedek | Serverless'ta bağlantı havuzu (pgBouncer/Neon pooler) şart |

Varsayılan: Vercel + Neon/Supabase. WebSocket/kuyruk işçisi gerekiyorsa ayrı küçük servis (Fly/Railway/VPS).

## Ortamlar ve env

- Üç ortam: **development** (lokal), **preview** (PR başına), **production**. Her birinin ayrı DB'si
  (preview'da Neon branch / Supabase branch ideal).
- Sırlar yalnızca platformun secret deposunda; repoda `.env.example` (değersiz anahtar listesi).
- `lib/env.ts` build/başlangıçta doğrular; eksik env ile deploy **başarısız olsun**, sessizce `undefined` ile çalışmasın.
- `NEXT_PUBLIC_*` build anında gömülür → preview ve prod için ayrı build; aynı imajı farklı env ile çalıştıramazsın
  (gerekiyorsa runtime config: sunucu bileşeninden prop olarak geçir).
- Prod anahtarlarını lokalde kullanma; `sk_live_`/`service_role` lokal `.env`de görünürse hook uyarır.
- Env değişimi = deploy; dokümante et (`docs/ENV.md`: ad, nerede kullanılıyor, kim sahip).

## CI: GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on: { pull_request: {}, push: { branches: [main] } }
concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck
      - run: pnpm lint
      - run: pnpm test --coverage
      - run: pnpm build
        env: { SKIP_ENV_VALIDATION: "1" }   # ya da CI'ya sahte env ver; build'de gerçek sır gerekmesin
  e2e:
    needs: check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps chromium
      - run: pnpm test:e2e
        env: { BASE_URL: ${{ github.event.deployment_status.target_url || 'http://localhost:3000' }} }
      - uses: actions/upload-artifact@v4
        if: failure()
        with: { name: playwright-report, path: playwright-report }
```
- `--frozen-lockfile`: kilit dosyası ile uyumsuzlukta hata.
- E2E'yi preview URL'sine karşı koşturmak en gerçekçisi (Vercel `deployment_status` olayı).
- Branch koruması: `check` zorunlu, en az 1 onay, `main`e doğrudan push kapalı.
- Dependabot/Renovate haftalık; güvenlik güncellemeleri otomatik PR.
- Sır taraması: `gitleaks` action'ı PR'da.

## Veritabanı migration

- Migration'lar repoda, CI'da sıfır DB'ye uygulanıp testler koşar.
- Deploy sırası: **migration → uygulama**. Vercel'de `build` komutuna `prisma migrate deploy &&` ekle
  (ya da ayrı "release" adımı); Docker'da entrypoint'te migrate, sonra start.
- Geriye uyumlu adımlar (expand → migrate → contract; bkz. `sky-data`): eski sürüm yeni şema ile çalışabilmeli,
  çünkü deploy sırasında ikisi aynı anda yaşar.
- Yıkıcı migration (drop/rename) **ayrı deploy**, bir önceki sürüm artık o sütunu kullanmıyorken.
- Prod'da `migrate dev`/`db push` **asla**; yalnızca `migrate deploy`.
- Uzun süren migration (büyük tablo indeksi) `CONCURRENTLY` ve bakım penceresi.

## Docker (Next.js standalone)

```dockerfile
FROM node:22-alpine AS base
RUN corepack enable
WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build                     # next.config: output: "standalone"

FROM node:22-alpine AS run
WORKDIR /app
ENV NODE_ENV=production PORT=3000 HOSTNAME=0.0.0.0
RUN addgroup -S app && adduser -S app -G app
COPY --from=build --chown=app:app /app/.next/standalone ./
COPY --from=build --chown=app:app /app/.next/static ./.next/static
COPY --from=build --chown=app:app /app/public ./public
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/api/health || exit 1
CMD ["node", "server.js"]
```
- `.dockerignore`: `node_modules`, `.next`, `.env*`, `.git`.
- İmaj etiketi = git SHA; `latest`e güvenme.
- Çok aşamalı → küçük imaj (~150MB). Sırlar `ARG` ile **gömülmez**; runtime env.
- `docker compose` lokal: app + postgres + (redis); prod'da Coolify/Dokploy aynı compose'u alır.

## Reverse proxy ve TLS (VPS)

Caddy en az yapılandırma:
```
example.com {
  encode zstd gzip
  reverse_proxy app:3000
  header {
    Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    X-Content-Type-Options nosniff
    Referrer-Policy strict-origin-when-cross-origin
  }
}
www.example.com { redir https://example.com{uri} permanent }
```
Otomatik Let's Encrypt. Nginx kullanıyorsan certbot + `proxy_set_header X-Forwarded-*`.
VPS temel güvenlik: SSH anahtar, parola girişi kapalı, `ufw` (22, 80, 443), otomatik güvenlik güncellemeleri, fail2ban.

## Sıfır kesinti ve geri alma

- Vercel: her deploy atomik; "Instant Rollback" ile önceki deploy'a dön; `main`e revert ile de.
- Docker: yeni konteyneri başlat → health check geçsin → trafiği çevir → eskiyi kapat (Coolify/Dokploy yapar;
  elle `docker compose up -d --no-deps --wait app`).
- Geri alma planı deploy'dan **önce** yazılı: hangi imaj, migration geri alınabilir mi (çoğu zaman: ileri düzeltme tercih).
- Feature flag ile riskli özelliği kapalı deploy et, sonra aç (env veya DB bayrağı).

## Alan adı ve DNS

- Apex `A/ALIAS` → platform; `www` → `CNAME`; biri diğerine 301.
- Vercel/Cloudflare'de alanı ekle, DNS'i doğrula; TTL'i geçişten önce düşür (300).
- E-posta gönderimi için SPF/DKIM/DMARC kayıtları (bkz. `sky-notifications`).
- `CAA` kaydı ile sertifika otoritesini kısıtla (isteğe bağlı).

## Yedekleme

- Yönetilen DB: PITR açık (Neon/Supabase planına bak); ek olarak günlük `pg_dump` → S3/R2 (30 gün).
- VPS Postgres: `pg_dump` cron + `restic`/`rclone` ile dış depolama; **geri yükleme testini** ayda bir yap.
- Kullanıcı dosyaları S3/R2'de versiyonlama açık.
- Yedek şifreli; erişim ayrı anahtar.

## Yayın kontrol listesi

- [ ] `sky-check` GEÇTİ; CI yeşil
- [ ] Env'ler prod'da tanımlı ve doğrulanıyor; test anahtarı yok
- [ ] Migration geriye uyumlu; sırası doğru
- [ ] `/api/health` çalışıyor; uptime izleme bağlı (bkz. `sky-observability`)
- [ ] Hata izleme (Sentry) release etiketiyle aktif; source map yüklü
- [ ] Güvenlik başlıkları ve HTTPS yönlendirme
- [ ] `robots.txt` prod'da izin veriyor, preview'da **engelliyor** (`X-Robots-Tag: noindex`)
- [ ] Alan adı, www yönlendirme, OG görselleri doğru URL'de
- [ ] Geri alma yolu biliniyor
- [ ] Deploy sonrası duman testi: ana sayfa, giriş, kritik akış (375px dahil)
