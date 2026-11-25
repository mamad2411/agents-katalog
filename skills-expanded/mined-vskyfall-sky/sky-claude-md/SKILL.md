---
name: sky-claude-md
description: >-
  Proje için CLAUDE.md (ve AGENTS.md) yazma ve bakımı: projeyi Claude'a 2 dakikada tanıtan
  yapı (amaç, stack, komutlar, klasör haritası, kurallar, yasaklar, doğrulama adımları), Sky
  skill'lerine bağlama, kısa ve güncel tutma, alt klasör CLAUDE.md'leri, takım kuralları ve
  yaygın hatalar. "CLAUDE.md yaz", "Claude projeyi anlamıyor", "proje kuralları", "AI için
  proje dokümanı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · CLAUDE.md

CLAUDE.md her oturumda okunur: **kısa, somut, güncel** olmalı. Uzun mimari roman değil; Claude'un tahmin edemeyeceği şeyler.

## Şablon

```markdown
# <Proje adı>

<Tek cümle: ne, kimin için.>  Canlı: https://…  ·  Staging: https://staging…

## Stack
Next.js 16 (App Router) · TypeScript strict · Tailwind v4 + shadcn/ui · Drizzle + Postgres (Supabase) · Better Auth · Vitest + Playwright · pnpm

## Komutlar
- `pnpm dev` — geliştirme (http://localhost:3000)
- `pnpm typecheck && pnpm lint && pnpm test` — her değişiklikten sonra
- `pnpm test:e2e` — kritik akışlar (dev server açık olmalı)
- `pnpm db:generate && pnpm db:migrate` — şema değişikliği sonrası
- `pnpm db:seed` — test verisi (test kullanıcıları: seed.ts içinde)

## Klasör haritası
- `src/app/(marketing)` landing · `src/app/(app)/o/[slug]` uygulama (org bazlı)
- `src/server/services` iş mantığı (yetki burada) · `src/server/db/schema.ts` şema
- `src/components/ui` tasarım sistemi (cva) · `src/styles/globals.css` token'lar

## Kurallar
- UI metinleri Türkçe, **sen** dili (bkz. Sky `sky-ux-writing`). Kod/commit İngilizce.
- Her server action: `requireMember(orgId)` + Zod. Yetki serviste.
- Renk/boşluk yalnızca token; keyfi Tailwind değeri yok.
- Para kuruş (int), tarih timestamptz; gösterim `src/lib/format.ts`.
- Yeni tablo → RLS politikası + `org_id` indeksi.

## Yapma
- `pnpm db:push` prod'a karşı · `.env` dosyalarını düzenleme · `src/components/ui`'yi shadcn CLI ile ezme
- Ödeme kodunda test anahtarı dışında anahtar kullanma

## Doğrulama
UI değişikliği: tarayıcıda 375px ve 1280px, açık/koyu tema. Bitmeden önce `/sky:sky-check`.

## Sky
Bu proje Sky kurallarını izler: `/sky:sky <görev>` ile başla. Özellikle: sky-nextjs, sky-supabase, sky-scheduling, sky-tr-integrations.
```

## Kurallar

- **≤ 150 satır**. Uzun dokümanlar `docs/`'ta; CLAUDE.md onlara bağlantı verir ("Ödeme akışı: docs/payments.md").
- Somut: "testleri çalıştır" değil `pnpm test -- src/server`. "İyi kod yaz" gibi genel tavsiye yok.
- **Proje-özgü tuzaklar** en değerli satırlardır: "Takvim saatleri `Europe/Istanbul`'da saklanır, UTC değil (eski karar, bkz. ADR-004)".
- Gizli bilgi yok (anahtar, parola, müşteri verisi).
- Alt klasörlerde ek CLAUDE.md (ör. `apps/mobile/CLAUDE.md`) — yalnızca o alana özgü kurallar.
- AGENTS.md (diğer AI araçları için) gerekiyorsa aynı içerik; birini diğerine bağla, iki kopya tutma.

## Bakım

- Claude aynı hatayı iki kez yaptıysa → CLAUDE.md'ye bir satır.
- Komut/klasör değişince güncelle (PR kontrol listesine ekle).
- Üç ayda bir oku ve eskimiş satırları sil — eskimiş kural yanlış kuraldan daha tehlikeli.

## Yaygın hatalar

Çok uzun (Claude önemliyi kaçırır), README kopyası, güncel olmayan komutlar, "her zaman X yap" ile çelişen başka satır, tüm stack'in ders kitabı açıklaması.
