---
name: brew-apt
description: Package manager commands for macOS (Homebrew) and Linux (apt, yum/dnf). Use when user mentions "brew", "homebrew", "apt", "apt-get", "yum", "dnf", "install package", "update packages", "package manager", "brew cask", "PPA", "system dependencies", "upgrade all", or managing system packages.
---

# Package Manager Reference: Homebrew, APT, DNF/YUM

## Homebrew (macOS)

### Install, Remove, Upgrade

```bash
brew install <package>              # Install a formula
brew install <package>@<version>    # Install specific version
brew uninstall <package>            # Remove a package
brew reinstall <package>            # Reinstall (useful after macOS upgrades)
brew update                         # Update Homebrew itself and tap metadata
brew upgrade                        # Upgrade all outdated packages
brew upgrade <package>              # Upgrade one package
brew outdated                       # List outdated packages
```

### Search and Inspect

```bash
brew search <term>                  # Search by name or partial match
brew info <package>                 # Version, dependencies, install path
brew list                           # All installed formulae
brew list --versions                # Installed formulae with versions
brew deps --tree <package>          # Dependency tree
```

### Casks (GUI Applications)

Casks manage macOS GUI applications (.app bundles, installers, fonts).

```bash
brew install --cask <app>           # Install a GUI app
brew list --cask                    # List installed casks
brew upgrade --cask                 # Upgrade all casks
brew uninstall --cask <app>         # Remove a cask
brew search --cask <term>           # Search casks
```

### Taps (Third-Party Repositories)

```bash
brew tap <user/repo>                # Add a third-party repository
brew tap                            # List all taps
brew untap <user/repo>              # Remove a tap
brew install <user/repo>/<formula>  # Install from a specific tap
```

### Brewfile (Reproducible Setups)

```bash
brew bundle dump --file=~/Brewfile          # Export current packages
brew bundle dump --force --file=~/Brewfile  # Overwrite existing Brewfile
brew bundle install --file=~/Brewfile       # Install from Brewfile
brew bundle check --file=~/Brewfile         # Check what is missing
brew bundle cleanup --file=~/Brewfile       # Remove unlisted packages
```

Example Brewfile:

```ruby
tap "homebrew/bundle"
tap "hashicorp/tap"
brew "git"
brew "node@20"
brew "python@3.12"
cask "visual-studio-code"
cask "docker"
mas "Xcode", id: 497799835   # Mac App Store (requires mas)
```

### Services

```bash
brew services start <service>       # Start (e.g., postgresql, redis)
brew services stop <service>        # Stop
brew services restart <service>     # Restart
brew services list                  # List all managed services
brew services run <service>         # Run once, no startup registration
```

### Cleanup

```bash
brew cleanup                        # Remove old versions and stale downloads
brew cleanup -n                     # Dry run
brew cleanup -s                     # Remove all cache files
du -sh "$(brew --cache)"            # Show cache size
```

### Pin Packages

Pinning prevents a package from being upgraded by `brew upgrade`.

```bash
brew pin <package>
brew unpin <package>
brew list --pinned
```

### Troubleshooting

```bash
brew doctor                         # Run diagnostic checks
brew update-reset                   # Reset to clean state (re-fetches taps)
brew --prefix <package>             # Show install path
brew install -v <package>           # Verbose install for debugging
```

---

## APT (Debian / Ubuntu)

### Install and Remove

```bash
sudo apt install <package>                # Install
sudo apt install -y <package>             # Install without prompting
sudo apt install <package>=<version>      # Specific version
sudo apt remove <package>                 # Remove (keeps config files)
sudo apt purge <package>                  # Remove including config files
sudo dpkg -i <file.deb>                   # Install local .deb file
```

### Update vs Upgrade vs Full-Upgrade

```bash
sudo apt update                    # Refresh package index (installs nothing)
sudo apt upgrade                   # Upgrade installed packages (never removes)
sudo apt full-upgrade              # Upgrade, removing obsolete packages if needed
```

Always run `apt update` before `apt upgrade`.

### Search and Inspect

```bash
apt search <term>                  # Search by name or description
apt show <package>                 # Package details
apt list --installed               # List installed packages
apt list --upgradable              # List upgradable packages
apt-cache policy <package>         # Version and repository info
```

### PPAs (Personal Package Archives)

