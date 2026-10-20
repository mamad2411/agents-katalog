## Gemini Added Memories
- ./backend contains the FastAPI backend. It uses uv as package manager.
- ./frontend contains the TS React frontend. It uses ShadCN components.

## Useful commands:

Run `make` with these targets:
  install                     Install all dependencies for frontend and backend
  dev                         Start the development servers for frontend and backend
  test                        Run tests for frontend and backend
  lint                        Lint the frontend and backend code
  docker-build                Build the production Docker images
  docker-up                   Start the production application with Docker Compose
  docker-down                 Stop the production application
  docker-dev-up               Start the development environment with Docker Compose
  docker-dev-down             Stop the development environment
  clean                       Remove generated files and caches

## Writing Tests

### General Guidance

- When adding tests, first examine existing tests to understand and conform to established conventions.
- Pay close attention to the mocks at the top of existing test files; they reveal critical dependencies and how they are managed in a test environment.

## Git Repo

The main branch for this project is called "master"

## Backend

Of course. Here is a similar markdown for an AI agent on how to write Python code for a backend with FastAPI, SQLAlchemy, and Alembic:

## Backend

When contributing to this Python, FastAPI, and SQLAlchemy codebase, please adhere to the following principles to ensure the code is robust, maintainable, and performs well. The focus is on leveraging modern Python features, functional programming concepts, and the specific strengths of our chosen frameworks.

### Prefer Functional Approaches and Data Classes over Traditional Classes

While Python is a multi-paradigm language that fully supports object-oriented programming, for our backend services, we favor a more functional approach, especially for business logic and data handling.

-   **Simplicity and Predictability**: Functions that operate on data are often simpler to reason about than classes with internal state and methods. This leads to more predictable code with fewer side effects. Pure functions, which always produce the same output for the same input and have no side effects, are the ideal.

-   **Seamless FastAPI Integration**: FastAPI is designed around functions. Dependencies are injected into functions, and route handlers are functions. Writing your logic in functions aligns perfectly with this design, leading to cleaner and more idiomatic FastAPI code.

-   **Data-Oriented Design with Pydantic**: Instead of creating complex classes to hold data, use Pydantic models. Pydantic provides data validation, serialization, and deserialization out of the box, all based on standard Python type hints. This is more declarative and less error-prone than manual implementation.

-   **Reduced Boilerplate**: Traditional classes can introduce boilerplate like `__init__` methods, `self`, and method binding. For many tasks, simple functions operating on Pydantic models or dictionaries are more concise and just as effective.

### Leveraging Python Modules for Encapsulation

Python's module system is the primary way to organize and encapsulate code. We prefer using modules to control visibility over class-based access modifiers like `_` or `__`.

-   **Clear Public API**: Anything you import from a module is part of its public API. Anything you don't is considered private. This is a simple and effective way to define module boundaries.

-   **Enhanced Testability**: Test the public functions and interfaces of your modules. If you find yourself needing to test an "internal" function, consider if it should be part of the public API or if the module should be broken down further.

-   **Reduced Coupling**: Well-defined modules with clear public APIs reduce coupling between different parts of the application, making it easier to refactor and maintain.

### Static Typing with Pydantic and Type Hints

Python's optional static typing is a powerful tool for writing robust and maintainable code. We use it extensively.

-   **Avoid `Any`**: The `Any` type subverts the type checker. Avoid it whenever possible. If you have a truly unknown type, be explicit about how you handle it.

-   **Leverage Pydantic for Validation**: Use Pydantic models for all data coming into and out of your API. This includes request bodies, query parameters, and response models. This ensures that your data is always in the expected shape.

-   **Use Type Hints Everywhere**: All function signatures should have type hints. This improves readability and allows static analysis tools to catch errors before they happen in production.

### Embracing Python's Built-in Data Structures and Comprehensions

Python has a rich set of built-in data structures and powerful syntax for working with them.

-   **List Comprehensions and Generator Expressions**: Prefer list comprehensions and generator expressions over `for` loops for creating lists and other collections. They are more concise and often more performant.

-   **Use the Right Data Structure**: Understand the use cases for lists, tuples, sets, and dictionaries, and use the appropriate one for the task at hand.

### FastAPI, SQLAlchemy, and Alembic Guidelines

