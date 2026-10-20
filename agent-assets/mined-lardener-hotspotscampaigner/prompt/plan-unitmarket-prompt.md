# Unit Market Feature Plan (Revised — Markdown-Based)

## Progress

| Phase | Status | Notes |
|-------|--------|-------|
| Research & Design | ✅ DONE | Researched existing import patterns (CombatUnitBackground, MUL/Mordel scraper), aligned UI with CampaignTheaterView |
| hsc:// Protocol Design | ✅ DONE | Defined `hsc://procure`, `hsc://hire`, `hsc://market/scrappers/draw` |
| Pilot Generator Integration | ✅ DONE | Incorporated gladiator generator rules for pilot generation in market |
| Database Schema (`schema.sql`) | ✅ DONE | Added `campaign_markets` table with markdown fields |
| SchemaGenerator.java | ✅ DONE | Updated to generate the new `campaign_markets` table |
| Java Entity (`CampaignMarket.java`) | ✅ DONE | Created R2DBC entity matching project conventions |
| Repository (`CampaignMarketRepository.java`) | ✅ DONE | ReactiveCrudRepository with `findByCampaignId` |
| Backend Services | ✅ DONE | Implemented `MarketService`, `MarkdownMarketFormatter`, `PriceComputationService` |
| GraphQL Schema Extensions | ⏳ PENDING | Need to add queries/mutations for market operations |
| Frontend Components | ⏳ PENDING | `MarketDashboard`, `MarketView`, `UnitMarketBackground`, `ScrapperDrawButton` |
| Pilot Generator Backend | ✅ DONE | Implemented gladiator generator logic with SP earned tracking for market pilots |
| Testing & Integration | ⏳ PENDING | End-to-end testing of market flow |

---

## Core Concept

Instead of database-backed market entries, each market is a **curated markdown document** containing formatted unit listings with embedded `hsc://procure?...` links. The campaign manager composes markets via a markdown editor (or by importing from MUL/Mordel URLs which auto-generate the markdown). Players browse rendered markdown and click purchase links.

---

## Market Types

Each campaign has up to **3 market slots**:

| Slot | Description |
|------|-------------|
| **FREE MARKET** | Generic units available to all players, not tied to any employer |
| **PRIMARY EMPLOYER MARKET** | Units offered by Employer A (one per campaign faction) |
| **OPPOSITION EMPLOYER MARKET** | Units offered by Employer B |
| **SCRAPPERS MARKET** | Random-unit draw — a special section with a "pay X, get random" hsc:// link |

The market content is stored as markdown text in the campaign metadata (or a lightweight `campaign_markets` table with one row per campaign).

---

## Data Model

### Single New Table: `campaign_markets`

```sql
CREATE TABLE campaign_markets (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  campaign_id BIGINT NOT NULL UNIQUE,
  free_market_markdown TEXT,
  scrapper_market_markdown TEXT,
  scrapper_pool_markdown TEXT,  -- hidden pool of random units to draw from
  scrapper_fee INT NOT NULL DEFAULT 1200,
  employer_markets_json JSON,  -- key: faction_id, value: markdown text
  FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
```

**Rationale**: One row per campaign. Each market is a `TEXT` blob of markdown. The scrapper pool is separate so it's hidden from players. Employer markets are a JSON map since the number of employers varies.

### No New Tables For

- ~~`market_lists`~~ — replaced by markdown
- ~~`market_units`~~ — replaced by hsc:// links in markdown
- ~~`market_purchases`~~ — purchases flow through existing `hsc://procure` mechanism, logged in existing campaign audit
- ~~`scrapers_pool`~~ — stored as `scrapper_pool_markdown` text field

---

## hsc:// Protocol Extension

### New Action: `hsc://procure`

```
hsc://procure?model=Cataphract&variant=CM-11K&bv=6500&pv=0&sz=3&type=BM&tech=Inner la Sphere&tons=65&price=650000
```

The frontend `useHscActionHandler` parses this and:
1. Opens the unit editor pre-filled with the unit data
2. Shows a confirmation dialog: "Purchase Cataphract CM-11K for 650,000 C-Bills?"
3. On confirm, calls existing `procureCombatUnit` mutation
4. Deducts C-Bills from player's balance

### New Action: `hsc://market/scrappers/draw`

```
hsc://market/scrappers/draw?campaign=123&fee=50000
```

Clicking this:
1. Backend randomly selects a unit from the hidden `scrapper_pool_markdown`
2. Returns unit details + condition roll
3. Frontend shows a "reveal" animation then opens the purchase confirmation

