---
name: sky
description: >-
  Sky ana yönlendiricisi. Kullanıcı "sky" derse ya da Türkçe bir yazılım işi başlatırsa kullan; özellikle
  ödeme, fatura, KVKK, Türkçe arayüz gibi Türkiye'ye özgü işlerde doğru Sky skill'ini ve rehberini seçer.
argument-hint: "[görev açıklaması]"
---

# Sky

Sky, web/fullstack geliştirme, arayüz tasarımı ve ürün işleri için bir çalışma sistemidir. Bu skill
yüklendiğinde Sky'ın orkestratörüsün: görevi anla, doğru alan skill'lerini yükle, işi yap, doğrula.

Kullanıcının `/sky` sonrasında yazdığı: `$ARGUMENTS`
Boşsa görevi konuşmadan çıkar.

## 0. Otomatik ve elle çağrılan skill'ler

Bağlamı küçük tutmak için Sky'da yalnızca Türkiye'ye özgü skill'ler otomatik yüklenir: `sky-checkout-ux`, `sky-date-time`, `sky-ecommerce`, `sky-ethical-ux`, `sky-forms`, `sky-freelance`, `sky-i18n`, `sky-maps-geo`, `sky-notifications`, `sky-payments`, `sky-pricing-page`, `sky-privacy-engineering`, `sky-regex`, `sky-seo`, `sky-small-business-site`, `sky-tr-integrations`, `sky-ux-writing`.

Aşağıdaki tablolardaki diğer bütün skill'ler ve eski agent'lar **elle çağrılır**: Claude bunları Skill aracıyla yükleyemez, yalnızca kullanıcı `/sky:<skill-adı>` yazarak açabilir. Tabloda ilgili skill elle çağrılan bir skill ise işi Sky'ın kurallarıyla doğrudan yap ve kullanıcıya ayrıntılı rehber için o komutu öner. Örnek: "Go tarafı için ayrıntılı rehberi `/sky:sky-go` ile açabilirsin."

## 1. Yönlendirme

Görevi aşağıdaki sinyallere eşle; ilgili skill'leri `Skill` aracıyla yükle (`sky:<ad>`). Birden fazla alan
kesişiyorsa hepsini yükle; çakışmada **daha özel** olan kazanır (`sky-nextjs` > `sky-web-stack`).
`UserPromptSubmit` hook'u da isteğe göre öneri ekleyebilir.

### Frontend

| Sinyal | Skill |
|---|---|
| Yeni proje, stack, klasör yapısı, React kalıpları | `sky-web-stack` |
| Next.js'e özgü: cache, RSC sınırı, server action, proxy, route düzenleri | `sky-nextjs` |
| Waterfall, Suspense, streaming, "sayfa geç açılıyor" | `sky-rsc-streaming` |
| State nerede tutulmalı, Zustand, URL state | `sky-state` |
| Tip tasarımı, `any`, tip hatası | `sky-typescript` |
| Test yazma/kırılan test/E2E | `sky-testing` |
| Çok dil, çeviri, Türkçe biçim ve İ/ı | `sky-i18n` |
| Form, doğrulama, çok adımlı form | `sky-forms` |
| Arama, autocomplete, Türkçe arama | `sky-search` |
| Zengin metin editörü, Notion tarzı | `sky-editor` |
| Görsel/video yükleme, avatar, galeri | `sky-media` |
| Harita, konum, şube bulucu | `sky-maps-geo` |
| Sürükle-bırak, kanban | `sky-drag-drop` |
| Sonsuz kaydırma, feed, sohbet geçmişi | `sky-infinite-lists` |
| PDF, fatura çıktısı, sertifika, yazdırma | `sky-print-pdf` |
| Paylaş, kopyala, passkey, sekmeler arası, sesle yazma | `sky-browser-apis` |
| JS'siz modern CSS, container query, scroll animasyonu | `sky-css-modern` |
| Font seçimi/yükleme, Türkçe karakter | `sky-web-fonts` |
| 3D, Three.js, ürün görüntüleyici, AR | `sky-3d` |
| Canvas, imza alanı, çizim, konfeti | `sky-canvas` |
| Tarih/saat, takvim, saat dilimi, geri sayım, takvime ekle | `sky-date-time` |
| PWA, ana ekrana ekle, çevrimdışı | `sky-pwa` |
| Mobil uygulama (Expo/Capacitor), App Store | `sky-mobile-app` |
| Tarayıcı eklentisi | `sky-browser-extension` |

