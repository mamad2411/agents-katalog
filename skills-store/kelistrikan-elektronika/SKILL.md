---
name: kelistrikan-elektronika
description: "Kelistrikan & elektronika: hukum Ohm, daya, rangkaian seri-paralel, dioda/transistor/IC, PCB, PSU, baterai, kelistrikan rumah tangga, dasar AC-DC. | EN: electronics electricity Ohm circuit diode transistor PCB power supply battery"
version: 1.0.0
category: knowledge-base
lang: id
---

# Kelistrikan & Elektronika

## Dasar DC
- V=IR · P=VI · hukum Kirchhoff (arus & tegangan loop).
- Seri: Rtot=ΣR, I sama; Paralel: 1/R=Σ1/R, V sama.
- Pembagi tegangan/arus; Thevenin/Norton untuk rangkaian kompleks.
- Kapasitor/resistor timing RC; LED wajib resistor (I=(Vs-Vf)/R).

## AC & daya
- V_rms = V_peak/√2 (220V PLN = 311V peak); f=50Hz Indonesia.
- Impedansi Z = √(R² + (XL-XC)²); daya P = VI cosφ.
- RLC resonansi f = 1/(2π√(LC)).

## Semikonduktor
- Dioda: forward 0.7V (Si) / 0.3V (Ge); LED 2-3.3V; zener untuk referensi/regulasi.
- Transistor BJT/NMOS: saklar & amplifikasi; MOSFET untuk daya.
- Op-amp: inverting/non-inverting; filter aktif RC.
- IC umum: 555 timer, LM317 regulator, optocoupler isolasi.

## Baterai & PSU
- Li-ion 3.7V sel (4.2V penuh), 18650; lead acid 12V (13.8V charging).
- SMPS vs linear: efisiensi SMPS >85%; cek rating arus kontinu.

## Rumah tangga PLN
- Daya tersambung VA; MCB pengaman; grounding wajib; jangan over-tap di stopkontak.
