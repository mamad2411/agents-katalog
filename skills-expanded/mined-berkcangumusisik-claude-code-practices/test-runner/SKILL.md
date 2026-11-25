---
name: test-runner
description: Testleri çalıştırır, başarısız olanları analiz eder ve düzeltme önerir
argument-hint: [test-pattern]
user-invocable: true
allowed-tools: Bash Read Edit Glob Grep
effort: medium
---

## Testleri Çalıştır

Önce mevcut test komutunu tespit et:
- `package.json` içindeki `test` scriptini oku
- Varsa test framework'ü belirle (Jest, Vitest, Mocha vb.)

Testleri çalıştır (pattern belirtilmişse: `$1`):
```bash
# Pattern varsa / If pattern provided: $1
```

## Sonuçları Analiz Et

### Başarısız Testler
Her başarısız test için:
1. Hata mesajını oku
2. İlgili kaynak dosyayı ve test dosyasını incele
3. Hatanın kaynağını tespit et:
   - Kod değişikliğinden mi kaynaklanıyor?
   - Test ortamı sorunu mu?
   - Beklenti (assertion) yanlış mı?

### Kök Neden Analizi
- Birden fazla test aynı sebepten mi başarısız?
- Ortak bir pattern var mı?

## Düzeltme Öner

Her başarısız test için:
- Sorunu açıkla
- Olası düzeltmeyi göster
- Düzeltmeyi uygulamamı ister misin? diye sor

## Özet Rapor

```
Toplam: X test
Geçti:  Y ✓
Kaldı:  Z ✗

Kök nedenler:
1. ...
2. ...
```
