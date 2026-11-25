# RockOps Mining Site Management System - Cursor AI Rules

## 🎯 Project Overview
RockOps is a comprehensive mining site management system with REST API + WebSocket support, built with Spring Boot 3.4.5, PostgreSQL, and MinIO storage. This system manages equipment, maintenance workflows, multi-site operations, and real-time notifications.

## 🏗 Architecture & Tech Stack
- **Backend**: Java 21 + Spring Boot 3.4.5
- **Frontend**: React 19.1.0 + Vite 6.3.5
- **Styling**: Sass + CSS Modules
- **HTTP Client**: Axios (configured in `frontend/src/config/api.config.js`)
- **WebSocket**: STOMP.js
- **Routing**: React Router v7
- **Icons**: Lucide React + React Icons
- **Charts**: Recharts
- **Internationalization**: i18next (config in `frontend/src/i18n.jsx`)
- **File Processing**: xlsx
- **Database**: PostgreSQL + Spring Data JPA
- **Storage**: MinIO (local) / Cloudflare R2 (production)
- **Authentication**: JWT + Role-based (13 roles)
- **Real-time**: WebSocket + STOMP
- **Build**: Maven (backend) + Vite (frontend) + Docker

## 📁 Project Structure (EXACT ACTUAL PATHS)
```
RockOps/
├── frontend/                                    # React frontend application
│   ├── package.json                            # Frontend dependencies
│   ├── src/
│   │   ├── components/                         # Reusable UI components
│   │   │   ├── common/                         # Shared common components
│   │   │   ├── equipment/                      # Equipment-specific components
│   │   │   └── procurement/                    # Procurement-specific components
│   │   ├── services/                           # API service classes
│   │   │   ├── hr/, merchant/, notification/   # Organized service directories
│   │   │   ├── payroll/, procurement/          # More service directories
│   │   │   ├── transaction/, warehouse/        # Additional service directories
│   │   │   └── *.js files                      # Individual service files
│   │   ├── pages/                              # Page components
│   │   │   ├── admin/, dashboards/, equipment/ # Page directories by module
│   │   │   ├── finance/, HR/, login/           # More page directories
│   │   │   ├── maintenance/, merchant/         # Additional page directories
│   │   │   ├── notification/, partners/       # More page directories
│   │   │   ├── payroll/, procurement/          # Additional page directories
│   │   │   ├── RelatedDocuments/, site/        # More page directories
│   │   │   └── warehouse/                      # Warehouse page directory
│   │   ├── styles/                             # Sass/CSS styling files
│   │   │   ├── cancel-modal-button.scss        # Specific component styles
│   │   │   ├── close-modal-button.scss         # Modal-related styles
│   │   │   ├── modal-styles.scss               # General modal styles
│   │   │   ├── primary-button.scss             # Button styles
│   │   │   ├── status-badges.scss              # Status indicator styles
│   │   │   ├── tabs.scss                       # Tab component styles
│   │   │   ├── textarea-styles.scss            # Form input styles
│   │   │   └── theme-variables.css             # CSS custom properties
│   │   ├── config/
│   │   │   └── api.config.js                   # Centralized API configuration
│   │   ├── contexts/                           # React contexts
│   │   │   ├── AuthContext.jsx                 # Authentication context
│   │   │   ├── JobPositionContext.jsx          # Job position management
│   │   │   ├── LanguageContext.jsx             # i18n language context
│   │   │   ├── SnackbarContext.jsx             # Notification context
│   │   │   └── ThemeContext.jsx                # UI theme context
│   │   ├── utils/                              # Frontend utilities
│   │   │   ├── apiClient.js                    # API client utilities
│   │   │   ├── errorHandler.js                 # Error handling utilities
│   │   │   ├── rbac.js                         # Role-based access control
│   │   │   └── roles.js                        # Role definitions
│   │   ├── constants/
│   │   │   └── documentTypes.js                # Document type constants
│   │   ├── assets/                             # Static assets
│   │   ├── App.jsx                             # Main App component
│   │   ├── App.css                             # Main app styles
│   │   ├── main.jsx                            # Entry point
│   │   ├── index.css                           # Global styles
│   │   └── i18n.jsx                            # Internationalization setup
│   ├── public/                                 # Static public assets
│   └── dist/                                   # Build output (ignored)
├── backend/                                    # Spring Boot backend
│   ├── src/main/java/com/example/backend/
│   │   ├── BackendApplication.java             # Main Spring Boot entry point
│   │   ├── authentication/                    # Auth-related classes
│   │   ├── config/                            # Configuration classes
│   │   ├── controllers/                       # REST endpoints
│   │   ├── services/                          # Business logic layer
│   │   │   ├── equipment/, finance/, hr/       # Organized service packages
│   │   │   ├── merchant/, notification/       # More service packages
│   │   │   ├── payroll/, procurement/          # Additional service packages
│   │   │   ├── site/, transaction/, warehouse/ # More service packages
│   │   │   └── *.java files                    # Individual service files
│   │   ├── models/                            # JPA entities
│   │   ├── dto/ & dtos/                       # Data transfer objects
│   │   ├── repositories/                      # Data access layer
│   │   ├── exceptions/                        # Custom exception classes
│   │   ├── events/                            # Event-driven components
│   │   └── utils/                             # Backend utilities
│   ├── src/main/resources/                    # Configuration files
│   │   ├── db/                                # Database migrations
│   │   ├── graphql-client/                    # GraphQL configurations
│   │   ├── application.properties             # Main configuration
│   │   ├── application-prod.properties        # Production configuration
│   │   └── application-docker.properties      # Docker configuration
│   ├── src/test/                              # Test classes
│   ├── target/                                # Maven build output (ignored)
│   └── pom.xml                                # Maven dependencies
├── deployment/                                 # Deployment configurations
├── multitenancy/                              # Multi-tenant related files
├── compose.yaml & compose-test.yaml           # Docker compose files
├── .cursorrules                               # Cursor AI configuration
├── generate-context.js                        # Context generator script
└── .gitignore                                 # Git ignore rules
```

