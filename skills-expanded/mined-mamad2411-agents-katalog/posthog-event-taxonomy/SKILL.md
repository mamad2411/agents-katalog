---
name: posthog-event-taxonomy
description: >
  Canonical event names and properties for all PostHog analytics in KairoFit.
  Use this skill when: adding any analytics tracking call, implementing PostHog
  event capture, building retention tracking, implementing the paywall flow,
  or adding new user interactions that should be measured. Analytics debt compounds
  quickly - inconsistent event names across the codebase make cohort analysis
  impossible. This taxonomy must be used for all events. Never type raw event
  name strings in components.
---

# PostHog Event Taxonomy

## Setup

```typescript
// src/lib/utils/analytics.ts
import posthog from 'posthog-js'
import { EVENTS } from './event-names'

export function track(event: keyof typeof EVENTS, properties?: Record<string, unknown>) {
  posthog.capture(EVENTS[event], properties)
}

// Usage in components - never use raw strings
// track('FIRST_WORKOUT_COMPLETED', { duration_minutes: 45 })
```

## Event Names (SCREAMING_SNAKE_CASE)

```typescript
// src/lib/utils/event-names.ts
export const EVENTS = {
  // ============================================================
  // ONBOARDING FUNNEL (critical for conversion tracking)
  // ============================================================
  ONBOARDING_STARTED: 'ONBOARDING_STARTED',
  ONBOARDING_STEP_COMPLETED: 'ONBOARDING_STEP_COMPLETED',
  ONBOARDING_STEP_SKIPPED: 'ONBOARDING_STEP_SKIPPED',
  EMAIL_GATE_REACHED: 'EMAIL_GATE_REACHED', // Screen 16
  EMAIL_GATE_SUBMITTED: 'EMAIL_GATE_SUBMITTED',
  EMAIL_GATE_ABANDONED: 'EMAIL_GATE_ABANDONED', // Left before submitting
  ARCHETYPE_REVEALED: 'ARCHETYPE_REVEALED', // Screen 15
  ONBOARDING_COMPLETED: 'ONBOARDING_COMPLETED', // Screen 22 done

  // ============================================================
  // PROGRAM GENERATION
  // ============================================================
  PROGRAM_GENERATION_STARTED: 'PROGRAM_GENERATION_STARTED',
  PROGRAM_GENERATION_COMPLETED: 'PROGRAM_GENERATION_COMPLETED',
  PROGRAM_GENERATION_FAILED: 'PROGRAM_GENERATION_FAILED',
  PROGRAM_ADJUSTED: 'PROGRAM_ADJUSTED',
  EXERCISE_SWAPPED: 'EXERCISE_SWAPPED',

  // ============================================================
  // WORKOUT SESSIONS (most important retention signals)
  // ============================================================
  WORKOUT_STARTED: 'WORKOUT_STARTED',
  FIRST_WORKOUT_STARTED: 'FIRST_WORKOUT_STARTED', // Day 1 retention
  SET_LOGGED: 'SET_LOGGED',
  WORKOUT_COMPLETED: 'WORKOUT_COMPLETED',
  FIRST_WORKOUT_COMPLETED: 'FIRST_WORKOUT_COMPLETED', // Day 1 completion
  WORKOUT_ABANDONED: 'WORKOUT_ABANDONED', // Started but did not finish

  // ============================================================
  // KIRO AI INTERACTIONS
  // ============================================================
  AI_GENERATION_STARTED: 'AI_GENERATION_STARTED',
  AI_GENERATION_COMPLETED: 'AI_GENERATION_COMPLETED',
  AI_GENERATION_FAILED: 'AI_GENERATION_FAILED',
  KIRO_DEBRIEF_VIEWED: 'KIRO_DEBRIEF_VIEWED',
  KIRO_DEBRIEF_DISMISSED: 'KIRO_DEBRIEF_DISMISSED',
  WORKOUT_RATED: 'WORKOUT_RATED', // 1-5 star rating

  // ============================================================
  // RETENTION SIGNALS
  // ============================================================
  APP_OPENED: 'APP_OPENED',
  STREAK_MAINTAINED: 'STREAK_MAINTAINED',
  STREAK_BROKEN: 'STREAK_BROKEN',
  DELOAD_WEEK_STARTED: 'DELOAD_WEEK_STARTED',
  PERSONAL_RECORD_SET: 'PERSONAL_RECORD_SET',

  // ============================================================
  // PAYWALL (gated, fires when PAYWALL_ENABLED=true)
  // ============================================================
  PAYWALL_SHOWN: 'PAYWALL_SHOWN',
  PAYWALL_DISMISSED: 'PAYWALL_DISMISSED',
  SUBSCRIPTION_STARTED: 'SUBSCRIPTION_STARTED',
  SUBSCRIPTION_CANCELED: 'SUBSCRIPTION_CANCELED',
  TRIAL_EXPIRED: 'TRIAL_EXPIRED',

  // ============================================================
  // SOCIAL
  // ============================================================
  WORKOUT_SHARED: 'WORKOUT_SHARED',
  USER_FOLLOWED: 'USER_FOLLOWED',
  CHALLENGE_JOINED: 'CHALLENGE_JOINED',
} as const
```

## Standard Properties (include on ALL events)

These properties should be set as PostHog user properties on signup,
then automatically included in every event:

```typescript
// Set once on profile creation, then PostHog includes automatically
posthog.identify(userId, {
  archetype: profile.archetype,
  experience_level: profile.experience_level,
  goal: profile.goal,
  days_per_week: profile.days_per_week,
  has_injuries: profile.injuries.length > 0,
  subscription_status: profile.subscription_status,
})
```

## Key Event Properties

```typescript
// ONBOARDING_STEP_COMPLETED
{
  step: number,           // 1-22
  step_id: string,        // 'goal', 'injuries', etc.
  phase: number,          // 1-5
  time_spent_seconds: number,
}

// WORKOUT_COMPLETED
{
  duration_minutes: number,
  total_sets: number,
  total_volume_kg: number,
  exercise_swap_count: number,   // proxy for AI recommendation quality
  perceived_effort: number,      // 1-10
  is_first_workout: boolean,
}

// AI_GENERATION_COMPLETED
{
  model: string,          // 'claude-sonnet-4-...'
  generation_ms: number,  // latency
  cached: boolean,        // whether prompt cache hit
  input_tokens: number,
  output_tokens: number,
}

// EXERCISE_SWAPPED (key quality metric - target < 15% swap rate)
{
  original_exercise: string,
  replacement_exercise: string,
  reason: string,         // user-provided or 'no_reason_given'
  session_position: number, // which exercise in the session (1-N)
}
```

## Key Metrics to Monitor (from the research doc)

| Metric                  | Target | PostHog Query                             |
| ----------------------- | ------ | ----------------------------------------- |
| Day 1 retention         | 35-45% | Users who opened app day after signup     |
| Day 7 retention         | 20-30% | Users who opened app 7 days after signup  |
| Workout completion rate | >70%   | WORKOUT_COMPLETED / WORKOUT_STARTED       |
| Exercise swap rate      | <15%   | EXERCISE_SWAPPED / total exercises shown  |
| Email gate conversion   | >60%   | EMAIL_GATE_SUBMITTED / EMAIL_GATE_REACHED |
| Onboarding completion   | >80%   | ONBOARDING_COMPLETED / ONBOARDING_STARTED |
