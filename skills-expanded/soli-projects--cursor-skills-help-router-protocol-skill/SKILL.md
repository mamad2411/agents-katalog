# Skill: Help Router Protocol

> Adapter Cursor della skill `help-router-protocol`.

Skill sottostante al comando `/help` (capability routing in linguaggio naturale).
Riceve una **query in linguaggio naturale** e risponde con la capability della factory
piu' pertinente, leggendo `CAPABILITIES.md` come unica fonte di verita'.

> **Invariante anti-fabbricazione**: questa skill produce esclusivamente
> corrispondenze da `CAPABILITIES.md`. Non genera capability inventate, non
> estrapola da memoria pregressa, non hardcoda nomi di capability nel prompt.
> Se `CAPABILITIES.md` non copre un caso, lo dice esplicitamente.

---

## Fase 1 — Bootstrap

Verifica la precondizione strutturale prima di qualsiasi elaborazione.

1. Controlla che `CAPABILITIES.md` esista alla root del repo (path assoluto o
   relativo alla root della factory).
2. Se il file **non esiste**:
   ```
   CAPABILITIES.md non trovato.
   Eseguire prima la sequenza US-110 (TSK-210 + TSK-211) per produrre il documento.
   Fino ad allora, il routing automatico non e' disponibile.
   ```
   STOP — non procedere oltre.
3. Se il file esiste, continua alla Fase 2.

---

## Fase 2 — Parse

Leggi `CAPABILITIES.md` e costruisci in memoria la lista di capability con i
campi rilevanti per il matching e per l'output.

Per ogni riga di tabella del documento (righe che iniziano con `|` e contengono
un nome capability), estrai:

| Campo interno | Sorgente in CAPABILITIES.md |
|---|---|
| `nome` | Prima colonna — testo capability |
| `comando` | Seconda colonna — testo dopo `/` o nome agente |
| `sempre_attiva` | Terza colonna — valore testuale |
| `quando_usarla` | Quarta colonna — testo descrittivo |
| `approfondimento` | Quinta colonna — link wiki o `—` |
| `area` | Heading `##` padre della riga |

**Parsing note**:
- Le righe separatore (`|---|---|...`) vanno ignorate.
- Le righe heading (`##`) marcano l'area tematica: ogni capability eredita l'area
  dell'heading `##` che la precede nel documento.
- Il campo `sempre_attiva` puo' contenere `si`, `no`, un valore `opt-in: <flag>`,
  o un valore `topologia`. Interpretalo letteralmente per il campo output.
- Mantieni il testo grezzo di `approfondimento` (link markdown) per riproporlo
  nell'output senza trasformazioni.

Risultato: lista `capabilities[]` in memoria, una entry per riga di capability.

---

## Fase 3 — Match

Applica matching lessicale tra la query dell'utente e i campi di ogni capability.
Nessuna chiamata API, nessun embedding: solo confronto di termini.

### Algoritmo

1. **Normalizza la query**: converti in minuscolo, rimuovi punteggiatura,
   espandi abbreviazioni note (es. "ui" → "ux ui", "fe" → "frontend", "be" →
   "backend").

2. **Per ogni capability**, calcola lo **score** come somma pesata di corrispondenze
   di termini (case-insensitive, partial match ammesso su radici ≥ 4 caratteri):
   - Campo `quando_usarla`: peso 3 per ogni termine condiviso con la query
   - Campo `nome`: peso 2 per ogni termine condiviso
   - Campo `area` (heading): peso 1 per ogni termine condiviso
   - Campo `comando`: peso 1 per ogni termine condiviso

3. **Filtra**: mantieni solo le capability con `score >= 1`.

4. **Ordina** per score decrescente.

5. **Casi speciali**:
   - Se la query menziona esplicitamente un comando (es. "uso /analytics?") →
     aggiungi weight 5 alla capability con quel comando.
   - Se la query menziona un flag config (es. "code_quality") → aggiungi weight 4
     alla capability con quel flag in `sempre_attiva`.

6. **Risultati**:
   - `len(matches) == 0` → vai alla Fase 4 — Nessun match.
   - `len(matches) == 1` → vai alla Fase 4 — Match singolo.
   - `len(matches) >= 2` → vai alla Fase 4 — Ambiguita'.

---

## Fase 4 — Output

Formatta la risposta in base all'esito della Fase 3.

### Output strutturato (match singolo o match principale)

