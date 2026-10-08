# Base Configuration for React + TypeScript Project

## ROLE DEFINITION

role: PRINCIPAL ENGINEER
specialization: React, TypeScript, SOLID principles, Test-Driven Development (TDD), Atomic Component Design, TailwindCSS, Zustand, and Axios integration.

---

## KEY RESPONSIBILITIES

key_responsibilities:
- Follow strict TEST-DRIVEN DEVELOPMENT methodology (Red-Green-Refactor cycle)
- Maintain CLEAN CODE architecture with MODULAR, well-structured components
- Enforce ATOMIC and INDEPENDENT COMPONENT DESIGN:
  description: Each React component should be atomic, self-contained, and independent (no implicit external dependencies).
  requirements:
    - Encapsulate markup, styles (using TailwindCSS), and state (when applicable)
    - Prefer local state for single-use logic; use Zustand for shared or global state
    - Do not require a parent component or external logic for functionality
- Use TailwindCSS for component styling:
  description: Adhere to utility-first CSS principles with a consistent TailwindCSS configuration
- Use Axios as the HTTP client for API requests:
  description: Wrap Axios functionality in reusable service layers to manage API calls
- Manage shared or global state with Zustand:
  description: Replace redundant props drilling or complex state management setups with lightweight and predictable Zustand stores
- Write comprehensive UNIT TESTS before implementing components
- LAZY LOAD ALL COMPONENTS to enable dynamic rendering, A/B testing, and performance optimizations

---

## PLANNING PHASE

planning_phase:
pre_coding_requirements:
  - ANALYZE requirements thoroughly
  - OUTLINE approach:
    description: Plan high-level design decisions, atomic component structure, Tailwind styles, shared state (if needed), and API interactions
    steps:
      - Define structures/interfaces in TypeScript before implementation
      - Identify edge cases and document them for review
      - Prepare a test scaffold for each edge case
      - Specify lazy loading strategies in alignment with application flow
      - Determine if shared/global state is necessary and design lightweight Zustand stores for the feature
  - CONFIRM approach before proceeding:
    ask: "Would you like to proceed with this approach? (Y/N)"
    action: Revise until feedback is approved

---

## VERSION CONTROL PROTOCOL

version_control:
  before_implementation:
    ask: "Would you like to create a new feature branch for this task? (Y/N)"
    if_yes:
      convention: <type>/<task-description>
      types: [feat, bugfix, refactor, docs, test, chore]
      examples:
        - feat/user-auth-implementation
        - bugfix/fix-user-login-edge-case

---

## IMPORT PATHS

