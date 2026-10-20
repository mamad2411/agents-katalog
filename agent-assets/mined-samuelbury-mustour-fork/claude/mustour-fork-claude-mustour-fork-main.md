# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Development server**: `yarn dev` (runs on port 3001 with Turbopack)
- **Build**: `yarn build` (includes Prisma generation)
- **Lint**: `yarn lint`
- **Database push**: `yarn generate` (pushes Prisma schema to database)
- **Create subscription products**: `yarn createProduct` (populates database with Stripe products)
- **Testing**: `yarn test` (Jest unit tests)

## Development Rules & Guidelines

### Core Development Principles

- **Simplicity First**: Always prefer simple solutions over complex ones. Check existing implementations before creating new code
- **DRY Principle**: Avoid code duplication - search the codebase for similar functionality before implementing
- **Environment Awareness**: Write code that adapts to dev, test, and prod environments using proper environment variables
- **Clean Architecture**: Keep files under 200-300 lines, maintain clear separation of concerns
- **No Production Mocking**: Only use mocking/stubbing for tests, never for dev/prod environments
- **Incremental Changes**: Make only requested changes or well-understood related modifications
- **Never Overwrite .env**: Always ask before modifying environment configuration

### Layered Architecture (MVC Pattern)

This project follows a strict 3-layer architecture aligned with the existing codebase structure:

**Controllers Layer** (Input validation & routing):

- **API Routes**: `/app/api/[resource]/route.ts` - RESTful endpoints
- **Server Actions**: `/actions/[action].ts` - Form submissions and mutations (flat structure, no subfolders)
- **tRPC Routes**: `/server/` - Type-safe API endpoints
- **Responsibilities**:
  - Input validation with Zod schemas
  - HTTP request/response handling
  - Calling appropriate services
  - Error response formatting

**Services Layer** (Business logic orchestration):

- **Location**: `/services/[resource]/*.service.ts`
- **Responsibilities**:
  - Business logic implementation
  - Workflow orchestration
  - Cross-domain operations
  - Data transformation and aggregation
  - Calling multiple repositories if needed
- **Restrictions**:
  - NO direct database access
  - NO input validation (assumes validated data)
  - NO HTTP handling

**Repository Layer** (Data access):

- **Structure**: `/repository/[resource]/queries.ts` and `/repository/[resource]/mutations.ts`
- **Database Import**: Always use `import { db } from "@/lib/database/db"`
- **Responsibilities**:
  - Pure database operations
  - External API calls
  - Data persistence logic
- **Restrictions**:
  - NO business logic
  - NO input validation
  - Only CRUD operations and data retrieval

### Authentication & Security

- **Framework**: Lucia Auth for all authentication (configured in `/lib/lucia/index.ts`)
- **OAuth Providers**: Google, Facebook, GitHub, Magic Link support
- **Session Management**: Lucia handles sessions, middleware protects routes
- **Route Protection**: Use `(protected)` route groups for authenticated pages
- **Security Headers**: Implement proper CORS, CSP, and security headers
- **Role-Based Access**: Implement RBAC for multi-tenant features

### Form Management & Validation

- **Form Library**: Always use React Hook Form for form state management
- **Validation**: Zod schemas for type-safe validation (define in `/types/`)
- **Component Structure**:
  ```typescript
  import { useForm } from "react-hook-form";
  import { zodResolver } from "@hookform/resolvers/zod";
  // Wrap inputs with @/components/Form/LabelBlock
  ```
- **Button Components**: Use `@/components/Button`, set `type="button"` for non-submit actions
- **Database Objects**: Every DB object requires a `dbId` for update/create distinction
- **Dynamic Forms**: Use `useFieldArray` for dynamic lists (beds, photos, equipment)
- **Data Fetching**: Use SWR for fetching existing data in update scenarios
- **Error Display**: Show validation errors through LabelBlock components

### Next.js 15 App Router Patterns

