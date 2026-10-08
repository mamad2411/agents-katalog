---
name: create
description: Quick wizard to create a new Pine Script from a description. Just describe what you want and get working code.
disable-model-invocation: true
argument-hint: [description]
---

# Quick Pine Script Creation

Creating new Pine Script from your description: $ARGUMENTS

## Implementation Steps

1. **Analyze the request** to determine:
   - Type: Indicator or Strategy?
   - Complexity: Simple, Medium, or Complex?
   - Key components needed

2. **Check for relevant templates** in:
   - `templates/indicators/` - For indicator patterns
   - `templates/strategies/` - For strategy patterns
   - `templates/utilities/` - For helper functions

3. **Create the file** at `projects/[descriptive-name].pine`

4. **Implement with best practices**:
   - `//@version=6` declaration
   - `//@strategy_alert_message` for strategies (after the `strategy()` call)
   - Proper input groups and tooltips
   - NA value handling
   - No repainting issues

5. **Add basic debugging** if helpful

## Quick Implementation Patterns

**For Indicators**:
```pinescript
//@version=6
indicator("Title", overlay=true)
// Implementation
```

**For Strategies**:
```pinescript
//@version=6
strategy("Title", overlay=true)
//@strategy_alert_message {{strategy.order.alert_message}}
// Implementation
```

## Quality Checklist

Before delivering:
- [ ] Compiles without errors
- [ ] Handles NA values
- [ ] Uses cached loop boundaries
- [ ] Ternary operators on single lines
- [ ] Inputs have tooltips
