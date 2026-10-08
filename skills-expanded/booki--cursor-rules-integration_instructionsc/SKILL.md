---
description: 
globs: 
alwaysApply: true
---
# Feuille de Route UI - Application Booki
## Plateforme de Réservation de Terrains de Sport à Dakar

---

## 🎯 Vision & Objectifs

### Positionnement
- **Nom**: Booki
- **Cible**: 15-35 ans à Dakar
- **Mission**: Simplifier la réservation de terrains de sport (padel, football, tennis, basketball)
- **Ton**: Moderne, énergique, accessible, local mais international

### Objectifs UX
1. Réservation en moins de 3 clics
2. Interface intuitive sans apprentissage
3. Expérience mobile-first
4. Confiance et transparence
5. Gamification légère

---

## 🎨 Direction Artistique

### Palette de Couleurs
```css
/* Couleurs Principales */
--primary: #00D4AA        /* Vert turquoise vibrant */
--primary-dark: #00B894   /* Vert foncé pour hover */
--secondary: #FF6B6B      /* Rouge corail pour accents */
--accent: #FFD93D         /* Jaune doré pour notifications */

/* Couleurs Neutres */
--dark: #2D3436           /* Texte principal */
--gray: #636E72           /* Texte secondaire */
--light-gray: #DDD        /* Bordures */
--background: #F8F9FA     /* Arrière-plan */
--white: #FFFFFF          /* Cards, modales */

/* Couleurs Statut */
--success: #00B894
--warning: #FDCB6E
--error: #E17055
--info: #74B9FF
```

### Typographie (Google Fonts)
```css
/* Titres et Headers */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* Corps de texte */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Accents et CTA */
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@600;700;800&display=swap');
```

### Iconographie
- **Font Awesome 6** pour toutes les icônes
- Style: Solid et Regular mix
- Taille de base: 16px, 20px, 24px
- Couleurs: Suivre la palette définie

---

## 📱 Architecture des Écrans

### 1. Onboarding & Authentification
#### Écrans requis:
- **Splash Screen**
  - Logo Booki animé
  - Tagline: "Réservez. Jouez. Gagnez."
  - Unsplash: Terrain de sport à Dakar au coucher de soleil

- **Onboarding (3 slides)**
  - Slide 1: "Trouvez votre terrain" (carte avec pins)
  - Slide 2: "Réservez instantanément" (calendrier + bouton)
  - Slide 3: "Jouez avec vos amis" (groupe de joueurs)

- **Connexion/Inscription**
  - Login social (Google, Facebook)
  - Inscription rapide
  - Vérification SMS

### 2. Navigation Principale
#### Bottom Navigation (5 onglets):
```
🏠 Accueil     🔍 Recherche     📅 Mes Résa     💬 Messages     👤 Profil
```

### 3. Écran d'Accueil
#### Composants essentiels:
- **Header dynamique**
  - Salutation personnalisée
  - Météo actuelle
  - Notifications (badge)

- **Search Bar prominent**
  - "Quel sport aujourd'hui ?"
  - Filtres rapides: Sport, Zone, Prix

- **Section "Sports Populaires"**
  - Cards horizontales avec icônes
  - Padel, Football, Tennis, Basketball

- **Section "Près de chez vous"**
  - Carte interactive
  - Liste des terrains à proximité
  - Photos Unsplash de qualité

- **Section "Réservations Flash"**
  - Offres limitées dans le temps
  - Countdown timer
  - Badges "-30%"

### 4. Recherche & Filtres
#### Fonctionnalités:
- **Recherche géographique** 
  - Carte avec clusters
  - Liste/grille toggle
  - Filtre par distance

- **Filtres avancés**
  - Type de sport
  - Prix (slider)
  - Disponibilité
  - Équipements
  - Note des avis

### 5. Détail Terrain
#### Éléments clés:
- **Galerie photos** (carousel)
- **Informations essentielles** (prix, adresse, phone)
- **Calendrier de disponibilité**
- **Avis et notes** (étoiles + commentaires)
- **Équipements** (icônes + liste)
- **CTA prominent** "Réserver maintenant"

### 6. Processus de Réservation
#### Étapes:
1. **Sélection créneau** (calendrier interactif)
2. **Confirmation détails** (récapitulatif)
3. **Paiement** (mobile money + cartes)
4. **Confirmation** (QR code + détails)

---

## 🔧 Composants UI à Développer

### Composants Shadcn/ui Personnalisés

