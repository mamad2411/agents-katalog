---
name: yolo-init
description: Use when setting up YOLO in a repo for the first time, or repairing the setup. Creates workspace/features/ and workspace/config.yaml. Triggers on "set up YOLO here", "init yolo", "yolo init".
---

# yolo-init

Make a repo YOLO-ready. Idempotent: safe to re-run as a repair. Rules:
`../../yolo/conventions.md`.

## Procedure
1. Create `workspace/features/` if missing, with a `.gitkeep`.
2. If `workspace/config.yaml` is missing, copy `../../yolo/templates/config.yaml` there. Set
   `project.name` to the repo directory name and `project.base_branch` with the detection
   rule (conventions *base_branch*). If it exists, only fill missing keys; never overwrite a
   value the user set.
3. Commit (`yolo: init`).

## Upgrading from older YOLO
Older versions also created `workspace/decisions/`, `workspace/debug/`, task trailers and a
routing block in the project's agent instructions file. Leave existing files alone; they are
history. If the user wants the routing block gone, remove the text between the
`YOLO:routing-block start` and `end` markers.

## Constraints
- Never git-ignore `workspace/`. It has to survive branches and worktrees.
- Writes only project state: `workspace/` and its config.
