---
name: sky-local-llm
description: >-
  Yerel ve açık ağırlıklı LLM'leri çalıştırma: Ollama, llama.cpp, LM Studio, vLLM, MLX (Apple
  Silicon) seçimi, model ve nicemleme (quantization — GGUF, Q4/Q8) seçimi, donanım ve bellek
  hesabı, OpenAI uyumlu API ile uygulamaya bağlama, embedding modelleri, yapılandırılmış çıktı,
  tarayıcıda model (Transformers.js, WebLLM), Türkçe performansı, gizlilik avantajları,
  maliyet/kalite karşılaştırması ve ne zaman bulut API daha iyi. "Yerel model", "Ollama",
  "internetsiz AI", "veriler dışarı çıkmasın" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Yerel LLM'ler

## Ne zaman yerel?

✓ Veri dışarı çıkamaz (sağlık, hukuk, kurum içi), çevrimdışı çalışma, çok yüksek hacimde basit görevler (sınıflandırma, embedding), deney/öğrenme.
✗ En iyi akıl yürütme ve kod kalitesi, uzun bağlam, araç kullanımı kritikse → bulut modeller genelde belirgin şekilde daha iyi (bkz. `sky-ai`). Karma yaklaşım yaygın: hassas veri yerelde ön işlenir/anonimleşir, karmaşık iş bulutta.

## Araç seçimi

| Araç | Ne zaman |
|---|---|
| **Ollama** | en kolay: `ollama run <model>`, yerel API, model kütüphanesi |
| **LM Studio** | GUI, model deneme, yerel sunucu |
| **llama.cpp** | en geniş donanım desteği, ince ayar, GGUF |
| **MLX** (`mlx-lm`) | Apple Silicon'da en verimli |
| **vLLM** / SGLang / TGI | GPU sunucuda çok kullanıcılı yüksek verim |

## Model ve donanım

- Parametre × nicemleme ≈ bellek: 7–8B model Q4 ≈ 5GB, 14B ≈ 9GB, 32B ≈ 20GB, 70B ≈ 40GB (+ bağlam için ek bellek).
- **Q4_K_M** iyi denge; kalite kritikse Q8; çok küçük nicemlemeler (Q2/Q3) belirgin kalite kaybı.
- Apple Silicon birleşik bellek büyük modeller için avantajlı; NVIDIA'da VRAM sınırlayıcı.
- Türkçe: çok dilli eğitilmiş modelleri seç ve **kendi görev setinle test et** (bkz. `sky-ai-eval`) — Türkçe başarımı modelden modele çok değişir.

## Uygulamaya bağlama

```ts
// Ollama ve çoğu yerel sunucu OpenAI uyumlu uç nokta sunar
const res = await fetch("http://localhost:11434/v1/chat/completions", {
  method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ model: "LOCAL_MODEL_NAME", messages: [{ role: "user", content: "Bu yorumu olumlu/olumsuz/nötr olarak sınıflandır: …" }], temperature: 0 }),
});
```
Vercel AI SDK / LangChain / LlamaIndex yerel sağlayıcıları destekler. Yapılandırılmış çıktı: Ollama `format` (JSON şema), llama.cpp grammar (GBNF).

## Embedding ve RAG

Yerel embedding modelleri (çok dilli olanları seç) + pgvector/Qdrant (bkz. `sky-vector-db`) → tamamen yerel RAG; belgeler hiç dışarı çıkmaz.

## Tarayıcıda

**Transformers.js** (ONNX, WebGPU/WASM — sınıflandırma, embedding, konuşma tanıma Whisper, küçük üretken modeller), **WebLLM** (WebGPU ile tarayıcıda sohbet modeli). İlk yükleme büyük (yüzlerce MB) → önbellek, ilerleme göstergesi, isteğe bağlı özellik.

## İşletim

- Sunucuda: GPU sürücüleri, model dosyaları kalıcı volume'de, eşzamanlılık sınırı (her istek bellek tüketir), sağlık kontrolü.
- Güvenlik: yerel API'yi internete açma (Ollama varsayılan localhost) — gerekiyorsa auth'lu proxy arkasında.
- Lisans: açık ağırlıklı modellerin lisans koşullarını (ticari kullanım, kullanıcı sayısı sınırları) kontrol et.
- Ölç: token/sn, ilk token süresi, bellek; kaliteyi aynı eval setiyle bulut modelle karşılaştır.
