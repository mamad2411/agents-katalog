---
name: React Developer
description: A description of your rule
---

## Development Guidelines
- Wrap everything in a single named export default function (e.g., export default function MyPage() { ... }).
- Include mock or placeholder data if the backend is not specified.
- If fetching data, simulate using useEffect with setTimeout or fetch() with sample endpoints.
- Always handle loading and error states if data is involved and provide a human-readable console.log with a description of errors.
- Avoid global state unless specified — stick with useState or useReducer.
- Prefer composition over repetition — break large components into reusable ones if logic is repeated.
- For interactive UI, use react-bootstrap and for styling use Tailwind CSS
- Use clean, readable layouts: flexbox or grid where needed.
- Use accessible HTML semantics (<section>, <header>, <nav>, <main>, <footer>, etc.).
- Make it responsive by default (e.g., max-w, px-4, sm: prefixes).
- The result should be self-contained and easy to copy-paste into a file like MyPage.jsx.
- No unnecessary imports, only include what’s used.
- Add a brief comment block at the top describing what the page does (optional).
- Use arrow functions for helpers inside the component (const handleClick = () => {}).
- Use descriptive variable and function names (no foo, bar, etc.).
- Use JSX fragments (<>...</>) where needed instead of wrapping everything in a div.
