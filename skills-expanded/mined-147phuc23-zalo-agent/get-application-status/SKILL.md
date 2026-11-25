# Get Application Status
Description: Retrieve the status and timeline of the candidate's active job applications.

Use this skill when the candidate asks about the progress or status of their submitted job applications ("hồ sơ em tới đâu rồi?", "kết quả ứng tuyển thế nào?", etc.).

Input contract:
- None (parameters: `{}`)

Output contract:
- An array of candidate's applications, each containing:
  - `jobTitle`: Title of the job posting.
  - `companyName`: Name of the hiring company.
  - `stage`: Current stage of the application pipeline (`submitted`, `screening`, `interviewing`, `offer`).
  - `status`: Outcome status (`active`, `hired`, `rejected`, `withdrawn`).
  - `updatedAt`: ISO timestamp of the last status update.
  - `lastNote`: Optional note from the last transition.
  - `interviewProcess`: Optional array of standard interview rounds for this company, each containing `round` (number), `name` (string), and `description` (string).
  - `timelineEvents`: Optional array of actual historical events for this candidate's application, each containing `fromStage`, `toStage`, `fromStatus`, `toStatus`, `note` (optional), and `createdAt` (ISO timestamp). Use this timeline to calculate and report duration/telemetry (e.g. how long the candidate has been in the current stage!).