## 🚨 CRITICAL RULES - ALWAYS FOLLOW

### 1. API Integration Rules
- **NEVER hard-code fetch requests** in pages or components
- **ALWAYS use the centralized API configuration** from `frontend/src/config/api.config.js`
- **ALWAYS** create and use service classes in `frontend/src/services/`
- **ORGANIZE services** by domain (hr/, procurement/, transaction/, etc.) when appropriate
- **ALWAYS** import services from the dedicated service files
- Example: `import EquipmentService from '../services/equipmentService';` then use `EquipmentService.getEquipment()`

### 2. Styling Consistency
- **ALWAYS use styles from `frontend/src/styles/` folder** for consistency
- **NEVER** write inline styles or create new CSS files without checking existing styles
- **USE existing style files** like `primary-button.scss`, `modal-styles.scss`, `status-badges.scss`
- **FOLLOW the theme variables** defined in `theme-variables.css`
- **CREATE new Sass files** following kebab-case naming convention
- Follow the established design system and color scheme

### 3. Component Reusability & Team Safety
- **IF creating something reusable, ALWAYS create a component** in `frontend/src/components/`
- **ORGANIZE components** by domain (`common/`, `equipment/`, `procurement/`) when appropriate
- **NEVER modify existing shared component interfaces** without team approval
- **CREATE wrapper components** instead of modifying existing shared components
- **USE composition patterns** to extend functionality without breaking existing usage
- **MAINTAIN backward compatibility** for all component prop interfaces
- **DOCUMENT component props and usage** in JSDoc format
- **CREATE new components** rather than modifying existing ones when in doubt

### 4. Multi-Developer Safety Rules (CRITICAL)
- **NEVER change how existing components are called** (prop names, interfaces, etc.)
- **NEVER remove or rename existing component props** without team coordination
- **NEVER modify existing service method signatures** without team approval
- **IF modification is needed**: Create a new component, service method, or wrapper
- **ALWAYS maintain backward compatibility** in all public interfaces
- **CREATE new service methods** instead of modifying existing ones when possible
- **DEPRECATE gracefully** by creating new methods and marking old ones as deprecated
- **EXTEND existing functionality** through composition, not modification
- **ISOLATE changes** to avoid affecting other developers' work