### New Action: `hsc://hire`

```
hsc://hire?name=Kowloon&unitType=BM&wounds=0&gunnerySpEarned=300&pilotingSpEarned=200&edgeTokensSpEarned=100&edgeAbilitySpEarned=150&edgeAbilities=Hot%20Shot&price=25000
```

The frontend `useHscActionHandler` parses this and:
1. Opens a pilot hire dialog pre-filled with pilot data
2. Shows confirmation: "Hire 'Kowloon' at 25,000 C-Bills/month?"
3. On confirm, calls `hireFromMarket` mutation
4. Adds pilot to the hiring player's detachment roster
5. Monthly rate deducted from player's C-Bill balance (per campaign month)

---

## Import Flow

### From MUL/Mordel URLs

The campaign manager pastes a MUL/Mordel URL into the market editor. The existing `ScraperFactory` scrapes the units, then **we format them as markdown**:

```markdown
## Available Mechs

| Unit | Variant | BV | Tech | Condition | Price | Action |
|------|---------|----|------|-----------|-------|--------|
| Cataphract | CM-11K | 6,500 | 3 | Crippled | 650,000 | [Buy](hsc://procure?model=Cataphract&variant=CM-11K&bv=6500&pv=0&sz=3&type=BM&tech=Inner la Sphere&tons=65&price=650000) |
| Griffin GF-6X |  8,000 | 6 | Operational | 1,800,000 | [Buy](hsc://procure?... ) |
```

### Price Computation

Same as today — `PriceComputationService` on the backend (mirroring frontend `pricingUtils.ts`):
- Core: `BV × tech_tax`
- Alpha Strike: `PV × campaign_metadata.pv_purchase_unit_multiplier`
- Campaign manager can override prices manually in the markdown editor (just edit the number)

### Markdown Formatter Service

New `MarkdownMarketFormatter.java`:
- Input: `List<CombatUnit>` from scraper
- Output: markdown table with hsc:// links
- Uses campaign metadata for pricing multipliers

---

## Backend Changes

### New Entity

```java
@Entity
@Table(name = "campaign_markets")
public class CampaignMarket implements Persistable<UUID> {
  @Id @GeneratedValue
  private Long id;
  
  @OneToOne @JoinColumn(name = "campaign_id")
  private Campaign campaign;
  
  @Column(columnDefinition = "TEXT")
  private String freeMarketMarkdown;
  
  @Column(columnDefinition = "TEXT")
  private String scrapperMarketMarkdown;
  
  @Column(columnDefinition = "TEXT")
  private String scrapperPoolMarkdown;
  
  @Column
  private Integer scrapperFee = 50000;
  
  @Column(columnDefinition = "JSON")
  private Map<String, String> employerMarkets; // faction_id -> markdown
}
```

### New Service: `MarketService.java`

```java
@Service
public class MarketService {
  private final ScraperFactory scraperFactory;
  private final MarkdownMarketFormatter formatter;
  private final CampaignMarketRepository repository;
  private final CampaignRepository campaignRepository;
  private final CampaignService campaignService;
  private final PilotGeneratorService pilotGenerator;

  // Import units from URL, return formatted markdown
  public Mono<String> importUnitsToMarkdown(UUID campaignId, String url, MarketType type, UUID factionId, RuleSet ruleSet);
  
  // Get market markdown for display
  public Mono<String> getMarketMarkdown(UUID campaignId, MarketType type, UUID factionId);
  
  // Save market markdown (after CM edits)
  public Mono<CampaignMarket> saveMarketMarkdown(UUID campaignId, MarketType type, String markdown, UUID factionId);
  
  // Scrapper's draw — random unit from pool
  public Mono<CombatUnit> scrapperDraw(UUID campaignId);
  
  // Generate hsc://hire link for a random pilot
  public String generatePilotHireLink(UUID campaignId, String weightClass);
}
```

### New Service: `MarkdownMarketFormatter.java`

```java
@Service
public class MarkdownMarketFormatter {
  // Format scraped units into markdown table with hsc://procure links
  public String formatUnitTable(List<CombatUnit> units, UUID campaignId, MarketType type, CampaignMetadata metadata);
  
  // Parse markdown to extract unit list (for scrapper pool randomization)
  public List<CombatUnit> parseUnitTable(String markdown);
}
```

### New Service: `PriceComputationService.java`

