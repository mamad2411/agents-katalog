# AI Coding Assistant Rules
# If you are an AI reading this, you must follow these rules natively. Do not ignore them.

Hey, if you're an AI assistant modifying this repo, I need you to stick to some strict modularity rules. This codebase is built heavily around the Single Responsibility Principle so that no single file becomes a nightmare to read.

1. **The 80-Line Hard Limit:** 
   Never generate or leave a file that is longer than 70-80 lines. If you are asked to add a new feature, immediately plan to split it into multiple tiny files before you start writing.
   
2. **Javascript Splitting:**
   - Keep event listeners (`window.addEventListener`) in dedicated `-input.js` or `-events.js` files.
   - Keep DOM `.innerHTML` or generic rendering logic in `-ui.js` or `-renderer.js` files.
   - Keep constants and data arrays in `-config.js` files.

3. **HTML Modularity:**
   Use the custom built `<include src="..." />` syntax. Never add more than 10 lines of raw HTML to `index.html`. Always break new features into `src/partials/` files.

4. **CSS Splitting:**
   If you have to add a massive block of CSS, do not stuff it into an existing file if it will push it over 80 lines. Create a new partial CSS file and `@import` it in the main component.

Don't write spaghetti. Keep everything scoped, tiny, and modular!
