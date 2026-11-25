---
name: data-science-kaggle
description: "Data science workflow ala Kaggle: EDA, feature engineering, baseline dulu, validasi KFold/GroupKFold, metrik, leaderboard mindset, notebook hygiene. | EN: kaggle data science EDA machine learning workflow feature engineering validation"
version: 1.0.0
category: knowledge-base
lang: id
---

# Data Science / Kaggle Workflow

## Urutan kerja
1. **EDA dulu**: shape, dtypes, missing, distribusi target, duplikat, leakage (kolom yang bocorkan target).
2. **Baseline sederhana**: mean/median untuk regresi, prior untuk klasifikasi — patok semua model harus mengalahkannya.
3. **Validasi yang benar**: KFold stratified (klasifikasi) / GroupKFold (data berkelompok) / TimeSeriesSplit (time series). JANGAN shuffle data temporal.
4. **Feature engineering**: agregasi, encoding (target/mean encoding hati-hati leakage), interaksi, binning.
5. **Model**: gradient boosting (LightGBM/XGBoost/CatBoost) untuk tabular; neural untuk teks/gambar.
6. **Submit bertahap**: jangan overfit LB publik; pakai CV lokal sebagai patokan.

## Aturan anti-curang
- Target encoding pakai fold training saja.
- Normalisasi fit di train, transform di test.
- Cek duplikat train↔test (pastikan test tidak bocor ke train).

## Metrik
- Regresi: RMSE/MAE/MAPE; Klasifikasi: AUC-ROC, F1, logloss; Imbalance → PR-AUC/F1.

## Tools
- pandas, numpy, scikit-learn, lightgbm, matplotlib/seaborn, SHAP untuk interpretasi.
- Dataset publik: Kaggle, UCI ML, HuggingFace, data.go.id (Indonesia).
