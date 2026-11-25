## Project Overview

We are creating a mockup site to ideate over user stories, discuss features, gather ideas, and generally work on building the ground work for our new site, Tech Central.

We have a folder `/html` where we started creating this site. We have now moved over to `/app` where we are creating our SvelteKit & Svelte 5 version of our site.

Your job is to keep everything in `/html` the same as it is. Only use it for reference. We're going to start by copying over pages, components, and elements into our `/app` SvelteKit app.

In the SvelteKit app, when we need to model fetching some data/content from the site, let's use the api routes to do this. We'll build it like we're building a real site that fetches data from a backend. The real site will ultimately be fetching content from a CMS at some point in the future, but not for our mockup site. The mockup will only fetch static content that we will get from the api routes.

## Event Handling

### ❌ Don't use `createEventDispatcher`

```typescript
// DEPRECATED - Don't do this
import { createEventDispatcher } from 'svelte'
const dispatch = createEventDispatcher<{
  someEvent: { data: string }
}>()
dispatch('someEvent', { data: 'value' })
```

### ✅ Do use props for event handling

```typescript
// CORRECT - Do this instead
export let onSomeEvent: (event: { data: string }) => void

// In your component logic
onSomeEvent({ data: 'value' })

// In the parent component
;<MyComponent onSomeEvent={handleSomeEvent} />
```

### Why?

- `createEventDispatcher` is deprecated in Svelte 5
- Props provide better type safety and clearer component interfaces
- Props make it easier to test and mock event handlers
- Props follow a more standard React-like pattern that's familiar to many developers

### Benefits of the new approach:

1. TypeScript support out of the box
2. Better IDE autocompletion
3. Clearer component API
4. More predictable behavior
5. Easier to test and maintain

## `aria` Rules for Buttons and Links

Buttons and links should either contain text or have an `aria-label` or `aria-labelledby` attribute
https://svelte.dev/e/a11y_consider_explicit_label

## Accessibility Rules

### Click Event Handling

- Visible, non-interactive elements with a click event must be accompanied by a keyboard event handler
- Consider using interactive elements like `<button type="button">` or `<a>` instead of divs with click handlers
- When using `<div>` elements with click handlers, they must have an appropriate ARIA role

### Examples

```typescript
// ❌ Don't do this
<div on:click={handleClick}>Click me</div>

// ✅ Do this instead
<button type="button" on:click={handleClick} on:keydown={handleKeydown}>Click me</button>

// If you must use a div, add appropriate ARIA role and keyboard handling
<div
  role="button"
  tabindex="0"
  on:click={handleClick}
  on:keydown={handleKeydown}
>
  Click me
</div>
```

### Why?

- Ensures keyboard accessibility for all interactive elements
- Makes the site usable for users who rely on keyboard navigation
- Improves overall accessibility compliance
- Makes the code more semantic and maintainable

## SvelteKit Store Usage

### Page Store

- The `page` store from `$app/stores` is deprecated
- Use `page` from `$app/state` instead
- This change is required for current SvelteKit compatibility
- When using `page` from `$app/state`, access it directly without the `$` prefix
- Use reactive declarations to track page changes

### Examples

```typescript
// ❌ Don't do this
import { page } from '$app/stores'
$: currentPath = $page.url.pathname

// ✅ Do this instead
import { page } from '$app/state'
$: currentPath = page.url.pathname
```

### Why?

- Ensures current SvelteKit compatibility
- Follows the latest SvelteKit best practices
- Prevents deprecation warnings
- Maintains consistent store usage across the application
- Provides proper reactivity with the new page API

# Tech Central Route Structure and Content Organization

## Main Navigation Tabs

### Learning Hub (/learning-hub)

- Primary purpose: Job aids and documentation for field technicians
- Content types:
  - Troubleshooting guides
  - Installation procedures
  - Technical documentation
  - Field reference materials
  - Hardware business rules
  - Equipment handling guides
  - Safety protocols
- Example routes:
  - `/learning-hub/installation-guides`
  - `/learning-hub/troubleshooting`
  - `/learning-hub/hardware-rules`
  - `/learning-hub/device-library`
  - `/learning-hub/equipment-safety`
  - `/learning-hub/technical-specs`
  - `/learning-hub/network-topology`
  - `/learning-hub/qa-checklists`

### ValueGen (/valuegen)

- Primary purpose: Deals, promotions, and customer offers
- Content types:
  - Current promotions
  - Special offers
  - Deal qualification guides
  - Customer benefit documentation
  - Regional offers
  - Language-specific content
  - Sales investigation tracking
