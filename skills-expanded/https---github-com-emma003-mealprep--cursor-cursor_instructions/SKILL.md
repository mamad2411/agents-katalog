# Cursor AI Development Instructions
*Meal Planner App - AI-Assisted Development Guide*

## 🎯 Project Overview
Building a comprehensive meal planner mobile app using React Native, Expo, Appwrite, and NativeWind with AI-driven development workflow.

**Tech Stack:** React Native + Expo + TypeScript + NativeWind + Appwrite

---

## 📁 Project Structure Requirements

### Core Directories
```
meal-planner/
├── components/          # Reusable UI components
├── app/            # Screen components
├── services/           # API and business logic
├── hooks/              # Custom React hooks
├── types/              # TypeScript definitions
├── utils/              # Helper functions
├── design-assets/
│   ├── ui-inspiration/     # Reference design images
│   ├── component-specs/    # Design system docs
│   └── user-flows/         # User journey visuals
├── .cursor/
│   ├── cursor-memory.md    # Project state tracking
│   ├── design-decisions.md # AI-made design choices
│   ├── code-patterns.md    # Reusable patterns
│   └── task-progress.json  # Current development status
```

---

## 🤖 AI Development Workflow

### Phase 1: Setup & Initialization

#### 1.1 Project Initialization


#### 1.2 AI Context Setup
```bash
# Create AI context files
touch .ai-context/{cursor-memory.md,design-decisions.md,code-patterns.md,task-progress.json}
touch docs/{prd.md,architecture.md,api-specs.md}
```

### Phase 2: Requirements & Planning

#### 2.1 PRD Creation Instructions
**Cursor Task:** Create comprehensive PRD in `docs/prd.md` using .cursor/create-prd.mdc and this instructions doc

**Prompt Template:**
```
Create a detailed PRD for a meal planner mobile app including:

USER FLOW: 
When the user opens the app, if not logged in, there is a landing page with a get started button (if they're logged in they go to dashboard immediately). When they click the get started button, they are taken to the login/sign up page. After logging in or signing up, they are taken to the dashboard where there are multiple tabs: dashboard (shows today's meals and a small calendar where they can pick a date and see this week's meals, a create meal plan button), a groceries tab with the grocery list of the week, a profile tab with user's dietary preference and logout button, a favorites tab with favorite recipes. When they press create meal plan, they are taken to a multi-screen form (vertical swipe between screens) that asks for the user's preferred number of main meals, snacks, desserts, soups, salads..., tee foods they would like to include/exclude, the types of cuisines they want to experiment within the meal plan. Once the user enters all that info, a request is made to Spoontacular API to fetch corresponding recipes, then the user is asked to choose amongst those and drag and drop the meals in a weekly calendar. 

CORE FEATURES:
- Landing page
- Authentication
- Dynamic vertical swipe form for meals preferences (how many main meals, soups, desserts.. Any foods to exclude, foods to include...)
  - User must swipe up to see the next form section
- Animated loading screen while the form data is used to get the recipe
- After all the recipes are fetched, the user is shown multiple recipe cards per meal type and must select the ones they want
- The response from Spoontacular API should include the recipe's instructions, grocery list, nutritional info (number of calories, amount of protein), a high definition picture to go along with the recipe card
- After the user is done choosing, they are taken back to their home dashboard where they see the meals they chose
- At this point: When user logs in, they are taken to their home dashboard with a button to create plan if they have none at the moment, 
- The home dashboard should include a horizontal scroll calendar where the user can pick any day of the we
- Weekly meal planning with drag-and-drop interface
- Automated shopping list generation
- Nutritional tracking and analysis
- Dietary restrictions and preferences
- Meal prep scheduling

IMPLEMENTATION SEQUENCE:
The implementation should be split in the following milestones:
1. Setup + Authentication + Global auth context
2. Form creation + global form data context
3. Fetch recipes from spoontacular API and Show options for user to select
4. Flesh out dashboard with selected recipes including plan dates and nutritional information
5. Set up profile page, favorites tab, ingredients tab

TECHNICAL REQUIREMENTS:
- React Native + Expo for cross-platform mobile
- Appwrite for backend services and real-time sync and authentication
- NativeWind for styling consistency
- TypeScript for type safety
- Spoontacular API for weekly meal plans
- Zustand for state management
- Zod for form validation
- Global auth context (zustand)
- UI design should follow the inspiration screenshots in design-assets/ui-inspiration, use the appropriate folder when implementing each feature

USER PERSONAS:
- Busy parents planning family meals
- Health-conscious individuals tracking nutrition
- Meal prep enthusiasts optimizing weekly cooking

ACCEPTANCE CRITERIA:
- Sub-2 second app launch time
- Support for iOS and Android

Include detailed user stories, technical specifications.
```

