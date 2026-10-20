---
description: Mermaid Diagram Syntax Rules - Critical rules for preventing rendering failures and ensuring diagrams render correctly
alwaysApply: false
---

# Mermaid Diagram Syntax Rules

## Critical Rules for Preventing Rendering Failures

### ❌ RULE 1: NEVER Put Style Statements Inside Subgraphs

**WRONG:**
```mermaid
flowchart TB
    subgraph Platform
        ServiceA[(Service A)]
        ServiceB[(Service B)]
        
        style ServiceA fill:#ffcccc     ← INSIDE subgraph - WILL FAIL!
        style ServiceB fill:#e6ccff     ← INSIDE subgraph - WILL FAIL!
    end
```

**CORRECT:**
```mermaid
flowchart TB
    subgraph Platform
        ServiceA[(Service A)]
        ServiceB[(Service B)]
    end
    
    style ServiceA fill:#ffcccc         ← OUTSIDE subgraph - WORKS!
    style ServiceB fill:#e6ccff         ← OUTSIDE subgraph - WORKS!
```

**Why:** Mermaid parser processes subgraphs first, then applies styles. Style statements inside subgraphs cause parsing errors and infinite rendering loops.

---

### ❌ RULE 2: NEVER Use Empty Arrow Labels

**WRONG:**
```mermaid
sequenceDiagram
    API1->>Service:      ← Empty label - WILL FAIL!
    Service->>External:          ← Empty label - WILL FAIL!
    External->>Service: response ← This one is OK
```

**CORRECT:**
```mermaid
sequenceDiagram
    API1->>Service: request       ← Has label - WORKS!
    Service->>External: /api/endpoint          ← Has label - WORKS!
    External->>Service: response                ← Has label - WORKS!
```

**Why:** Empty arrow labels confuse the parser and can cause rendering to hang or fail. Always provide descriptive text for every arrow.

---

### ❌ RULE 3: AVOID Nested Subgraphs with Long Labels

**PROBLEMATIC:**
```mermaid
flowchart TB
    subgraph MainComponents[Main Components]
        subgraph PublicAPI[Public API]           ← NESTED - May cause issues
            AuthAPI[Auth API]
        end
        subgraph InternalAPI[Internal API]       ← NESTED - May cause issues
            ServiceAPI[Service API]
        end
    end
```

**BETTER (Use Flat Structure):**
```mermaid
flowchart LR
    subgraph PublicAPI["Public API"]             ← NOT NESTED - Reliable
        AuthAPI[Auth API]
    end
    
    subgraph InternalAPI["Internal API"]         ← NOT NESTED - Reliable
        ServiceAPI[Service API]
    end
    
    PublicAPI --- InternalAPI
```

**Why:** Nested subgraphs with labels containing spaces can trigger Mermaid layout calculation bugs, causing infinite loops and browser hangs.

---

### ❌ RULE 4: Limit Line Breaks in Labels (Max 2-3)

**WRONG:**
```mermaid
flowchart TB
    A[Component<br/>router<br/>with<br/>additional<br/>info]  ← Too many <br/> tags!
    B -->|API<br/>get preference<br/>biller Id<br/>(id)<br/>return updated<br/>loanNumber| C  ← Way too complex!
```

**CORRECT:**
```mermaid
flowchart TB
    A[Component router]                  ← Simple, clear
    B -->|API: get preference and biller Id| C   ← Simplified, readable
```

**Why:** Excessive line breaks cause:
- Text overflow issues
- Layout calculation problems
- Rendering failures or hangs
- Poor readability

**Guideline:** If a label needs more than 2-3 line breaks, it's too complex. Simplify the text or use a Note instead.

---

### ❌ RULE 5: Declare All External Nodes Explicitly

**WRONG:**
```mermaid
flowchart TB
    subgraph Platform
        ServiceA[(Service A)]
    end
    
    ServiceA -->|call| ExternalService[External Service]  ← Declared inline - May cause issues
```

**CORRECT:**
```mermaid
flowchart TB
    subgraph Platform
        ServiceA[(Service A)]
    end
    
    ExternalService[External Service]              ← Declared explicitly first
    
    ServiceA -->|call| ExternalService               ← Then referenced
```

