---
name: sky-system-design
description: >-
  Sistem tasarımı (gerçek projeler ve mülakatlar için): gereksinimleri netleştirme, kapasite
  tahmini (QPS, depolama, bant genişliği — zarf arkası hesap), yüksek seviye mimari, veri
  modeli ve depolama seçimi, ölçekleme (yatay, önbellek, CDN, replikasyon, sharding),
  tutarlılık/erişilebilirlik dengeleri (CAP pratikte), kuyruklar ve asenkron işleme, rate
  limiting, tekil ID üretimi, klasik tasarımlar (URL kısaltıcı, haber akışı, sohbet, bildirim,
  randevu sistemi) ve mülakat yapısı. "Sistem tasarımı", "nasıl ölçeklenir", "system design
  mülakatı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Sistem Tasarımı

## Çerçeve (45 dakikalık mülakatta da, gerçek projede de)

1. **Gereksinimler (5 dk)**: işlevsel (kullanıcı ne yapabilir) + işlevsel olmayan (ölçek, gecikme, erişilebilirlik, tutarlılık, maliyet). Kapsamı daralt.
2. **Kapasite tahmini (5 dk)**: kullanıcı, QPS (okuma/yazma oranı), depolama/yıl, bant genişliği.
3. **API ve veri modeli (5–10 dk)**: ana uç noktalar, tablolar/koleksiyonlar, erişim kalıpları.
4. **Yüksek seviye mimari (10 dk)**: istemci → CDN → yük dengeleyici → uygulama → önbellek → DB, kuyruklar, depolama.
5. **Derinleş (10–15 dk)**: darboğaz ve en zor parça (sıcak anahtar, sıralama, tekilleştirme, gerçek zamanlılık).
6. **Ödünleşimler ve gelecek (5 dk)**: neyi bilerek seçmedin, 10× büyümede ne değişir, izleme ve hata senaryoları.

## Zarf arkası sayılar

- 1 gün ≈ 86.400 sn ≈ 10^5 sn. 1M istek/gün ≈ 12 QPS ortalama; zirve ≈ 2–5× ortalama.
- Bellek ~100 ns, SSD rastgele okuma ~100 µs, aynı veri merkezi ağ turu ~0,5 ms, kıtalar arası ~100–150 ms.
- Tek Postgres örneği: iyi indeksle binlerce basit sorgu/sn; tek Redis: 100k+ işlem/sn.
- 1M kullanıcı × 1KB profil = 1GB — çoğu "büyük veri" aslında tek makineye sığar.

## Ölçekleme araç kutusu

| Sorun | Araç |
|---|---|
| Okuma yükü | önbellek (Redis, CDN), okuma replikaları, materialized view |
| Yazma yükü | kuyrukla tamponlama, toplu yazma, sharding (son çare) |
| Statik içerik | CDN, nesne depolama |
| Uzun işler | asenkron işçiler + kuyruk (bkz. `sky-jobs`) |
| Ani yük | otomatik ölçekleme, kuyruk, rate limit, zarif bozulma |
| Coğrafi gecikme | edge (CDN/Workers), bölgesel replikalar |
| Arama | ayrı arama motoru (bkz. `sky-search`) |
Önce dikey ölçek (daha büyük makine) — basit ve çoğu zaman yeterli; yatay ölçek için uygulama sunucuları durumsuz olmalı (oturum Redis/DB'de).

## Veri

- İlişkisel (Postgres) varsayılan; anahtar-değer (Redis/DynamoDB) yüksek hızlı basit erişim; doküman (Mongo) esnek şema; geniş sütun (Cassandra) devasa yazma; zaman serisi (Timescale/ClickHouse) metrik/analitik.
- **Sharding** anahtarı erişim kalıbından (kiracı ID'si çoğu SaaS'ta doğal); çapraz shard sorguları pahalı.
- **Replikasyon**: birincil-ikincil (okuma ölçeği, failover); replikasyon gecikmesi → "kendi yazdığını oku" sorunu (yazandan sonra birincilden oku).

## Tutarlılık ve erişilebilirlik

Ağ bölünmesinde ya tutarlılık ya erişilebilirlik (CAP); pratikte soru: "hangi veri güçlü tutarlılık ister?" — para, stok, rezervasyon (çift satış yok) → güçlü
(tek birincil, transaction, kısıt); beğeni sayısı, akış, analitik → nihai tutarlılık yeter.

## Sık bileşenler

- **Rate limiter**: token bucket / sliding window, Redis'te atomik sayaç (bkz. `sky-caching`).
- **Tekil ID**: UUIDv7 / ULID (zaman sıralı, koordinasyonsuz), Snowflake (64-bit, makine ID'li).
- **Idempotency**: istemci anahtarı + saklanan yanıt (bkz. `sky-payments`).
- **Bildirim fan-out**: yazmada (takipçi listelerine yaz — az takipçide) vs okumada (okuma anında birleştir — ünlülerde); karma.
- **Gerçek zamanlı**: WebSocket bağlantı sunucuları + pub/sub (bkz. `sky-realtime`).

## Klasik tasarımlar (kısa notlar)

- **URL kısaltıcı**: base62 kısa kod (sayaç veya rastgele + çakışma kontrolü), okuma ağırlıklı → önbellek + CDN 301/302, analitik asenkron.
- **Haber akışı**: gönderiler tablosu + kullanıcı başına önceden hesaplanmış akış (Redis sıralı küme), ünlüler için okuma anında birleştirme.
- **Sohbet**: bağlantı sunucuları, mesaj deposu (konuşma bazlı bölümleme), teslim/okundu durumları, çevrimdışıya push (bkz. `sky-chat-product`).
- **Randevu sistemi**: çift rezervasyonu DB kısıtıyla önleme, geçici slot tutma, saat dilimi, hatırlatma kuyruğu (bkz. `sky-scheduling`).
- **Bildirim sistemi**: olay → tercih kontrolü → kanal kuyrukları → sağlayıcılar, yeniden deneme, tekilleştirme (bkz. `sky-notifications`).

## Mülakat ipuçları

Sesli düşün, önce soru sor, sayıları yazıya dök, ödünleşimleri adlandır ("X'i seçtim çünkü …, bedeli …"), tek "doğru cevap" yok;
çalışan basit tasarımı önce kur, sonra ölçekle.
