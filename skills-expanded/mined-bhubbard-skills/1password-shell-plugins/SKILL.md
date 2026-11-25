---
name: 1password-shell-plugins
description: Securely authenticate third-party CLIs (like AWS, GitHub) using 1Password Shell Plugins and biometrics, avoiding plaintext credentials on disk.
---

# 1Password Shell Plugins

This skill explains how to use and build 1Password Shell Plugins to secure CLI tool authentication.

## Overview
1Password Shell Plugins eliminate the need to store plaintext API keys or credentials on your disk. They securely authenticate third-party command-line interfaces (CLIs) using your 1Password credentials and biometrics.

## Usage
- **Listing Plugins**: Run `op plugin list` to see all supported plugins.
- **Initialization**: Run `op plugin init` to configure your environment to use shell plugins. By default, this configures `~/.config/op/plugins.sh`.
- **Authentication**: Once configured, running a supported CLI command (like `aws` or `gh`) will prompt for 1Password biometric authentication instead of relying on plaintext configuration files.

## Building a Plugin
If a CLI you use is not supported natively, you can build a custom shell plugin.
1. Clone the official repository: [1Password/shell-plugins](https://github.com/1Password/shell-plugins).
2. Run `make new-plugin` to scaffold a new plugin.
3. Follow the contribution guidelines to build and test your plugin, and optionally contribute it back to the community.
