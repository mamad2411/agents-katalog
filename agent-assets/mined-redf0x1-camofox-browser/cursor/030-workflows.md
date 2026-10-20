---
description: "Common camofox-browser workflows and automation patterns"
alwaysApply: true
---

# CamoFox Workflow Patterns

## 1) Basic Interaction Loop
```bash
camofox open https://example.com                   # open tab
camofox snapshot                                   # get refs
camofox click e5                                   # click
camofox type e7 "hello"                            # type
camofox snapshot                                   # refresh refs
```

## 2) Search Workflow
```bash
camofox open https://google.com                    # create tab
camofox search "camofox" --engine google           # navigate to search results
camofox snapshot                                   # inspect result refs
```

## 3) Login Workflow (Vault-Safe)
```bash
camofox auth save account --url https://service.com/login   # store encrypted credentials
camofox open https://service.com/login                      # open login page
camofox snapshot                                            # get username/password refs
camofox auth load account --inject --username-ref e5 --password-ref e9  # inject without stdout leaks
```

## 4) Pipeline Workflow
```bash
camofox run login-flow.txt                        # run file
camofox run login-flow.txt --continue-on-error    # keep going after failures
echo "get-url" | camofox run -                    # stdin pipeline
```

## 5) API + curl Workflow
```bash
curl -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","sessionKey":"task1","url":"https://example.com"}'

curl "http://localhost:9377/tabs/<tabId>/snapshot?userId=agent1"
```

## 6) Session Restore Workflow
```bash
camofox session save before-login                  # save cookies
# ... close/restart ...
camofox session load before-login                  # restore cookies to tab
```

## 7) CAPTCHA / Visual Intervention Workflow
```bash
curl -X POST http://localhost:9377/sessions/agent1/toggle-display \
  -H 'Content-Type: application/json' \
  -d '{"headless":"virtual"}'                   # restart with noVNC
# solve challenge manually via returned vncUrl
curl -X POST http://localhost:9377/sessions/agent1/toggle-display \
  -H 'Content-Type: application/json' \
  -d '{"headless":true}'                          # return to headless
```
