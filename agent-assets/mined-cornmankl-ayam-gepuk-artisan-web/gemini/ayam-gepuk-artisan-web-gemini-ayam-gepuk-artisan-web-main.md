# GEMINI.md - AYAM-GEPUK-ARTISAN-WEB

## Project Overview

This project is a web application for "Ayam Gepuk Artisan". It is built using React, Vite, and TypeScript. The styling is done using Tailwind CSS. The application features a menu, promotions, online ordering, and other pages related to the business.

**Key Technologies:**

*   **Framework:** React
*   **Build Tool:** Vite
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS
*   **Routing:** React Router DOM
*   **State Management:** React Context API (for Cart, Theme, Auth, Loyalty)

**Architecture:**

The project follows a standard React project structure.

*   `src/pages`: Contains the main pages of the application.
*   `src/components`: Contains reusable UI components.
*   `src/router.tsx`: Defines the application's routes.
*   `src/context`: Contains React context providers for state management.
*   `src/data`: Contains static data for the application.
*   `public`: Contains static assets like images and logos.

## Building and Running

1.  **Install Dependencies:**
    ```bash
    npm install
    ```

2.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5175`.

3.  **Build for Production:**
    ```bash
    npm run build
    ```
    The production-ready files will be generated in the `dist` directory.

4.  **Preview Production Build:**
    ```bash
    npm run preview
    ```

## Development Conventions

*   **Linting:** The project uses ESLint for code quality. To run the linter, use:
    ```bash
    npm run lint
    ```
*   **Type Checking:** The project uses TypeScript for static type checking. To check for type errors, use:
    ```bash
    npm run type-check
    ```
*   **Testing:** The project uses Vitest for testing. To run the tests, use:
    ```bash
    npm run test
    ```
*   **Styling:** The project uses Tailwind CSS for styling. Utility classes should be used whenever possible. Custom styles can be added to `src/index.css`.
*   **Components:** Reusable components should be created in the `src/components` directory.
*   **State Management:** For global state, React Context API is used. New contexts can be added in the `src/context` directory.
