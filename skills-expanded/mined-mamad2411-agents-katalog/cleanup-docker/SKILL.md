---
name: cleanup-docker
description: Remove unused Docker images, containers, volumes, and build cache to reclaim disk space
argument-hint: "[--images|--volumes|--all]"
related:
  - ask-me
  - run-clean
  - run-cleanup
---

## Goal

Clean up unused Docker resources — dangling images, stopped containers, unused volumes, build cache — to safely reclaim disk space

## Scope

- Covers: `docker system`, images, containers, volumes, build cache, networks
- Destructive: requires a dry run (show reclaimable) + user confirmation before deleting
- Skip: running containers, mounted volumes, recently used images

## Execute

### 1. Survey Usage

> Goal: Measure current space and resources

1. `docker system df` — view reclaimable space by category
2. `docker images`, `docker ps -a`, `docker volume ls`, `docker network ls` — gather everything
3. `docker builder du` — view build cache breakdown

### 2. Classify Candidates

> Goal: Separate deletable items from those to keep

1. Safe: dangling images (`<none>`), stopped containers older than N days, unused networks, build cache
2. Caution: tagged images with no container using them, unattached volumes
3. Keep: running containers, mounted volumes, images of active projects, recent base images
4. Cross-check volumes against compose files in the project — named volumes may hold important data

### 3. Dry-Run Report

> Goal: Show what will be deleted and the space reclaimed

1. Use a table: `No.`, `Resource`, `Type`, `Size`, `Last Used`, `Safe`
2. Summarize the reclaimable total from `docker system df`
3. Wait for user confirmation via `/ask-me` before deleting

### 4. Clean

> Goal: Delete according to the confirmed scope

1. `docker container prune` — stopped containers
2. `docker image prune` — dangling; `docker image prune -a` only if the user opts in
3. `docker volume prune` — only after confirming no important data
4. `docker builder prune` — build cache
5. `docker network prune` — unused networks
6. Or `docker system prune` per scope — never add `-a`/`--volumes` without explicit confirmation

### 5. Verify

> Goal: Confirm space reclaimed and nothing broke

1. `docker system df` again — compare reclaimable before/after
2. Confirm running containers still work — `docker ps`
3. Report the space actually reclaimed

## Rules

### 1. Confirmation Required

- Never prune without showing reclaimable first and getting confirmation
- `prune -a` and `--volumes` are highly destructive — they require separate explicit approval

### 2. Data Safety

- Volumes may hold database data — always check before deleting
- If unsure whether a volume matters → keep it and flag it for the user to decide

### 3. Evidence-Based

- Report actual sizes from `docker system df`, not guesses
- Include last-used or created date when it helps the decision
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Disk space reclaimed as reported, with real numbers
- No running services or important data deleted
- List of kept resources with reasons
