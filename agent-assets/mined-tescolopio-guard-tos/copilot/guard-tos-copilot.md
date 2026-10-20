# GitHub Copilot Instructions for guard_tos Project

## Code Documentation Standards

### Timestamped Comments Requirement

**All code changes MUST include date-stamped comments using the format `YYYY-MM-DD`**

#### When to Add Timestamps

1. **File Headers**: When making significant updates to a file
   ```javascript
   /**
    * Sidepanel Controller
    * Last Updated: 2025-10-17
    * Changes: Updated to work with new HTML structure from interactive_demo.html
    */
   ```

2. **Function Modifications**: When updating existing functions
   ```javascript
   // 2025-10-17: Updated to use serviceName instead of termsTitle
   updateDocumentInfo(info) {
     // ...
   }
   ```

3. **Code Block Changes**: When modifying specific sections
   ```javascript
   // 2025-10-17: Simplified - new HTML structure doesn't have loadingIndicator element
   loadingManager = {
     // ...
   };
   ```

4. **Element Renames**: When updating DOM element references
   ```javascript
   // 2025-10-17: Updated to use new element names (rightsScore, confidence, readabilityScore, flagsContainer)
   updateSummaryMetrics(metrics) {
     // ...
   }
   ```

#### Timestamp Format

- **Required Format**: `YYYY-MM-DD` (e.g., `2025-10-17`)
- **Placement**: 
  - At the start of inline comments: `// 2025-10-17: Description`
  - In block comments: Use "Last Updated:" or "Updated:" prefix
  - In function docstrings: Add after main description

#### Examples

**Good ✅**
```javascript
// 2025-10-17: Update Rights Score card (renamed from summaryRightsScore)
if (this.elements.rightsScore) {
  this.elements.rightsScore.textContent = 
    typeof uriScore === 'number' ? Math.round(uriScore) : '--';
}
```

**Bad ❌**
```javascript
// Update Rights Score card
if (this.elements.rightsScore) {
  this.elements.rightsScore.textContent = 
    typeof uriScore === 'number' ? Math.round(uriScore) : '--';
}
```

### Best Practices

1. **Be Specific**: Include what changed and why
   - Good: `// 2025-10-17: Updated to use documentGrade instead of combinedGrade`
   - Bad: `// Updated element`

2. **Group Related Changes**: Use one timestamp comment for related modifications
   ```javascript
   // 2025-10-17: Excerpts feature not in new HTML structure - keeping for API compatibility but not rendering
   updateExcerpts(excerpts) {
     // ...
   }
   ```

3. **Update File Headers**: When making multiple changes in a file
   ```javascript
   /**
    * Last Updated: 2025-10-17
    * Changes: Updated to work with new HTML structure from interactive_demo.html
    */
   ```

4. **No Retroactive Timestamps**: Only add timestamps to new changes, don't modify existing timestamped comments

## Additional Standards

### File Organization
- Keep related functionality together
- Use clear, descriptive function names
- Follow existing code style

### Error Handling
- Always include try-catch blocks for async operations
- Log errors with descriptive messages
- Provide user-friendly fallbacks

### Testing
- Test changes with `npm run build` before committing
- Verify UI changes in the browser
- Check console for errors

## Current Date Reference

When asked to add timestamps, always confirm the current date with the user before proceeding. Do not assume or guess the date - **ask explicitly**.

Example: "Before I add timestamps, could you confirm today's date in YYYY-MM-DD format?"

---

*Last Updated: 2025-10-17*
*Purpose: Ensure clear tracking of code changes and progress visibility*
