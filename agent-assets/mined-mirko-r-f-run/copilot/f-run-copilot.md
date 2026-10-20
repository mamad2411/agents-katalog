# F-Run Rust CLI: istruzioni vincolanti per Copilot

Queste istruzioni valgono per tutto il lavoro futuro sul core Rust in `src/` e devono prevalere su suggerimenti generici.


## Ambito del progetto

- Questo repository è un **binary crate CLI**, non una libreria: l'entrypoint è in `src/main.rs` e il flusso applicativo è top-down.
- Il codice è organizzato in cinque aree root stabili:
	- `src/config`: modello e persistenza di `frun.yaml`, inizializzazione globale, feature detection.
	- `src/core`: servizi condivisi, runner comandi, parser `pubspec`, updater, codici di uscita, utility e menu.
	- `src/features`: workflow operativi Flutter/Android/iOS, build, fastlane, shorebird, generatori, localization e automazioni di progetto.
	- `src/network`: accesso HTTP centralizzato e client condiviso per download, manifest remoti e traduzioni.
	- `src/ui`: stampa terminale, TUI e orchestration dei menu.
- Quando aggiungi una nuova responsabilità, collocala nel modulo coerente con questa struttura e registra sempre il file nel relativo `mod.rs`.
- Evita di introdurre nuovi strati architetturali astratti o pattern enterprise: il progetto privilegia orchestrazione esplicita e funzioni piccole orientate ai workflow CLI.

## Gerarchia modulare e organizzazione dei file

- Rispetta la gerarchia modulare già esistente in `src/`: il progetto separa chiaramente moduli root (`config`, `core`, `features`, `network`, `ui`) e sottomoduli verticali come `core/menu`, `core/utils`, `features/build` e `features/localization`.
- Ogni nuova funzionalità deve nascere nel modulo di competenza. Se lo scope è nuovo e non appartiene in modo chiaro a un modulo esistente, crea un nuovo modulo dedicato invece di forzarlo in un file generico.
- Non accorpare logiche eterogenee nello stesso file. Se un modulo cresce oltre una singola responsabilità, rifattorizzalo in directory con `mod.rs` e file separati, seguendo il pattern già presente in `src/core/menu`, `src/core/utils`, `src/features/build` e `src/features/localization`.
- Mantieni la granularità attuale: un file per orchestrazione, un file per responsabilità operativa specifica, un file per tipi o helper specializzati quando servono. Evita file-monolite che mescolano menu, shell runner, parsing, build e UI.
- Non creare moduli “misc”, “helpers” o “common” come contenitori indistinti. Se una responsabilità non è chiaramente localizzabile, prima chiarisci lo scope e poi scegli il modulo corretto.
- Quando trasformi un file in una directory modulare, preserva nomi e responsabilità espliciti. Esempio di pattern corretto già presente: `features/build/builder.rs` come orchestratore, con implementazioni di piattaforma in `features/build/android.rs` e `features/build/ios.rs`.
- Mantieni separata la logica di UI dalla logica operativa: menu, rendering e stampa restano sotto `ui` o `core/menu`; workflow Flutter, localization e deploy restano sotto `features`; servizi condivisi restano sotto `core`; accesso HTTP e download restano sotto `network`; stato/configurazione restano sotto `config`.

## Visibilità e separazione logica

- Usa la visibilità minima necessaria. Non esportare simboli con `pub` per default solo per comodità.
- Mantieni privati helper e dettagli interni che non servono fuori dal modulo.
- Limita i `pub mod` ai moduli che devono davvero partecipare alla struttura pubblica del crate binario. Se introduci sotto-componenti interni a un modulo, valuta se tenerli non pubblici.
- Mantieni separati i tipi di dati e la logica di esecuzione quando la complessità lo richiede: `struct` ed `enum` devono restare leggibili e stabili, mentre la logica operativa deve vivere in `impl`, funzioni dedicate o moduli separati.
- Evita file che mischiano indiscriminatamente definizione dei dati, IO, orchestrazione di processi esterni e rendering UI. Se una `struct` o un `enum` acquisisce troppe responsabilità operative, estrai la logica in un modulo vicino ma separato.
- Quando aggiungi API nuove, progetta prima il confine del modulo: chi espone cosa, chi consuma cosa, e cosa deve restare dettaglio interno. L'incapsulamento attuale del progetto va preservato anche se il crate è binario e non libreria.

## Pattern concreti da seguire

