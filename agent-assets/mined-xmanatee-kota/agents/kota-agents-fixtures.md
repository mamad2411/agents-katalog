# Telegram Fixtures

This directory holds redacted Telegram update and rendered-message fixtures used
by Telegram module tests.

- Keep examples small but representative of real channel shapes.
- Do not commit bot tokens, private file ids, raw media, phone numbers, or
  unredacted personal identifiers.
- Fixtures should exercise adapter boundaries; routing policy still belongs to
  the inbound-signals module.