### 5. Task Isolation Rules (CRITICAL FOR TEAM SAFETY)
- **ONLY modify files relevant to the current task domain**
- **IF working on warehouse features**: NEVER modify hr/, finance/, procurement/ files
- **IF working on equipment features**: NEVER modify warehouse/, payroll/, merchant/ files
- **IF working on HR features**: NEVER modify equipment/, warehouse/, finance/ files
- **SCOPE changes** to the specific domain being worked on
- **AVOID cross-domain modifications** unless explicitly required
- **CREATE domain-specific utilities** instead of modifying shared ones
- **KEEP changes contained** within the relevant service packages and page directories

### 6. Error Handling & User Experience Rules (CRITICAL)
- **ALWAYS handle errors gracefully** with meaningful user messages
- **NEVER show raw server errors** (500, 400, etc.) to users
- **ALWAYS use SnackbarContext** from `frontend/src/contexts/SnackbarContext.jsx` for all user feedback
- **USE appropriate SnackbarContext methods**:
  - `showError()` for error messages
  - `showInfo()` for informational messages
  - `showSuccess()` for success confirmations
  - `showWarning()` for warnings
  - **For confirmations/actions**: Include action buttons (OK/Cancel, Yes/No, etc.)
- **PROVIDE specific, actionable error messages** instead of generic ones
- **TRANSLATE technical errors** into user-friendly language
- **HANDLE validation errors** with field-specific messages
- **SHOW loading states** during async operations
- **PROVIDE retry mechanisms** for failed operations when appropriate
- **INCLUDE action buttons** in snackbar when user confirmation is required

#### Error Message Examples:
- **Unique Constraint**: "Serial number must be unique. This serial number is already used by equipment [Equipment Name]"
- **Required Field**: "Equipment name is required and cannot be empty"
- **Invalid Format**: "Serial number must contain only letters and numbers"
- **Network Error**: "Unable to save equipment. Please check your connection and try again"
- **Permission Error**: "You don't have permission to create equipment. Please contact your administrator"

#### SnackbarContext Usage Patterns:

**For Errors:**
```javascript
import { useContext } from 'react';
import { SnackbarContext } from '../contexts/SnackbarContext';

const { showError } = useContext(SnackbarContext);

// Handle API errors
if (error.response?.status === 409) {
  showError(`Serial number must be unique. This serial number is already used by equipment ${existingEquipmentName}`);
}
```

**For Success Messages:**
```javascript
const { showSuccess } = useContext(SnackbarContext);
showSuccess('Equipment created successfully');
```

**For Informational Messages:**
```javascript
const { showInfo } = useContext(SnackbarContext);
showInfo('Equipment status has been updated');
```

**For Warnings:**
```javascript
const { showWarning } = useContext(SnackbarContext);
showWarning('This action cannot be undone');
```

**For Confirmations with Actions:**
```javascript
const { showError, showInfo } = useContext(SnackbarContext);

const handleDelete = () => {
  showInfo('Are you sure you want to delete this equipment?', {
    actions: [
      {
        label: 'Cancel',
        onClick: () => {}, // Close snackbar
        variant: 'secondary'
      },
      {
        label: 'Delete',
        onClick: async () => {
          try {
            await EquipmentService.deleteEquipment(equipmentId);
            showSuccess('Equipment deleted successfully');
          } catch (error) {
            showError('Failed to delete equipment. Please try again.');
          }
        },
        variant: 'danger'
      }
    ]
  });
};
```

**Complete Error Handling Pattern:**
```javascript
try {
  setLoading(true);
  const result = await EquipmentService.createEquipment(data);
  showSuccess('Equipment created successfully');
} catch (error) {
  if (error.response?.status === 409 && error.response?.data?.field === 'serialNumber') {
    showError(`Serial number must be unique. This serial number is already used by equipment ${error.response.data.existingEquipmentName}`);
  } else if (error.response?.status === 400) {
    showError(error.response.data.message || 'Please check your input and try again');
  } else if (error.response?.status === 403) {
    showError('You don\'t have permission to create equipment. Please contact your administrator');
  } else if (error.response?.status === 500) {
    showError('Server error occurred. Please try again later or contact support');
  } else {
    showError('Unable to create equipment. Please check your connection and try again');
  }
} finally {
  setLoading(false);
}
```