-   **Dependency Injection**: Use FastAPI's dependency injection system to manage resources like database sessions. This makes your code more testable and easier to reason about.

-   **Database Sessions**: A database session should be created for each request and closed when the request is finished. The dependency injection system is the perfect place to manage this.

-   **Asynchronous Code**: Use `async` and `await` for all I/O-bound operations, especially database queries. This is crucial for the performance of a FastAPI application.

-   **SQLAlchemy ORM**: Use the SQLAlchemy ORM for all database interactions. Avoid raw SQL queries whenever possible to prevent SQL injection vulnerabilities. Define your models clearly, and use relationships to express the connections between your data.

-   **Alembic Migrations**: All database schema changes must be accompanied by an Alembic migration script. Write clear and reversible migrations.

### Process

1.  **Analyze the User's Request**: Understand the desired functionality or change.
2.  **Consult Best Practices**: Before writing code, think about the best way to implement the feature using the principles outlined above.
3.  **Write Clear and Concise Code**: The code should be easy to read and understand.
4.  **Provide Explanations**: When suggesting code, explain the reasoning behind the implementation and how it aligns with our best practices.

### Optimization Guidelines

-   **Efficient Database Queries**: Write efficient SQLAlchemy queries. Avoid the N+1 problem by using `joinedload` or `selectinload`.
-   **Isolate Side Effects**: Keep side effects (like sending emails or interacting with external services) separate from your core business logic.
-   **Structure for Concurrency**: Write your `async` code to take advantage of concurrency, running I/O-bound operations in parallel when possible.

## Frontend

When contributing to this React, Node, and TypeScript codebase, please prioritize the use of plain JavaScript objects with accompanying TypeScript interface or type declarations over JavaScript class syntax. This approach offers significant advantages, especially concerning interoperability with React and overall code maintainability.

### Preferring Plain Objects over Classes

JavaScript classes, by their nature, are designed to encapsulate internal state and behavior. While this can be useful in some object-oriented paradigms, it often introduces unnecessary complexity and friction when working with React's component-based architecture. Here's why plain objects are preferred:

- Seamless React Integration: React components thrive on explicit props and state management. Classes' tendency to store internal state directly within instances can make prop and state propagation harder to reason about and maintain. Plain objects, on the other hand, are inherently immutable (when used thoughtfully) and can be easily passed as props, simplifying data flow and reducing unexpected side effects.

- Reduced Boilerplate and Increased Conciseness: Classes often promote the use of constructors, this binding, getters, setters, and other boilerplate that can unnecessarily bloat code. TypeScript interface and type declarations provide powerful static type checking without the runtime overhead or verbosity of class definitions. This allows for more succinct and readable code, aligning with JavaScript's strengths in functional programming.

- Enhanced Readability and Predictability: Plain objects, especially when their structure is clearly defined by TypeScript interfaces, are often easier to read and understand. Their properties are directly accessible, and there's no hidden internal state or complex inheritance chains to navigate. This predictability leads to fewer bugs and a more maintainable codebase.

- Simplified Immutability: While not strictly enforced, plain objects encourage an immutable approach to data. When you need to modify an object, you typically create a new one with the desired changes, rather than mutating the original. This pattern aligns perfectly with React's reconciliation process and helps prevent subtle bugs related to shared mutable state.

- Better Serialization and Deserialization: Plain JavaScript objects are naturally easy to serialize to JSON and deserialize back, which is a common requirement in web development (e.g., for API communication or local storage). Classes, with their methods and prototypes, can complicate this process.

### Embracing ES Module Syntax for Encapsulation

Rather than relying on Java-esque private or public class members, which can be verbose and sometimes limit flexibility, we strongly prefer leveraging ES module syntax (`import`/`export`) for encapsulating private and public APIs.

- Clearer Public API Definition: With ES modules, anything that is exported is part of the public API of that module, while anything not exported is inherently private to that module. This provides a very clear and explicit way to define what parts of your code are meant to be consumed by other modules.

- Enhanced Testability (Without Exposing Internals): By default, unexported functions or variables are not accessible from outside the module. This encourages you to test the public API of your modules, rather than their internal implementation details. If you find yourself needing to spy on or stub an unexported function for testing purposes, it's often a "code smell" indicating that the function might be a good candidate for extraction into its own separate, testable module with a well-defined public API. This promotes a more robust and maintainable testing strategy.

