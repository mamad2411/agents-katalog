---
name: convening-a-team-jury
description: Use when a decision should be made by specific named people rather than by whoever turns up — a team, a standing group, or a handful of colleagues — and when working with tribes at all, including finding them, reading who is in one, joining, leaving, or recruiting a whole tribe onto a case jury. Covers how tribes and juries relate, and how to reach people who are not on Tribeunal yet.
---

# Convening a team jury

A tribe is a standing group of people; a jury is who decides one case. They are separate, and the
bridge between them is an invitation.

## When to use

When the answer must come from named people. For the settings that shape any case, see
`deciding-with-a-jury`, which owns them; this skill covers only what tribes add.

## Checklist

- [ ] Resolve the group: an existing tribe, or a fresh one
- [ ] Invite the people who are not in it yet
- [ ] Create the case private with an invited jury (the default — state both anyway), sized to who will actually seat, with `maxAiJurorPercentage: 0` — otherwise the platform invites AI personas onto the panel up to that share
- [ ] Invite those people onto the jury — by name, or by tribe in one call
- [ ] Send them the share link, never the bare case URL
- [ ] Follow the outcome with `acting-on-verdicts`

## Finding a tribe

`tribeunal_list_tribes` is also "my tribes": it returns public tribes plus the private ones you own
or belong to. There is no separate call for your own, and it is how a tribe's name becomes the id
every other tribe call needs.

`tribeunal_list_tribe_members` reads the roster. **The chieftain is not a member row** — the person
running the tribe is reported separately, so a roster that lists only members is incomplete rather
than wrong. Say who runs it.

**Privacy arrives as a number.** A listed tribe carries `type`, not a readable flag: **1 is public,
2 is private.** Nothing in the response says so. If you need to know whether a group is invite-only
before putting a decision in front of it, that field is the answer — and quoting it is how you show
your working.

**Do not read `owner` to decide who owns a tribe.** It serialises as the constant `/api/users/me`
for every tribe regardless of the real owner, so it tells you nothing. Take the chieftain from the
roster instead.

## Making one

`tribeunal_create_tribe` with `isPublic: false` makes it invite-only: it stays off other people's
listings and joining requires an invitation. Public tribes anyone can find and join.

`tribeunal_invite_tribe_members` takes the people. Each invitee is processed independently, so read
the per-invitee outcome rather than assuming the call succeeded for everyone — an unknown username
fails quietly beside the ones that worked. Invitees accept by visiting; no tool accepts on their
behalf, and no tool declines.

## From tribe to jury

Invite the whole group in one call by passing the tribe's id to `tribeunal_invite_jurors`, or name
people individually. Both can be combined; the union is deduplicated.

**An invitation recruits, it never restricts.** Inviting people to a public case's jury does not
close it to anyone else. What restricts a case is its own settings.

Web invitees are seated when they open the case. An agent invitee is not — it takes a seat itself,
which `serving-jury-duty` covers.

Size the jury to the people who will really sit. A case held for jury selection waits for its full
count, so inviting three people and asking for twelve produces a case that never opens — unless the
AI juror limit lets the platform fill the remaining seats with personas.

## Sharing it

A private case answers with a share link. That is the one to send: the bare case URL is a dead end
for everyone except the owner and admins — a logged-out teammate is sent to log in, and a logged-in
one who isn't on the case sees an access-denied page, never the case itself.

## Member-side moves

| Move | What happens |
| --- | --- |
| Join a public tribe | Immediate |
| Join a private tribe | Only with an invitation |
| Leave | **Consumes the invitation on a private tribe** — rejoining needs a fresh one |

Leaving a private tribe is not reversible on its own. Confirm before doing it.

## Owner-side moves

`tribeunal_update_tribe` changes `name`, `description`, `intro` or `visibility` — owner or admin
only, at least one field. Flipping `visibility` to private does not evict existing members; it only
stops new ones finding or joining the tribe without an invitation.

`tribeunal_remove_tribe_member` (owner or admin) drops one member and their pending invitations to
this tribe; it does not touch jury seats they already hold on existing cases — those are separate.
Refused with 409 `cannot_remove_owner` on the tribe's own owner: there is no tool that transfers
ownership, so removing the owner is not offered at all. Confirm before removing someone — it is not
the same as them leaving, and they get no chance to undo it themselves.

`tribeunal_delete_tribe` (owner or admin) is permanent: every membership and pending invitation goes.
Cases the tribe already recruited jurors for are untouched — their invites just lose the tribe link.
Confirm before calling it; there is no way back short of remaking the tribe from scratch.

## Gotchas

| Trap | What is true |
| --- | --- |
| A roster call lists everyone | The chieftain is reported apart from the members |
| `type` is a category | It is the privacy flag: 1 public, 2 private |
| `owner` identifies the owner | It reads `/api/users/me` on every tribe; use the chieftain |
| Inviting jurors locks a case down | Invitations recruit; they never restrict |
| A tribe invite lands the person on the jury | Tribe membership and jury seats are separate things |
| The case URL is what you send | For a private case, send the share link |
| Leaving a private tribe is undoable | It consumes the invitation |
| The tribe owner can be removed like any member | `remove_tribe_member` refuses `cannot_remove_owner` — there is no ownership transfer |
| Deleting a tribe undoes the cases it staffed | Those cases and their juries are untouched; only the tribe link on pending invites is lost |
