---
name: component-generator
description: Use this skill when creating a new React component. It provides the exact file template, prop typing rules, and patterns to follow for client and server components in this project.
---

# Component Generator — Hair Salon Booking App

## Rules
- Max 150 lines per component — split if exceeded
- One component per file
- Always type props explicitly — no implicit `any`
- Prefer Server Components by default — add `'use client'` only when needed

## When to use `'use client'`
- Component uses `useState`, `useEffect`, `useRef`
- Component handles user events (onClick, onChange…)
- Component uses a browser API

---

## Server Component Template
```tsx
// components/ui/booking-card.tsx

import type { Booking } from '@/types/booking'

interface BookingCardProps {
  booking: Booking
  className?: string
}

export function BookingCard({ booking, className }: BookingCardProps) {
  return (
    <div className={className}>
      {/* content */}
    </div>
  )
}
```

## Client Component Template
```tsx
// components/ui/time-slot-picker.tsx
'use client'

import { useState } from 'react'

interface TimeSlotPickerProps {
  slots: string[]
  onSelect: (slot: string) => void
}

export function TimeSlotPicker({ slots, onSelect }: TimeSlotPickerProps) {
  const [selected, setSelected] = useState<string | null>(null)

  function handleSelect(slot: string) {
    setSelected(slot)
    onSelect(slot)
  }

  return (
    <div>
      {slots.map((slot) => (
        <button
          key={slot}
          onClick={() => handleSelect(slot)}
          className={selected === slot ? 'bg-black text-white' : 'bg-white'}
        >
          {slot}
        </button>
      ))}
    </div>
  )
}
```

---

## Forbidden Patterns
```tsx
// ❌ No default exports for components
export default function BookingCard() {}

// ❌ No untyped props
export function BookingCard(props: any) {}

// ❌ No inline styles
<div style={{ color: 'red' }} />

// ❌ No prop spreading without type guard
<div {...props} />
```

## Tailwind Class Guidelines
- Use semantic grouping: layout → spacing → typography → color → state
- Extract repeated class combinations into a variable if used 3+ times
```tsx
const baseButtonClass = 'rounded-lg px-4 py-2 text-sm font-medium transition-colors'
```
