---
name: publicist-germany-compliance
description: Germany compliance and legal guardrails, UWG §7, GDPR/ePrivacy, DDG §5, Pressekodex, DSK Werbung, TDDDG, Abmahnungsschutz. Use as mandatory compliance gate for all Germany earned media activities.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Germany compliance & legal guardrails, Germany market

**Scope**. Mandatory compliance checks for ALL Germany earned media activities. Pair with `publicist-germany` + all platform skills.

## Legal framework (must recheck at task time)

| Law/Regulation | Scope | Key Requirement | Escalation Trigger |
|---|---|---|---|
| **UWG §7** (Gesetz gegen unlauteren Wettbewerb) | E-Mail/Telefon/Telemedien-Werbung | Prior express consent (Einwilligung) required; narrow existing-customer exception §7(3) | Jeder Pitch per E-Mail/Telefon ohne Einwilligung |
| **GDPR / DSGVO** (Art. 6, 21, 95) | Personendatenverarbeitung | Lawful basis, transparency, objection rights, Art. 95 lex specialis for ePrivacy | Journalistendaten in CRM/Modell/Overseas |
| **ePrivacy / TDDDG** (§25, §7 UWG) | Cookies, Tracking, E-Mail-Werbung | Consent for non-essential tracking; UWG §7 for direct marketing | Opening-Tracking in Mailings, Pixel |
| **DDG §5** (Digitale-Dienste-Gesetz) | Impressum, Anbieterkennzeichnung | Name, Anschrift, Kontakt, Register, Regulator, USt-Id, leicht erkennbar, direkt erreichbar | Jede E-Mail, Landingpage, Presskit |
| **Pressekodex** (Deutscher Presserat) | Redaktionelle Ethik | Wahrheit, Sorgfalt, Korrektur, Trennung redaktionell/kommerziell | Sponsored Content Kennzeichnung |
| **DSK Werbung** (Datenschutzkonferenz) | Datenschutz bei Werbung | GDPR + UWG parallel; legitimate interest balancing | Legitimate Interest Assessments |
| **Abmahnung** (UWG §8, §12) | Wettbewerbsrechtliche Abmahnung | Wettbewerber/Verbraucherverbände können abmahnen. Kostenrisiko €1.000-5.000+ | Jede kommerzielle Aussendung |

## UWG §7, electronic direct marketing (Kernregel)

### Grundsatz
> **Unzulässig**. E-Mail/Telefon/Fax-Werbung ohne **vorherige ausdrückliche Einwilligung** des Empfängers.

### Ausnahme: Bestandskundenprivileg (§7 Abs. 3 UWG)
**Alle 4 Bedingungen müssen erfüllt sein.**
1. **E-Mail-Adresse im Zusammenhang mit Verkauf** erhalten (Kauf/Vertrag)
2. **Werbung für eigene ähnliche Waren/Dienstleistungen**
3. **Kunde hat nicht widersprochen** (Opt-out bei Erhebung + jeder Nachricht)
4. **Klarer Hinweis auf Widerspruchsmöglichkeit** (einfach, kostenlos)

### CJEU C-654/23 (Nov 2025), "Soft Opt-In" Erweiterung
- **Kostenlose Registrierung** = "Verkauf" i.S.v. Art. 13(2) ePrivacy-RL
- **Indirekte Vergütung** genügt (Kosten der Gratis-Leistung in Bezahl-Preis eingerechnet)
- **Newsletter = Direktwerbung** wenn kommerzieller Zweck (auch bei redaktionellem Inhalt)
- **Art. 95 DSGVO**. ePrivacy-Regelung verdrängt DSGVO-Prüfung für Zulässigkeit der Kommunikation

### Praktisches Compliance-Template (Pitch-E-Mail)
```
Betreff: [Kategorie] Konkretes Thema: Nutzen

Sehr geehrte Frau Dr. Müller,

[Bezug + Kernbotschaft + Ask]

---

**Absenderinformationen (§5 DDG / §5 TMG).**
Max Mustermann
Musterfirma GmbH
Musterstraße 1, 10115 Berlin
Geschäftsführer: Max Mustermann
HRB 12345 B, Amtsgericht Berlin
USt-IdNr.: DE123456789
Telefon: +49 30 1234567
E-Mail: max@musterfirma.de

**Widerspruchsrecht (UWG §7 / TDDDG).**
Sie erhalten diese E-Mail, weil Sie [Bezug: Kauf/Vertrag/Anfrage] bei uns getätigt haben.
Falls Sie keine weiteren Informationen wünschen, antworten Sie bitte kurz mit "Abbestellen"
oder klicken Sie hier: [Abmeldelink]. Dies ist kostenlos und jederzeit möglich.
```

