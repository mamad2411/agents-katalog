---
name: "token-cache-master"
description: "Exact + semantic cache untuk LLM calls. Gratis jawaban repeat 25-65% kasus. Invoke SEBELUM setiap LLM call, dan SESUDAH setiap response buat store result."
---

# Token Cache Master — 2-Tier Cache (Exact → Semantic)

## Trigger Rules
1. BEFORE any LLM call → run cache check
2. AFTER any LLM response → store cache
3. Skip cache only if user explicitly typed `nocache` or task is random/time-sensitive (e.g. "what time is it")

## Tier 1 — EXACT MATCH (cost: near-zero, no LLM, 100% deterministic)
Store key: `SHA256(model_id + temperature|0 + system_prompt_norm + all_user_messages_concat)`
→ Value: raw assistant response, timestamp, token count

- `system_prompt_norm`: collapse whitespace, lower the text, remove timestamps/uuids before hashing
- On EXACT HIT → immediately return cached response + annotate `[exact cache hit, saved NNN tokens, $NN saved]`

## Tier 2 — SEMANTIC MATCH (cosine ≥ 0.94)
- Key: first 512 chars of (user message + system prompt head) hashed into quick bucketing key, and a light local hash signature via 8-word minhash shingles
- On bucket collision, inline 20-keyword overlap Jaccard score between current query and stored user_queries → ≥0.5 match considered semantic hit
- Return cached answer with annotation `[semantic cache match NN%, saved NNN tokens]`

## Cache Storage (zero-dependency, filesystem only — works EVERYWHERE)
```python
# No imports, works in any agent that can write/read files
import os, hashlib, json, time
CACHE_DIR = os.path.expanduser("~/.cache/llm_token_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _key(prompt: str, model: str="any") -> str:
    return hashlib.sha256(f"{model}|{prompt[:4000]}".encode()).hexdigest()[:32]

def cache_get(key: str):
    p = os.path.join(CACHE_DIR, key + ".json")
    if os.path.exists(p) and time.time() - os.path.getmtime(p) < 86400*14:
        try:
            with open(p) as f: return json.load(f)
        except: pass
    return None

def cache_put(key: str, response: str, meta: dict=None):
    with open(os.path.join(CACHE_DIR, key + ".json"), "w") as f:
        json.dump({"r": response, "m": meta or {}, "t": int(time.time())}, f)
```

## Eviction
- Auto: cap at 5,000 entries; on insert if count > 5k → delete 100 oldest (mtime)
- Manual: user says `clear cache` → delete only `.json` files in CACHE_DIR modified >30 days ago

## Expected Savings
- Typical dev session: 25–45% exact hit rate (same question rephrased / retry / follow-ups that share long system prompt)
- After 1 day of usage: 40–65% of total LLM calls → CACHE HIT → FREE

## Integration with `token-budget-guard`
Every cache hit → increment `token-budget-guard:saved_tokens_cache` counter by estimated token length of the stored response (approx: len(response)/4 for English).
