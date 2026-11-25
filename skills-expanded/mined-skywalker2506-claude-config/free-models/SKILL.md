---
name: free-models
description: "Ücretsiz modelleri tara (Groq + HuggingFace), karşılaştır, free-models.json güncelle. Triggers: free models, ücretsiz modeller, free model ara, model tara."
argument-hint: "[update|list|search <konu>|sources] — varsayılan: list+update"
---

# /free-models — Multi-Source Free Model Scanner & Updater

Groq ve HuggingFace kaynaklarını tarayarak güncel free modelleri bulur, değerlendirir ve `config/free-models.json`'u günceller.

## Argüman davranışı

| Argüman | Davranış |
|---------|----------|
| `/free-models` | Tüm kaynaklardan taze çek + json güncelle |
| `/free-models list` | Mevcut json'u göster (API çağrısı yapma) |
| `/free-models update` | Tüm kaynaklardan taze çek + json güncelle |
| `/free-models search <konu>` | O konuya uygun free model öner (frontend, unity, backend, scraping) |
| `/free-models sources` | Hangi kaynaklar tarandı, kaç model bulundu özeti |

## Kaynaklar

### 1. Groq Free Tier
```
GET https://api.groq.com/openai/v1/models
```
Groq'un tüm modelleri ücretsizdir (rate limit var). API key gerekmez liste için.
Bilinen güçlü Groq modelleri: `llama-3.3-70b-versatile`, `llama-3.1-70b-versatile`, `gemma2-9b-it`, `mixtral-8x7b-32768`

### 2. HuggingFace Inference API
```
GET https://huggingface.co/api/models?inference=warm&limit=20&sort=trending
```
Filter: `pipeline_tag` == `text-generation`, ücretsiz inference endpoint'i olanlar.
Her modelin `inference` alanı `"warm"` ise ücretsiz servis ediliyor.

## Değerlendirme & Tier Sistemi

### Güç skoru
| Kriter | Ağırlık |
|--------|---------|
| Context ≥ 200K | +2 |
| Context ≥ 128K | +1 |
| Tool calling desteği | +2 |
| Bilinen güçlü model ailesi (Qwen3, Llama 3.3, Nemotron 120B) | +2 |
| 70B+ parametre | +2 |
| 30B-70B parametre | +1 |

Puan: 0-2 → `low`, 3-4 → `medium`, 5-6 → `high`, 7+ → `very-high`

### Tier ataması (kota koruma için)
| Tier | Kullanım |
|------|---------|
| `primary` | very-high/high + tool calling → ağır coding, agent görev |
| `secondary` | medium + tool calling → orta iş, kota taşması fallback |
| `lightweight` | low/medium, tool calling opsiyonel → basit soru-cevap, metin, trivial iş — **ücretli kota yemesin** |

## Uzmanlaşmış Alan Eşlemesi

Aşağıdaki alanlar için en uygun free modeli ata:

| Alan | Tercih edilen özellik |
|------|-----------------------|
| `frontend` | Yüksek context, tool calling, UI/JSX bilgisi (Qwen, Gemma) |
| `backend` | Güçlü code gen + tool calling (Nemotron, Qwen) |
| `unity` | C# bilgisi, code gen güçlü (Nemotron, Qwen) |
| `data-scraping` | Hızlı inference, iyi instruction following (Groq Llama, Qwen) |
| `lightweight` | Küçük model, hızlı → kota yemeden trivial iş (LiquidAI, Gemma 9B) |
| `vision` | Multimodal input → görsel analiz (Nemotron VL, Qwen3.6 Plus) |

## Akış

### 1. Mevcut durumu oku
`~/Projects/claude-config/config/free-models.json` oku — son güncelleme tarihi.

### 2. Kaynakları paralel tara
İki kaynağı `mcp__fetch__fetch_json` ile çek (paralel mümkünse sırayla).

### 3. Değerlendirme & puanlama
Her model için: güç skoru hesapla → tier ata → alan eşle.

### 4. Değişim tespiti
Mevcut json ile karşılaştır:
- 🆕 Yeni modeller
- ❌ Kaldırılanlar (deprecated: true yap, silme)
- 🔄 Güncellenenler
- ⚠️ Yakında biten (expiration_date < 14 gün)

### 5. JSON güncelle
`~/Projects/claude-config/config/free-models.json`:
- `version` minör artır
- `last_updated` bugünün tarihi
- `agent_mapping` güncelle (alan → model listesi)
- Groq ve HF modelleri ayrı `source` alanıyla işaretle

### 6. CLAUDE.md tablosunu kontrol et
Yeni very-high model → tablo satırı öner.

### 7. Rapor

```
## Free Model Tarama Sonucu (YYYY-MM-DD)

### Kaynak Özeti
| Kaynak | Taranan | Free Bulunan |
|--------|---------|-------------|
| Groq | N | N |
| HuggingFace | N | N |

### Primary Tier (ağır iş)
| Model | Kaynak | Context | Tool | Güç | Alan |
...

### Secondary Tier (orta iş / fallback)
...

### Lightweight Tier (trivial iş — kota koru)
...

### Uzmanlaşmış Eşleme
- Frontend: ...
- Backend: ...
- Unity: ...
- Data Scraping: ...
- Vision: ...
- Lightweight (kota koruma): ...

### Değişimler
- 🆕 Yeni: ...
- ❌ Kaldırılan: ...
- ⚠️ Yakında bitiyor: ...

### Eylemler
- [ ] free-models.json güncellendi
- [ ] CLAUDE.md kontrol edildi
- [ ] Commit önerisi: chore: update free model list YYYY-MM-DD
```

## Kurallar
- Sadece gerçekten ücretsiz modelleri listele
- Eski modelleri silme — `deprecated: true` işaretle
- Groq modelleri `"source": "groq"` ile işaretle
- HF modelleri `"source": "huggingface"` ile işaretle
- Max 20 tool call

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
