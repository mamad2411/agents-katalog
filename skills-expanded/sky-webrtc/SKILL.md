---
name: sky-webrtc
description: >-
  WebRTC ile görüntülü/sesli görüşme, ekran paylaşımı ve P2P veri: getUserMedia ve izin akışı,
  RTCPeerConnection, sinyalleşme sunucusu (WebSocket), STUN/TURN (coturn), mesh vs SFU (LiveKit,
  mediasoup, Daily) seçimi, cihaz seçimi ve önizleme, bağlantı kalitesi ve yeniden bağlanma,
  kayıt, DataChannel, mobil tarayıcı tuhaflıkları, güvenlik ve gizlilik. "Görüntülü görüşme",
  "online muayene", "canlı yayın", "ekran paylaşımı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · WebRTC

## Mimari seçimi

| Senaryo | Seçim |
|---|---|
| 1-1 görüşme (online danışmanlık, muayene) | P2P + TURN yedeği — veya yönetilen servis |
| 3+ kişi, toplantı, webinar | **SFU**: LiveKit (açık kaynak + bulut), mediasoup, Janus; yönetilen: Daily, Twilio, Agora |
| Canlı yayın (1→çok) | WHIP/WHEP veya LiveKit/Cloudflare Stream; çok büyük kitlede HLS |
Çoğu ürün için **yönetilen SFU** (LiveKit Cloud / Daily) en hızlı ve güvenilir yol — kendi TURN/SFU altyapını işletmek ciddi iş.

## Temel akış (P2P)

```ts
const pc = new RTCPeerConnection({ iceServers: [{ urls: "stun:stun.l.google.com:19302" },
  { urls: "turn:turn.site.com:3478", username: tmpUser, credential: tmpPass }] });   // TURN kimliği kısa ömürlü, sunucudan
const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 }, audio: { echoCancellation: true, noiseSuppression: true } });
stream.getTracks().forEach((t) => pc.addTrack(t, stream));
pc.ontrack = (e) => (remoteVideo.srcObject = e.streams[0]);
pc.onicecandidate = (e) => e.candidate && signal.send({ type: "ice", candidate: e.candidate });
const offer = await pc.createOffer(); await pc.setLocalDescription(offer); signal.send({ type: "offer", sdp: offer });
```
Sinyalleşme (offer/answer/ICE alışverişi) için kendi WebSocket kanalın (bkz. `sky-realtime`), oda yetkisi sunucuda.
"Perfect negotiation" kalıbı çakışan teklifleri çözer. TURN olmadan kurumsal ağlarda/mobil operatörlerde bağlantıların bir kısmı kurulamaz.

## Kullanıcı deneyimi (insanların sevdiği)

- **Ön izleme ekranı**: kamera/mikrofon seçimi, ses seviyesi göstergesi, "Kameramı kapalı katıl", bulanık arka plan (MediaPipe / LiveKit eklentisi).
- İzin reddedildiyse tarayıcıya özel adım adım talimat; cihaz yoksa yalnızca ses.
- Bağlantı kalitesi göstergesi (`getStats`: paket kaybı, RTT), zayıf ağda video kalitesini düşür (simulcast + SFU).
- Yeniden bağlanma (ICE restart) ve "Bağlantı yeniden kuruluyor…" bandı.
- Ekran paylaşımı `getDisplayMedia`, konuşanı vurgulama, sessize alma kısayolu (Boşluk basılı tut = konuş).
- Bekleme odası ve "doktor sizi kabul edecek" akışı (sağlık/danışmanlık).

## Kayıt

Sunucu tarafında (SFU egress — LiveKit Egress) kayıt; tarayıcıda `MediaRecorder` yalnızca yerel. Kayıt öncesi **tüm katılımcılara açık bildirim ve onay** (KVKK; sağlık görüşmelerinde ek dikkat).

## Mobil ve tarayıcı

iOS Safari: `playsinline`, otomatik oynatma kısıtları (kullanıcı etkileşimi), arka plana geçince kamera durur. Android'de farklı codec'ler. Sekme arka plandayken video gönderimini düşür.

## Güvenlik

Medya DTLS-SRTP ile şifreli (P2P'de uçtan uca; SFU'da sunucu medyayı görür — E2EE gerekiyorsa Insertable Streams/SFrame). Oda bağlantıları kısa ömürlü token ile, katılımcı yetkisi (yayıncı/izleyici) sunucuda; TURN kimlik bilgileri kısa ömürlü.
