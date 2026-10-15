---
name: one-liners
description: Command-line one-liners for file manipulation, text processing, system administration, and quick automation. Use when user mentions "one-liner", "quick command", "bash one-liner", "command line trick", "shell trick", "pipe chain", "quick script", "inline command", "find and replace all files", "bulk rename", "process log files", "count lines", "disk usage", or needs a single-line shell command to solve a problem fast.
---

# One-Liners

Quick reference for single-line shell commands. For helper functions see `scripts/bash-helpers.sh` and `scripts/system-diagnostics.sh`. For extended examples see `references/bash-oneliners.md` and `references/advanced-oneliners.md`. Structured examples in `examples/common-oneliners.json`.

## File Operations

```bash
# Find by name, size, or age
find . -name "*.log" -type f
find . -type f -size +100M -exec ls -lh {} +
find . -type f -mtime -1                          # Modified in last 24h
find . -type f \( -name "*.ts" -o -name "*.tsx" \)

# Bulk rename
for f in *.jpeg; do mv "$f" "${f%.jpeg}.jpg"; done
for f in *; do mv "$f" "$(echo "$f" | tr 'A-Z' 'a-z')"; done
n=1; for f in *.png; do mv "$f" "$(printf '%03d.png' $n)"; ((n++)); done
rename 's/IMG_(\d+)/photo_$1/' *.jpg               # Perl rename

# Bulk delete
find /tmp -type f -mtime +30 -delete
find . -name "node_modules" -type d -prune -exec rm -rf {} +
find . -type d -empty -delete
ls -tp | grep -v '/$' | tail -n +6 | xargs rm --   # Keep 5 most recent

# Dedup and permissions
find . -type f -exec md5sum {} + | sort | uniq -w32 -dD
find . -type d -exec chmod 755 {} + && find . -type f -exec chmod 644 {} +
find . -name "*.sh" -exec chmod +x {} +
find / -type f -perm -o+w 2>/dev/null              # World-writable files
find / -nouser 2>/dev/null                          # Files owned by no user

# Backup with timestamp
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz directory/
```

## Text Processing

### grep Pipelines

```bash
grep -rn "TODO" --include="*.py" -A 2              # Recursive with context
grep -rc "import" --include="*.ts" . | grep -v ":0$" | sort -t: -k2 -rn
grep -v "^#" config.txt | grep -v "^$"             # Strip comments + blanks
grep -E "error|warn|fatal" app.log                  # Multiple patterns
grep -oP '(?<=email=)[^\s&]+' access.log            # Extract match only
grep -rL "use strict" --include="*.js" .            # Files NOT matching
```

### awk Columns

```bash
awk '{print $1, $4}' access.log                     # Specific columns
awk '{sum += $3} END {print sum}' data.txt           # Sum column
awk -F, '$3 > 100 {print $1, $3}' data.csv          # Filter by value
awk '{count[$1]++} END {for (k in count) print k, count[k]}' access.log | sort -k2 -rn
awk '!seen[$0]++' file.txt                           # Deduplicate preserving order
awk '{sum+=$1; sumsq+=$1*$1; n++} END {print "avg=" sum/n, "std=" sqrt(sumsq/n-(sum/n)^2)}' numbers.txt
```

### sed Replacements

```bash
# In-place replacement across files
find . -name "*.js" -exec sed -i '' 's/oldFunc/newFunc/g' {} +   # macOS
find . -name "*.js" -exec sed -i 's/oldFunc/newFunc/g' {} +      # Linux

sed '/^#/d' config.txt                               # Delete comment lines
sed -n '/BEGIN/,/END/p' file.txt                     # Extract between markers
sed '10,20s/foo/bar/g' file.txt                      # Replace on specific lines
sed 's/\x1b\[[0-9;]*m//g' colored-output.txt        # Strip ANSI codes
sed '/\[dependencies\]/a new_dep = "1.0"' Cargo.toml # Insert line after match
```

### Sorting and Counting

```bash
sort | uniq -c | sort -rn                            # Frequency count
sort file.txt | uniq -c | sort -rn | head -10        # Top 10 most common
sort -t, -k3 -n data.csv                             # Sort CSV by column 3
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn   # LOC per extension
find . -name "*.py" -exec grep -cv '^[[:space:]]*$\|^[[:space:]]*#' {} + | awk -F: '{sum+=$2} END {print sum}'
```