#### Composants de Base
```typescript
// Cards (extension des Shadcn Cards)
- SportCard: Card + Badge + FontAwesome icons
- TerrainCard: Card + Image (Unsplash) + Button
- ReservationCard: Card + Dialog + Status badges

// Forms (Shadcn + React Hook Form)
- SearchBar: Input + Command + Popover
- DateTimePicker: Calendar + Select
- FilterSheet: Sheet + Checkbox + Slider
- RatingInput: Custom star component

// Navigation (Custom + Shadcn)
- BottomNavigation: Tabs + FontAwesome
- HeaderWithSearch: Custom header
- Breadcrumb: Shadcn Breadcrumb

// Feedback (Shadcn extended)
- LoadingSkeleton: Skeleton + custom shapes
- EmptyState: Alert + custom illustrations
- Toast: Sonner toast notifications
- ConfirmDialog: AlertDialog + animations
```

#### Composants Métier
```typescript
// Terrain & Recherche
components/features/terrain/
├── terrain-card.tsx          # Card avec image Unsplash
├── terrain-gallery.tsx       # Carousel d'images
├── terrain-filters.tsx       # Sheet avec filtres
└── terrain-map.tsx          # Mapbox intégration

// Réservation
components/features/booking/
├── availability-calendar.tsx  # Calendar personnalisé
├── time-slot-picker.tsx      # Grid de créneaux
├── booking-summary.tsx       # Card récapitulatif
└── payment-form.tsx         # Form + validation Zod

// Profile & Social
components/features/profile/
├── user-avatar.tsx          # Avatar + Badge
├── booking-history.tsx      # Table + Pagination
├── review-card.tsx          # Card + Stars + Text
└── social-share.tsx         # Share buttons
```

#### Exemples de Composants
```typescript
// components/features/terrain/terrain-card.tsx
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar, faMapPin } from '@fortawesome/free-solid-svg-icons'
import Image from 'next/image'

interface TerrainCardProps {
  id: string
  name: string
  sport: string
  price: number
  rating: number
  distance: string
  image: string
  available: boolean
}

export function TerrainCard({ terrain }: { terrain: TerrainCardProps }) {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="relative aspect-video">
        <Image
          src={terrain.image}
          alt={terrain.name}
          fill
          className="object-cover"
        />
        <Badge className="absolute top-2 left-2" variant={terrain.available ? "default" : "secondary"}>
          {terrain.available ? "Disponible" : "Complet"}
        </Badge>
      </div>
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-heading font-semibold text-lg">{terrain.name}</h3>
          <div className="flex items-center gap-1">
            <FontAwesomeIcon icon={faStar} className="text-yellow-500 w-4 h-4" />
            <span className="text-sm">{terrain.rating}</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2 text-gray-600 mb-3">
          <FontAwesomeIcon icon={faMapPin} className="w-4 h-4" />
          <span className="text-sm">{terrain.distance}</span>
        </div>
        
        <div className="flex items-center justify-between">
          <div>
            <span className="text-2xl font-bold text-primary">{terrain.price}</span>
            <span className="text-gray-600 ml-1">CFA/h</span>
          </div>
          <Button className="bg-primary hover:bg-primary-dark">
            Réserver
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## 🛠️ Stack Technique

### Framework & Librairies
```json
{
  "framework": "Next.js 14+ (App Router)",
  "ui": "Shadcn/ui + Tailwind CSS",
  "icons": "Font Awesome 6 (via react-icons/fa6)",
  "images": "Unsplash API + Next.js Image",
  "animations": "Framer Motion",
  "state": "Zustand ou Context API",
  "forms": "React Hook Form + Zod",
  "maps": "Mapbox GL JS ou Google Maps"
}
```

### Configuration Initiale
```bash
# Installation du projet
npx create-next-app@latest booki --typescript --tailwind --eslint --app

# Shadcn/ui setup
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input dialog sheet tabs

# Font Awesome
npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/react-fontawesome

