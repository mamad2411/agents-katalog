---
name: framer-motion-builder
description: "Framer Motion animation library — fade, scale, stagger, scroll-reveal, page transitions. Used in website-builder Actor 4 for production-quality React animations."
allowed-tools: Read, Bash, Write
---

# Framer Motion Builder — Animation System

## Triggers
"framer motion" / "framer animation" / "animate react" / "scroll reveal" / "page transition" / "hover animation" / "stagger animation"

## Setup

```bash
npm install framer-motion
```

## Core Animation Variants (`/lib/animations.ts`)

```tsx
export const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
}

export const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.5 } }
}

export const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.15 } }
}

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.5 } }
}

export const slideInLeft = {
  hidden: { opacity: 0, x: -40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6 } }
}

export const slideInRight = {
  hidden: { opacity: 0, x: 40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6 } }
}
```

## Standard Component Pattern

```tsx
import { motion } from "framer-motion"
import { fadeUp, staggerContainer } from "@/lib/animations"

<motion.section
  variants={staggerContainer}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, margin: "-100px" }}
>
  <motion.h1 variants={fadeUp}>Headline</motion.h1>
  <motion.p variants={fadeUp}>Copy</motion.p>
  <motion.div variants={scaleIn}>Card</motion.div>
</motion.section>
```

## Hover + Tap Interactions

```tsx
<motion.button
  whileHover={{ scale: 1.05, backgroundColor: "#E94560" }}
  whileTap={{ scale: 0.97 }}
  transition={{ duration: 0.2 }}
>
  Click me
</motion.button>
```

## Page Transitions (`/app/layout.tsx`)

```tsx
import { AnimatePresence, motion } from "framer-motion"

export default function RootLayout({ children }) {
  return (
    <AnimatePresence mode="wait">
      <motion.main
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.main>
    </AnimatePresence>
  )
}
```

## Integration

- **Actor 4** in `website-builder` pipeline — applied to every component
- Works with all 21st.dev components (wrap with `motion.*`)
- QA'd by Actor 5 (Kimi K2.6 vision) via Playwright screenshot diff