- Usa `src/features/build` come riferimento per una feature verticale ben separata: `builder.rs` orchestra il flusso, mentre `android.rs` e `ios.rs` contengono implementazioni di piattaforma specializzate.
- Usa `src/features/localization` come riferimento per moduli orientati a un dominio specifico: `localize.rs` orchestra il flusso, mentre `easy_localization.rs` e `katana.rs` contengono implementazioni specializzate per i diversi sistemi di localizzazione.
- Usa `src/core/menu` come riferimento per la suddivisione della CLI interattiva: `menus.rs` contiene le primitive di selezione, `main_menu.rs` e `generators_menu.rs` gestiscono flussi diversi, `menu_theme.rs` isola il tema grafico.
- Usa `src/core/utils` come riferimento per utility verticali condivise ma non UI: `filesystem.rs`, `dependency_checks.rs`, `command_availability.rs` e `android_artifacts.rs` restano vicine al dominio operativo senza gonfiare `core/mod.rs`.
- Usa `src/config` come riferimento per separare modello e logica: `frunconfig.rs` definisce i tipi e lo stato globale, `configurer.rs` contiene inizializzazione, load, save e reload, `features.rs` isola le feature configurabili.
- Usa `src/network` come riferimento per l'accesso HTTP: `client.rs` centralizza download, parsing JSON remoto e traduzioni, evitando client duplicati nei moduli chiamanti.
- Usa `src/ui` come riferimento per la separazione del rendering: `printer.rs` gestisce output testuale e notifiche, `tui.rs` la UI strutturata, `menu_runner.rs` l'orchestrazione del loop utente, `colors.rs` le costanti visive.

## Anti-pattern da evitare

- Non aggiungere nuove build Flutter direttamente in `src/features/mod.rs` o `src/main.rs`: devono restare sotto `src/features/build` o in un nuovo sottomodulo verticale equivalente.
- Non inserire parsing YAML, accesso a `frun.yaml` o feature detection dentro `src/ui` o `src/features`: queste responsabilità restano nel layer `src/config`.
- Non mettere codice di stampa terminale, notifiche o scelta menu dentro i moduli di build, fastlane, shorebird o localization oltre al minimo necessario per orchestrare il workflow.
- Non usare file generici per accorpare utility non correlate. Se una nuova utility serve solo alla build Android, deve stare vicino a `src/features/build/android.rs`, non in un contenitore trasversale ambiguo.
- Non creare client HTTP, download helper o parsing di risposte remote dentro `core`, `features` o `ui`: queste responsabilità restano nel layer `src/network`.
- Non pubblicare automaticamente ogni nuovo modulo o helper con `pub mod` o `pub fn`: esporta solo ciò che serve davvero ai moduli chiamanti già esistenti.

## Convenzioni Rust obbligatorie

- Mantieni `edition = "2024"` e non introdurre compatibilità legacy se non richiesta esplicitamente.
- Rispetta il contratto implicito già imposto dal crate root:
	- `#![warn(clippy::all, clippy::pedantic, clippy::nursery)]`
	- `#![deny(clippy::unwrap_used)]`
- Non usare `unwrap()`. Se un errore è recuperabile o runtime-facing, usa `unwrap_or_else(...)` con `ui::printer::error_and_exit(...)` oppure restituisci `Result` solo nei punti del codice che già seguono quel modello.
- `expect(...)` è ammesso solo per invarianti locali davvero stabili, come nel codice esistente. Non usarlo per input utente, filesystem, rete o processi esterni.
- Mantieni nomi di tipi, funzioni, enum e moduli in inglese tecnico. Mantieni i messaggi utente, warning, errori e menu in italiano, coerenti con il resto della CLI.
- Preferisci firme esplicite e side effect evidenti. Non introdurre macro, trait o genericità extra se una funzione concreta è sufficiente.

## Gestione errori obbligatoria

- In questo progetto la strategia standard **non** è `anyhow`/`thiserror`/error tree tipizzato.
- Non introdurre `anyhow`, `thiserror`, `eyre` o tipi di errore custom senza richiesta esplicita.
- Per errori fatali usa sempre `ui::printer::error_and_exit(...)` con un codice preso da `core::exit_codes`.
- Non stampare errori fatali con `eprintln!` sparsi nel codice: centralizza il comportamento nella UI condivisa.
- Per comandi esterni usa `core::runner::run_command(...)` o helper collegati. Nei workflow procedurali che non ritornano `Result`, continua a usare il pattern bool/short-circuit già presente.
- Se una nuova funzione appartiene a un modulo che oggi usa `Result` in modo locale, mantieni quello stile locale invece di forzare una propagazione globale fino a `main`.

## Crate e dipendenze: uso previsto

- `serde` e `serde_yaml_ng` sono lo standard per configurazione e parsing YAML. Nuovi file di configurazione o campi persistenti devono integrarsi in questo stack, non introdurre parser alternativi.
- `std::sync::OnceLock` è il meccanismo standard per stato globale lazy condiviso. Se serve nuovo stato globale, riusa questo pattern invece di creare singleton ad hoc.
- `crossterm` è la base dei menu interattivi testuali e della gestione input terminale; mantieni i pattern già presenti in `src/core/menu`.
- `ureq` è lo standard per l'accesso HTTP sincrono del progetto e deve restare centralizzato in `src/network/client.rs`.
- `regex-lite`, `glob`, `zip`, `indicatif`, `figlet-rs`, `time` e `serde_json` sono già parte del design corrente: se devi estendere funzionalità correlate, preferisci questi crate prima di aggiungerne di nuovi.