- **Component Simplicity**: Keep components focused, move complex logic to custom hooks
- **Hook Organization**: Business logic in `/hooks/` directory with descriptive names
- **File Naming**: Descriptive names, consistent patterns (ComponentName.tsx, useHookName.ts)
- **Early Returns**: Improve readability with guard clauses (`if (!data) return null`)
- **Styling**: Tailwind CSS only, no separate CSS files or inline styles
- **Accessibility**: ARIA labels, proper tabIndex, keyboard navigation support
- **Function Declaration**: Arrow functions as constants (`const handleClick = () => {}`)
- **TypeScript**: Strict typing, never use `any`, define interfaces in `/types/`
- **Client Data**: SWR for client-side data fetching and caching
- **Internationalization**: Use next-intl with `/messages/` directory structure

### Error Handling & Logging

- **Centralized Logging**: Use `@utils/logger` for all error logging with contextual information
- **Error Context**: Include request IDs, user data, operation context in logs
- **Environment-Specific**: Full details in dev, sanitized logs in production
- **Prisma Error Handling**: Wrap all Prisma operations with `@/lib/handlers/withErrorHandling.ts`
- **Structured Responses**: Standardized error objects with proper HTTP status codes
- **Async Operations**: Always wrap in try-catch blocks for DB calls and API requests
- **Global Error Boundary**: Implement React error boundaries for unhandled errors
- **Error Monitoring**: Consider Sentry integration for production error tracking

### Database & Prisma Best Practices

- **Database Import**: Consistent use of `import { db } from "@/lib/database/db"`
- **Schema Organization**: Domain-split schemas in `/prisma/` (users, flights, hosting, etc.)
- **Repository Pattern**: Strict separation - only repositories access Prisma client
- **Input Validation**: Validate all inputs before database operations (in controllers)
- **Query Optimization**: Use proper indexing, select only needed fields, server-side filtering
- **Transactions**: Use Prisma transactions for complex multi-table operations
- **Migration Management**: Use `yarn generate` for schema changes
- **Row-Level Security**: Implement where needed for multi-tenant data isolation
- **Connection Management**: Proper connection pooling and cleanup

### TypeScript Excellence

- **Type Safety**: Avoid `any` - define proper types in `/types/` directory (Note: TypeScript strict mode is currently disabled in tsconfig.json)
- **Export Strategy**: Prefer named exports over default exports for better refactoring
- **Module Design**: Use ES modules, avoid circular dependencies
- **Interface Design**: Single responsibility principle for interfaces and types
- **Performance**: Code splitting with dynamic imports, lazy loading for large components
- **Generic Types**: Use generics for reusable type patterns
- **Utility Types**: Leverage TypeScript utility types (Pick, Omit, Partial, etc.)
- **Type Guards**: Implement type guards for runtime type checking
- **Discriminated Unions**: Use for complex state management

### UI/UX Component System

- **Component Reusability**: Always search existing components before creating new ones
- **Design System**: Use consistent component patterns across the application
- **Component Architecture**:
  - Keep components simple and focused on presentation
  - Extract business logic into custom hooks or container components
  - Use container pattern: `ComponentContainer` handles logic, `Component` handles UI
  - Props should be minimal and focused on what the component needs to render
- **Toast System**:
  ```typescript
  import { toast } from "@/components/ui/use-toast";
  toast({
    title: "Opération réussie!",
    description: "Le type d'âge a été créé avec succès",
  });
  ```
- **Button Consistency**: Use `@/components/Button` with proper type attributes
- **Form Components**: Standardize with `@/components/Form/LabelBlock` wrapper
- **Loading States**: Implement skeleton components for better UX
- **File Uploads**: Use Cloudflare R2 integration with drag-and-drop support
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints

### Project Structure Alignment

This structure aligns with the existing codebase organization:

- **`/actions/`**: Server actions for mutations (flat structure only)
- **`/app/[locale]/`**: Internationalized routes with locale-specific pages
  - **`(protected)/`**: Authenticated routes (dashboard, admin panel)
  - **`(withLayout)/`**: Public pages with consistent layout
