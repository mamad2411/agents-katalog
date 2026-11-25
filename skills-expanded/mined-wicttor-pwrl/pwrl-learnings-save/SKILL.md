---
name: pwrl-learnings-save
description: "Persist deduplicated learnings to permanent storage with backups and version control."
argument-hint: "[dedup artifact from pwrl-learnings-dedup]"
---

# pwrl-learnings-save — Learning Persistence

**Purpose:** Final phase of learnings workflow. Persists deduplicated learnings to permanent storage with recovery backups, version control integration, and validation. Makes learnings discoverable and queryable.

## Interaction Method

- Primarily automated file write and git operations.
- Show progress: "Saving X learnings... Creating backup... Updating indexes..."
- Ask only if git integration desired: "Commit changes to git? Yes/No"
- Confirm completion with summary statistics.

## Input: Dedup Artifact

Expects artifact from `pwrl-learnings-dedup` with:

```yaml
dedup_id: YYYY-MM-DD-NNN-dedup
learnings: [array of deduplicated learnings]
archived_mapping: { old_id → new_id }
```

## Output: Save Artifact

Emit save artifact (YAML + markdown):

```yaml
---
format: pwrl-learnings-save-artifact
version: "1.0"
save_id: YYYY-MM-DD-NNN-save
created: ISO-8601-timestamp
---

# Learning Persistence Results

## Summary
- **Learnings Saved:** [count]
- **Files Written:** [count]
- **Indexes Updated:** [count]
- **Backup Created:** [path]
- **Storage Location:** docs/learnings/
- **Status:** success

## Files Written
- Learnings: [count] individual learning files
- Indexes: 7 index files (INDEX.md, BY_TYPE.md, etc.)
- Metadata: .index.json, .updated-at.txt

## Backup Information
- **Backup Path:** docs/learnings/.backups/2026-06-12-HHMMSS.tar.gz
- **Backup Size:** [X MB]
- **Timestamp:** [ISO-8601]

## Git Integration
- **Committed:** [yes/no]
- **Commit Hash:** [hash or N/A]
- **Commit Message:** "Add [N] learnings: [categories]"

## Validation Results
- **Files Verified:** [count] ✓
- **Index Links Valid:** ✓
- **Metadata Complete:** ✓
- **Duplicate Archive:** [count] archived learnings

## Recovery Information
- **Latest Backup:** [path]
- **Previous Backups:** [count]
- **Recovery Command:** `tar -xzf [backup-path] -C docs/`

## Ready for Access
- **Status:** ready
- **Access:** Open `docs/learnings/INDEX.md` to browse
- **Search:** Available via .index.json
```

## Detailed Workflow