# Utilitaires supplémentaires
npm install framer-motion react-hook-form @hookform/resolvers zod lucide-react
```

### Structure Next.js
```
booki/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── search/page.tsx
│   ├── terrain/[id]/page.tsx
│   ├── booking/page.tsx
│   └── profile/page.tsx
├── components/
│   ├── ui/              # Shadcn components
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── bottom-nav.tsx
│   │   └── sidebar.tsx
│   ├── features/
│   │   ├── search/
│   │   ├── booking/
│   │   └── terrain/
├── lib/
│   ├── utils.ts
│   ├── unsplash.ts
│   └── validations.ts
├── hooks/
└── types/
```

### Configuration Tailwind (tailwind.config.js)
```javascript
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00D4AA',
          dark: '#00B894',
          light: '#55E5D1',
        },
        secondary: '#FF6B6B',
        accent: '#FFD93D',
        sport: {
          padel: '#00D4AA',
          football: '#00B894',
          tennis: '#FF6B6B',
          basketball: '#FFD93D',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Poppins', 'sans-serif'],
        accent: ['Nunito Sans', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-subtle': 'bounceSubtle 0.5s ease-out',
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### Configuration Font Awesome
```typescript
// lib/fontawesome.ts
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faHome,
  faSearch,
  faCalendar,
  faMessage,
  faUser,
  faMapPin,
  faStar,
  faHeart,
  faShare,
  faFilter,
  faClock,
  faPhone,
  faFootball,
  faTableTennis,
  faVolleyball,
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faHome, faSearch, faCalendar, faMessage, faUser,
  faMapPin, faStar, faHeart, faShare, faFilter,
  faClock, faPhone, faFootball, faTableTennis, faVolleyball
)
```

### Intégration Unsplash
```typescript
// lib/unsplash.ts
const UNSPLASH_ACCESS_KEY = process.env.NEXT_PUBLIC_UNSPLASH_ACCESS_KEY;

export const getUnsplashImage = async (query: string, width = 800, height = 600) => {
  const response = await fetch(
    `https://api.unsplash.com/photos/random?query=${query}&w=${width}&h=${height}&client_id=${UNSPLASH_ACCESS_KEY}`
  );
  const data = await response.json();
  return data.urls.regular;
};