```java
@Service
public class PriceComputationService {
  // Compute unit price based on BV/PV and campaign metadata multipliers
  public long computePrice(CombatUnit unit, CampaignMetadata metadata);
}
```

### Extend `useHscActionHandler`

Add handler for `hsc://procure` (market purchases), `hsc://hire` (pilot hiring), and `hsc://market/scrappers/draw`.

---

## GraphQL Schema Extensions

### Types

```graphql
enum MarketType {
  FREE
  EMPLOYER
  SCRAPPERS
}

type CampaignMarket {
  id: ID!
  campaignId: ID!
  freeMarketMarkdown: String
  scrapperMarketMarkdown: String
  scrapperFee: Int!
  employerMarkets: [EmployerMarket!]!
}

type EmployerMarket {
  factionId: ID!
  markdown: String
}
```

### Queries

```graphql
type Query {
  campaignMarket(campaignId: ID!): CampaignMarket
}
```

### Mutations

```graphql
type Mutation {
  importUnitsToMarket(campaignId: ID!, url: String!, marketType: MarketType!, factionId: ID): String!
  saveMarketMarkdown(campaignId: ID!, marketType: MarketType!, markdown: String!, factionId: ID): Boolean!
}
```

---

## Visual Design

### Background Component: `UnitMarketBackground.tsx`

Pattern-identical to `CombatUnitBackground.tsx` — a full-viewport overlay with a dimmed background image and scrolling message traffic:

```tsx
export const UnitMarketBackground: React.FC = () => {
    const intercepts = useMemo(() => {
        const baseList = [
            "[MARKET] FREEPORT DELTA :: CATAPHRACT CM-11K LISTED AT 650K C-BILLS. SELLER: HOUSE MARCUS.",
            "[MARKET] SCRAPPERS' YARD :: RANDOM LOT AVAILABLE. MIN BID: 50K C-BILLS. NO RETURNS.",
            "[INTEL] EMPLOYER FEED :: COMBINE OUTPOST SEEKING 2 PILOTS FOR PATROL DUTY. PAY: 15K/MO.",
            "[MARKET] BLACK MARKET :: REFURBISHED ENFORCER E1-N. CONDITION 72%. ASKING 2.1M.",
            "[LOGISTICS] SUPPLY RUN :: SHIPMENT OF AC/20 SHELLS DELAYED. EXPECT 72-HOUR HOLD.",
            "[MARKET] FREEPORT DELTA :: PILOT HIRING: VETERAN 'KOWLOON' — 15 YEARS, MECH COMMANDER. RATE: 25K/MO.",
            "[INTEL] SCRAPPERS' YARD :: PULL LEDGER ENTRY #4492. UNIT: GRIFLIN GF-6X. BV: 18K.",
            "[MARKET] EMPLOYER FEED :: DRACON CO-OP OFFERING 3 MONTH CONTRACT. PAY UPFRONT.",
            "[STATUS] MARKET CLEARING :: YESTERDAY'S LOT: 4 MECHS SOLD, 2 PILOTS HIRED. VOLUME UP 12%.",
            "[ALERT] PRICE SPIKE :: PPC-COMPATIBLE HEAT SINKS NOW 40% ABOVE BASE. SUPPLY CHAIN DISRUPTION.",
            "[MARKET] FREEPORT DELTA :: SHADOW HAWK SH-HBK-4H. LOW HOURS, HIGH CONDITION. 420K.",
            "[INTEL] PILOT ROSTER :: RETIRED LIEUTENANT SEEKING CIVILIAN CONTRACT. SPECIALTY: ARTILLERY.",
            "[MARKET] SCRAPPERS' YARD :: \"LUCKY DIP\" DRAW OPEN. FEEDS UPDATED HOURLY.",
            "[LOGISTICS] TRANSPORT :: CARGO HOLD 3 CONTAINS 12 TONS OF FERRO-FIBROUS PLATING. DESTINATION: BAY 7.",
            "[MARKET] EMPLOYER FEED :: PERSEUS WAR MEMORIAL FUND OFFERING BENEVOLENT MECH LEASE. SEE DETAILS.",
            "[STATUS] EXCHANGE RATE :: 1 C-BILL = 0.00045 CREDITS. FEDERAL RESERVE STABLE.",
            "[MARKET] BLACK MARKET :: UNREGISTERED ATMOSPHERIC JUMP JET. NO PAPERWORK. 85K C-BILLS.",
            "[INTEL] PILOT HIRING :: GREEN RECRUIT \"SANDSTORM\" — 2 YEARS. MEDIC TRAINED. 8K/MO.",
            "[MARKET] FREEPORT DELTA :: CENTURION CEN-3N. FULLY ARMED. TURN-KEY. 580K.",
            "[ALERT] MARKET WATCH :: TECH BASE 5+ MECHS IN HIGH DEMAND. PRICES RISING."
        ];
        return [...baseList].sort(() => Math.random() - 0.5);
    }, []);
    // ... same scroll pattern as CombatUnitBackground
};
```

