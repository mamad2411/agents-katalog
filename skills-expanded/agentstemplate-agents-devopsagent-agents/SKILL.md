# Project Overview:

This project intends to

# Technical details

## Project Discovery

Before starting any work, you MUST first search through the repo or folder to understand the project and its patterns. Do not assume you know the project — discover it:

- **Search the codebase** to understand what the project is about, its purpose, and its structure.
- **Identify patterns** for key subjects such as:
    - Infrastructure as Code tooling (Terraform, Pulumi, CloudFormation, CDK, Ansible)
    - Container orchestration (Kubernetes, Docker Swarm, ECS, Nomad)
    - CI/CD platforms (GitHub Actions, GitLab CI, Jenkins, CircleCI, ArgoCD)
    - Cloud provider and services (AWS, GCP, Azure, DigitalOcean)
    - Deployment strategy (blue-green, canary, rolling, immutable)
    - Environment management (dev, staging, production, ephemeral)
    - Secret management (Vault, AWS Secrets Manager, GCP Secret Manager, SOPS)
    - Monitoring and alerting (Prometheus, Grafana, Datadog, CloudWatch, PagerDuty)
    - Logging infrastructure (ELK, Loki, CloudWatch Logs, Fluentd)
    - Networking patterns (VPC, load balancers, CDN, DNS, service mesh)
    - Container registry and image management
    - Cost management and resource tagging
    - Disaster recovery and backup strategy
    - Security scanning (SAST, DAST, container scanning, dependency scanning)
    - Naming conventions (resources, tags, environments, variables)
    - Folder structure and IaC module organization
- **Use glob and grep tools** to quickly scan for these patterns before writing any code.
- **Read key files** like terraform configs, Dockerfile, docker-compose, CI configs, README, and existing infrastructure source to understand the infra stack and conventions.
- **Write your findings concisely** into the **Project Overview** and **Technical details** sections above, so they persist for future reference.

### If the project is new (empty or no existing patterns found)

Survey the user with the following questions and document their answers into the **Project Overview** and **Technical details** sections above. For each question, provide suggestions based on what you find in the codebase OR based on your knowledge of common patterns and best practices — the user can accept a suggestion, modify it, or provide their own answer. If the project is new and empty, help the user brainstorm by suggesting well-known options and trade-offs for each question:

1. What is this project from the infrastructure perspective? What services and environments need to be managed?
2. What Infrastructure as Code tooling will be used? (Terraform, Pulumi, CloudFormation, CDK, Ansible)
3. What cloud provider and services will be used?
4. What container orchestration platform will be used? (Kubernetes, ECS, Docker Swarm)
5. What CI/CD platform will be used? (GitHub Actions, GitLab CI, Jenkins, ArgoCD)
6. What deployment strategy will be followed? (blue-green, canary, rolling)
7. What secret management solution will be used?
8. What monitoring and alerting stack is in place?
9. What disaster recovery and backup strategy is required?
10. What security scanning and compliance requirements must be met?

### After discovery is complete

Once all findings have been documented into the **Project Overview** and **Technical details** sections — or if the user opts not to answer the survey questions — remove this entire **Project Discovery** section from AGENTS.md. Its purpose is one-time bootstrapping only.

# Strategy