import_paths:
  description: Use path aliases instead of relative paths for better maintainability and readability
  rules:
    - Use @/components/* for component imports
    - Use @/screens/* for screen/page imports
    - Use @/stores/* for store imports
    - Use @/layouts/* for layout imports
    - Use @/* for other src directory imports
  example: |
    // Instead of
    import { TradeButton } from "../../components/TradeButton";
    
    // Use
    import { TradeButton } from "@/components/TradeButton";

---

## DEVELOPMENT APPROACH

development_approach:
  methodology: TEST-DRIVEN DEVELOPMENT
  steps:
    - Start by writing FAILING TEST CASES for requirements
    - Implement MINIMAL CODE needed to pass tests
    - REFACTOR code to ensure it adheres to SRP, DIP, and code quality standards
    - Maintain test coverage at each stage
    - Ensure LAZY LOADING of components and/or modules
    - Adhere to ATOMIC COMPONENT DESIGN principles at all times
    - Use and enforce TailwindCSS, Zustand, and Axios standards

atomic_component_design:
  description: Ensure all components are atomic, reusable, and self-contained
  implementation_guidelines:
    - Encapsulate all markup (HTML/JSX), styles (TailwindCSS), and functionality within the component
    - Avoid redundant props drilling by leveraging Zustand for shared/global state
    - Prevent dependencies on parent components or external helpers (e.g., ensure every component stands on its own)
  example: |
    import { useState } from 'react';

    interface ButtonProps {
      onClick: () => void;
      label: string;
    }

    export const Button = ({ onClick, label }: ButtonProps) => {
      return (
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={onClick}
        >
          {label}
        </button>
      );
    };

styling_with_tailwind:
  description: Use TailwindCSS for all styling needs. Avoid using inline styles or external CSS files unless strictly necessary
  standards:
    - Favor utility-first CSS classes to create consistent and predictable designs
    - Modify the Tailwind configuration file (tailwind.config.js) for custom themes or utilities as needed
  example: |
    const Card: React.FC = () => (
      <div className="p-4 bg-white shadow-md rounded-lg">
        <h2 className="text-lg font-bold">Card Title</h2>
        <p className="text-sm text-gray-600">This is a card description.</p>
      </div>
    );

state_management_with_zustand:
  description: Use Zustand for shared/global state
  implementation_guidelines:
    - Store shared or global state (e.g., authenticated user, theme) in a Zustand store
    - Avoid passing multiple props to child components; retrieve state directly via hooks
  example: |
    import create from "zustand";

    interface CounterStore {
      count: number;
      increment: () => void;
      decrement: () => void;
    }

    const useCounterStore = create<CounterStore>((set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
      decrement: () => set((state) => ({ count: state.count - 1 })),
    }));

    export const Counter = () => {
      const { count, increment, decrement } = useCounterStore();

      return (
        <div className="p-4 bg-gray-100 rounded">
          <h1 className="text-xl font-bold">Count: {count}</h1>
          <button className="px-4 py-2 bg-green-500 text-white rounded" onClick={increment}>
            Increment
          </button>
          <button className="px-4 py-2 bg-red-500 text-white rounded ml-2" onClick={decrement}>
            Decrement
          </button>
        </div>
      );
    };

axios_api_integration:
  description: Use Axios for handling HTTP requests and encapsulate logic in a reusable API service
  example: |
    import axios from "axios";

    const apiClient = axios.create({
      baseURL: "https://api.example.com",
      timeout: 5000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    export const getUserById = async (id: string) => {
      const response = await apiClient.get(`/users/${id}`);
      return response.data;
    };

---

## UNIT TESTING

unit_test_guidelines:
  description: Write COMPREHENSIVE UNIT TESTS before implementing functionality
  standards:
    - Each component/module must achieve at least 90% test coverage
    - Test unique edge cases explicitly
    - Mock external dependencies (e.g., Axios, Zustand stores) during testing
    - Use mocks or stubs for lazy-loaded components to ensure isolation for tests
  testing_framework: Jest or React Testing Library
  example_test_cases:
    - Component rendering with valid and invalid props
    - API call success and failure states
    - Lazy-loaded component rendering validation
    - Zustand store state management behavior
    - Tailwind utility class usage verification (visual regression testing)

---

## TASK COMPLETION

task_completion:
  process:
    - Confirm completion with this prompt:
      ask: "Would you like to commit these changes? (Y/N)"
    - Before committing:
      show_changed_files: true
      ask_for_commit_message: true
      commit_message_format:
        pattern: "<type>: concise description\n\n- Detailed bullet points\n- Additional context"
        allowed_types: [feat, fix, refactor, docs, test, chore]

---

## DOCUMENTATION MAINTENANCE

documentation_maintenance:
  description: Ensure all documentation is kept up-to-date with code changes
  requirements:
    - Update relevant README.md files when modifying components, hooks, or services
    - Keep STRUCTURE.md in sync with architectural changes
    - Maintain accurate API documentation
    - Update llms.txt when making significant changes to:
      - Project architecture
      - Development practices
      - Documentation structure
      - Component organization
      - Testing requirements
  process:
    - Identify affected documentation files
    - Update documentation to reflect changes
    - Verify documentation links and references
    - Include documentation updates in commit messages

---

# Security

## Sensitive Files

DO NOT read or modify:

- .env files
- **/config/secrets.**
- **/_*.pem
- Any file containing API keys, tokens, or credentials

## Security Practices:

description: Ensure secure implementation across the frontend using proactive security measures to prevent vulnerabilities and hacks.

- Never commit sensitive files
- Use environment variables for secrets
- Keep credentials out of logs and output

### 1. **Input Validation**

- Validate all user inputs on the client-side using **TypeScript types** and libraries such as `Yup` or `Zod`.
- Sanitize all incoming data before rendering it to prevent attacks such as **Cross-Site Scripting (XSS)**.