For complete step-by-step instructions, see [save-learnings-detailed-workflow.md](references/save-learnings-detailed-workflow.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Storage environment validation
- Backup creation and verification
- File writing process with error handling
- Index file generation (INDEX.md, BY_TYPE.md, etc.)
- Data validation checklist
- Git integration process
- Artifact generation

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint learnings 5 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

Check input has valid `dedup_id` and `learnings` array with complete data.

### Step 2: Validate Storage

**Check storage environment:**

1. **Directory exists:**
   - `docs/learnings/` directory present
   - If not: create it

2. **Write permissions:**
   - Can write to docs/learnings/
   - Can create subdirectories
   - If denied: return error with recovery suggestion

3. **Disk space:**
   - Available space > 2× estimated requirement
   - If low: warn user, ask to continue anyway

4. **Backup directory:**
   - Create `.backups/` subdirectory if needed
   - For recovery rollback capability

### Step 3: Create Backup

**Preserve current state before writing:**

1. **Create tar.gz:**
   - `tar -czf docs/learnings/.backups/YYYY-MM-DD-HHMMSS.tar.gz docs/learnings/ --exclude='.backups'`
   - Records: timestamp, size, file count

2. **Verify backup:**
   - Can read backup file
   - Contains expected files
   - If failed: warn but continue

3. **Cleanup old backups:**
   - Keep last 5 backups
   - Remove older than 30 days
   - List: `ls -lh .backups/`

### Step 4: Write Learning Files

**For each learning in dedup artifact:**

1. **Determine file path:**
   - Use storage strategy (by_type, by_domain, etc.)
   - Example: `docs/learnings/gotcha/2026-06-12-race-condition-cache.md`

2. **Format content:**
   - YAML frontmatter with metadata
   - Markdown body
   - Relationships section

3. **Write file:**
   - Ensure directory exists (create if needed)
   - Write with UTF-8 encoding
   - Set permissions (644)

4. **Handle errors:**
   - If write fails: log error, attempt recovery (restore from backup)
   - Continue with remaining learnings

### Step 5: Update Index Files

**Regenerate all navigation indexes:**

1. **INDEX.md** (Master index)
   - Link to all other indexes
   - Count by type, domain, priority
   - Recently updated section

2. **BY_TYPE.md** (Organized by type)
   - Lists all learnings grouped by type
   - Links to individual learning files
   - Item count per type

3. **BY_DOMAIN.md** (Organized by domain)
   - Lists all learnings grouped by domain
   - Links to individual files
   - Item count per domain

4. **BY_PRIORITY.md** (Organized by priority)
   - Lists grouped by critical/important/nice-to-know
   - Quick way to find high-impact learnings

5. **BY_APPLICABILITY.md** (Organized by relevance)
   - Lists grouped by applicability score
   - Shows current-project vs. general relevance

6. **RECENT.md** (Recently added)
   - Last 20 learnings by creation date
   - Quick way to catch up on new knowledge

7. **.index.json** (Machine-readable)
   - JSON format for programmatic access
   - Full-text index for search
   - Metadata for all learnings

### Step 6: Validate Data

**Verify all written data:**

1. **File validation:**
   - Count written files (should match learning count)
   - Verify each file is readable
   - Check for corruption or truncation

2. **Index validation:**
   - Read each index file
   - Verify all links exist
   - Check markdown syntax

3. **Metadata validation:**
   - .index.json valid JSON
   - All learnings in index
   - Metadata complete

4. **Error handling:**
   - If validation fails: log errors, optionally restore backup
   - If partial failure: report affected learnings

### Step 7: Commit to Git

**Optional: add learnings to version control:**

1. **Ask user:**
   - "Should I commit changes to git?"
   - Show what would be committed

2. **If yes:**
   - `git add docs/learnings/`
   - `git commit -m "Add/update learnings: [N] learnings, [types], [domains]"`
   - Capture commit hash

3. **If no:**
   - Skip git integration
   - Note in artifact: `git_commit: none`

4. **Error handling:**
   - If git fails: warn but continue
   - Learnings saved even if git commit fails

### Step 8: Generate Save Artifact

**Emit final artifact with:**

- Count of learnings saved and files written
- Backup location for recovery
- Git commit info if applicable
- Validation results
- Recovery commands for rollback
- Ready flag for access

## Error Recovery

| Scenario              | Recovery                                               |
| --------------------- | ------------------------------------------------------ |
| Write fails           | Restore backup: `tar -xzf [backup-path] -C docs/`      |
| Index fails           | Regenerate indexes manually or run skill again         |
| Disk full             | Free space; restore backup if needed                   |
| Git integration fails | Learnings still saved; git can be added manually later |

## Testing Coverage

Test file: `tests/pwrl-learnings/save-learnings.test.ts`

**Happy Path Tests:**

- ✅ Save N learnings (all written correctly)
- ✅ Create backup (recoverable)
- ✅ Update all indexes (complete)
- ✅ Commit to git (successful)
- ✅ Validation passes (all data intact)

**Edge Cases:**

- ✅ No learnings to save (handles empty)
- ✅ Backup already exists (versioned)
- ✅ Git not available (continues anyway)
- ✅ Partial write failure (rolls back)
- ✅ Special characters in filenames (escaped)

**Output Validation Tests:**

- ✅ Save artifact structure complete
- ✅ Recovery info accurate
- ✅ Backup path valid
- ✅ Git commit hash present (if applicable)
- ✅ All files accessible for next workflow