## GDPR / DSGVO, journalist data handling

### Was sind Personendaten (Art. 4 DSGVO)?
- Journalist: Name, Redaktion, Beat, E-Mail, Telefon, Social Media, Lebenslauf, Artikelhistorie, Präferenzen
- **Kriterium**. "Identifizierte oder identifizierbare natürliche Person", Einzelnd oder in Kombination

### Cross-border transfer triggers (art. 44-50 DSGVO)
| Scenario | Status | Required Path |
|---|---|---|
| Salesforce/HubSpot/Notion/Airtable (US) mit Journalistendaten | **Drittlandtransfer** | SCC (Standardvertragsklauseln) + Transfer Impact Assessment + Einwilligung |
| Gmail/Outlook (US) für Journalistenkontakte | **Drittlandtransfer** | SCC + TIA + Einwilligung |
| OpenAI/Claude/Gemini API mit Journalistenprofilen | **Drittlandtransfer** | SCC + TIA + Einwilligung |
| Meltwater/Cision (US/UK) Monitoring | **Prozessor-Drittland** | AVV + SCC + TIA (Anbieter prüfen) |
| Lokale Tools (Nextcloud, Self-hosted, deutsche Cloud) | **Kein Drittland** | Kein Zusatzaufwand (Empfohlen: **ponytail: local-first**) |

### Minimal compliance checklist (per project)
- [ ] **Datenverzeichnis**. Welche Journalisten-Daten, wo gespeichert, Zweck, Rechtsgrundlage
- [ ] **Rechtsgrundlage**. Einwilligung / berechtigtes Interesse (Art. 6), dokumentiert
- [ ] **Informationspflichten** (Art. 13/14): Privacy Notice verlinkt in Signatur/Presskit
- [ ] **Betroffenenrechte** (Art. 15-22): 30-Tage-Frist für Auskunft/Löschung/Widerspruch
- [ ] **Löschkonzept**. Automatische Löschung nach Zweckentfall (z.B. 2 Jahre nach letztem Kontakt)
- [ ] **Auftragsverarbeitung** (Art. 28): AVV mit allen Tools (CRM, Mailing, Monitoring)

## DDG §5 / TMG §5, impressumspflicht

### Pflichtangaben (jede geschäftliche E-Mail, Landingpage, Presskit)
1. **Name/ Firma** (bei GmbH: "GmbH", bei AG: "AG")
2. **Anschrift** (Straße, PLZ, Ort, keine Postfach-only)
3. **Kontakt** (E-Mail + Telefon, **direkt erreichbar**)
4. **Vertretungsberechtigte** (Geschäftsführer, Vorstände)
5. **Registergericht + Registernummer** (HRB / HRA)
6. **USt-IdNr.** (DEXXXXXXXX)
7. **Aufsichtsbehörde** (falls zulassungspflichtig: BaFin, Gewerbeamt, etc.)

**In E-Mail-Signatur** (verkürzt zulässig):
```
Max Mustermann
Musterfirma GmbH | Musterstraße 1 | 10115 Berlin
GF: Max Mustermann | HRB 12345 B | USt-Id: DE123456789
Tel: +49 30 1234567 | max@musterfirma.de | www.musterfirma.de
```

## Pressekodex & DSK Werbung, editorial ethics

### Pressekodex (Kernregeln)
- **Ziffer 1**. Wahrheit, Keine falschen/verzerrten Tatsachen
- **Ziffer 2**. Sorgfalt, Recherche, Quellenprüfung, Korrektur
- **Ziffer 3**. Korrektur, Unrichtiges unverzüglich berichtigen
- **Ziffer 7**. Trennung, Redaktionell vs. kommerziell deutlich kennzeichnen
- **Ziffer 8**. Interessenkonflikte, Offenlegen (Beteiligungen, Mandate)