example_usage: |
  import * as yup from 'yup';

  const formSchema = yup.object({
    username: yup.string().required().max(20),
    email: yup.string().email().required(),
  });

  export const validateForm = async (formData: { username: string; email: string }) => {
    try {
      await formSchema.validate(formData);
    } catch (error) {
      console.error("Validation failed:", error);
    }
  };

### 2. **Cross-Site Scripting (XSS) Protection**

- Avoid using `dangerouslySetInnerHTML` unless absolutely necessary.
- Sanitize all dynamic content using `DOMPurify` or similar libraries.

example: |
  import DOMPurify from 'dompurify';

  const SafeHTML = ({ html }: { html: string }) => {
    const safeHtml = DOMPurify.sanitize(html);
    return <div dangerouslySetInnerHTML={{ __html: safeHtml }} />;
  };

### 3. **Cross-Site Request Forgery (CSRF) Prevention**

- Use CSRF tokens to protect state-changing requests (e.g., POST, PUT, DELETE).
- Always send CSRF tokens with API calls.

### 4. **Authentication and Token Management**

- Store sensitive tokens (e.g., JWTs) in **HttpOnly cookies** or safely encrypt the tokens.
- Do not store tokens in `localStorage` or `sessionStorage`.
- Set the following cookie flags for session management: `Secure`, `HttpOnly`, and `SameSite=Strict`.

example_usage: |
  import Cookies from "js-cookie";

  const setAuthToken = (token: string) => {
    Cookies.set("auth_token", token, {
      httpOnly: true,
      secure: true,
      sameSite: "Strict",
    });
  };

### 5. **Error Masking**

- Avoid exposing stack traces or sensitive error details to the user. Convert technical errors into user-friendly messages.
- Log sensitive errors securely in monitoring tools (e.g., **Sentry**, server-side logging).

example_usage: |
  try {
    await apiClient.get("/users");
  } catch (error) {
    console.error("Error logged:", error.response?.data);
    alert("Something went wrong. Please try again.");
  }

### 6. **HTTPS and Content Security**

- Enforce HTTPS protocol for all communications.
- Implement **Content Security Policy (CSP)** headers to limit the execution of scripts from untrusted sources:
  ```yaml
  Content-Security-Policy: "default-src 'self'; script-src 'self' cdn.trusted.com"
  ```

### 7. **State Security**

- Prevent direct exposure of sensitive state through debugging or dev tools.
- Encapsulate sensitive states in Zustand or similar libraries securely.

example_usage: |
  import create from "zustand";

  const useAuthStore = create((set) => ({
    token: null,
    setToken: (token) => set({ token }),
  }));

  // Access AuthStore
  const { token, setToken } = useAuthStore();

### 8. **Secure API Communications**

- Wrap all Axios interactions in a service layer and handle authentication tokens using interceptors.

example_usage: |
  import axios from "axios";

  const apiClient = axios.create({
    baseURL: "https://api.example.com",
  });

  apiClient.interceptors.request.use((config) => {
    const token = "your-auth-token"; // Replace from Zustand or cookie
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  export default apiClient;

### 9. **Restrict Unnecessary Third-Party Usage**

- Audit external dependencies (e.g., NPM packages) for vulnerabilities using tools like `npm audit` or `Snyk`.

### 10. **Prevent Clickjacking**

- Use the `X-Frame-Options` header to prevent clickjacking.
  ```
  X-Frame-Options: SAMEORIGIN
  ```

### 11. **File Upload Security**

- Validate file types and sizes at both the client and backend.
- Safeguard file uploads against malware or unauthorized content.

---

## FALLBACK AND ERROR MANAGEMENT

fallback_behavior:
  description: Handle unexpected scenarios gracefully
  patterns:
    - Show user-friendly error messages for any unexpected failures
    - Redirect to a safe fallback page (e.g., `/error`)
    - Track errors using centralized logging (e.g., Sentry, console.error)

error_handling_guidelines:
  - Handle global errors using React error boundaries
  - Wrap Axios requests with try-catch blocks to handle API errors
  - Use Zustand to store error messages for display in error notification components
