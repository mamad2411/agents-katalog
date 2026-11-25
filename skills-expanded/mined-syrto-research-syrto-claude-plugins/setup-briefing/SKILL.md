---
name: setup-briefing
description: >-
  Comando esplicito: configura, sposta o ferma l'automazione ricorrente del briefing
  giornaliero. Usala solo quando l'utente chiede di programmare il briefing ("configura il
  briefing giornaliero", "schedula il briefing", "sposta l'orario del briefing", "set up my
  daily briefing"). Non per preparare un briefing adesso (usa briefing).
---

# Setup Daily Briefing

Configura la routine automatica che ogni sera prepara il briefing per i meeting del prossimo
giorno lavorativo, tramite uno scheduled task.

## Cosa fare

1. **Verifica prerequisiti**: connettore **Syrto**, connettore **calendario** (quello connesso, es. Outlook o Google Calendar) e la
   ricerca web devono essere disponibili. Se manca qualcosa, spiega all'utente cosa connettere.
   Serve anche una capacità di automazione nel client (in Codex, le automazioni): se il client
   non la offre, dillo e suggerisci di chiedere "briefing di oggi" a mano.

2. **Chiedi l'orario** (se non indicato nella richiesta):
   - Default suggerito: **21:00** (la sera prima, per preparare il giorno dopo).
   - L'utente può scegliere qualsiasi orario.
   - Se sceglie un orario mattutino (es. 07:00), avvisa che il briefing sarà per i meeting di
     oggi stesso, non del giorno dopo.

3. **Riepiloga e chiedi conferma prima di creare**: orario, giorni attivi (lun-ven) e cosa verrà
   generato. Ricorda che ogni esecuzione legge i dati Syrto come una richiesta manuale, quindi
   conta nell'utilizzo del piano anche nei giorni in cui il briefing non viene aperto. Crea
   l'automazione solo dopo un sì.

4. **Crea o aggiorna un'automazione ricorrente** usando la capacità di automazione
   disponibile. Imposta l'orario nella timezone locale dell'utente e limita l'esecuzione ai
   giorni lavorativi, senza mostrare o chiedere all'utente una regola cron grezza.
   - **prompt salvato**: un'esecuzione automatica non ricorda questa conversazione, quindi il
     prompt deve bastare a se stesso. La data target si decide qui, in base all'orario, così
     l'esecuzione non deve calcolarla:
     - orario dalle 18:00 in poi:
       ```
       Esegui la skill briefing in modalità calendario per i meeting del prossimo giorno
       lavorativo (dopo il venerdì viene il lunedì). È un'esecuzione automatica: non fare
       domande e non proporre scelte, usa i default della skill e annota le ipotesi nel
       riepilogo. Leggi il contesto salvato dell'utente (profilo e contesto commerciale),
       se presente. Salva l'HTML e riassumi in chat meeting, verdetti e aziende non trovate
       su Syrto.
       ```
     - orario prima delle 18:00: lo stesso prompt, con "per i meeting di oggi" al posto di "per
       i meeting del prossimo giorno lavorativo (dopo il venerdì viene il lunedì)".
   - **name**: "Daily Briefing".
   - Mantieni l'automazione silenziosa quando non ci sono meeting o azioni utili; notifica solo
     quando il briefing è pronto, l'esecuzione fallisce o serve un intervento dell'utente.

5. **Conferma** all'utente: orario configurato, giorni attivi (lun-ven), cosa verrà generato
   (briefing con profilo aziende + persone + fit read + talking points), come cambiarlo
   (chiedendo, per esempio, "sposta il briefing alle 7:30") e come lanciarlo a mano
   (chiedendo "briefing di oggi").

## Se l'automazione esiste già

Controlla prima le automazioni esistenti. Se esiste già "Daily Briefing", aggiornala invece di
crearne una seconda, e riscrivi il prompt salvato con la variante che corrisponde all'orario.
Se l'utente non ha chiesto un nuovo orario, preserva quello esistente. Se chiede di fermarla,
sospendila o eliminala.
