---
name: transcriptr
description: "YouTube transkript, ozet, arastirma ve soru-cevap araci. transcriptr'in yerel headless API'sini (localhost:8080) kullanir; her projeden cagrilabilir. Triggers: transcriptr, youtube transkript, video transkript, videoyu transkript et, video ozet, videoyu ozetle, youtube ozet, konu arastir, youtube arastir, video arastir, videolardan ozet, video soru cevap, transcript, summarize video, research youtube."
---

# transcriptr — YouTube transkript & arastirma (headless)

transcriptr'in yerel API'si ile bir konuyu YouTube videolarindan **arastir**,
**transkript** cikar, **ozetle**, **birlestir** ve **soru sor**. Baska
projelerden de calisir. LLM saglayicilar kullanicinin login'li CLI'larini
(Claude/Gemini) kullanir — API key yok, token ucreti yok.

Proje yolu: `/Users/musabkara/Projects/transcriptr`

## 1) API'yi hazirla (her zaman once)

```bash
# Calisiyor mu?
curl -s --max-time 2 http://localhost:8080/health || {
  # Degilse arka planda baslat
  ( cd /Users/musabkara/Projects/transcriptr && nohup dart run tool/caption_server.dart >/tmp/transcriptr-api.log 2>&1 & )
  # Hazir olmasini bekle
  curl -s --retry 40 --retry-connrefused --retry-delay 1 http://localhost:8080/health
}
```

## 2) Istege gore endpoint sec

Hepsi `provider=` alir: `claude` (varsayilan, hizli **haiku** modeli) · `gemini`
· `gpt` · `ollama` · `extractive` (ucretsiz/offline). `model=` ile model sec.
Sorgulari **URL-encode et** (bosluk → `%20`).

### Konu arastir (EN GUCLU — tek cagri)
Kullanici "X arastir / X hakkinda videolar / X ozeti cikar" derse:
```bash
curl -s "http://localhost:8080/research?q=KONU&limit=5&provider=claude&ask=SORU(opsiyonel)"
```
Doner: `videos[]` (her birinin ozeti) + `digest` (birlesik) + `answer` (ask varsa).
Filtre eklenebilir: `&sort=date|views &duration=short|medium|long &upload=today|week|month|year &subtitles=true`.

### Tek video transkript
```bash
curl -s "http://localhost:8080/transcribe?url=URL&format=text&timestamps=false"
```
`format=json|text|srt` · `captions=<dil-kodu>` ile altyazi dili.

### Tek video ozet
```bash
curl -s "http://localhost:8080/summary?url=URL&provider=claude&mode=summary&format=text"
```
`mode=summary|bullets|tldr|detailed|outline` · `lang=English|Turkish|...` (ceviri).

### Sadece arama (liste)
```bash
curl -s "http://localhost:8080/search?q=KONU&limit=10&sort=date&duration=short&subtitles=true"
```

### Playlist / kanal
```bash
curl -s "http://localhost:8080/playlist?url=PLAYLIST_VEYA_KANAL_URL&limit=20"
```

### Coklu video birlesik ozet (map-reduce)
Belirli birkac videoyu tek ozete indir. Once her birini ozetler, sonra birlestirir.
```bash
curl -s "http://localhost:8080/digest?ids=ID1,ID2,ID3&provider=claude&sentences=5"
```
Doner: `videos[]` (her birinin ozeti) + `digest` (birlesik). `provider` varsayilani `extractive`.

### Coklu videoya soru sor
```bash
curl -s "http://localhost:8080/ask?ids=ID1,ID2&q=SORU&provider=claude&format=text"
```
LLM saglayici zorunlu (`extractive` reddedilir). Doner: `answer` + `videos[]`.

### Yapilandirilmis cikarim (not / adim / SSS ...)
Transkripti yapilandirilmis bir belgeye cevir.
```bash
curl -s "http://localhost:8080/extract?videoId=ID&type=notes&provider=claude&format=text"
```
`type`: `notes|takeaways|steps|faq|quotes|glossary|recipe`. LLM zorunlu.

### Kutuphane RAG (cok videoda ara + alintili cevap)
Once indeksle (Ollama `nomic-embed-text`, ucretsiz/offline), sonra sor.
```bash
curl -s "http://localhost:8080/index?videoId=ID"            # her video icin bir kez
curl -s "http://localhost:8080/rag?q=SORU&provider=claude"  # tum indeksli kutuphanede
```
`/rag` doner: `answer` + `sources[]` (`title`, `ts_ms`, `score`). LLM + Ollama zorunlu.

### Yerel dosya transkript (Whisper, offline)
YouTube degil, diskteki bir ses/video dosyasi icin.
```bash
curl -s "http://localhost:8080/transcribe-file?path=/abs/yol/ses.mp3&format=text"
```
Sunucunun eristigi yerel `path` gerekir (ffmpeg + whisper.cpp).

### Yardimci
`GET /providers` (hangi LLM bagli) · `GET /languages?videoId=ID` ·
`GET /has-captions?ids=ID1,ID2` (toplu altyazi kontrolu) · `GET /` (tum API).

## 3) Sun

- JSON donen yerlerde onemli alanlari (`video_title`, `summary`, `digest`,
  `answer`) cikar; ham JSON'u dokme.
- Kullaniciya **Turkce**, derli toplu sun.
- `502` + `connect` ipucu donerse: ilgili CLI'a giris gerekiyor (mesaji aktar).

## Notlar
- Sadece **YouTube**; videonun altyazisi olmali.
- GPT/Codex bozuk kurulumda calismaz; Claude + Gemini sorunsuz. Ollama opt-in.
- Hizli + ucretsiz ama kaba ozet icin `provider=extractive`.
