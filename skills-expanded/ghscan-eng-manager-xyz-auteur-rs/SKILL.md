# AI Design Prompt Generation: Requirement Translation

Meta-skill for translating business requirements (BRD), product requirements (PRD), and engineering requirements (ERD) into AI-ready design specifications using systematic extraction, decomposition, and vocabulary mapping to Base Web components, Fusion.js plugins, and Atreyu RPC patterns.

## When to Use This Skill

Use this skill when:
- Converting user stories into Base Web component specifications
- Translating PRD features into AI design prompts using Uber's stack
- Mapping BRD business rules to UI behaviors with Base Web components
- Extracting implicit requirements from specifications
- Preserving traceability from requirement to implementation
- Bridging product management and AI-assisted design in the Uber web-code monorepo

**UI Library**: Base Web (baseui) -- Uber's design system
**Framework**: Fusion.js with plugin architecture
**Data Layer**: Atreyu RPC + fusion-plugin-rpc + fusion-plugin-react-query
**Styling**: Styletron (atomic CSS-in-JS)

**Used by AI Designer**: This is a meta-skill that transforms source requirements into prompts for other aiux-* skills.

## Core Principles for Requirement Translation

Requirements documents speak product language; AI tools speak design language. Translation bridges this gap systematically, mapping to the Uber technology stack.

Key principles:
1. **Decompose Before Translate**: Break requirements into atomic units before mapping to Base Web components
2. **Explicit Over Implied**: Surface hidden assumptions in requirements
3. **Vocabulary Mapping**: Map business terms to Base Web component names and Fusion.js patterns
4. **Traceability Preserved**: Link generated specs to source requirements
5. **Completeness Over Brevity**: AI needs more detail than human-readable requirements

## Requirement Translation Framework

### Translation Process

**Step 1: Requirement Parsing**
- Identify requirement type (user story, acceptance criteria, business rule)
- Extract actors, actions, and objects
- Note explicit constraints
- Surface implicit assumptions

**Step 2: Decomposition**
- Break into atomic units (one Base Web component per unit)
- Identify UI patterns implied by actions
- Map business objects to Base Web components
- Extract validation rules (Zod schemas)

**Step 3: Vocabulary Mapping**
- Map business terms to Base Web component names
- Map actions to interactions (Modal, Toast, Popover, navigation)
- Map data to display patterns (StatefulDataTable, ListItem, Card)
- Map rules to constraints (FormControl error, Banner, Dialog)
- Map data fetching to RPC patterns (useRpcQuery, useRpcMutation)

**Step 4: Specification Generation**
- Generate aiux-* skill inputs from mapped elements
- Preserve traceability (requirement ID to spec section)
- Add missing specifications (loading states, error handling, accessibility)
- Validate completeness

### Requirement Types & Extraction

#### User Story Translation

**Format**: As a [actor], I want [action], so that [outcome]

**Extraction Pattern**:
| Element | Maps To | Uber Stack Reference |
|---------|---------|---------------------|
| Actor | User context, USSO role | fusion-plugin-auth-headers provides UUID, roles, groups |
| Action verb | Interaction type | Base Web component + RPC handler |
| Object | Component/data type | Base Web component (StatefulDataTable, Card, Modal) |
| Outcome | Success state, feedback | Toast, Banner, navigation |

**Example Translation**:
```markdown
**User Story**:
As an admin, I want to view all orders, so that I can monitor fulfillment.

**Extraction**:
- Actor: admin (authenticated via USSO, role check via fusion-plugin-auth-headers)
- Action: view all orders (read-only display, useRpcQuery)
- Object: orders (list/table of Order entities from Atreyu service)
- Outcome: monitor fulfillment (status visibility via Tag KIND indicators)

**UI Implications**:
- Component: StatefulDataTable (baseui/data-table) with CategoricalColumn for status
- Key column: Status (prominent, using Tag with KIND.positive/negative/warning/accent)
- Permissions: Server-side role check in RPC handler via ctx from auth-headers
- Data: useRpcQuery('getOrders', { orgId }) via fusion-plugin-react-query

**Mapped Spec**:
-> aiux-data-display: Orders StatefulDataTable with status CategoricalColumn, Tag badges
-> aiux-state-management: Spinner loading, empty state (HeadingSmall + ParagraphMedium), error Banner
-> aiux-navigation-architecture: SideNavigation (baseui/side-navigation) with Orders link
```

