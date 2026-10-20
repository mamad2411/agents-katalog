# Source Root

Application source files including entry points, configuration, and global styles.

## Files

| File            | What                                                   | When to read                       |
| --------------- | ------------------------------------------------------ | ---------------------------------- |
| `main.ts`       | Application bootstrap entry point                      | App initialization changes         |
| `app.config.ts` | Angular application configuration (providers, imports) | Adding providers, global config    |
| `index.html`    | HTML entry point with meta tags and root element       | Meta tags, title, external scripts |
| `styles.css`    | Global styles, design tokens, Tailwind setup           | Design system changes, theming     |
| `fonts.css`     | Font face definitions for custom fonts                 | Font changes                       |
| `polyfills.ts`  | Browser polyfills configuration                        | Polyfill additions                 |
| `test.ts`       | Karma test setup                                       | Test configuration                 |

## Directories

| Directory       | What                            | When to read            |
| --------------- | ------------------------------- | ----------------------- |
| `app/`          | Main application code           | Any feature work        |
| `assets/`       | Static assets (fonts, images)   | Asset management        |
| `environments/` | Environment configuration files | API URLs, feature flags |
| `styles/`       | Additional style files          | Extra styling           |
