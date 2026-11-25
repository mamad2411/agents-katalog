# === Cursor Rules for LMS Frontend ===
# Project Type: Next.js (App Router) with src/ directory
# Goal: Lightweight LMS-type web app using mock data, later integrated with Strapi
# Features: Courses, Modules per Course, Exam taking, Progress Tracking (no auth)

instructions:
  - Always use TypeScript and functional components with Next.js App Router.
  - Follow folder structure under `/src/app` (App Router style).
  - Use Tailwind CSS for UI layout and styling.
  - Mock data should be stored in `/src/lib/mockData.ts` for now.
  - Use clean, reusable components for CourseCard, ModuleList, ExamSection, and ProgressBar.
  - Do not include authentication logic.
  - API integration with Strapi will be added later.

folder_structure:
  src/
    app/
      layout.tsx
      page.tsx                     # Home page showing list of courses
      courses/
        [slug]/
          page.tsx                 # Course page showing modules and progress
          exam/
            page.tsx               # Exam page for selected course
    components/
      CourseCard.tsx               # Displays each course in the homepage
      ModuleList.tsx               # Lists modules for a given course
      ProgressBar.tsx              # Visual progress tracker
      ExamSection.tsx              # Displays exam questions (mocked for now)
    lib/
      mockData.ts                  # Mock data for courses, modules, and exams
      progressUtils.ts             # Helper to calculate progress percentage
    styles/
      globals.css

mock_data_example:
  courses:
    - id: 1
      title: "Database Administration"
      slug: "database-administration"
      description: "Learn about relational databases, normalization, and SQL."
      modules:
        - title: "Introduction to Databases"
          completed: true
        - title: "SQL Basics"
          completed: false
        - title: "Normalization"
          completed: false
    - id: 2
      title: "Systems Integration and Architecture"
      slug: "systems-integration"
      description: "Study system interoperability, APIs, and architecture models."
      modules:
        - title: "System Components"
          completed: true
        - title: "APIs and Communication"
          completed: true
        - title: "Integration Patterns"
          completed: false

example_component_usage:
  # Home Page
  - Import and display all courses from mockData in a responsive grid using <CourseCard />.
  # Course Page
  - Fetch selected course by slug from mockData.
  - Display <ProgressBar /> and <ModuleList />.
  - Include "Take Exam" button that links to `/courses/[slug]/exam`.
  # Exam Page
  - Display mock questions from mockData.exams for the current course.
  - After completion, update progress via a local state (no backend yet).

style_guide:
  - Tailwind CSS for layout and spacing
  - Responsive grid for course cards
  - Rounded, soft shadows for cards and containers
  - Use `text-gray-800` for text, `bg-gray-100` for panels, and `bg-blue-600` for buttons/progress

notes:
  - The entire app must work offline using mockData before Strapi integration.
  - No authentication, user profiles, or backend API calls for now.
  - Progress tracking can use React state or localStorage.

