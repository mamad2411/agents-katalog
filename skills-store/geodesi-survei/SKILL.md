---
name: geodesi-survei
description: "Geodesi & surveying: koordinat UTM/WGS84, proyeksi, datum, GPS/GNSS, total station, leveling, azimut bearing, luas polygon, konversi DMS-decimal. | EN: geodesy surveying GPS GNSS UTM WGS84 coordinate projection total station"
version: 1.0.0
category: knowledge-base
lang: id
---

# Geodesi & Survei

## Koordinat & proyeksi
- **WGS84/GRS80**: datum geosentrik; lintang/bujur derajat.
- **UTM**: 60 zona (lebar 6°); Indonesia zona 48-51S; easting 500km di tengah, northing dari ekuator/5000km di selatan.
- Konversi UTM↔latlon butuh parameter zona + false easting/northing.
- **DMS↔desimal**: derajat + menit/60 + detik/3600.

## Pengukuran
- **GPS/GNSS**: absolut (code ~5-10m, RTK ~cm-level); butuh ≥4 satelit; PDOP rendah lebih baik.
- **Total station**: jarak + sudut; backsight/orientation sebelum ukur; prism/360°.
- **Leveling**: beda tinggi via staff; closure error toleransi ~±(3-12)√K mm (K=km).
- **Theodolit**: sudut horizontal/vertikal.

## Hitungan
- Jarak: Pythagoras local / haversine untuk geografis:
  a = sin²(Δφ/2)+cosφ1cosφ2sin²(Δλ/2); d = 2R·asin(√a), R=6371km.
- Bearing/azimut: atan2(ΔE, ΔN) dari utara searah jarum jam.
- Luas polygon (koordinat): rumus shoelace — jumlah (xi·yi+1 - xi+1·yi)/2.

## Indonesia
- SRGI (Sistem Referensi Geospasial Indonesia) — terestrial & vertikal (geoid EGM2008+).
- Perangkat: total station (Trimble/Topcon), GNSS RTK, waterpass.
