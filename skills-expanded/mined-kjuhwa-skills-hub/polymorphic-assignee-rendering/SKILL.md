---
name: polymorphic-assignee-rendering
description: Model an assignee that may be a human member OR an AI agent with (assignee_type, assignee_id) columns and render-time dispatch to distinct visual styling.
category: architecture
version: 1.0.0
tags: [domain-model, polymorphism, agents, issue-tracker, ui]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- A product where AI agents are first-class actors: they can be assigned, create work, comment, and change status.
- You want to avoid leaking agent semantics into code that only cares about humans, and vice versa.

## Steps

1. Schema: two columns on the parent entity, plus separate tables for members and agents:
   ```sql
   ALTER TABLE issues
     ADD COLUMN assignee_type TEXT
       CHECK (assignee_type IN ('member', 'agent')),
     ADD COLUMN assignee_id UUID;
   CREATE INDEX idx_issues_assignee ON issues (assignee_type, assignee_id);
   ```
   No foreign key — you can't FK a polymorphic column. Enforce existence at the application layer.
2. Query helper that hydrates either an Agent or Member based on `assignee_type`:
   ```go
   type AssigneeRef struct {
       Type string  // "member" | "agent"
       ID   string
   }
   func LoadAssignee(ctx context.Context, q *db.Queries, ref *AssigneeRef) (Member, *Agent, error) {
       if ref == nil { return Member{}, nil, nil }
       switch ref.Type {
       case "member": m, err := q.GetMember(ctx, ref.ID); return m, nil, err
       case "agent":  a, err := q.GetAgent(ctx,  ref.ID); return Member{}, &a, err
       }
       return Member{}, nil, fmt.Errorf("unknown assignee_type: %q", ref.Type)
   }
   ```
3. TS type union on the frontend:
   ```ts
   export type Assignee =
     | { type: "member"; id: string; name: string; avatar_url: string }
     | { type: "agent";  id: string; name: string; icon: string };
   ```
4. Render-time dispatch with distinct styling:
   ```tsx
   function AssigneeAvatar({ assignee }: { assignee: Assignee }) {
     if (assignee.type === "agent") {
       return <div className="bg-purple-500/10 text-purple-600 rounded-full p-1"><RobotIcon /></div>;
     }
     return <Avatar src={assignee.avatar_url} />;
   }
   ```
5. Permission checks branch on type too: "can assign" may allow assigning to any workspace member but only to non-archived agents, etc.

## Example

Issue list shows a mix of `assignee_type: "member"` (standard avatar) and `assignee_type: "agent"` (purple robot icon). Users can filter by assignee kind as well as by specific assignee.

## Caveats

- Keep validation server-side: reject writes where `assignee_type = "agent"` and the referenced UUID is not in the agents table for this workspace.
- Don't try to merge members and agents into one logical table; their lifecycle and permissions diverge enough that you'd regret it. The polymorphism is at the reference site only.
- Report filters and dashboards that split by type are worth the effort — hiding the distinction in aggregate stats loses signal ("how much work did agents do this week?").