**Why:** Declaring nodes explicitly before referencing them ensures consistent parsing and prevents ambiguous node references.

---

### ✅ RULE 6: Use Sequential Rendering for Complex Documents

**For documents with 5+ diagrams or complex nested diagrams:**

```javascript
// Set startOnLoad: false
mermaid.initialize({ 
    startOnLoad: false,
    // ... other config
});

// Render one at a time with delays
function renderNext() {
    mermaid.render(id, content).then(success).catch(error);
    setTimeout(renderNext, 100);  // 100ms delay between diagrams
}
```

**Why:** Rendering all diagrams simultaneously can overwhelm the browser's rendering engine, especially with complex flowcharts or many sequence diagrams. Sequential rendering with delays prevents browser hangs.

---

## Best Practices Summary

### ✅ DO:
1. **Place style statements OUTSIDE subgraphs** (at the end of diagram)
2. **Provide labels for ALL arrows** (never leave blank after `:`)
3. **Keep labels concise** (max 2-3 `<br/>` tags)
4. **Flatten nested subgraphs** when possible
5. **Declare external nodes** explicitly before use
6. **Use sequential rendering** for documents with many/complex diagrams
7. **Test diagrams individually** before adding to large documents

### ❌ DON'T:
1. ❌ Put `style` statements inside `subgraph` blocks
2. ❌ Use empty arrow labels (`A->>B:` with nothing after)
3. ❌ Nest subgraphs with long labels containing spaces
4. ❌ Use excessive `<br/>` tags (more than 3)
5. ❌ Create overly complex labels on arrows
6. ❌ Use `startOnLoad: true` for documents with 10+ diagrams

---

## Diagram Validation Checklist

Before committing any Mermaid diagram, verify:

- [ ] All `style` statements are OUTSIDE subgraph blocks
- [ ] Every arrow has a descriptive label (no empty labels)
- [ ] Subgraphs are not nested more than 1 level deep
- [ ] Labels use max 2-3 `<br/>` tags
- [ ] All external nodes are declared explicitly
- [ ] Diagram renders without errors in HTML preview
- [ ] For 5+ diagrams: Sequential rendering is enabled

---

## Known Mermaid Parser Limitations

### Causes of Infinite Loops / Browser Hangs:
1. Style statements inside subgraphs
2. Deeply nested subgraphs with labeled nodes
3. Empty arrow labels in sequence diagrams
4. Rendering 10+ complex diagrams simultaneously

### Causes of Rendering Failures:
1. Excessive line breaks in labels (4+ `<br/>` tags)
2. Very long text in labels (200+ characters)
3. Inconsistent node declarations
4. Invalid syntax in style statements

---

## Testing Strategy

### Local Testing:
1. **Validate syntax** using Mermaid Live Editor: https://mermaid.live/
2. **Test in isolation** - Create a minimal HTML file with just one diagram
3. **Test sequentially** - Add diagrams one at a time to identify problematic ones
4. **Check browser console** - Look for Mermaid errors or warnings

### Integration Testing:
1. Generate HTML from markdown using conversion script
2. Open in browser and check console for "All X diagrams rendered"
3. Visually verify each diagram renders correctly
4. Test with browser cache disabled

---

## Recovery from Rendering Failures

If diagrams fail to render:

1. **Open browser DevTools Console** (F12) to see error messages
2. **Identify which diagram failed** (console shows diagram number)
3. **Check for common issues:**
   - Styles inside subgraphs?
   - Empty arrow labels?
   - Nested subgraphs?
   - Too many `<br/>` tags?
4. **Apply fixes** using rules above
5. **Regenerate HTML** and test again

---

## Remember

✅ **Styles Outside Subgraphs**: Always place style statements outside subgraph blocks  
✅ **No Empty Labels**: Every arrow must have a descriptive label  
✅ **Flatten Nested Subgraphs**: Avoid deep nesting when possible  
✅ **Limit Line Breaks**: Max 2-3 `<br/>` tags per label  
✅ **Explicit Node Declaration**: Declare external nodes before referencing  
✅ **Sequential Rendering**: For documents with 5+ diagrams, use sequential rendering  
✅ **Test Individually**: Test each diagram before adding to large documents
