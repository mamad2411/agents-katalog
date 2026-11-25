---
name: struktur-menara
description: "Struktur menara sipil: menara lattice self-supporting & guyed, monopole, tiang distribusi; beban angin, pondasi, guy wire, perhitungan cepat, perawatan. | EN: tower structure lattice guyed monopole wind load foundation civil engineering"
version: 1.0.0
category: knowledge-base
lang: id
---

# Struktur Menara (Civil)

## Tipe
- **Lattice self-supporting**: truss siku; 60-120m; beban sendiri besar; pondasi blok/tiang.
- **Guyed/lattice dengan guy**: menara ramping + 3-4 guy wire ke angker; ekonomis >80m.
- **Monopole/tube**: silinder; 20-60m; untuk rooftop/substation.
- **Tiang distribusi**: 9-18m; beton/baja; untuk jaringan listrik.

## Beban utama
- **Angin**: F = q·G·Cf·A; q = kecepatan angin² (PPIU/BMKG regional; Jakarta ±35-45 m/s ultimate).
  A = luas proyeksi efektif (soliditas truss ×0.6-0.8). Beban angin GOVERNING di kebanyakan desain.
- **Berat sendiri**: member + peralatan (antena, feeder, rectifier ~ratusan kg).
- **Gempa**: spektrum respons site class; kombinasi 0.6D+1.0W atau 1.2D+L+0.5W (SNI 1726).
- **Guy pretension**: prategang guy 5-15% breaking strength.

## Perhitungan cepat beban angin (lattice)
- V = 40 m/s → q ≈ 800 N/m² (q=0.613·V²); soliditas 0.7, Cf≈1.2-2.0.
- Gaya horizontal ≈ q·Cf·A_proj; titik tangkap di centroid anggota.

## Pondasi
- Self-supporting: blok beton + anchor bolt (deformation check uplift).
- Guyed: tiap anchor = blok/plat + turnbuckle; cek uplift & sliding.
- Tutup dengan gravel/drainase; grounding ring.

## Perawatan
- Inspeksi guy tension (turnbuckle), baut, korosi cat, blockage bird nest, lighting FAA/SN.