#### 2.2 Architecture Documentation
**Cursor Task:** Create `docs/architecture.md`

**Requirements:**
- Component hierarchy and data flow
- State management strategy (Zustand)
- API integration patterns (Appwrite)
- Navigation structure
- Performance optimization strategies

---

## 🎨 Design-Driven Development

### Design Context Guidelines

#### Before Any Frontend Task:
1. **Always check** `design-assets/ui-inspiration/` for relevant design references
2. **Load visual context** by opening related design images in Cursor workspace
3. **Reference design system** in `design-assets/component-specs/`
4. **Follow established patterns** documented in `.ai-context/code-patterns.md`

#### UI Component Creation Prompt Template:
```
Context: Creating ${COMPONENT_NAME} component
Design Reference: design-assets/ui-inspiration/${RELEVANT_FOLDER}/
Requirements: ${SPECIFIC_REQUIREMENTS}

Tech Stack Guidelines:
- React Native with TypeScript
- NativeWind for styling (Tailwind classes)
- Follow atomic design principles
- Implement loading and error states

Deliverables Required:
1. Component implementation with TypeScript interfaces
2. Storybook story for visual testing
3. Usage documentation with examples

Code Standards:
- Use descriptive component and prop names
- Include JSDoc comments for complex logic
- Implement proper error boundaries
- Follow established patterns in .ai-context/code-patterns.md
- Ensure mobile-first responsive design
```

---

## 📋 Task Management Integration

### TaskMaster AI Integration

#### Task Template Structure:
```json
{
  "task_id": "unique-identifier",
  "task_type": "frontend|backend|documentation",
  "title": "Descriptive task title",
  "description": "Detailed requirements and acceptance criteria",
  "design_reference": "design-assets/path/to/relevant/images",
  "dependencies": ["list-of-prerequisite-tasks"],
  "deliverables": [
    "Code implementation",
    "Documentation"
  ]
}
```

#### Task Execution Workflow:
1. **Load Task Context:** Review task requirements and dependencies
2. **Prepare Design Context:** Open relevant design assets
3. **Review Previous Decisions:** Check `.ai-context/design-decisions.md`
4. **Implement Solution:** Follow established code patterns
5. **Update Context:** Document decisions and patterns

---

## 🔧 Code Standards & Patterns

### TypeScript Guidelines
- **Always use strict typing** - no `any` types
- **Use component-level interfaces** - define interfaces at the top of each component file
- **Shared interfaces only** - put in `lib/types/` only when used across multiple components
- **Use discriminated unions** for state management
- **Implement proper error types** with detailed error handling
- **Co-location principle** - keep related types close to their usage

### React Native Patterns
```typescript
// Component Template with component-level interfaces
interface ComponentNameProps {
  // Props definition with JSDoc
  /** Description of the prop */
  propName: PropType;
}

interface ComponentNameState {
  // Component-specific state if needed
  loading: boolean;
  error: string | null;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  propName,
}) => {
  // Hooks at the top
  const [state, setState] = useState<ComponentNameState>({
    loading: false,
    error: null,
  });
  
  // Event handlers
  const handleAction = useCallback(() => {
    // Implementation
  }, [dependencies]);
  
  // Render
  return (
    <View 
      className="container-styles"
    >
      {/* Component content */}
    </View>
  );
};
```

### State Management (Zustand)
```typescript
// Store Template
interface StoreState {
  // State definition
  data: DataType[];
  loading: boolean;
  error: string | null;
  
  // Actions
  fetchData: () => Promise<void>;
  updateData: (data: DataType) => void;
  clearError: () => void;
}

export const useStore = create<StoreState>((set, get) => ({
  data: [],
  loading: false,
  error: null,
  
  fetchData: async () => {
    set({ loading: true, error: null });
    try {
      // Implementation
      set({ data: result, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  
  // Other actions...
}));
```

