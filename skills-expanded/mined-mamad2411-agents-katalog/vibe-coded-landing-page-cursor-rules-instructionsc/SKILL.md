---
description: 
globs: 
alwaysApply: false
---
# Technical Specification - Loan Lending Platform Landing Page

## Overview
This technical specification details the implementation approach for a minimalist, high-impact landing page for a loan lending platform inspired by CRED. This document translates the PRD requirements into technical details and implementation guidelines.

## Technology Stack

### Core Technologies
- **Framework**: Next.js 15.0.0+ with Static Site Generation (SSG)
- **Animation Library**: GSAP 3.13.0+ (GreenSock Animation Platform)
- **Styling**: Tailwind CSS (latest stable version)
- **Package Manager**: npm/yarn

### Supporting Libraries
- **Form Validation**: React Hook Form with Zod schema validation
- **Typography**: Roboto Flex (optimized via Next.js Font optimization)
- **Icons**: Lucide React (exclusively)
- **Image Optimization**: Next.js Image component for automatic optimization

## Project Structure

```
/
├── app/                        # App Router (Next.js 15+)
│   ├── layout.tsx              # Root layout with global fonts and providers
│   ├── page.tsx                # Landing page (/) route
│   ├── globals.css             # Global styles and Tailwind imports
│   └── favicon.ico             # Site favicon
├── components/
│   ├── layout/
│   │   ├── Header.tsx          # Navigation and logo
│   │   ├── Footer.tsx          # Site footer with links and legal info
│   │   └── Layout.tsx          # Wrapping layout component
│   ├── sections/
│   │   ├── Hero.tsx            # Hero section with GSAP animations
│   │   ├── Features.tsx        # Features grid with staggered reveals
│   │   ├── HowItWorks.tsx      # Process timeline with step animations
│   │   ├── Testimonials.tsx    # Testimonial carousel
│   │   ├── Benefits.tsx        # Comparison section
│   │   └── CtaSection.tsx      # Final call-to-action with form
├── hooks/
├── constants/
│   ├── features.ts             # Feature data (title, desc, icon)
│   ├── testimonials.ts         # Customer testimonials
│   ├── process-steps.ts        # How it works data
│   ├── benefits.ts             # Platform benefits data
│   └── navigation.ts           # Navigation links
├── lib/
│   ├── utils.ts                # Utility functions
│   └── animation.ts            # Animation helper functions
├── public/
│   └── images/
│       ├── hero/
│       ├── features/
│       ├── testimonials/
│       └── benefits/
├── types/
│   └── index.ts                # TypeScript type definitions
├── next.config.ts              # Next.js configuration
├── tsconfig.json               # TypeScript configuration
└── package.json
```

## Detailed Component Specifications

### Layout Components

#### Header.jsx
```javascript
// Component responsibilities:
// - Fixed navigation bar with logo
// - Navigation links (Home, Features, How it Works, etc.)
// - CTA button
// - Mobile responsive hamburger menu
// - Background changes on scroll (transparent to solid)
```

**Implementation Details:**
- Use `useState` and `useEffect` to track scroll position
- Implement smooth transition for background change
- Use Tailwind's responsive utilities for mobile menu

#### Footer.jsx
```javascript
// Component responsibilities:
// - Logo and company info
// - Navigation links
// - Social media links
// - Legal links (Privacy Policy, Terms)
// - Copyright information
```

### Section Components

#### Hero.jsx
```javascript
// Component responsibilities:
// - Full viewport height section with gradient background
// - Animated headline with text reveal
// - Floating 3D credit card with mouse tracking
// - Primary CTA button
// - Brief value proposition text
```

**Implementation Details:**
- GSAP timeline for coordinated animations:
  - Text reveal animation (staggered letters/words)
  - Card float-in animation
- Mouse move event listener for parallax effect on card
- Responsive layout adjustments for mobile

**Animation Sequence:**
1. Background gradient subtle pulse (continuous)
2. Headline text reveal animation (on load)
3. Credit card scale and fade in (after headline)
4. CTA button fade and scale (after card animation)

#### Features.jsx
```javascript
// Component responsibilities:
// - Grid layout of feature cards
// - Each card contains icon, title, and brief description
// - Staggered reveal animations on scroll
```

**Implementation Details:**
- Map through features from constants file
- Use GSAP ScrollTrigger for triggering animations
- Implement staggered reveal with opacity and Y-position transform
- Responsive grid (1 column mobile, 2 tablet, 3-4 desktop)

