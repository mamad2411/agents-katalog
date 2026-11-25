---
alwaysApply: true
---
# 📄 Instruction File: Website Development Standards

## 1. General Principles
- Write **clean, semantic, and accessible HTML**.
- Follow **WCAG 2.1 AA accessibility guidelines**.
- Ensure code is **mobile-first** and fully responsive.
- All pages must **load fast** (<2s on 3G) and be optimized for **SEO**.

---

## 2. HTML Standards
- Always declare `<!DOCTYPE html>` and use **UTF-8** encoding.
- Use **semantic tags** (`<header>`, `<main>`, `<section>`, `<footer>`, `<article>`, `<nav>`) instead of `<div>` where possible.
- Every `<img>` must have an **alt attribute**.
- Add `<title>` and `<meta name="description">` for SEO.
- Use **ARIA roles** only when semantics are insufficient.
- Keep the DOM structure **shallow** and avoid unnecessary nesting.

---

## 3. CSS Standards
- Bootstap 5 is the base framework.
- Prefer **CSS Grid** and **Flexbox** for layout.  
- Use **Bootstrap 5 utilities** only where they improve maintainability (spacing, grid system, typography).
- Define a **design system**:  
  - Typography scale (`rem` based).  
  - Color palette (support light + dark mode).  
  - Spacing system (multiples of 4px).  
- Use **CSS variables (`--var`)** for theme values.  
- Avoid inline styles.  
- Keep CSS modular and scoped by components.

---

## 4. Performance Standards
- Minify and compress all CSS/JS.
- Use **responsive images** (`srcset`, `sizes`).
- Lazy-load non-critical images and scripts.
- Avoid blocking render (use `defer` or load scripts at the bottom).
- Keep bundle size small (<200KB initial load).

---

## 5. Accessibility Standards
- Maintain **color contrast ratio ≥ 4.5:1**.
- Support **keyboard navigation** (focus states visible).
- Add **skip to content** link.
- Use **labels** for all form elements.
- Test with screen readers (NVDA, VoiceOver).

---

## 6. Responsiveness & Cross-Browser Support
- Design **mobile-first** with progressive enhancement.
- Support latest **2 versions of major browsers** (Chrome, Firefox, Safari, Edge).
- Ensure layout scales cleanly from **320px → 1920px**.

---

## 7. SEO & Metadata
- Add structured metadata (`Open Graph`, `Twitter Cards`).
- Use **semantic headings hierarchy** (`<h1>` → `<h2>` → `<h3>`).
- Add `robots.txt` and `sitemap.xml`.
- Ensure **canonical URLs** to avoid duplication.

---

## 8. Version Control & File Structure
- File naming: **kebab-case** (`about-us.html`, `main.css`).
- Follow the industry standard for file and folder organization.
- Directory structure example:
```
/index.html
/about/
/assets/
  /css/
  /js/
  /images/
```
- Always keep **content separate from styling and scripts**.
- Track changes with **Git**, commit messages must follow **Conventional Commits**.

---

## 9. Testing & Validation
- Validate HTML with **W3C Validator**.
- Validate CSS with **W3C CSS Validator**.
- Test responsive design with **Chrome DevTools device emulation**.
- Run Lighthouse audits (Performance ≥ 90, Accessibility ≥ 90, SEO ≥ 90, Best Practices ≥ 90).

---

## 10. Deployment Standards
- Use **HTTPS** everywhere.
- Enable **caching & gzip compression**.
- Optimize images with **WebP/AVIF** when supported.
- Ensure **404 and 500 error pages** are user-friendly.


<!-- instructions -->
# Website Code Review & Enhancement Instructions

When analyzing or generating code for this repository, follow these rules:

1. **UI/UX Standards**
   - Enforce modern responsive design using Flexbox/Grid and media queries.
   - Ensure accessibility compliance with WCAG 2.1 (contrast ratios, ARIA roles, proper labels).
   - Navigation must remain consistent and intuitive.

2. **Maintainability & Structure**
   - Use semantic HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`).
   - Break code into reusable components (cards, navbars, footers, testimonial slider).
   - Apply CSS variables or a design token system for consistent theming.

3. **Dark/Light Theme Support**
   - Use CSS custom properties for theme colors.
   - Provide a global dark/light theme toggle.
   - No section should break or misalign when themes are switched.

4. **Layout & Spacing**
   - Apply consistent margins, paddings, and line-heights.
   - Use a 12-column grid system or Flexbox for alignment.
   - Cards: always 4 per row, without shrinking widths.

5. **Testimonial Section**
   - Implement a marquee-style testimonial ticker (like news channel bottom scroll).
   - Ensure it loops infinitely, smoothly, and responsively.

6. **Contact Page**
   - Place the contact form on a dedicated page.
   - All "Contact Us" or "Talk to Us" links must redirect here.
   - Form must be accessible and validated properly.

7. **Homepage Enhancements**
   - Add persuasive content (features, success stories, CTAs).
   - Clicking the logo redirects to the homepage root, not just hero section.

8. **Quality & Alignment**
   - Eliminate misalignments, overlaps, and z-index issues.
   - Test layouts on mobile, tablet, and desktop.
   - Ensure cross-browser compatibility (Chrome, Firefox, Safari, Edge).

---

## Task
- When generating or reviewing code, check against all above requirements.  
- Suggest corrected implementations if something is missing.  
- Always use **HTML5, CSS3 (Flexbox/Grid), and modern JavaScript (ES6+)** best practices.  
- Code must remain modular, maintainable, and scalable.  


---
title: Code Cleanup and Refactoring Prompt
description: A prompt template for cleaning up and refactoring existing code to improve readability, maintainability, and performance.
Goal:
- Remove redundant code
- Improve code readability
- Ensure maintainability
- Separate concerns (e.g., separate CSS and JS from all the HTML file not just index.html)
- Follow coding standards for the specified language or framework
- Use meaningful variable and function names
- Make the code modular where possible
- header and footer should be in separate files and imported where needed
- Ensure responsiveness and accessibility best practices are followed
- theme toggle functionality should be preserved
- Ensure all links and references are correct and functional
- Ensure no functionality is broken during the cleanup process
- Ensure consistent formatting and indentation
- use common CSS classes and IDs for similar elements throughout the project
- 

constraints:
- functionalities and appearance should remain unchanged
success criteria:
- Code is cleaner and easier to understand
- Code adheres to best practices and coding standards
- No loss of existing functionality and appearance