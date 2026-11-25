# ICDBolt Project Rules

## UI/UX Standards

### Color Palette (Medical Trust)
- **Primary Navigation**: Use Tailwind `primary` color which maps to `#103766` (Dark Blue)
- **Secondary Highlights**: Use `accent` color which maps to `#2E865F` (Sage Green)
- **All UI components MUST use the Tailwind color system**: Use semantic color tokens (`primary`, `accent`, `destructive`, `muted`, etc.) instead of hardcoded hex values
- **WCAG 2.1 AA Compliance**: All text-to-background contrast ratios must meet or exceed 4.5:1
- **Typography**: Use Inter font stack (IBM Plex Sans as fallback)
- **Enterprise Healthcare Aesthetic**: Clean, minimalist design with no playful/neon effects

### Component Design Principles
- Use Tailwind CSS utility classes exclusively
- Avoid inline styles; use Tailwind classes
- Maintain consistent spacing using Tailwind spacing scale
- Use semantic HTML elements with proper accessibility attributes
- All interactive elements must have focus states and keyboard navigation

## Code Documentation

### JSDoc Requirements
- **ALL billing logic functions MUST have JSDoc comments** including:
  - Function description
  - `@param` tags for all parameters with types and descriptions
  - `@returns` tag with return type and description
  - `@throws` tags for error conditions (if applicable)
  - `@example` tags for complex functions

Example:
```typescript
/**
 * Calculates DRG-based reimbursement estimate based on code selections and region.
 * 
 * @param codes - Array of code selections (primary diagnosis + comorbidities)
 * @param region - Geographic region for DRG calculation (US, MY, AU, KSA, UAE, EU)
 * @returns DRGCalculationResult with estimated reimbursement, or null if no codes provided
 * 
 * @example
 * const result = calculateDRGReimbursement(
 *   [{ code: 'E11.9', description: 'Type 2 diabetes', isPrimary: true }],
 *   'US'
 * )
 */
```

### TypeScript Standards
- Use strict TypeScript typing; avoid `any`
- Define interfaces for all data structures
- Use union types for enums/constants
- Export types/interfaces that are used across modules

## HIPAA/Regulatory Compliance

### PHI (Protected Health Information) Handling
- **NEVER log PHI data** (patient names, dates of birth, SSNs, medical record numbers, etc.)
- **NEVER include PHI in console.log, console.error, or any logging statements**
- Use sanitized identifiers or hashed values if logging is necessary
- All logging functions must strip PHI before writing to logs
- Use structured logging that excludes sensitive fields

### Data Handling Rules
- All clinical data processing must happen server-side when possible
- Client-side data must be cleared from memory after use
- Never store PHI in localStorage, sessionStorage, or cookies (except encrypted session tokens)
- Use secure, encrypted connections for all API calls

### Audit Trail Requirements
- All code selections must be logged to audit trail (without PHI)
- Include timestamps, user IDs, and code selections (not patient data)
- Audit logs must be immutable and permanent

### Error Handling
- Error messages must not expose PHI or internal system details
- Use generic error messages for production
- Detailed errors only in development mode with proper guards

## Code Quality Standards

### React/Next.js Patterns
- Use functional components with hooks
- Use TypeScript for all components
- Implement proper error boundaries
- Use Next.js App Router patterns correctly
- Handle SSR/client-side hydration mismatches properly

### File Organization
- Keep components in `/components` directory
- Keep utilities in `/lib` directory
- Keep types in `/types` directory or co-located with components
- Use consistent naming: PascalCase for components, camelCase for functions

### Testing Requirements
- Write unit tests for all billing/revenue calculation functions
- Include edge cases and error scenarios
- Mock external dependencies
- Test accessibility requirements

### Performance
- Use React.memo for expensive components
- Implement proper loading states
- Use Next.js Image component for images
- Optimize bundle size

## Regional Compliance

### Regional Coding Standards
- Respect regional ICD-10 variants (ICD-10-AM for Australia, SBS-9 for KSA, etc.)
- Implement region-specific validation logic
- Support regional DRG systems (MY-DRG for Malaysia, etc.)
- Use region-appropriate base rates and currency formatting

### Data Residency
- Respect data sovereignty laws (KSA, UAE, etc.)
- Never process data across regional boundaries
- Use regional database instances based on tenant configuration

## Security Best Practices

### Authentication & Authorization
- Use JWT tokens for API authentication
- Implement role-based access control (RBAC)
- Validate user permissions on both client and server
- Never expose authentication tokens in URLs or logs

### Input Validation
- Validate all user inputs on the client and server
- Sanitize inputs before processing
- Use TypeScript types to catch validation errors at compile time

## Business Logic Rules

### Billing/Revenue Logic
- All DRG calculations must be documented with JSDoc
- Include confidence scores and validation results
- Flag unspecified codes (.9 endings) as audit risks
- Calculate comorbidity adjustments correctly

### Code Selection
- Provide clinical rationale for all code suggestions
- Include evidence snippets from clinical notes
- Flag laterality mismatches
- Warn about unspecified codes

## Git & Code Management

### Commit Messages
- Use clear, descriptive commit messages
- Reference ticket/issue numbers when applicable
- Separate subject from body with blank line

### Code Reviews
- All code changes require review
- Check for PHI in logs/comments
- Verify JSDoc on billing functions
- Confirm UI uses correct color palette

## Examples of What NOT to Do

```typescript
// ❌ BAD: Hardcoded color
<div style={{ backgroundColor: '#103766' }}>

// ✅ GOOD: Use Tailwind semantic token
<div className="bg-primary">

// ❌ BAD: Logging PHI
console.log('Patient:', patient.name, 'DOB:', patient.dob)

// ✅ GOOD: Log sanitized data
console.log('Processing code selection for user:', userId)

// ❌ BAD: Missing JSDoc on billing function
function calculateReimbursement(codes) { ... }

// ✅ GOOD: Complete JSDoc documentation
/**
 * Calculates reimbursement based on DRG weights and base rates.
 * @param codes - Array of ICD-10 code selections
 * @returns Estimated reimbursement amount
 */
function calculateReimbursement(codes: CodeSelection[]): number { ... }
```

## Additional Notes

- When in doubt, prioritize security and compliance over convenience
- Follow the principle of least privilege for data access
- Maintain clear separation between clinical logic and presentation logic
- Use TypeScript to catch errors at compile time rather than runtime
- Keep components small and focused on a single responsibility

