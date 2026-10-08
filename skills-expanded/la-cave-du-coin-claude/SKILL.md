# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev     # Start development server
npm run build   # Build for production
npm run start   # Start production server
npm run lint    # Run ESLint
```

## Architecture

**Next.js 16** project using the **App Router** (`app/` directory).

### Tech Stack
- **Framework**: Next.js 16.2.2, React 19.2.4
- **Styling**: Tailwind CSS v4 with custom CSS variables (OKLCH color space)
- **UI Components**: shadcn/radix-ui, Magic UI
- **Animations**: GSAP with @gsap/react (SplitText, ScrollTrigger plugins)
- **Icons**: Lucide React
- **Fonts**: Custom local fonts (The Seasons, Century 751, Quicksand)

### Project Structure
```
app/              # Next.js App Router
  ├── page.js     # Homepage (hero, sections, footer)
  ├── layout.js   # Root layout
  ├── globals.css # Tailwind v4 + theme variables
  └── fonts.js    # Local font definitions
components/
  ├── ui/         # shadcn/Magic UI components
  └── *.jsx       # Custom components (CopyBlur, MorphingText)
lib/
  └── utils.js    # cn() utility for class merging
public/           # Static assets (fonts, images, logo)
```

### Key Patterns
- Path alias `@/*` maps to project root (see `jsconfig.json`)
- All components use client-side rendering (`"use client"`) where GSAP animations are needed
- Custom fonts are preloaded and exported from `app/fonts.js`
- Tailwind v4 uses `@import "tailwindcss"` and `@theme inline` for custom tokens

---

## Brand Identity

### Nom & Slogan
- **Nom** : La Cave du Coin
- **Sous-titre** : Le Repère des Copains
- **Slogan** : Vous accompagne pour trinquer à vos jolis moments
- **Année d'ouverture** : 2024
- **Type** : Cave à vins indépendante

### Description courte
Pour tous vos jolis moments — mariage, baptême, cousinade, grande tablée du dimanche — La Cave du Coin vous accompagne avec des sélections de vins, champagnes et spiritueux sur-mesure, pensées pour surprendre et régaler vos invités. Chaque événement est unique, votre sélection aussi.

### L'histoire
Quatre amis, quatre amoureux du vin et du travail bien fait. Ils se lancent un défi : partager leur passion en ouvrant une cave à vin près de l'église. La Cave du Coin, c'est un véritable repère de copains où vous découvrirez des vins que vous ne trouverez pas ailleurs.

Les vedettes sont les petits producteurs qui osent sortir des sentiers battus — des vins authentiques, souvent qualifiés de « nature » ou « vivants », élaborés sans produits chimiques de synthèse, ni intrants œnologiques, à partir de raisins biologiques vendangés à la main.

Ici, pas de vins déguisés avec des sulfites, levures ou arômes ajoutés. L'objectif est de revenir aux racines du terroir. Plus de 200 références en boutique, de la rareté exceptionnelle au vin plus abordable dès 6 euros la bouteille.

### Équipe
- **Propriétaire** : Yann DANIEL
- **Caviste** : Samuel Miseriaux — jeune talent de la commune, en fin d'études de caviste

### Animations
Les **jeudis et vendredis soir** : soirées dégustation régulières autour des vins de la cave — découvrir en convivialité une région, un cépage… Un rendez-vous de bons copains où chaque bouteille raconte une histoire.

---

## Informations Pratiques

### Coordonnées
- **Adresse** : 36 place Andrée Récipon, Laillé, 35890
- **Téléphone** : 06 86 89 12 88
- **Email** : mimi-li@hotmail.fr (contact perso)

### Horaires d'ouverture
| Jour | Horaires |
|------|----------|
| Lundi | Fermé |
| Mardi | 15h30 – 19h00 |
| Mercredi | 10h00 – 13h00 · 15h30 – 19h00 |
| Jeudi | 10h00 – 13h00 · 15h30 – 21h30 |
| Vendredi | 10h00 – 13h00 · 15h30 – 21h30 |
| Samedi | 10h00 – 13h00 · 14h30 – 19h00 |
| Dimanche | Fermé |

### Réseaux sociaux
- **Instagram** : [@lacaveducoin.laille](https://www.instagram.com/lacaveducoin.laille)
- **Facebook** : [La Cave du Coin](https://www.facebook.com/people/La-Cave-du-Coin/61570527667602/)

---

## Design System

### Couleurs
| Nom | Hex | Usage |
|-----|-----|-------|
| Bleu Ardoise | `#26495f` | Couleur principale — nav, headers, CTA |
| Blanc Pur | `#FFFFFF` | Fond, texte sur foncé |
| Nuit | `#1a3347` | Footer, ombres |
| Horizon | `#3a6b87` | Hover, états actifs |
| Brume | `#a8c4d0` | Bordures, tags |
| Écume | `#e8f2f6` | Fonds alternatifs |
| Or Vieilles Vignes | `#c9a84c` | Accent — prix, badges, highlights |
| Parchemin | `#f5f0e8` | Cartes, sections tièdes |

### Typographie
- **The Seasons** — titres principaux, identité
- **Century 751** — logo, caractère
- **Quicksand** — corps de texte, UI

### Sections du site (ordre recommandé)
1. **Hero** — logo + menu + image background
2. **Notre histoire** — 4 amis, philosophie vins nature, Yann & Samuel
3. **Nos vins** — 200+ références, bio, local, dès 6€
4. **La carte / Ardoise** — vins au verre, suggestions du moment
5. **Boutique** — bouteilles à emporter, sélection sur-mesure événements
6. **Coup de cœur** — producteur mis en avant chaque mois
7. **Événements** — soirées jeudi/vendredi, dégustations
8. **Galerie** — ambiance du lieu, comptoir, équipe
9. **Réservation** — formulaire simple (événements, sélection sur-mesure)
10. **Footer** — adresse, horaires, réseaux, Google Maps