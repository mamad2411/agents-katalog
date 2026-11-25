---
name: domino-launchers
description: Create and run Domino Launchers - self-service web forms that pass text, select, multi-select, date, checkbox and uploaded-file inputs to a script that runs as a Domino Job. Covers the launcher wizard, the command placeholder syntax, how arguments reach the script, result files and email delivery, roles, and finding launcher runs through the Jobs API. Use when building self-service reports, batch scoring forms, or data-product UIs for non-technical users.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino Launchers

Applies to Domino 6.3 and Domino Cloud.

A Launcher is a web form built in the Domino UI. When a consumer submits it, Domino starts a **Job** with the form values substituted into a command line, so every run is tracked, reproducible and auditable like any other Job. Results reach the consumer by email and through the Jobs dashboard. Launchers are defined in the UI wizard or through the Launchers web UI routes ("API" below); there is no YAML or file-based launcher definition and no Public API route.

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/launchers (same path under `/6.3/`).

## Build a Launcher

1. In the Project go to **Deployments > Launchers > New Launcher**.
2. Give it a name and description (the description is the help text consumers see).
3. Enter the **command**. It is the Job command with one `${name}` placeholder per form field; hard-coded arguments can be mixed in:
   ```shell
   generate_report.py --start ${start_date} --end ${end_date} --region ${region}
   launcher.R ${A} ${B}
   ```
4. Add one input control per placeholder. The available types are **Text**, **Select** (one item), **Multi-select**, **Date**, **Checkbox** (yes/no) and **Upload files**. There is no numeric type: accept a number as Text and validate it in the script.
5. Choose the hardware tier (on a Nexus deployment this also selects the data plane the Job runs in) and the environment, then save.

### How values reach the script

- Each value is wrapped in single quotes, so spaces and shell characters survive but environment variables inside a value are not expanded.
- **Upload files** passes the path of the uploaded file; uploaded files are stored as Project results (keep them well under a few GB).
- **Multi-select** passes the chosen options as one comma-separated string.
- Positional order follows the command, so parse with `sys.argv` / `argparse` in Python or `commandArgs(trailingOnly = TRUE)` in R. Worked scripts: [EXAMPLES.md](./EXAMPLES.md).

MPI compute clusters cannot be attached to Launcher runs.

## Results and notifications

Launcher output is Job output: every file the script creates or modifies is captured as a result and shown on the Job, and images or HTML are rendered in the results view.

- DFS Project: write results anywhere under the Project root (`/mnt`); in a Git-based Project write them under `/mnt/artifacts/results/` so they are attached to the email and shown as results.
- An `email.html` (Project root on DFS, `/mnt/artifacts/` on Git-based) becomes the body of the success email; `<head><title>` sets the subject. If you add a `.dominoresults` file to limit attachments, list `email.html` in it.
- Everyone on the launcher's notification list receives the email; the run also appears in **Jobs** with its inputs and results.
- Notebooks: a command that names an `.ipynb` file executes the notebook and saves it; use `jupyter nbconvert` in a wrapper script for HTML or PDF.

Details and patterns: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/jobs/customize-job-results and [EXAMPLES.md](./EXAMPLES.md).

## Run a Launcher

Consumers open **Deployments > Launchers**, click the launcher, fill in the form and run it. Collaborators with the **Contributor** or **Launcher User** role can run launchers; **Results Consumers** can only view results. Grant the role under Project **Settings > Access and Sharing** or with the Public API, `POST /api/projects/v1/projects/{projectId}/collaborators` `{"id": "<user id>", "role": "launcherUser"}` (6.3 and Cloud; `GET /api/users/v1/self` and the user routes give ids; details in [domino-projects](../domino-projects/SKILL.md)).

## Copy a Launcher between Projects

Open the launcher, click the gear icon > **Edit** > **Switch to JSON Edit Mode** to view or paste the JSON definition. This editor exists only on self-managed deployments; on Domino Cloud rebuild the launcher in the wizard.

## API

The Public API has no launcher routes. Launchers are managed through non-public routes, labelled per [route types](../domino-api-intro/SKILL.md#route-types); call them on `$DOMINO_API_HOST` with a bearer token ([domino-api-intro](../domino-api-intro/SKILL.md)).

- Create, read, update, delete: `POST /u/{owner}/{project}/runLaunchers`, then `GET` / `PUT` / `DELETE /u/{owner}/{project}/runLaunchers/{launcherId}` (non-public route; may change in a future Domino version). Create takes the full launcher JSON and returns it with its `id` as a draft (default `command`); `PUT` the object back with your `command` to store it, which also lists it on the Launchers page. Every parameter needs all its fields (`shouldQuoteValue` included); a missing one is an HTTP 500 `JsResultException` naming it. Bodies and listing: [EXAMPLES.md](./EXAMPLES.md#manage-launchers-from-code).
- List: no JSON list route; the Launchers page `GET /u/{owner}/{project}/endpoints/launchers` embeds it in its `LaunchersPage` mount props ([EXAMPLES.md](./EXAMPLES.md#manage-launchers-from-code)), or keep the ids you create.
- Start: `POST /v4/projects/{projectId}/launcherJob/{launcherId}` (non-public route; may change in a future Domino version) with `{"project": "<projectId>", "postParameters": [{"key": "<parameter>", "value": ["<value>"]}], "uploadedFiles": [], "notifyOnCompleteEmailAddresses": []}`; the response is the Job id and the Job's `runCommand` carries the substituted values.
- Find runs and results: `GET /api/jobs/beta/jobs?projectId=...` returns each run as a Job with `runLauncherId` set; `GET /api/jobs/beta/jobs/{jobId}` and `.../logs` give status and logs; fetch a result file with `GET /api/projects/v1/projects/{projectId}/files/{commitId}/{path}/content` using `commitDetails.outputCommitId` ([domino-jobs](../domino-jobs/SKILL.md)).

For a one-off run without a form, `POST /api/jobs/v1/jobs` with explicit arguments is simpler.

## Best practices

- Validate inputs in the script and fail with a clear message; a non-zero exit marks the run failed and triggers the failure email.
- Print progress to stdout; it is shown in the Job logs.
- Keep the command idempotent so consumers can re-run with different inputs.
- Test the script as a plain Job first with the same arguments.

## Troubleshooting

- **Run fails immediately**: run the command as a Job with literal values; check that every `${name}` has a matching control and that file paths are relative to the working directory (`/mnt` on DFS, `/mnt/code` on Git-based Projects).
- **Wrong or empty arguments**: remember the single-quoting; do not rely on `$VAR` expansion inside a value.
- **No email**: check the notification list on the launcher and the Project notification preferences; the email is sent on completion only.
- **Results missing from email**: Git-based Project outputs belong under `/mnt/artifacts/results/`; a `.dominoresults` file restricts attachments to what it lists.

## Reference files

- [EXAMPLES.md](./EXAMPLES.md): argument parsing in Python and R, result and `email.html` patterns, a complete scoring launcher.
- [domino-model-delivery](../domino-model-delivery/BATCH-SCORING.md): the scoring script behind a batch scoring form, and the scheduled Job alternative when nobody needs to submit a form.
