# WorkConnect - Cursor Project Rules
# Maintains consistent code organization and architecture patterns

## 📁 Project Structure Rules

### Directory Organization
- **ALWAYS** follow the modular architecture pattern:
  - `src/frontend/app/modules/{module-name}/{components,pages,services,styles}`
  - `src/backend/src/modules/{module-name}/{controllers,services,models,routes,middleware}`
  - `src/database/{migrations,schemas,seeds,triggers,views,functions,scripts}`
  - `docs/{architecture,diagrams,compliance,guides,requirements,presentation}`

### File Naming Conventions
- **Frontend JavaScript**: Use PascalCase for services (e.g., `DashboardService.js`), camelCase for utilities
- **HTML Pages**: Use PascalCase (e.g., `DashboardPage.html`)
- **CSS Files**: Use kebab-case (e.g., `dashboard-enhanced.css`)
- **Backend Files**: Use camelCase for services/controllers, PascalCase for models
- **Database Files**: Use snake_case with descriptive prefixes (e.g., `001_initial_schema.sql`)

### Module Organization
Each module MUST have:
- `components/` - Reusable UI components specific to the module
- `pages/` - Page-level components/HTML
- `services/` - Business logic and API interactions
- `styles/` - Module-specific styles (if needed)

### Shared Code
- **ALWAYS** place shared utilities in `src/frontend/app/shared/utils/`
- **ALWAYS** place shared components in `src/frontend/app/shared/components/`
- **ALWAYS** place shared services in `src/frontend/app/shared/services/`
- **NEVER** duplicate code across modules - extract to shared when used in 2+ places

### Core Functionality
- Authentication: `src/frontend/app/core/auth/`
- Routing: `src/frontend/app/core/routing/`
- State Management: `src/frontend/app/core/state/`
- API Client: `src/frontend/app/core/api/`

### Assets Organization
- Images: `src/frontend/assets/images/`
- Icons: `src/frontend/assets/icons/`
- Fonts: `src/frontend/assets/fonts/`
- Global Styles: `src/frontend/assets/styles/{base,components,themes,utilities}/`

### Documentation
- Architecture docs: `docs/architecture/`
- Diagrams: `docs/diagrams/{classes,database,use-cases}/`
- Compliance: `docs/compliance/`
- Guides: `docs/guides/`
- Requirements: `docs/requirements/`
- Presentation: `docs/presentation/`

## 🎯 Code Organization Principles

### 1. Feature-Based Structure
- Group files by feature/module, not by file type
- Each module is self-contained with its own components, services, and styles
- Modules communicate through shared services or events

### 2. Separation of Concerns
- **Services**: Business logic, API calls, data manipulation
- **Components**: UI rendering and user interaction
- **Pages**: Page-level composition and routing
- **Styles**: Visual presentation (scoped to module or global)

### 3. Dependency Direction
```
Pages → Components → Services → API/Storage
```
- Pages depend on Components
- Components depend on Services
- Services depend on API/Storage
- **NEVER** reverse this dependency flow

### 4. Import Path Rules
- Use relative paths for same-module imports: `./Component.js`
- Use absolute paths from `src/frontend/app/` for cross-module: `@/shared/utils/common.js`
- Use `@/core/` for core functionality: `@/core/auth/auth.js`
- Use `@/assets/` for assets: `@/assets/styles/base/variables.css`

## 📝 Code Style Guidelines

### JavaScript
- Use ES6+ features (const/let, arrow functions, destructuring)
- Use meaningful variable and function names
- Add JSDoc comments for public functions
- Keep functions small and focused (single responsibility)
- Use async/await for asynchronous operations

### HTML
- Use semantic HTML5 elements
- Include proper ARIA labels for accessibility
- Keep HTML structure clean and readable
- Use data attributes for JavaScript hooks (e.g., `data-module="dashboard"`)

