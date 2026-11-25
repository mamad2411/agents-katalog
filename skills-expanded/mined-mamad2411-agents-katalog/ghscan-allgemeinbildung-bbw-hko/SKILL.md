# Evaluation — KI-Aufträge (2+1) Skill für bbw-hko

**Frage:** Wie bauen wir eine Skill, die nach der Generierung einer bbw-hko-Einheit
durch deren Inhalte geht und – komplementär zur publizierten Unit – die
KI-Dokumente erzeugt, die hko-deploy bereits rendert?

**Entscheid (Pietro):** Gleiches Rendering wie hko-deploy, an bbw-hko angepasst –
die zwei Repos sind sehr ähnlich.

**Erweiterung (Pietro, 2026-06-17):** Die KI-Aufträge sollen die Lernenden, wo
möglich, auch auf den **KN** vorbereiten; zusätzlich ein **4. KI-Doc** als
learner-facing **KI-Lernbegleiter** — Strategien + Prompts zum Repetieren und
zur KN-Vorbereitung («KI-Fluency fürs Lernen»). Die Suite wird damit **2+1+1**
(siehe §5).

**Datum:** 2026-06-17 · Status: Evaluation, noch nicht umgesetzt.

---

## 1. Vorbild: Wie hko-deploy die «KI-Aufträge (2+1)» erzeugt

In der Skill `hko-3er-to-praxis` (hko-deploy) entstehen die drei KI-Dokumente aus
**zwei JSON-Dateien**, in zwei separaten Phasen:

| Phase | Datei | Inhalt |
|---|---|---|
| **Phase 5** | `{slug}_ki.json` | die **2 KI-Aufträge** (`assignments[2]`) |
| **Phase 8** | `{slug}_lernprompt.json` | der **+1 Prompting-Guide** |

«3 Dokumente» = 2 Dateien, aber 3 gerenderte Views (`ki_1`, `ki_2`, `lernprompt`).

### Phase 5 — die 2 KI-Aufträge (`ki.json`)

1. **Pattern-Scoring** (`references/ki-scoring.md`): Alle 7 Mission-KI-Patterns
   (`ai_gegenpositionen`, `ai_redaktion`, `ai_lernassistent`, `ai_ethik_tribunal`,
   `ai_entscheidungscoach`, `ai_prompt_duell`, `ai_zeitkapsel`) werden gescort
   gegen `prinzip.aspekte`, `sk_schnittmenge_kn.primary` (= sk_targets),
   `herausforderungen[*].handlungsprodukt_typ` und `praxis_spec`.
2. **Auswahl:** genau die **2 höchsten** Scores, die zwei *verschiedene*
   KI-Kompetenzen trainieren (sonst Drittplatzierten nachziehen). Minimum-Score 30.
3. **Pro Auftrag** befüllen: `pattern, titel, ziel, bezug, auftrag,
   prompt_strategie[], ki_frei_vorher, schritte[5], guetekriterien[3-4],
   reflexion[3]`. Set-Level zusätzlich: `nrlp_anker` + `ki_leitfragen`.
4. **Harte Regel (Check P6):** `bezug` muss **alle drei Herausforderungen + das
   Transfer-Prinzip** nennen — sonst ist es kein Set-Auftrag.

Leitidee (`ki-set-architecture.md`): **AI-Fluency, keine Produktions-Abkürzung.**
Die KI prüft/challengt/spiegelt das Handlungsprodukt, ersetzt es nie. Pflicht-
Gütekriterium: jede KI-Quelle nachgeschlagen.

### Phase 8 — der Lernprompt (`lernprompt.json`)

4 von 6 kanonischen Techniken (immer `rollen_prompting` + `kontextualisieren`,
+2 nach SK/Aspekt/Produkt-Signalen aus dem **Prinzip**), je mit `erklaerung`,
`thema_bezug`, `beispiel_basis`/`beispiel_fortgeschritten`, `warnung`, `baukasten`,
plus zwei `stacking_seite_1/2`-Blöcke (Prompt 2 baut explizit auf Prompt 1 auf).

### Rendering in hko-deploy

`setUnit.js` lädt `ki.json` + `lernprompt.json` als **separate, beim Laden
gemergte Dateien**; `SetWorkbench.jsx` rendert sie als drei Views unter der
Nav-Gruppe «KI-Fluency» (`ki_1`, `ki_2`, `lernprompt`), Farbpalette
`#1E3A5F / #E8F0FE / #3B6FD4`.

