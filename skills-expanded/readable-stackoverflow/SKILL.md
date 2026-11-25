---
name: readable-stackoverflow
description: Fetches a Stack Overflow question body and its answers via the Stack Exchange API (api.stackexchange.com/2.3 with the withbody filter, gzip-compressed). Anonymous quota is 300 req/day per IP; honor the response backoff field. Surface the question URL when displaying content (CC BY-SA attribution). Use when the URL is in the form stackoverflow.com/questions/{id}/...
---

# Stack Overflow Question Reader

Uses the public Stack Exchange API. Anonymous usage is rate-limited to ~300 requests per IP per day.

## Steps

### 1. Extract the question ID

From a URL like `https://stackoverflow.com/questions/12345678/some-slug`, the ID is `12345678`.

### 2. Fetch the question body

```bash
curl -s --compressed \
  "https://api.stackexchange.com/2.3/questions/{id}?site=stackoverflow&filter=withbody"
```

### 3. Fetch the answers

```bash
curl -s --compressed \
  "https://api.stackexchange.com/2.3/questions/{id}/answers?site=stackoverflow&filter=withbody&sort=votes&order=desc"
```

The response uses gzip; the `--compressed` flag is required by the API.

### 4. Honor backoff

If a response includes a `backoff` field, do not call the API again for that many seconds.

## Attribution

Stack Exchange content is licensed under CC BY-SA. When surfacing answers, include the question URL and note the source as Stack Overflow.

## Reference

- API docs: https://api.stackexchange.com/docs
- Throttle / backoff: https://api.stackexchange.com/docs/throttle
- Data licensing: https://stackoverflow.com/help/licensing
