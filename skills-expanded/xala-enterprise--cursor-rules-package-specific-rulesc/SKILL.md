---
description: 
globs: 
alwaysApply: true
---
# Package-Specific Placement Rules

## 🎯 DETAILED PACKAGE PLACEMENT RULES

### 1. **@xbooking/types** - Type Definitions
```typescript
// ✅ PLACE HERE - All TypeScript interfaces and types
export interface User { id: string; email: string; }
export interface ApiResponse<T> { data: T; success: boolean; }
export type UserRole = 'admin' | 'user' | 'guest';

// ❌ NEVER PLACE HERE - Implementation logic
const validateUser = (user: User) => { /* logic */ }
```

**PLACEMENT CRITERIA:**
- [ ] Pure TypeScript interfaces, types, enums
- [ ] Framework-agnostic type definitions
- [ ] API request/response types
- [ ] Shared data structures
- [ ] No implementation logic

### 2. **@xbooking/ui** - Generic UI Components
```typescript
// ✅ PLACE HERE - Generic, reusable UI components
export const Button = ({ children, onClick, variant }) => { /* generic button */ }
export const Modal = ({ isOpen, onClose, children }) => { /* generic modal */ }
export const Card = ({ children, className }) => { /* generic card */ }

// ❌ NEVER PLACE HERE - Business-specific components
export const BookingForm = () => { /* booking logic */ } // ← Goes to @xbooking/business-components
export const TenantDashboard = () => { /* tenant logic */ } // ← Goes to @xbooking/business-components
```

**PLACEMENT CRITERIA:**
- [ ] **Generic** UI components (Button, Input, Modal, Card)
- [ ] **No business logic** embedded
- [ ] **Reusable** across different domains
- [ ] **Presentation-only** components
- [ ] **Framework-specific** (React) but domain-agnostic

### 3. **@xbooking/business-components** - Business Logic Components
```typescript
// ✅ PLACE HERE - Business-specific components
export const BookingForm = ({ booking, onSubmit }) => { /* booking business logic */ }
export const TenantDashboard = ({ tenant }) => { /* tenant-specific dashboard */ }
export const LocationCard = ({ location }) => { /* location business logic */ }
export const RouteManagementPanel = () => { /* route management logic */ }

// ❌ NEVER PLACE HERE - Generic UI components
export const Button = () => { /* generic button */ } // ← Goes to @xbooking/ui
```

**PLACEMENT CRITERIA:**
- [ ] **Business domain knowledge** embedded
- [ ] **Specific to XBooking** use cases
- [ ] **Combines multiple** @xbooking/ui components
- [ ] **Contains business logic** and validation
- [ ] **Higher-level abstractions** for business processes

### 4. **@xbooking/hooks** - React Hooks & Utilities
```typescript
// ✅ PLACE HERE - React hooks and utilities
export const useAuth = () => { /* authentication hook */ }
export const useApi = (endpoint) => { /* data fetching hook */ }
export const useLocalStorage = (key) => { /* storage hook */ }

// ❌ NEVER PLACE HERE - Non-hook utilities
export const formatDate = (date) => { /* utility function */ } // ← Goes to utility functions in appropriate package
```

**PLACEMENT CRITERIA:**
- [ ] **React hooks** (use* functions)
- [ ] **Hook-based utilities** and abstractions
- [ ] **State management hooks**
- [ ] **Side effect management**
- [ ] **Framework-specific** (React) utilities

### 5. **@xbooking/store** - State Management
```typescript
// ✅ PLACE HERE - Global state management
export const useAuthStore = create(() => ({ /* auth state */ }))
export const useTenantStore = create(() => ({ /* tenant state */ }))
export const useRouteManagementStore = create(() => ({ /* route state */ }))

// ❌ NEVER PLACE HERE - Local component state
const [isOpen, setIsOpen] = useState(false); // ← Stays in component
```

**PLACEMENT CRITERIA:**
- [ ] **Global application state**
- [ ] **Cross-component** state sharing
- [ ] **Persistent state** management
- [ ] **Store slices** and actions
- [ ] **State synchronization** logic

### 6. **@xbooking/api-client** - API Services
```typescript
// ✅ PLACE HERE - API service classes and HTTP client
export class UserService {
  async getUsers(): Promise<User[]> { /* API call */ }
}
export class BookingService {
  async createBooking(data: CreateBookingDto): Promise<Booking> { /* API call */ }
}

// ❌ NEVER PLACE HERE - Business logic or UI components
export const validateBooking = (booking) => { /* validation */ } // ← Goes to business-components or utils
```

**PLACEMENT CRITERIA:**
- [ ] **HTTP client** configuration
- [ ] **API service classes**
- [ ] **Request/response** handling
- [ ] **API endpoint** abstractions
- [ ] **Network-related** utilities

### 7. **@xbooking/design-system** - Design Tokens & Styles
```css
/* ✅ PLACE HERE - Design tokens and CSS variables */
:root {
  --color-primary: #3b82f6;
  --spacing-md: 1rem;
  --radius-lg: 0.5rem;
}

/* ❌ NEVER PLACE HERE - Component-specific styles */
.booking-form { /* specific styles */ } /* ← Goes with component in business-components */
```

**PLACEMENT CRITERIA:**
- [ ] **Design tokens** (colors, spacing, typography)
- [ ] **CSS custom properties**
- [ ] **Global styles** and resets
- [ ] **Theme configurations**
- [ ] **Brand-agnostic** design system

### 8. **@xbooking/localization** - Internationalization
```typescript
// ✅ PLACE HERE - Translation system and i18n utilities
export const useTranslation = (namespace) => { /* translation hook */ }
export const translateContent = (key, locale) => { /* translation logic */ }

// ❌ NEVER PLACE HERE - Translated content
const messages = { welcome: "Welcome" }; // ← Goes in JSON files or database
```

**PLACEMENT CRITERIA:**
- [ ] **Translation system** logic
- [ ] **Locale management**
- [ ] **i18n utilities** and hooks
- [ ] **Language detection**
- [ ] **Translation resolution** logic

## 🔄 PLACEMENT DECISION FLOWCHART

```
📝 NEW CODE TO PLACE
    ↓
❓ Is it a TypeScript type/interface?
    ✅ YES → @xbooking/types
    ❌ NO ↓
    
❓ Is it a generic UI component (Button, Input, Modal)?
    ✅ YES → @xbooking/ui
    ❌ NO ↓
    
❓ Does it contain business domain logic?
    ✅ YES → @xbooking/business-components
    ❌ NO ↓
    
❓ Is it a React hook?
    ✅ YES → @xbooking/hooks
    ❌ NO ↓
    
❓ Is it global state management?
    ✅ YES → @xbooking/store
    ❌ NO ↓
    
❓ Is it an API service or HTTP client?
    ✅ YES → @xbooking/api-client
    ❌ NO ↓
    
❓ Is it a design token or CSS variable?
    ✅ YES → @xbooking/design-system
    ❌ NO ↓
    
❓ Is it translation/i18n related?
    ✅ YES → @xbooking/localization
    ❌ NO ↓
    
❓ Is it configuration or environment related?
    ✅ YES → @xbooking/config
    ❌ NO ↓
    
❓ Is it logging or error handling?
    ✅ YES → @xbooking/logger
    ❌ NO ↓
    
❓ Is it AI/ML related?
    ✅ YES → @xbooking/ai-service
    ❌ NO ↓
    
❓ Is it monitoring or metrics related?
    ✅ YES → @xbooking/monitoring
    ❌ NO ↓
    
❌ UNCLEAR → ANALYZE FURTHER OR ASK FOR GUIDANCE
