---
name: li-carosello
description: >-
  Costruisce un post documento (carosello) per LinkedIn: testo slide per slide,
  la copertina che fa scorrere, e il PDF da caricare. Usala quando l'utente dice
  "carosello", "post documento", "slide per LinkedIn", "trasformalo in un
  carosello", o ha un'idea a elenco che come post di solo testo morirebbe.
---

# li-carosello

I post documento sono il formato in cui si resta più a lungo su LinkedIn,
perché ogni slide sfogliata conta. Il formato premia un'idea divisa in
passaggi. Punisce un post di testo tagliato a pezzi.

## Quando usarlo al posto di un post di testo

Usa un carosello quando l'idea ha una **sequenza**: passaggi, un conto alla
rovescia, un prima e dopo progressivo, un metodo con delle parti. Usa un post
di testo quando l'idea è un'affermazione sola. Spezzare un'affermazione su
otto slide è il modo più comune in cui i caroselli falliscono: se è quello che
ha l'utente, diglielo e passalo a `/li-post`.

## Struttura

8-12 slide. Sotto le 8 è un post di testo. Sopra le 12, in pochi arrivano in
fondo.

```
1        COPERTINA  l'apertura, 6 parole al massimo, più una riga di promessa
2        LA POSTA   perché conta, in una frase
3-N      UN'IDEA PER SLIDE. Un titolo di 3-7 parole e al massimo 25 parole
                    sotto. Se una slide ha bisogno di un paragrafo, sono due slide.
N+1      RIEPILOGO  tutto come elenco, così lo screenshot è utile da solo
ULTIMA   AZIONE     una sola. Segui, commenta una parola, o il link. Una.
```

## Regole per il testo

- **La slide 1 è l'80% del risultato.** Sei parole, grandi. Il resto non salva
  una copertina che nessuno sfoglia. In italiano sei parole sono più lunghe:
  controlla che stiano su due righe al massimo.
- **Numera ogni slide** (3/10). Se si vede la fine, si arriva in fondo più spesso.
- **Nessuna slide è un paragrafo.** Se non sta in 25 parole, dividila.
- **Il riepilogo è la slide che si salva.** Deve reggersi da sola.
- **Il nome utente in ogni slide**, piccolo, in basso. Gli screenshot girano
  senza di te.

## Il PDF

LinkedIn vuole un PDF, 1080x1350 (4:5) per occupare più spazio nel feed, sotto
i 100 MB e le 300 pagine. Fallo in HTML e stampalo in PDF:

```bash
# una pagina per slide, 1080x1350, senza margini
# poi: Chrome headless --print-to-pdf, o qualsiasi convertitore HTML-PDF
```

Scrivi l'HTML con una `<section>` per slide, `width:1080px; height:1350px;
page-break-after:always`, un solo colore d'accento e testo mai sotto i 28px:
si leggono sul telefono, in miniatura. Se nel progetto c'è un design system o
una skill di brand, usala e non inventare una palette. Controlla accenti e
apostrofi nel PDF finale: alcuni font li rendono male.

## Output

Prima il testo slide per slide, come elenco numerato che l'utente legge in
dieci secondi. Poi il **testo del post**: un carosello ha comunque bisogno di
2-3 righe sopra, che sono la vera apertura nel feed. Passa entrambi per
`/li-umano`. Costruisci il PDF solo se l'utente approva il testo.

Non si carica niente su LinkedIn. Il PDF lo pubblica l'utente.
