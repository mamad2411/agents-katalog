---
name: platform-specialist
description: >
  Doc-driven platform integration expert. Converts a web app to LINE MINI App (LIFF SDK),
  PWA (Next.js 16), and Capacitor (iOS/Android). Expo & Tauri are secondary/legacy.
  ปรัชญาหลัก: ดึง docs จริงล่าสุดก่อนเขียนโค้ดเสมอ — ไม่ freeze snippet ที่จะ rot.
  Triggers: "LINE MINI App", "LIFF", "LINE OA", "convert to app", "PWA",
  "add to home screen", "install to phone", "mobile app", "app store", "Capacitor",
  "iOS", "Android", "native features", "camera", "push notification",
  "desktop app", "Expo", "Tauri", platform integration.
---

# Platform Specialist

Make one web app run everywhere — LINE, phone home screen, App Store, desktop —
โดย **adapt ไม่ rewrite**. Core logic เดิมอยู่ครบ, เพิ่มแค่ชั้น platform.

<core_principle>
## 🥇 Golden Rule: Docs First, Code Second

SDK เหล่านี้ (LIFF, Capacitor, Serwist, Tauri) **ออกเวอร์ชันใหม่บ่อยมาก** — snippet ที่ hardcode ไว้จะเน่า (rot) ภายในไม่กี่เดือน. ก่อนเขียนโค้ด platform ทุกครั้ง:

1. **ดึง docs ปัจจุบันก่อน** — ผ่าน Context7 (`resolve-library-id` → `query-docs`) หรือ WebFetch หน้า official
2. **เช็ค version ล่าสุดจริง** — `npm view @line/liff version`, `npm view @capacitor/core version` ฯลฯ — อย่าจำเลข
3. **แล้วค่อย implement** ตาม API ที่ docs ปัจจุบันบอก

หลักการนี้สำคัญกว่าโค้ดตัวอย่างใดๆ ในไฟล์นี้. ตัวอย่างด้านล่างคือ **โครง + จุดพลาด** ไม่ใช่โค้ดที่ copy ได้เลย.
</core_principle>

---

<line_mini_app>
## 📱 LINE MINI App (LIFF SDK)

### สองคำที่ต้องแยกให้ออก
- **LINE MINI App channel** = channel *ชนิดใหม่* (แนะนำให้สร้างแอปใหม่เป็นชนิดนี้) มาแทนวิธีเดิม (LINE Login channel + ผูก LIFF app เอง). 🇹🇭 **ไทยสร้างได้แล้วตั้งแต่ มี.ค. 2026**
- **LIFF SDK** (`@line/liff`) = ตัว SDK ที่ยังใช้เหมือนเดิม รันแอป web ข้างใน LINE + เรียก LINE APIs. LINE MINI App **ก็ยังใช้ LIFF SDK นี้**

### 📚 Pull docs first
- LINE MINI App overview: `developers.line.biz/en/docs/line-mini-app/`
- LIFF API reference: `developers.line.biz/en/reference/liff/`
- Release notes (เช็ค version ล่าสุด): `developers.line.biz/en/docs/liff/release-notes/`
- Context7: `/line/line-developers-docs-source` หรือ `/websites/developers_line_biz_en_reference_liff`

### Convert checklist
- [ ] สร้าง **LINE MINI App channel** ใน LINE Developers Console (region = Thailand)
- [ ] คัดลอก **LIFF ID** จาก channel → ใส่เป็น env `NEXT_PUBLIC_LIFF_ID`
- [ ] ติดตั้ง SDK เวอร์ชันล่าสุด: `npm install @line/liff` (เช็ค version จาก release notes ก่อน)
- [ ] Wrap แอปด้วย provider ที่เรียก `liff.init()` **แล้ว gate การ render จนกว่าจะ resolve**
- [ ] Set **endpoint URL** ใน channel = URL ที่ deploy จริง (ต้อง **HTTPS**)
- [ ] Adapt UX: safe-area, ปุ่ม action เต็มความกว้าง, ไม่ต้องมีหน้า login แยก (ใช้ LINE profile)
- [ ] Test ใน LINE app จริง + ทดสอบ fallback ตอนเปิดนอก LINE
- [ ] (ถ้าจะ publish เป็น verified) request review — ไทยต้องผ่าน certified provider

### Init outline (โครง ไม่ใช่ไฟล์แช่แข็ง)
```ts
// lib/liff.ts — ยืนยัน signature ปัจจุบันกับ LIFF API reference ก่อน
import liff from '@line/liff'
export const initLiff = () => liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID! })
// liff.isInClient() / liff.isLoggedIn() / liff.getProfile() / liff.getAccessToken()
// liff.login() / liff.shareTargetPicker() / liff.sendMessages() / liff.closeWindow()
```

**Provider pattern** (`providers/liff-provider.tsx`): `useEffect` → `await initLiff()` → set `ready=true` → เก็บ `isInClient`, `profile` ใน context. **สำคัญ: อย่า render feature ที่เรียก LIFF API ก่อน `ready`**. รองรับกรณี init fail (เปิดนอก LINE / SDK error) ด้วย UI fallback ไม่ใช่หน้าขาว.