---

## 2. Befund: Was in bbw-hko schon passt — und was fehlt

### Datenmodell: praktisch deckungsgleich (Adapter ist trivial)

Die Scoring-Inputs liegen in bbw-hko in fast identischen Feldern:

| Scorer braucht | hko-deploy | bbw-hko | Differenz |
|---|---|---|---|
| sk_targets | `prinzip.sk_schnittmenge_kn` | `prinzip.sk_schnittmenge_kn` | **identisch** |
| Aspekte | `prinzip.aspekte` | `prinzip.aspekte` | **identisch** |
| Handlungsprodukt-Typen | `herausforderung_*.handlungsprodukt` | `herausforderung_*.handlungsprodukt` | **identisch** |
| Transfer-Szene (für `bezug` + Zeitkapsel/Voraussicht) | `prinzip.praxis_spec` | `prinzip.hybrid_situation_spec` + `kn.hybrid_situation` | **ein Feld umbenennen** |

Der einzige inhaltliche Unterschied: hko-deploy ist «Praxis-backwards» (2
Praxisaufträge), bbw-hko ist «KN-backwards» (Kompetenznachweis). Das **«Transfer-
Prinzip»**, das beide KI-`bezug`-Felder nennen müssen, ist in bbw-hko die
**KN-Hybrid-Situation** (`kn.hybrid_situation`) statt der Praxis-`transfer_situation`.
→ Reiner Input-Adapter, sonst keine Logikänderung.

### Renderer: das ist der eigentliche Aufwand

bbw-hko hat **keinerlei KI-Rendering**. Einheiten werden über
`EinheitWorkbench.tsx` publiziert → ein herunterladbares **ZIP aus HTML+DOCX**,
gebaut von React-Komponenten (`DocS`, `DocKnS`, `DocKnLp`, `DocAustausch`) +
`docx-builder.ts`. Es gibt:

- **kein** `DocKi` / `DocLernprompt`,
- **kein** Laden von ki/lernprompt-JSONs in `loadEinheit()`,
- **keine** Nav-Items im Workbench, **keinen** ZIP-Eintrag,
- **keine** `buildKi`/`buildLernprompt` im docx-builder.

Gute Nachricht: bbw-hkos Doc-Komponenten *sind* Ports der Renderer-Doc-Factories
(gemeinsames `chrome.tsx` mit `A4Page`, `Badge`, `Schreibfeld`, `SectionHead`).
Die hko-deploy-KI-Templates lassen sich also in dieselbe Komponenten-Idiomatik
übersetzen — «gleiches Rendering, an bbw-hko angepasst» ist realistisch.

---

## 3. Konsequenz: Die Arbeit zerfällt in zwei Teile

Eine Skill **allein** liefert das nicht. Es braucht:

### Teil A — Einmaliger Renderer-Port in bbw-hko (Hand/Claude Code, nicht pro Unit)

1. `src/lib/einheiten/types.ts` — Typen `KiJson` (`assignments[]`, `nrlp_anker`,
   `ki_leitfragen`), `LernpromptJson` **und `LernbegleiterJson`** ergänzen;
   `EinheitFullSet` um `ki` + `lernprompt` + `lernbegleiter` erweitern.
2. `src/lib/einheiten/index.ts` — `loadEinheit()` lädt zusätzlich
   `pickJson('ki')` + `pickJson('lernprompt')` + `pickJson('lernbegleiter')`
   (Glob deckt `*/*.json` bereits ab).
3. `src/components/einheiten/docs/DocKi.tsx` + `DocLernprompt.tsx` **+
   `DocLernbegleiter.tsx`** — neue A4-Doc-Komponenten, portiert aus hko-deploys
   KI-/Lernprompt-Templates (Lernbegleiter neu, siehe §5), auf `chrome.tsx`
   aufsetzend. Liefern Preview **und** `renderToStaticMarkup`-HTML.
4. `src/lib/einheiten/docx-builder.ts` — `buildKi()` + `buildLernprompt()`
   **+ `buildLernbegleiter()`**.
5. `src/components/einheiten/EinheitWorkbench.tsx` — Nav-Gruppe «KI-Fluency»
   (`doc-ki-1`, `doc-ki-2`, `doc-lernprompt`, **`doc-lernbegleiter`**) +
   ZIP-Einträge (HTML+DOCX).
