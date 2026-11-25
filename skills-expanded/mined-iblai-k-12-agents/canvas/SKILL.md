---
name: canvas
description: Canvas LMS (Instructure) — read and write courses, modules, assignments, rubrics, grades, and submissions for K-12 classroom workflows.
metadata: {"openclaw":{"requires":{"env":["CANVAS_API_TOKEN","CANVAS_BASE_URL"]}},"primaryEnv":"CANVAS_API_TOKEN"}
---

# Canvas

## What it is
Canvas by Instructure is a leading cloud-based Learning Management System used widely in K-12 districts for course content delivery, assignment management, grading, and student communication. It exposes a comprehensive REST API supporting both read and write operations across its full data model.

## When to use this skill
- Retrieving assignment descriptions, rubrics, and due dates to give tutoring or writing-feedback context
- Publishing lesson modules, assignment shells, or pacing calendars created by the lesson-planning agent
- Uploading teacher-created content (worksheets, slide decks) to a course module
- Reading student submission text or attached documents for writing feedback workflows
- Pushing finalized quiz scores or rubric-scored grades back to the Canvas gradebook after teacher approval

## Credentials
This skill authenticates using env vars declared in the frontmatter metadata and provided via `~/.openclaw/.env` (see `.env.example` at the segment root). Required variables:
- `CANVAS_BASE_URL` - root URL of the Canvas instance (e.g. `https://district.instructure.com`)
- `CANVAS_API_TOKEN` - user or service-account API token generated in Canvas account settings

## Key operations
- `GET /api/v1/courses` — list courses for the authenticated user
- `GET /api/v1/courses/{id}/assignments` — retrieve assignments with rubrics and due dates
- `GET /api/v1/courses/{id}/modules` — read course module structure and items
- `POST /api/v1/courses/{id}/pages` — create a new content page in a course
- `GET /api/v1/courses/{id}/submissions` — fetch student submission bodies and metadata
- `PUT /api/v1/courses/{id}/assignments/{aid}/submissions/{uid}` — post a grade or rubric assessment
- `POST /api/v1/courses/{id}/quizzes` — create a new quiz (New Quizzes via LTI integration)

## Notes
- Canvas API uses pagination via `Link` headers; always follow `next` links when listing large collections.
- Rate limit is 3000 requests per hour per token by default; batch operations where possible.
- Write operations (grade passback, content publishing) require teacher-level or higher token scope.
- Prefer the Canvas Data 2 (CD2) streaming export for bulk analytics rather than paginated REST calls.
