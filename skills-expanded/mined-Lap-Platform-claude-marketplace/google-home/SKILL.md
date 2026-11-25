---
name: google-home
description: "Google Home API skill. Use when working with Google Home for supported_timezones, get_app_device_id, supported_locales. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Home
API version: 2.0

## Auth
ApiKey cast-local-authorization-token in header

## Base URL
http://example.com/setup

## Setup
1. Set your API key in the appropriate header
2. GET /supported_timezones -- verify access
3. POST /get_app_device_id -- create first get_app_device_id

## Endpoints

30 endpoints across 18 groups. See references/api-spec.lap for full details.

### supported_timezones
| Method | Path | Description |
|--------|------|-------------|
| GET | /supported_timezones | Timezones |

### get_app_device_id
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_app_device_id | App Device ID |

### supported_locales
| Method | Path | Description |
|--------|------|-------------|
| GET | /supported_locales | Locales |

### assistant
| Method | Path | Description |
|--------|------|-------------|
| POST | /assistant/check_ready_status | Check Ready Status |
| POST | /assistant/set_night_mode_params | Night Mode settings |
| GET | /assistant/alarms | Get Alarms and Timers |
| POST | /assistant/alarms/delete | Delete Alarms and Timers |
| POST | /assistant/notifications | Do Not Disturb |
| POST | /assistant/alarms/volume | Alarm Volume |
| POST | /assistant/a11y_mode | Accessibility |

### offer
| Method | Path | Description |
|--------|------|-------------|
| GET | /offer | Offer |

### eureka_info
| Method | Path | Description |
|--------|------|-------------|
| GET | /eureka_info | Eureka Info |

### test_internet_download_speed
| Method | Path | Description |
|--------|------|-------------|
| POST | /test_internet_download_speed | Test Internet Download Speed |

### reboot
| Method | Path | Description |
|--------|------|-------------|
| POST | /reboot | Reboot and Factory Reset |

### set_eureka_info
| Method | Path | Description |
|--------|------|-------------|
| POST | /set_eureka_info | Set Eureka Info |

### user_eq
| Method | Path | Description |
|--------|------|-------------|
| POST | /user_eq/set_equalizer | Set Equalizer Values |

### bluetooth
| Method | Path | Description |
|--------|------|-------------|
| GET | /bluetooth/scan_results | Get Scan Results |
| POST | /bluetooth/bond | Forget paired device |
| POST | /bluetooth/discovery | Change Discoverability |
| POST | /bluetooth/connect | Pair with Speaker |
| GET | /bluetooth/status | Status |
| POST | /bluetooth/scan | Scan for devices |
| GET | /bluetooth/get_bonded | Get Paired Devices |

### connect_wifi
| Method | Path | Description |
|--------|------|-------------|
| POST | /connect_wifi | Connect to Wi-Fi Network |

### scan_wifi
| Method | Path | Description |
|--------|------|-------------|
| POST | /scan_wifi | Scan for Networks |

### configured_networks
| Method | Path | Description |
|--------|------|-------------|
| GET | /configured_networks | Get Saved Networks |

### forget_wifi
| Method | Path | Description |
|--------|------|-------------|
| POST | /forget_wifi | Forget Wi-Fi Network |

### scan_results
| Method | Path | Description |
|--------|------|-------------|
| GET | /scan_results | Get Wi-Fi Scan Results |

### NOTICE.html.gz
| Method | Path | Description |
|--------|------|-------------|
| GET | /NOTICE.html.gz | Legal Notice |

### icon.png
| Method | Path | Description |
|--------|------|-------------|
| GET | /icon.png | Chromecast Icon |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all supported_timezones?" -> GET /supported_timezones
- "Create a get_app_device_id?" -> POST /get_app_device_id
- "List all supported_locales?" -> GET /supported_locales
- "Create a check_ready_status?" -> POST /assistant/check_ready_status
- "List all offer?" -> GET /offer
- "List all eureka_info?" -> GET /eureka_info
- "Create a test_internet_download_speed?" -> POST /test_internet_download_speed
- "Create a reboot?" -> POST /reboot
- "Create a set_night_mode_param?" -> POST /assistant/set_night_mode_params
- "Create a set_eureka_info?" -> POST /set_eureka_info
- "List all alarms?" -> GET /assistant/alarms
- "Create a delete?" -> POST /assistant/alarms/delete
- "Create a notification?" -> POST /assistant/notifications
- "Create a volume?" -> POST /assistant/alarms/volume
- "Create a set_equalizer?" -> POST /user_eq/set_equalizer
- "Create a a11y_mode?" -> POST /assistant/a11y_mode
- "List all scan_results?" -> GET /bluetooth/scan_results
- "Create a bond?" -> POST /bluetooth/bond
- "Create a discovery?" -> POST /bluetooth/discovery
- "Create a connect?" -> POST /bluetooth/connect
- "List all status?" -> GET /bluetooth/status
- "Create a scan?" -> POST /bluetooth/scan
- "List all get_bonded?" -> GET /bluetooth/get_bonded
- "Create a connect_wifi?" -> POST /connect_wifi
- "Create a scan_wifi?" -> POST /scan_wifi
- "List all configured_networks?" -> GET /configured_networks
- "Create a forget_wifi?" -> POST /forget_wifi
- "List all scan_results?" -> GET /scan_results
- "List all NOTICE.html.gz?" -> GET /NOTICE.html.gz
- "List all icon.png?" -> GET /icon.png
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