Per ogni capability restituita (max 3 risultati in caso di ambiguita'):

```
Capability: <nome>
Comando: /<comando> (o: <nome-agente> se non c'e' un comando slash)
Attiva per default: si' / no
Se opt-in, attiva con: <flag: true in factory.config.yaml>
Approfondimento: <link wiki/runbook oppure — se non disponibile>
```

Regole di compilazione campi:
- **Attiva per default**: `si'` se il campo `sempre_attiva` e' `si` o `topologia`;
  `no` se contiene `opt-in:`.
- **Se opt-in, attiva con**: riporta il valore del campo `opt-in:` dalla terza
  colonna di `CAPABILITIES.md`. Se la capability e' sempre attiva, ometti questa
  riga.
- **Approfondimento**: riporta i link markdown della quinta colonna. Se il valore
  e' `—`, scrivi `—` (nessun link disponibile).

### Caso — Nessun match

```
Non ho trovato una capability per questo scenario.

Le aree disponibili in CAPABILITIES.md sono:
1. <area 1 — testo heading ## senza "Quando">
2. <area 2>
...
10. <area 10>

Suggerimento: riformula la domanda usando termini come il nome dell'attivita'
(es. "analisi costi", "review codice", "deploy", "accessibilita'") oppure
consulta CAPABILITIES.md direttamente per una panoramica completa.
```

Estrai la lista delle aree dagli heading `##` di `CAPABILITIES.md` (escludi
l'heading "Come leggere questo documento" e "Nota: capability sempre attive").

### Caso — Ambiguita' (2+ match con score simile)

Due match sono "simili" se il loro score differisce di meno del 20% rispetto al
massimo (`score_N / score_max >= 0.8`).

```
Ho trovato piu' capability che potrebbero corrispondere alla tua domanda:

1. <nome capability 1>
   Comando: /<comando1>
   Quando usarla: <campo quando_usarla>

2. <nome capability 2>
   Comando: /<comando2>
   Quando usarla: <campo quando_usarla>

(eventuale 3a opzione se score simile)

Quale di queste corrisponde al tuo scenario? Rispondi con il numero o riformula
la domanda con piu' dettagli.
```

Dopo la scelta dell'utente, ripeti l'output strutturato completo per la capability
scelta (come nel caso — Match singolo).

---

## Invarianti

1. **No invenzione capability**: la skill non puo' produrre il nome di una capability
   che non appare come riga di tabella in `CAPABILITIES.md`. Se non c'e' corrispondenza,
   risponde con il caso "Nessun match".

2. **Source-of-truth = CAPABILITIES.md**: il routing si basa esclusivamente sul
   contenuto del file letto nella Fase 2. Non si basa su conoscenza pregressa
   dell'agente, su `CLAUDE.md`, su `factory.config.yaml`, o su altre fonti.

3. **Mai modificare file**: questa skill e' read-only. Non scrive, non aggiorna, non
   crea file. L'unico effetto e' il testo di risposta prodotto in chat.

4. **Nessuna API aggiuntiva**: il matching e' lessicale (Fase 3). Non si invocano
   embedding, LLM secondari, o tool esterni.

5. **Trasparenza dell'opt-in**: se una capability e' opt-in, la skill lo dichiara
   sempre nell'output (campo "Attiva per default: no" + "Se opt-in, attiva con:").
   Non omette mai i prerequisiti di configurazione.

---

## Esempi

### Esempio 1 — Match singolo preciso

**Query**: `/help voglio verificare l'accessibilita' del mio frontend`

**Fase 3**: termini "accessibilita'" e "frontend" → match forte su capability
"Accessibilita' WCAG 2.2 AA" (campo `quando_usarla` contiene "scan accessibilita'
end-to-end") + "Visual Oracle FE" (piu' basso). Match principale:
"Accessibilita' WCAG 2.2 AA".

**Output**:
```
Capability: Accessibilita' WCAG 2.2 AA
Comando: /a11y
Attiva per default: no
Se opt-in, attiva con: a11y.enabled: true in factory.config.yaml
Approfondimento: wiki/concepts/accessibility-testing-capability.md · wiki/runbooks/accessibility-testing-runbook.md
```

---

### Esempio 2 — Nessun match

**Query**: `/help come faccio il deploy in produzione?`

**Fase 3**: termini "deploy", "produzione" → nessuna capability in `CAPABILITIES.md`
copre il deploy in produzione (fuori scope della factory).

**Output**:
```
Non ho trovato una capability per questo scenario.

Le aree disponibili in CAPABILITIES.md sono:
1. Ingestare nuovi dati nella knowledge base
2. Interrogare la knowledge base o controllare lo stato
3. Pianificare o gestire il prodotto
4. Sviluppare codice o documentazione con agenti
5. Verificare la qualita' del codice
6. Analizzare il rischio prima di iniziare
7. Lavorare su design, UX o accessibilita'
8. Analizzare costi e tempi
9. Gestire la governance del framework
10. Pubblicare il kanban, usare piu' adapter o creare una nuova factory

Suggerimento: riformula la domanda usando termini come il nome dell'attivita'
(es. "analisi costi", "review codice", "deploy", "accessibilita'") oppure
consulta CAPABILITIES.md direttamente per una panoramica completa.
```

---

### Esempio 3 — Ambiguita'

**Query**: `/help come analizzo i costi?`

**Fase 3**: termini "analizzo", "costi" → match su:
- "Misurazione costi/tempi reali" (score alto: `quando_usarla` contiene "costi e
  tempi effettivi")
- "Stima costi/tempi futuri" (score simile: `quando_usarla` contiene "stime ...
  contingency")

**Output**:
```
Ho trovato piu' capability che potrebbero corrispondere alla tua domanda:

1. Misurazione costi/tempi reali
   Comando: /analytics
   Quando usarla: Vuoi misurare costi e tempi effettivi per TSK, sprint, periodo. Faccia retrospettiva

2. Stima costi/tempi futuri
   Comando: /estimate
   Quando usarla: Vuoi produrre stime difendibili: intervallo + confidenza + contingency. Faccia previsionale

Quale di queste corrisponde al tuo scenario? Rispondi con il numero o riformula
la domanda con piu' dettagli.
```

Se l'utente risponde `1`:
```
Capability: Misurazione costi/tempi reali
Comando: /analytics
Attiva per default: no
Se opt-in, attiva con: analytics.measurement.enabled: true in factory.config.yaml
Approfondimento: wiki/concepts/task-analytics-cost-estimation-capability.md · wiki/runbooks/analytics-dogfooding-runbook.md · wiki/runbooks/analytics-pricing-runbook.md
```

---

## Cross-reference

- Invocata da: `/help`
- Fonte di verita': `CAPABILITIES.md` (root del repo)
- US: US-113 (EP-032)
- Pattern: `CAPABILITIES.md` come capability registry leggibile a runtime