#### HowItWorks.jsx
```javascript
// Component responsibilities:
// - 3-step process visualization
// - Horizontal timeline with connections
// - Animated transitions between steps
// - Illustrations for each step
```

**Implementation Details:**
- GSAP timeline triggered by ScrollTrigger
- Draw line animation connecting steps
- Step cards with staggered reveal
- Position indicators (numbers) with fill animation

#### Testimonials.jsx
```javascript
// Component responsibilities:
// - Testimonial carousel/slider
// - Auto-rotation with manual controls
// - Customer photos, names, and quotes
// - Trust metrics display
```

**Implementation Details:**
- GSAP for smooth transitions between slides
- Auto-rotation using setInterval with pause on hover/focus
- Simple dot navigation
- Responsive design for mobile viewing

#### Benefits.jsx
```javascript
// Component responsibilities:
// - Split layout comparing traditional loans vs platform
// - Animated data points and metrics
// - Visual elements highlighting differences
```

**Implementation Details:**
- Side-by-side comparison for desktop
- Stacked comparison for mobile
- Counter animations for metrics (using GSAP)
- Visual highlights on key differentiators

#### CtaSection.tsx
```typescript
// Component responsibilities:
// - Final call-to-action with simplified signup
// - Background with subtle animation
// - Trust indicators and badges
```

**Implementation Details:**
- Form with minimal fields (email/phone)
- React Hook Form with Zod schema validation
- TypeScript interfaces for form data
- Success/error states with animations
- GSAP for background subtle movements

### UI Components

#### Button.tsx
```typescript
// Reusable button component with props:
// - variant: 'primary', 'secondary', 'outline'
// - size: 'sm', 'md', 'lg'
// - fullWidth: boolean
// - withIcon: boolean + icon component
// - animation: type of hover animation
```

