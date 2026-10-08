# Caelinus-World — Cursor / AI Agent Kuralları

> Bu dosya Cursor (ve diğer AI ajanların) projeyi sıfır karışıklıkla devralması için.
> Son güncelleme: 2026-06-18 (akşam) · Faz B ilerliyor: ten rengi + giydirme çalışıyor.

## 📣 Cursor'a not — devralırken oku (2026-06-18 akşam)
Bugün tamamlandı (detay: `docs/faz-b-durumu-ve-kalan-isler.md`):
- **Ten rengi çalışıyor** — gövdeye gerçek zamanlı uygulanıyor, saç/göz korunuyor.
- **Kıyafet giydirme çalışıyor** — kart tıkla → bind; avatar açılışta giyinik (ilk 3D kıyafet).
- **`-vr` türev üretildi** — `caelinus-body-base-fem-vr.glb` (UI'a henüz bağlı değil).
- **Mimari temizlik:** mesh-sayısı tahmini kaldırıldı → `BodyEntry.pipeline` + `isCaelinusBodyUrl()`.

**YARIN ÖNCELİK — kıyafet oturması:** Meshy GLB'leri rijit (skin'siz), tek kemiğe
yapışık → poz takip etmiyor, sarong uçuşuyor. Çözüm seçenekleri A/B/C için
`docs/faz-b-durumu-ve-kalan-isler.md` §1.5'e bak. **Şeyma karar verecek, sorma-yapma yok.**
`aries.glb` bozuk (zstd-blend) — geçerli GLB export edilene kadar önizleme-only.

## Dil & davranış
- **Türkçe konuş**, teknik terimleri İngilizce bırak. Kısa ve doğrudan cevap ver.
- **Dosyaları okumadan değişiklik önerme/yapma.**
- **Güvenlik açığı oluşturma:** XSS, SQL injection, command injection yok. Kullanıcı girdisini sanitize et.
- Müşteri (CaelinusAl) commit'leri RSS/atom feed'den görüyor → **commit mesajları dürüst** olmalı.

## Proje
- **Next.js 16 (Turbopack) + React 19 + TypeScript**, app router. App kökü repo kökünde.
- **3D avatar:** Three.js + React-Three-Fiber. Ana bileşen `components/shop/ModelAvatar.tsx`
  (SkeletonUtils.clone, Mixamo retarget, bone-scaling slider deform).
- **Supabase** backend. Env zorunlu: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  (yoksa `next build` page-data toplarken patlar; prod'da Vercel dashboard'da set edilir).

## Avatar GLB sözleşmesi (kontrat — bozma)
Kaynak: `docs/avatar-system-and-sema-brief.md` BÖLÜM 4. Kapı: `_tools/validate-avatar.js`.
- `-hires`: ≤ 60k tris, ≤ 2048² texture, **sıkıştırma YASAK** (motorda KTX2/Draco/Meshopt loader yok → ekran boş gelir).
- `-vr`: ≤ 25k tris, ≤ 1024², sıkıştırma serbest.
- **Mixamo bone isimleri** (`mixamorig:` prefix OK — motor `stripMixamo` ile normalize eder).
- **ARKit blendshape min-5** birebir: `eyeBlinkLeft/Right`, `jawOpen`, `mouthSmileLeft/Right`.
- **+Y up**, scale [1,1,1], **embed texture** (harici .png = 404).
- Her export sonrası: `node _tools/validate-avatar.js <dosya.glb>` → **KAPI AÇIK** olmadan teslim yok.
- Saç/animasyon **ayrı GLB** ver (base'le merge etme — rig kaybolur):
  - Saç: `public/models/hair/*.glb`, tek mesh + tek atlas + spring-bone zinciri (`Hair_01→02→03`), Head-bind.
  - Catwalk: `public/models/caelinus-catwalk.glb`, **in-place** (Hips translation kanalı yok).

## Mevcut durum (Faz A — tamam)
- **Selin** (`selin-v1`) default beden: `public/models/caelinus-body-base-fem.glb`
  — 14104 vert, 54 bone (göz bone dahil), 52 ARKit blendshape, gömülü PBR deri + göz texture.
- Gerçek göz: gözbebeği mesh + `mixamorig:LeftEye/RightEye` + iris/sclera atlas.
- Saç: `public/models/hair/hair-long-wave.glb`. Catwalk: `public/models/caelinus-catwalk.glb` (in-place).
- Kayıt: `lib/avatar-bodies.ts` (`CAELINUS_BODY_LIBRARY`, `DEFAULT_BODY_ID="selin-v1"`) + `public/avatars/manifest.json` (v0.7.0). `AVATARS_IN_PRODUCTION=false`.
- Blender çalışma dosyası: `_work/caelinus-body-base-fem.blend` (Blender 4.5.9 + MPFB 2.0.16).

## Faz B — yapılacaklar
- [x] Saç **runtime Head-bind** wiring — PR #5 (canlı: `✓ saç bind edildi → mixamorigHead`).
- [x] `-vr` ≤ 25k türev — `caelinus-body-base-fem-vr.glb` (UI'a bağlanması Faz E).
- [x] **Ten rengi (skin tone)** gövdeye uygulanıyor — `ModelAvatar.tsx` + `avatar-bodies.ts`.
- [ ] **Kıyafet oturması** (YARIN öncelik) — Meshy GLB'leri rijit; rig/tune/poz. §1.5.
- [ ] Yüz **ayrı material slot** (skin-tone'dan bağımsız yüz; şu an yüz gövde materyalinde).
- [ ] VRM 1.0 köprüsü (göz/parmak bone + ARKit + spring zaten hazır → ucuz gelir).

## Komutlar
- `npm run dev` → localhost:3000 · test: `/universe/shop/avatar`
- `npm run build` (env şart) · `npm run lint`
- `node _tools/validate-avatar.js public/models/<dosya>.glb` (GLB kapısı)

## Tuzaklar
1. Sıkıştırma verme (-hires). 2. Tek armature. 3. In-place anim (Hips=0). 4. Embed texture.
5. `selin-v1` id'si localStorage'da → **değiştirme**. 6. Export sonrası daima validate.
