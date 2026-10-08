# Cursor Rules for Sonari Project

## Critical Spacing and Typography Rules

### Root Font Size and Tailwind Spacing Scale

- **CRITICAL**: The root font size in this project is 16px
- This means Tailwind's spacing scale is based on 16px:
  - `gap-1` = 4px
  - `gap-2` = 8px
  - `gap-4` = 16px
  - `gap-8` = 32px
  - etc.
- Always consider this when using Tailwind spacing classes

### React Native Flexbox Rules

- **CRITICAL**: React Native flexbox behavior is different from web CSS
- ALWAYS specify `flex-row` or `flex-col`, never use just `flex` alone
- Use `flex flex-row` or `flex flex-col` explicitly

### Theme Compatibility

- **CRITICAL**: All screens and components MUST be dark and light mode compatible
- Use Tailwind theme classes instead of inline styles for colors
- Use classes like `bg-background`, `text-foreground`, `text-muted-foreground`, `bg-primary`, etc.
- NEVER use inline style colors

### Component Naming

- All components created for this project must be prefixed with `sonari-`
- Example: `sonari-splash-button`, `sonari-animated-image-grid`

### Icons

- Always use Lucide React Native icons instead of custom SVG files
- Import from `lucide-react-native` for consistent, scalable icons

### Responsive Design

- Use responsive utilities (`wp`, `hp`, etc.) for sizing instead of fixed pixel values
- These utilities are found in `utils/responsive.ts`

### Code Style

- Avoid unnecessary comments in the codebase
- Write concise, technical TypeScript code
- Use functional and declarative programming patterns
- Follow Expo's official documentation and best practices