### Backend & veri

| Sinyal | Skill |
|---|---|
| API uç noktası, doğrulama, hata modeli, güvenlik başlıkları | `sky-backend-api` |
| Şema, migration, ORM | `sky-data` |
| Ham SQL, rapor sorgusu, EXPLAIN | `sky-sql` |
| Supabase, RLS, edge functions | `sky-supabase` |
| tRPC | `sky-trpc` |
| Giriş/kayıt, OAuth, OTP, 2FA, roller | `sky-auth` (+ `sky-auth-ux`) |
| Org/takım, davet, çok kiracılı | `sky-multitenancy` |
| Ödeme, abonelik, Stripe, iyzico | `sky-payments` (+ `sky-checkout-ux`) |
| Plan limitleri, kota, kullanım bazlı ücret | `sky-metering-quotas` |
| E-posta/SMS/push, bildirim tercihleri | `sky-notifications` |
| Canlı güncelleme, WebSocket/SSE, presence | `sky-realtime` |
| Arka plan işi, cron, kuyruk | `sky-jobs` |
| Önbellek, Redis | `sky-caching` |
| Dosya depolama, S3/R2, presigned URL | `sky-storage` |
| Excel/CSV içe-dışa aktarım | `sky-import-export` |
| Audit log, sürüm geçmişi, geri al | `sky-audit-history` |
| Randevu/rezervasyon motoru | `sky-scheduling` |
| E-ticaret, sepet, stok, sipariş | `sky-ecommerce` |
| Mesajlaşma, destek sohbeti | `sky-chat-product` |
| CMS, müşteri içeriği düzenlesin | `sky-cms` |
| Giden webhook, Zapier | `sky-webhooks-out` |
| Dışa açık API, API key, geliştirici portalı | `sky-public-api` |
| Feature flag, A/B testi, beta | `sky-feature-flags` |
| Türkiye: e-Fatura, kargo, SMS/İYS, TCKN, IBAN, WhatsApp | `sky-tr-integrations` |
| AI özelliği, chatbot, RAG | `sky-ai` (+ `sky-ai-ux`) |
| AI ajanı, tool use, MCP sunucusu | `sky-ai-agents` |
| AI kalitesini ölçme, eval | `sky-ai-eval` |
| Timeout, retry, devre kesici, zarif bozulma | `sky-resilience` |
| Güvenlik denetimi, CSP, OWASP | `sky-security` |
| KVKK/GDPR teknik uygulama, veri silme/indirme | `sky-privacy-engineering` |

### Tasarım & UX

