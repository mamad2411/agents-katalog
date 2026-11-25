---
name: int-evo-crm
description: "Query and manage Evo AI CRM data via REST API. Use when you need to list/search contacts, conversations, messages, inboxes, pipelines (with stages and items), or labels. Supports filtering, pagination, creating/updating/deleting resources. Calls the CRM API directly with no third-party proxy."
metadata:
  openclaw:
    requires:
      env:
        - EVO_CRM_URL
        - EVO_CRM_TOKEN
      bins:
        - python3
    primaryEnv: EVO_CRM_TOKEN
    files:
      - "scripts/*"
---

# Evo CRM

Interact with your Evo AI CRM instance directly via the REST API.

## Setup (one-time)

1. Get your API access token from your CRM admin panel.
2. Set environment variables:
   ```
   EVO_CRM_URL=https://api.evoai.app
   EVO_CRM_TOKEN=your_api_access_token
   ```

## Commands

### Contacts

#### List contacts
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contacts [--sort name] [--page 1]
```

#### Get contact details
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contact <id>
```

#### Search contacts
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py search_contacts --q <term>
```

#### Filter contacts (advanced)
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py filter_contacts --payload '{"attribute_key":"city","filter_operator":"equal_to","values":["NYC"]}'
```

#### Create contact
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py create_contact --name "John Doe" [--email john@example.com] [--phone +5511999999999]
```

#### Update contact
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py update_contact <id> [--name "New Name"] [--email new@example.com] [--phone +5511999999999]
```

#### Delete contact
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py delete_contact <id>
```

#### Contact conversations
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contact_conversations <id>
```

#### Contact notes
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contact_notes <id>
```

#### Create contact note
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py create_contact_note <id> --content "Note text here"
```

#### Contact pipelines
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contact_pipelines <id>
```

### Conversations

#### List conversations
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py conversations [--status open] [--assignee_type all] [--inbox_id <id>] [--page 1]
```

#### Get conversation details
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py conversation <id>
```

#### Search conversations
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py search_conversations --q <term>
```

#### Filter conversations (advanced)
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py filter_conversations --payload '{"status":"open"}' [--page 1]
```

#### Conversation counts by status
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py conversation_meta [--status open] [--assignee_type all]
```

#### Create conversation
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py create_conversation --contact_id <id> --inbox_id <id>
```

#### Assign conversation
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py assign_conversation <id> --assignee_id <user_id>
```

#### Toggle conversation status
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py toggle_status <id> --status resolved
```

#### Toggle conversation priority
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py toggle_priority <id> --priority urgent
```

#### Mute/Unmute conversation
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py mute_conversation <id>
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py unmute_conversation <id>
```

#### Mark conversation as unread
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py mark_unread <id>
```

#### Send conversation transcript
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py send_transcript <id> --email user@example.com
```

### Messages

#### List messages in conversation
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py messages <conversation_id>
```

#### Send message (or private note)
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py create_message <conversation_id> --content "Hello" [--private]
```

#### Update message
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py update_message <conversation_id> <message_id> --content "Updated text"
```

#### Delete message
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py delete_message <conversation_id> <message_id>
```

#### Retry failed message
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py retry_message <conversation_id> <message_id>
```

### Inboxes

#### List all inboxes
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py inboxes
```

#### Get inbox details
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py inbox <id>
```

#### List inbox agents
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py inbox_agents <inbox_id>
```

#### Get assignable agents
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py assignable_agents <inbox_id>
```

#### List inbox message templates
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py inbox_templates <inbox_id>
```

### Pipelines

#### List all pipelines
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipelines
```

#### Get pipeline details
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline <id>
```

#### Pipeline stats
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline_stats
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline_stat <id>
```

#### List pipeline stages
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline_stages <pipeline_id>
```

#### List pipeline items
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline_items <pipeline_id> [--stage_id <id>] [--page 1]
```

#### Create pipeline item
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py create_pipeline_item <pipeline_id> --contact_id <id> --stage_id <id>
```

#### Move item to stage
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py move_item <pipeline_id> <item_id> --stage_id <target_stage_id>
```

#### Bulk move items
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py bulk_move_items <pipeline_id> --item_ids id1,id2,id3 --stage_id <target>
```

#### Remove pipeline item
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py remove_pipeline_item <pipeline_id> <item_id>
```

#### Pipeline items stats
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py pipeline_items_stats <pipeline_id>
```

### Labels

#### Contact labels
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py contact_labels <contact_id>
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py add_contact_labels <contact_id> --labels label1,label2
```

#### Conversation labels
```bash
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py conversation_labels <conversation_id>
python3 /mnt/skills/user/int-evo-crm/scripts/evo_crm_client.py add_conversation_labels <conversation_id> --labels label1,label2
```

## Output

JSON to stdout. List responses include pagination metadata:
```json
{
  "success": true,
  "data": [...],
  "meta": { "pagination": { "page": 1, "total": 336, "totalPages": 17 } }
}
```

## Resources

- contacts, conversations, messages, inboxes, pipelines, pipeline_stages, pipeline_items, labels