- Reduced Coupling: Explicitly defined module boundaries through import/export help reduce coupling between different parts of your codebase. This makes it easier to refactor, debug, and understand individual components in isolation.

### Avoiding `any` Types and Type Assertions; Preferring `unknown`

TypeScript's power lies in its ability to provide static type checking, catching potential errors before your code runs. To fully leverage this, it's crucial to avoid the `any` type and be judicious with type assertions.

- **The Dangers of `any`**: Using any effectively opts out of TypeScript's type checking for that particular variable or expression. While it might seem convenient in the short term, it introduces significant risks:
  - **Loss of Type Safety**: You lose all the benefits of type checking, making it easy to introduce runtime errors that TypeScript would otherwise have caught.
  - **Reduced Readability and Maintainability**: Code with `any` types is harder to understand and maintain, as the expected type of data is no longer explicitly defined.
  - **Masking Underlying Issues**: Often, the need for any indicates a deeper problem in the design of your code or the way you're interacting with external libraries. It's a sign that you might need to refine your types or refactor your code.

- **Preferring `unknown` over `any`**: When you absolutely cannot determine the type of a value at compile time, and you're tempted to reach for any, consider using unknown instead. unknown is a type-safe counterpart to any. While a variable of type unknown can hold any value, you must perform type narrowing (e.g., using typeof or instanceof checks, or a type assertion) before you can perform any operations on it. This forces you to handle the unknown type explicitly, preventing accidental runtime errors.

  ```
  function processValue(value: unknown) {
     if (typeof value === 'string') {
        // value is now safely a string
        console.log(value.toUpperCase());
     } else if (typeof value === 'number') {
        // value is now safely a number
        console.log(value * 2);
     }
     // Without narrowing, you cannot access properties or methods on 'value'
     // console.log(value.someProperty); // Error: Object is of type 'unknown'.
  }
  ```

