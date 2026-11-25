# General coding style

Keep a clean and easy to understand codebase using idiomatic Rust that interoperates well with the wider embedded rust ecosystem.

Write good documentation for users (cargo docs), including useful examples and
usage code snippets. For developers, document the architecture and reasoning
behind coding decisions well. Do not add superfluous comments restating what is
obvious from the code.

Always make and maintain a long term project plan depending on the goals and progress.
Make semantic and atomic git commits with conventional commit messages according to subtasks.

# Project specific

I want to build a embedded-rust driver for the smartaudio and irctramp
protocols for communicating with FPV VTXs using half-duplex uart. it should be
built on a modular and layered architecture that is io and hal agnostic at the bottom with
layers of wrappers for common frameworks like embedded-hal, embedded-hal-async, embassy, rtic, etc.

A basic C implementation of the protocols are included in `reference/` to be used to understand the communication protocols.
The API need not match exactly, instead it should follow what is idiomatic in embedded rust and aim for more flexibility and ease of use.

For embedded rust projects efficiency and low overhead is the most importance, memory and cpu cycles are precious resources.
