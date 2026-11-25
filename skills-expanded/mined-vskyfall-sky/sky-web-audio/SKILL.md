---
name: sky-web-audio
description: >-
  Web'de ses ve müzik uygulamaları: Web Audio API (AudioContext, düğüm grafiği, gain, filtre,
  analyser), otomatik oynatma kısıtları ve kilit açma, Tone.js ile ritim/sentez/zamanlama,
  ses görselleştirme (dalga formu, spektrum), mikrofon kaydı (MediaRecorder) ve sesli mesaj,
  ses oynatıcı (podcast/müzik — Media Session API ile kilit ekranı kontrolleri), düşük gecikme,
  AudioWorklet ve erişilebilirlik. Müzik/ses uygulaması, oynatıcı, sesli not veya ses
  efektleri gerektiğinde kullan.
disable-model-invocation: true
---

# Sky · Web Ses

## AudioContext ve kilit açma

```ts
const ctx = new AudioContext();
document.addEventListener("pointerdown", () => ctx.state === "suspended" && ctx.resume(), { once: true });
```
Tarayıcılar kullanıcı etkileşimi olmadan ses çalmaz → ilk dokunuşta `resume()` ("Başlamak için dokun"). Tek `AudioContext` paylaş (çok sayıda oluşturma).

## Düğüm grafiği

```ts
const buffer = await ctx.decodeAudioData(await (await fetch("/sfx/click.mp3")).arrayBuffer());
function play(rate = 1) {
  const src = ctx.createBufferSource(); src.buffer = buffer; src.playbackRate.value = rate * (0.95 + Math.random() * 0.1);
  const gain = ctx.createGain(); gain.gain.value = settings.sfxVolume;
  src.connect(gain).connect(ctx.destination); src.start();
}
```
Kaynak → gain → filtre (`BiquadFilterNode`) → `AnalyserNode` → hedef. Parametre değişimlerini `setTargetAtTime`/`linearRampToValueAtTime` ile yumuşat (tık sesi olmasın).

## Tone.js (müzik)

Sentezleyiciler, örnekleyici (sampler), efektler (reverb, delay), **Transport** ile tempo ve doğru zamanlama (`Tone.Transport.scheduleRepeat`), nota/ölçü gösterimi ("4n", "8n"). Ritim makinesi, piyano, sekansör uygulamaları için.

## Görselleştirme

`AnalyserNode.getByteFrequencyData` → canvas'ta spektrum çubukları; `getByteTimeDomainData` → dalga formu; `requestAnimationFrame` döngüsü, sekme gizliyken dur. Dosya dalga formu için wavesurfer.js (bölge seçimi, yakınlaştırma).

## Kayıt ve sesli mesaj

```ts
const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
const rec = new MediaRecorder(stream, { mimeType: MediaRecorder.isTypeSupported("audio/webm") ? "audio/webm" : "audio/mp4" });
```
Basılı tut-kaydet, iptal için kaydır, süre göstergesi, canlı dalga formu, yükleme öncesi önizleme (bkz. `sky-chat-product`). Safari `audio/mp4` üretir — sunucuda dönüştürme gerekebilir. Konuşmayı metne çevirme: Web Speech (bkz. `sky-browser-apis`) veya sunucu tarafı STT.

## Oynatıcı (podcast, müzik, ders)

`<audio>` + özel kontroller (oynat/duraklat, ±15 sn, hız 0.75–2×, ilerleme, kalan süre), kaldığı yeri hatırlama (localStorage), **Media Session API** ile kilit ekranı/bildirim kontrolleri ve kapak görseli — mobilde "gerçek uygulama" hissi. HLS akışı için hls.js.

## İleri

AudioWorklet (özel DSP, düşük gecikme, ana thread dışında), Web MIDI API (MIDI klavye), `latencyHint: "interactive"`.

## Erişilebilirlik

Otomatik çalan ses yok, görünür ses kontrolü ve sessiz düğmesi, ses içeriğine metin/altyazı alternatifi, klavye ile tüm kontroller, ayrı müzik/efekt seviyeleri.
