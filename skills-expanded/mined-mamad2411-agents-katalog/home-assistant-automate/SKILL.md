---
name: home-assistant-automate
description: Smart home automation with Home Assistant
version: 1.0.0
tags: [iot, smart-home, automation, self-hosted]
---

# Home Assistant – Smart Home Automation

Home Assistant is the world's most popular open-source home automation
platform with 2000+ integrations and a powerful REST API.

- **GitHub**: github.com/home-assistant/core (85 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Foundation-backed. Regular security updates. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{HASS_URL}}` | Base URL of the Home Assistant instance |
| `{{HASS_TOKEN}}` | Long-lived access token |

## Usage Examples

### Get all entity states

```bash
curl -s "{{HASS_URL}}/api/states" \
  -H "Authorization: Bearer {{HASS_TOKEN}}"
```

### Toggle a light

```bash
curl -s -X POST "{{HASS_URL}}/api/services/light/toggle" \
  -H "Authorization: Bearer {{HASS_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}'
```

### Fire an automation

```bash
curl -s -X POST "{{HASS_URL}}/api/services/automation/trigger" \
  -H "Authorization: Bearer {{HASS_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'
```

## AI Agent Tips

- REST API covers states, services, events, config, and history.
- Use WebSocket API for real-time event stream.
- Automations can be triggered, enabled, or disabled via API.
- Integrates with voice assistants, cameras, sensors, and climate systems.