#### Acceptance Criteria Translation

**Format**: Given [context], When [action], Then [result]

**Extraction Pattern**:
| Element | Maps To | Uber Stack Reference |
|---------|---------|---------------------|
| Given | Pre-condition, state | React Query cache state, URL params |
| When | Trigger | onClick, onSubmit, RPC mutation |
| Then | Response | Toast, Modal, state update, navigation |

**Example Translation**:
```markdown
**Acceptance Criteria**:
Given the user is on a product page,
When they click "Add to Cart",
Then the product is added to their cart,
And a confirmation toast appears,
And the cart count updates.

**Extraction**:
- Context: Product page, product data loaded via useRpcQuery
- Trigger: Click on Button (baseui/button, KIND.primary)
- Responses:
  1. Cart state updates (useRpcMutation('addToCart'))
  2. Toast notification (toaster.positive from baseui/toast)
  3. Cart badge count increments (React Query invalidation)

**UI Implications**:
- Button: Button KIND.primary, isLoading during mutation
- Toast: toaster.positive('Added to cart', { autoHideDuration: 3000 })
- Badge: Badge (baseui/badge) on cart icon with count
- Optimistic update: React Query onMutate optimistic update

**Mapped Spec**:
-> aiux-component-description: Button KIND.primary with isLoading state
-> aiux-interaction-behavior: Click -> isLoading -> toaster.positive
-> aiux-state-management: React Query mutation with optimistic update
```

#### Business Rule Translation

**Format**: If [condition], then [action], otherwise [alternative]

**Extraction Pattern**:
| Element | Maps To | Uber Stack Reference |
|---------|---------|---------------------|
| Condition | UI conditional | RPC response field, React Query data |
| Action | Enabled behavior | Button, form, navigation |
| Alternative | Fallback UI | Different Button KIND, disabled state, hidden |

**Example Translation**:
```markdown
**Business Rule**:
If the product is in stock, allow purchase.
If the product is out of stock, show "Notify Me" instead.
If the product is discontinued, hide the action buttons.

**Extraction**:
- Condition 1: inStock === true -> Button KIND.primary "Add to Cart"
- Condition 2: inStock === false && !discontinued -> Button KIND.secondary "Notify Me"
- Condition 3: discontinued === true -> No buttons rendered

**Mapped Spec**:
-> aiux-state-management:
  When inStock: Button KIND.primary "Add to Cart"
  When !inStock && !discontinued: Button KIND.secondary "Notify Me"
  When discontinued: Block display="none" or conditional render
```

### Vocabulary Mapping Tables

#### Action Verbs -> Base Web Patterns

| Verb | UI Pattern | Base Web Component |
|------|------------|-------------------|
| View | Read-only display | Card, ListItem, TableSemantic, Block |
| List | Collection display | StatefulDataTable, ListItem, FlexGrid |
| Create | Form input | FormControl + Input/Select/DatePicker, Modal |
| Edit | Inline edit or form | FormControl + inputs, Modal or inline |
| Delete | Destructive action | Dialog (baseui/dialog) for confirmation |
| Search | Query input | Input with startEnhancer (search icon), Select TYPE.search |
| Filter | Refinement controls | StatefulDataTable built-in filters, Select multi |
| Sort | Column ordering | StatefulDataTable sortable columns |
| Select | Choice input | Select, Checkbox (v2), RadioGroup (v2) |
| Upload | File input | FileUploader (baseui/file-uploader) |
| Download | Export action | Button KIND.secondary with download icon |
| Share | Distribution action | Button + Modal or StatefulPopover |
| Approve/Reject | Binary decision | Button pair (KIND.primary + KIND.secondary) |
| Assign | Relationship action | Select with user options, Combobox |