- **`/app/constants/`**: Application-wide constants (Stripe config, feature flags)
- **`/components/`**: Domain-organized reusable UI components
  - **Feature folders**: Flight/, Hosting/, Trip/, etc.
  - **Shared folders**: ui/, Form/, Button/
- **`/hooks/`**: Custom hooks for state management and business logic
- **`/lib/`**: Core utilities, database client, authentication setup
- **`/server/`**: tRPC router definitions for type-safe APIs
- **`/services/`**: Business logic layer (calls repositories)
- **`/repository/`**: Data access layer (queries.ts + mutations.ts per domain)
- **`/types/`**: Shared TypeScript interfaces and Zod schemas
- **`/utils/`**: Pure utility functions and helpers

### Domain-Specific Implementation

- **Travel Domains**: Flight, Autocar, Hosting, Trip management
- **Complex Pricing**: Multi-period, room-type, age-combination pricing for accommodations
- **Multi-tenancy**: Subscription-based features with quota enforcement
- **File Management**: Document tracking with entity relationships
- **Client Management**: CRM functionality with ClientSheet components

### Performance & Security Guidelines

- **Bundle Optimization**: Remove unused dependencies, implement code splitting
- **Caching Strategy**: SWR for client-side caching, server-side caching where appropriate
- **Security Headers**: Implement CSP, CORS, security headers
- **Input Sanitization**: Zod validation prevents injection attacks
- **Memory Management**: Proper cleanup of connections and event listeners
- **SEO Optimization**: Server-side rendering with Next.js App Router
- **Monitoring**: Error tracking and performance monitoring setup

### Testing Strategy

- **Unit Testing**: Test business logic in hooks and services with proper mocking
- **Integration Testing**: Test API routes and database interactions
- **Component Testing**: Test UI components with React Testing Library
- **E2E Testing**: Critical user flows with Playwright or Cypress
- **Error Scenarios**: Test error handling and edge cases
- **Test Organization**: Descriptive test names, grouped by feature

## Architecture Overview

This is a multi-tenant travel management SaaS platform built with Next.js 15 App Router and TypeScript. The application follows a layered architecture with clear separation between presentation, business logic, and data access layers.

### Core Tech Stack

- **Frontend**: Next.js 15.3.5 with App Router, React 19.1.0, TypeScript 5, Tailwind CSS 3.3.0
- **Backend**: Next.js API Routes + tRPC 11.0.0 for type-safe APIs
- **Database**: PostgreSQL with Prisma ORM 5.17.0
- **Authentication**: Lucia Auth 3.0.1 with OAuth providers (Google, Facebook, GitHub, Magic Link)
- **State Management**: Redux Toolkit 1.9.3 + Jotai 2.12.2 for specific atomic state
- **Data Fetching**: SWR 2.3.2, React Query 5.62.11
- **Forms**: React Hook Form 7.50.1 with Zod 3.24.2 validation
- **Internationalization**: next-intl 3.26.3 (English/French)
- **Payments**: Stripe 16.2.0 with subscription management
- **Storage**: Cloudflare R2 (AWS SDK) + Firebase Storage
- **Email**: SendGrid
- **Charting**: ApexCharts, Chart.js, Recharts
- **UI Components**: Shadcn/ui, Full Calendar, React Beautiful DnD

### Project Structure

**Route Organization:**

- `/app/[locale]/` - Internationalized routes
  - `(protected)/` - Authenticated routes (dashboard, admin)
  - `(withLayout)/` - Public pages with layout
- `/components/` - Reusable UI components organized by feature
- `/lib/` - Core utilities, database client, authentication
- `/server/` - tRPC router definitions
- `/actions/` - Server actions for mutations
- `/repository/` - Data access layer
- `/services/` - Business logic layer

**Domain-Specific Features:**

