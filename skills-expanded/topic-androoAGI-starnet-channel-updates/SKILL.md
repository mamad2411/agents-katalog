---
name: channel-updates
description: "Send short, phone-first updates to the Commander on Telegram, Discord, Slack, Matrix or Signal — and know when a message should not be sent at all."
license: MIT
metadata:
  title: "Channel Updates"
  category: "Communication"
  author: "StarNet"
---

An update on a phone is read in five seconds between other things. It either tells the Commander something they needed, or it teaches them to mute the station. Most runs should not ping.

## When NOT to ping
- Nothing crossed the bar the Commander set. In a routine, reply exactly `[SILENT]` — a silent run delivers nothing.
- The Commander is talking to you in COMMS right now. Answer there.
- It is progress, not an outcome ("started", "still working") — unless they asked for progress.
- The same news already went out. One change, one message.
- You are not sure it is true. Verify first; a wrong alert costs more than a late one.

## Method
1. **See who you can reach (channel.targets).** It lists the chats a person has actually opened with this station, their channel, the agent each is bound to, and whether it is connected right now. You cannot message a new id, number or channel name — reach is widened by a person opening a chat, never by you.
2. **Lead with the outcome.** First line: what happened and what it means — "Build is green on main, ready to ship." Then at most three short lines: the key number, the file, and the one decision needed, if any.
3. **Fit the phone.** One screen. No tables, no headers, no wall of bullets. Plain text is split into platform-sized parts automatically, but a message needing more than eight parts is refused — put the detail in a file.
4. **Attach instead of pasting.** Pass up to four workspace files in `files`: images arrive inline, other files as documents. A channel that cannot carry files gets the path named instead.
5. **Ask at most one question,** answerable with one word or a number.
6. **Send (channel.send) and read the result.** In APPROVAL mode the Commander confirms the send. A channel that is not connected is refused with nothing sent — report that, and point them to the CHANNELS panel to reconnect.
7. **For scheduled updates, use the routine's own delivery, not channel.send.** An unattended run has nobody to approve a send. Create the routine from the chat that should receive it (routine.create with `deliver: origin`) and write the `[SILENT]` rule into its prompt.

## Rules
- **Report exactly what was sent.** The tool says how many parts landed; never say "sent" when it failed or stopped part way.
- **Never send secrets, keys or private file contents** to a chat, even the Commander's own. The station scrubs what it recognizes; do not rely on that.
- **Never ping to prove you are working.** Silence is the correct report when nothing changed.
- Match the Commander's language and tone.

## Done means
The message the Commander needed arrived on a connected chat, the tool confirmed delivery, and nothing went out that did not clear the bar.

## Output
The target, the message as sent, the delivery result — or the reason nothing was sent.

*Needs the DISH object (outbound channels ride the station's antenna). Scheduled delivery uses the ORCHESTRATOR's routine tools.*
