# vnsh Skill

Securely share files via encrypted, expiring links using the `vnsh` CLI.

This skill allows you to:
1.  Upload a local file to get a secure `vnsh.dev` URL.
2.  Read a `vnsh.dev` URL to decrypt and access its content.

## Usage

The `vnsh` tool has two main modes: uploading and reading.

### 1. Upload a file

To share a file, use the `vnsh` command followed by the file path. The tool will encrypt the file, upload it, and return a secure URL.

**Command:**
```bash
vnsh [options] <file_path>
```

**Example:**
```bash
vnsh /path/to/my/document.pdf
```

**Output:**
```
https://vnsh.dev/s/xxxxxxxxxxxxxxxx
```

#### Options

- `-t, --ttl <hours>`: Set the Time-To-Live (expiry time) for the link in hours. Default is 24 hours, max is 168 (7 days).

**Example with TTL:**
```bash
# Link will expire in 1 hour
vnsh -t 1 /path/to/my/secret.txt
```

### 2. Read (Decrypt) a URL

To access the content of a `vnsh` link, use the `read` command.

**Command:**
```bash
vnsh read <url>
```

**Example:**
```bash
vnsh read https://vnsh.dev/s/xxxxxxxxxxxxxxxx
```

The tool will download, decrypt, and print the content to standard output. For binary files, you may want to redirect the output to a file.

**Example for a binary file:**
```bash
vnsh read https://vnsh.dev/s/yyyyyyyyyyyyyyyy > received_image.png
```
