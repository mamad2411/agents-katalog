---
description: Gmail'den takip bekleyen e-postaları bulup otomatik hatırlatma ve takip planı oluşturur
---

# Gmail Takip Sistemi

## Amaç

Gmail'deki gönderilmiş e-postaları tarayıp henüz cevap gelmemiş olanları tespit eder. Her birine uygun takip e-postası taslağı hazırlar. Solopreneur'ların en büyük gelir kaçağı olan "cevap gelmedi, unuttum" sorununu çözer.

**Kategori**: Yapay Zeka ve Otomasyon
**MCP Gereksinimi**: Gmail MCP bağlı olmalı

## Süreç

### Adım 1: Takip bekleyen e-postaları bul

Gmail MCP `gmail_search_messages` ile şu aramaları yap:
- `in:sent after:7d` — son 7 günde gönderilen
- `in:sent -in:inbox` — cevap gelmemiş olanlar (yanıt geldiyse inbox'ta thread görünür)

Veya daha spesifik:
- `in:sent subject:(teklif OR proposal OR fiyat OR görüşme) after:3d` — iş e-postaları

### Adım 2: Önceliğe göre sınıflandır

Her cevapsız e-postayı şu kategorilere ayır:

| Öncelik | Kural | Eylem |
|---------|-------|-------|
| **ACİL** | Teklif/proposal gönderilmiş, 48+ saat cevap yok | Bugün takip et |
| **YÜKSEK** | Müşteri/lead ile görüşme, 3+ gün cevap yok | Bu hafta takip et |
| **NORMAL** | Genel iletişim, 5+ gün cevap yok | Hafta sonu takip et |
| **BIRAK** | Soğuk outreach, 7+ gün cevap yok | Artık takip etme |

### Adım 3: Takip e-postası taslakları oluştur

Her ACİL ve YÜKSEK e-posta için takip taslağı hazırla:

**Takip #1 (48 saat sonra):**
```
Konu: Re: [orijinal konu]

Merhaba [isim],

Geçen gönderdiğim [konu] hakkında bir güncelleme var mı diye merak ettim.

Sorularınız varsa memnuniyetle cevaplayabilirim.

[imza]
```

**Takip #2 (5 gün sonra):**
```
Konu: Re: [orijinal konu]

Merhaba [isim],

[Konu] hakkındaki e-postamı görme şansınız oldu mu?

Eğer zamanlaması uygun değilse anlayışla karşılarım — ileride tekrar konuşmak isterseniz haber vermeniz yeterli.

[imza]
```

**Takip #3 (10 gün sonra — son):**
```
Konu: Re: [orijinal konu]

Merhaba [isim],

Bu konuda son bir kez ulaşmak istedim. Eğer şu an öncelikleriniz arasında değilse sorun değil.

İleride ihtiyacınız olursa buradayım.

[imza]
```

### Adım 4: Taslakları kaydet

Kullanıcı onayıyla Gmail MCP `gmail_create_draft` ile taslakları oluştur. Her taslak orijinal thread'e yanıt olarak ayarlansın.

### Adım 5: Takip raporu sun

Kullanıcıya kısa bir özet göster:
- Kaç e-posta cevapsız
- Kaçına takip hazırlandı
- Kaçı "bırak" kategorisinde

## Örnek Çıktı

```
📧 Gmail Takip Raporu — 21 Mart

Cevap bekleyen: 7 e-posta

ACİL (bugün takip et):
  1. Ahmet Yılmaz — Web sitesi teklifi (gönderim: 18 Mart)
     → Takip taslağı hazırlandı ✉️

  2. Startup XYZ — Danışmanlık görüşmesi (gönderim: 19 Mart)
     → Takip taslağı hazırlandı ✉️

YÜKSEK (bu hafta):
  3. Elif Kaya — Logo projesi soruları (gönderim: 16 Mart)
     → Takip taslağı hazırlandı ✉️

NORMAL:
  4-5. İki genel e-posta → Hafta sonuna planlandı

BIRAK:
  6-7. İki soğuk outreach → 10+ gün, takip önerilmez

Taslakları Gmail'e kaydedeyim mi?
```