```bash
sudo add-apt-repository ppa:<user>/<ppa-name>
sudo apt update
sudo add-apt-repository --remove ppa:<user>/<ppa-name>   # Remove a PPA
# List configured repos
grep -r --include='*.list' '^deb ' /etc/apt/sources.list /etc/apt/sources.list.d/
```

On newer Ubuntu, repos use DEB822 `.sources` files in `/etc/apt/sources.list.d/`.

### Hold Packages

```bash
sudo apt-mark hold <package>       # Prevent upgrades
sudo apt-mark unhold <package>     # Allow upgrades again
apt-mark showhold                  # List held packages
```

### Cleanup

```bash
sudo apt autoremove                # Remove orphaned dependencies
sudo apt clean                     # Clear local package cache
sudo apt autoclean                 # Remove only outdated cached packages
```

---

## DNF / YUM (RHEL / Fedora / CentOS)

DNF replaced YUM starting with Fedora 22 and RHEL 8. Command syntax is nearly identical.

### Install and Remove

```bash
sudo dnf install <package>         # Install
sudo dnf install -y <package>      # Install without prompting
sudo dnf remove <package>          # Remove
sudo dnf reinstall <package>       # Reinstall
```

### Upgrade

```bash
sudo dnf upgrade                   # Upgrade all packages
sudo dnf check-update              # Check for updates without installing
sudo dnf upgrade <package>         # Upgrade one package
```

`dnf update` is an alias for `dnf upgrade`.

### Search and Inspect

```bash
dnf search <term>                  # Search
dnf info <package>                 # Package details
dnf list installed                 # List installed
dnf list updates                   # List available updates
dnf provides <file-or-command>     # Find which package provides a file
```

### Repositories

```bash
dnf repolist                                    # List enabled repos
dnf repolist all                                # List all repos
sudo dnf config-manager --add-repo <url>        # Add a repo
sudo dnf config-manager --set-enabled <repo-id> # Enable a repo
sudo dnf config-manager --set-disabled <repo-id># Disable a repo
```

### Version Lock

```bash
sudo dnf install dnf-plugin-versionlock    # Install the plugin
sudo dnf versionlock add <package>         # Lock a package
sudo dnf versionlock delete <package>      # Unlock
dnf versionlock list                       # List locked packages
```

### Cleanup

```bash
sudo dnf autoremove                # Remove unneeded dependencies
sudo dnf clean all                 # Clean cached metadata and packages
sudo dnf clean packages            # Clean cached packages only
```

---

## Cross-Platform Comparison

| Task                       | Homebrew (macOS)          | APT (Debian/Ubuntu)              | DNF (RHEL/Fedora)              |
|----------------------------|--------------------------|----------------------------------|--------------------------------|
| Refresh package index      | `brew update`            | `sudo apt update`                | `sudo dnf check-update`       |
| Install                    | `brew install pkg`       | `sudo apt install pkg`           | `sudo dnf install pkg`        |
| Remove                     | `brew uninstall pkg`     | `sudo apt remove pkg`            | `sudo dnf remove pkg`         |
| Upgrade all                | `brew upgrade`           | `sudo apt upgrade`               | `sudo dnf upgrade`            |
| Upgrade one                | `brew upgrade pkg`       | `sudo apt install --only-upgrade pkg` | `sudo dnf upgrade pkg`   |
| Search                     | `brew search term`       | `apt search term`                | `dnf search term`             |
| Package info               | `brew info pkg`          | `apt show pkg`                   | `dnf info pkg`                |
| List installed             | `brew list`              | `apt list --installed`           | `dnf list installed`          |
| List outdated              | `brew outdated`          | `apt list --upgradable`          | `dnf list updates`            |
| Hold / pin version         | `brew pin pkg`           | `sudo apt-mark hold pkg`        | `sudo dnf versionlock add pkg`|
| Remove unused deps         | `brew autoremove`        | `sudo apt autoremove`            | `sudo dnf autoremove`         |
| Clean cache                | `brew cleanup`           | `sudo apt clean`                 | `sudo dnf clean all`          |
| Diagnose issues            | `brew doctor`            | `sudo apt --fix-broken install`  | `sudo dnf distro-sync`        |
| Add third-party repo       | `brew tap user/repo`     | `add-apt-repository ppa:u/repo`  | `dnf config-manager --add-repo`|
