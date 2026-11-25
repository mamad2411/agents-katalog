# AssemblyAI Transcriber 🎙️

Transkribiert Audio-Dateien mit Speaker Diarization (wer spricht wann).

## Features

- ✅ Transkription in 100+ Sprachen
- ✅ Speaker Diarization (Sprecher A, B, C...)
- ✅ Timestamps pro Äusserung
- ✅ Automatische Spracherkennung
- ✅ Unterstützt MP3, WAV, M4A, FLAC, OGG, WEBM

## Setup

1. AssemblyAI Account erstellen: https://www.assemblyai.com/
2. API Key holen (kostenlos, 100 Min/Monat im Free Tier)
3. Config speichern:

```json
// ~/.assemblyai_config.json oder workspace/.assemblyai_config.json
{
  "api_key": "YOUR_API_KEY"
}
```

## Verwendung

### Audio transkribieren (lokal)

```
Transkribiere die Datei /pfad/zur/aufnahme.mp3 mit Speaker Diarization
```

### Audio von URL transkribieren

```
Transkribiere https://example.com/meeting.mp3
```

### Telegram Voice Message

Einfach eine Sprachnachricht senden - der Agent transkribiert automatisch!

## Workflow

1. Audio wird zu AssemblyAI hochgeladen
2. Transkription + Diarization läuft (wenige Sekunden)
3. Ergebnis wird formatiert zurückgegeben:

```
## Transkript

**Speaker A** [00:00]: Hallo zusammen, willkommen zum Meeting.
**Speaker B** [00:03]: Danke! Freut mich dabei zu sein.
**Speaker A** [00:06]: Lass uns mit dem ersten Punkt starten...
```

## API Script

Das Script `scripts/transcribe.py` kann direkt aufgerufen werden:

```bash
python3 scripts/transcribe.py /pfad/zur/datei.mp3
python3 scripts/transcribe.py https://example.com/audio.mp3
```

## Kosten

- **Free Tier**: 100 Minuten/Monat kostenlos
- **Danach**: ~$0.01/Minute (~CHF 0.01/Min)

## Output Formate

Der Agent kann das Transkript:
- Im Chat anzeigen
- Als Markdown-Datei speichern
- In Obsidian ablegen (z.B. `/Voice Notes/`)
- Zusammenfassen lassen

## Tipps

- Für beste Speaker Diarization: klare Sprecherwechsel, wenig Überlappung
- Hintergrundgeräusche werden gut gefiltert
- Bei mehreren Sprachen: Auto-Detection funktioniert gut

---

*Skill by xenofex7 🦭*