#### Business Objects -> Base Web Components

| Object | Component Pattern | Base Web Import |
|--------|-------------------|-----------------|
| User | Avatar + LabelSmall | baseui/avatar, baseui/typography |
| Order | StatefulDataTable row or Card | baseui/data-table or baseui/card |
| Product | Card with StyledBody/StyledAction | baseui/card |
| Message | Block with custom styling | baseui/block |
| Notification | Toast or Notification | baseui/toast or baseui/notification |
| Setting | ListItem with Switch/Toggle | baseui/list, baseui/switch |
| File | ListItem with file icon | baseui/list |
| Comment | Block with Avatar + ParagraphMedium | baseui/block, baseui/avatar |
| Task | ListItem with Checkbox | baseui/list, baseui/checkbox-v2 |
| Event | Card with DatePicker | baseui/card, baseui/datepicker |

#### Status Values -> Tag Variants

| Status Category | Values | Tag KIND (baseui/tag) |
|-----------------|--------|----------------------|
| Progress | pending, processing | KIND.warning, KIND.accent |
| Success | completed, approved, active | KIND.positive |
| Error | failed, rejected | KIND.negative |
| Warning | expiring, low stock | KIND.warning |
| Neutral | draft, archived | KIND.neutral |
| Info | new, updated | KIND.accent |

#### Data Fetching -> RPC Patterns

| Requirement Pattern | RPC Pattern | React Query Hook |
|--------------------|-------------|------------------|
| "Load list of X" | RPC handler query | useRpcQuery('getXList', params) |
| "Get details of X" | RPC handler query | useRpcQuery('getXDetails', { id }) |
| "Create new X" | RPC handler mutation | useRpcMutation('createX') |
| "Update X" | RPC handler mutation | useRpcMutation('updateX') |
| "Delete X" | RPC handler mutation | useRpcMutation('deleteX') |
| "Search for X" | RPC handler query | useRpcQuery('searchX', { query }) |
| "Paginated list" | RPC handler query | useRpcInfiniteQuery('getXList') |

### Implicit Requirement Extraction

Requirements often omit common needs. Extract these:

**Always Required** (if not specified):
- Loading states: Spinner (baseui/spinner) or Skeleton (baseui/skeleton)
- Error states: Banner (baseui/banner) KIND.negative or Notification
- Empty states: Block with HeadingSmall + ParagraphMedium (contentSecondary)
- Validation: FormControl error prop + Zod schemas
- Confirmation for destructive actions: Dialog (baseui/dialog)

**Usually Required**:
- Success feedback: toaster.positive() from baseui/toast
- Undo capability: Snackbar (baseui/snackbar) with actionMessage
- Pagination: Pagination (baseui/pagination) for large datasets
- Search: Input with search enhancer for filterable content
- Responsive behavior: Grid/Cell with responsive arrays [small, medium, large]

**Context-Dependent**:
- Auth checks: fusion-plugin-auth-headers role/group checks
- Feature flags: fusion-plugin-feature-toggles
- i18n: baseui/locale LocaleProvider
- Accessibility: Built into Base Web components (ARIA, focus management)

### Traceability Format

```markdown
## OrdersTable Component

**Traces to**:
- REQ-101: "Admin can view all orders"
- REQ-102: "Admin can filter orders by status"
- BR-045: "Cancelled orders show negative badge"

**Requirement Coverage**:
| Requirement | Covered By | Base Web Component |
|-------------|------------|-------------------|
| REQ-101 | Data display | StatefulDataTable |
| REQ-102 | Filtering | CategoricalColumn (built-in filter) |
| BR-045 | Status badge | Tag KIND.negative |
```

## Prompt Validation Framework

### Evaluation Rubric

#### Category 1: Completeness (Weight: 30%)