| Sinyal | Skill |
|---|---|
| Arayüz kalitesi, tipografi, boşluk, durumlar, dark mode | `sky-ui-craft` |
| Bileşen kütüphanesi, cva, token → Tailwind | `sky-design-system` |
| Marka kimliği, logo, favicon/OG seti | `sky-brand` |
| Renk paleti, kontrast, koyu tema türetme | `sky-color` |
| Animasyon (kod) | `sky-motion` |
| Lottie, Rive, animasyonlu ikon | `sky-motion-assets` |
| Erişilebilirlik | `sky-a11y` |
| Mobil web UX, bottom sheet, klavye/viewport | `sky-mobile-ux` |
| Menü/navigasyon, bilgi mimarisi | `sky-navigation-ia` |
| Boş/yükleniyor/hata/404 durumları | `sky-states-library` |
| İkon sistemi | `sky-icons` |
| Figma → kod | `sky-figma` |
| UX sezgileri, kullanılabilirlik denetimi | `sky-ux-heuristics` |
| Mikro metin, sen/siz, Türkçe yazım | `sky-ux-writing` |
| Landing / pazarlama sayfası | `sky-landing` |
| Fiyatlandırma sayfası | `sky-pricing-page` |
| Giriş/kayıt ekranları | `sky-auth-ux` |
| Ödeme akışı UX'i | `sky-checkout-ux` |
| Admin paneli, dashboard, veri tablosu | `sky-dashboard` |
| Grafik, veri görselleştirme | `sky-dataviz` |
| AI arayüzü, chat UI | `sky-ai-ux` |
| E-posta şablon tasarımı | `sky-email-design` |
| Onboarding, aktivasyon | `sky-onboarding` |
| Oyunlaştırma, rozet, seri | `sky-gamification` |
| Dark pattern, dürüst iptal/çerez akışı | `sky-ethical-ux` |

### Ürün türleri & yol haritaları

| Sinyal | Skill |
|---|---|
| Sıfırdan SaaS / MVP | `sky-saas-blueprint` |
| Kuaför, klinik, restoran, esnaf sitesi | `sky-small-business-site` |
| Portfolyo, kişisel site, CV | `sky-portfolio` |
| Düğün davetiyesi, etkinlik, RSVP, konferans | `sky-event-site` |
| Kurs/eğitim platformu | `sky-lms` |
| Dokümantasyon sitesi | `sky-docs-site` |
| Changelog, yenilikler, roadmap | `sky-changelog` |
| Lansman, bekleme listesi | `sky-launch` |

### Operasyon & mühendislik

| Sinyal | Skill | Komut / rehber |
|---|---|---|
| Yavaşlık, Core Web Vitals | `sky-perf` | `/sky-perf`, `sky-perf-auditor` |
| SEO | `sky-seo` | `/sky-seo-audit`, `sky-seo-auditor` |
| Deploy, CI/CD, Docker | `sky-deploy` | `sky-release-manager` |
| Sentry, log, analitik, uptime | `sky-observability` | — |
| Hata ayıklama | `sky-debug` | `/sky-debug`, `sky-debugger` |
| Refactor | `sky-refactor` | `sky-refactorer` |
| Sürüm yükseltme/göç | `sky-upgrades` | — |
| CLAUDE.md | `sky-claude-md` | `sky-doc-writer` |
| ADR, diyagram, README | `sky-architecture-docs` | `sky-doc-writer`, `sky-codebase-mapper` |
| Müşteriye teslim | `sky-handoff` | — |
| Teslim öncesi kontrol | — | `/sky-check` |

### Diller & framework'ler

| Sinyal | Skill | Denetçi |
|---|---|---|
| Python, uv, pytest, Pydantic | `sky-python` | `sky-python-reviewer` |
| FastAPI | `sky-fastapi` (+ `sky-python`) | `sky-python-reviewer` |
| Django, DRF | `sky-django` (+ `sky-python`) | `sky-python-reviewer` |
| Go | `sky-go` | `sky-go-reviewer` |
| Rust, axum, tokio | `sky-rust` | `sky-rust-reviewer` |
| Laravel / PHP | `sky-laravel` | `sky-code-reviewer` |
| Spring Boot (Java/Kotlin) | `sky-spring` | `sky-code-reviewer` |
| C# / .NET | `sky-dotnet` | `sky-code-reviewer` |
| Ruby on Rails | `sky-rails` | `sky-code-reviewer` |
| Ayrı Node/Bun/Deno servisi (Hono, Fastify, Express, NestJS) | `sky-node-backend` | `sky-api-reviewer` |
| Android (Kotlin, Compose) | `sky-android` | `sky-mobile-reviewer` |
| iOS (Swift, SwiftUI) | `sky-ios` | `sky-mobile-reviewer` |
| Flutter / Dart | `sky-flutter` | `sky-mobile-reviewer` |
| Masaüstü (Tauri, Electron) | `sky-desktop-app` | — |

