# Voice Notes Pro

Inteligentna transkrypcja i kategoryzacja notatek gosowych z WhatsApp.

## Opis

Voice Notes Pro automatycznie transkrybuje notatki gosowe wysane przez WhatsApp i kategoryzuje je do odpowiednich plikw Markdown. Obsuguje 6 kategorii: teksty piosenek, zadania, zakupy, pomysy, baz ludzi i watchlist filmw/seriali.

## Funkcje

- ?? Transkrypcja przez Whisper API (OpenAI)
- ??? Automatyczna kategoryzacja po sowach-kluczach
- ?? Zapis w Markdown z timestampami
- ?? Baza ludzi (dodawanie/sprawdzanie osb)
- ?? Watchlist (filmy/seriale do obejrzenia)
- ? Zadania z priorytetem i deadline
- ?? Lista zakupw z licznikiem produktw
- ?? Pomysy z tagowaniem projektw

## Triggery

Uywaj tego skill'a gdy uytkownik:
- Wysya notatk gosow przez WhatsApp
- Prosi o transkrypcj audio
- Dyktuje tekst piosenki
- Dodaje zadanie gosem
- Dyktuje list zakupw
- Zapisuje pomys gosowo
- Dodaje osob do bazy kontaktw
- Zapisuje film/serial do watchlisty

## Kategorie

### 1. ?? Piosenki
**Sowa-klucze:** "dyktuj", "tekst utworu", "piosenka", "rap", "zwrotka", "refren"
**Lokalizacja:** `~/notes/songs/brudnopis.md`

### 2. ? Zadania
**Sowa-klucze:** "zadanie", "todo", "zrb", "zadzwo", "napisz", "wylij"
**Lokalizacja:** `~/notes/tasks/inbox.md`

### 3. ?? Zakupy
**Sowa-klucze:** "zakupy", "kup", "kupi", "do sklepu", "lista zakupw"
**Lokalizacja:** `~/notes/lists/shopping.md`

### 4. ?? Pomysy
**Sowa-klucze:** "pomys", "idea", "projekt", "fajnie by byo", "moe warto"
**Lokalizacja:** `~/notes/ideas/[data]-[projekt]/README.md`

### 5. ?? Baza Ludzi
**Sowa-klucze:** "dodaj osob", "osoba", "kontakt", "sprawd osob"
**Lokalizacja:** `~/notes/people/database.md`

### 6. ?? Watchlist
**Sowa-klucze:** "zapisz film", "serial", "obejrze", "watchlist", "do obejrzenia"
**Lokalizacja:** `~/notes/watchlist/watchlist.md`

## Przykady uycia

### Piosenka
```
?? Uytkownik (voice): "Dyktuje tekst utworu: jestem te o eN aka cinacz Gw..."
? Bot: "?? Zapisano tekst w ~/notes/songs/brudnopis.md"
```

### Zadanie
```
?? Uytkownik (voice): "Zadanie: zadzwoni do klienta jutro o 10"
? Bot: "? Dodano zadanie: zadzwoni do klienta jutro o 10"
```

### Zakupy
```
?? Uytkownik (voice): "Zakupy: mleko, chleb, jajka, maso"
? Bot: "?? Dodano 4 produkty do ~/notes/lists/shopping.md"
```

### Baza Ludzi
```
?? Uytkownik (voice): "Dodaj osob: Michael Jackson, urodzony 1958, zmar 2009"
? Bot: "? Dodano: Michael Jackson
?? 1958 - 2009
?? 2026-02-07 18:30
?? ~/notes/people/database.md"
```

### Watchlist
```
?? Uytkownik (voice): "Zapisz film: Oppenheimer Christopher Nolan"
? Bot: "?? Dodano: Oppenheimer
?? ~/notes/watchlist/watchlist.md"
```

## Wymagania

- OpenAI API key (dla Whisper)
- WhatsApp poczony z OpenClaw
- Node.js z npm
- Uprawnienia do zapisu w `~/notes/`

## Konfiguracja
```json
{
  "voice-notes-pro": {
    "enabled": true,
    "whatsapp": {
      "enabled": true,
      "phoneNumber": "+48534722885"
    },
    "whisper": {
      "model": "whisper-1",
      "language": "pl"
    },
    "directories": {
      "songs": "/root/notes/songs",
      "tasks": "/root/notes/tasks",
      "shopping": "/root/notes/lists",
      "ideas": "/root/notes/ideas",
      "people": "/root/notes/people",
      "watchlist": "/root/notes/watchlist"
    }
  }
}
```

## Instalacja
```bash
cd ~/.openclaw/skills/voice-notes-pro
npm install
openclaw gateway restart
```

## Status

? **Production Ready**
- Testowany z WhatsApp
- Obsuguje polskie i angielskie notatki
- Automatyczne backupy plikw
- Error handling dla bdnych transkrypcji

## Author

Created for Toniacz - AI automation specialist ??