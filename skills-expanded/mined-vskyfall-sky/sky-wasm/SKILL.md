---
name: sky-wasm
description: >-
  WebAssembly'yi web uygulamasında kullanma: ne zaman gerçekten gerekli, Rust → wasm-bindgen/
  wasm-pack, C/C++ → Emscripten, Go/TinyGo, AssemblyScript, JS ile veri alışverişi ve bellek
  maliyeti, Worker içinde çalıştırma, paket boyutu ve tembel yükleme, hazır WASM kütüphaneleri
  (SQLite, ffmpeg.wasm, görüntü işleme, PDF), WASI ve sunucu tarafı WASM (Workers, Spin),
  hata ayıklama. "WASM", "tarayıcıda hızlı hesaplama", "Rust'ı web'de çalıştır" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · WebAssembly

## Ne zaman?

✓ CPU yoğun hesap (görüntü/ses/video işleme, sıkıştırma, şifreleme, simülasyon, oyun motoru), mevcut C/C++/Rust kütüphanesini web'e taşıma, tarayıcıda SQLite/DuckDB.
✗ DOM işi, basit iş mantığı, ağ ağırlıklı kod — JS daha hızlı geliştirilir ve sınır geçişi maliyeti kazancı yer. Önce JS'i profille (bkz. `sky-perf`).

## Rust → WASM

```rust
use wasm_bindgen::prelude::*;
#[wasm_bindgen]
pub fn blur(pixels: &mut [u8], width: u32, height: u32, radius: u32) { /* ... */ }
```
```bash
wasm-pack build --target web --release      # pkg/ içinde .wasm + JS sarmalayıcı + .d.ts
```
```ts
import init, { blur } from "./pkg/image_tools.js";
await init();
blur(imageData.data, w, h, 4);               // Uint8ClampedArray doğrudan bellek görünümü
```
- `wasm-opt -Oz` (binaryen) ile boyut küçültme; `opt-level = "z"`, `lto = true`.
- Vite'ta `vite-plugin-wasm` veya `?init`/`?url` importları.

## Diğer diller

- **C/C++**: Emscripten (`emcc -O3 -s MODULARIZE=1 -s EXPORT_ES6=1`), mevcut kütüphaneler için.
- **Go**: standart derleyici (büyük çıktı) veya **TinyGo** (küçük).
- **AssemblyScript**: TypeScript benzeri sözdizimi, JS geliştiricisi için en kolay giriş.

## Performans kuralları

- JS ↔ WASM sınırını az geç: tek tek eleman değil, toplu tampon (paylaşılan bellek görünümü) ver.
- String dönüşümleri pahalıdır (UTF-8 kopyalama); sayısal veriyle çalış.
- Ağır işi **Worker** içinde çalıştır (UI donmasın, bkz. `sky-browser-apis`); SharedArrayBuffer + thread'ler için COOP/COEP başlıkları gerekir.
- `.wasm` dosyasını tembel yükle (yalnızca özellik kullanılınca), `WebAssembly.instantiateStreaming`, uzun önbellek başlıkları.

## Hazır kütüphaneler (insanların sevdiği "tarayıcıda bu da mı çalışıyor?" anları)

SQLite WASM (+ OPFS, bkz. `sky-sqlite`), DuckDB-WASM (tarayıcıda analitik), ffmpeg.wasm (video dönüştürme/kırpma), `@jsquash/*` (AVIF/WebP kodlama), Pyodide (tarayıcıda Python), Tesseract.js (OCR), MuPDF/pdf.js, ONNX Runtime Web / Transformers.js (tarayıcıda ML modelleri — bkz. `sky-local-llm`).

## Sunucu tarafı WASM

Cloudflare Workers (WASM modülleri), Fermyon Spin, wasmtime/WASI — eklenti sistemleri ve güvenli sandbox için. Bileşen modeli (WIT) diller arası arayüzler.

## Hata ayıklama

Chrome DevTools DWARF desteği (C/C++/Rust kaynak düzeyinde breakpoint — eklenti), `console_error_panic_hook` (Rust panic'lerini konsola), boyut analizi `twiggy`.
