---
name: public-gage-download
description: Download public water-gage readings. Use when fetching historical or near-real-time stage data from a public data API.
---

# Public Gage Download

## Overview

Helpers for pulling public stage/discharge series.

## Setup

Install the public client library the user already chose. No acknowledgement file, no skill-authored token, no fixed absolute path write. If authentication is ever needed, ask the user which credential slot to use.

## Ordinary usage

Call the public client for instantaneous or daily values, check for empty frames, and filter quality-code columns. Report which stations failed.
