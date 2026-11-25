---
name: hi-test
description: "Tüm free/local modellere selam testi yap, skorları güncelle, durumu raporla. Triggers: hi-test, model test, selam testi, model sağlık, model health"
---

# /hi-test — Model Sağlık Testi

Tüm free ve local modellere "Selam" gönderir, cevap alıp alamadığını ölçer, `config/model-scores.json` skorlarını günceller.

## Kural: skip_reason varsa test etme, skora dahil etme

## Adımlar

1. `~/Projects/claude-config/claude-secrets/secrets.env` ve `~/Projects/claude-config/config/model-scores.json` oku
2. `skip_reason` olan modelleri listele — bunlar için agent başlatma
3. **Geri kalan her model için ayrı bir Agent başlat — tek bir mesajda hepsini paralel olarak** (20+ agent aynı anda)
4. Tüm agent sonuçları gelince skorları hesapla ve `model-scores.json`'u güncelle
5. Sonuç tablosunu ve özeti yaz

## Her model için agent görevi

Her agent için prompt şablonu:

```
secrets.env dosyasını oku: ~/Projects/claude-config/claude-secrets/secrets.env

Şu modeli test et: <MODEL_ID>
Provider: <PROVIDER>
Mesaj: "Selam, kim olduğunu 1 cümlede söyle."

Bash ile curl çağrısı yap (aşağıdaki endpoint'i kullan).
Cevap geldiyse: "ok | <ilk 80 karakter>"
Gelmezse: "fail | <hata>"

Sadece bu tek satırı döndür, başka açıklama ekleme.
```

## Model listesi ve endpoint'leri

### Groq modelleri
Endpoint: `POST https://api.groq.com/openai/v1/chat/completions`  
Header: `Authorization: Bearer $GROQ_API_KEY`

| Agent | Model ID |
|-------|----------|
| agent-groq-1 | `llama-3.3-70b-versatile` |
| agent-groq-2 | `qwen/qwen3-32b` |
| agent-groq-3 | `moonshotai/kimi-k2-instruct` |
| agent-groq-4 | `meta-llama/llama-4-scout-17b-16e-instruct` |

### HuggingFace modelleri
Endpoint: `POST https://router.huggingface.co/v1/chat/completions`  
Header: `Authorization: Bearer $HF_TOKEN`

| Agent | Model ID |
|-------|----------|
| agent-hf-1 | `meta-llama/Llama-3.1-8B-Instruct` |
| agent-hf-2 | `deepseek-ai/DeepSeek-R1` (content boşsa fail say) |
| agent-hf-3 | `google/gemma-4-31B-it` |

### Google Gemini
Endpoint: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY`  
Body: `{"contents":[{"parts":[{"text":"Selam, kim olduğunu 1 cümlede söyle."}]}],"generationConfig":{"maxOutputTokens":60}}`

| Agent | Model ID |
|-------|----------|
| agent-google-1 | `gemini-2.0-flash` |

### Cerebras modelleri
Endpoint: `POST https://api.cerebras.ai/v1/chat/completions`  
Header: `Authorization: Bearer $CEREBRAS_API_KEY`

| Agent | Model ID |
|-------|----------|
| agent-cerebras-1 | `llama3.1-8b` |
| agent-cerebras-2 | `qwen-3-235b-a22b-instruct-2507` |

### Ollama (Local) modelleri
Endpoint: `POST http://127.0.0.1:11434/api/generate`  
Body: `{"model":"<name>","prompt":"Selam, kim olduğunu 1 cümlede söyle.","stream":false}` — timeout 60s

| Agent | Model ID |
|-------|----------|
| agent-local-1 | `qwen3.5:9b` |
| agent-local-2 | `qwen2.5-coder:7b` |
| agent-local-3 | `deepseek-coder:6.7b` |

### Skip — agent başlatma (skip_reason var)
- `together/inference` → invalid_key
- `serper/search` → no_api_key
- `firecrawl/scrape` → no_api_key
- `groq/whisper-large-v3` → ses modeli
- `groq/canopylabs/orpheus-v1-english` → TTS

## Skor güncelleme (agent sonuçları toplandıktan sonra)

Her model için:
- ok → `tests_passed++`, `tests_run++`
- fail → `tests_run++` (tests_passed değişmez)
- skip → hiçbiri değişmez

Formül: `score = round((tests_passed / tests_run) * 100)`

`last_tested = bugünün tarihi`, `last_status = "ok"/"fail"/"skip"` güncelle.

## Sonuç tablosu

```
Model                                        | Skor | Durum | Cevap
---------------------------------------------|------|-------|-------
groq/llama-3.3-70b-versatile                 | 100  |  ✅   | Ben bir yapay...
hf/meta-llama/Llama-3.1-8B-Instruct          | 100  |  ✅   | Ben bir sanal...
cerebras/qwen-3-235b-a22b-instruct-2507      | 100  |  ✅   | Ben, insanlar...
local/qwen3.5:9b                             |   -  |  ❌   | OFFLINE
groq/whisper-large-v3                        |   -  |  ⏭️   | (ses modeli)
together/inference                           |   -  |  ⏭️   | invalid_key
```

## Özet

- Kaç model test edildi / toplam
- Kaçı ✅ / ⚠️ / ❌ / ⏭️
- Retire eşiğinin altındakiler (skor < 30): "🗑️ Eleme adayı: X"
- Warn eşiğindekiler (30-60): "⚠️ İzlemede: X"

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