- **Flight/** - Flight booking and management with ALLOTMENT/SALE allocation system
- **Autocar/** - Bus/coach transportation management
- **Hosting/** - Accommodation with complex multi-dimensional pricing (periods, age combinations, room types)
- **Trip/** - Trip planning linking flights, transfers, and accommodations
- **ClientSheet/** - CRM with client relationships, companies, and commercial tracking
- **AgeTypes/** - Organization-specific age categorization for pricing

### Key Architectural Patterns

**Prisma Schema Organization:**

- Schema is split across multiple `.prisma` files by domain (users, flights, autocars, hosting, trips)
- Located in `/prisma/` directory
- Use `yarn generate` to push schema changes to database

**Authentication Flow:**

- Lucia Auth handles session management (configured in `/lib/lucia/index.ts`)
- OAuth providers configured in `/lib/auth/` (Google, Facebook, GitHub, Magic Link)
- Protected routes use middleware for authentication checks (`middleware.ts`)
- Route groups organize protected vs public pages

**Data Layer:**

- Repository pattern for data access (`/repository/`) - queries.ts and mutations.ts per domain
- Service layer for business logic (`/services/`) - orchestrates repositories
- tRPC provides type-safe API endpoints (`/server/`) - replaces traditional REST where applicable

**Complex Pricing System:**

- Accommodation pricing supports multiple periods, room types, and age combinations
- Pricing logic in `/services/hosting/` following the service layer pattern
- Database models support flexible pricing structures with proper normalization

**File Upload System:**

- Cloudflare R2 integration for secure file storage
- Document tracking with entity relationships
- FileUpload component supports drag-and-drop with progress tracking

### Multi-tenancy & Subscriptions

- Subscription-based SaaS model with Stripe integration
- Feature quotas enforced per subscription plan
- Admin dashboard for user and subscription management
- Payment links and products configured in `/app/constants/stripe.ts`

### Development Notes

- **Port Configuration**: Port 3001 is used for development to avoid conflicts with other services
- **Build System**: Turbopack enabled for faster builds and hot reloading
- **Database Management**: Schema changes require running `yarn generate` (pushes to database)
- **Internationalization**: Messages located in `/messages/` directory (English/French support)
- **Environment Setup**: Variables defined in `.env` (see `.env.example` for reference)
- **Error Handling**: All routes must use `@/lib/handlers/withErrorHandling.ts` for Prisma operations
- **Code Quality**: ESLint enforced (TypeScript strict mode is currently disabled)

## Domain Architecture Details

### Flight Management System

The flight domain implements a sophisticated seat allocation system:

- **Dual Allocation Modes**: ALLOTMENT (pre-allocated blocks) and SALE (direct sales)
- **Agency Management**: Multiple agencies per flight with access control
- **Seat Classes**: Support for different classes (economy, business, etc.)
- **Stopovers**: Full support for multi-leg flights with baggage transfer options
- **Options**: Additional services (meals, insurance, etc.)

### Trip Management System

The trip module orchestrates complete travel packages by combining multiple services:

#### Core Concepts

- **Organigramme**: Visual trip builder with drag-and-drop interface for organizing travel components
- **Direction Management**: Handles outbound (aller) and return (retour) journey segments
- **Component Linking**: Smart linking between flights and their associated transfers
- **Order Management**: Maintains chronological order of trip components with reordering capabilities

#### Trip Components (OrganigrammeItem)

Each trip can include multiple component types with sub-type options:

- **Transport**:
  - **Vol (Flight)**: Flights with specific direction (aller/retour)
  - **Autocar**: Bus/coach as main transportation (not transfer)
- **Transfert**: Ground transportation (autocars) linked to flights
- **Hébergement**: Accommodations with pricing period selection (Hotel only currently)
- **Restaurations**: Meal arrangements with sub-types (Standard, Premium) - future implementation
- **Activités**: Activities and excursions with sub-types (Visite, Shopping, Sport) - future implementation
- **Other**: Miscellaneous services (Excursion) - future implementation

#### Key Features

1. **Visual Trip Builder** (`/components/Trip/SelectedItemsList/`):

   - Drag-and-drop interface for organizing trip components
   - Real-time preview of trip structure
   - Visual indicators for component types and directions
   - Automatic transfer suggestions based on flight selections
   - **Smart Transfer Grouping**: Transfers with same date and direction are automatically grouped into a single display line with count indicator (e.g., "TRANSFERT ALLER (3)")
   - **Temporary Products Support**: Users can create temporary products during the search phase that can later be finalized into real products

2. **Component Selection System** (`/components/Trip/`):

   - **ProductSelectorModal**: Initial category selection with sub-type options
     - Each product category displays a dropdown for selecting sub-types
     - Transport category offers "Vol" (default) or "Autocar" options
     - Visual consistency: all categories show a dropdown even with single option
   - **Sub-type Selection Flow**:
     - User selects product category (Transport, Transfert, etc.)
     - User selects sub-type from dropdown (e.g., Vol vs Autocar for Transport)
     - System routes to appropriate search modal based on selection
   - **OrganigrammeModal**: Handles searching and adding items
     - Receives `selectedTransportType` to differentiate between Vol and Autocar
     - ItemSearchPanel adapts its configuration based on sub-type
   - **Smart Context Switching**:
     - Transport with "autocar" sub-type uses autocar search endpoints
     - Transport with "flight" sub-type uses flight search endpoints
     - Transfert always uses autocar endpoints (single option)
   - Search and filter available flights, transfers, and accommodations
   - Direction-based filtering (aller/retour)
   - Smart defaults based on trip context
   - Bulk selection capabilities

3. **Trip Form Management** (`/hooks/organigram/useTrip.ts`):

   - Complex form state management with React Hook Form
   - Nested validation for all trip components
   - Photo and document attachment support
   - Auto-save and draft management

4. **Data Structure**:

   ```typescript
   // Trip contains references to all components
   Trip {
     flights: TripFlight[]      // Flight references with direction
     transfers: TripTransfer[]  // Transfer references linked to flights
     accommodations: TripAccommodation[] // Hosting references with periods
     documents: Document[]      // Attached documents
   }
   ```

5. **Linking Logic**:

   - Transfers can be linked to specific flights via `linkedFlightId`
   - Automatic suggestion of transfers based on flight destinations
   - Direction inheritance from parent flight to linked transfers
   - Visual grouping of linked components in the UI

6. **State Management** (`/hooks/organigram/useOrganigramme.ts`):

   - Centralized state for trip building process
   - Section-based component organization
   - Global ordering system for all components
   - Real-time synchronization with form state
   - Preserves all transfer properties (dates, cities, etc.) during state management

7. **Transfer Grouping Logic** (`/components/Trip/SelectedItemsList/hooks.ts`):

   - Automatic grouping of transfers by departure date and direction
   - Single-line display for grouped transfers with count
   - Expansion available when group contains temporary products
   - Maintains first transfer's information as representative of the group

8. **Temporary Products System**:

   - **Purpose**: Allows users to save search criteria as temporary products when the exact product doesn't exist yet
   - **Storage**: JSON field in Trip table for lightweight, flexible storage
   - **User Workflow**:

     1. User fills search form with desired criteria (dates, cities, etc.)
     2. Clicks "Créer temporaire" button to save as temporary product
     3. Product appears in trip list with 50% opacity and orange Edit3 icon
     4. User can click the edit icon to reopen search form with prefilled data
     5. User can then create the final product to replace the temporary one

   - **Visual Indicators**:

     - 50% opacity for temporary products
     - Orange Edit3 icon instead of blue Edit icon
     - No external link icon (since product doesn't exist yet)
     - Special handling for transfer groups with temporary items (expandable dropdown)

   - **Technical Implementation**:

     - **Database Schema** (`/prisma/schema/trip.prisma`):

       ```prisma
       model Trip {
         temporaryProducts Json? // Stores all temporary products as JSON
       }
       ```

     - **Type Definitions** (`/types/trip.ts`):

       ```typescript
       interface TemporaryProduct {
         id: string;
         productType: "flight" | "autocar" | "hosting";
         searchData: Record<string, any>; // Flexible search criteria
         direction?: "aller" | "retour";
         order: number;
         createdAt: string;
       }

       interface TemporaryProductsCollection {
         flights: TemporaryProduct[];
         transfers: TemporaryProduct[];
         accommodations: TemporaryProduct[];
       }
       ```

     - **Data Flow**:

       1. **Creation**: `ItemSearchPanel` → `createTemporaryProduct` action → Repository saves to JSON
       2. **Display**: `useOrganigrammeWithTemporary` hook merges real and temporary products
       3. **Editing**: Click edit → Opens `OrganigrammeModal` with `temporaryItem` prop → Prefills search form
       4. **Finalization**: Save in product creation form → `finalizeTemporaryProduct` action → Replaces temporary with real product
       5. **Deletion**: Custom `handleRemoveItem` → `deleteTemporaryProduct` action → Removes from JSON

     - **Repository Layer** (`/repository/trip/mutations.ts`):

       - `addTemporaryProduct`: Adds to JSON array
       - `removeTemporaryProduct`: Removes from JSON array
       - `updateTemporaryProduct`: Updates existing temporary product

     - **Service Layer** (`/services/trip/trip.service.ts`):

       - `createTemporaryProduct`: Business logic for creation
       - `finalizeTemporaryProduct`: Converts temporary to real product
       - `deleteTemporaryProduct`: Handles deletion

     - **UI Components**:

       - `ItemSearchPanel`: "Créer temporaire" button and logic
       - `SelectedItemsList`: Display and management of temporary products
       - `TableRow`: Special rendering for temporary products
       - `OrganigrammeModal`: Handles editing of temporary products

     - **State Management**:
       - `useOrganigrammeWithTemporary`: Hook that merges real and temporary products for display
       - SWR integration for data refresh after operations
       - No page reload needed - uses `mutate()` for updates

   - **Special Behaviors**:
     - Transfer groups with temporary items are expandable (normally collapsed)
     - Temporary products can't have documents attached
     - Temporary products don't have external links
     - All temporary product operations trigger SWR revalidation

#### Technical Implementation

- **Repository Layer**: `/repository/trip/` handles all database operations
- **Service Layer**: `/services/trip/` orchestrates business logic
- **Actions**: `/actions/trip.ts` and `/actions/tripActions.ts` for server-side mutations
- **Types**: `/types/trip.ts` defines all TypeScript interfaces
- **API Routes**: `/api/trips/` for REST endpoints
- **Product Categories Hook**: `/hooks/organigram/useProductCategories.ts`
  - Defines available options for each product category
  - Returns helper functions for accessing icons and labels
  - Central source of truth for product sub-types
- **Temporary Products Actions** (`/actions/tripActions.ts`):
  - `createTemporaryProduct`: Creates a new temporary product in JSON storage
  - `finalizeTemporaryProduct`: Converts temporary product to real product
  - `deleteTemporaryProduct`: Removes temporary product from JSON storage

#### Best Practices

- Always maintain trip component order for chronological consistency
- Link transfers to flights when applicable for better UX
- Validate direction consistency (aller components before retour)
- Use the organigramme for visual trip building
- Implement proper error handling for component conflicts
- Use temporary products for planning trips when exact products don't exist yet
- Always trigger SWR revalidation after modifying temporary products
- Ensure visual differentiation between temporary and real products
- Handle temporary product deletion separately from regular product deletion

### Hosting Pricing System

Complex multi-dimensional pricing structure:

- **Pricing Periods**: Main periods (e.g., high season) with sub-periods (weekends, weekdays)
- **Age Combinations**: Flexible room occupancy (e.g., 2 adults + 1 child)
- **Room Types**: Different categories with specific equipment and bed configurations
- **Restauration**: Integrated meal plans with age-based pricing
- **Dynamic Pricing**: Support for purchase/sale/allotment pricing types

#### SALE Pricing with Purchase Dates

When PURCHASE mode has dates with room availabilities:

- **Date Synchronization**: SALE mode automatically displays the same dates from PURCHASE
- **Price Segmentation**: Each date-room combination has independent pricing
- **Automatic PricingDate Creation**: When saving SALE prices with a date, the system automatically creates/finds a corresponding PricingDate entry of type SALE
- **Data Flow**:
  1. Frontend sends date ISO string without pricingDateId for SALE
  2. Backend creates/retrieves SALE PricingDate for that date
  3. Prices are stored with the SALE pricingDateId, segmented by date AND room
  4. Retrieval uses the date ISO to find the correct SALE PricingDate
- **Visual Synchronization**: SALE dates remain visually synchronized with PURCHASE dates while maintaining separate pricing data

#### Room Search & Pricing Logic

**FIFO Selection** (`/services/reservation/hotelSearch.service.ts`):

- Periods contain `pricingDates` (specific dates) and/or `subPeriods` (date ranges)
- Search: Loop pricingDates chronologically → first with `quantity > 0` wins → fallback to period availability
- Pricing: Base prices from source (pricingDate/period) + subPeriod overrides per night → average by ageType/position

**AgeType Positions**: Multiple positions per age type for differential pricing (e.g., 1st adult ≠ 2nd adult)

- Composite key: `${ageTypeId}_${position}` prevents overwrites
- `outsideParentRoom`: boolean for children sleeping outside parent room

### Multi-tenancy Implementation

- **Organization Isolation**: All queries filtered by `organizationId`
- **Feature Quotas**: Usage tracking per subscription plan
- **Subscription Tiers**: basic, basic_plus, premium with different feature sets
- **Row-Level Security**: Automatic filtering at repository layer

### Patterns & Best Practices

#### Component Patterns

- **Container/Presenter**: Business logic in containers, UI in presenters
- **Custom Hooks**: Extract complex logic (e.g., `usePricing`, `useFlightForm`)
- **Controlled Components**: React Hook Form for all form management
- **Dynamic Fields**: `useFieldArray` for lists (seats, beds, equipment)

#### Data Flow Patterns

- **Service Layer**: Orchestrates business logic, no direct DB access
- **Repository Pattern**: Pure data operations, no business logic
- **Server Actions**: Standardized response format `{ success, error?, data? }`
- **Error Handling**: Centralized logging with contextual information

#### State Management

- **Redux**: Authentication and global app state
- **Jotai**: Component-specific atomic state (e.g., edit modes)
- **SWR**: Data fetching with caching and revalidation
- **React Hook Form**: Form state management

#### TypeScript Patterns

```typescript
// Type-safe response pattern
type ActionResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Discriminated unions for complex states
type AllocationMode =
  | { type: "SALE"; price: number }
  | { type: "ALLOTMENT"; quantity: number; agency: string };

// Generic table components
interface TableFormProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  onUpdate: (row: T) => Promise<void>;
}
```

### Code Organization Standards

#### Import Order

1. React/Next.js imports
2. Third-party libraries
3. Internal absolute imports (@/)
4. Types
5. Local components

#### File Structure

- Components: Feature-based organization
- Hooks: Prefixed with `use`, contain business logic
- Services: Singleton objects with business methods
- Repositories: Separated queries.ts and mutations.ts

#### Naming Conventions

- **Components**: PascalCase (e.g., `FlightForm`)
- **Hooks**: camelCase with `use` prefix (e.g., `useFlightData`)
- **Services**: camelCase with `Service` suffix (e.g., `flightService`)
- **Actions**: Descriptive verbs (e.g., `createFlight`, `updateSeats`)
- **Types**: PascalCase with context suffix (e.g., `FlightFormData`)