### 7. Documentation & File Management
- **ALWAYS document changes** in comments and commit messages
- **GENERATE documentation files** only when they genuinely help code understanding
- **AUTO-ADD all generated .md files** to .gitignore to avoid cluttering the repository
- **USE comment-based documentation** in code when possible instead of separate files
- **CREATE temporary analysis files** that are automatically ignored
- **EXPLAIN business logic** in service layer comments
- **DOCUMENT API endpoints** with proper annotations

### 8. Unused File Detection & Analysis
- **SCAN import statements** to identify unused components/services across frontend and backend
- **GENERATE temporary reports** (auto-gitignored) listing unused files by category
- **IDENTIFY orphaned files** with no references across the entire codebase
- **ANALYZE service dependencies** to find unused service methods
- **CHECK component usage** across all pages and other components
- **CATEGORIZE findings**: Definitely unused, Potentially unused, Needs review
- **NEVER delete files automatically** - only report findings in temporary analysis files
- **CREATE usage analysis reports** in `.cursor-temp/` directory
- **SUGGEST cleanup opportunities** but require manual confirmation for all deletions

### 9. Frontend Element Identification
- **ALWAYS use unique identifiers** for divs, classes, and components
- **USE descriptive and specific names** that indicate the page/component context
- **FOLLOW naming pattern**: `{pageName}-{componentType}-{purpose}`
- Examples:
  - `equipment-list-container`, `maintenance-form-wrapper`, `dashboard-stats-card`
  - `procurement-order-header`, `warehouse-transaction-row`, `finance-report-chart`
- **ADD data-testid attributes** for testing and easy identification
- **USE semantic HTML elements** with unique class names when possible

### 10. Testing Requirements (Backend)
- **ALWAYS create tests** for new backend components in `backend/src/test/`
- **TEST all edge cases** based on described scenarios
- **INCLUDE unit tests** for service layer methods
- **ADD integration tests** for controller endpoints
- **MOCK external dependencies** in tests
- **NEVER skip testing** for business-critical functionality
- **ALWAYS maintain frontend-backend synchronization** when making changes to either side
- **IF backend API changes are made**: Update corresponding frontend services and components
- **IF frontend requirements change**: Update backend endpoints, DTOs, and validation accordingly
- **ENSURE API contract consistency** between frontend services and backend endpoints
- **UPDATE both sides atomically** - never leave frontend and backend out of sync
- **VALIDATE integration** after any changes to either frontend or backend

#### Backend-to-Frontend Integration Pattern:
**When Backend Changes Are Made:**
1. **Update backend endpoint** (Controller, Service, Repository, Entity)
2. **Update corresponding DTO** if data structure changes
3. **Update frontend service** in `frontend/src/services/` to match new API
4. **Update frontend components** that use the changed service
5. **Update TypeScript interfaces** if applicable
6. **Test integration** to ensure frontend-backend communication works

**Example: Adding new field to Equipment**
```javascript
// 1. Backend: Add field to Equipment entity
@Entity
public class Equipment {
    // ... existing fields
    @Column(name = "maintenance_priority")
    private String maintenancePriority;
}

// 2. Backend: Update DTO
public class EquipmentDTO {
    // ... existing fields
    private String maintenancePriority;
}

// 3. Backend: Update Controller endpoint
@PostMapping("/equipment")
public ResponseEntity<EquipmentDTO> createEquipment(@RequestBody EquipmentDTO equipmentDTO) {
    // Updated to handle maintenancePriority
}

// 4. Frontend: Update service to send new field
// In frontend/src/services/equipmentService.js
class EquipmentService {
    static async createEquipment(equipmentData) {
        const response = await api.post('/equipment', {
            ...equipmentData,
            maintenancePriority: equipmentData.maintenancePriority // New field
        });
        return response.data;
    }
}

// 5. Frontend: Update component to include new field
// In frontend/src/components/equipment/EquipmentForm.jsx
const EquipmentForm = () => {
    const [formData, setFormData] = useState({
        // ... existing fields
        maintenancePriority: '' // New field
    });
}
```

#### Frontend-to-Backend Integration Pattern:
**When Frontend Requirements Change:**
1. **Identify new frontend requirements** (new fields, validation, endpoints)
2. **Update backend entities** to support new data requirements
3. **Create/update backend DTOs** for new data structures
4. **Update backend validation** to match frontend requirements
5. **Update/create backend endpoints** to support frontend operations
6. **Update backend services** to handle new business logic
7. **Test integration** to ensure backend supports frontend needs