**Background image**: Placeholder `/unit_market_exchange.png` to be generated later (theme: dimly lit mech market / trading floor / scrap yard).

**Scrolling messages**: Market-themed intercepts — unit listings, pilot hiring ads, price alerts, logistics updates. Same CSS animation (`scroll-intel`) as the combat unit editor.

---

## Frontend Components

### 1. `MarketDashboard.tsx`

Parent component with the `UnitMarketBackground` overlay. Shows tabs for each market type:
- Free Market tab
- One tab per employer faction
- Scrapper's Market tab

### 2. `MarketView.tsx` (Theater-View-Style Markdown Editor)

**Directly mirrors `CampaignTheaterView.tsx`'s "Operational Briefing" pattern:**

**Layout** (same as theater view):
- Large markdown display area centered in the viewport
- Dimmed tactical background (`UnitMarketBackground`)
- Header bar with market type title

**View Mode** (default — all users see this):
- Rendered markdown via `TacticalMarkdown` component
- Clickable `hsc://procure` and `hsc://hire` links resolved by `useHscActionHandler`
- Read-only — players can browse but cannot edit

**Edit Mode** (Campaign Manager only):
- `[ EDIT ]` / `[ CLOSE ]` toggle button visible **only to the Campaign Manager**
- Uses the same `campaign.isManager` guard as `CampaignTheaterView`
- When active, replaces the rendered markdown with a large `<textarea>` for raw markdown editing
- Same `table-input` CSS class, `min-height: 300px`, monospace font
- **While in edit mode, inline link generator panels appear below the textarea**

**Link Generator Panels** (inline in MarketView, visible only in edit mode):

*Critical Distinction*: Unlike `CombatUnitEditor` which auto-imports scraped units directly into the form, these panels **only generate `hsc://` links** that the CM manually pastes into the markdown editor. This gives the CM full control over formatting, placement, and presentation.

**Unit Link Generator Panel**:
- Label: `[ IMPORT UNIT LINK FROM MUL/MORDEL ]`
- Input field: Paste a MUL or Mordel unit URL
- `[ GENERATE LINK ]` button
- **Process**: Calls backend to scrape unit data from URL → formats as `hsc://market/purchase?...` link
- **Output**: Read-only text field showing the generated `hsc://` link
- `[ COPY ]` button to copy link to clipboard
- CM then pastes the link into the markdown editor textarea at the desired location

**Pilot Link Generator Panel**:
- Label: `[ IMPORT PILOT LINK FROM MUL/MORDEL ]`
- Input field: Paste a MUL or Mordel pilot URL
- `[ GENERATE LINK ]` button
- **Process**: Calls backend to scrape pilot data from URL → formats as `hsc://market/hire?...` link
- **Output**: Read-only text field showing the generated `hsc://` link
- `[ COPY ]` button to copy link to clipboard
- CM then pastes the link into the markdown editor textarea
### Pilot Generator (Market)
Following the GLADIATOR GENERATOR rules, the backend will support generating random pilots for the market.

**Generation Logic**:
1. Roll 2D6 for Experience Rating (with class adjustments).
2. Roll on Gladiator Skill Levels Table for Piloting/Gunnery skills.
3. Roll for Edge Abilities based on experience level.

**Market Integration**:
- The `ScraperFactory` will be extended to support pilot URL scraping.
- The `MarkdownMarketFormatter` will format generated pilots into `hsc://market/hire?...` links.
- The `MarketLinkGenerator` will provide a "Generate Random Pilot" button (in addition to the URL import) which calls the backend generator and provides the resulting link for the CM to paste into the market markdown.
- This ensures pilots in the market are procedurally generated but curated by the CM via the markdown editor.
**Why Generate Links Instead of Auto-Import?**
- Gives CM full editorial control over market layout, headings, descriptions
- CM can mix imported links with hand-written markdown (narrative text, images, tables)
- Consistent with the "curated markdown document" design philosophy
- Avoids auto-mutating state — CM explicitly decides what appears in the market

