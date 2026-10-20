---
description: Upload a local file to surge.sh and return a public unguessable URL
argument-hint: <path/to/file>
---

You will publish the file `$ARGUMENTS` to surge.sh and return a public URL.

Steps:

1. If `$ARGUMENTS` is empty, tell the user the usage is `/share-file <path>` and stop.

2. Verify the file exists with `test -f "$ARGUMENTS"`. If it doesn't, report the error and stop.

3. Check if `surge` is installed: `command -v surge`. If not, run `npm install -g surge` and report what happened. If install fails (likely a permissions issue), tell the user to run `sudo npm install -g surge` themselves and stop.

4. If this is the first surge use on this machine, surge needs an account. Run `surge whoami` to check. If it says not logged in, tell the user they need to run `surge login` (or `surge` once interactively) themselves to create a free account, then re-run the command. Do not try to automate the login.

5. Create a temp deploy directory: `STAGE=$(mktemp -d)`.

6. Determine the filename and extension. If the file is `.html` or `.htm`, copy it as `index.html` so it renders at the root: `cp "$ARGUMENTS" "$STAGE/index.html"`. Otherwise (e.g. `.md`, `.txt`, anything else):
   - For `.md`: convert to HTML with `npx --yes marked -i "$ARGUMENTS" -o "$STAGE/index.html"`. If marked is unavailable or fails, fall back to copying the raw file as `index.html` and note that in the final output.
   - For anything else: copy the file into `$STAGE` keeping its name, AND create a minimal `$STAGE/index.html` that links to it, so the share URL works directly.

7. Generate a random subdomain: `SUB=$(openssl rand -hex 6).surge.sh`.

8. Deploy: `surge "$STAGE" "$SUB"`. Capture output.

9. If deploy succeeded, output ONLY this to the user (no other commentary):

   ```
   https://<SUB>
   ```

   Replace `<SUB>` with the actual subdomain. That single line is the entire response.

10. If deploy failed, show the surge error output and stop.

Notes:
- The URL is public but unguessable (12 hex chars = 2^48 entropy).
- The deployment persists until removed with `surge teardown <SUB>`.
- Do NOT delete `$STAGE` — surge needs nothing from it after deploy, but leaving it costs nothing and avoids race conditions.
