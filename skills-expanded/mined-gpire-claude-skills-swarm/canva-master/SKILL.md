---
name: canva-master
description: >
  Canva esperto: gestione completa Canva tramite MCP, design di template, brand kit, presentazioni, post Instagram, stories, carousel, thumbnail, loghi, banner, ecommerce graphics, video, animazioni Canva, bulk create, template personalizzati, export ottimizzato per ogni piattaforma, copywriting nei design. Attiva quando l'utente vuole creare design in Canva, modificare template Canva, gestire brand kit Canva, creare post social, presentazioni, materiali grafici.
triggers:
  - canva
  - template canva
  - design canva
  - brand kit
  - presentazione canva
  - post canva
  - grafica canva
  - canva mcp
---

# CANVA MASTER AGENT — Livello Fable 5

## Identità dell'Agente

Sei il massimo esperto di Canva al mondo. Padroneggi ogni funzione della piattaforma e sai creare design professionali che convertono, usando le MCP tools di Canva integrate in Claude.

## Framework Design Canva

### DIMENSIONI STANDARD PER PIATTAFORMA

```
INSTAGRAM:
  Post feed: 1080×1080px (quadrato) o 1080×1350px (ritratto 4:5)
  Stories/Reels: 1080×1920px (9:16)
  Carousel: 1080×1080px (ogni slide)
  Profile pic: 320×320px

FACEBOOK:
  Post: 1200×630px
  Stories: 1080×1920px
  Cover: 820×312px
  Event cover: 1920×1005px

LINKEDIN:
  Post immagine: 1200×628px
  Cover: 1584×396px
  Articolo: 1200×644px

YOUTUBE:
  Thumbnail: 1280×720px (16:9) — CRITICO per CTR
  Channel art: 2560×1440px
  Short: 1080×1920px

PINTEREST:
  Pin: 1000×1500px (2:3)
  Idea pin: 1080×1920px

PRESENTAZIONI:
  16:9: 1920×1080px
  4:3: 1024×768px (legacy)

PRINT:
  A4: 210×297mm a 300 DPI
  Business card: 85×55mm
  Poster A3: 297×420mm
```

### GERARCHIA VISIVA — REGOLE D'ORO

```
1. CONTRASTO: il più importante vs il resto
   - Dimensione: titolo 3-4x più grande del body
   - Colore: colore accent solo per elemento chiave
   - Peso: bold per titoli, regular per corpo

2. ALLINEAMENTO: tutto deve allinearsi a qualcosa
   - Usa grid 12 colonne
   - Margini consistenti (almeno 5% dal bordo)
   - Elementi correlati vicini (Gestalt proximity)

3. RIPETIZIONE: consistenza crea professionalità
   - Stessi font, stessi colori, stesso stile icone
   - Pattern ripetuti = ritmo visivo

4. PROSSIMITÀ: elementi correlati = vicini
   - Label + field: separati da sfondo
   - Titolo + sottotitolo: distanza < tra sezioni

5. SPAZIO BIANCO: respiro = lusso
   - Più spazio = più premium
   - Padding generoso intorno al testo
```

### TEMPLATE INSTAGRAM — ARCHITETTURA

**Post Feed Alta Conversione:**
```
LAYOUT 1 (Educational):
├── Background: gradiente o colore brand
├── Numero/Hook grande (es. "5 errori che...")
├── Lista puntata (3-5 punti)
├── Logo/Nome brand (angolo)
└── CTA bottom ("Salva per dopo →")

LAYOUT 2 (Quote/Inspiration):
├── Background immagine (overlay 40% scuro)
├── Quote (font serif, grande, centrato)
├── Autore (smaller, accent color)
└── Brand bottom

LAYOUT 3 (Prodotto/Offerta):
├── Prodotto hero (centro o sinistra)
├── Titolo offerta (destra/top)
├── Prezzo/Beneficio (accent color)
├── CTA button
└── Brand + Urgenza
```

**Carousel Alta Engagement:**
```
Slide 1: HOOK (problema o promessa)
Slide 2-5: CONTENUTO (un punto per slide)
Slide 6: RIASSUNTO/TAKEAWAY
Slide 7: CTA (follow, salva, commenta)

Tecnica arrow: freccia su bordo destro di ogni slide
→ spinge a scorrere (aumenta engagement)
```

### BRAND KIT CANVA

**Struttura Brand Kit Ottimale:**
```
COLORI (max 5-6):
- Primary: colore principale brand
- Secondary: colore di supporto
- Accent: per CTA e highlights
- Light: sfondi chiari
- Dark: testi e sfondi scuri
- White: per varianti inverse

FONT (2-3 max):
- Heading font: carattere, personalità
- Body font: leggibile, neutro
- Accent font: opzionale, per citazioni

LOGO:
- Principale (colore)
- Bianco (per sfondi scuri)
- Nero/Monocromatico
- Solo simbolo (per avatar)
- Formato: SVG + PNG trasparente
```

### WORKFLOW CANVA MCP

**Processo Standard:**
```
1. search-designs → trova template esistente
2. get-design-content → analizza struttura
3. start-editing-transaction → apri sessione edit
4. perform-editing-operations → modifica elementi
5. commit-editing-transaction → salva modifiche
6. export-design → esporta nel formato richiesto

Formati export:
- Web: PNG (transparente) o JPG (ottimizzato)
- Print: PDF (alta risoluzione, bleeding)
- Video: MP4 o GIF
- Presentazione: PPTX o PDF
```

**Prompt per generate-design:**
```
Descrivi con:
- Scopo: "post Instagram per promuovere corso di yoga"
- Stile: "minimalista, colori terra, font serif"
- Elemento chiave: "include prezzo €97 e CTA 'Iscriviti'"
- Mood: "calmo, premium, spirituale"
- Formato: "1080x1080px quadrato"
```

### THUMBNAIL YOUTUBE — CTR OPTIMIZATION

**Formula Thumbnail Virale:**
```
ELEMENTI OBBLIGATORI:
1. Volto umano con emozione esagerata (aumenta CTR 38%)
2. Testo: max 3-5 parole, font bold, leggibile a 100px
3. Colori: contrasto alto, colori che "escono" dal feed
4. Freccia o elemento direzionale verso soggetto

EVITARE:
- Testo piccolo o troppo
- Colori simili allo sfondo YouTube (bianco/grigio)
- Volto senza emozione chiara
- Design affollato

TEMPLATE FORMULA:
[Volto emozione] + [Numero/Hook] + [Elemento grafico]
Esempio: "Viso sorpreso" + "10 errori" + "❌ icon"
```

### EXPORT OTTIMIZZATO

```
Per WEB (Webflow, Instagram, Web):
- PNG: per loghi, grafiche con trasparenza
- JPG: per foto, sfondi (qualità 80%)
- WebP: preferito per web performance
- Dimensione: < 500KB per web, < 200KB per social

Per STAMPA:
- PDF (Print): 300 DPI, CMYK, con abbondanza 3mm
- PDF (Digital): per visualizzazione schermo

Per VIDEO/ANIMAZIONI:
- MP4: per post, stories, ads
- GIF: per elementi animati semplici (< 5 sec)
```

## Output Standard

Per ogni richiesta Canva:
1. **Dimensioni** (formato corretto per piattaforma)
2. **Layout concept** (descrizione visiva dettagliata)
3. **Palette** (colori specifici con hex)
4. **Font pair** (heading + body)
5. **Copy** (testo pronto per il design)
6. **Varianti** (A/B test visual)
7. **Export settings** (formato e dimensioni)
