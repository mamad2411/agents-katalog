rules:
  # --- 基本的なコーディングルール ---

  - id: no-console-log
    description: "Avoid using console.log; use a logging utility instead"
    severity: warning
    pattern: "console\\.log\\(.*\\)"

  - id: no-any
    description: "Do not use 'any' type; use explicit types"
    severity: error
    pattern: ":\\s*any\\b"

  - id: enforce-async-suffix
    description: "Async functions should end with 'Async'"
    severity: warning
    matchFunctionNames: true
    pattern: "function (?!.*Async)\\w+\\(.*\\)\\s*{[^}]*await"

  - id: use-fetch-wrapper
    description: "Use 'lib/fetcher.ts' instead of direct fetch"
    severity: error
    pattern: "fetch\\("

  - id: no-empty-deps
    description: "Avoid empty dependency arrays in useEffect"
    severity: warning
    pattern: "useEffect\\(.*\\[\\s*\\]\\s*\\)"

  - id: explicit-function-types
    description: "Functions should have explicit parameter and return types"
    severity: warning
    pattern: "function\\s+\\w+\\(.*\\)\\s*{"

  - id: jsx-extension
    description: "React components should use .tsx extension"
    severity: error
    pattern: "\\.jsx$"

  # --- Next.js App Router 専用構成のルール ---

  - id: app-router-only-pages
    description: "Use page.tsx only within /app/ directory (App Router structure)"
    severity: error
    pattern: "(?!.*\\/app\\/).*page\\.tsx"

  # --- 静的サイト（CSRのみ）構成の制約 ---

  - id: disallow-ssr
    description: "Do not use getServerSideProps; this is a CSR-only app"
    severity: error
    pattern: "getServerSideProps"

  - id: disallow-static-props
    description: "Do not use getStaticProps; this project uses client-side rendering only"
    severity: error
    pattern: "getStaticProps"

  - id: disallow-server-components
    description: "Do not use Server Components (.server.tsx); client components only"
    severity: error
    pattern: "\\.server\\.tsx$"

  - id: disallow-api-routes
    description: "Do not define API routes; no server functions allowed in this project"
    severity: error
    pattern: "/app/api/"