**Example: Frontend needs equipment filtering by location**
```javascript
// 1. Frontend requirement: Filter equipment by location
// In frontend/src/services/equipmentService.js
class EquipmentService {
    static async getEquipmentByLocation(locationId) {
        const response = await api.get(`/equipment/location/${locationId}`);
        return response.data;
    }
}

// 2. Backend: Create new endpoint to support this
// In backend/src/main/java/com/example/backend/controllers/EquipmentController.java
@GetMapping("/equipment/location/{locationId}")
public ResponseEntity<List<EquipmentDTO>> getEquipmentByLocation(@PathVariable Long locationId) {
    List<EquipmentDTO> equipment = equipmentService.findByLocationId(locationId);
    return ResponseEntity.ok(equipment);
}

// 3. Backend: Update service to support location filtering
// In backend/src/main/java/com/example/backend/services/EquipmentService.java
public List<EquipmentDTO> findByLocationId(Long locationId) {
    List<Equipment> equipment = equipmentRepository.findByLocationId(locationId);
    return equipment.stream().map(this::convertToDTO).collect(Collectors.toList());
}

// 4. Backend: Update repository with new query
// In backend/src/main/java/com/example/backend/repositories/EquipmentRepository.java
List<Equipment> findByLocationId(Long locationId);
```

#### Integration Validation Checklist:
**After Any Frontend or Backend Change:**
- [ ] **API endpoints** match between frontend services and backend controllers
- [ ] **Data structures** (DTOs) are consistent between frontend and backend
- [ ] **Validation rules** are synchronized (frontend validation matches backend validation)
- [ ] **Error handling** covers all backend error responses in frontend
- [ ] **Success responses** are properly handled in frontend
- [ ] **Loading states** are implemented for all async operations
- [ ] **User feedback** is provided through SnackbarContext for all operations

#### Common Integration Scenarios:
**New Feature Development:**
1. **Plan API contract** first (endpoints, data structures, error responses)
2. **Implement backend** (Entity → Repository → Service → Controller → DTO)
3. **Update frontend service** to match new API
4. **Create/update frontend components** to use new service
5. **Test end-to-end integration**

**Existing Feature Modification:**
1. **Identify impact** on both frontend and backend
2. **Update backend** with new requirements (maintain backward compatibility when possible)
3. **Update frontend** to use new backend capabilities
4. **Ensure error handling** covers new scenarios
5. **Test integration thoroughly**

**Error Response Synchronization:**
- **Backend error responses** must be handled in frontend services
- **Frontend error handling** must cover all possible backend error scenarios
- **Error messages** should be consistent and user-friendly
- **HTTP status codes** should be properly interpreted by frontend

#### Integration Anti-Patterns to Avoid:
- **DON'T** update only frontend without considering backend impact
- **DON'T** update only backend without updating corresponding frontend code
- **DON'T** leave API contracts inconsistent between frontend and backend
- **DON'T** skip testing integration after changes
- **DON'T** forget to update error handling when API responses change
- **DON'T** leave frontend services calling non-existent backend endpoints
- **DON'T** ignore validation synchronization between frontend and backend

## 🎯 Development Patterns

### Backend Development Pattern
1. **Entity**: Create JPA entity in `backend/src/main/java/com/example/backend/models/`
2. **Repository**: Extend JpaRepository in `backend/src/main/java/com/example/backend/repositories/`
3. **Service**: Implement business logic in `backend/src/main/java/com/example/backend/services/`
   - Use organized packages (`equipment/`, `finance/`, `hr/`, etc.) for complex domains
   - Place simple services directly in `services/` directory
   - **IMPLEMENT proper error handling** with meaningful exception messages
   - **THROW custom exceptions** for business logic violations (e.g., duplicate serial numbers)
4. **Controller**: Create REST endpoints in `backend/src/main/java/com/example/backend/controllers/`
   - **HANDLE validation errors** with specific field-level messages
   - **RETURN meaningful error responses** instead of generic server errors
5. **DTO**: Create data transfer objects in `backend/src/main/java/com/example/backend/dto/` or `dtos/`
6. **Tests**: Write comprehensive tests in `backend/src/test/`