### DSK Orientierungshilfe Werbung (2018, noch aktuell)
- **GDPR + UWG parallel anwenden.** Nicht entweder/oder.
- **Legitimes Interesse** (Art. 6 Abs. 1 f): Interessenabwägung dokumentieren
- **Widerspruchsrecht** (Art. 21): Prominent, einfach, kostenlos
- **Profiling/Scoring**. Besondere Vorsicht, Transparenz

## Abmahnungsschutz, Risikominimierung

### Typische Abmahngründe (PR-Kontext)
| Verstoß | Beispiel | Risiko |
|---|---|---|
| **UWG §7** | Kaltakquise-E-Mail ohne Einwilligung | €1.500-3.000 + Unterlassung |
| **Irreführung** | "Marktführer" ohne Beleg, "kostenlos" mit Haken | €2.000-5.000 |
| **Fehlendes Impressum** | E-Mail ohne §5 DDG Angaben | €500-1.500 |
| **Tracking ohne Einwilligung** | Öffnungs-Pixel ohne Consent | €1.000-2.500 |
| **Pressekodex Ziff. 7** | Sponsored Content nicht als "Anzeige" gekennzeichnet | Presserat-Rüge + Reputationsschaden |

### Abmahnung erhalten, Sofort-Reaktion
1. **Nicht ignorieren.** Fristen (meist 7-14 Tage) laufen.
2. **Nicht selbst unterschreiben.** Anwalt (Fachanwalt IT-Recht / Gewerblicher Rechtsschutz).
3. **Prüfen**. Berechtigt? Teils berechtigt? Unberechtigt?
4. **Modifizierte Unterlassungserklärung.** Nur das Notwendige anerkennen.
5. **Prozesskosten vermeiden.** Vergleich oft günstiger als Klage.

## Compliance checklist (per Pitch/Release)
- [ ] **UWG §7**. Einwilligung vorliegend ODER Bestandskundenprivileg (4 Bedingungen) erfüllt
- [ ] **CJEU C-654/23**. Soft-Opt-In geprüft (kostenlose Registrierung = Verkauf?)
- [ ] **DSGVO**. Rechtsgrundlage dokumentiert, Drittlandtransfer geprüft/ausgeschlossen
- [ ] **DDG §5**. Vollständiges Impressum in E-Mail/Presskit/Link
- [ ] **TDDDG §25**. Tracking-Consent für Öffnungs-Pixel/Links
- [ ] **Pressekodex**. Sponsored Content als "Anzeige"/"Sponsored" gekennzeichnet
- [ ] **Absenderkennung**. Klarer Name + Organisation (kein "info@", "press@")
- [ ] **Opt-out**. Einfache, kostenlose Abmeldemöglichkeit in jeder kommerziellen Mail
- [ ] **Abmahnungssicher**. Keine unbelegten Superlative ("Marktführer", "einzigartig", "Nr. 1")

## Negative patterns (Vermeiden)
- Verteiler gekauft, also darf ich mailen. Keine Einwilligung bedeutet einen UWG-Verstoß.
- Journalistendaten sind öffentlich, also DSGVO-egal. Öffentlich zugänglich heißt nicht frei verwertbar.
- Tracking-Pixel sind technisch notwendig. TDDDG §25 verlangt Einwilligung.
- Der Pressekodex gilt nur für Journalisten. PR unterliegt ebenfalls Ziffer 7 zur Trennung.
- Eine Abmahnung ist nur eine Drohung. Abmahnungen können durchgesetzt werden und Kosten verursachen.

## References
- `https://www.gesetze-im-internet.de/uwg_2004/__7.html`, UWG §7
- `https://eur-lex.europa.eu/eli/reg/2016/679/oj`, DSGVO
- `https://www.gesetze-im-internet.de/ddg/__5.html`, DDG §5
- `https://www.presserat.de`, Pressekodex PDF
- `https://datenschutzkonferenz-online.de/media/oh/20181107_oh_werbung.pdf`, DSK Werbung
- `https://www.sza.de/en/thinktank/cjeu-existing-customer-privilege-newsletter-without-consent`, C-654/23 Analysis
- `skills/publicist-germany/references/law-and-ethics.md`
- `skills/publicist-germany/references/sources.md`

## What this skill does not do
- NG No legal advice (escalate to German-qualified counsel)
- NG No automated compliance checker
- NG No MCP/CLI tools (reference only)