For each implementation, generate a folder with the implementation name in the format `.specs/function-or-bug-fix`, each folder will have the name of the function or bug fix it intends to achieve.
- Inside it, you will generate three documents:
    - **Requirements:** What needs to happen, in the format of user story:
        - **UC[Number]:** As a user, I want/need to [what needs to happen or needs to be fixed]
    - **Conditional**:
        - If a feature:
            - **design.md:** How it will be done.
                - **Overview**: The context of the task being achieved. A concise three paragraphs introduction to the task.
                - **Glossary**: The naming conventions encountered or useful for the task execution. All the terms the agent will need to keep in the context while executing the plan.
                - **Architecture:**
                    - A Brief paragraph describing the architecture of the design of the feature.
                    - Titles with mermaid diagrams, flow, success criteria, components, files to be created, code snippets, testing strategy, verification approach, etc... Everything the design needs to be achieved... More items can be added as needed.
                        - Each item will be a title or subtitle.
                - **Infrastructure Specification:**
                    - Resource definitions and dependencies
                    - Network topology and security groups
                    - Cost estimation notes
                    - Scaling policies and resource limits
                    - Rollback and disaster recovery plan
        - If a bug:
            - **bugfix.md**:
                 - **Overview**: The context of the task being achieved. A concise three paragraphs introduction to the task.
                - **Glossary**: The naming conventions encountered or useful for the task execution. All the terms the agent will need to keep in the context while executing the plan.
                - **Bug details**: What is the anomaly?
                - **Bug condition**: This bug manifests when... [details]
                - **Examples:** Examples of the bug occurrence.
                - **Logs and metrics**: Relevant monitoring output for diagnosis
                - **Impact assessment**: Which environments/services are affected
                - **Unchanged behaviors**
                - **Fix Implementation**
                    - Assuming our root analysis is correct:
                        - Implementation description
                        - Rollback procedure
        - **tasks.md**: Step by step implementation with verification gates of the previous files. The tasks itself.
            - [ ] 1. Task
            - [ ] 2. Task
            - [ ] 3. Task
            - [ ] etc...
            - Each task can have as many subtasks as needed.
            - ## Task Dependency Graph
            ```json
            {
              "waves": [
                { "wave": 1, "tasks": ["<task_id>", "..."] },
                { "wave": 2, "tasks": ["<task_id>", "..."] }
              ]
            }
            ```
            Task IDs reference the numbered tasks above. Tasks in the same wave have no dependencies on each other and can run in parallel. A wave only starts after all tasks in the previous wave are complete. Add as many waves as the task complexity demands.
        - After the conclusion of any task is completed, mark it as done.
        - Update AGENTS.md regularly to match the project architecture, code standards, build instructions and things as such.

## DevOps-Specific Rules

- **Immutable infrastructure**: Prefer recreating resources over mutating them in place. State is managed declaratively.
- **Least privilege**: Every service account, IAM role, and network rule must grant the minimum permissions required. No wildcards in production.
- **Zero-downtime deployments**: All deployment strategies must account for maintaining availability. Document rollback procedures for every change.
- **Drift detection**: IaC must be the single source of truth. Manual console changes are prohibited unless in an emergency, and must be back-imported.
- **Cost awareness**: Every infrastructure change must include a cost impact assessment. Tag all resources for cost allocation.
- **Secret hygiene**: Secrets are never stored in plaintext, environment variables in CI configs, or committed to repositories. Use a secrets manager exclusively.
- **Blast radius minimization**: Changes should be scoped to the smallest possible impact. Use feature flags, canary releases, and progressive rollouts.

## Verification & Validation

After implementing infrastructure changes, you MUST verify:

- **Validate IaC**: Run linting (tflint, checkov, terrascan, hadolint) and plan commands to catch errors before apply.
- **Test in isolation**: Apply changes to a non-production environment first. Verify resource creation and configuration.
- **Check monitoring**: After deployment, confirm metrics and health checks are reporting as expected.
- **Verify rollback**: Ensure the rollback procedure has been tested or documented before promoting to production.

## User Confirmation Before Proceeding

Before starting the implementation of a spec, you MUST present the plan to the user and wait for explicit confirmation. This is not optional — no spec implementation should be started without user approval.

- **Always wait for user confirmation** before beginning implementation of a spec (i.e., after requirements, design, and tasks documents are created). No exceptions.
- Present a clear summary of what will be done, which resources will be created/modified, estimated cost impact, and potential risks.
- Only proceed after the user explicitly confirms (e.g., "yes", "go ahead", "proceed").
- If the user rejects or requests changes, update the plan accordingly and ask for confirmation again.