# Vesta

Vesta is an AI-powered content transformation application that helps you convert content from one format to another using your own examples. It leverages few-shot learning to adapt to your unique style, enabling seamless conversions between formats like Jupyter Notebooks, blogs, tweet threads, and LinkedIn posts.

## Features

- Custom Content Conversions: Define your own input and output content types and provide examples to guide the AI
- Few-Shot Learning: The AI uses your examples to learn and replicate your style in content transformations
- Flexible Architecture: Easily add new content types and conversion pairs
- Shared Schemas: TypeScript interfaces are shared between the frontend and backend for consistent data models

## Objects

- **User**: A user of the application.
- **Project**: A project is a collection of content around a single topic. For example, a video transcript, a blog post, or a tweet thread all about a single topic would all be part of the same project.
- **Content**: A content is a piece of content for a specific project.


## Brand Identity and Style

Vesta's brand identity combines modern professionalism with dynamic energy. The color palette creates depth through gradients 
and thoughtful layering:

### Colors
- Primary Gradient: from-blue-600 (#2563eb) to-purple-600 (#9333ea)
- Secondary Blue: #2563eb
- Secondary Purple: #9333ea
- Background Gradient: from-gray-50 (#f9fafb) to-white
- Text Colors:
  - Primary: text-gray-900 (#111827)
  - Secondary: text-gray-600 (#4b5563)
  - Tertiary: text-gray-500 (#6b7280)

### Design Elements
- Generous use of gradients for visual hierarchy
- Subtle backdrop blur effects (backdrop-blur-sm) for depth
- Card-based layouts with soft shadows (shadow-lg)
- Smooth hover transitions (duration-300)
- Interactive elements use gradient backgrounds
- Floating orbs and beam animations for dynamic feel
- Subtle patterns and overlays for texture

### Typography
- Font: Inter for clean, professional readability
- Headings: Large, bold (text-4xl font-bold)
- Body: Comfortable reading size (text-lg/text-xl)
- Subtle text gradients for emphasis

### Components
- Cards: White backgrounds with subtle shadows
- Buttons: Gradient backgrounds with hover states
- Badges: Used for highlighting features/status
- Icons: Used consistently for visual reinforcement

### Animation
- Subtle fade-ins for content sections
- Smooth hover transitions
- Floating animations for background elements
- Underline animations for emphasis

The overall aesthetic maintains professionalism while incorporating modern design elements that suggest innovation and 
transformation. All interactions should feel smooth and intentional, reinforcing Vesta's role as a sophisticated yet 
approachable content transformation tool.


## User Flow:

1. User logs in and creates a new project
2. They set the title and description of the project
3. They add each piece of content they have for that project by setting the `type` and pasting the content in the text area
4. They save the project and repeat this 2 more times until they have 3 projects with content for each
5. They start the generation process by selecting 2 types of content they want to convert between. For example Jupyter notebook to blog.
6. They paste in a new Jupyter notebook and add some custom instructions for the conversion.
7. They hit the start button or whatever and it generates a blog post and displays it for the user in an editable textarea.

## Project Structure

Vesta uses a monorepo setup with npm workspaces, containing both the frontend and backend projects.

## Folder Structure

vesta/
├── packages/
│ ├── backend/ # Fastify Typescript backend application
│ │ ├── src/
│ │ │ ├── config/ # Configuration for the application
│ │ │ ├── routes/ # API Routes
│ │ │ ├── scripts/ # Scripts for the application
│ │ │ ├── server.ts # Main file for starting the server
│ │ │ └── services/ # API Services
│ │ └── test/ # Test files
│ │ ├── http/ # .http test files
│ ├── frontend/
│ │ ├── src/

# Instructions and Rules

- It is important that you update this file if anything in it changes! If you are unable to do so, please ask for help!
- Avoid arrow functions
- Include JSDocs for functions
- For adjusting dependencies, give me the terminal commands to run instead of editing the package.json file directly
- Use Tailwind CSS for styling in the frontend. Make it beautiful and adhere to the brand identity.
- Feel free to push back if you disagree with any of my suggestions. You are extremely smart, I trust your judgement!
- Never modify the api-docs.json directly. Instead adjust the code used to generate it if you need to.
- Assume I barely understand front end development. 
- Assume I know nothing about proper design or UI/UX, and you are responsible for making the app beautiful and user friendly.
- If you need to import a new component from shadcn, just give me the command to run to install it and import it. The proper command is `npx shadcn@latest add ...`
