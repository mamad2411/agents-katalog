---
name: pr-review
description: Mevcut PR'ı veya belirtilen PR numarasını kapsamlı şekilde inceler
argument-hint: [pr-number]
user-invocable: true
allowed-tools: Bash(gh *) Read Grep
effort: medium
---

## PR Bağlamı

Diff:
```
!`gh pr diff $1 2>/dev/null || gh pr diff`
```

Açıklama ve yorumlar:
```
!`gh pr view $1 --comments 2>/dev/null || gh pr view --comments`
```

CI durumu:
```
!`gh pr checks $1 2>/dev/null || gh pr checks`
```

---

## İnceleme Kriterleri

Aşağıdaki alanlarda kapsamlı inceleme yap:

### Doğruluk
- Değişiklikler PR açıklamasındaki amacı karşılıyor mu?
- Edge case'ler ele alınmış mı?
- Hata yönetimi yeterli mi?

### Güvenlik
- SQL injection, XSS, CSRF gibi açıklar var mı?
- Hassas veriler loglanıyor veya expose ediliyor mu?
- Yetkilendirme kontrolleri doğru mu?

### Kod Kalitesi
- Kod DRY prensiplerine uyuyor mu?
- Fonksiyonlar tek sorumluluk ilkesini takip ediyor mu?
- Karmaşık mantık için yeterli yorum var mı?

### Test
- Yeni kod için test yazılmış mı?
- Mevcut testler hâlâ geçiyor mu?
- Test senaryoları yeterli kapsamı sağlıyor mu?

### Performans
- Gereksiz veritabanı sorgusu veya API çağrısı var mı?
- Büyük veri setleri için düşünülmüş mü?

---

## Çıktı Formatı

Şu başlıklar altında bulgularını sun:

**Kritik Sorunlar** - merge öncesi mutlaka düzeltilmeli  
**Öneriler** - kaliteyi artıracak değişiklikler  
**Küçük Notlar** - stil veya tercih meselesi  
**Olumlu Noktalar** - iyi yapılan şeyler  

Her bulgu için ilgili dosya ve satır numarasını belirt.
