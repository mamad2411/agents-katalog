---
name: share-report
description: Publish this machine's agenttrail-guard scan report as a Claude artifact on claude.ai, private to the user until they share it. Use only when the user asks to share or publish their agenttrail-guard scan report, or asks for a link to it.
when_to_use: For example "share my guard scan report", "publish my agenttrail report as an artifact", "give me a link to my guard report". Not for reading a scan locally, not for Cursor scans, and not for any other report.
---

# Share an agenttrail-guard scan report

The page you publish is the report the agenttrail-guard tool writes. The user installed that tool; it runs on this machine over the user's own Claude Code transcripts; and the page goes to the user's own claude.ai account, at their request, as their content. It carries the tool's name and logo the way any tool's generated report does. It is not a page by or on behalf of agenttrail, and you publish it exactly as the tool wrote it.

## Steps

1. **Check for the Artifact tool.** If Claude Code's Artifact tool is not available to you, including as a deferred tool you can load, follow "Without the Artifact tool" below instead.

2. **Scan.** Make a new temporary directory outside the project (your session's scratch directory if you have one), and run this with `<dir>` replaced by its absolute path:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/scripts/guard-scan.mjs" --agent claude --artifact --out "<dir>/agenttrail-guard-report.html" --no-open
   ```

   This writes the report into that directory only. Nothing leaves the machine in this step. Do not add `--review`: it prints the raw values of MCP tool calls, which the report never contains, into this conversation. If the command fails or the file is missing, show the output and stop.

3. **Show the user** the summary the command printed. Say that the report covers every Claude Code project on this machine, and quote the report's "Before you share this" section. Offer to list every command shape and guardrail name the file contains, read from the file itself.

4. **Ask before publishing**, even if your permission mode would let you publish without asking: "Publish this as a Claude artifact? It stays private to you until you share it." Continue only on a clear yes.

5. **Read the whole file** with the Read tool, continuing with `offset` and `limit` until you have read every line. Do not edit, reformat, restyle or regenerate it: the file the user reviewed is the file that gets published. If something in it looks wrong, tell the user instead of changing it.

6. **Publish** `<dir>/agenttrail-guard-report.html` with the Artifact tool, icon `shield`, and the description "agenttrail-guard scan report, generated on the user's machine from their own Claude Code sessions." If the publish is refused, show the reason and stop; never alter the file to get it through. To update the page later in this session, repeat step 2 with the same `<dir>` and publish the same path again.

7. **Reply** with the link. Say that the page is private to them until they share it, that anyone they share it with can read every command shape and guardrail name in it, and that the local copy is at `<dir>/agenttrail-guard-report.html`.

## Without the Artifact tool

A session signed in with an API key, on Bedrock, Vertex AI or Foundry, or with artifacts turned off, cannot publish. Run step 2 without `--artifact`, show the summary as in step 3, give the user the path of the file it wrote, and offer to open it in their browser. Do not upload it anywhere else.

## Cursor

Only Claude Code scans are published this way. For a Cursor scan, tell the user to run `agenttrail-guard scan --agent cursor`, which writes the report and opens it in their browser.
