# Architecture Review

Review changes for architectural consistency before implementation.

## Instructions

Before implementing significant changes, run this review:

1. **Schema Consistency** - Do changes follow data schema?
2. **Pattern Alignment** - Do changes match existing patterns?
3. **Layer Boundaries** - Are concerns properly separated?
4. **Dependencies** - Are new dependencies justified?

## Review Checklist

### Data Schema
- [ ] Properties use standard names (sd, ed, ev, src, bt, nm)
- [ ] Evidence levels are h/m/l
- [ ] Dates are integers (years)
- [ ] Coordinates are EPSG:4326

### MapLibre Patterns
- [ ] Filters use legacy syntax (not expression)
- [ ] Layers follow z-ordering convention
- [ ] Sources have attribution
- [ ] Popups follow standard format

### Python Patterns
- [ ] Scripts use argparse
- [ ] Scripts have --dry-run option
- [ ] Logging follows project style
- [ ] GeoJSON output is valid

### Frontend Patterns
- [ ] UI components use CSS variables
- [ ] State changes trigger layer updates
- [ ] Error states are handled
- [ ] Mobile responsive

## Common Issues

### Filter Syntax
```javascript
// WRONG - expression syntax
['<=', ['get', 'sd'], year]

// RIGHT - legacy filter syntax
['<=', 'sd', year]
```

### Property Naming
```javascript
// WRONG - inconsistent
{ start_date, endDate, evidence_level }

// RIGHT - standard schema
{ sd, ed, ev }
```

### Layer Ordering
```javascript
// WRONG - labels under polygons
addLayer('water-fill');
addLayer('water-label');  // will be hidden

// RIGHT - proper order
addLayer('water-fill');
addLayer('buildings-fill');  // on top
```

## Output Format

```markdown
## Architecture Review: [Change Description]

### Schema Consistency
- [x] Properties follow schema
- [ ] ISSUE: Using 'start_year' instead of 'sd'

### Pattern Alignment
- [x] Follows existing patterns
- [ ] ISSUE: Using expression filter syntax

### Recommendations
1. Rename start_year → sd
2. Use legacy filter syntax

### Approved: Yes/No (with conditions)
```
