# Find Work Skill

Scan for available work and self-assign the highest-priority unassigned task.

## Steps

1. **Check coordinator for claimed tasks**: Query `GET /tasks` to see what's already claimed.
2. **List open issues**: Run `gh issue list --state open --search "no:assignee" --json number,title,labels,createdAt --limit 20` to find unassigned GitHub issues.
3. **Filter out claimed**: Remove issues that already appear in the coordinator's task list.
4. **Pick highest priority**: Select the issue with the highest priority label, or the oldest unassigned issue if no priority labels exist.
5. **Self-assign**: Publish a `task` message to your own DM channel with the selected issue details.

## Priority Labels (highest first)

- `P0` / `critical` / `urgent`
- `P1` / `high`
- `P2` / `normal` (default)
- `P3` / `low`

## Output

If work is found, publish to your DM channel:
```json
{
  "type": "task",
  "payload": {
    "task": "Work on issue #<number>: <title>",
    "issue_number": <number>,
    "source": "find-work"
  }
}
```

If no work is available, do nothing (silent return).

## Notes

- This skill is designed to be triggered by the BehaviorManager during idle periods.
- It should NOT be triggered while actively processing a task.
- The coordinator is optional — if unreachable, just scan GitHub issues.
