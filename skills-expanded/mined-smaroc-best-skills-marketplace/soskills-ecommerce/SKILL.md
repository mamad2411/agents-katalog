---
name: soskills-ecommerce
description: >
  Generate a complete Next.js 16 e-commerce store with cart, Stripe checkout, SEO, and one-click
  Vercel deployment. Helps users find trending products via /last30days if they have no idea.
  Finds dropshipping suppliers from Amazon links (AliExpress, Alibaba, CJ Dropshipping, etc.)
  with margin calculations and comparison reports. Outputs a full project folder ready to deploy.
  Beginner-friendly deployment guide included.
  Use when user says 'page de vente', 'sales page', 'landing page produit', 'page e-commerce',
  'page infoproduit', 'vendre un produit', 'créer une page de vente', 'boutique', 'shop',
  'e-commerce', 'fournisseur', 'dropshipping', 'supplier', or wants to build a conversion-optimized online store.
---

# E-commerce Store Generator

Generate a complete, production-ready Next.js 16 e-commerce store with cart, SEO, and one-click Vercel deployment.

## CRITICAL: French Language with Proper Accents

**ALL generated content MUST use correct French accents and diacritics.** This is non-negotiable.

Examples of CORRECT French:
- "Élevé" not "Eleve"
- "Caractéristiques" not "Caracteristiques"
- "Première" not "Premiere"
- "Récapitulatif" not "Recapitulatif"
- "Général" not "General"
- "Sécurisé" not "Securise"
- "Créer" not "Creer"
- "Vérifiée" not "Verificee"
- "Complète" not "Complete"
- "Livré" not "Livre"
- "Prêt" not "Pret"
- "Télécharge" not "Telecharge"
- "Séléctionne" → "Sélectionne"
- "Clé" not "Cle"
- "Régulièrement" not "Regulierement"
- "Propriété" not "Propriete"
- "Société" not "Societe"

This applies to:
- All UI text (buttons, labels, headings, descriptions)
- Product data (names, descriptions, specs, reviews)
- Legal pages (CGV, mentions légales)
- DEPLOYER.md and README.md
- FAQ questions and answers
- Comments in code (if in French)
- Metadata (SEO titles, descriptions)
- Testimonials
- Error messages

**Use `&apos;` for apostrophes in JSX, and standard `'` in .md/.txt files.**

## Workflow

### Phase 1 : Product Discovery

Ask the user:

> Quel type de produit tu veux vendre ?
> 1. **Produit physique** (vêtements, accessoires, gadgets, beauté...)
> 2. **Produit digital / infoproduit** (formation, ebook, template, coaching...)
>
> Si tu n'as pas encore d'idée, dis-moi juste ta niche ou dis "trouve-moi un produit" et je vais chercher les tendances du moment.

**If the user has no idea or says "trouve-moi un produit" :**

Use the `/last30days` skill to research trending products. Run it with a prompt like:

```
/last30days
```

Then prompt: "Produits e-commerce tendance et forte demande en [niche si donnée, sinon généraliste]. Recherche sur Reddit (r/shutupandtakemymoney, r/BuyItForLife, r/entrepreneur, r/dropshipping), X (trending products, viral products), et le web (Google Trends, trending on Amazon/TikTok Shop). Je cherche des produits avec forte demande, peu de concurrence, et bonne marge."

From the results, propose **3 product ideas** to the user with:
- Product name and category
- Why it's trending (data from the research)
- Estimated price range
- Target audience
- Viral potential score (1-5)

Let the user pick one, then proceed.

**If the user has a product idea :**

Ask for the following details (skip what they already provided):

