---
name: github-workflows
description: Manage and automate Android CI/CD workflows using GitHub Actions in this repository.
---

# GitHub Workflows Skill

This skill provides instructions for managing, extending, and troubleshooting the GitHub Actions workflows in the `automated-build-android-app-with-github-action` project.

## Workflow Overview

The repository contains several workflows located in `.github/workflows/`:

1.  **Android CI (Main)**:
    - `android-ci-generate-apk-aab-upload-push-github.yml`: Builds APK/AAB and pushes the results to the `buildActionResult` folder in the repository.
    - `android-ci.yml`: Basic CI for building and testing.
2.  **Artifact Management**:
    - `android-ci-generate-apk-aab-upload.yml`: Builds and uploads artifacts to GitHub Actions.
    - `android-ci-generate-apk-aab-download.yml`: Research workflow for downloading artifacts.
3.  **Deployment**:
    - `android-ci-publish-play-store.yml`: (In research) Template for publishing to Google Play Store.

## Key Environment Variables

Each workflow uses common environment variables defined at the top of the file:

- `main_project_module`: Usually `app`.
- `playstore_name`: Display name for the app (e.g., `Frogobox ID`).
- `build_output_path`: Directory where build results are stored (e.g., `buildActionResult`).

## Common Tasks

### Adding a New Build Step
To add a new Gradle task to a workflow, insert a new step in the `jobs.build.steps` section:

```yaml
- name: Your Task Name
  run: ./gradlew yourTaskName
```

### Modifying the Output Directory
If you want to change where the APKs/AABs are pushed in the repository, update the `build_output_path` env variable.

### Triggering Workflows
- **Push**: Workflows are typically triggered on push to `release/**` branches.
- **Manual**: Use `workflow_dispatch` to trigger manually from the GitHub Actions tab.

## Troubleshooting

- **Permissions**: Ensure `./gradlew` has execution permissions (`chmod +x ./gradlew`).
- **JDK Version**: Workflows use JDK 17 by default. Ensure compatibility with your Gradle version.
- **Secrets**: Deployment workflows require secrets like `SIGN_KEY`, `ALIAS`, `STORE_KEY_PASSWORD`, and `KEY_PASSWORD`.