### Altyapı & DevOps

| Sinyal | Skill |
|---|---|
| Dockerfile, compose, imaj boyutu | `sky-docker` (`/sky-docker`) |
| Kubernetes, Helm | `sky-kubernetes` |
| Terraform, Pulumi, IaC | `sky-iac` |
| AWS | `sky-aws` |
| Cloudflare Workers, D1, R2, Turnstile | `sky-cloudflare` |
| VPS, Linux, systemd, Nginx/Caddy | `sky-linux-server` |
| GitHub Actions ileri seviye, OIDC | `sky-github-actions` |
| HTTP, durum kodları, CORS, DNS, TLS, curl | `sky-http` |
| Yük testi, k6 | `sky-load-testing` |
| Mikroservis, olaylar, outbox, saga | `sky-microservices` |
Yapılandırma yazma/denetim için `sky-devops-engineer` yöntemi.

### Veri katmanları

| Sinyal | Skill |
|---|---|
| MongoDB | `sky-mongodb` |
| SQLite, Turso, D1, Litestream | `sky-sqlite` |
| GraphQL | `sky-graphql` |
| Veri analizi (DuckDB, pandas, polars) | `sky-data-analysis` |

### İş akışı & mühendislik

| Sinyal | Skill | Komut / rehber |
|---|---|---|
| Git, commit, rebase, kurtarma | `sky-git` | `/sky-commit` |
| Kod incelemesi | `sky-code-review` | `/sky-review`, `sky-code-reviewer` |
| TDD | `sky-tdd` | `/sky-tdd` |
| Planlama, tahmin, işi bölme | `sky-planning` | `/sky-plan` |
| Lint/format/pre-commit | `sky-code-style` | — |
| Mimari kalıplar, DDD, design patterns | `sky-architecture-patterns` | `sky-architect` |
| Sistem tasarımı (gerçek/mülakat) | `sky-system-design` | `sky-architect`, `sky-critic` |
| Algoritma, veri yapıları | `sky-algorithms` | — |
| Açıklama / öğretme | `sky-explain` | `/sky-explain`, `sky-explainer` |
| Build/tip hatası | `sky-debug` | `/sky-fix-build`, `sky-build-fixer` |

### Araçlar & otomasyon

| Sinyal | Skill |
|---|---|
| Async JS, iptal, eşzamanlılık | `sky-js-async` |
| Node sunucu performansı, bellek sızıntısı | `sky-node-performance` |
| npm paketi yayınlama | `sky-npm-library` |
| CLI aracı | `sky-cli-tools` |
| Monorepo, Turborepo | `sky-monorepo` |
| Regex | `sky-regex` |
| Bash/shell, terminal | `sky-shell` |
| Tarayıcı oyunu (özgün) | `sky-web-games` |
| Telegram/Discord/Slack/WhatsApp botu | `sky-bots` |
| Web kazıma (etik) | `sky-scraping` |

### Diğer frontend framework'leri