6. `scripts/build-einheiten-index.mjs` + `einheiten.index.json` — `has.ki` /
   `has.lernprompt` / **`has.lernbegleiter`**-Flags ergänzen (optional, fürs
   Katalog-Badge).

Aufwand: überschaubar, weil es ein 1:1-Port etablierter Muster ist; aber es ist
echte App-Arbeit im bbw-hko-Repo, **kein** Per-Unit-Skill-Job.

### Teil B — Die Skill selbst (läuft pro Unit, nach den Assignments)

Ein **Fork von hko-3er-to-praxis, reduziert auf Phase 5 + Phase 8 + eine neue
Lernbegleiter-Phase (§5)**, mit bbw-hko-Input-Adapter. Lift-over praktisch
unverändert:

- `references/ki-set-architecture.md`, `ki-scoring.md`, `lernprompt-techniken.md`
- `assets/ki-set-template.json`, `lernprompt-template.json`
- Sprach-/Umlaut-/Gendern-Regeln, Coherence-Checks **P5, P6, P7** (Gütekriterien
  vorhanden, `bezug` deckt A/B/C + Transfer, Layer-Dateien separat).

Neu zu schreiben: `references/lernbegleiter-architecture.md` +
`assets/lernbegleiter-template.json` + Checks **L1–L3** (§5).

Anzupassen:

- **Scope-Zeile:** schreibt nur nach `bbw-hko/src/data/einheiten/<slug>/` →
  `ki.json` + `lernprompt.json` **+ `lernbegleiter.json`** (nicht ins
  `3er/`-Verzeichnis).
- **Input-Adapter:** liest bestehende `prinzip.json` + `kn.json` +
  `herausforderung_{A,B,C}.json`; mappt `praxis_spec` → `hybrid_situation_spec` /
  `kn.hybrid_situation`; `bezug`-Transfer-Prinzip = KN-Hybrid-Situation; der
  Lernbegleiter liest zusätzlich `kn.kn_typen[]` + `kn.rubrik_shared` (§5).
- **KN-Orientierung der 2 KI-Aufträge (weiche Regel):** wo das Pattern es
  zulässt, rahmt mind. ein Auftrag `reflexion[3].R3` explizit als Brücke zum KN
  (Transfer aufs künftige KN-Verhalten) — ohne den formativen Charakter der
  Aufträge zu ändern.
- **Trigger-Beschreibung:** «nachdem eine bbw-hko-Einheit fertig ist, erzeuge die
  komplementären KI-Aufträge + Lernprompt + Lernbegleiter».
- **Abschluss:** Hinweis auf `npm run build:einheiten-index` (falls has-Flags),
  Verifikations-Route im EinheitWorkbench.

---

## 4. Empfohlenes Vorgehen

1. **Zuerst Teil A** (Renderer-Port) als Claude-Code-Handoff in bbw-hko – einmal,
   mit der bestehenden `1.1.1_konflikt_kommunizieren`-Unit als Testfall (von Hand
   ein `ki.json` + `lernprompt.json` hineinlegen, Rendering verifizieren).
2. **Dann Teil B** (Skill) als `bbw-hko/.claude/skills/hko-ki-komplement/` —
   Fork der zwei Phasen + Adapter. (bbw-hko hat aktuell **kein** `.claude/skills/`,
   wird also neu angelegt.)
3. **Validierung:** Skill auf eine zweite Unit laufen lassen, im Workbench
   prüfen, ZIP-Download gegenchecken.

**Risiken / offene Punkte:**

- KI-Patterns in hko-deploy verweisen teils auf Praxis-spezifische Trade-offs
  (`trade_off_raum`); in bbw-hko aus `mehrdeutigkeits_architektur` /
  `kn.mehrdeutigkeits_pflicht` ziehen.
- `ai_zeitkapsel`/Voraussicht liest `zirkularitaet.r2/r3_voraussicht` — in beiden
  Repos vorhanden, vor Übernahme verifizieren.
- DOCX-Layout der **drei** neuen Docs muss A4-Overflow bestehen (gleicher Check
  wie bei DocKnS/DocKnLp).

---

## 5. Erweiterung — KN-Vorbereitung + 4. Doc «KI-Lernbegleiter»

### Warum das 4. Doc hierher passt