### Frontend Development Pattern
1. **API Config**: Use centralized configuration from `frontend/src/config/api.config.js`
2. **Services**: Create service classes in `frontend/src/services/`
   - Organize by domain in subdirectories when appropriate
   - Use consistent naming: `{domain}Service.js`
   - **IMPLEMENT comprehensive error handling** in all service methods
   - **PARSE backend error responses** and transform to user-friendly messages
3. **Components**: Create reusable components in `frontend/src/components/`
   - Organize by domain (`common/`, `equipment/`, `procurement/`)
   - Use React 19 features and hooks
   - **INTEGRATE SnackbarContext** for error and success messages
   - **SHOW loading states** during async operations
   - **ENSURE integration** with updated backend APIs when services change
4. **Pages**: Create page components in `frontend/src/pages/`
   - Organize by module/domain
   - Use services and components, no direct API calls
   - **HANDLE form validation errors** with specific field messages
   - **PROVIDE user feedback** for all operations
5. **Styles**: Use Sass files in `frontend/src/styles/`
   - Leverage existing styles like `primary-button.scss`, `modal-styles.scss`
   - Follow theme variables from `theme-variables.css`
6. **Contexts**: Use React contexts from `frontend/src/contexts/` for state management
7. **Utils**: Place utility functions in `frontend/src/utils/`
8. **Constants**: Define constants in `frontend/src/constants/`

### Authentication & Authorization
- Use JWT tokens via authentication classes in `backend/src/main/java/com/example/backend/authentication/`
- Frontend auth context: `frontend/src/contexts/AuthContext.jsx`
- Roles defined in `frontend/src/utils/roles.js`
- RBAC utilities in `frontend/src/utils/rbac.js`
- Protected endpoints use `@PreAuthorize("hasRole('ROLE_NAME')")`
- Frontend: Check user roles before rendering components using contexts

### WebSocket Integration
- Use STOMP.js client for WebSocket connections
- Backend config in `backend/src/main/java/com/example/backend/config/`
- Frontend notification context: `frontend/src/contexts/SnackbarContext.jsx`
- Send notifications via NotificationService
- Topics: `/user/queue/notifications` (personal), `/topic/notifications` (broadcast)
- Always handle connection errors and reconnection logic
- Use React hooks to manage WebSocket state
- Implement proper cleanup in useEffect cleanup functions

## 🏢 Business Logic Rules

### Equipment Management
- Equipment status flow: AVAILABLE → IN_MAINTENANCE → AVAILABLE
- All equipment operations must be site-specific
- Track equipment location and assignment history
- Equipment services in `frontend/src/services/equipmentService.js`
- Equipment components in `frontend/src/components/equipment/`
- Equipment pages in `frontend/src/pages/equipment/`

### Maintenance Workflow
1. Create MaintenanceRecord with proper validation
2. Add MaintenanceSteps with assigned technicians
3. Update equipment status during maintenance
4. Complete maintenance and return equipment to service
5. Send real-time notifications for status changes
- Maintenance services in `frontend/src/services/maintenanceService.js` and `inSiteMaintenanceService.js`
- Maintenance pages in `frontend/src/pages/maintenance/`

### Multi-Site Architecture
- **ALL entities must be site-specific**
- **Users are assigned to specific sites**
- **Implement data isolation per site**
- **Validate site access in all operations**
- Site services in `frontend/src/services/siteService.js`
- Site pages in `frontend/src/pages/site/`

## 🔧 Code Quality Standards

### Java/Spring Boot
- Use Spring Boot annotations correctly (`@Service`, `@Controller`, `@Entity`)
- Implement proper exception handling using classes in `backend/src/main/java/com/example/backend/exceptions/`
- Use dependency injection instead of static methods
- Follow REST API conventions (GET, POST, PUT, DELETE)
- Validate input using Bean Validation annotations
- Organize services in domain packages when complexity warrants it

