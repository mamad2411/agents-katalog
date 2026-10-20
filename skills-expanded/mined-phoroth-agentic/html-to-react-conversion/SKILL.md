---
name: html-to-react-conversion
description: Expert in converting HTML to React JSX components. Covers all conversion rules, best practices, common pitfalls, and workflow patterns for migrating HTML to React.
risk: unknown
source: community
date_added: '2026-08-07'
---

## Use this skill when

- Converting HTML mockups to React components
- Migrating static HTML sites to React applications
- Learning JSX syntax and HTML-to-JSX differences
- Converting inline HTML to React components
- Needing guidance on attribute transformations
- Working with existing HTML templates in React projects

## Do not use this skill when

- Working with pure HTML without React conversion
- Task is unrelated to HTML/React conversion
- Needing server-side rendering (SSR) specific guidance
- Working with non-React frameworks

## Instructions

### Core HTML to JSX Conversion Rules

#### 1. class Becomes className
`class` is a reserved keyword in JavaScript, so JSX uses `className`:
```html
<div class="container"> → <div className="container">
```

#### 2. for Becomes htmlFor
Form labels use `htmlFor` instead of `for`:
```html
<label for="email"> → <label htmlFor="email">
```

#### 3. Inline Styles Take JavaScript Objects
Style attributes become JavaScript objects with camelCase properties:
```html
<div style="color: red; margin-top: 10px;"> → 
<div style={{ color: 'red', marginTop: '10px' }}>
```

#### 4. Self-Closing Tags Are Required
All void elements must be self-closed:
```html
<img src="logo.png"> → <img src="logo.png" />
<input type="text"> → <input type="text" />
<br> → <br />
```

#### 5. Event Handlers Use camelCase
All event attributes become camelCase and accept functions:
```html
<button onclick="handleClick()"> → <button onClick={handleClick}>
<input oninput="handleChange()"> → <input onInput={handleChange}>
```

#### 6. Comments Use JSX Syntax
HTML comments become JSX comments:
```html
<!-- comment --> → {/* comment */}
```

#### 7. Boolean Attributes
Boolean attributes work differently in JSX:
```html
<input disabled> → <input disabled={true} /> or just <input disabled />
<input required> → <input required={true} />
```

#### 8. data-* and aria-* Attributes Stay the Same
These attributes remain unchanged:
```html
<div data-id="123"> → <div data-id="123">
<button aria-label="Close"> → <button aria-label="Close">
```

### Structural Rules

#### Single Root Element
Components must return a single parent element:
```jsx
// ❌ Multiple root elements
return (
  <div>Header</div>
  <div>Content</div>
)

// ✅ Wrapped in parent
return (
  <div>
    <div>Header</div>
    <div>Content</div>
  </div>
)

// ✅ Using Fragment
return (
  <>
    <div>Header</div>
    <div>Content</div>
  </>
)
```

### Common Conversions Guide

#### HTML to React Native
When converting HTML to React Native/Expo:
- `div` → `View`
- `span`, `p`, `h1-h6` → `Text`
- `img` → `Image`
- `a` → `Text` with onPress
- CSS → StyleSheet objects
- Inline styles → style prop with objects

#### Form Elements
```html
<form onsubmit="handleSubmit()"> → 
<form onSubmit={handleSubmit}>

<input type="text" placeholder="Name"> → 
<input type="text" placeholder="Name" />

<select onchange="handleChange()"> → 
<select onChange={handleChange}>
```

### Best Practices

#### Component Structure
1. **Identify reusable parts** - Break HTML into logical components
2. **Name components clearly** - Use PascalCase for component names
3. **Separate concerns** - Split logic, styling, and markup
4. **Use props wisely** - Pass data through props, avoid prop drilling

#### Styling Conversion
- Extract inline styles to StyleSheet objects
- Use CSS-in-JS libraries (styled-components, emotion)
- Consider CSS Modules for larger projects
- Maintain consistent naming conventions

#### Accessibility
- Keep `aria-*` attributes intact
- Convert `for` to `htmlFor` on labels
- Ensure semantic HTML structure is maintained
- Add proper ARIA labels where needed

### Conversion Workflow

1. **Analyze HTML structure**
   - Identify component boundaries
   - Note reusable patterns
   - Check for dynamic content

2. **Plan component hierarchy**
   - Create parent/child relationships
   - Define prop interfaces
   - Plan state management

3. **Convert systematically**
   - Start with structural conversion
   - Handle attribute transformations
   - Convert styles to appropriate format
   - Add event handlers

4. **Test and refine**
   - Verify rendering matches original
   - Test interactive elements
   - Check responsive behavior
   - Validate accessibility

### Common Pitfalls

#### Reserved Keywords
Watch out for JavaScript reserved words:
- `class` → `className`
- `for` → `htmlFor`
- `readonly` → `readOnly`
- `tabindex` → `tabIndex`

#### Style Property Names
CSS property names become camelCase:
- `background-color` → `backgroundColor`
- `font-size` → `fontSize`
- `margin-top` → `marginTop`

#### Self-Closing Tags
Don't forget to self-close void elements:
- `<img>`, `<input>`, `<br>`, `<hr>`, `<meta>`, `<link>`

#### Event Handler Naming
Use camelCase for all event handlers:
- `onclick` → `onClick`
- `onchange` → `onChange`
- `onsubmit` → `onSubmit`

### Advanced Patterns

#### Conditional Rendering
```html
<div class="hidden">Content</div> →
{!showHidden && <div>Content</div>}
```

#### Lists and Keys
```html
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul> →
<ul>
  {items.map((item, index) => (
    <li key={index}>{item}</li>
  ))}
</ul>
```

#### Forms and State
```html
<input type="text" value="name"> →
<input 
  type="text" 
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

### Tools and Resources

- **HTML to JSX converters**: Online tools for quick conversion
- **React DevTools**: For inspecting component structure
- **ESLint plugins**: For catching JSX errors
- **Prettier**: For consistent code formatting