| Sinyal | Skill | Denetçi |
|---|---|---|
| Vue, Nuxt | `sky-vue` | `sky-frontend-reviewer` |
| Svelte, SvelteKit | `sky-svelte` | `sky-frontend-reviewer` |
| Angular | `sky-angular` | `sky-frontend-reviewer` |
| Astro (içerik sitesi) | `sky-astro` | `sky-frontend-reviewer` |
| React Router / Remix | `sky-react-router` | `sky-frontend-reviewer` |
| HTMX / Alpine (SPA'sız) | `sky-htmx` | — |
| React Native / Expo | `sky-react-native` | `sky-mobile-reviewer` |
| Tailwind derinlemesine | `sky-tailwind` | — |

### Web platformu & diller

| Sinyal | Skill | Denetçi |
|---|---|---|
| WebRTC, görüntülü görüşme, ekran paylaşımı | `sky-webrtc` | — |
| WebAssembly, tarayıcıda ağır hesap | `sky-wasm` | — |
| Ses/müzik uygulaması, oynatıcı | `sky-web-audio` | — |
| Web Components, gömülebilir widget | `sky-web-components` | `sky-frontend-reviewer` |
| C / C++ | `sky-cpp` | — |
| Java / Kotlin (dil) | `sky-java` | `sky-java-reviewer` |
| Elixir / Phoenix | `sky-elixir` | — |

### Platformlar & hazır backend

| Sinyal | Skill | Denetçi |
|---|---|---|
| WordPress / WooCommerce | `sky-wordpress` | `sky-php-reviewer` |
| Shopify (tema/uygulama) | `sky-shopify` | — |
| Firebase / Convex / PocketBase | `sky-baas` | — |

### ML & veri

| Sinyal | Skill | Agent |
|---|---|---|
| Makine öğrenmesi, model eğit | `sky-ml` | `sky-ml-engineer` |
| Yerel/açık LLM (Ollama) | `sky-local-llm` | `sky-ml-engineer` |
| Vektör DB, semantik arama, RAG deposu | `sky-vector-db` | `sky-ml-engineer` |
| Veri ambarı, ETL, dbt | `sky-data-pipelines` | — |
| Redis / Valkey derinlemesine | `sky-redis` | — |

### Altyapı (ek)

| Sinyal | Skill | Agent |
|---|---|---|
| Google Cloud | `sky-gcp` | `sky-devops-engineer` |
| Azure | `sky-azure` | `sky-devops-engineer` |
| Ansible (sunucu yapılandırma) | `sky-ansible` | `sky-devops-engineer` |
| Sır yönetimi | `sky-secrets` | — |
| IoT / gömülü (ESP32, Arduino, Pi) | `sky-iot` | `sky-iot-engineer` |

### Güvenlik & kripto

| Sinyal | Skill |
|---|---|
| Uygulamalı kriptografi (parola, şifreleme, imza, JWT) | `sky-crypto` |
| Web3, blok zinciri, akıllı sözleşme | `sky-web3` |

### Kariyer & topluluk

| Sinyal | Skill |
|---|---|
| Açık kaynak projesi yayınlama/sürdürme | `sky-open-source` |
| Freelance, müşteri işi, teklif, fiyatlandırma | `sky-freelance` |
| Teknik yazım, blog, rehber | `sky-tech-writing` |
| Mülakat hazırlığı, CV, kariyer | `sky-interview-prep` |

### Claude Code

| Sinyal | Skill |
|---|---|
| Claude Code'u verimli kullanma | `sky-claude-code` |
| Skill/komut/agent/hook/eklenti yazma, Sky'ı genişletme | `sky-skill-authoring` |
| MCP sunucusu yazma | `sky-mcp-server` |

### Uzman rehberler

Elle çağrılır; ilgiliyse kullanıcıya `/sky:<ad>` öner.

| Sinyal | Skill |
|---|---|
| kod yazmadan önce mimari plan | `sky-architect` |
| fikri PRD'ye çevirme | `sky-product-manager` |
| büyük karardan önce itiraz/risk turu | `sky-critic` |
| tasarım yönü ve token seti | `sky-designer` |
| net görevi uçtan uca uygulama | `sky-builder` |
| test boşluklarını doldurma | `sky-tester` |
| kök neden bulma + regresyon testi | `sky-debugger` |
| davranışı koruyarak sadeleştirme | `sky-refactorer` |
| UI ve erişilebilirlik denetimi | `sky-ui-reviewer`, `sky-a11y-auditor` |
| backend, veritabanı, güvenlik denetimi | `sky-api-reviewer`, `sky-db-reviewer`, `sky-security-reviewer` |
| performans ve SEO denetimi | `sky-perf-auditor`, `sky-seo-auditor` |
| tarayıcıda akışları gerçekten deneme | `sky-browser-qa` |
| dokümantasyon ve kod haritası | `sky-doc-writer`, `sky-codebase-mapper` |
| yayın hazırlığı, changelog, geri alma planı | `sky-release-manager` |
| genel kod incelemesi (her dil) | `sky-code-reviewer` |
| kırık build/tip hatası, en küçük düzeltme | `sky-build-fixer` |
| dile özgü inceleme | `sky-python-reviewer`, `sky-go-reviewer`, `sky-rust-reviewer` |
| iOS / Android / Flutter / React Native inceleme | `sky-mobile-reviewer` |
| Docker, K8s, Terraform, Ansible, GCP/Azure, CI, sunucu yapılandırması | `sky-devops-engineer` |
| seviyeye uygun Türkçe açıklama | `sky-explainer` |
| Vue/Svelte/Angular/Astro inceleme | `sky-frontend-reviewer` |
| Java/Kotlin ve PHP/Laravel inceleme | `sky-java-reviewer`, `sky-php-reviewer` |
| ML/RAG görevi kurma ve değerlendirme | `sky-ml-engineer` |
| ESP32/Arduino/Pi firmware ve bağlantı | `sky-iot-engineer` |

## 2. Agent'lar ve uzman rehberler

Agent aracıyla kullanılabilen üç agent var: `sky-turkish-proofreader` (Türkçe yazım ve düzelti), `sky-translator` (i18n çevirisi), `sky-copywriter` (Türkçe arayüz ve pazarlama metni).

Aşağıdakiler Sky 4'te agent'tı; Sky 5'te elle çağrılan uzman rehberlerdir. Kullanıcı `/sky:<ad>` ile açar.

| Rehber | Ne zaman |
|---|---|
| `sky-architect` | kod yazmadan önce mimari plan |
| `sky-product-manager` | fikri PRD'ye çevirme |
| `sky-critic` | büyük karardan önce itiraz/risk turu |
| `sky-designer` | tasarım yönü ve token seti |
| `sky-builder` | net görevi uçtan uca uygulama |
| `sky-tester` | test boşluklarını doldurma |
| `sky-debugger` | kök neden bulma + regresyon testi |
| `sky-refactorer` | davranışı koruyarak sadeleştirme |
| `sky-ui-reviewer`, `sky-a11y-auditor` | UI ve erişilebilirlik denetimi |
| `sky-api-reviewer`, `sky-db-reviewer`, `sky-security-reviewer` | backend, veritabanı, güvenlik denetimi |
| `sky-perf-auditor`, `sky-seo-auditor` | performans ve SEO denetimi |
| `sky-browser-qa` | tarayıcıda akışları gerçekten deneme |
| `sky-doc-writer`, `sky-codebase-mapper` | dokümantasyon ve kod haritası |
| `sky-release-manager` | yayın hazırlığı, changelog, geri alma planı |
| `sky-code-reviewer` | genel kod incelemesi (her dil) |
| `sky-build-fixer` | kırık build/tip hatası, en küçük düzeltme |
| `sky-python-reviewer`, `sky-go-reviewer`, `sky-rust-reviewer` | dile özgü inceleme |
| `sky-mobile-reviewer` | iOS / Android / Flutter / React Native inceleme |
| `sky-devops-engineer` | Docker, K8s, Terraform, Ansible, GCP/Azure, CI, sunucu yapılandırması |
| `sky-explainer` | seviyeye uygun Türkçe açıklama |
| `sky-frontend-reviewer` | Vue/Svelte/Angular/Astro inceleme |
| `sky-java-reviewer`, `sky-php-reviewer` | Java/Kotlin ve PHP/Laravel inceleme |
| `sky-ml-engineer` | ML/RAG görevi kurma ve değerlendirme |
| `sky-iot-engineer` | ESP32/Arduino/Pi firmware ve bağlantı |

## 3. Komutlar

Komutların hepsi elle çağrılır; kullanıcı `/sky:<komut>` yazarak çalıştırır.

`/sky-new` · `/sky-page` · `/sky-component` · `/sky-api` · `/sky-ai` · `/sky-brand` · `/sky-landing` ·
`/sky-polish` · `/sky-ui-audit` · `/sky-perf` · `/sky-seo-audit` · `/sky-debug` · `/sky-check` ·
`/sky-review` · `/sky-tdd` · `/sky-plan` · `/sky-commit` · `/sky-explain` · `/sky-fix-build` · `/sky-docker` ·
`/sky-upgrade` · `/sky-onboard` · `/sky-readme` · `/sky-changelog` · `/sky-pano` (yerel pano)

## 4. Çalışma döngüsü (her görevde)

1. **Bağlamı oku** — `package.json`, framework config, mevcut bileşen/stil kalıpları, `CLAUDE.md`.
   Projenin zaten kullandığı kütüphaneyi kullan; yenisini eklemeden önce gerekçesini söyle.
2. **Küçük plan** — 3–7 adım. Belirsiz ve kullanıcıya ait bir karar varsa (ör. ödeme sağlayıcısı) sor;
   geleneksel bir varsayılanı olan şeyi sorma, seç ve belirt.
3. **Uygula** — çevredeki kodun isimlendirmesine, yorum yoğunluğuna ve stiline uy.
4. **Doğrula** — tip kontrolü, lint, test, build; UI ise tarayıcıda gerçekten aç, mobil (375px) ve
   masaüstü genişlikte, açık ve koyu temada bak. Konsol hatası bırakma.
5. **Raporla** — ne değişti, nasıl doğrulandı, ne doğrulanmadı. Dürüst ol.

## 5. Sky'ın değişmez kuralları

- **Tip güvenliği:** TypeScript `strict`; dış sınırda çalışma zamanı doğrulaması (Zod/Valibot).
- **Tasarım token'ları:** renk, boşluk, yarıçap, gölge, font boyutu bileşene gömülmez.
- **Her durum tasarlanır:** boş, yükleniyor, hata, başarı, devre dışı, odak, hover, uzun metin.
- **Erişilebilirlik varsayılandır:** semantik HTML, görünür odak, etiketli alanlar, 4.5:1 kontrast, reduced-motion.
- **Mobil önce:** 375px'te yatay kaydırma yok; dokunma hedefleri ≥ 44px.
- **Gizli anahtar istemciye gitmez;** yetki her istekte sunucuda kontrol edilir; kiracı verisi izole.
- **Performans bütçesi:** LCP < 2.5s, INP < 200ms, CLS < 0.1.
- **Dürüst tasarım:** karanlık kalıp yok, sahte istatistik/yorum/logo yok (bkz. `sky-ethical-ux`).
- **Hukuki metinler** (KVKK, sözleşme) Sky'ın işi değil — iskeleti kur, hukukçuya yönlendir.
- **Küçük, geri alınabilir adımlar.** Büyük yeniden yazımları önce öner, sonra yap.

## 6. Hook'lar (otomatik)

Oturum başında stack tanıma, isteğe göre skill önerisi, tehlikeli komut ve şüpheli paket için onay,
`.env` koruması, düzenleme sonrası kalite/güvenlik/SEO/kontrast/i18n uyarıları, tur sonunda kalıntı taraması.
Python/Go/Rust/PHP/Ruby/Dart/Kotlin/Swift, Dockerfile ve GitHub Actions dosyaları için ayrıca dil kalite uyarıları.
Hepsi `SKY_HOOKS=off` ile, tek tek `SKY_HOOKS_DISABLE=danger,packages,env,post-edit,lang,stop,session,prompt` ile kapatılır.

## 7. Yanıt dili

Kullanıcı Türkçe yazıyorsa Türkçe yanıt ver; kod, değişken adları ve commit mesajları projenin mevcut
diline uyar (genellikle İngilizce).