- Example routes:
  - `/valuegen/current-offers`
  - `/valuegen/promotions-calendar`
  - `/valuegen/incentive-rates`
  - `/valuegen/qualification-guides`
  - `/valuegen/regional-offers`
  - `/valuegen/alerts`
  - `/valuegen/sales-investigations`
  - `/valuegen/solicitation-policy`

### Billing/PSB (/billing)

- Primary purpose: Professional Services Billing documentation
- Content types:
  - Billing procedures
  - Rate cards
  - Invoice templates
  - Billing guidelines
  - Regional billing rules
  - Skill-specific billing
  - Repair billing guidelines
- Example routes:
  - `/billing/quick-guide`
  - `/billing/procedures`
  - `/billing/rate-cards`
  - `/billing/guidelines`
  - `/billing/regional-rules`
  - `/billing/repair-guidelines`
  - `/billing/skill-specific`
  - `/billing/updates`

### Partners (/partners)

- Primary purpose: Resources for Telus partners and subcontractors
- Content types:
  - Partner-specific job aids
  - Service documentation
  - Partner guidelines
  - Contract information
  - Partner training materials
  - Partner performance metrics
- Example routes:
  - `/partners/job-aids`
  - `/partners/guidelines`
  - `/partners/contracts`
  - `/partners/training`
  - `/partners/performance`
  - `/partners/onboarding`

### Training (/training)

- Primary purpose: Training materials and learning resources
- Content types:
  - Training modules
  - Learning materials
  - Certification guides
  - Skill development resources
  - Learning paths
  - Training calendar
  - Mentorship program
- Example routes:
  - `/training/learning-paths`
  - `/training/modules`
  - `/training/certifications`
  - `/training/calendar`
  - `/training/onboarding`
  - `/training/knowledge-checks`
  - `/training/mentorship`
  - `/training/compliance`

### Managers (/managers)

- Primary purpose: Field management resources
- Content types:
  - Management dashboards
  - Performance metrics
  - Team management tools
  - Field operations guides
  - Training management
  - Certification tracking
  - Team scheduling
- Example routes:
  - `/managers/dashboard`
  - `/managers/metrics`
  - `/managers/team-tools`
  - `/managers/scheduling`
  - `/managers/training-management`
  - `/managers/certifications`
  - `/managers/access-requests`
  - `/managers/reports`

## URL Structure Rules

1. Use kebab-case for all URLs
2. Keep URLs descriptive but concise
3. Use plural nouns for resource collections
4. Use singular nouns for specific resources
5. Include version numbers in URLs when applicable (e.g., `/training/fiber-installation-v2`)

## Content Organization Rules

1. Each section should have a clear, distinct purpose
2. Content should be organized hierarchically
3. Related content should be cross-linked when appropriate
4. Each section should have its own navigation structure
5. Content should be tagged with appropriate metadata for filtering and search

## Mockup Development Rules

1. All routes should be functional in the mockup
2. Use static data for mockup development
3. Structure data to match future CMS integration
4. Include loading states and error handling
5. Maintain consistent UI patterns across sections

## Svelte 5 Event Handling

### Event Handlers

In Svelte 5, event handlers are properties rather than directives:

```typescript
// ❌ Don't do this (Svelte 4 style)
<button on:click={handleClick}>Click me</button>

// ✅ Do this instead (Svelte 5 style)
<button onclick={handleClick}>Click me</button>
```

### Component Events

For component events, use callback props instead of `createEventDispatcher`:

```typescript
// ❌ Don't do this (Svelte 4 style)
import { createEventDispatcher } from 'svelte'
const dispatch = createEventDispatcher()
dispatch('event', data)

// ✅ Do this instead (Svelte 5 style)
export let onEvent: (data: any) => void
onEvent(data)
```

### $derived vs $effect

Use $derived for computed values and $effect for side effects:

```typescript
// ❌ Don't do this
$effect(() => {
  doubledCount = count * 2 // Computing values in an effect
})

// ✅ Do this instead
const doubledCount = $derived(count * 2)

// ✅ Use $effect only for side effects
$effect(() => {
  localStorage.setItem('count', count.toString())
  document.title = `Count: ${count}`
})
```

### Rules of thumb:

1. If you're calculating a value based on other state, use $derived
2. If you're performing side effects (DOM manipulation, API calls, etc.), use $effect
3. Never modify state inside a $derived calculation
4. Keep $effect functions focused on side effects only
