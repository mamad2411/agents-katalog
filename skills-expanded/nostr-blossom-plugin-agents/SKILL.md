# AGENTS.md

Dieses Dokument definiert die verbindlichen Engineering-Regeln für das Projekt.

## 1) Zielbild

Wir entwickeln ein Monorepo mit:

- `packages/blossom-plugin`: Wiederverwendbares Blossom-Upload-Plugin für Svelte-Clients und TipTap.
- `apps/demo`: Einfacher Nostr-Demo-Client zum Testen von Login, Upload, URL-Übernahme, Editor-Integration und Event-Publish.

## 2) Scope (MVP)

MVP enthält:

- Headless Upload-API (mehrere Blossom-Server, NIP-94 Tag-Ausgabe).
- Svelte Action für Input-Enhancement (Upload-Icon + URL ins Input).
- TipTap-Integration zum Einfügen hochgeladener Datei-Links.
- Demo-Client mit Login über NIP-07 und NIP-46.
- Event Composer inkl. Publish-Fluss.
- Upload History im Demo-Client.

MVP enthält **nicht**:

- Direkten `nsec` Login (deaktiviert aus Sicherheitsgründen).

## 3) Technische Standards

- Stack: SvelteKit + TypeScript + Vite.
- Paketmanager: pnpm.
- Monorepo: `apps/*` und `packages/*`.
- Alle öffentlichen APIs sind typisiert und stabil dokumentiert.

## 4) Blossom-/Nostr-Spezifikation

Implementierung richtet sich an:

- Blossom BUDs aus `hzrd149/blossom`.
- Nostrify Blossom Uploader (`nostrify.dev/upload/blossom`) als Referenz für Upload-Flows und NIP-94 Tags.

Regeln:

- Upload-Responses werden in NIP-94 Tags normalisiert.
- `url` Tag ist Pflicht; fehlt `url`, gilt Upload als ungültig.
- Multi-Server Verhalten ist robust gegen partiellen Server-Ausfall.

## 5) Architekturregeln

### Plugin (`packages/blossom-plugin`)

- `core/`: Protokoll- und Upload-Logik, framework-unabhängig.
- `svelte/`: Svelte Action + optionale Svelte UI.
- `tiptap/`: TipTap-Erweiterung/Commands.
- `index.ts`: Nur stabile Public Exports.

### Demo (`apps/demo`)

- `lib/nostr/`: Signer und Publish-Logik.
- `lib/components/`: UI-Komponenten.
- `lib/stores/`: UI- und Session-State.

## 6) Sicherheitsregeln

- Keine Speicherung sensibler Schlüssel im MVP.
- Kein `nsec`-Persistenzpfad im MVP.
- Externe Requests (Blossom, Relays) müssen Fehlerzustände explizit behandeln.
- Keine stillen Fallbacks bei Signaturfehlern.

## 7) Test-Policy

### P0 (Release-Blocker)

- Upload-Kern: Erfolg, Fehler, Timeout/Abort, Tag-Validierung.
- Svelte Input-Flow: Icon-Injection, Dialog, URL-Rückgabe.
- Demo End-to-End: Login (NIP-07/NIP-46), Upload, Publish mit korrekten Tags.
- Security-Scope: `nsec` im MVP nicht verfügbar.

### P1 (nach MVP)

- TipTap Edge-Cases und Recovery.
- Erweiterte Store-/History-Tests.
- Nightly Tests gegen mehrere öffentliche Blossom-Server.

## 8) Dokumentationsregeln

Für jede neue/geänderte öffentliche Komponente oder API ist Dokumentation Pflicht.

Mindestinhalt pro Komponente:

- Zweck und Verantwortungsbereich.
- Public API (Props/Optionen/Events/Returns).
- Zustände (idle/loading/success/error).
- Fehlerfälle und erwartetes Verhalten.
- Accessibility-Hinweise (falls UI-Komponente).

Mindestinhalt pro Usage-Dokumentation:

- Installationsschritte.
- Minimalbeispiel.
- Integrationsbeispiel in Host-App.
- Hinweise zu Limits/Annahmen (Server, MIME, Größe, Auth).

## 9) CHANGELOG-Regeln

Fortschritt wird in `CHANGELOG.md` nach Keep a Changelog geführt.

- Es gibt immer einen `## [Unreleased]` Abschnitt.
- Kategorien:
  - `### Added`
  - `### Changed`
  - `### Fixed`
  - `### Docs`
  - `### Tests`
  - `### Security`
- Jede PR ergänzt mindestens einen Eintrag in `Unreleased`.
- Release: Neuer Versionsabschnitt mit Datum, `Unreleased` wird geleert.

## 10) Definition of Done

Ein Task ist nur fertig, wenn:

1. Implementierung vollständig ist.
2. Relevante Tests vorhanden und grün sind.
3. Dokumentation für Komponenten/APIs/Usage aktualisiert wurde.
4. `CHANGELOG.md` unter `Unreleased` aktualisiert wurde.
5. Demo-Smoketest ohne kritische Fehler durchläuft.