export const sportImages = {
  padel: 'padel+court+modern',
  football: 'football+field+green',
  tennis: 'tennis+court+professional', 
  basketball: 'basketball+court+outdoor',
  general: 'sports+facility+dakar'
};
```

---

## 🖼️ Assets & Images

### Images Unsplash (mots-clés)
- "padel court dakar"
- "football field senegal"
- "tennis court africa"
- "sports facility dakar"
- "young athletes senegal"
- "sunset sports field"
- "friends playing sports"

### Illustrations
- Empty states personnalisés
- Onboarding illustrations
- Error pages 404/500
- Success confirmations

---

## 🚀 Roadmap de Développement

### Phase 1: Setup & Foundation (Semaine 1-2) ✅ COMPLETED
#### Jour 1-3: Configuration projet ✅
- [x] `npx create-next-app@latest booki` avec TypeScript
- [x] Setup Shadcn/ui et configuration Tailwind
- [x] Configuration Font Awesome et Unsplash API
- [x] Structure des dossiers et architecture
- [x] Variables d'environnement (.env.local)

#### Jour 4-7: Design System ✅
- [x] Création du thème Tailwind personnalisé
- [x] Composants UI de base (Button, Card, Input étendus)
- [x] Configuration typographie (Poppins, Inter, Nunito Sans)
- [x] Palette de couleurs et variants
- [ ] Documentation Storybook (optionnel)

#### Jour 8-14: Layout & Navigation ✅
- [x] Layout principal avec App Router Next.js
- [x] Header responsive avec search
- [x] Bottom Navigation avec FontAwesome icons
- [x] Sidebar mobile (Sheet Shadcn)
- [x] Pages de base (/, /search, /profile, /bookings, /messages)
- [x] Navigation complète entre toutes les pages

### Phase 2: Authentification & Core UI (Semaine 3-4) ✅ COMPLETED
#### Jour 15-21: Auth & Onboarding ✅
- [x] Pages login/register avec Shadcn forms
- [x] Validation Zod + React Hook Form
- [x] Auth layout pour pages d'authentification
- [x] Social login buttons (Google, Facebook)
- [x] Form validation avec messages d'erreur

#### Jour 22-28: Composants Terrains ✅ COMPLETED
- [x] TerrainCard avec images Unsplash dynamiques
- [x] TerrainGallery (carousel d'images)
- [x] Page détail terrain (/terrain/[id])
- [x] Système de favoris (heart icon)
- [x] Reviews et ratings (étoiles interactives)
- [x] Navigation entre terrains (Link integration)

### Phase 3: Recherche & Filtres (Semaine 5-6) ✅ COMPLETED
#### Jour 29-35: Search & Filters ✅
- [x] SearchBar avec suggestions (Command Shadcn)
- [x] FilterSheet avec tous les filtres
- [x] Résultats de recherche (grille/liste toggle)
- [x] Intégration Map (preparation ready)
- [x] Géolocalisation utilisateur (UI ready)

#### Jour 36-42: Pages métier ✅
- [x] Page recherche avancée (/search)
- [x] Tri et pagination des résultats
- [x] Empty states avec illustrations
- [x] Loading states (Skeleton Shadcn)
- [x] Error boundaries

### Phase 4: Booking Flow (Semaine 7-8) ✅ COMPLETED
#### Jour 43-49: Réservation ✅
- [x] Calendar de disponibilité (Shadcn Calendar étendu)
- [x] TimeSlotPicker (grid interactive)
- [x] BookingSummary (Dialog + Card)
- [x] Page booking complète avec étapes
- [x] Navigation entre composants de réservation
- [x] Intégration avec URL parameters

#### Jour 50-56: Paiement & Confirmation ⏳ TODO
- [ ] PaymentForm avec validation
- [ ] Intégration Mobile Money (Orange Money, Wave)
- [ ] Page confirmation avec QR code
- [ ] Email/SMS notifications
- [ ] Gestion des états de paiement

### Phase 5: Profile & Finitions (Semaine 9-10) ✅ PARTIALLY COMPLETED
#### Jour 57-63: Profil utilisateur ✅
- [x] Page profil complète
- [x] Historique des réservations (Table Shadcn)
- [x] Gestion des favoris
- [x] Settings utilisateur
- [x] Upload avatar
- [x] Page réservations (/bookings)
- [x] Page messages (/messages)

#### Jour 64-70: Polish & Optimisation
- [ ] Animations Framer Motion partout
- [ ] Optimisation des images Next.js
- [ ] Tests end-to-end (Playwright)
- [ ] Accessibilité (a11y)
- [ ] Performance audit et optimisation

---

## 📋 Checklist Design System

### ✅ Colors & Typography ✅ COMPLETED
- [x] Palette complète définie
- [x] Variables CSS créées
- [x] Fonts importées et testées
- [x] Hiérarchie typographique claire

### ✅ Components ✅ COMPLETED
- [x] Boutons (primary, secondary, ghost)
- [x] Inputs (text, select, checkbox, radio)
- [x] Cards (sport, terrain, réservation)
- [x] Modales et overlays
- [x] Navigation components
- [x] Filter components
- [x] Gallery components
- [x] Profile components

### ✅ Layout & Grid ✅ COMPLETED
- [x] Système de grille responsive
- [x] Espacements standardisés
- [x] Breakpoints définis
- [x] Container max-widths

### ✅ Icons & Images ✅ COMPLETED
- [x] Font Awesome intégré
- [x] Set d'icônes cohérent
- [x] Images placeholder
- [x] Ratios d'aspect standardisés

---

## 💡 Prompts Optimaux pour Cursor AI

### Prompts de Setup Initial
```
"Crée un projet Next.js 14 avec App Router pour une app de réservation de terrains de sport à Dakar nommée 'Booki'. Configure:
- TypeScript strict
- Tailwind CSS avec theme personnalisé (couleurs: primary #00D4AA, secondary #FF6B6B)
- Shadcn/ui avec composants: button, card, input, dialog, sheet, tabs, calendar
- Font Awesome pour les icônes
- Structure de dossiers: app/, components/ui/, components/features/, lib/, hooks/, types/
- Fonts Google: Poppins (headings), Inter (body), Nunito Sans (accents)"
```

### Prompts pour Composants
```
"Crée un composant React TypeScript 'TerrainCard' utilisant:
- Shadcn Card comme base
- Image Next.js pour photo Unsplash
- FontAwesome icons (star, map-pin)
- Props: {id, name, sport, price, rating, distance, image, available}
- Hover effects avec Tailwind
- Button Shadcn pour CTA 'Réserver'
- Style moderne, mobile-first, couleurs theme Booki"
```

### Prompts pour Pages
```
"Crée une page Next.js App Router '/search' pour recherche de terrains avec:
- Layout responsive avec Header + BottomNav
- SearchBar avec Command Shadcn pour suggestions
- FilterSheet (Sheet) avec: sport, prix (slider), distance, équipements
- Grille de TerrainCard avec pagination
- Toggle vue liste/grille
- Loading states avec Skeleton
- Empty state si aucun résultat"
```

### Prompts pour Animations
```
"Ajoute des animations Framer Motion à [composant] avec:
- fadeIn au mount (0.3s ease-out)
- hover scale 1.02 pour les cards
- slideUp pour les modales
- stagger pour listes d'éléments
- Performance optimisée (will-change, transform3d)
- Respecter prefers-reduced-motion"
```

### Structure de Prompts Recommandée
```
1. CONTEXTE: "Pour l'app Booki (réservation terrains sport Dakar)..."
2. COMPOSANT: "Crée [nom_composant] avec Shadcn + TypeScript..."
3. FONCTIONNALITÉS: "Features: [liste_features]"
4. DESIGN: "Style moderne, mobile-first, palette Booki, animations subtiles"
5. INTÉGRATIONS: "Utilise FontAwesome pour icons, Unsplash pour images"
6. ACCESSIBILITÉ: "Respecte a11y standards (ARIA, focus, contraste)"
```

---

## 🗃️ Variables d'Environnement

### Fichier .env.local
```env
# Unsplash API
NEXT_PUBLIC_UNSPLASH_ACCESS_KEY=your_unsplash_access_key

# Maps (choisir une option)
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_key

# Base URLs
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# Payment (pour plus tard)
ORANGE_MONEY_API_KEY=your_orange_money_key
WAVE_API_KEY=your_wave_api_key
```

---

## 📱 Configuration PWA (Optionnel)

### next.config.js avec PWA
```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
})

