---
name: file_operations
description: Create, read, write, edit, move, copy, and delete files and directories
triggers: [file, create, write, read, delete, rename, copy, move, mkdir, directory, folder, файл, создай файл, папк]
tools: [shell]
platform: all
---

## File operations

Use shell commands for file and directory work.

### Create

Single line:

```
echo "content" > /path/to/file.txt
```

Here-doc:

```
cat > /path/to/file.txt << 'EOF'
Line 1
Line 2
Line 3
EOF
```

Empty file:

```
touch /path/to/file.txt
```

### Read

Whole file:

```
cat /path/to/file.txt
```

First N lines:

```
head -n 10 /path/to/file.txt
```

Last N lines:

```
tail -n 10 /path/to/file.txt
```

### Write / append

Overwrite:

```
echo "new content" > /path/to/file.txt
```

Append:

```
echo "more content" >> /path/to/file.txt
```

### Directories

Create:

```
mkdir -p /path/to/new/directory
```

List:

```
ls -la /path/to/directory
```

### Copy / move / delete

Copy file:

```
cp /source/file.txt /destination/file.txt
```

Copy tree:

```
cp -r /source/dir /destination/dir
```

Move or rename:

```
mv /old/path/file.txt /new/path/file.txt
```

Delete file:

```
rm /path/to/file.txt
```

Delete directory:

```
rm -r /path/to/directory
```

### Find

By name:

```
find /search/path -name "*.txt" -maxdepth 3
```

By content:

```
grep -r "search text" /search/path --include="*.txt"
```

### Rules

1. Use absolute paths or paths relative to the working directory.
2. After creating files, verify with `ls -la`.
3. Use `mkdir -p` for nested directories.
4. Before deleting, confirm with the user what will be removed.
5. Use `cat` for small files; `head`/`tail` for large ones.
6. Prefer `cat << 'EOF'` (single-quoted EOF) to avoid accidental variable expansion.
