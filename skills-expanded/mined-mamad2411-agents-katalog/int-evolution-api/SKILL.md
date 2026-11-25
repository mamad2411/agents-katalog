---
name: int-evolution-api
description: "Manage WhatsApp instances and send messages via the Evolution API. Use when you need to list/create/connect instances, send messages (text, media, location, contact, buttons, lists, polls), query chats/contacts, manage groups, or configure webhooks. Calls the Evolution API REST endpoints directly."
metadata:
  openclaw:
    requires:
      env:
        - EVOLUTION_API_URL
        - EVOLUTION_API_KEY
      bins:
        - python3
    primaryEnv: EVOLUTION_API_KEY
    files:
      - "scripts/*"
---

# Evolution API

Interact with your Evolution API instance to manage WhatsApp connections, send messages, query chats, manage groups, and configure webhooks.

## Setup (one-time)

1. Get your API URL and global API key from your Evolution API instance.
2. Set environment variables:
   ```
   EVOLUTION_API_URL=https://api.evolution-api.com
   EVOLUTION_API_KEY=your-global-api-key
   ```

## Instance Management

### List all instances
```bash
python3 scripts/evolution_api_client.py instances
```

### Create a new instance
```bash
python3 scripts/evolution_api_client.py create_instance my-instance
python3 scripts/evolution_api_client.py create_instance my-instance --qrcode
```

### Connect instance (returns QR code)
```bash
python3 scripts/evolution_api_client.py connect my-instance
```

### Get connection state
```bash
python3 scripts/evolution_api_client.py connection_state my-instance
```

### Restart an instance
```bash
python3 scripts/evolution_api_client.py restart my-instance
```

### Logout and disconnect
```bash
python3 scripts/evolution_api_client.py logout my-instance
```

### Delete an instance
```bash
python3 scripts/evolution_api_client.py delete_instance my-instance
```

### Set presence
```bash
python3 scripts/evolution_api_client.py set_presence my-instance --presence available
```

### Summary of all instances
```bash
python3 scripts/evolution_api_client.py summary
```

## Send Messages

### Send text
```bash
python3 scripts/evolution_api_client.py send_text my-instance 5511999999999 "Hello, world!"
```

### Send media (image, video, audio, document)
```bash
python3 scripts/evolution_api_client.py send_media my-instance 5511999999999 --type image --url https://example.com/photo.jpg --caption "Check this out"
```

### Send location
```bash
python3 scripts/evolution_api_client.py send_location my-instance 5511999999999 --lat -23.5505 --lng -46.6333 --name "Sao Paulo"
```

### Send contact card
```bash
python3 scripts/evolution_api_client.py send_contact my-instance 5511999999999 --name "John Doe" --phone 5511888888888
```

### Send buttons
```bash
python3 scripts/evolution_api_client.py send_buttons my-instance 5511999999999 --text "Choose an option" --buttons '[{"buttonId":"1","buttonText":{"displayText":"Option 1"}}]'
```

### Send list
```bash
python3 scripts/evolution_api_client.py send_list my-instance 5511999999999 --title "Menu" --sections '[{"title":"Section 1","rows":[{"title":"Item 1","rowId":"1"}]}]'
```

### Send poll
```bash
python3 scripts/evolution_api_client.py send_poll my-instance 5511999999999 --name "Favorite color?" --values "Red,Blue,Green"
```

### React to a message
```bash
python3 scripts/evolution_api_client.py send_reaction my-instance --key '{"remoteJid":"5511999999999@s.whatsapp.net","fromMe":false,"id":"MSG_ID"}' --reaction "👍"
```

### Send template message
```bash
python3 scripts/evolution_api_client.py send_template my-instance 5511999999999 "Template text here"
```

## Chat Operations

### Find chats
```bash
python3 scripts/evolution_api_client.py find_chats my-instance
python3 scripts/evolution_api_client.py find_chats my-instance --where '{"id":"5511999999999@s.whatsapp.net"}' --take 10
```

### Find messages
```bash
python3 scripts/evolution_api_client.py find_messages my-instance --where '{"key":{"remoteJid":"5511999999999@s.whatsapp.net"}}' --take 20
```

### Mark messages as read
```bash
python3 scripts/evolution_api_client.py mark_read my-instance --messages '[{"remoteJid":"5511999999999@s.whatsapp.net","fromMe":false,"id":"MSG_ID"}]'
```

### Archive/unarchive chat
```bash
python3 scripts/evolution_api_client.py archive_chat my-instance 5511999999999 --archive true
```

### Update profile name
```bash
python3 scripts/evolution_api_client.py update_profile_name my-instance "New Name"
```

### Update profile status
```bash
python3 scripts/evolution_api_client.py update_profile_status my-instance "Available for business"
```

## Contacts

### Find contacts
```bash
python3 scripts/evolution_api_client.py find_contacts my-instance --where '{"id":"5511999999999@s.whatsapp.net"}'
```

### Check numbers on WhatsApp
```bash
python3 scripts/evolution_api_client.py check_numbers my-instance --numbers 5511999999999,5511888888888
```

## Group Operations

### Create group
```bash
python3 scripts/evolution_api_client.py create_group my-instance --subject "My Group" --participants 5511999999999,5511888888888
```

### Get group info
```bash
python3 scripts/evolution_api_client.py group_info my-instance --jid 120363xxxxx@g.us
```

### List group participants
```bash
python3 scripts/evolution_api_client.py group_participants my-instance --jid 120363xxxxx@g.us
```

### Add/remove/promote/demote participants
```bash
python3 scripts/evolution_api_client.py update_participant my-instance --jid 120363xxxxx@g.us --action add --participants 5511999999999
```

## Webhook Management

### List webhooks
```bash
python3 scripts/evolution_api_client.py webhooks my-instance
```

### Set webhook
```bash
python3 scripts/evolution_api_client.py set_webhook my-instance --url https://example.com/hook --events messages.upsert,connection.update
```

### Delete webhook
```bash
python3 scripts/evolution_api_client.py delete_webhook my-instance
```

## Output

All output is JSON to stdout. Use `--json` flag for raw JSON on any command (default behavior).

## Notes

- Phone numbers use country code format without `+` (e.g. `5511999999999`).
- Group JIDs follow the pattern `120363...@g.us`.
- The `connect` endpoint returns a QR code as base64 PNG in the response.
- The `summary` command is composite: it calls `fetchInstances` then `connectionState` for each instance.
