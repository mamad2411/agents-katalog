---
name: handoff-templates
description: Agent arasi iletisim sablonlari. Standard handoff, QA verdict (PASS/FAIL), escalation, bug report, security finding ve status update formatlari.
---

# Handoff Templates - Agent Arasi Iletisim Standartlari

Agent'lar arasi mesajlarda bu sablonlari kullan.

## 1. Standard Handoff (Is Teslimi)

```
DURUM: <tamamlanan is ozeti>
DOSYALAR: <degisen dosyalar>
BAGIMLILIKLAR: <onkosullar>
TESLIM: <ne bekleniyor, kabul kriterleri>
KALITE: <test/review durumu>
```

## 2. QA Verdict: PASS

```
--topic review-result --subject "QA PASS: <task>"
--body "KARAR: PASS
KANIT: <test sonuclari, screenshot, metrik>
KRITERLER: [x] Kriter1 [x] Kriter2 [x] Kriter3
SONRAKI: <bir sonraki adim>"
```

## 3. QA Verdict: FAIL

```
--topic review-result --priority high
--subject "QA FAIL: <task> (deneme N/3)"
--body "KARAR: FAIL
SORUN 1: [severity] <aciklama>
  BEKLENEN: <ne olmali>
  GERCEK: <ne oluyor>
  FIX: <ne yapilmali>
  DOSYA: <hangi dosya>
SORUN 2: ...
RETRY: Sadece listelenen sorunlari duzelt, yeni ozellik EKLEME"
```

## 4. Escalation (3 Denemeden Sonra)

```
--topic escalation --priority critical
--subject "ESCALATION: <task> 3/3 basarisiz"
--body "TASK: <aciklama>
GECMIS:
  Deneme 1: <ne oldu, neden fail>
  Deneme 2: <ne oldu, neden fail>
  Deneme 3: <ne oldu, neden fail>
KOK NEDEN: <neden surekli basarisiz>
ONERI: [reassign|decompose|revise|defer]
ETKI: <neyi blokluyor>"
```

## 5. Bug Report

```
--topic bug-report --priority <severity>
--subject "BUG: <kisa aciklama>"
--body "NE OLUYOR: <hata aciklamasi>
BEKLENEN: <dogru davranis>
TEKRAR: <nasil reproduce edilir>
DOSYA: <ilgili dosyalar>
TAHMIN: <olasi root cause>"
```

## 6. Security Finding

```
--topic security-finding --priority critical
--subject "SECURITY: <acik tipi> - <konum>"
--body "TIP: <XSS|SQLi|SSRF|Auth Bypass|...>
KONUM: <dosya:satir>
ETKI: <ne olabilir>
EXPLOIT: <nasil istismar edilir>
FIX: <cozum onerisi>
ACILIYET: <hemen|sprint|sonraki>"
```

## 7. Status Update

```
--topic status --subject "Durum: <agent> - <ozet>"
--body "TAMAMLANAN: <liste>
DEVAM EDEN: <liste>
BLOCKER: <varsa>
SONRAKI: <plan>"
```

## Kurallar

- TURKCE yaz (teknik terimler haric)
- Body 500 karakter max (comms CLI limiti)
- Priority dogru sec: critical sadece gercek acil durumlar
- Her handoff'ta kabul kriterleri belirt
- QA FAIL'de spesifik fix talimati ver, genel yorum YAZMA
