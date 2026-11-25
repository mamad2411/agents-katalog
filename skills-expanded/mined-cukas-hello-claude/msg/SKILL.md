# /msg — Send a message to another Claude session

Send a message to another active Claude Code session by callsign.

## When to use

- When the user says `/msg <callsign> "message"`
- When Claude decides another session should be informed of a change
- When replying to an incoming message from another session

## How to execute

1. Parse the target callsign and message from the arguments
2. Run the send script:

```bash
bash "$PLUGIN_DIR/scripts/send.sh" "<callsign>" "<message>"
```

3. Report the result to the user

## If no target specified

Run the list-sessions script to show who's available:

```bash
bash "$PLUGIN_DIR/scripts/list-sessions.sh"
```

Then ask the user who they want to message.

## Examples

- `/msg backend "I updated the API types, pull latest"`
- `/msg compiler "What's the current rule count?"`
- `/msg kirk "The landing page is ready for review"`

ARGUMENTS: callsign "message"
