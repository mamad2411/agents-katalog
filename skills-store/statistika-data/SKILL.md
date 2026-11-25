---
name: statistika-data
description: "Statistika & analisis data: deskriptif, distribusi normal, uji hipotesis t-test chi-square ANOVA, korelasi Pearson/Spearman, regresi linear, interval kepercayaan, p-value. | EN: statistics data analysis hypothesis test regression correlation distribution"
version: 1.0.0
category: knowledge-base
lang: id
---

# Statistika & Analisis Data

## Deskriptif
- Mean, median, modus · varian s², std σ · IQR, skewness, kurtosis.
- Visualisasi: histogram, boxplot, scatter, QQ-plot.

## Distribusi
- Normal N(μ,σ²): 68-95-99.7 rule · z-score = (x-μ)/σ.
- Binomial, Poisson (λ kejadian jarang), t (n kecil), chi-square, F.
- Central limit theorem: n>30 → sampling mean ~normal.

## Uji hipotesis
- H0 vs H1; α (0.05); p-value < α → tolak H0.
- t-test: 1 sampel/2 sampel/berpasangan; asumsi normalitas & homogen varians.
- Chi-square: kategorik (independensi, goodness of fit).
- ANOVA: >2 grup; post-hoc Tukey.
- Non-parametrik: Mann-Whitney, Wilcoxon, Kruskal-Wallis.

## Korelasi & regresi
- Pearson r (-1..1, linear); Spearman ρ (rank, monoton non-linear).
- Regresi linear y = a+bx; R²; residual harus random (cek heteroskedastisitas).
- Regresi logistik untuk klasifikasi biner; multivariat hati-hati multikolinearitas (VIF).

## Interval & kesalahan
- CI 95%: x̄ ± t·(s/√n) · standard error · power analysis sebelum eksperimen.
- Data leakage & survivorship bias = kesalahan klasik ML.