---

## 🔌 Appwrite Integration Patterns

### Service Layer Template
```typescript
// services/appwrite.ts
import { Client, Databases, Account } from 'appwrite';

class AppwriteService {
  private client: Client;
  private databases: Databases;
  private account: Account;

  constructor() {
    this.client = new Client()
      .setEndpoint(process.env.EXPO_PUBLIC_APPWRITE_ENDPOINT!)
      .setProject(process.env.EXPO_PUBLIC_APPWRITE_PROJECT_ID!);
    
    this.databases = new Databases(this.client);
    this.account = new Account(this.client);
  }

  // CRUD operations with proper error handling
  async createDocument<T>(
    collectionId: string, 
    data: Omit<T, 'id'>
  ): Promise<T> {
    try {
      const response = await this.databases.createDocument(
        process.env.EXPO_PUBLIC_APPWRITE_DATABASE_ID!,
        collectionId,
        'unique()',
        data
      );
      return response as T;
    } catch (error) {
      throw new AppwriteError('Failed to create document', error);
    }
  }
}
```

---

## 📱 UI Development Guidelines

### NativeWind Styling Patterns
- **Use semantic class names:** `container`, `card`, `button-primary`

### Animation & Interactions
- **Use React Native Reanimated** for smooth animations
- **Implement gesture handling** with React Native Gesture Handler
- **Add haptic feedback** for user interactions
- **Optimize for 60fps** performance

---

## 🚀 Performance Optimization

### Bundle Optimization
- **Implement code splitting** for screens and heavy components
- **Use lazy loading** for non-critical features
- **Optimize images** with appropriate formats and sizes
- **Minimize bundle size** with tree shaking

### Runtime Performance
- **Use React.memo** for expensive components
- **Implement proper list virtualization** with FlatList
- **Optimize re-renders** with useCallback and useMemo
- **Handle memory management** properly

---

## 🔄 Context Management

### Update .ai-context Files After Each Task

#### cursor-memory.md Updates:
```markdown
## Current Development Status
- Last completed task: [Task Name]
- Current focus area: [Frontend/Backend]
- Next priority: [Next Task]

## Recent Decisions
- [Date]: Decision about [topic] - [rationale]

## Current Blockers
- [Any impediments or dependencies]
```

#### design-decisions.md Updates:
```markdown
## Component Design Patterns
- [Component Type]: [Established pattern and rationale]

## UI/UX Decisions
- [Feature]: [Design choice and reasoning]

## Technical Architecture Decisions
- [System]: [Implementation choice and rationale]
```

#### code-patterns.md Updates:
```typescript
// Document reusable patterns established during development
// Update this file when creating new patterns or modifying existing ones
```

---

## 🎯 Success Criteria

### Task Completion Checklist
- [ ] Functionality implemented according to requirements
- [ ] Design matches visual references
- [ ] TypeScript types properly defined
- [ ] Documentation updated
- [ ] AI context files updated
- [ ] Code follows established patterns

### Quality Gates
- **TypeScript compilation** must be error-free
- **Linting** must pass without warnings
- **Design review** against reference materials

---

## 🚨 Important Reminders

### Always Remember:
1. **Check design assets** before any UI work
2. **Update AI context** after significant decisions
3. **Follow TypeScript strict mode** - no shortcuts
4. **Document patterns** for future AI reference
5. **Optimize for mobile performance** in all implementations

### Never Skip:
- Post-task documentation updates
- Type safety implementations
- Error handling and edge cases
- Performance impact assessment

---

*This document should be referenced for every development task to ensure consistency and quality across the entire project.*

*FOR EVERY TASK, ALWAYS ALWAYS ENSURE TO FOLLOW BEST PRACTICES AS OUTLINED BY REACT NATIVE OFFICIAL DOCS (https://reactnative.dev/docs/getting-started), NATIVEWIND DOCS (https://www.nativewind.dev/docs) and APPWRITE DOCS (https://appwrite.io/docs)*