### Frontend Best Practices
- Use React 19 features (automatic batching, concurrent features)
- Use Vite for fast development and building
- **IMPLEMENT comprehensive error handling** for all Axios API calls using `frontend/src/utils/errorHandler.js`
- **ALWAYS use appropriate SnackbarContext hook** (`useSnackbar`) for user feedback
- **USE proper snackbar methods**: `showError`, `showSuccess`, `showInfo`, `showWarning`, `showConfirmation`
- **INCLUDE confirmations** for destructive actions using `showConfirmation`
- **SHOW loading states** during all async operations
- **PROVIDE meaningful error messages** translated from backend responses
- Use React Router v7 for navigation
- Leverage Sass for styling with proper organization in `frontend/src/styles/`
- Use React hooks appropriately (useState, useEffect, useContext)
- Handle WebSocket connection states gracefully with STOMP.js
- Use i18next for internationalization (config in `frontend/src/i18n.jsx`)
- Utilize contexts from `frontend/src/contexts/` for state management
- Use API client utilities from `frontend/src/utils/apiClient.js`

#### Required Error Handling Pattern for All Frontend Operations:
```javascript
import { useContext } from 'react';
import { SnackbarContext } from '../contexts/SnackbarContext';

const MyComponent = () => {
  const { showSnackbar } = useContext(SnackbarContext);

  const handleSubmit = async (data) => {
    try {
      setLoading(true);
      const result = await SomeService.createItem(data);
      showSnackbar('Item created successfully', 'success');
    } catch (error) {
      // Handle specific errors with meaningful messages
      if (error.response?.status === 409) {
        showSnackbar('This item already exists. Please use a different identifier.', 'error');
      } else if (error.response?.status === 400) {
        const message = error.response.data?.message || 'Please check your input and try again';
        showSnackbar(message, 'error');
      } else {
        showSnackbar('Unable to create item. Please try again later.', 'error');
      }
    } finally {
      setLoading(false);
    }
  };
};
```

## 📝 File Naming Conventions
- **Backend Entities**: PascalCase in `models/` (e.g., `Equipment.java`, `MaintenanceRecord.java`)
- **Backend Services**: PascalCase + Service in `services/` (e.g., `EquipmentService.java`)
- **Backend Controllers**: PascalCase + Controller in `controllers/` (e.g., `EquipmentController.java`)
- **Backend DTOs**: PascalCase + DTO/Request/Response in `dto/` or `dtos/` (e.g., `EquipmentDTO.java`)
- **Frontend Components**: PascalCase in `components/` (e.g., `EquipmentCard.jsx`)
- **Frontend Pages**: PascalCase in `pages/` (e.g., `EquipmentDashboard.jsx`)
- **Frontend Services**: camelCase + Service in `services/` (e.g., `equipmentService.js`)
- **Sass files**: kebab-case in `styles/` (e.g., `equipment-card.scss`, `dashboard-layout.scss`)
- **Utility files**: camelCase in `utils/` (e.g., `formatUtils.js`, `validationHelpers.js`)
- **Context files**: PascalCase + Context in `contexts/` (e.g., `AuthContext.jsx`)

## 🚫 What NOT to Do
- **DON'T** hard-code API URLs or endpoints (use `frontend/src/config/api.config.js`)
- **DON'T** create inline styles or bypass the `frontend/src/styles/` folder
- **DON'T** duplicate code that could be a reusable component
- **DON'T** modify existing shared component interfaces without team approval
- **DON'T** change existing service method signatures without coordination
- **DON'T** commit code without proper tests (backend)
- **DON'T** ignore site-specific data isolation rules
- **DON'T** create endpoints without proper authentication/authorization
- **DON'T** forget to handle WebSocket connection errors
- **DON'T** use generic class names like 'container', 'wrapper', 'content' without context
- **DON'T** reuse the same class names across different pages/components
- **DON'T** skip input validation on API endpoints
- **DON'T** delete unused files without manual confirmation
- **DON'T** create documentation files that will clutter the repository
- **DON'T** break backward compatibility for other developers
- **DON'T** show raw server errors to users (500, 400, etc.)
- **DON'T** modify files outside the current task domain
- **DON'T** skip error handling in service methods
- **DON'T** forget to provide user feedback for operations
- **DON'T** work on cross-domain features without explicit requirements