**Implementation Details:**
- Tailwind classes using the theme colors (#059669 for primary, etc.)
- GSAP for hover animations
- Loading state with spinner
- Accessibility attributes
- TypeScript props interface

#### AnimatedText.jsx
```javascript
// Text component with animation capabilities:
// - Split text into chars/words/lines
// - Various animation types (fade, slide, etc.)
// - Control for animation timing
```

**Implementation Details:**
- SplitText GSAP plugin for character/word splitting
- GSAP timeline for coordinated animations
- Props for customization of animation style

#### FloatingCard.jsx
```javascript
// 3D credit card component:
// - Perspective transform based on mouse position
// - Subtle continuous floating animation
// - Light reflections and highlights
```

**Implementation Details:**
- CSS 3D transforms with Tailwind
- GSAP for continuous floating animation
- Mouse position calculation for perspective shift

## Animation Strategy

### GSAP Implementation

#### Custom Hooks
`useGSAP.ts` will provide a consistent way to implement GSAP animations:

```typescript
import { useEffect, RefObject } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import { SplitText } from 'gsap/dist/SplitText';

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger, SplitText);

type GSAPCallback = (gsapInstance: typeof gsap) => void;

export const useGSAP = (
  callback: GSAPCallback, 
  dependencies: any[] = [], 
  scopeRef?: RefObject<HTMLElement>
) => {
  useEffect(() => {
    // Create a GSAP context for proper cleanup
    let ctx = gsap.context(() => {
      callback(gsap);
    }, scopeRef?.current || null);
    
    // Clean up animations when component unmounts
    return () => ctx.revert();
  }, dependencies);
};
```

#### Animation Types

1. **Text Reveal Animations**
   - Character by character reveal
   - Word by word reveal
   - Line by line reveal with masks

2. **Scroll-Triggered Animations**
   - Fade and slide in from bottom
   - Staggered reveals for lists/grids
   - Parallax effects for depth

3. **Interactive Animations**
   - Button hover effects
   - Card hover tilts
   - Mouse-follow effects

4. **Transition Animations**
   - Section transitions
   - Page load animations
   - Modal/popup animations

## Performance Optimization

### Image Optimization
- Use Next.js Image component with:
  - Proper sizing (responsive sizes)
  - WebP format with fallbacks
  - Lazy loading for below-the-fold images
  - Placeholder blurs for large images

### Animation Performance
- Use `will-change` properties judiciously
- Hardware acceleration for animations (`transform` over position properties)
- Debounce scroll and resize events
- Disable complex animations on mobile devices

### Core Web Vitals Focus
- Optimize Largest Contentful Paint (LCP):
  - Preload hero image using Next.js priority prop
  - Minimize critical CSS with Tailwind's purge optimization
  - Use Next.js Font optimization for Roboto Flex
- Improve Cumulative Layout Shift (CLS):
  - Set explicit image dimensions with Next.js Image component
  - Implement proper font loading strategy
  - Avoid dynamic content insertion above existing content
- Enhance Interaction to Next Paint (INP):
  - Minimize JavaScript execution time
  - Use `requestIdleCallback` for non-critical operations
  - Optimize event handlers with debouncing and throttling

## Responsive Design Strategy

### Breakpoints
Following Tailwind's default breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Mobile-First Approach
- Design core layout for mobile first
- Enhance layouts for larger screens
- Simplify animations on mobile devices

### Specific Mobile Adaptations
- Stack comparison sections
- Single column for features grid
- Reduced motion for animations
- Simplified navigation (hamburger menu)

## Data Management

### Constant Files Structure

#### features.js
```javascript
export const features = [
  {
    id: 'instant-approval',
    title: 'Instant Approval',
    description: 'Get your loan approved in minutes, not days.',
    icon: 'bolt', // Mapped to icon component
    animationDelay: 0.2,
  },
  {
    id: 'low-interest',
    title: 'Low Interest Rates',
    description: 'Enjoy rates lower than traditional banks.',
    icon: 'percentage',
    animationDelay: 0.4,
  },
  // Additional features...
];
```

#### testimonials.js
```javascript
export const testimonials = [
  {
    id: 1,
    name: 'Sarah Johnson',
    role: 'Small Business Owner',
    quote: 'The loan process was incredibly simple and fast. I had funds in my account within 24 hours!',
    image: '/images/testimonials/sarah.jpg',
  },
  // Additional testimonials...
];
```

#### process-steps.js
```javascript
export const processSteps = [
  {
    id: 'apply',
    step: 1,
    title: 'Quick Application',
    description: 'Fill out our simple form in under 2 minutes.',
    icon: 'form',
  },
  // Additional steps...
];
```

## Accessibility Considerations

### Implementation Requirements
- All interactive elements must be keyboard accessible
- Proper ARIA roles and labels on custom components
- Focus management for interactive elements
- Color contrast ratios meeting WCAG AA standards
- Animation pausing for users with reduced motion preference

### Specific Component Requirements
- Navigation: keyboard accessible dropdown
- Forms: proper label associations and error states
- Carousel: keyboard controls and proper ARIA roles
- Animations: respect `prefers-reduced-motion` media query


### Animation References
- CRED's card animations and text reveals
- Apple's smooth scrolling and parallax effects
- Stripe's subtle UI interactions

### Design System Constants

#### Color Palette
```
  primary: '#059669',   // Brand Primary
  text: '#171717',      // Default Font
  subtext: '#737373',   // Subtext Color
  border: '#e5e5e5',    // Neutral Border
  white: '#ffffff',     // White
  background: '#ffffff' // Default Background
```

#### Typography
- Font Family: Roboto Flex (variable font)
- Font implementation via Next.js Font optimization

#### Spacing System
- Following Tailwind's default spacing scale
- Key component spacings defined in design tokens

#### Animation Timing Variables
- Slow: 1.2s
- Default: 0.8s
- Fast: 0.4s
- Micro: 0.2s

### GSAP Animation Examples
```typescript
// Example for Hero section text animation using the useGSAP hook
import { useGSAP } from '@/hooks/useGSAP';
import { useRef } from 'react';
import SplitType from 'split-type';

const Hero = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  useGSAP(() => {
    // Split text for character animation
    const splitText = new SplitType('.hero-title', { types: 'chars' });
    
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.from(splitText.chars, {
      opacity: 0,
      y: 100,
      duration: 1,
      stagger: 0.03
    });

    tl.from(".hero-card", {
      opacity: 0,
      scale: 0.8,
      duration: 1,
      ease: "back.out(1.7)"
    }, "-=0.5");

    tl.from(".hero-cta", {
      opacity: 0,
      y: 20,
      duration: 0.8
    }, "-=0.3");
  }, [containerRef]);

  return (
    <div ref={containerRef} className="bg-background text-text">
      {/* Hero content */}
    </div>
  );
};

```