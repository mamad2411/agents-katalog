---
name: li-piano
description: >-
  Costruisce la settimana su LinkedIn: cosa pubblicare, quando, e con chi
  interagire, tenendo conto del calendario italiano (agosto, ponti, festività)
  e del fuso orario del pubblico. Usala quando l'utente dice "pianifica la mia
  settimana", "cosa pubblico", "piano editoriale", "non so cosa scrivere", o
  vuole un calendario di pubblicazione e una lista di persone da seguire.
---

# li-piano

La sala di controllo. Tutto il resto del pacchetto esegue; questa decide cosa
eseguire. Va lanciata una volta a settimana, sempre lo stesso giorno.

## Cosa serve

Se `~/.claude/linkedin/voce.md` e `log.md` esistono, leggili: il piano non deve
ripetere un tema delle ultime due settimane. Se non esistono, chiedi quattro
cose e scrivile:

1. Cosa vende o offre l'utente, e a chi (o, se cerca lavoro, che ruolo cerca
   e dove).
2. I tre o quattro temi per cui vuole essere riconosciuto.
3. Cosa è successo davvero questa settimana: una call con un cliente, un
   numero, un errore, una cosa costruita, una discussione. I post nascono da qui.
4. Da dieci a venti persone o aziende da cui vuole farsi vedere.

## Cosa pubblicare

Quattro post a settimana battono sette. La costanza è un pavimento, non un
obiettivo, e il quinto post della settimana è quasi sempre quello debole che
abbassa la media. Se l'utente parte da zero o ha poco tempo, due post a
settimana fatti bene sono un ottimo inizio.

Mescola i tipi, mai due uguali di fila:

| tipo | quanti | a cosa serve |
| --- | --- | --- |
| **Prova** | 1 a settimana | una cosa successa, con un numero |
| **Opinione** | 1 a settimana | una posizione che potrebbe farti perdere qualche follower |
| **Insegna** | 1 a settimana | una cosa che il lettore può fare oggi |
| **Storia** | 1 ogni due settimane | una scena con un dialogo e un costo |
| **Offerta** | 1 ogni due settimane | cosa offri, detto chiaro, senza scuse |

Per ogni slot: il tema, l'angolo preciso preso da quello che è successo
davvero questa settimana, e il numero della formula di apertura da
`li-post/hooks.json`. Non un argomento, un angolo. "IA" non è un piano. "Il
preventivo che abbiamo perso perché la bozza fatta con l'IA aveva una lineetta
lunga" è un post.

## Quando pubblicare

Pubblica quando il pubblico dell'utente è alla scrivania. Per un pubblico
professionale italiano, il punto di partenza ragionevole è **da martedì a
giovedì, tra le 8:00 e le 9:30**, con la pausa pranzo (13:00-14:00) e il lunedì
dopo le 10 come seconda scelta. Il fine settimana è per le storie personali,
o per niente.

**Il calendario italiano conta più dell'ora:**

- **Agosto**, e soprattutto le due settimane intorno a Ferragosto: il pubblico
  professionale è in ferie. Riduci i post o pubblica solo storie. Non lanciare
  niente di importante.
- **Ponti**: 25 aprile, 1° maggio, 2 giugno, 1° novembre, 8 dicembre. Se cadono
  a metà settimana, la settimana è corta: tre post al massimo.
- **Dal 20 dicembre al 6 gennaio**: attività bassa. Bilanci e riflessioni
  funzionano, le offerte no.
- **Settembre e gennaio** sono i mesi della ripartenza: buon momento per post
  di posizionamento e offerte.

E dillo chiaramente: **il giorno e l'ora contano molto meno della prima riga.**
Se l'utente sta ottimizzando gli orari prima che le sue aperture funzionino,
sta lucidando la cosa sbagliata, e glielo devi dire.

**Fuso orario:** ancora gli orari al pubblico, non all'utente. Un italiano che
vive a Melbourne e scrive per un pubblico italiano pubblica alle 8:00 ora di
Roma, cioè la sera in Australia. Se ha due pubblici (Italia ed estero), usa
`/li-bilingue` e pianifica due fasce.

## Con chi interagire

Una lista di 10, divisa in tre:

- **5 per la portata**: persone con il pubblico che l'utente vuole, ai cui post
  può aggiungere qualcosa di vero. Commenta prima che abbiano 20 commenti, o
  non ti vede nessuno.
- **3 pari**: stesso livello, stesso campo. È il gruppo che ricambia.
- **2 decisori**: persone che potrebbero davvero comprare o assumere. Commenta
  i loro post per settimane prima di qualsiasi messaggio, e non fare mai
  proposte commerciali in un commento.

Venti minuti al giorno, prima di pubblicare, non dopo. Sono i commenti sui post
degli altri che fanno funzionare il tuo.

## Output

```
SETTIMANA DEL 8 SETTEMBRE

LUN  solo interazioni  (20 min, lista sotto)
MAR  8:15  PROVA      #17 L'ancora di tempo  - preventivi da 5 ore a 20 minuti
MER  solo interazioni
GIO  8:00  OPINIONE   #1  Controcorrente     - perché abbiamo tolto la call conoscitiva
VEN  8:30  INSEGNA    #21 Il regalo          - l'email di 4 righe per riaprire un cliente
SAB  -
DOM  -

INTERAZIONI  (5 portata / 3 pari / 2 decisori)
  ...

Di' "scrivi martedì" e preparo la bozza.
```

Scrivi il piano in `~/.claude/linkedin/piano.md`, così le altre skill possono
leggerlo. Non viene programmato né pubblicato niente: è un piano, e lo esegue
l'utente.
