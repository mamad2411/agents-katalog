# AGENTS.md

## Scopo

Questo file definisce le istruzioni permanenti di progetto da seguire quando si lavora su pagine web da creare o replicare in **WordPress con Elementor**.

Chiunque lavori su questo progetto deve considerare queste regole come il riferimento principale per:

- analisi della pagina
- documentazione delle sezioni
- replica del layout
- costruzione in Elementor
- responsive design
- modificabilita` dei contenuti

## Obiettivo principale

Quando viene richiesto di creare o replicare una pagina web in WordPress con Elementor, le istruzioni fornite devono essere:

- complete
- precise
- operative
- prive di ambiguita`
- pensate per Elementor
- adatte a desktop, tablet e mobile
- orientate a contenuti modificabili direttamente nel builder

## Regola fondamentale

Non dare mai istruzioni generiche o incomplete.

Per ogni sezione della pagina devono essere sempre indicati **tutti i parametri necessari** alla costruzione reale in Elementor.

Questo include sempre:

- container principali
- sotto-container
- widget
- classi CSS
- font
- misure
- spaziature
- margini
- padding
- allineamenti
- colori
- background
- overlay
- bordi
- pulsanti
- form
- comportamento responsive

## Vincoli obbligatori

Ogni pagina o sezione progettata deve rispettare sempre questi vincoli:

1. Deve essere costruibile in Elementor con elementi modificabili.
2. Deve essere responsive su desktop, tablet e mobile.
3. Deve evitare, salvo eccezioni motivate, l'uso di un unico widget HTML che blocca l'editing.
4. Deve preferire:
   - container Elementor
   - widget nativi Elementor
   - form reali Elementor o shortcode configurabili
5. Deve usare CSS personalizzato per lo stile, non per sostituire la struttura editabile.

## Livello minimo di dettaglio richiesto

Per ogni sezione devono sempre essere descritti:

- obiettivo della sezione
- struttura completa dei container
- direzione dei container
- larghezze
- min-height
- gap
- padding desktop
- padding tablet
- padding mobile
- margin desktop
- margin tablet
- margin mobile
- background e immagini
- overlay
- border
- radius
- z-index
- position
- widget esatti da inserire
- ordine dei widget
- contenuti testuali
- font family
- font size per breakpoint
- font weight
- line-height
- letter-spacing
- colori
- link
- anchor
- comportamento responsive

## Responsive obbligatorio

Ogni soluzione deve essere pensata per:

- desktop
- tablet
- mobile

Le istruzioni devono sempre specificare:

- numero colonne per breakpoint
- cambi direzione row/column
- riduzione font
- variazione padding e margini
- adattamento dei pulsanti
- adattamento del form
- eventuale stacking dei blocchi

Nessuna sezione deve essere descritta solo in versione desktop.

## Form modificabili

Se la pagina include un form:

- deve essere configurabile in Elementor oppure tramite shortcode
- devono essere descritti i campi in ordine
- devono essere indicati label, placeholder, required, larghezze e layout responsive
- devono essere indicate le azioni post invio se rilevanti

## Formato richiesto delle istruzioni

Ogni volta che viene descritta una pagina o una sezione, usare una struttura chiara del tipo:

### Nome sezione

- obiettivo
- container principale
- sotto-container
- widget
- stile tipografico
- spacing
- responsive desktop/tablet/mobile
- note operative

## Riferimento esteso

Per il dettaglio completo dello standard operativo, consultare anche:

- `ELEMENTOR_PAGE_REPLICATION_INSTRUCTIONS.md`

Questo file contiene la versione estesa e strutturata delle regole da seguire.

## Comportamento atteso

Quando viene aperto questo progetto e viene chiesto supporto su una pagina WordPress/Elementor:

1. leggere queste istruzioni come standard del progetto
2. assumere che l'utente voglia istruzioni complete e non generiche
3. fornire dettagli pratici e parametri esatti
4. mantenere sempre il vincolo di modificabilita` in Elementor
5. mantenere sempre il vincolo responsive su desktop, tablet e mobile

## Nota finale

Se queste istruzioni entrano in conflitto con una richiesta esplicita dell'utente, va chiarito il tradeoff, ma per default il comportamento corretto e`:

- privilegiare Elementor modificabile
- privilegiare responsive design
- privilegiare istruzioni sezione per sezione
- non lasciare parametri impliciti