**Score 5 (Excellent)**:
- All explicit requirements mapped to Base Web components
- Implicit requirements surfaced (loading: Spinner, error: Banner, empty state)
- Edge cases identified from business rules
- All actors/roles considered (USSO roles via auth-headers)

**Score 1 (Poor)**:
- Missing key requirements
- Only happy path considered
- No implicit requirements surfaced

#### Category 2: Vocabulary Accuracy (Weight: 25%)

**Score 5 (Excellent)**:
- All business terms mapped to Base Web components (not generic or shadcn/ui)
- Action verbs mapped to correct UI patterns with correct component names
- Status values mapped to Tag KIND variants
- Data fetching mapped to useRpcQuery/useRpcMutation patterns

**Score 1 (Poor)**:
- Business terms used without mapping to Base Web
- shadcn/ui or generic component names
- No RPC pattern mapping

#### Category 3: Decomposition Quality (Weight: 20%)

**Score 5 (Excellent)**:
- Each requirement decomposed to atomic Base Web component units
- Clear 1:1 mapping (requirement to component/feature)
- Appropriate granularity

**Score 1 (Poor)**:
- Requirements not decomposed
- Unclear mappings

#### Category 4: Traceability (Weight: 15%)

**Score 5 (Excellent)**:
- Every spec links to source requirement
- Requirement coverage matrix present
- Base Web component names in coverage matrix

**Score 1 (Poor)**:
- No requirement links

#### Category 5: Specification Quality (Weight: 10%)

**Score 5 (Excellent)**:
- Generated specs use correct Base Web component names
- Specs reference correct aiux-* skills
- Ready for implementation in Fusion.js app

**Score 1 (Poor)**:
- Specs use wrong component library
- Would not work in Uber web-code monorepo

### Overall Score Calculation

```
Total = (Completeness x 0.30) + (Vocabulary x 0.25) + (Decomposition x 0.20) +
        (Traceability x 0.15) + (Specification x 0.10)

Pass Threshold: >= 3.5/5.0
Excellent Threshold: >= 4.5/5.0
```

### Validation Checklist

**Critical (Must Pass)**:
- [ ] All explicit requirements mapped to Base Web components
- [ ] Action verbs mapped to correct Base Web UI patterns
- [ ] Business objects mapped to Base Web component names (not shadcn/ui)
- [ ] Loading (Spinner/Skeleton), error (Banner), empty states included
- [ ] Data fetching mapped to useRpcQuery/useRpcMutation
- [ ] Requirement IDs preserved for traceability

**Important (Should Pass)**:
- [ ] Implicit requirements surfaced
- [ ] Edge cases from business rules addressed
- [ ] All user roles/actors considered (USSO roles)
- [ ] Coverage matrix with Base Web component names
- [ ] Status values mapped to Tag KIND variants

**Enhancement (Nice to Have)**:
- [ ] Alternative flows documented
- [ ] Feature flag requirements noted (fusion-plugin-feature-toggles)
- [ ] i18n requirements noted (baseui/locale)
- [ ] Accessibility requirements explicit (Base Web built-in ARIA)

## Generation Guidance

### Do This:

**Systematic Translation with Uber Stack**:
```markdown
## Requirement Translation: Driver Onboarding

### Source Requirements

**User Stories**:
- US-201: As a new driver, I want to submit my documents for verification
- US-202: As a new driver, I want to see my verification status
- US-203: As an ops agent, I want to review driver documents

### Translation Output

#### Document Upload (US-201)

**Decomposition**:
| Requirement | UI Element | Base Web Component | Spec Target |
|-------------|------------|-------------------|-------------|
| Upload documents | File upload | FileUploader (baseui/file-uploader) | aiux-form-patterns |
| Document type selection | Dropdown | Select (baseui/select) | aiux-form-patterns |
| Upload progress | Progress indicator | ProgressBar (baseui/progress-bar) | aiux-interaction-behavior |
| Success confirmation | Toast notification | toaster.positive (baseui/toast) | aiux-interaction-behavior |

**Data Fetching**:
- Upload: useRpcMutation('uploadDocument')
- Get upload URL: useRpcQuery('getUploadUrl', { docType })

**Implicit Requirements**:
- Loading state: Button isLoading during upload
- Error state: Banner KIND.negative for upload failure
- File validation: FormControl error for wrong type/size
- Retry: "Try again" Button KIND.secondary on error

-> aiux-form-patterns: FormControl + FileUploader + Select
-> aiux-interaction-behavior: Upload progress, toaster.positive on success
-> aiux-state-management: Spinner during upload, Banner on error

---

#### Verification Status (US-202)

**Decomposition**:
| Requirement | UI Element | Base Web Component |
|-------------|------------|-------------------|
| Status display | Status badge | Tag (baseui/tag) with KIND mapping |
| Document list | Item list | ListItem (baseui/list) |
| Step progress | Progress steps | ProgressSteps (baseui/progress-steps) |

**Status -> Tag KIND Mapping**:
| Status | Tag KIND | Label |
|--------|----------|-------|
| pending | KIND.warning | "Pending review" |
| approved | KIND.positive | "Approved" |
| rejected | KIND.negative | "Rejected" |
| expired | KIND.warning | "Expired" |

-> aiux-data-display: ListItem with Tag status badges
-> aiux-visual-tokens: Tag KIND color mapping

---

#### Document Review (US-203)

**Decomposition**:
| Requirement | UI Element | Base Web Component |
|-------------|------------|-------------------|
| Document list | Data table | StatefulDataTable (baseui/data-table) |
| Document preview | Modal viewer | Modal (baseui/modal) SIZE.auto |
| Approve/reject | Action buttons | Button KIND.primary + KIND.secondary |
| Rejection reason | Text input | Modal + FormControl + Textarea |

**Data Fetching**:
- List: useRpcQuery('getDriverDocuments', { status: 'pending' })
- Approve: useRpcMutation('approveDocument')
- Reject: useRpcMutation('rejectDocument')

-> aiux-data-display: StatefulDataTable with CustomColumn for actions
-> aiux-interaction-behavior: Modal for preview, Dialog for rejection reason
-> aiux-form-patterns: FormControl + Textarea for rejection reason

### Requirement Coverage Matrix

| Req ID | Spec Section | Base Web Component | Status |
|--------|-------------|-------------------|--------|
| US-201 | Document Upload | FileUploader, Select | Covered |
| US-202 | Verification Status | ListItem, Tag, ProgressSteps | Covered |
| US-203 | Document Review | StatefulDataTable, Modal, Dialog | Covered |
```

### Don't Do This:

**Generic Translation without Uber Stack**:
```markdown
Requirements say driver can upload documents, so we need:
- A file upload component
- A status page
- A review table for ops

Let's use shadcn/ui FileUpload and DataTable with Tailwind styling...
```

**Why This Fails**:
- References shadcn/ui instead of Base Web
- References Tailwind instead of Styletron
- No Base Web component names (FileUploader, StatefulDataTable)
- No RPC pattern mapping (useRpcQuery, useRpcMutation)
- No status-to-Tag-KIND mapping
- No implicit requirement extraction

## Related Skills

**Produces inputs for**:
- `aiux-component-description`: Component specs with Base Web component names
- `aiux-form-patterns`: Forms with FormControl + Base Web inputs
- `aiux-data-display`: Tables/lists with StatefulDataTable, ListItem
- `aiux-navigation-architecture`: Flows with SideNavigation, Tabs, Breadcrumbs
- `aiux-state-management`: States with React Query patterns
- `aiux-interaction-behavior`: Interactions with Modal, Toast, Popover

**Validated by**:
- `aiux-prompt-validation`: Checks generated specs

**See Also**:
- `rpc-api`: For Atreyu + fusion-plugin-rpc + React Query patterns
- `api-design-patterns`: For RPC handler design
- `authentication-patterns`: For USSO role/permission checks
