---
name: set-model
description: "Jarvis ana model seç — cache'den listele, tek model test et, geçerse kalıcı set et. Triggers: set model, jarvis model, model değiştir, model seç, which model, hangi model"
---

# /set-model — Jarvis Ana Model Seçici

Jarvis'in (ana Claude Code oturumu) hangi modeli kullanacağını seç ve kalıcı olarak ayarla.

## Nasıl çalışır

- `claude` komutu `CLAUDE_FREE_MODEL` env var'ı setliyse onu kullanır, yoksa `settings.json` modelini kullanır
- Bu skill `CLAUDE_FREE_MODEL`'i `~/.claude/secrets/secrets.env`'e yazar → kalıcı olur
- Sonraki terminal açılışında otomatik aktif olur (secrets.env source edilir)

## Adımlar

### 1. Mevcut durumu göster

`~/Projects/claude-config/config/model-scores.json` oku.

Şu anki aktif model:
```bash
grep 'CLAUDE_FREE_MODEL' ~/.claude/secrets/secrets.env 2>/dev/null || echo "(ayarlanmamış — settings.json default)"
```

### 2. Model listesini göster

Sadece LLM modelleri listele (`category` "llm-*" olanlar), skip_reason olmayanlar:

```
#  | Model                                      | Skor | Son Test   | Durum  | Not
---|---------------------------------------------|------|------------|--------|-----
1  | openrouter/qwen/qwen3.6-plus:free           | 100  | 2026-04-07 | ✅     | (AKTİF)
2  | cerebras/qwen-3-235b-a22b-instruct-2507     | 100  | 2026-04-07 | ✅     |
3  | groq/llama-3.3-70b-versatile                | 100  | 2026-04-07 | ✅     |
4  | hf/google/gemma-4-31B-it                    | 100  | 2026-04-07 | ✅     |
5  | sonnet                                      |  —   |     —      | 🔵 Claude |
6  | opus                                        |  —   |     —      | 🔵 Claude |
7  | haiku                                       |  —   |     —      | 🔵 Claude |
...
```

Skor durumları:
- ✅ score >= 80, last_status ok
- ⚠️ score 30-79 veya last_status fail ama geçmiş ok var
- ❌ score < 30 veya sürekli fail
- 🔵 Claude native model (Anthropic API — her zaman çalışır, test gerekmez)
- `(AKTİF)` — şu an CLAUDE_FREE_MODEL'de set olan

Native Claude modeller (test gerekmez, her zaman çalışır):
- `sonnet` → claude-sonnet-4-6
- `opus` → claude-opus-4-6  
- `haiku` → claude-haiku-4-5-20251001

### 3. Kullanıcıdan seçim al

"Hangi modeli seçmek istersin? (numara veya model adı)" diye sor.

### 4. Test et

**Native Claude model seçildiyse (sonnet/opus/haiku/claude-*):**
- Test gerekmez, direkt adım 5'e geç

**Free/external model seçildiyse:**

`~/Projects/claude-config/claude-secrets/secrets.env` oku → API key'leri al.

Seçilen modeli tek bir Bash curl ile test et:

**OpenRouter modeli:**
```bash
curl -s -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "fail"
```

**Groq modeli:**
```bash
curl -s -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "fail"
```

**HuggingFace modeli:**
```bash
curl -s -X POST https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); c=d['choices'][0]['message'].get('content',''); print('ok|'+c[:80]) if c else print('fail|empty content')" 2>/dev/null || echo "fail"
```

**Cerebras modeli:**
```bash
curl -s -X POST https://api.cerebras.ai/v1/chat/completions \
  -H "Authorization: Bearer $CEREBRAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"Selam, 1 cümlede kim olduğunu söyle."}],"max_tokens":60}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "fail"
```

**Ollama/Local modeli:**
```bash
curl -s --max-time 60 -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"<MODEL_ID>","prompt":"Selam, 1 cümlede kim olduğunu söyle.","stream":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok|'+d['response'][:80])" 2>/dev/null || echo "fail|OFFLINE"
```

#### Test sonucu

**Test geçtiyse (ok):**
- model-scores.json'u güncelle: `last_tested = bugün`, `last_status = "ok"`, `tests_run++`, `tests_passed++`
- Adım 5'e geç

**Test başarısızsa (fail):**
- model-scores.json'u güncelle: `last_tested = bugün`, `last_status = "fail"`, `tests_run++`
- Kullanıcıya bildir: "❌ <MODEL> test başarısız. Sonnet ile devam etmek ister misin?"
- Kullanıcı onaylarsa → `sonnet` ile adım 5'e geç
- Kullanıcı reddederse → dur

### 5. Kalıcı olarak set et

**Native Claude model (sonnet/opus/haiku):**
```bash
# CLAUDE_FREE_MODEL satırını sil (native modelde env var olmamalı)
sed -i '' '/^CLAUDE_FREE_MODEL=/d' ~/.claude/secrets/secrets.env
# settings.json model alanını güncelle
jq --arg m "<MODEL>" '.model = $m' ~/.claude/settings.json > /tmp/settings_tmp.json && mv /tmp/settings_tmp.json ~/.claude/settings.json
```

**Free/external model:**
```bash
# Önce eskiyi sil, sonra yeni değeri ekle
sed -i '' '/^CLAUDE_FREE_MODEL=/d' ~/.claude/secrets/secrets.env
echo "CLAUDE_FREE_MODEL=<MODEL_ID>" >> ~/.claude/secrets/secrets.env
# settings.json model'i sonnet'e bırak (proxy üzerinden gidiyor)
jq '.model = "sonnet"' ~/.claude/settings.json > /tmp/settings_tmp.json && mv /tmp/settings_tmp.json ~/.claude/settings.json
```

### 6. Sonucu bildir

```
✅ Jarvis modeli ayarlandı: <MODEL>
📁 ~/.claude/secrets/secrets.env güncellendi
🔄 Yeni terminalde otomatik aktif olur (source ~/.zshrc veya yeni terminal aç)
```

Eğer test yapıldıysa skor bilgisini de göster:
```
🧪 Test: ✅ geçti | Cevap: "<ilk 80 karakter>"
📊 Güncel skor: <SCORE>/100
```