### CSS
- Use CSS custom properties (variables) for theming
- Follow BEM naming convention for component styles
- Keep styles scoped to components when possible
- Use utility classes for common patterns

## 🔧 Configuration Files

### Package.json
- Keep scripts organized by purpose (dev, build, test, deploy)
- Group dependencies logically (dependencies, devDependencies)
- Use semantic versioning

### Vite Config
- Located at: `src/frontend/config/vite.config.js`
- Configure path aliases for `@/` imports
- Set up proper build outputs

## 🚫 Anti-Patterns to Avoid

1. **DON'T** create files in root `src/` directory
2. **DON'T** mix frontend and backend code
3. **DON'T** put business logic in components
4. **DON'T** create circular dependencies between modules
5. **DON'T** duplicate code - extract to shared
6. **DON'T** use global variables - use modules/services
7. **DON'T** hardcode paths - use configuration
8. **DON'T** commit build artifacts or node_modules

## ✅ When Adding New Features

1. **Identify the module** (or create new one if needed)
2. **Create service** in `{module}/services/` for business logic
3. **Create components** in `{module}/components/` for UI
4. **Create page** in `{module}/pages/` if it's a full page
5. **Add styles** in `{module}/styles/` if module-specific
6. **Update routing** in `core/routing/` if needed
7. **Add tests** in `tests/` directory
8. **Update documentation** in `docs/` if needed

## 📚 Documentation Requirements

- **ALWAYS** update README.md when adding major features
- **ALWAYS** document API changes in `docs/architecture/`
- **ALWAYS** update diagrams when database schema changes
- **ALWAYS** add JSDoc comments for public APIs

## 🔍 Code Review Checklist

Before submitting code, ensure:
- [ ] Files are in correct directory structure
- [ ] No circular dependencies
- [ ] Shared code is in `shared/` directory
- [ ] Module-specific code is in module directory
- [ ] Imports use correct paths
- [ ] No hardcoded values (use constants/config)
- [ ] Code follows naming conventions
- [ ] Documentation is updated if needed

## 🎨 Module Examples

### Dashboard Module
```
src/frontend/app/modules/dashboard/
├── components/
│   ├── ChartCard.js
│   └── MetricCard.js
├── pages/
│   └── DashboardPage.html
├── services/
│   └── dashboardService.js
└── styles/
    └── dashboard.css
```

### Estoque Module
```
src/frontend/app/modules/estoque/
├── components/
│   ├── ProductList.js
│   ├── ProductForm.js
│   └── StockAlert.js
├── pages/
│   └── EstoquePage.html
├── services/
│   └── estoqueService.js
└── styles/
    └── estoque.css
```

## 🔄 Migration Notes

- Old structure files are preserved in `app/` directory
- New structure is in `src/` directory
- Gradually migrate references from old to new paths
- Update build configurations to use new paths
- Test thoroughly after migration

## 📖 Additional Resources

- See `docs/architecture/` for detailed architecture documentation
- See `docs/guides/` for development guides
- See `ROADMAP.md` for project roadmap

## 📋 Additional Organization Rules

### Root Directory
- **ONLY** essential files in root: `README.md`, `package.json`, `.gitignore`, `.cursorrules`, `CHANGELOG.md`, `ROADMAP.md`
- **ALL** documentation goes to `docs/`
- **ALL** source code goes to `src/`
- **ALL** scripts go to `scripts/`
- **ALL** configuration goes to `config/`

### File Placement
- **Screenshots/Images**: `src/frontend/assets/images/`
- **Server Files**: `scripts/server/`
- **Database Scripts**: `src/database/scripts/`
- **Presentation Materials**: `docs/presentation/`
- **Meta Documentation**: `docs/meta/`

### Naming Consistency
- Use kebab-case for directories
- Use PascalCase for component files
- Use camelCase for utility files
- Use descriptive names (avoid abbreviations)

---

**Last Updated**: 2025-01-12
**Version**: 2.0.0

