---
name: set-jarvis-model
description: "Jarvis ana model seç — cache'den listele, tek model test et, geçerse kalıcı set et. Triggers: set jarvis model, jarvis model, set-jarvis-model, model değiştir, model seç, which model, hangi model"
---

# /set-jarvis-model — Jarvis Ana Model Seçici

Jarvis'in hangi modelle çalışacağını seç, test et, kalıcı olarak ayarla.

## Mekanizma

- `settings.json` → `model` alanı Jarvis'in modeli
- Claude native modeller (sonnet/opus/haiku) doğrudan settings.json'a yazılır
- External modeller (groq, cerebras, hf vb.) `--model` flag'ı ile çalışır → settings.json'a tam model ID yazılır
- Tüm komutlar (`cl`, `claude`, `clhq`) settings.json'dan okur — başka override yok

## Adımlar

### 1. Mevcut durumu göster

```bash
jq -r '.model // "sonnet"' ~/.claude/settings.json
```

`~/Projects/claude-config/config/model-scores.json` oku.

### 2. Model listesini göster

Sadece LLM modelleri (`category` "llm-*" olanlar). skip_reason olanları listenin sonunda göster ama seçilemez yap.

Tablo formatı — **Kaynak** sütunu provider'ı gösterir:

```
#  | Model                                   | Kaynak     | Skor | Son Test   | Durum
---|------------------------------------------|------------|------|------------|------
1  | qwen-3-235b-a22b-instruct-2507          | Cerebras   | 100  | 2026-04-07 | ✅ (AKTİF)
2  | llama-3.3-70b-versatile                  | Groq       | 100  | 2026-04-07 | ✅
3  | google/gemma-4-31B-it                    | HuggingFace| 100  | 2026-04-07 | ✅
4  | qwen3.5:9b                              | Local      | 100  | 2026-04-07 | ✅
5  | qwen2.5-coder:7b                        | Local      | 100  | 2026-04-07 | ✅
6  | deepseek-coder:6.7b                     | Local      | 100  | 2026-04-07 | ✅
7  | gemini-2.0-flash                        | Google     |  90  | 2026-04-07 | ✅
—  | sonnet                                  | Claude API |  —   |     —      | 🔵
—  | opus                                    | Claude API |  —   |     —      | 🔵
—  | haiku                                   | Claude API |  —   |     —      | 🔵
```

**Kaynak mapping** (model-scores.json `provider` alanından):
- `groq` → Groq
- `huggingface` → HuggingFace
- `cerebras` → Cerebras
- `google` → Google
- `ollama` → Local
- Claude native → Claude API

**Sıralama:** Skor yüksekten düşüğe. Aktif model en üstte. Claude native'ler listenin sonunda (her zaman çalışır).

**Durum ikonları:**
- ✅ score >= 80 ve last_status ok
- ⚠️ score 30-79 veya tutarsız
- ❌ score < 30 veya sürekli fail
- 🔵 Claude native (test gerekmez)
- `(AKTİF)` — şu an settings.json'da set olan model

**Model adı gösterimi:** Prefix'leri kaldır, kısa göster:
- `groq/llama-3.3-70b-versatile` → `llama-3.3-70b-versatile`
- `hf/google/gemma-4-31B-it` → `google/gemma-4-31B-it`
- `cerebras/llama3.1-8b` → `llama3.1-8b`
- `local/qwen3.5:9b` → `qwen3.5:9b`

### 3. Kullanıcıdan seçim al

"Hangi modeli seçmek istersin? (numara veya model adı)" diye sor.

### 4. Test et

**Claude native model seçildiyse (sonnet/opus/haiku/claude-*):**
- Test gerekmez → adım 5'e geç

**External model seçildiyse:**

`~/Projects/claude-config/claude-secrets/secrets.env` oku → API key'leri al.

Seçilen modelin provider'ına göre tek curl çağrısı yap:

**Groq** (`provider: groq`):
Model ID: `groq/` prefix'ini kaldır
```bash
curl -s -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "fail"
```

**HuggingFace** (`provider: huggingface`):
Model ID: `hf/` prefix'ini kaldır
```bash
curl -s -X POST https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); c=d['choices'][0]['message'].get('content',''); print('ok|'+c[:80]) if c else print('fail|empty')" 2>/dev/null || echo "fail"
```

**Cerebras** (`provider: cerebras`):
Model ID: `cerebras/` prefix'ini kaldır
```bash
curl -s -X POST https://api.cerebras.ai/v1/chat/completions \
  -H "Authorization: Bearer $CEREBRAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "fail"
```

**Google** (`provider: google`):
```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/<MODEL_ID>:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Selam, 1 cümlede kim olduğunu söyle."}]}],"generationConfig":{"maxOutputTokens":60}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['candidates'][0]['content']['parts'][0]['text'][:80])" 2>/dev/null || echo "fail"
```

**Ollama/Local** (`provider: ollama`):
Model ID: `local/` prefix'ini kaldır
```bash
curl -s --max-time 60 -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","prompt":"Selam, 1 cümlede kim olduğunu söyle.","stream":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['response'][:80])" 2>/dev/null || echo "fail|OFFLINE"
```

#### Test sonucu

**Geçtiyse (ok):**
- model-scores.json güncelle: `last_tested = bugün`, `last_status = "ok"`, `tests_run++`, `tests_passed++`
- Adım 5'e geç

**Başarısızsa (fail):**
- model-scores.json güncelle: `last_tested = bugün`, `last_status = "fail"`, `tests_run++`
- Kullanıcıya bildir: "❌ <MODEL> test başarısız. Sonnet ile devam etmek ister misin?"
- Onaylarsa → `sonnet` ile adım 5
- Reddederse → dur

### 5. Kalıcı olarak set et

settings.json'daki `model` alanını güncelle:

```bash
jq --arg m "<SETTINGS_MODEL_VALUE>" '.model = $m' ~/.claude/settings.json > /tmp/settings_tmp.json && mv /tmp/settings_tmp.json ~/.claude/settings.json
```

**Model → settings.json değeri mapping:**

| Seçilen model türü | settings.json `model` değeri |
|--------------------|------------------------------|
| Claude native: sonnet | `sonnet` |
| Claude native: opus | `opus` |
| Claude native: haiku | `haiku` |
| Groq: `llama-3.3-70b-versatile` | `groq/llama-3.3-70b-versatile` |
| HuggingFace: `google/gemma-4-31B-it` | `hf/google/gemma-4-31B-it` |
| Cerebras: `llama3.1-8b` | `cerebras/llama3.1-8b` |
| Google: `gemini-2.0-flash` | `google/gemini-2.0-flash` |
| Local/Ollama: `qwen3.5:9b` | `local/qwen3.5:9b` |

Yani settings.json'a **model-scores.json'daki key** (tam prefix'li halı) yazılır.

### 6. Sonucu bildir

```
✅ Jarvis modeli ayarlandı: <MODEL_ADI> (<KAYNAK>)
📁 settings.json güncellendi
🔄 Yeni session'da aktif olur
```

Test yapıldıysa:
```
🧪 Test: ✅ geçti | Cevap: "<ilk 80 karakter>"
📊 Güncel skor: <SCORE>/100
```

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