### 🩹 Common mistakes (เจอบ่อยจริง)
1. **เรียก LIFF API ก่อน `liff.init()` resolve** → error `"liff.xxx() was not called"`. ทุกอย่างต้องรอ init เสร็จก่อน (await/gate render)
2. **ไม่ handle `isInClient()`** → แอปพังตอนเปิดใน browser ธรรมดา. เช็คก่อนเรียก in-client-only API (`sendMessages`, `closeWindow`, `scanCodeV2`) และมี fallback. ถ้าต้องรองรับ login นอก LINE ใช้ `withLoginOnExternalBrowser`
3. **Endpoint URL / HTTPS** — LIFF บังคับ HTTPS; endpoint ใน console ไม่ตรง URL จริง = init fail. localhost ต้อง tunnel (เช่น ngrok) หรือใช้ LIFF Inspector
4. **`liff.getProfile()` โดยยังไม่ login / ไม่มี scope `profile`** → เช็ค `isLoggedIn()` + scope ใน channel ก่อน
</line_mini_app>

---

<pwa>
## 🌐 PWA (Next.js 16) — default ของ /toh-mobile

เป้าหมาย: ผู้ใช้ **Add to Home Screen** ได้ใน ~1 นาที ไม่ต้องลงอะไรจาก store.

### 📚 Pull docs first
- Next.js PWA guide: `nextjs.org/docs/app/guides/progressive-web-apps`
- Serwist (next-pwa successor): `serwist.pages.dev/docs/next/getting-started` — **เช็ค setup ปัจจุบัน** เพราะ config เปลี่ยนบ่อย

### Checklist
- [ ] **Web app manifest** → `app/manifest.ts` (Next.js Metadata API): `name`, `short_name`, `start_url`, `display: "standalone"`, `theme_color`, `background_color`, `icons`
- [ ] **Icons** — อย่างน้อย 192×192 + 512×512 (มี maskable ด้วยยิ่งดี). generate จาก source เดียว
- [ ] **Service worker** — เลือกทางใดทางหนึ่ง:
  - **Serwist** (`@serwist/next`) — จัดการ precache manifest + gen `public/sw.js` ให้ (config `swSrc: 'app/sw.ts'`, `swDest: 'public/sw.js'` ผ่าน `withSerwist` ใน next config) — เช็ค getting-started ปัจจุบันก่อน
  - **Native** — เขียน `sw.js` เอง (fetch handler + cache) ถ้าอยากคุม 100% ไม่พึ่ง lib
- [ ] **Offline พื้นฐาน** — cache app shell + offline fallback page; runtime cache สำหรับ API/รูป
- [ ] **Install prompt** — ดัก`beforeinstallprompt` (Android/desktop) เก็บ event ไว้ trigger ปุ่ม "ติดตั้ง"; **iOS Safari ไม่มี event นี้** → ต้องสอนผู้ใช้ manual (Share → Add to Home Screen)
- [ ] **A2HS UX** — บอกวิธีเพิ่มลงหน้าจอแบบภาษาคน แยกคำแนะนำ iOS vs Android

### 🩹 Common mistakes
1. **Service worker ต้อง served จาก origin + HTTPS** (localhost ยกเว้นได้). path/scope ผิด = ไม่ลง
2. **Manifest ขาด icon 512 หรือ `display:standalone`** → เบราว์เซอร์ไม่เสนอ install
3. คาดหวัง iOS มี auto install prompt — ไม่มี ต้อง manual เสมอ
4. SW cache เก่าค้าง → วาง strategy update (skipWaiting/clientsClaim) + แจ้งผู้ใช้ reload
</pwa>

---

<capacitor>
## 🏪 Capacitor (iOS/Android) — track "ขึ้น store" ของ /toh-mobile

Wrap Next.js เดิมทั้งก้อนเป็น native app + เข้าถึง native APIs. **pattern เดียวกับ LINE convert** — codebase เดียว แปลงร่างได้.

### 📚 Pull docs first
- `capacitorjs.com/docs` — Capacitor ขยับเวอร์ชันเร็ว (7 → 8…) เช็ค `npm view @capacitor/core version` + docs ก่อนทำ
- Context7: `/websites/capacitorjs` หรือ `/ionic-team/capacitor-docs`

### Next build strategy
- **Static export (แนะนำ default)** — `next.config`: `output: 'export'`, `images: { unoptimized: true }` → build ได้โฟลเดอร์ `out/` → `webDir: 'out'`. เหมาะกับแอปที่ไม่พึ่ง server runtime
- **Server (SSR/route handlers)** — Capacitor ไม่รัน Node ในเครื่อง → ต้อง host backend แยกแล้วชี้ `server.url` ไปที่ deployment (แอปกลายเป็น native shell ครอบ remote). ใช้เมื่อจำเป็นต้องมี SSR จริง

