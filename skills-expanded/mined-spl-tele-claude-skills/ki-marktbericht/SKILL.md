---
name: ki-marktbericht
description: "Erstellt strukturierte, faktenbasierte Marktberichte über neue KI-Fähigkeiten und -Funktionen weltweit. Trigger-Phrasen: KI-Neuigkeiten, AI News, KI-Marktbericht, neue KI-Features, KI-Updates, was gibt es Neues bei KI, AI-Ankündigungen, KI-Entwicklungen, KI-Nachrichten. Nutze diesen Skill wenn der Benutzer nach aktuellen KI-Nachrichten fragt, neue Funktionen von KI-Tools erfahren möchte, oder einen Überblick über KI-Marktentwicklungen benötigt. Alle Informationen werden aus offiziellen Quellen doppelt validiert."
---

# KI-Marktbericht Skill

Erstellt faktenbasierte, doppelt validierte Berichte über neue KI-Entwicklungen.

## Kernprinzipien

1. **Nur offizielle Quellen**: Unternehmensblogs, Pressemitteilungen, verifizierte Tech-News (TechCrunch, The Verge, Heise, Ars Technica, CNBC, Fortune, SiliconANGLE)
2. **Keine Meinungen**: Ausschließlich faktische Informationen, keine Einschätzungen oder Spekulationen
3. **Doppelte Validierung**: Jede Information aus mindestens einer offiziellen Quelle verifizieren
4. **Diskrepanzen kennzeichnen**: Bei widersprüchlichen Quellen beide nennen

## Abzudeckende KI-Kategorien

| Kategorie | Beispiele |
|-----------|-----------|
| Large Language Models | OpenAI GPT, Anthropic Claude, Google Gemini, Meta Llama, Mistral, xAI Grok, Cohere |
| Bildgenerierung | Midjourney, DALL-E, Stable Diffusion, Adobe Firefly, Leonardo AI, Ideogram |
| Videogenerierung | OpenAI Sora, Runway, Pika Labs, Kling AI, Luma AI, HeyGen |
| Coding-Assistenten | GitHub Copilot, Cursor, Windsurf, Codeium, Tabnine, JetBrains AI, Replit |
| Automatisierung & Agenten | n8n, Zapier AI, Microsoft Copilot, LangChain, CrewAI |
| DevOps & Infrastruktur-KI | Datadog Bits AI, HashiCorp, Docker AI, Kubernetes-Tools |
| Sprach- und Audio-KI | ElevenLabs, OpenAI Voice/Whisper, Suno AI, Udio |
| KI-Hardware & Investments | NVIDIA, AMD, Intel, SoftBank, a16z, Sequoia |

## Recherche-Workflow

### Schritt 1: Zeitraum bestimmen
- Standard: Letzte 72 Stunden
- Bei Benutzerangabe: Angegebenen Zeitraum verwenden

### Schritt 2: Systematische Suche
Für jede Kategorie mindestens eine Suche durchführen:
```
[Kategorie] AI news [Zeitraum]
[Kategorie] announcement [Zeitraum]
[Unternehmen] release [Zeitraum]
```

### Schritt 3: Validierung
- Jede Information mit Originalquelle abgleichen
- Datum der Ankündigung explizit verifizieren
- Bei Unsicherheit: Zusätzliche Suche durchführen

### Schritt 4: Strukturierte Ausgabe
Ergebnisse in Markdown-Tabellen formatieren.

## Output-Format

```markdown
# KI-Ankündigungen [Zeitraum]

## Zusammenfassung
[2-3 Sätze zu den wichtigsten Entwicklungen]

## Verifizierte Ankündigungen

### [Kategorie 1]
| Unternehmen | Feature | Datum | Quelle | Beschreibung |
|-------------|---------|-------|--------|--------------|
| ... | ... | ... | ... | ... |

## Keine Ankündigungen gefunden
[Liste der Kategorien ohne neue Meldungen]

## Methodologie
[Kurze Beschreibung der verwendeten Quellen und Validierung]
```

## Qualitätskriterien

**Erforderlich:**
- Nur verifizierte Fakten
- Exakte Datumsangaben
- Direkte Links zu Originalquellen
- Klare Kennzeichnung von Gerüchten vs. bestätigten News
- Transparenz bei fehlenden Informationen

**Verboten:**
- Persönliche Einschätzungen
- Spekulationen über zukünftige Entwicklungen
- Community-Gerüchte als Fakten

## Sprachliche Richtlinien

- Akademische Ausdrucksweise in einfachen Worten
- Deutsche Sprache, technische Begriffe im Original belassen
- Präzise, ohne Füllwörter
- Neutral und faktenorientiert