## System Information

```bash
# Disk
du -sh */ | sort -rh | head -10                      # Largest directories
df -h                                                # Disk usage summary
df -i                                                # Inode usage

# Memory and CPU
ps aux --sort=-%mem | head -10                       # Linux: top by memory
ps aux -m | head -10                                 # macOS: top by memory
ps aux --sort=-%cpu | head -10                       # Linux: top by CPU
ps aux -r | head -10                                 # macOS: top by CPU
free -h                                              # Linux memory summary
nproc                                                # Linux CPU count
sysctl -n hw.ncpu                                    # macOS CPU count

# Network connections
ss -tlnp                                             # Linux: listening ports
lsof -iTCP -sTCP:LISTEN -n -P                       # macOS: listening ports
lsof -p $(pgrep -f myapp)                            # Open files by process
fuser /var/log/syslog                                # Linux: who uses a file
lsof /var/log/system.log                             # macOS: who uses a file
watch -n 1 'uptime; free -h; df -h /'               # Linux: live dashboard
```

## Process Management

```bash
lsof -i :8080                                        # Find process by port
lsof -ti :8080 | xargs kill -9                       # Kill process on port
pkill -f "node server.js"                            # Kill by pattern
watch -n 1 "ps aux | grep '[n]ode'"                  # Monitor process
nohup ./long-task.sh > output.log 2>&1 &             # Background with nohup
timeout 30s ./slow-script.sh                         # Linux: run with timeout
gtimeout 30s ./slow-script.sh                        # macOS: needs coreutils
ps aux | awk '$8 == "Z" {print}'                     # List zombie processes
kill $(pgrep -f myapp) && sleep 5 && kill -9 $(pgrep -f myapp) 2>/dev/null   # Graceful then force
```

## Git One-Liners

```bash
# Log analysis
git shortlog -sn --all                               # Commits per author
git log --format='%ai' | cut -d' ' -f1 | sort | uniq -c
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20   # Hotspots
git log --author="name" --pretty=tformat: --numstat | awk '{a+=$1; r+=$2} END {print "+" a, "-" r}'

# Blame and search
git blame -L 10,20 file.js
git log -p -S "deletedFunction" --all                # Search history for string
git log --all --grep="fix login"                     # Search commit messages
git log --diff-filter=D --summary | grep "delete.*filename"

# Cleanup
git branch --merged main | grep -v "main" | xargs git branch -d
git remote prune origin
git clean -nd && git clean -fd                       # Dry run then remove
git gc --aggressive --prune=now
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print $3, $4}' | sort -rn | head -20
```

## Network

```bash
# curl
curl -o /dev/null -s -w "%{time_total}\n" https://example.com    # Response time
curl -LIs https://example.com                        # Follow redirects + headers
curl -s -X POST -H "Content-Type: application/json" -d '{"key":"val"}' https://api.example.com
curl --retry 3 --retry-delay 2 --retry-max-time 30 https://api.example.com/data

# Check multiple endpoints
for url in https://api.example.com/{health,ready,info}; do echo "$url: $(curl -s -o /dev/null -w '%{http_code}' "$url")"; done

# DNS
dig +short example.com A
dig +short example.com MX
dig -x 93.184.216.34                                 # Reverse DNS

# Batch downloads
xargs -n1 curl -O < urls.txt
cat urls.txt | xargs -P 4 -I {} curl -sO {}          # Parallel

# SSL certificate expiry
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Port scan without nmap
for port in 22 80 443 8080; do (echo >/dev/tcp/host/$port) 2>/dev/null && echo "$port open"; done
```

## JSON/YAML Processing

### jq

```bash
jq . data.json                                       # Pretty print
jq '.results[].name' data.json                       # Extract nested field
jq '[.[] | select(.status == "active")]' users.json  # Filter array
jq -r '.[] | [.id, .name, .email] | @csv' data.json > out.csv
jq -s '.[0] * .[1]' defaults.json overrides.json    # Merge files
jq '[group_by(.status)[] | {status: .[0].status, count: length}]' data.json
jq '.version = "2.0.0"' package.json | sponge package.json   # Modify in place
```

### yq