bbw-hko behält den **summativen KN** (anders als hko-deploy, das ihn durch
Praxisaufträge ersetzt hat). Eine KI-gestützte **Repetition + KN-Vorbereitung**
ist deshalb inhaltlich begründet — es ist die learner-facing Ergänzung zu den
zwei (eher produkt-/inhaltsbezogenen) KI-Aufträgen. Leitmotiv: **KI-Fluency fürs
Lernen** statt fürs Produzieren.

### Leitplanke (zwingend) — Integrität des KN

Der KN ist summativ und prüft **Transfer** über eine *neue* Hybrid-Szene/Persona.
Der Lernbegleiter bereitet darum auf die **Kompetenz** vor (Repetition,
Selbstabfrage, Übungs-Feedback), **nie auf die konkrete KN-Abgabe**. Verbote,
analog zur Regel «AI-Fluency, keine Produktions-Abkürzung»:

- Die KI darf **keine fertige KN-Lösung / kein KN-Produkt** erzeugen.
- Übungs-Fälle der KI sind **andere** Fälle als die KN-Hybrid-Situation
  (frische Persona/Szene) — der Begleiter trainiert das Übertragen, nicht das
  Auswendiglernen einer Musterlösung.
- Feedback-Prompts fordern **Hinweise auf Lücken, keine Musterantwort**.

### Inhalt (learner-facing, ~2 A4-Seiten — Schema `lernbegleiter-template.json`)

1. **Ziel** — KI als Lerncoach für Repetition + KN-Vorbereitung (1 Satz).
2. **KI-frei zuerst** — eigener Wissensstand gegen das `kern_kompetenzversprechen`
   (Selbsteinschätzung), bevor die KI genutzt wird.
3. **Strategie-Karten** (Lerntechnik × kopierbarer Prompt), je `technik`, `wann`,
   `prompt_basis`, `prompt_fortgeschritten`, `warnung`:
   - **Abfragen / Retrieval** — «Stell mir 5 Prüfungsfragen zu … und gib die
     Lösung erst nach meiner Antwort.»
   - **Selbst-Erklären / Feynman** — «Ich erkläre dir X; finde Lücken und Fehler
     in meiner Erklärung.»
   - **Mock-Transfer-Fall** — «Gib mir einen *neuen* Fall zum Thema und bewerte
     meine Lösung nach diesen Kriterien {SuK/Ges aus `rubrik_shared`}.»
   - **Übungs-Feedback** — «Hier ist mein Übungsversuch; nenne, was nach
     Kriterium X fehlt — **keine** Musterlösung.»
   - **Repetitionsplan / Karteikarten** — «Erstelle aus diesen Themen einen
     Repetitionsplan / Karteikarten.»
4. **KN-Typ-Tracks** — pro möglichem `kn.kn_typen[]` ein kurzer Übungsfokus
   (Fachgespräch → mündliche Begründung proben; Mini-Case schriftlich →
   schriftlichen Transfer üben; Werkschau → Präsentation/Verteidigung proben).
5. **Bezug zur Rubrik** — die SuK/Ges-Dimensionen aus `rubrik_shared` als
   Übungsziele sichtbar machen (worauf wird bewertet).
6. **Selbstcheck + Warnung** — Verifikationspflicht, eigene Worte, Integritäts-
   Leitplanke in Lernenden-Sprache.

### Neue Coherence-Checks

| # | Check | Severity |
|---|---|---|
| L1 | Lernbegleiter referenziert `kern_kompetenzversprechen` + `kn.kn_typen[]` + `rubrik_shared`-Dimensionen | ERR |
| L2 | Kein Prompt erzeugt das KN-Produkt / eine Musterlösung; Mock-Fälle sind disjunkt von der KN-Hybrid-Situation | ERR |
| L3 | Jede Strategie-Karte hat `prompt_basis` **und** eine technik-spezifische `warnung` (nicht generisch) | ERR |

### Folge fürs Vorgehen (§4)

Teil A wächst um **eine** Komponente (`DocLernbegleiter` + `buildLernbegleiter` +
Lade-/Nav-/ZIP-Eintrag). Teil B wächst um **eine** Phase (Lernbegleiter) + die
weiche KN-Regel für die zwei KI-Aufträge. Beim Renderer-Test (`1.1.1_konflikt_
kommunizieren`) ein `lernbegleiter.json` mitlegen und mitprüfen.