## Regole per configurazione e stato

- Qualsiasi nuova opzione persistente deve essere modellata nei tipi di configurazione esistenti in `src/config/frunconfig.rs` e correlati, serializzata con `serde` e salvata in `frun.yaml`.
- Non creare file di configurazione paralleli se l'informazione appartiene chiaramente a `frun.yaml`.
- Quando aggiungi feature detection automatica, implementala nel layer `config` e non direttamente nei menu o nei workflow UI.

## Regole per workflow Flutter

- Questo tool è una CLI Rust che orchestra tool Flutter, Fastlane, Shorebird, ADB e strumenti di sistema. Le nuove feature devono preservare questo ruolo di orchestratore, non replicare internamente il comportamento degli strumenti esterni.
- Se aggiungi logica di build o deploy Flutter, rispetta le convenzioni già codificate nei path:
	- `environment/{env}.json`
	- `environment/{flavor}/{env}.json`
	- `lib/main.dart`
	- `lib/flavors/main_{flavor}.dart`
- Le build Android/iOS e i workflow multi-flavor devono integrarsi nei moduli sotto `src/features`, non essere cablati in `main.rs`.

## Target e build: regole vincolanti

- Da `Cargo.toml` non emerge un target triple esplicito, quindi non hardcodare nuovi target di compilazione nel codice Rust senza richiesta esplicita.
- Dal codice sorgente il tool è chiaramente **host-oriented per macOS**: usa `osascript`, Terminal.app, Homebrew, `xcrun` e workflow iOS locali. Quando modifichi il core, preserva prima di tutto il comportamento macOS esistente.
- Se proponi portabilità multipiattaforma, trattala come estensione separata e non rompere il percorso macOS attuale.
- Quando ti viene chiesto come compilare o verificare il progetto, considera come profilo release preferito quello definito in `Cargo.toml`:
	- `opt-level = "z"`
	- `lto = "fat"`
	- `codegen-units = 1`
	- `strip = true`
	- `panic = "abort"`
	- `debug = false`
	- `incremental = false`
- Non suggerire modifiche a questi flag per default. Cambiali solo se il task richiede esplicitamente un tradeoff diverso tra dimensione, debug o tempi di build.
- Per verifiche locali del core Rust, preferisci nell'ordine:
	- `cargo build`
	- `cargo clippy`
	- `cargo build --release`
	Questo repository non espone una suite test evidente come flusso principale; non inventare test harness inesistenti.

## Standard di documentazione rustdoc

- Usa `//!` all'inizio dei moduli non banali per descrivere responsabilità, contesto operativo e collegamenti con altri moduli.
- Usa `///` su tutte le funzioni pubbliche, struct, enum e metodi pubblici che partecipano ai workflow CLI, alla configurazione o alla UI.
- La lingua della documentazione deve seguire il progetto: testo descrittivo in italiano, simboli e nomi API in inglese tecnico.
- Per funzioni pubbliche, mantieni la struttura già usata nel repository quando applicabile:
	- breve frase iniziale
	- se utile, una riga aggiuntiva sul comportamento
	- sezione `# Parametri`
	- sezione `# Return` quando esiste un valore di ritorno significativo
	- sezione `# Panics` solo se il codice può davvero fare panic Rust oppure termina intenzionalmente il processo
- Non scrivere doc-comment generici o tautologici. Le doc devono spiegare precondizioni, side effect, path attesi, uso di flavor/environment e dipendenze esterne.
- Mantieni le doc allineate alla firma reale e al comportamento reale: non documentare `Result` se la funzione ritorna `Self`, non scrivere `# Panics` se in realtà il codice usa `error_and_exit`, e non lasciare sezioni stale dopo un refactor.
- Quando aggiungi un nuovo modulo pubblico o una funzione usata dai menu/workflow principali, scrivi la rustdoc nello stesso commit della modifica, così `cargo doc` resta utile anche per un binary crate interno.

## Regola obbligatoria sugli use

- Gli `use crate::...` devono essere **sempre file-scoped** e dichiarati all'inizio del file, mai inline o dentro funzioni/blocchi. Qualsiasi nuovo modulo, funzione o refactor deve rispettare questa convenzione.

## Cosa evitare

- Non trasformare il progetto in una libreria pubblica salvo richiesta esplicita.
- Non spostare logica di workflow in `main.rs`.
- Non introdurre dependency injection, trait object o layering aggiuntivo senza un bisogno reale visibile nel codice.
- È consentito usare `#[tokio::main]` e un `main` async quando semplifica integrazioni async richieste dal workflow.
- Non duplicare logica di path Flutter, flavor o ambiente già presente nei moduli `features/build`, `features/flavors` e `core/pubspec`.
- Non duplicare logica HTTP o parsing di risposte remote già presente in `network/client.rs`.
- Non aggiungere messaggi utente in inglese in nuove feature, salvo output tecnico imposto da tool esterni.
