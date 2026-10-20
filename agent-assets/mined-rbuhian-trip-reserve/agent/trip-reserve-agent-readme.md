# Trip Reserve Agents

> "When you play the game of thrones, you win or you die." - Cersei Lannister

These agents assist with development of Trip Reserve. Each agent is named after a Game of Thrones character whose traits match their responsibilities.

---

## The Queen - Orchestrator

| Agent | Character | Role |
|-------|-----------|------|
| **Daenerys** | Mother of Dragons | Feature orchestrator - breaks down features, assigns agents, coordinates implementation |

**Usage**: Start with Daenerys when implementing any feature. She will analyze the request and delegate to the appropriate agents.

```
"Daenerys, implement the customer booking history feature (CUST-30 to CUST-37)"
"Daenerys, orchestrate the driver availability calendar"
```

---

## The Small Council

| Agent | Character | Role | Domain |
|-------|-----------|------|--------|
| **Sansa** | Sansa Stark | UI Craftsman | Flutter widgets, screens, components |
| **Bran** | Bran Stark | Database Oracle | Supabase schemas, migrations, RLS |
| **Arya** | Arya Stark | Model Shapeshifter | Dart models with freezed |
| **Varys** | The Spider | State Master | Riverpod providers |
| **Tyrion** | Tyrion Lannister | Repository Hand | Data access layer |
| **Hound** | Sandor Clegane | Test Warrior | Unit & widget tests |
| **Littlefinger** | Petyr Baelish | Route Master | GoRouter navigation |
| **Jon** | Jon Snow | Map Ranger | Google Maps, location |
| **Tywin** | Tywin Lannister | Payment Lord | PayMongo, transactions |
| **Brienne** | Brienne of Tarth | Auth Guardian | Supabase Auth, sessions |

## Usage

Reference an agent when working on its domain:

```
"Use Sansa to create the booking card widget"
"Ask Bran to design the bookings table schema"
"Have Arya generate the Vehicle model"
```

## Agent Files

```
.claude/agents/
├── daenerys.md     # 👑 Orchestrator (start here)
├── sansa.md        # Flutter UI
├── bran.md         # Supabase Database
├── arya.md         # Dart Models
├── varys.md        # Riverpod State
├── tyrion.md       # Repository Layer
├── hound.md        # Testing
├── littlefinger.md # Router/Navigation
├── jon.md          # Maps Integration
├── tywin.md        # Payments
└── brienne.md      # Authentication
```

## Workflow Example

Building a new feature (e.g., "View Booking Details"):

0. **Daenerys** - Analyze feature, create implementation plan, assign agents
1. **Bran** - Design/verify database schema
2. **Arya** - Generate Dart models
3. **Tyrion** - Create repository methods
4. **Varys** - Set up Riverpod providers
5. **Sansa** - Build the UI screen
6. **Littlefinger** - Add routes
7. **Hound** - Write tests

```
┌─────────────┐
│  DAENERYS   │  ← Start here (orchestrator)
│  👑 Queen   │
└──────┬──────┘
       │ delegates to
       ▼
┌──────────────────────────────────────────────────────┐
│                  SMALL COUNCIL                        │
├────────┬────────┬────────┬────────┬────────┬────────┤
│  Bran  │  Arya  │ Tyrion │ Varys  │ Sansa  │ Hound  │
│   🌳   │   🗡️   │   🍷   │   🕷️   │   👑   │   🐕   │
│   DB   │ Models │  Repo  │ State  │   UI   │ Tests  │
└────────┴────────┴────────┴────────┴────────┴────────┘
       │
       │ specialists (when needed)
       ▼
┌──────────────────────────────────────┐
│  Littlefinger  │   Jon   │  Tywin   │  Brienne  │
│      🗝️        │   ❄️    │    🦁    │    ⚔️     │
│    Routes      │  Maps   │ Payments │   Auth    │
└────────────────┴─────────┴──────────┴───────────┘
```

---

## Session Management

Daenerys tracks implementation progress to prevent token cutoffs.

```
.claude/sessions/
├── TEMPLATE.md     # Session file template
├── active.md       # Current session (created when starting)
├── history/        # Completed sessions
└── handoff/        # Interrupted sessions to resume
```

### Commands

```
"Continue from handoff"     → Resume interrupted session
"Show session status"       → Check current progress
"Save checkpoint"           → Force progress save
```

### Session Health

| Status | Meaning |
|--------|---------|
| 🟢 GOOD | Continue normally |
| 🟡 CAUTION | Complete checkpoint, then assess |
| 🔴 WRAP_UP | Finish task, save state, handoff |

---

*"Valar Morghulis"* - All code must be tested.
