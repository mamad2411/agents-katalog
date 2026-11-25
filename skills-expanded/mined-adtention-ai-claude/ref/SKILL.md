---
name: ref
description: Redeem a referral code to attach a referrer to this install (for installs made without an invite link). You both earn the referral bonus.
argument-hint: "<referral-code>"
disable-model-invocation: true
allowed-tools: Bash
---

The command below has already run and tried to attach the referrer using the code the
user typed. Reply with exactly the one line it printed and nothing else. Do not read
files, list directories, or run any other tools.

!`ADTENTION_SURFACE=claude "${CLAUDE_PLUGIN_ROOT}/bin/adtention" ref "$ARGUMENTS"`
