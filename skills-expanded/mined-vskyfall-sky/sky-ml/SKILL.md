---
name: sky-ml
description: >-
  Uygulamalı makine öğrenmesi (geliştirici için): problemi doğru çerçeveleme (sınıflandırma,
  regresyon, öneri, anomali, zaman serisi), önce basit temel model, veri hazırlama ve sızıntı
  önleme, scikit-learn pipeline'ları, gradient boosting (XGBoost/LightGBM), değerlendirme
  metrikleri ve doğrulama, PyTorch temelleri ve ince ayar, deney takibi (MLflow/W&B), model
  servis etme (FastAPI, ONNX, BentoML), izleme ve kayma (drift), ne zaman ML yerine kural/LLM.
  "Tahmin modeli", "makine öğrenmesi", "model eğit", "öneri sistemi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Makine Öğrenmesi

## Önce: ML gerekli mi?

1. Basit kural/SQL eşiği yetiyor mu? ("3 kez gelmeyen müşteri riskli")
2. Hazır bir LLM/API çözüyor mu? (sınıflandırma, çıkarma — bkz. `sky-ai`)
3. Yeterli ve etiketli veri var mı? Başarı metriği ve iş değeri net mi?
ML'e ancak bunlardan sonra.

## Çerçeveleme

| Soru | Tür | Örnek |
|---|---|---|
| Hangi sınıf? | sınıflandırma | randevuya gelmeme (no-show) riski |
| Ne kadar? | regresyon | haftalık talep, teslim süresi |
| Ne önerelim? | öneri / sıralama | "bunu alanlar şunu da aldı" |
| Olağan dışı mı? | anomali | sahte işlem, sensör arızası |
| Gelecek değer? | zaman serisi | günlük randevu sayısı tahmini |

## Süreç

1. **Temel model**: en basit tahmin (çoğunluk sınıfı, geçen haftanın ortalaması) — her model bunu geçmeli.
2. **Veri**: tek tablo hâline getir, hedef değişken, özellikler; **sızıntı yok** (tahmin anında bilinmeyecek bilgi özellik olamaz — "iptal tarihi" ile iptali tahmin etmek gibi).
3. **Bölme**: zamana bağlı veride zamana göre böl (geçmişle eğit, gelecekle test); rastgele bölme gerçekçi olmayan iyi sonuç verir.
4. **Model**: tablo verisinde önce **gradient boosting** (LightGBM/XGBoost/CatBoost) — çoğu zaman en iyi; scikit-learn pipeline:
```python
pipe = Pipeline([("prep", ColumnTransformer([("num", StandardScaler(), num_cols), ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)])),
                 ("model", HistGradientBoostingClassifier())])
scores = cross_val_score(pipe, X_train, y_train, cv=TimeSeriesSplit(5), scoring="roc_auc")
```
5. **Değerlendirme**: dengesiz sınıflarda doğruluk yanıltır → precision/recall, PR-AUC, F1; iş maliyetiyle eşik seç ("yanlış alarm" vs "kaçırma" maliyeti); karışıklık matrisi; segment bazında hata analizi.
6. **Açıklanabilirlik**: özellik önemleri, SHAP — kullanıcıya "neden riskli?" gösterebilmek güven verir.

## Derin öğrenme

Görsel/metin/ses verisi → **önceden eğitilmiş model + ince ayar** (Hugging Face Transformers, timm); sıfırdan eğitme nadiren gerekir.
PyTorch döngüsü temelleri, karışık hassasiyet, erken durdurma; GPU yoksa bulut defter (Colab/Kaggle) veya küçük modeller.
Metin sınıflandırma için önce LLM + few-shot dene, hacim/maliyet artınca küçük model ince ayarı.

## Deney takibi ve tekrar üretilebilirlik

MLflow / Weights & Biases: parametreler, metrikler, veri sürümü, model artefaktı; sabit rastgelelik tohumu; `uv` ile sabit bağımlılıklar (bkz. `sky-python`).

## Servis etme

- Toplu tahmin (gece işi, sonuçları DB'ye) çoğu zaman gerçek zamanlıdan basit ve ucuz.
- Gerçek zamanlı: FastAPI uç noktası (bkz. `sky-fastapi`) + model yükleme lifespan'de; ONNX Runtime ile hızlı/çok dilli çıkarım; BentoML/Ray Serve büyük ölçekte.
- Girdi şeması doğrulama, sürümlü model, gölge mod (yeni modeli yan yana çalıştırıp karşılaştır), A/B (bkz. `sky-feature-flags`).

## İzleme

Veri kayması (özellik dağılımları değişti mi?), tahmin dağılımı, gerçekleşen sonuçlarla performans (geri bildirim döngüsü), yeniden eğitim takvimi. Kişisel veriyle eğitimde KVKK ve önyargı (bias) kontrolü.
