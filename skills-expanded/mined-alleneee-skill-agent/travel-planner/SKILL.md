---
name: travel-planner
description: Creates comprehensive travel itineraries with destination analysis, budget planning, transportation, accommodation, and local insights. Use when planning trips, organizing travel schedules, or seeking destination recommendations.
license: MIT
allowed-tools:
  - Bash
  - web_search
  - read_file
  - write_file
---

# Travel Planner

## Overview

Expert travel planning assistant for creating detailed, practical itineraries. Covers destination research, budget optimization, logistics coordination, and cultural preparation.

**Keywords**: travel, itinerary, trip planning, vacation, destination, budget, transportation, accommodation, sightseeing, culture

## Planning Framework

### 1. Trip Profile Analysis

Before planning, gather:

- **Duration**: Total days available
- **Budget**: Total budget and daily limit
- **Travel Style**: Luxury / Mid-range / Budget / Backpacker
- **Interests**: Culture, Nature, Adventure, Food, Shopping, Relaxation
- **Physical Ability**: Walking tolerance, mobility constraints
- **Group Composition**: Solo, Couple, Family with kids, Group

### 2. Destination Research

Analyze each destination for:

- **Best Season**: Weather patterns, peak/off-peak periods
- **Visa Requirements**: Entry rules, document preparation
- **Local Currency**: Exchange rates, payment methods
- **Language**: Common phrases, translation needs
- **Safety**: Travel advisories, local risks
- **Health**: Vaccinations, medical considerations

### 3. Budget Allocation

Recommended distribution:

| Category | Budget % | Notes |
|----------|----------|-------|
| Accommodation | 30-40% | Varies by destination cost |
| Transportation | 20-25% | Flights, local transit |
| Food | 15-20% | Mix of local and familiar |
| Activities | 15-20% | Tours, attractions, experiences |
| Emergency | 10% | Unexpected expenses buffer |

### 4. Daily Itinerary Structure

```
Morning (8:00-12:00)
├── Primary attraction (high energy activity)
├── Travel time buffer: 30min
└── Mid-morning break

Afternoon (12:00-18:00)
├── Lunch (local cuisine recommended)
├── Secondary attractions
├── Flexible exploration time
└── Rest period (especially in hot climates)

Evening (18:00-22:00)
├── Dinner
├── Night activity or leisure
└── Return to accommodation
```

### 5. Pacing Guidelines

- **Maximum 3 major attractions per day**
- **Include 2-3 hours of unplanned time**
- **Build in one "slow day" per 4 days of travel**
- **Account for jet lag (first 1-2 days lighter)**
- **Consider local meal times and siesta cultures**

## Output Format

### Itinerary Template

```markdown
# [Destination] Travel Plan
**Dates**: [Start Date] - [End Date] ([N] days)
**Budget**: [Amount] [Currency]
**Travelers**: [Number and composition]

## Pre-Trip Checklist
- [ ] Passport validity (6+ months)
- [ ] Visa arranged
- [ ] Travel insurance
- [ ] Vaccinations
- [ ] Currency/cards prepared
- [ ] Accommodation booked
- [ ] Transportation booked

## Day 1: [Date] - [Theme]
**Location**: [City/Area]
**Weather**: [Expected conditions]

### Schedule
| Time | Activity | Location | Cost | Notes |
|------|----------|----------|------|-------|
| 08:00 | ... | ... | ... | ... |

### Meals
- Breakfast: [Recommendation]
- Lunch: [Recommendation]
- Dinner: [Recommendation]

### Transportation
- [Detail local transport for the day]

## Budget Summary
| Category | Planned | Actual |
|----------|---------|--------|
| Total | [Amount] | - |

## Emergency Contacts
- Embassy: [Contact]
- Local Emergency: [Number]
- Hotel: [Contact]
```

## Practical Considerations

### Transportation Planning

**Flights**:
- Book 6-8 weeks ahead for best prices
- Consider layover times (minimum 2 hours international)
- Note baggage allowances

**Local Transit**:
- Research transit cards/passes
- Download offline maps
- Note taxi apps used locally

### Accommodation Strategy

**Location Priority**:
1. Safety of neighborhood
2. Proximity to main attractions
3. Public transit access
4. Local dining options

**Booking Tips**:
- Read recent reviews (within 6 months)
- Check cancellation policies
- Verify check-in/out times
- Note any additional fees

### Food Planning

- Research local specialties
- Identify dietary restriction options
- Note meal timing customs
- Budget for food markets and street food
- Reserve popular restaurants in advance

### Activity Booking

**Book in Advance**:
- Popular museums (skip-the-line tickets)
- Tours with limited capacity
- Special events or performances
- Restaurants with reservations

**Leave Flexible**:
- Local markets
- Neighborhood walks
- Cafe visits
- Shopping

## Cultural Preparation

### Essential Research

- Local customs and etiquette
- Dress codes (religious sites, restaurants)
- Tipping practices
- Photography restrictions
- Bargaining expectations

### Useful Phrases

Prepare translations for:
- Greetings and thank you
- Directions and numbers
- Food allergies/restrictions
- Emergency phrases
- Polite refusals

## Risk Management

### Document Backup

- Scan passport and save digitally
- Copy of travel insurance
- Hotel confirmations
- Emergency contact list
- Credit card emergency numbers

### Health Preparation

- Pack personal medications
- Basic first aid kit
- Know nearest hospital location
- Travel insurance covers medical evacuation

### Safety Awareness

- Register with embassy
- Share itinerary with family
- Know local scam tactics
- Keep valuables secure
- Have offline access to maps and contacts