```bash
yq '.services.web.image' docker-compose.yml          # Read value
yq -i '.spec.replicas = 3' deployment.yaml           # Update value
yq -o=json '.' config.yaml                           # YAML to JSON
yq -P '.' config.json                                # JSON to YAML
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' base.yaml override.yaml
yq -i 'del(.metadata.annotations)' resource.yaml    # Delete key
```

## Docker One-Liners

```bash
docker ps -q | xargs docker stop                     # Stop all containers
docker system prune -af --volumes                    # Remove everything unused
docker system df -v                                  # Disk usage breakdown
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name
docker exec -it $(docker ps -lq) sh                  # Exec into latest container
docker ps -qf "label=app=myapp" | xargs -I {} docker cp {}:/app/logs ./logs-{}
docker compose logs -f --tail 50 api worker
docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -rh
docker export container_name | tar -tf - | head -50  # Inspect filesystem
```

## macOS-Specific

```bash
open .                                                # Open Finder here
open -a "Visual Studio Code" file.js                  # Open with app
pbcopy < file.txt                                     # Copy to clipboard
pbpaste > output.txt                                  # Paste from clipboard
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder   # Flush DNS
defaults write com.apple.finder AppleShowAllFiles YES; killall Finder
mdfind "kMDItemKind == 'PDF' && kMDItemFSName == '*invoice*'"    # Spotlight
say "build complete"                                  # Text to speech
xattr -d com.apple.quarantine /Applications/MyApp.app
system_profiler SPHardwareDataType SPSoftwareDataType
```

## Linux-Specific

```bash
inotifywait -m -r -e modify,create,delete ./src      # Watch file changes
systemctl status nginx && journalctl -u nginx --since "1 hour ago"
apt list --installed 2>/dev/null | grep -i pattern    # Debian/Ubuntu
rpm -qa | grep -i pattern                             # RHEL/Fedora
(crontab -l; echo "0 2 * * * /path/to/backup.sh") | crontab -   # Add cron job
for f in /proc/*/status; do awk '/VmSwap|Name/{printf $2 " " $3}' "$f" 2>/dev/null; echo; done | sort -k2 -rn | head -10
ldd /usr/bin/git                                      # Shared library deps
```

## Composability Patterns

### xargs and parallel

```bash
# xargs: parallel execution
find . -name "*.png" | xargs -P 4 -I {} convert {} -resize 50% {}
find . -name "*.log" -print0 | xargs -0 rm           # Null-delimited (safe)
git branch --merged | grep -v main | xargs -I {} git branch -d {}

# GNU parallel
parallel convert {} -resize 800x {} ::: *.jpg
parallel -a hosts.txt ping -c 1 {}
find . -name "*.csv" | parallel -j$(nproc) "wc -l {}"
parallel --bar gzip ::: *.log                         # With progress bar
```

### tee and Process Substitution

```bash
make 2>&1 | tee build.log                             # Write to file + stdout
diff <(ls dir1) <(ls dir2)                            # Compare two outputs
tail -f app.log | tee >(grep ERROR >> errors.log) >(grep WARN >> warnings.log)
curl -s https://api.example.com/data | tee response.json | jq '.count'
```

### Pipeline Recipes

```bash
# Find TODO/FIXME sorted by file
grep -rn "TODO\|FIXME" --include="*.py" | sort -t: -k1,1 -k2,2n

# Top 10 largest files modified in last week
find . -type f -mtime -7 -exec du -h {} + | sort -rh | head -10

# Monitor with change highlighting
watch -d -n 5 'curl -s https://api.example.com/status | jq .health'

# Fetch, process, store
curl -s https://api.example.com/users | jq -r '.[] | [.id, .email] | @csv' >> users.csv

# Retry until success
until curl -sf http://localhost:8080/health; do sleep 2; done; echo "Service up"

# Quick web server
python3 -m http.server 8000

# Base64
echo -n "secret" | base64
echo "c2VjcmV0" | base64 -d
```

## Reference Files

- `scripts/bash-helpers.sh` -- Reusable shell functions for port checking, JSON conversion, container ops, git cleanup
- `scripts/system-diagnostics.sh` -- Functions for CPU, memory, network, and disk diagnostics
- `references/bash-oneliners.md` -- Categorized one-liners for files, git, network, docker, performance
- `references/advanced-oneliners.md` -- Advanced data processing, system admin, development workflows
- `examples/common-oneliners.json` -- Structured one-liner examples with categories and descriptions
