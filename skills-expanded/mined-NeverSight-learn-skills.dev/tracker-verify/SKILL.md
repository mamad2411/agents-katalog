---
name: tracker-verify
description: |
  Post-update verification for Excel trackers. Reads updated trackers and verifies all action items were added correctly with proper formatting.

  TRIGGERS: verify tracker, check tracker update, validate changes, confirm action items added

  Use when: After updating any tracker files to ensure changes were applied correctly
---

# Tracker Verify Skill

Verification system for tracker updates. Reads Excel files after modification and validates that all expected changes were made correctly.

## When to Use This Skill

**Always use after updating tracker files** to catch:
- Missing action items that should have been added
- Incorrect data in cells (wrong owner, date, task)
- Formatting issues (missing yellow highlighting for AI Generated items)
- Row count mismatches
- Corrupted files that can't be re-opened

---

## Inputs Required

When calling this skill, provide:

```yaml
trackers_updated:
  - tracker_path: "/sessions/ecstatic-nifty-galileo/mnt/Claude trackers/POD3/POD 3 Tracker.xlsx"
    sheet_name: "Internal - POD Open Issues"
    expected_additions: 2

  - tracker_path: "/sessions/ecstatic-nifty-galileo/mnt/Claude trackers/Manager Tracker.xlsx"
    sheet_name: "Manager Open Issues"
    expected_additions: 3

expected_items:
  - task: "(AI Generated) Add Tony Fair to SFDC"
    owner: "Jack"
    due_date: "2026-02-06"
    tracker: "POD 3"
    sheet: "Internal - POD Open Issues"

  - task: "(AI Generated) Log Cambridge AI event in Salesforce"
    owner: "Michele"
    due_date: "2026-02-06"
    tracker: "POD 4"
    sheet: "Internal - POD Open Issues"
```

---

## Verification Process

### Step 1: File Health Check

For each tracker file:

```python
from openpyxl import load_workbook

def verify_file_health(tracker_path):
    """
    Verify file can be opened and is not corrupted
    """
    try:
        wb = load_workbook(tracker_path)
        print(f"✓ File opens successfully: {tracker_path}")
        return True, wb
    except Exception as e:
        print(f"✗ File corrupted or unreadable: {tracker_path}")
        print(f"  Error: {str(e)}")
        return False, None
```

### Step 2: Row Count Verification

```python
def verify_row_count(wb, sheet_name, expected_additions):
    """
    Check if the number of rows increased by expected amount
    """
    ws = wb[sheet_name]

    # Find last row with data
    last_row = ws.max_row

    print(f"  Sheet: {sheet_name}")
    print(f"  Total rows: {last_row}")
    print(f"  Expected additions: {expected_additions}")

    # Note: We can't verify exact count without baseline,
    # but we can verify rows exist
    return last_row
```

### Step 3: Content Verification

For each expected item, verify:

```python
def verify_item_added(ws, expected_item):
    """
    Search for expected item in tracker
    Returns: (found, row_number, discrepancies)
    """
    found = False
    row_num = None
    discrepancies = []

    # Search all rows for the task
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        task_cell = row[1]  # Column B (Task)

        if task_cell.value and expected_item['task'] in task_cell.value:
            found = True
            row_num = task_cell.row

            # Verify owner (Column E)
            owner_cell = row[4]
            if owner_cell.value != expected_item['owner']:
                discrepancies.append(
                    f"Owner mismatch: expected '{expected_item['owner']}', "
                    f"found '{owner_cell.value}'"
                )

            # Verify due date (Column I)
            due_date_cell = row[8]
            expected_date = datetime.strptime(expected_item['due_date'], '%Y-%m-%d')
            if due_date_cell.value != expected_date:
                discrepancies.append(
                    f"Due date mismatch: expected '{expected_item['due_date']}', "
                    f"found '{due_date_cell.value}'"
                )

            # Verify yellow highlighting
            task_fill = task_cell.fill.start_color.rgb if task_cell.fill else None
            if task_fill != 'FFFFFF99' and task_fill != 'FFFF99':  # Yellow
                discrepancies.append(
                    f"Missing yellow highlighting on task cell"
                )

            break

    return found, row_num, discrepancies
```

### Step 4: Generate Verification Report

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TRACKER VERIFICATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**File Health Check:**
✓ POD 3 Tracker.xlsx - Opens successfully
✓ POD 4 Tracker.xlsx - Opens successfully
✓ Manager Tracker.xlsx - Opens successfully

**Content Verification:**

POD 3 Tracker - Internal - POD Open Issues:
  ✓ Row 45: (AI Generated) Add Tony Fair to SFDC
    - Owner: Jack ✓
    - Due Date: 2026-02-06 ✓
    - Yellow highlighting: ✓

POD 4 Tracker - Internal - POD Open Issues:
  ✓ Row 23: (AI Generated) Log Cambridge AI event in Salesforce
    - Owner: Michele ✓
    - Due Date: 2026-02-06 ✓
    - Yellow highlighting: ✓

  ✗ Row 24: (AI Generated) Finalize C-suite pitch deck
    - Owner: Michele ✓
    - Due Date: 2026-02-07 ✗ FOUND: 2026-02-08
    - Yellow highlighting: ✓

Manager Tracker - Manager Open Issues:
  ✓ All 3 items verified successfully

**Summary:**
- Total items expected: 6
- Items found: 6
- Items with discrepancies: 1
- Items missing: 0

⚠️ ISSUES FOUND:
1. POD 4 Tracker, Row 24: Due date mismatch (expected 2026-02-07, found 2026-02-08)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Output Format

Always provide:

1. **Health Check Status** - Can all files be opened?
2. **Item-by-Item Verification** - Each expected item found/missing?
3. **Discrepancy Details** - What doesn't match expectations?
4. **Summary Statistics** - Overall success rate
5. **Action Required** - What needs to be fixed?

---

## Usage Example

```markdown
User: I just updated POD 3, POD 4, and Manager trackers. Can you verify the changes?