1. **Product name** and **brand name**
2. **Price** (+ original price if there's a promo/strikethrough)
3. **Product images** — see "Phase 1.5: Product Images" below
4. **Variants** — sizes, colors, options (if applicable)
5. **Short description** (2-3 lines) + **detailed description**
6. **Specs** — material, dimensions, weight, etc.
7. **Target audience** and **pain points** (3-5)
8. **Benefits** (5-7)
9. **Testimonials** (2-3) — generate realistic ones if not provided
10. **Guarantee** — e.g. "Retour gratuit 30 jours"
11. **Shipping info** — e.g. "Livraison gratuite en 48h"
12. **Stripe publishable key** — use `pk_test_YOUR_KEY` placeholder if not provided
13. **Stripe price ID** — use `price_YOUR_ID` placeholder if not provided

If the user doesn't have all info, generate sensible defaults based on the product type and research.

### Phase 1.3 : Supplier Research (Dropshipping)

**Triggered when the user provides Amazon links, product URLs, or says "trouve-moi des fournisseurs".**

> Tu veux que je recherche des fournisseurs pour tes produits ?
> 1. **J'ai des liens Amazon** — donne-moi les URLs et je trouve les fournisseurs équivalents
> 2. **J'ai une liste de produits** — décris-les et je cherche les meilleurs fournisseurs
> 3. **Non merci** — je passe aux images

**If the user provides Amazon links or product descriptions :**

For each product URL or description provided, use web search to:

1. **Extract product info from the Amazon link** — product name, brand, price, key specs, ASIN
2. **Search for equivalent products on supplier platforms:**
   - **AliExpress** — search: `site:aliexpress.com "[product name]" OR "[key specs]"`
   - **Alibaba** — search: `site:alibaba.com "[product name]" wholesale`
   - **CJ Dropshipping** — search: `site:cjdropshipping.com "[product name]"`
   - **DHgate** — search: `site:dhgate.com "[product name]"`
   - **1688.com** (Chinese domestic) — search: `site:1688.com "[product name in English]"`
   - **Temu (wholesale)** — search: `site:temu.com "[product name]"`
   - General search: `"[product name]" dropshipping supplier wholesale`

3. **For each supplier found, collect:**
   - Supplier name and platform
   - Product URL
   - Unit price (and price tiers if available)
   - Minimum order quantity (MOQ)
   - Estimated shipping time to France/Europe
   - Shipping cost estimate
   - Seller rating / reviews / years on platform
   - Product images available
   - Variants available (sizes, colors)

4. **Calculate margins for each supplier:**
   - Amazon retail price (reference)
   - Supplier unit cost
   - Estimated shipping cost
   - **Potential margin** = Amazon price - (supplier cost + shipping)
   - **Margin percentage** = margin / Amazon price × 100

5. **Generate a Supplier Report** saved as `~/Desktop/boutique-[slug]/FOURNISSEURS.md`:

```markdown
# Rapport Fournisseurs — [Date]

## Produit 1 : [Nom du produit]

**Référence Amazon :** [lien Amazon]
**Prix Amazon :** [prix] EUR
**ASIN :** [code]

### Fournisseurs trouvés

#### Fournisseur 1 (Recommandé) — [Nom]
- **Plateforme :** AliExpress / Alibaba / CJ Dropshipping
- **Lien :** [URL]
- **Prix unitaire :** [prix] EUR
- **MOQ :** [quantité]
- **Livraison :** [délai] jours vers la France
- **Frais de livraison :** [prix] EUR
- **Note vendeur :** [note] / 5 ([nombre] avis)
- **Ancienneté :** [X] ans sur la plateforme
- **Marge potentielle :** [montant] EUR ([pourcentage]%)
- **Avantages :** [points forts]
- **Inconvénients :** [points faibles]

#### Fournisseur 2 — [Nom]
(même structure)

#### Fournisseur 3 — [Nom]
(même structure)

### Comparatif rapide

| Fournisseur | Prix | Livraison | Marge | Note |
|---|---|---|---|---|
| [Nom 1] | X EUR | X jours | X% | X/5 |
| [Nom 2] | X EUR | X jours | X% | X/5 |
| [Nom 3] | X EUR | X jours | X% | X/5 |

### Recommandation

[Explication de pourquoi le fournisseur 1 est recommandé : meilleur rapport qualité/prix/fiabilité/délai]

---

(Répéter pour chaque produit)

---

## Conseils dropshipping

### Avant de commander
- **Commande un échantillon** — teste toujours le produit toi-même avant de vendre
- **Vérifie la qualité** — compare avec le produit Amazon pour s'assurer que c'est équivalent
- **Négocie les prix** — sur Alibaba, contacte le fournisseur directement pour des prix de gros
- **Vérifie les certifications** — CE, ROHS pour l'Europe si produit électronique

### Automatisation dropshipping
- **CJ Dropshipping** — intégration API disponible, fulfillment automatique
- **DSers** (app Shopify/WooCommerce) — connecte AliExpress et automatise les commandes
- **AutoDS** — automatisation complète du dropshipping multi-plateforme
- **Zendrop** — fulfillment US/EU rapide avec branding personnalisé

### Prix de vente recommandé
- **Marge minimum viable :** 30% après tous les coûts (produit + livraison + pub)
- **Formule :** Prix de vente = (Coût produit + Livraison) × 3
- **Inclure dans le calcul :** frais Stripe (1.4% + 0.25 EUR), coût publicitaire moyen

### Plateformes de paiement fournisseur
- **AliExpress :** CB directe, pas de minimum
- **Alibaba :** Trade Assurance (protection acheteur), virement, CB
- **CJ Dropshipping :** Solde prépayé ou CB
- **PayPal** : éviter pour les gros volumes (frais élevés)
```

6. **After generating the report, ask:**

> J'ai trouvé [X] fournisseurs pour tes [Y] produits. Le rapport complet est dans `FOURNISSEURS.md`.
>
> Tu veux que je :
> 1. **Configure la boutique avec les prix optimisés** (basés sur les marges calculées)
> 2. **Approfondisse la recherche** sur un fournisseur spécifique
> 3. **Continue avec les images et la boutique**

**Use the recommended supplier's product images if available** (with user permission) for the store, or proceed to Phase 1.5 for image options.

### Phase 1.5 : Product Images

**ALWAYS ask the user about images before generating the store:**

> Pour les images produit, tu préfères :
> 1. **J'ai déjà mes images** — donne-moi les URLs ou les chemins de fichiers
> 2. **Génère-les avec l'IA** — je crée des visuels produit réalistes avec Gemini (5 images : face, profil, détail, packaging, mode de vie)
> 3. **Utilise des placeholders** — je mettrai mes vraies photos plus tard

**If the user chooses option 1 (has images) :**
- Ask for 3-5 image URLs or local file paths
- Copy local files to `public/images/` in the project
- Use the provided URLs directly in `products.ts`

**If the user chooses option 2 (generate with AI) :**
- Use the `/cc-nano-banana` skill to generate 5 product images with Gemini
- Generate the following angles:
  1. **Main product shot** — clean, centered, on white/light background, studio lighting
  2. **Lifestyle shot** — product in use, in a real environment
  3. **Detail/close-up** — texture, material, key feature close-up
  4. **Packaging** — product in its box/packaging, unboxing feel
  5. **Ambiance/context** — product in a styled room or setting

- Prompt template for each image (adapt to the specific product):
  ```
  Professional e-commerce product photo of [product name and description].
  [Specific angle: front view / lifestyle / close-up / packaging / styled room].
  Clean, bright lighting, white or light background, high resolution,
  commercial product photography style, no text, no watermark.
  ```

- Save generated images to `public/images/` in the project:
  - `product-main.jpg`
  - `product-lifestyle.jpg`
  - `product-detail.jpg`
  - `product-packaging.jpg`
  - `product-ambiance.jpg`

- Reference them in `products.ts` as `/images/product-main.jpg`, etc.

**If the user chooses option 3 (placeholders) :**
- Use `https://placehold.co/800x800/f5f5f5/9ca3af?text=Photo+Produit` style placeholders
- Generate 5 with different labels: Face, Profil, Détail, Packaging, Mode+de+vie
- Easy for the user to replace later with real photos in `public/images/`

### Phase 1.7 : Ad Creatives (Optional)

**After product images are handled, propose ad creative generation:**

> Tu veux que je te génère aussi des visuels publicitaires prêts à poster ?
> 1. **Oui, pour Instagram + TikTok** — je crée des ads au format portrait (1080x1350 pour Instagram, 1080x1920 pour TikTok)
> 2. **Non merci** — je passe directement à la boutique

**If the user says yes :**

Use the `/cc-nano-banana` skill to generate ad creatives. Save them in `~/Desktop/boutique-[slug]/ads/`.

Generate **4 ad creatives** with different angles:

#### Ad 1 — Hero Product (Instagram 1080x1350)
```
Professional product advertisement for [product name].
Product centered on a clean lifestyle background.
Bold promotional text overlay: "[PRODUCT NAME]" at top, "-[X]% AUJOURD'HUI" badge.
Price "[XX,XX] €" prominent. "Livraison gratuite" mention.
Modern e-commerce ad style, premium feel, portrait format 1080x1350.
No watermark.
```

#### Ad 2 — Before/After or Problem/Solution (Instagram 1080x1350)
```
Split-screen advertisement for [product name]. Portrait format 1080x1350.
Top half: the problem (dull/boring/frustrating situation without the product).
Bottom half: the solution (beautiful/satisfying result with the product).
Clean modern design, subtle divider line, product shown in solution half.
Text: "Avant / Après" or "Le problème / La solution". No watermark.
```

#### Ad 3 — Social Proof (Instagram 1080x1350)
```
Customer testimonial advertisement for [product name]. Portrait format 1080x1350.
Product image with 5-star rating overlay.
Quote: "[short testimonial text]" with customer name.
Badge: "[X]+ clients satisfaits". Trust indicators.
Clean white background, modern typography. No watermark.
```

#### Ad 4 — TikTok/Reels Cover (1080x1920)
```
TikTok-style product showcase for [product name]. Portrait format 1080x1920 (9:16).
Product in a trendy lifestyle setting, vibrant and eye-catching.
Bold text overlay: "[catchy hook about the product]".
Modern, Gen-Z aesthetic, slightly saturated colors, dynamic composition.
Looks native to TikTok/Reels feed. No watermark.
```

**Output structure:**
```
~/Desktop/boutique-[slug]/ads/
├── ad-instagram-hero-1080x1350.png
├── ad-instagram-before-after-1080x1350.png
├── ad-instagram-social-proof-1080x1350.png
├── ad-tiktok-cover-1080x1920.png
└── README-ADS.md
```

**README-ADS.md** contains:
- Which ad to use for which platform
- Recommended caption for each ad
- Targeting suggestions (age, interests, lookalike)
- A/B testing recommendations (test hero vs social proof first)
- Budget allocation suggestion (start with 5-10€/day, scale what works)

### Phase 2 : Generate the Next.js 16 Store

Generate a complete Next.js 16 application in a folder on the Desktop:

```
~/Desktop/boutique-[slug]/
```

#### Project Structure

```
boutique-[slug]/
├── package.json
├── next.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.mjs
├── .env.local.example
├── public/
│   ├── images/
│   │   └── (product images or placeholders)
│   ├── favicon.ico
│   └── robots.txt
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout + metadata + fonts
│   │   ├── page.tsx            # Homepage / product page
│   │   ├── panier/
│   │   │   └── page.tsx        # Cart page
│   │   ├── checkout/
│   │   │   └── page.tsx        # Stripe checkout page
│   │   ├── merci/
│   │   │   └── page.tsx        # Thank you / success page
│   │   ├── mentions-legales/
│   │   │   └── page.tsx        # Legal page
│   │   ├── cgv/
│   │   │   └── page.tsx        # Terms page
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── Header.tsx          # Nav bar with cart icon + count
│   │   ├── Footer.tsx          # Footer with links
│   │   ├── ProductHero.tsx     # Product image gallery + info (2-col)
│   │   ├── ProductGallery.tsx  # Image gallery with thumbnails
│   │   ├── ProductInfo.tsx     # Price, variants, add to cart
│   │   ├── Benefits.tsx        # Why this product section
│   │   ├── Reviews.tsx         # Customer reviews
│   │   ├── FAQ.tsx             # Accordion FAQ
│   │   ├── CartDrawer.tsx      # Slide-out cart drawer
│   │   ├── CartItem.tsx        # Single cart item row
│   │   ├── QuantitySelector.tsx
│   │   ├── VariantSelector.tsx
│   │   ├── TrustBadges.tsx     # Shipping, payment, guarantee icons
│   │   ├── StickyAddToCart.tsx  # Mobile sticky bottom bar
│   │   ├── NewsletterBar.tsx
│   │   └── SEOJsonLd.tsx       # Structured data component
│   ├── context/
│   │   └── CartContext.tsx      # Cart state management (React Context)
│   ├── lib/
│   │   ├── stripe.ts           # Stripe client init
│   │   ├── products.ts         # Product data
│   │   └── utils.ts            # Price formatting, etc.
│   └── types/
│       └── index.ts            # TypeScript types
├── FOURNISSEURS.md             # Supplier research report (if dropshipping)
├── DEPLOYER.md                 # Step-by-step deployment guide
└── README.md                   # Quick start
```

#### Tech Stack

- **Next.js 16** (App Router, React 19, Turbopack)
- **TypeScript**
- **Tailwind CSS 4** (latest)
- **Stripe** (client-side checkout via `@stripe/stripe-js`)
- **No database needed** — product data is in `lib/products.ts`
- **No backend API routes needed** — uses Stripe Checkout redirect (client-side)

#### package.json

```json
{
  "name": "boutique-[slug]",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^16",
    "react": "^19",
    "react-dom": "^19",
    "@stripe/stripe-js": "^5"
  },
  "devDependencies": {
    "@types/node": "^22",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5.7",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "postcss": "^8"
  }
}
```

#### Key Implementation Details

**Cart (CartContext.tsx) :**
- React Context + useReducer
- Actions: ADD_ITEM, REMOVE_ITEM, UPDATE_QUANTITY, CLEAR_CART
- Persist cart to localStorage (restore on mount)
- Expose: items, totalItems, totalPrice, addItem, removeItem, updateQuantity, clearCart
- Cart drawer slides in from right when item added

**Product Page (page.tsx) :**
- 2-column layout on desktop (gallery left 55%, info right 45%)
- Image gallery with thumbnail selector (click to swap main image)
- Variant selector (size/color) with visual buttons
- Quantity selector with +/- buttons
- "Ajouter au panier" primary CTA (blue, full-width)
- Trust badges: livraison gratuite, paiement sécurisé, retour 30j
- Accordion: Description, Caractéristiques, Livraison & Retours
- Below fold: Benefits, Reviews, FAQ
- Sticky mobile bar at bottom with price + "Ajouter au panier"
- Breadcrumb: Accueil > [Catégorie] > [Produit]

**Cart Page (panier/page.tsx) :**
- List of cart items with image, name, variant, quantity, price
- Quantity update and remove buttons
- Order summary sidebar: sous-total, livraison, total
- "Passer commande" button → Stripe checkout
- "Continuer mes achats" link back to product

**Checkout (checkout/page.tsx) :**
- Loads Stripe.js
- Redirects to Stripe Checkout with cart items
- Uses lineItems from cart context
- successUrl: /merci
- cancelUrl: /panier

**Thank You (merci/page.tsx) :**
- Confirmation message
- Order summary
- Clear cart on mount
- Link back to store

#### SEO Implementation

**In layout.tsx — Global Metadata:**
```tsx
export const metadata: Metadata = {
  title: "[Brand] — [Product Name] | Livraison Gratuite",
  description: "[Product short description optimized for search - 155 chars max]",
  keywords: ["[product]", "[catégorie]", "[brand]", "acheter", "pas cher", "livraison gratuite"],
  openGraph: {
    title: "[Product Name] — [Brand]",
    description: "[Short description]",
    images: ["/images/product-main.jpg"],
    type: "website",
    locale: "fr_FR",
  },
  twitter: {
    card: "summary_large_image",
    title: "[Product Name]",
    description: "[Short description]",
    images: ["/images/product-main.jpg"],
  },
  robots: { index: true, follow: true },
  alternates: { canonical: "https://[domain].vercel.app" },
};
```

**SEOJsonLd.tsx — Product Structured Data:**
```tsx
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "description": "[Description]",
  "image": ["[image URLs]"],
  "brand": { "@type": "Brand", "name": "[Brand]" },
  "offers": {
    "@type": "Offer",
    "price": "[price]",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "[product URL]",
    "priceValidUntil": "[date + 30 days]",
    "seller": { "@type": "Organization", "name": "[Brand]" }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "[count]"
  }
}
</script>
```

**robots.txt:**
```
User-agent: *
Allow: /
Sitemap: https://[domain]/sitemap.xml
```

**Additional SEO:**
- All images have descriptive alt text (in French with accents)
- Semantic HTML (main, article, section, nav, footer)
- Heading hierarchy (single H1 = product name)
- Internal links between pages
- Fast loading (no external dependencies except Stripe)
- Mobile-first responsive design

#### Design System (Tailwind) — LIGHT SHOPIFY THEME

Use the light Shopify-style aesthetic from `references/design-system.md`:

- **Background:** white (#ffffff), secondary: #fafafa
- **Cards:** white with subtle border (#e5e7eb) and light shadow
- **Accent/CTA:** blue (#2563eb) — clean, trustworthy, Shopify-like
- **Text:** dark (#1a1a1a), muted: #6b7280, dim: #9ca3af
- **Price/promo:** red (#dc2626) for sale prices and promo badges
- **Success:** green (#16a34a) for stock indicators and guarantees
- **Font:** Inter via next/font/google
- **Rounded corners:** rounded-xl for cards, rounded-lg for buttons
- **Borders:** border-gray-200 (#e5e7eb), subtle and clean
- **Shadows:** light and minimal (shadow-sm, shadow-md)
- **Hover states:** slightly darker bg, stronger shadow on cards

**Shopify Light Theme Reference Points:**
- Clean white background, lots of breathing room
- Product images on light/white bg look professional
- Subtle gray borders define sections, not bold lines
- Blue CTA buttons (trust color) — NOT red buttons
- Red only for prices and promo badges
- Light gray (#fafafa) for alternating sections and footer
- Header: white bg with bottom border
- Footer: light gray bg (#fafafa)
- Trust badges: light bg with subtle border
- Cards: white with thin gray border + minimal shadow

**IMPORTANT: The store MUST look like a real premium Shopify store with a light theme. Think Allbirds, Glossier, or default Shopify Dawn theme. Clean, bright, trustworthy, professional. Product images are the hero. NO dark mode.**

**CRITICAL: NO EMOJIS, NO AI-LOOKING ELEMENTS**

The store must be indistinguishable from a real Shopify store built by a human designer. This means:

- **ZERO emojis anywhere** — no 🚚, no 🔒, no ↩️, no 🌅, no 📸, no 💡, no 🔌, no ✓ emoji. NONE.
- Use **SVG icons or plain text** instead of emojis for trust badges, benefits, etc.
- Use simple checkmarks (✓ character or SVG) for "verified" labels
- **No gradient text**, no glow effects, no neon colors
- **No "AI copywriting" patterns**: avoid overly enthusiastic language, excessive exclamation marks, or formulaic benefit lists
- **No floating badges** or animated attention-grabbers
- **Typography must be restrained**: no ALL CAPS on body text, uppercase only for small labels/badges
- **Icons**: use simple SVG stroke icons (Heroicons style) or no icons at all — let the text speak
- **Trust badges**: simple text with a small icon or just text, not emoji-heavy badges
- **Benefits section**: clean cards with a short title + description, NO emoji icons — use subtle SVG icons or just a number/bullet
- **Reviews**: no emoji stars, use SVG star icons or simple "★" character in a muted color
- **CTA buttons**: clean text, no emojis, no arrows unless it's a standard → character
- **Stock indicator**: a simple colored dot (CSS) + text, no emoji
- **Thank you page**: no large emoji, use a simple heading + text

The goal is that someone looking at the store cannot tell it was generated by AI. It should look like a real store that a Shopify merchant set up using the Dawn theme with minor customizations.

#### .env.local.example

```
# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY

# Site
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### Phase 3 : Generate DEPLOYER.md

This file is CRITICAL. It must be written for someone who has NEVER deployed an app before. Use simple language, no jargon, explain every step. **ALL French text must have proper accents.**

````markdown
# Comment mettre ta boutique en ligne (5 minutes)

## Ce dont tu as besoin

- Un compte GitHub (gratuit) — github.com
- Un compte Vercel (gratuit) — vercel.com
- Un compte Stripe (gratuit) — stripe.com

## Étape 1 : Prépare ton projet

1. Ouvre le dossier `boutique-[slug]` sur ton Bureau
2. Copie le fichier `.env.local.example` et renomme-le `.env.local`
3. Ouvre `.env.local` avec un éditeur de texte (TextEdit sur Mac, Notepad sur Windows)
4. Remplace `pk_test_YOUR_KEY` par ta clé publique Stripe (on t'explique comment la trouver juste en dessous)

### Où trouver ta clé Stripe ?

1. Va sur dashboard.stripe.com
2. Clique sur "Développeurs" en haut à droite
3. Clique sur "Clés API"
4. Copie la "Clé publiable" (elle commence par pk_test_ ou pk_live_)
5. Colle-la dans ton fichier .env.local

### Créer un prix Stripe pour ton produit

1. Sur dashboard.stripe.com, va dans "Produits"
2. Clique "Ajouter un produit"
3. Remplis le nom, la description, le prix
4. Après création, copie l'ID du prix (il commence par price_)
5. Ouvre le fichier `src/lib/products.ts` et remplace `price_YOUR_ID` par ton ID

## Étape 2 : Mets le projet sur GitHub

### Option A : Avec GitHub Desktop (le plus simple)

1. Télécharge GitHub Desktop : desktop.github.com
2. Connecte-toi avec ton compte GitHub
3. Clique "File" > "Add Local Repository"
4. Sélectionne le dossier `boutique-[slug]` sur ton Bureau
5. Il va te proposer de "Create a Repository" — clique dessus
6. Clique "Publish repository"
7. Décoche "Keep this code private" si tu veux (optionnel)
8. Clique "Publish Repository"

### Option B : En ligne de commande (si tu es à l'aise)

```bash
cd ~/Desktop/boutique-[slug]
git init
git add .
git commit -m "Initial commit"
gh repo create boutique-[slug] --public --source=. --push
```

## Étape 3 : Déploie sur Vercel

1. Va sur vercel.com et connecte-toi avec ton compte GitHub
2. Clique "Add New..." > "Project"
3. Tu vas voir ton repo `boutique-[slug]` dans la liste — clique "Import"
4. **IMPORTANT** : Avant de déployer, clique sur "Environment Variables"
5. Ajoute cette variable :
   - Name: `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
   - Value: ta clé publiable Stripe (pk_test_... ou pk_live_...)
6. Clique "Deploy"
7. Attends 1-2 minutes... et c'est en ligne !

Vercel te donne une URL comme : `boutique-[slug].vercel.app`

## Étape 4 : Configure Stripe pour la production

Quand tu es prêt à vendre pour de vrai :

1. Sur Stripe, active ton compte (vérification d'identité)
2. Remplace ta clé `pk_test_` par ta clé `pk_live_` dans Vercel :
   - Va sur vercel.com > ton projet > Settings > Environment Variables
   - Modifie la valeur de `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
   - Clique "Save"
3. Redeploy : va dans l'onglet "Deployments" > clique les 3 points sur le dernier > "Redeploy"

## Étape 5 : Nom de domaine personnalisé (optionnel)

Si tu veux un vrai nom de domaine (genre maboutique.com) :

1. Achète un domaine sur namecheap.com ou ovh.com (~10 euros/an)
2. Sur Vercel : Settings > Domains > ajoute ton domaine
3. Vercel te donne des DNS à configurer chez ton registrar
4. Suis les instructions (ça prend 5 minutes)

## En cas de problème

- **La page est blanche** : Vérifie que tu as bien ajouté les variables d'environnement sur Vercel
- **Le paiement ne marche pas** : Vérifie ta clé Stripe et l'ID du prix dans `src/lib/products.ts`
- **Les images ne s'affichent pas** : Vérifie que les fichiers sont dans `public/images/`
- **Erreur au build** : Lance `npm run build` en local pour voir les erreurs

## C'est fait !

Ta boutique est en ligne. Partage le lien et commence à vendre.
````

### Phase 4 : Install Dependencies and Test

After generating all files, run:

```bash
cd ~/Desktop/boutique-[slug]
npm install
```

Then tell the user:

> Ta boutique est prête ! Le dossier est sur ton Bureau.
>
> Pour la tester en local :
> ```
> cd ~/Desktop/boutique-[slug]
> npm run dev
> ```
> Puis ouvre http://localhost:3000 dans ton navigateur.
>
> Pour la mettre en ligne, suis le guide `DEPLOYER.md` dans le dossier.

Open the folder:
```bash
open ~/Desktop/boutique-[slug]
```

## Copywriting Rules

- French with **correct accents everywhere** (é, è, ê, ë, à, â, ù, û, ô, î, ï, ç)
- Tutoiement ("tu")
- Headlines: specific pain → specific promise
- Benefits over features
- Social proof: numbers, names, specifics
- CTA: action verb + what they get ("Ajouter au panier", "Commander maintenant")
- FAQ: address real objections (price, quality, shipping, returns)
- No fluff words: "innovant", "révolutionnaire" — be concrete
- Product descriptions should sell, not just describe

## Design Rules

- **Light Shopify theme** (see `references/design-system.md`)
- White background, clean and bright
- Looks like a real Shopify store (Dawn theme), NOT a dark landing page
- Blue CTA buttons (#2563eb) — trustworthy and clean
- Red only for prices and promo badges
- Light gray sections (#fafafa) for visual rhythm
- Product images are the hero element
- Subtle borders and minimal shadows
- Clean, minimal, professional, trustworthy
- Mobile-first responsive
- Smooth interactions (cart drawer slide, image gallery, sticky CTA)
- Fast: no heavy libraries, minimal JS