## 🔍 Accurate File Locations for Quick Reference
- **Main Spring Boot App**: `backend/src/main/java/com/example/backend/BackendApplication.java`
- **Backend Config**: `backend/src/main/java/com/example/backend/config/`
- **Database Config**: `backend/src/main/resources/application.properties`
- **API Configuration**: `frontend/src/config/api.config.js`
- **Frontend Services**: `frontend/src/services/`
- **Frontend Components**: `frontend/src/components/`
- **Frontend Styles**: `frontend/src/styles/`
- **React Contexts**: `frontend/src/contexts/`
- **Frontend Utils**: `frontend/src/utils/`
- **Available Style Files**: `primary-button.scss`, `modal-styles.scss`, `status-badges.scss`, `theme-variables.css`

## 📊 Auto-Generated Documentation Management

### Cursor Documentation Rules
- **AUTO-ADD to .gitignore**: All generated documentation files
- **CREATE temporary analysis files** in `.cursor-temp/` directory
- **GENERATE reports** for unused files, component usage, dependency analysis
- **USE meaningful filenames** for generated reports: `unused-files-YYYY-MM-DD.md`
- **AVOID creating permanent documentation files** that clutter the repository
- **DOCUMENT in code comments** when possible instead of separate files

### Auto-Gitignore Patterns for Generated Files
```gitignore
# Cursor AI generated documentation (auto-added)
*.cursor-analysis.md
*-documentation.md
*-analysis-*.md
.cursor-temp/
analysis-*.md
component-usage-*.md
unused-files-*.md
dependency-analysis-*.md
code-structure-*.md
service-usage-*.md
component-dependency-*.md
```

## 🎯 When Making Changes
1. **Check existing patterns** before implementing new solutions
2. **Use the established architecture** (Entity → Repository → Service → Controller)
3. **Follow the service pattern** for frontend-backend communication
4. **Reuse existing components** and styles where possible
5. **CREATE new components/services** instead of modifying shared ones
6. **Write tests first** for complex business logic
7. **Document the reasoning** behind architectural decisions
8. **Validate site-specific access** in all operations
9. **Update relevant documentation** when adding new features
10. **NEVER break existing component interfaces** without team coordination
11. **ISOLATE changes** to the relevant domain (equipment, warehouse, hr, etc.)
12. **MAINTAIN backward compatibility** at all times
13. **IMPLEMENT proper error handling** with SnackbarContext for user feedback
14. **SCOPE modifications** to only files relevant to the current task
15. **PROVIDE loading states** for all async operations
16. **TRANSLATE technical errors** into user-friendly messages

## 🔄 Real-time Features
- Equipment status changes trigger WebSocket notifications
- Maintenance updates are broadcast to relevant users
- Site-specific notifications are sent to appropriate channels
- Always handle WebSocket reconnection scenarios
- Use STOMP.js for WebSocket communication
- Notification context available at `frontend/src/contexts/SnackbarContext.jsx`

## 🧹 Unused File Detection Protocol
1. **SCAN all import statements** across frontend (`frontend/src/`) and backend (`backend/src/`)
2. **IDENTIFY files with no incoming references** in the entire codebase
3. **ANALYZE service method usage** across all service files
4. **CHECK component usage** across all pages and components
5. **EXAMINE style file usage** across all components and pages
6. **GENERATE temporary report** in `.cursor-temp/unused-files-YYYY-MM-DD.md`
7. **CATEGORIZE findings**:
   - **Definitely unused**: No references found anywhere
   - **Potentially unused**: Only referenced in comments or documentation
   - **Needs review**: References found but may be obsolete
   - **Keep**: Active usage confirmed
8. **SUGGEST cleanup actions** but require manual confirmation
9. **NEVER auto-delete** any files
10. **UPDATE gitignore** to include the analysis report

## 🤝 Team Collaboration Guidelines
- **COMMUNICATE before making breaking changes** to shared components or services
- **CREATE wrapper components** to extend functionality without affecting existing usage
- **USE composition over modification** for extending existing functionality
- **DEPRECATE gradually** by creating new interfaces while maintaining old ones
- **DOCUMENT breaking changes** thoroughly before implementing
- **TEST backward compatibility** when extending existing functionality
- **COORDINATE with team** before removing or significantly modifying shared code

Remember: The goal is to maintain consistency, reusability, and proper separation of concerns while ensuring the system remains scalable and maintainable for a mining site management context. Always prioritize team collaboration and backward compatibility over quick fixes. Protect your colleagues' work by creating new solutions rather than modifying existing shared code.