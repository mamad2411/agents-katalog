---
name: antena-telekomunikasi
description: "Antena & telekomunikasi: jenis antena (omni, directional, grid, yagi), gain dBi, polarisasi, frekuensi, link budget, feeder/coax, VSWR, site tower. | EN: antenna gain dBi polarization link budget VSWR telecommunication tower feeder"
version: 1.0.0
category: knowledge-base
lang: id
---

# Antena & Telekomunikasi

## Jenis antena
- **Omni**: memancar 360° horizontal (sector/panel); dipakai BTS kota.
- **Directional**: beam sempit (grid parabolic, yagi, horn); jarak jauh/backhaul.
- **Sector**: 3×120° per site → coverage 360°.

## Parameter
- **Gain**: dBi (referensi isotropik) / dBd (=dBi-2.15). Omni 6-9 dBi, grid 20-30+ dBi.
- **Polarization**: vertikal/horizontal/kircular; harus sama di kedua ujung.
- **VSWR**: <1.5 bagus; 1.5-2 ok; >2 buruk (refleksi, panas feeder).
- **Feeder**: coax LDF4-50A (~3.9 dB/100m @900MHz), jumper, grounding.

## Link budget (LOS)
- P_r = P_t + G_t + G_r - L_fs - L_misc; L_fs = 20log(d_km) + 20log(f_MHz) + 32.44.
- Contoh 2GHz, 10km: L_fs ≈ 112.4 dB. Margin target ≥10-15 dB (fading).
- Fresnel zone: r = 17.3√(d_km/f_MHz) — LOS wajib bebas 60% zone pertama.

## Menara
- Ketinggian = coverage + Fresnel + obstacle; gain tinggi = radius naik.
- Grounding: petir (air terminal + down conductor), surge arrester.
- Standar: SNI tiang/menara, beban angin sesuai PPIU/BMKG, lighting obstruction.
