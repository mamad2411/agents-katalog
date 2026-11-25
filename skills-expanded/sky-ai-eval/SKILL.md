---
name: sky-ai-eval
description: >-
  AI özelliklerini ölçme ve iyileştirme: altın test seti oluşturma, kural tabanlı ve LLM-judge
  değerlendiriciler, RAG metrikleri (bulma doğruluğu, sadakat/faithfulness, kaynak doğruluğu),
  prompt/model değişikliğinde regresyon testi, CI'da eval, üretim geri bildirimi (👍/👎) ve
  izleme (Langfuse, Braintrust), A/B karşılaştırma ve maliyet/gecikme ölçümü. "AI cevapları
  kötü", "prompt'u değiştirdim bozuldu mu", "AI kalitesini ölç" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · AI Değerlendirme

"Prompt'u değiştirdim, daha iyi gibi" ölçüm değildir. Her AI özelliğinin bir **eval seti** olsun.

## 1. Altın set

- 30–100 gerçekçi girdi: kolay, zor, kenar durum, kötü niyetli (prompt injection), Türkçe yazım hataları,
  karışık dil, eksik bilgi.
- Her girdi için **beklenen** çıktı veya kabul ölçütleri (birebir metin değil, kriter).
- Üretimdeki 👎 alan örnekler sete eklenir (sürekli büyür).
- `evals/<özellik>/cases.jsonl`: `{ "id", "input", "expected", "tags": ["kenar", "injection"] }`.

## 2. Değerlendiriciler

| Tür | Ne zaman | Örnek |
|---|---|---|
| **Kural/kod** | çıktı yapılandırılmışsa | JSON şemaya uyuyor mu, tarih doğru mu, kategori eşleşiyor mu |
| **Benzerlik** | serbest metin, referans var | embedding benzerliği, anahtar kelime kapsamı |
| **LLM-judge** | kalite/ton/doğruluk | "Bu cevap bağlamdaki bilgiye sadık mı? 1–5 ve gerekçe" |
| **İnsan** | ilk kalibrasyon, kritik alan | haftalık 20 örnek etiketleme |

LLM-judge kuralları: puan ölçütlerini yaz (rubrik), önce gerekçe sonra puan, judge'ı insan etiketleriyle
kalibre et (uyum ≥ %80), mümkünse ikili karar (geçti/kaldı) — 1–10 ölçeği gürültülüdür.

## 3. RAG metrikleri

- **Bulma (retrieval) recall@k**: doğru parça ilk k sonuçta mı? (soruya doğru parça ID'lerini etiketle)
- **Sadakat (faithfulness)**: cevaptaki her iddia bağlamda var mı? (judge)
- **Kaynak doğruluğu**: gösterilen kaynak iddiayı destekliyor mu?
- **Cevap verilebilirlik**: bağlamda yokken "bilmiyorum" diyor mu? (halüsinasyon testi)
Önce bulmayı düzelt — kötü bulma ile hiçbir prompt iyi cevap üretemez.

## 4. Regresyon döngüsü

```
prompt/model/parçalama değişikliği → eval seti çalıştır → önceki sürümle karşılaştır
  → geçme oranı, ortalama puan, maliyet/istek, p95 gecikme → kötüleşen örnekleri incele → karar
```
- CI'da: PR'da prompt dosyası değiştiyse eval çalışsın, özet yorum olarak çıksın; eşik altına düşerse uyarı.
- Determinizm için `temperature: 0` (mümkün olan modellerde) ve her örneği 2–3 kez çalıştırıp ortalama.
- Promptlar kod gibi sürümlenir (`prompts/booking-extract.v3.md`).

## 5. Üretim izleme

- İz (trace): girdi, getirilen bağlam, çıktı, token, gecikme, model sürümü — Langfuse / Braintrust / Helicone / kendi tablon.
- Kullanıcı geri bildirimi: 👍/👎 + isteğe bağlı neden; düzenlenen çıktılar = örtük negatif sinyal.
- Haftalık rapor: geri bildirim oranı, en sık 👎 kategorileri, maliyet trendi.
- Kişisel veri: izlerde maskeleme, saklama süresi (bkz. `sky-privacy-engineering`).

## 6. Karşılaştırma

Yeni model/prompt için: aynı set üzerinde A/B, kör LLM-judge ikili karşılaştırma ("hangisi daha iyi, neden"),
maliyet ve gecikme tablosu. Kazanan kalite + maliyet dengesine göre seçilir, yalnızca kaliteye göre değil.

## Rapor biçimi

```
Eval: randevu-çıkarma  set: 64 örnek
            v2      v3
Geçme      %81     %90
Ort. puan  3.9     4.4
$/istek    0.0021  0.0018
p95 (ms)   1450    1210
Kötüleşen: #17 (göreli tarih "öbür gün"), #41 (iki kişi tek mesajda)
```