- **Type Assertions (`as Type`) - Use with Caution**: Type assertions tell the TypeScript compiler, "Trust me, I know what I'm doing; this is definitely of this type." While there are legitimate use cases (e.g., when dealing with external libraries that don't have perfect type definitions, or when you have more information than the compiler), they should be used sparingly and with extreme caution.
  - **Bypassing Type Checking**: Like `any`, type assertions bypass TypeScript's safety checks. If your assertion is incorrect, you introduce a runtime error that TypeScript would not have warned you about.
  - **Code Smell in Testing**: A common scenario where `any` or type assertions might be tempting is when trying to test "private" implementation details (e.g., spying on or stubbing an unexported function within a module). This is a strong indication of a "code smell" in your testing strategy and potentially your code structure. Instead of trying to force access to private internals, consider whether those internal details should be refactored into a separate module with a well-defined public API. This makes them inherently testable without compromising encapsulation.

### Embracing JavaScript's Array Operators

To further enhance code cleanliness and promote safe functional programming practices, leverage JavaScript's rich set of array operators as much as possible. Methods like `.map()`, `.filter()`, `.reduce()`, `.slice()`, `.sort()`, and others are incredibly powerful for transforming and manipulating data collections in an immutable and declarative way.

Using these operators:

- Promotes Immutability: Most array operators return new arrays, leaving the original array untouched. This functional approach helps prevent unintended side effects and makes your code more predictable.
- Improves Readability: Chaining array operators often lead to more concise and expressive code than traditional for loops or imperative logic. The intent of the operation is clear at a glance.
- Facilitates Functional Programming: These operators are cornerstones of functional programming, encouraging the creation of pure functions that take inputs and produce outputs without causing side effects. This paradigm is highly beneficial for writing robust and testable code that pairs well with React.

By consistently applying these principles, we can maintain a codebase that is not only efficient and performant but also a joy to work with, both now and in the future.

## React Guidelines

### Follow these guidelines in all code you produce and suggest

Use functional components with Hooks: Do not generate class components or use old lifecycle methods. Manage state with useState or useReducer, and side effects with useEffect (or related Hooks). Always prefer functions and Hooks for any new component logic.

Keep components pure and side-effect-free during rendering: Do not produce code that performs side effects (like subscriptions, network requests, or modifying external variables) directly inside the component's function body. Such actions should be wrapped in useEffect or performed in event handlers. Ensure your render logic is a pure function of props and state.

Respect one-way data flow: Pass data down through props and avoid any global mutations. If two components need to share data, lift that state up to a common parent or use React Context, rather than trying to sync local state or use external variables.

Never mutate state directly: Always generate code that updates state immutably. For example, use spread syntax or other methods to create new objects/arrays when updating state. Do not use assignments like state.someValue = ... or array mutations like array.push() on state variables. Use the state setter (setState from useState, etc.) to update state.

Accurately use useEffect and other effect Hooks: whenever you think you could useEffect, think and reason harder to avoid it. useEffect is primarily only used for synchronization, for example synchronizing React with some external state. IMPORTANT - Don't setState (the 2nd value returned by useState) within a useEffect as that will degrade performance. When writing effects, include all necessary dependencies in the dependency array. Do not suppress ESLint rules or omit dependencies that the effect's code uses. Structure the effect callbacks to handle changing values properly (e.g., update subscriptions on prop changes, clean up on unmount or dependency change). If a piece of logic should only run in response to a user action (like a form submission or button click), put that logic in an event handler, not in a useEffect. Where possible, useEffects should return a cleanup function.

Follow the Rules of Hooks: Ensure that any Hooks (useState, useEffect, useContext, custom Hooks, etc.) are called unconditionally at the top level of React function components or other Hooks. Do not generate code that calls Hooks inside loops, conditional statements, or nested helper functions. Do not call Hooks in non-component functions or outside the React component rendering context.

Use refs only when necessary: Avoid using useRef unless the task genuinely requires it (such as focusing a control, managing an animation, or integrating with a non-React library). Do not use refs to store application state that should be reactive. If you do use refs, never write to or read from ref.current during the rendering of a component (except for initial setup like lazy initialization). Any ref usage should not affect the rendered output directly.

Prefer composition and small components: Break down UI into small, reusable components rather than writing large monolithic components. The code you generate should promote clarity and reusability by composing components together. Similarly, abstract repetitive logic into custom Hooks when appropriate to avoid duplicating code.

Optimize for concurrency: Assume React may render your components multiple times for scheduling purposes (especially in development with Strict Mode). Write code that remains correct even if the component function runs more than once. For instance, avoid side effects in the component body and use functional state updates (e.g., setCount(c => c + 1)) when updating state based on previous state to prevent race conditions. Always include cleanup functions in effects that subscribe to external resources. Don't write useEffects for "do this when this changes" side effects. This ensures your generated code will work with React's concurrent rendering features without issues.

Optimize to reduce network waterfalls - Use parallel data fetching wherever possible (e.g., start multiple requests at once rather than one after another). Leverage Suspense for data loading and keep requests co-located with the component that needs the data. In a server-centric approach, fetch related data together in a single request on the server side (using Server Components, for example) to reduce round trips. Also, consider using caching layers or global fetch management to avoid repeating identical requests.

Rely on React Compiler - useMemo, useCallback, and React.memo can be omitted if React Compiler is enabled. Avoid premature optimization with manual memoization. Instead, focus on writing clear, simple components with direct data flow and side-effect-free render functions. Let the React Compiler handle tree-shaking, inlining, and other performance enhancements to keep your code base simpler and more maintainable.

Design for a good user experience - Provide clear, minimal, and non-blocking UI states. When data is loading, show lightweight placeholders (e.g., skeleton screens) rather than intrusive spinners everywhere. Handle errors gracefully with a dedicated error boundary or a friendly inline message. Where possible, render partial data as it becomes available rather than making the user wait for everything. Suspense allows you to declare the loading states in your component tree in a natural way, preventing “flash” states and improving perceived performance.

### Process

1. Analyze the user's code for optimization opportunities:
   - Check for React anti-patterns that prevent compiler optimization
   - Look for component structure issues that limit compiler effectiveness
   - Think about each suggestion you are making and consult React docs for best practices

2. Provide actionable guidance:
   - Explain specific code changes with clear reasoning
   - Show before/after examples when suggesting changes
   - Only suggest changes that meaningfully improve optimization potential

### Optimization Guidelines

- State updates should be structured to enable granular updates
- Side effects should be isolated and dependencies clearly defined

## Comments policy

Only write high-value comments if at all. Avoid talking to the user through comments.