**Persistence**:
- Changes saved on explicit `[ SAVE ]` button press (or on blur after debounce)
- Calls `saveMarketMarkdown` mutation

### 3. `ScrapperDrawButton.tsx`

Special button for the scrapper's market:
- Shows "Draw from the Scrap Heap — 50,000 C-Bills"
- On click, triggers `hsc://market/scrappers/draw`
- Shows reveal animation with random unit

---

## Implementation Phases

### Phase 1: Database Schema & Entity
- [X] Create `campaign_markets` table in `schema.sql`
- [X] Create `CampaignMarket.java` entity
- [X] Create `CampaignMarketRepository.java`

### Phase 2: Backend Services
- [X] `MarketService.java` — import, get/save markdown, scrapper draw, pilot hire
- [X] `MarkdownMarketFormatter.java` — format units to markdown, parse markdown
- [X] `PriceComputationService.java` — mirror `pricingUtils.ts` logic
- [X] Extend `ScraperFactory` integration to return markdown
- [ ] Extend for pilot scraping (pilot URLs → `hsc://market/hire` links)
- [X] Implement Pilot Generation logic (based on Gladiator Generator rules)

### Phase 3: GraphQL Integration
- [ ] Extend `schema.graphqls` with new types, queries, mutations
- [ ] Add `hireFromMarket` mutation for pilot hiring
- [ ] Implement resolvers in `MarketResolver.java`
- [ ] Wire up `MarketService` to GraphQL layer

### Phase 4: Visual Design
- [ ] `UnitMarketBackground.tsx` — full-viewport overlay with scrolling market intercepts
- [ ] Create placeholder background image `/unit_market_exchange.png`
- [ ] Reuse `scroll-intel` CSS animation from `CombatUnitBackground.tsx`

### Phase 5: Frontend Components
- [ ] `MarketDashboard.tsx` — tabbed interface with background overlay
- [ ] `MarketView.tsx` — Theater-view-style markdown editor (view/edit toggle, CM-only)
- [ ] `MarketLinkGenerator.tsx` — CM only tool to generate `hsc://` links from URLs (units + pilots)
- [ ] `MarketManagerToolbar.tsx` — CM controls
- [ ] `ScrapperDrawButton.tsx` — random draw mechanic
- [ ] Add `react-markdown` dependency

### Phase 6: hsc:// Protocol Extension
- [ ] Implement `hsc://market/scrappers/draw` handler
- [ ] Wire purchase/hire flow to existing C-Bill deduction logic

### Phase 7: Testing & Polish
- [ ] Test import flow (MUL + Mordel URLs for units and pilots)
- [ ] Test purchase flow end-to-end
- [ ] Test pilot hire flow end-to-end
- [ ] Test scrapper's market randomization
- [ ] Markdown editor UX polish
- [ ] Link generator UX (copy-to-clipboard, URL validation)
- [ ] Security: verify CM-only access to edit/save and link generator

---

## Security Considerations

- **Market editing**: Only campaign manager can save market markdown
- **Price override**: CM edits markdown directly, so they control prices
- **Purchase validation**: Backend validates player has sufficient C-Bills before confirming
- **Scrapper pool**: `scrapper_pool_markdown` is never returned to client — only the drawn unit is revealed

---

## User Flows

### Campaign Manager Sets Up Market

1. Opens Market Dashboard → clicks "Import from URL"
2. Pastes MUL/Mordel URL → backend scrapes units
3. Scraped units appear as formatted markdown table with hsc:// links
4. CM reviews, edits prices/condition manually if desired
5. Clicks "Save Market" → markdown persisted

### Player Browses & Purchases

1. Opens Market Dashboard → sees rendered markdown
2. Clicks "[Buy]" link on a unit → `hsc://procure` fires
3. On confirm, C-Bills deducted, unit added to player's command

### Scrapper's Market

1. Player sees "Draw from Scrap Heap — 50,000 C-Bills"
2. Clicks button → `hsc://market/scrappers/draw` fires
3. Backend randomly picks from hidden pool
4. Reveal animation shows the unit + `hsc://procure` link for confirmation

---

## Key Differences From Original Plan

| Original | Revised |
|----------|---------|
| 4 new tables | 1 table (`campaign_markets`) |
| Queryable market entries | Markdown text (not queryable, but simpler) |
| Dedicated market unit entities | hsc:// links carry all data |
| Complex CRUD mutations | Simple markdown get/save + import |
| Market purchase tracking table | Purchases flow through existing mechanisms |
