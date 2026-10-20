---
name: entropia-frontend-parity
description: >
  Entropia frontend işinin sınırı: v18 mockup görsel otoritedir ve iş
  presentation-only'dir — route path, react-query key, OCC token, Idempotency-Key,
  hook'lar, SSE taksonomisi, API çağrıları ve lib/*.ts veri mantığı ellenmez.
  Sayfa/stil/etiket değiştirirken, mockup'a hizalarken, kırılan frontend testini
  onarırken, yeni bileşen eklerken oku. Backend sözleşmesi değişecekse bu skill
  DUR der.
license: MIT
---

# Entropia frontend parity — presentation-only sınırı

Her frontend/UI değişikliği görsel kaynağını
`docs/spec/index_guncellenmis_duzeltilmis_v18.html` (kanonik v18 mockup)
dosyasından alır. Tema `frontend/src/styles/global.css` değişkenlerinde:
`--accent:#00a9e8`, `--border:#cfcfcf`, `--radius:4px`, `--text:#222`, Arial.

Yerel önizleme (gitignore'lu, dev-only kopya — kanonik `docs/spec/` içinde kalır):

```bash
cp docs/spec/index_guncellenmis_duzeltilmis_v18.html frontend/public/mockup_v18.html
```

## ELLENMEYENLER — presentation işi bunlara dokunamaz

| Alan | Neden |
|---|---|
| Route path'leri | Backend sözleşmesi |
| react-query key'leri | Cache invalidation zinciri; SSE `EVENT_QUERY_KEYS` buna bağlı |
| OCC token'ları — `If-Match`, `expected_*_version`, `X-*-Version` | O-12; tek değerin iki yazımı, çelişki 409 |
| `Idempotency-Key` | O-13; retry semantiği |
| Hook'lar, API çağrıları, `lib/*.ts` veri mantığı | Veri katmanı, sunum değil |
| SSE event taksonomisi | `docs/CODEMAPS/JOBS_AND_EVENTS.md` |
| `app/nav.ts` NAV / ALL_NAV_ITEMS | **Birebir kalır** |

Bunlardan birinin değişmesi gerekiyorsa iş **presentation-only değildir** →
dur, kullanıcıya söyle, backend sözleşmesi tarafını ayrı ele al.

## Kırılan testi onarma kuralı

Test **YENİ markup'a hizalanır**, markup teste değil. Ama:

- **option değerleri değişmez**
- **OCC / Idempotency assertion'ları değişmez**
- yalnız **görünür etiket** ve **container kapsamı** (`aria-label` + `role`)
  güncellenir

Bir assertion'ı "artık geçmiyor" diye silmek regresyon gizlemektir.

## Erişilebilirlik — kapı CI'da

- Visual regression ve **axe-core ratchet** CI'da **bloklayıcıdır**.
- Kalan 45 düğüm imza-mavisi **D-10 (2026-07-30) imzalı kalıcı sapmadır**;
  **WCAG 2.2 AA 1.4.3 karşılanmıyor** — ürün bu ölçüt için uyumlu sayılamaz.
  Bunu "uyumlu" diye raporlama.
- Ekran okuyucu (NVDA/VoiceOver) denetimi **hâlâ yapılmadı**; iskele var
  (`scripts/a11y-audit-stack.sh`), defter **boş**.
- Yeni etkileşimli düğüm eklerken: klavye erişimi, görünür focus, `<button>` vs
  `<a>` ayrımı, modal focus trap + Escape.

## Doğrulama

```bash
cd frontend && npm run lint && npm run typecheck && npm run coverage && npm run build
```

- vitest için **`--no-file-parallelism` ZORUNLU**.
- Worktree'de `node_modules` yoksa önce `npm ci`; ilk koşudaki
  `ERR_MODULE_NOT_FOUND` test hatası değildir.
- Coverage eşikleri `frontend/vite.config.ts` — **kapıdır**, indirilmez.

## Bilinen kalıntı (yeni değil)

**F-07 raw-id sweep** — `display_label`, `source_package_name`, `item_label`,
`scope_label` + ortak `components/LabelledId.tsx` yerinde; pinli artefaktların
etiketi snapshot/manifest'ten gelir, canlı composition'dan **asla** join edilmez.
Açık kalıntı: `pages/PanelLogs.tsx:134` hâlâ id'den türetilmiş
`Backtest Result <id>` başlığını basıyor (Results History'de bilerek terk edildi).

## Harita

Sayfa → `lib/*.ts` → react-query key → endpoint grubu eşlemesi:
`docs/CODEMAPS/FRONTEND_MAP.md`. Bir sayfaya ilk kez dokunuyorsan **önce onu oku**.