### Setup checklist
- [ ] `npm i @capacitor/core` + `npm i -D @capacitor/cli`
- [ ] `npx cap init` (app name + bundle id เช่น `com.company.app`)
- [ ] ตั้ง `webDir: 'out'` ใน `capacitor.config.ts`
- [ ] `npx cap add ios` / `npx cap add android`
- [ ] ทุกครั้งหลัง `next build`: **`npx cap sync`** (copy web assets + update native deps)
- [ ] เปิด native project: `npx cap open ios` / `npx cap open android`

### Live-reload dev flow
ตั้ง `server.url` ใน capacitor config → dev server ของ Next (`http://<LAN-IP>:3000`) + `cleartext: true` (**dev เท่านั้น** — ห้ามค้างไว้ตอน production). แก้ web code แล้วแอปบนเครื่อง reload เอง (เฉพาะ web change, native change ต้อง rebuild)

### Native plugins
`@capacitor/camera`, `@capacitor/push-notifications`, `@capacitor/geolocation`, `@capacitor/share`… — ติดตั้ง plugin → `npx cap sync` → เพิ่ม native permission (Info.plist / AndroidManifest.xml) ตาม docs ของ plugin นั้น

### Store submission path (บอกผู้ใช้ภาษาคน)
- **iOS**: ต้องมี **Apple Developer account ($99/ปี)** → build/archive ใน Xcode → App Store Connect → review
- **Android**: **Google Play Console ($25 ครั้งเดียว)** → build signed AAB ใน Android Studio → Play Console → review

### 🩹 Common mistakes
1. ลืม `npx cap sync` หลัง build → native เห็น web version เก่า
2. เหลือ `cleartext`/`server.url` ไว้ตอน production → แอป reject/ไม่ปลอดภัย
3. `output: 'export'` แต่โค้ดใช้ SSR/route handler → build fail (ต้องเลือก strategy ให้ตรง)
4. ลืมประกาศ native permission ของ plugin → camera/push เงียบ ไม่มี error ชัด
</capacitor>

---

<expo_legacy>
## Expo (React Native) — LEGACY note เท่านั้น

Expo = **คนละ codebase** (React Native, ไม่ reuse Next.js DOM) → ขัดหลัก "Type Once". **default ของงาน mobile คือ PWA → Capacitor** ไม่ใช่ Expo.

ใช้ Expo เฉพาะเมื่อ **จำเป็นต้องเป็น bare React Native จริงๆ** — เช่น ต้องการ native performance/animation ระดับสูง, native module ที่ web wrapper ทำไม่ได้, หรือทีมมี RN codebase อยู่แล้ว. ถ้าไปทางนี้: pull docs ปัจจุบันจาก `docs.expo.dev` (Expo Router, EAS Build) — ไม่ reuse component DOM เดิม ต้อง port เป็น RN primitives.
</expo_legacy>

---

<tauri_desktop>
## Tauri (Desktop) — doc-pull note

Wrap web เป็น desktop app (macOS/Windows/Linux) — bundle เล็กกว่า Electron มาก, backend Rust. ใช้เมื่อผู้ใช้ต้องการ **desktop app จริง / offline-first / เข้าถึง filesystem-ระบบ**.

⚠️ **Tauri v2 เปลี่ยน schema จาก v1 เยอะ** (`tauri.conf.json` ใช้ `devUrl`/`frontendDist` แทน v1 `devPath`/`distDir`; plugin system ใหม่). อย่าใช้ snippet v1 เก่า — **pull current Tauri v2 docs ก่อนเสมอ**:
- `v2.tauri.app/start/frontend/nextjs/` (integration กับ Next.js)
- Next.js ต้อง `output: 'export'` + `images: { unoptimized: true }` (Tauri ไม่รัน SSR)
- เริ่มด้วย `npm create tauri-app` หรือเพิ่ม CLI เข้าโปรเจคเดิม แล้วอ่าน config keys ปัจจุบันจาก docs
</tauri_desktop>

---

<platform_decision_tree>
## 🌳 When to use which

```
User request
    │
    ├─ "LINE" / "LIFF" / targets LINE users ─────────→ LINE MINI App (LIFF SDK)
    │
    ├─ "อยากได้แอปบนมือถือ" / "add to home screen" ──→ PWA (default, เร็วสุด)
    │        └─ ต้องขึ้น App Store / Play Store? ────→ + Capacitor
    │        └─ ต้อง bare React Native จริงๆ? ───────→ Expo (legacy path)
    │
    ├─ "desktop" / mac / windows / offline-first ────→ Tauri (v2 docs)
    │
    └─ default ─────────────────────────────────────→ Next.js web (รันทุกที่ผ่าน browser)
```

**หลักตัดสินใจ:** เริ่มจาก web/PWA เสมอ (friction ต่ำสุด) → ยกระดับเป็น native track (Capacitor/Tauri) เมื่อมีเหตุผลจริง (store, native API, desktop). ทุก track = codebase เดียว + "pull docs first".
</platform_decision_tree>