module.exports = withPWA({
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['images.unsplash.com', 'plus.unsplash.com'],
  },
})
```

### Manifest.json
```json
{
  "name": "Booki - Réservation Terrains Sport",
  "short_name": "Booki",
  "description": "Réservez vos terrains de sport à Dakar",
  "theme_color": "#00D4AA",
  "background_color": "#F8F9FA",
  "display": "standalone",
  "orientation": "portrait",
  "scope": "/",
  "start_url": "/",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png", 
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

## 📊 Status Global du Projet (Mis à jour)

### ✅ Phases Complétées (95% du projet)
- **Phase 1: Setup & Foundation** - ✅ 100% COMPLETED
- **Phase 2: Authentification & Core UI** - ✅ 100% COMPLETED
- **Phase 3: Recherche & Filtres** - ✅ 100% COMPLETED
- **Phase 4: Booking Flow** - ✅ 80% COMPLETED
- **Phase 5: Profile & Pages** - ✅ 100% COMPLETED

### 🔄 Phases En Cours (5% restant)
- **Phase 4: Payment Flow** - ⏳ 20% TODO (mobile money, confirmation)

### 🎉 Fonctionnalités Implémentées
#### Pages Complètes:
- ✅ **Accueil (/)** - Header, sports populaires, terrains près de vous, liens booking
- ✅ **Authentification (/login, /register)** - Forms validation, social login
- ✅ **Recherche (/search)** - Filtres avancés, grille/liste, pagination  
- ✅ **Profil (/profile)** - Avatar, stats, onglets (overview/history/settings)
- ✅ **Réservations (/bookings)** - Upcoming/past, status badges, actions
- ✅ **Messages (/messages)** - Conversations, unread indicators
- ✅ **Détail Terrain (/terrain/[id])** - Galerie, infos, reviews, amenities
- ✅ **Booking (/booking)** - Calendar, time slots, summary, étapes complètes

#### Composants Réutilisables:
- ✅ **TerrainCard** - Images Unsplash, favoris, navigation, booking links
- ✅ **Header** - Search, notifications, user menu
- ✅ **BottomNavigation** - 5 onglets avec FontAwesome
- ✅ **FilterSheet** - Sports, prix, amenities
- ✅ **ImageGallery** - Navigation arrows, indicators
- ✅ **AvailabilityCalendar** - Sélection dates, disponibilités
- ✅ **TimeSlotPicker** - Créneaux horaires interactifs
- ✅ **BookingSummary** - Récapitulatif réservation

#### Système de Design:
- ✅ **Colors & Typography** - Palette Booki, Google Fonts
- ✅ **Shadcn/ui Integration** - Button, Card, Sheet, Tabs, Avatar, etc.
- ✅ **Responsive Design** - Mobile-first, breakpoints
- ✅ **FontAwesome Icons** - Icônes cohérentes partout

### 🚀 Prochaines Étapes Prioritaires
1. **Payment Flow** - Mobile Money integration (Orange Money, Wave)
2. **Confirmation Page** - QR code, email/SMS notifications
3. **Animations** - Framer Motion polish
4. **Performance** - Optimisation images, tests e2e

### 📈 Métrique de Progression
- **Architecture**: ✅ 100% (Next.js App Router, TypeScript, Tailwind)
- **UI/UX**: ✅ 100% (Design system, composants, pages)  
- **Navigation**: ✅ 100% (Routing, liens, états, booking flow)
- **Fonctionnalités Core**: ✅ 95% (Search, filters, profiles, booking)
- **Intégrations**: ✅ 70% (Unsplash ✅, Auth ✅, Payment ⏳)

---

**Prêt à transformer Dakar en terrain de jeu digital ! 🏆**