---
name: sky-chat-product
description: >-
  Uygulama içi mesajlaşma ürünü: konuşma/oda/thread veri modeli, birebir ve grup sohbet,
  okundu bilgisi ve "yazıyor…", çevrimiçi durumu, ek dosya ve görsel, emoji tepkileri, yanıt
  (reply) ve alıntı, mesaj düzenleme/silme, bildirim ve sessize alma, arama, moderasyon ve
  engelleme, müşteri destek sohbeti (widget) ve hazır servisler (Stream, Sendbird). "Mesajlaşma
  ekle", "sohbet", "müşteriyle yazışma", "WhatsApp gibi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Sohbet Ürünü

## Hazır mı, kendin mi?

- **Stream Chat / Sendbird / TalkJS**: UI kiti, okundu bilgisi, moderasyon, push hazır — hızlı ama ölçekte pahalı.
- Kendin: Postgres + realtime katmanı (bkz. `sky-realtime`) — temel özellikler 1–2 hafta.
- Müşteri desteği: Crisp / Intercom / Chatwoot (açık kaynak) — sıfırdan yazma.

## Veri modeli

```
conversations   id, org_id, type (direct|group|support), title, last_message_at, created_at
participants    conversation_id, user_id, role, last_read_message_id, muted_until, joined_at
messages        id, conversation_id, sender_id, body, reply_to_id, edited_at, deleted_at, created_at
attachments     message_id, file_id, kind (image|file|voice)
reactions       message_id, user_id, emoji   PK(message_id,user_id,emoji)
```
- Mesaj ID'si sıralanabilir (UUIDv7/ULID) → sayfalama ve okundu karşılaştırması kolay.
- Okunmamış sayısı: `count(*) where id > last_read_message_id` (indeksli) veya sayaç sütunu.

## Gönderim akışı

1. İstemci `clientId` ile mesajı **anında** listeye ekler (soluk, saat ikonu).
2. Sunucu kaydeder, realtime ile odaya yayınlar (yayın kaydetmeden sonra).
3. Gönderen kendi mesajını `clientId` ile eşler → tek tik ✓.
4. Alıcı görünce okundu → çift tik ✓✓ (mavi). Hata → kırmızı "Gönderilemedi · Tekrar dene".
Çevrimdışı gönderilenler kuyrukta bekler, bağlanınca gider.

## İnsanların sevdiği detaylar

- "Yazıyor…" göstergesi (bkz. `sky-realtime`), çevrimiçi yeşil nokta / "son görülme 5 dk önce" (gizlenebilir).
- Mesaja **yanıtla** (alıntı balonu), kaydırarak yanıtla (mobil).
- Emoji tepkileri (çift tıkla ❤️), tepki sayıları, kimin tepki verdiği tooltip'te.
- Görsel yapıştır/sürükle, önizlemeli gönderim; sesli mesaj (MediaRecorder, dalga formu).
- Bağlantı önizleme kartı (sunucuda OG çekme, SSRF koruması).
- Mesaj düzenle (15 dk içinde, "düzenlendi" etiketi), sil ("Bu mesaj silindi").
- Gün ayraçları ("Bugün", "Dün", "3 Kasım"), ardışık mesajları grupla (avatar bir kez).
- Yeni mesaj gelince en alttaysan kaydır, değilsen "↓ 2 yeni mesaj" (bkz. `sky-infinite-lists`).
- Taslak saklama (konuşma değişince yazdığın kaybolmasın).
- Enter gönderir, Shift+Enter yeni satır (mobilde tersi).

## Bildirimler

- Uygulama açık ve o konuşmadaysa bildirim yok; başka sayfadaysa toast + sekme başlığı rozeti.
- Kapalıysa push/e-posta (gruplanmış: "Ayşe'den 3 yeni mesaj"); sessize alma (1 saat, 8 saat, her zaman).
- @mention sessizde bile bildirir.

## Arama

Mesaj gövdesinde full-text (bkz. `sky-search`), konuşma ve kişi filtresi; sonuca tıklayınca o mesaja kaydırıp vurgula.

## Moderasyon ve güvenlik

- Engelle / bildir (rapor kuyruğu admin panelinde), kötü kelime filtresi (isteğe bağlı), spam hız sınırı.
- Mesaj içeriği HTML değil düz metin + güvenli Markdown alt kümesi; bağlantılar `rel="nofollow ugc noopener"`.
- Ek dosyalar taranır, yalnızca katılımcılar imzalı URL ile erişir.
- Yetki: yalnızca katılımcılar okur/yazar — RLS veya servis kontrolü + realtime kanal yetkisi.

## Destek sohbeti widget'ı

Sağ altta balon; misafir de yazabilir (e-posta isteyerek); mesai dışı otomatik yanıt; ekip tarafında gelen kutusu
(atama, durum: açık/çözüldü), hazır yanıtlar, müşteri bilgisi yan paneli. AI ilk yanıt (bkz. `sky-ai`) + insana devret.
