---
name: turbo-browser
description: Use when driving a browser through the turbo-browser MCP tools (tabs_batch, inspect_compact, smart_fill_form, act_fast, batch_actions). Gives the low-token loop for reading pages, filling forms, chaining steps and verifying a submit.
---

# Driving a browser with turbo-browser

Aim for few calls and small results. Each call below replaces several one-action calls.

## 1. Look once, then only changes

Call `inspect_compact` once. Later calls pass `onlyChanged` so the result lists only new or changed elements (marked `*`). Narrow big pages with `query` or `selector`. Use refs from the latest snapshot only.

```
inspect_compact {"mode":"forms"}
inspect_compact {"onlyChanged":true}
inspect_compact {"mode":"article","selector":"main","maxChars":3000}
```

For plain reading use `extract_clean_text` (`format` markdown or text).

## 2. Fill a whole form in one call

`smart_fill_form` takes every field at once. Comboboxes use `option`, uploads use file paths. It stops before Submit.

```
smart_fill_form {"fields":[{"selector":"#email","value":"a@b.co"},{"ref":"f0:e7","option":"Vietnam"},{"selector":"input[type=file]","file":"cv.pdf"},{"ref":"f0:e9","check":true}],"returnSnapshot":true,"snapshotMode":"forms"}
```

## 3. Chain steps

`batch_actions` runs steps in order. Set `returnSnapshot` to get the end state in the same reply. Add `snapshotQuery` when a re-render is large and you only need part of it.

```
batch_actions {"steps":[{"action":"click","text":"Next"},{"action":"wait","textNew":"Step 2"},{"action":"fill","selector":"#phone","value":"0900000000"}],"returnSnapshot":true,"snapshotQuery":"phone|Continue"}
```

Read feeds with `collect`, which scrolls, reads and de-duplicates:

```
batch_actions {"steps":[{"action":"navigate","url":"https://example.com/list"},{"action":"collect","selector":".row","scrolls":8,"maxItems":100}]}
```

## 4. Waiting

In `act_fast` or a step, `wait` accepts `text`, `textGone`, `url` or `loadState`. Use `textNew` to wait for text that was not on the page when the step started; plain `text` returns at once if the words already exist.

```
act_fast {"action":"wait","textNew":"Saved|Error","timeoutMs":8000}
```

## 5. Submit safely

Final actions (Submit, Send, Pay, Book, Schedule) are blocked unless `allowSubmit` is true. Pass `expect` so the reply says whether it worked. Prefer `textNew` over `textMatches`, because old text on the page also matches `textMatches`. Add `submissionKey` to stop a second submit.

```
batch_actions {"steps":[{"action":"click","text":"Schedule meeting"}],"allowSubmit":true,"expect":{"textNew":"confirmed","timeoutMs":8000},"submissionKey":"booking-2026-11-20"}
```

Check `submitVerified` in the result. If it is false, inspect the page before retrying.

## 6. Login, captchas, 2FA

Use `wait_for_human` with `urlMatches` or `selector`. The agent resumes in the same tab. Do not try to solve checks.

```
wait_for_human {"message":"Log in, then return","urlMatches":"/dashboard","timeoutMs":300000}
```

## 7. Tabs and separate sessions

`tabs_batch` opens and lists tabs in one call. Give `isolatedContext` a name to get separate cookies and storage, for example two accounts at once.

```
tabs_batch {"operations":[{"action":"open","url":"https://example.com","isolatedContext":"acct-a"},{"action":"open","url":"https://example.com","isolatedContext":"acct-b"}]}
tabs_batch {"operations":[{"action":"open_many","urls":["https://example.com/a","https://example.com/b"]}]}
```

## Habits

- Prefer `text` or `ref` targets over coordinates.
- One `batch_actions` call beats five `act_fast` calls.
- Treat an error as data: read it, fix the target, retry once.
