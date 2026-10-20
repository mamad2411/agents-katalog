<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dreadlocked
description: CTF writeups and security challenges by dreadlocked.
---

# Writeups by dreadlocked

Source repository: `/repos/dreadlocked`

## Repository Index

- ctf-writeups/midnightsun-ctf/bigspin.md
- ctf-writeups/midnightsun-ctf/cloudb.md
- ctf-writeups/nn8ed/README.md

## Writeup Content


### File: ctf-writeups/nn8ed/README.md

## Tindermon (Web)
This weekend, Navaja Negra 8 CTF started, organized by ka0labs.org. This web challenge has the following statement:

Get the admin password! There is a WAF and it is NodeJS... Easy peasy!
[http://tindermon.ka0labs.org](http://tindermon.ka0labs.org/)

### Intro
This challenge presents us a classic NodeJS + Express app. Source code of index is:
```html
<html>
<-- WebSite Created by the admin pikachu --!>
<title>Welcome to our Pokemon-Tinder!!!!!</title>
<body  style="background: pink">
<center><h1>List of Users Registered in Tindermon</h1>
<br><br><img  src="[/avatar/magikarp](http://tindermon.ka0labs.org/avatar/magikarp)"  height="480"  width="290">
<img  src="[/avatar/bulbasaur](http://tindermon.ka0labs.org/avatar/bulbasaur)"  height="480"  width="290">
<img  src="[/avatar/diglet](http://tindermon.ka0labs.org/avatar/diglet)"  height="480"  width="290">
</center></body>
</html>
```

Two interesting things here:

- The admin username is pikachu
- There's a route /avatar/```username``` which, when visited, redirects us to /img/``ìd``.jpg where id seems to be the user id.

```
GET /avatar/magikarp HTTP/1.0

-> 302 Found, Location: /imgs/1.jpg
```

#### Not that easy, there's a "WAF"
Testing some characters shows us that there's some kind of check for the following chars:
```" ' . (space)```
Why those characters and not others like > or <? Because (not-so-obviously) what they are trying to avoid is a NoSQL Injection, probably on a MongoDB database.

So logic seems to be:

- Express router process the request.
- The controller searchs for the URL parameter, which is everything following /avatar/ to the next "/" and is intended to be a username.
- Looks for the username on MongoDB, if exists, returns a 302 redirection to users image path.

Easy right? We are in front of a NoSQL Injection challenge like many others, but this time we need to figure out how to bypass NodeJS checks.

Well, at first, some tricks come to my mind, such as Orange Tsai's 2017 Black Hat presentation about  NodeJS inconsistency on parsing Full-Width Characters: https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf but it doesn't seems to work on this case.

#### Reading a bit about how JavaScript Unicode decoding standards works.

This article gives us some keys https://mathiasbynens.be/notes/javascript-unicode. As the article says, for backwards compatibility with ES5 and older standards,  unicodes are divided in groups of two, each one of 2 bytes, those are called "surrogate pairs".

So, for example, the emoji 💩 becomes ```\uD83D\uDCA9```. How this split is done? The answer is, again, in the same blog: https://mathiasbynens.be/notes/javascript-encoding
```javascript
H = Math.floor((C - 0x10000) / 0x400) + 0xD800  
L = (C - 0x10000) % 0x400 + 0xDC00
```

Cool, at this point a hint is released, the hint are emojis, it seems clear that we need some Unicode trick to bypass NodeJS checks. But, do not forget, those unicodes needs to make sense for MongoDB, which is the final endpoint of our string.

#### Error, error, error, error, victory!
After a lot of testing and a key of my man X-C3LL, seems that MongoDB is reading the least significant byte of each surrogate pair, well, let's test if this is true using ```"||"1"=="1``` payload,  but remember, we can't just use ```"```, so we need to figure out a unicode which contains 0x22 and 0x7C as their least significant bytes of each surrogate pair.

```ruby
# This receives a string of two characters, and looks for a unicode hex who's surrogate pairs least significant byte, match each character hex representation.
def uni(find)
  for i in 0...0xFFFFF
    h = (((i - 0x10000) / 0x400) + 0xD800).to_i.to_s(16)[-2..-1].to_i(16).chr
    l = ((i - 0x10000) % 0x400 + 0xDC00).to_i.to_s(16)[-2..-1].to_i(16).chr

    if(h == find[0] && l == find[1])
      return URI.encode [i.to_i].pack('U')
    end
  end
end
```
A return without the URI encode for the string ```"|```, the unicode ```\u{1887c}```  when divided in surrogate pairs:
```
H: 0xD822
L: 0xDC7C
```
Their least significant byte's match with ```"```and ```|``` respectively.

So we got some restrictions to bypass using this trick, those restrictions are the characters forbidden by backend controller, a bit of code helps me to create strings based on this trick for the restricted characters:

```ruby
# Takes pairs of characters where a forbidden char is and
# converts it to unicode representation.
def convert_forbidden(string)
  final_string = ""
  skip = false
  for i in 0..string.length-1 do
      if !skip then
        if $waf.include? string[i] then
          res = uni(string[i] + string[i+1])
          final_string += res
          skip = true
        else
          final_string += URI.encode string[i]
        end
      else
        skip = false
      end
  end

  return final_string.gsub("/","%2F").gsub("[","%5B").gsub("]","%5D").gsub("&","%26")
end
```

For the string ```"||"1=="1``` this returns: ```%F0%98%A1%BC%7C%F0%98%A0%B1%F0%98%A0%BD=%F0%98%A0%B1```

Testing on the live application, it works!! ```/avatar/%F0%98%A1%BC%7C%F0%98%A0%B1%F0%98%A0%BD=%F0%98%A0%B1``` returns 1.jpg, the same process but using "1"=="0" instead of "1" =="1" returns us 404.jpg. So we can confirm the injection.

#### Exploiting Blind NoSQL Injection 
Now we need to write a bit more code to exfiltrate data, byte by byte. After some digging and refresh of MongoDB basics, it ended up on this payload:

```pikachu"&&(this.password.match(/^_string_/))=="_string_"||"1"=="0```

This will return true only if the string starts with the _string_ value. Look at the script to get more details if you are unfamiliar with Blind techniques.

#### Run and gimme the flag!
Running the final script starts exfiltrating us the password for the user pikachu, character by character, but we know that flag starts with ```nn8ed{```, so some work is done:
```
Found! nn8ed{T
Found! nn8ed{Th
Found! nn8ed{Thi
... (lot of time)
Found! nn8ed{This.Old.Challenge.With.Unic0de}
```

So there's the flag. Super funny challenge, I learned a lot about how NodeJS 8 works with Unicode and how inconsistencies at encoding treatment can compromise a system. 

Congratz to ka0labs.org for this great challenge!



### File: ctf-writeups/midnightsun-ctf/bigspin.md


## Bigspin (web)

This weekend, my mates of ID-10-T Team and I decided to play the Midnightsun CTF, we had a long time without playing CTFs so it was nice to meet again and solve some challenges.

The Bigspin challenge, from web cathegory, has the following statement:

```
This app got hacked due to admin and uberadmin directories being open. Was just about to wget -r it, but then they fixed it :( Can you help me get the files again?

Service: http://bigspin-01.play.midnightsunctf.se:3123

Author: avlidienbrunn
```

### Intro
First is first, let's see what this application looks like on it's root path:
```
<html>
    What's it gonna be? Are you an 
    <a href="/uberadmin/">uberadmin</a>, 
    an <a href="/admin/">admin</a>, 
    a <a href="/user/">user</a>, 
    or (most likely) just a <a href="/pleb/">pleb</a>?
</html>
```
Ok so we have four kind of "privilege" levels, and probably we need to reach /uberadmin/ path, cool but, How? Trying to just navigate http://bigspin-01.play.midnightsunctf.se:3123/uberadmin/ shows us an Nginx 403 default error, the same occurs with /user, otherwise, /admin shows a 404. How about /pleb?.

/pleb path returns a 200 OK with the HTML body of http://www.example.com/. 

![pleb1](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/bigspin/bigspin_1.png)

Usually, when I face Nginx servers on CTFs and in some real-world cases, I instantly think about Nginx-alias path traversal vulenerabilities, so I tested /pleb../ and.. the server returns 502 Bad Gateway error. 

![pleb2](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/bigspin/bigspin_2.png)

Wait, what? If not vulnerable, it should return 404, if vulnerable it should return 404 or 200, as we are asking for an existing file or path.

### 1/3 beating user level.
Now we have an unexpected behaviour, when the /pleb/ string is present on the path, the server returns the HTML body of example.com, this could be an indicative of ```proxy_pass``` Nginx directive acting as a reverse proxy to www.example.com, but if we add any characters to the end of /pleb, like /plebidiot, the server returns 502, this means that the server is trying to reach www.example.comidiot, as it can't reach that domain, it returns 502.

Well, so now we know that some kind of SSRF can be done here, my man @dj.thd told us, what if you use a dynamically resolver dns server based on level1 subdomain, and ignoring  other low-level subdomains? Like this www.example.com.127.0.0.1.idiots.com -> 127.0.0.1. Great idea, fortunately for us, there's a service that does exactly this, nip.io. 

So, let's see what happens, when we try to reach /pleb.127.0.0.1.nip.io/user/,

![pleb3](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/bigspin/bigspin_3.png)

Ding ding ding!!! Win!!! We reached /users/ folder, with shows us an Index folder where we can see an "nginx.cönf " file. To read it, my man @patatasfritas used double URL encoding, as Nginx is not that friendly when trying to read files with special characters.

The nginx.conf file contained the following directives:
```
 # omited for readability

http {

    # omited for readability

    server {
        listen 80;

        location / {
            root /var/www/html/public;
            try_files $uri $uri/index.html $uri/ =404;
        }

        location /user {
            allow 127.0.0.1;
            deny all;
            autoindex on;
            root /var/www/html/;
        }

        location /admin {
            internal;
            autoindex on;
            alias /var/www/html/admin/;
        }

        location /uberadmin {
            allow 0.13.3.7;
            deny all;
            autoindex on;
            alias /var/www/html/uberadmin/;
        }

        location ~ /pleb([/a-zA-Z0-9.:%]+) {
            proxy_pass   http://example.com$1;
        }

        access_log /dev/stdout;
        error_log /dev/stdout;
    }

}
```

Well, see that? /user path can only be reached on localhost, we aimed that using the location /pleb SSRF, pointing a user controlled domain to 127.0.0.1 using nip.io, a classic SSRF tip.

### 2/3 beating admin level.
Now we need to reach ```/admin```, it's configuration is the same, but this time it has an ```internal``` nginx directive, what means internal? Let's Google a bit:

```
Specifies that a given location can only be used for internal requests. 
For external requests, the client error 404 (Not Found) is returned. Internal requests are the following:

-   requests redirected by the error_page, index, random_index, and try_files directives;
-   requests redirected by the “X-Accel-Redirect” response header field from an upstream server;
-   subrequests formed by the include virtual command of the  ngx_http_ssi_module  module, by the ngx_http_addition_module module directives,
and by auth_request and  mirror directives; requests changed by the rewrite directive.
```

Ok, while reading this snippet of documentation, the ```X-Accel-Redirect``` header shines among so many directives. What if we try to do the same as the previous step, but this time resolving to a user controlled server, which always redirects with ```X-Accel-Redirect```pointing to ```/admin```? We can use nip.io again to do this. 

First, we need to setup a simple python web server and configure it to always redirect, simple. Then, we try to reach /pleb.X.X.X.X.nip.io, if everything works, the admin folder should be returned and...

Ding ding ding!!! Win!!! Another win, now we can reach /admin location.

### 3/3 beating uberadmin level.
This level was easy peasy, as when seeing the Nginx configuration file, it highlights the alias traversal on /admin location, so we just need to configure our python server with ```X-Accel-Redirect: /admin..uberadmin/flag.txt``` and...

![pleb4](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/bigspin/bigspin_4.png)

Win!!! We got the flag.

### Final thoughts
This challenge was really funny, it's curious how sensitive an Nginx configuration file is. Thanks to @HackingPatatas and @dj.thd for solving this challenge with me.

Feel free to ping me if you see any mistake at @_dreadlocked on twitter.



### File: ctf-writeups/midnightsun-ctf/cloudb.md


## Cloudb (web) 8 solves

This weekend, my mates of ID-10-T Team and I decided to play the Midnightsun CTF, we had a long time without playing CTFs so it was nice to meet again and solve some challenges.

The Cloudb challenge, from web cathegory, has the following statement:

```
These guys made a DB in the cloud. Hope it's not a rain cloud...

Service:  [http://cloudb-01.play.midnightsunctf.se](http://cloudb-01.play.midnightsunctf.se/)

Author: avlidienbrunn
```

### Intro
Another cloud challenge, I love them! This challenge is about reaching ```admin``` privileges on a Cloud data storage platform.

![cloud1](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/cloudb/cloudb_1.png)

The platform lets you upload a profile pic by directly posting it to an Amazon AWS S3 bucket. The upload process consists on two different requests:

- A GET to ```/signature``` path, passing an ACL and a HMAC sign as parameters. This request returns a base64 encoded JSON, with an AWS S3 bucket POST policy:

![cloud1](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/cloudb/cloudb_3.png)

The decoded base64:
```json
{
  "expiration": "2019-04-06T14:17:03.000Z",
  "conditions": [
      ["content-length-range", 1, 10000], {"bucket": "cloudb-profilepics"},
      {"acl": "public-read"},
      ["starts-with", "$key", "profilepics/"]
  ]
}
```

- A POST request to the Amazon AWS S3 bucket using the amazon standard for this kind of requests, explained here: https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-post-example.html

![cloud1](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/cloudb/cloudb_4.png)

Seems like first we are creating a policy, then using this policy to POST our profile pic to the S3 bucket.

Our profile pic is saved at ```/profilepics/idiotsctf@idiots.con/ejemplo.jpeg```.

Also, the application lets us request our profile information, at ```/userinfo/idiotsctf@idiots.com/info.json``` endpoint, returning the following JSON:

```json
{
  "admin": false, 
  "profilepic": "/profilepics/idiotsctf@idiots.com/ejemplo.jpeg", 
  "hmac": "427881d9d33e2e619047bbaff90205a6c804524405d3574c8f4dfcabee162788", 
  "name": "idiotsctf", 
  "email": "idiotsctf@idiots.com"
}
```

Hmm... that "admin" flag set to ```false```, seems like we will need to overwrite our ```/userinfo/idiotsctf@idiots.com/info.json``` profile file and set the admin flag to true.

### Understanding a bit how AWS S3 POST Policy works.
Before continuing, it's necesary to understand a bit how AWS S3 policy works. Amazon let developers upload content via POST requests to a S3 bucket. To do this, the developer needs to define a policy parameter for each user upload, this is what the ```GET /signature``` request does. 

That policy controls how much time the client-side has to upload the content, where it's going to be uploaded, the content type, which bucket is allowed etc.

The above JSON policy (on Intro), tells:
- Your POST upload permission ends at ```2019-04-06T14:17:03.000Z```
- You can upload files between 1 and 10000 bytes length.
- You are allowed to upload it to cloudb-profilepics bucket.
- Your ACL will be public-read, so everyone can read the content you upload.
- And the S3 bucket key where you upload the content, must start with ```profilepics/```

### The magic of team work.
Phiber, from int3pids is one of our ID10Ts team colleague, he was the first who started working on this challenge. When I woke up, he had some work done over the challenge as he realized **how to inject characters on the S3 policy** generated by the ```/signature``` controller. 

- First he found the secret key which where used to create the sign on the ```hmac``` parameter. That signed the ```acl``` parameter. The key was ```[object Object]```, literally.
- Second, he was able to inject JSON strings on the ```acl``` parameter. Let's explain it:

A "common" query, could be ```/signature?hmac=<hmac>&acl=public-read```, this returns the above mentioned JSON (on Intro). Now, if we inject some strings, like this: ```/signature?hmac=<hmac>&acl=public-read'} test```, the base64 encoded policy acl looks like this:

``` ... {'acl': 'public-read'}, test ...```


We can inject things on the policy!!!

### Looking for the buckets.
Now we know that we can tamper the policy, we know we need to overwrite ```/userinfo/idiotsctf@idiots.com/info.json``` file to obtain admin privileges, but we don't know the S3 bucket name where the user information is being stored.

**Patatas in action:**
Our team mate @HackingPatatas has an incredible ability to try random things and make it work. He tried ```cloud-users.s3.amazonaws.com``` and it was a valid bucket. So it's highly probable that the ```info.json```file is being stored on that bucket.

### Bypassing policy restrictions.
The policy tells us we can't just query ```cloud-users``` bucket, as the buckets and the keys of the buckets we are allowed to query, are well defined on the policy. We need to figure out how to invalidate those restrictions and add our own.

If we try to POST something like this :
```
POST https://cloudb-users.s3.amazonaws.com/

{
"key":"users/idiotsctf@idiots.com/info.json",
...
}
```

The AWS S3 server will fail as the policy only allows ```cloud-profilepics``` as bucket and ```profilepics/``` as bucket key path.

A way to bypass, at least the ```bucket``` restriction is adding another ```conditions``` JSON block. In JSON if the same key appears many times on the same level, the last is going to be the valid one. In this case, as the ```conditions``` directive appears before the user controlled ```acl``` injectable parameter, we can inject something like this to invalidate the previous conditions:

```
public-read'}], 
'conditions': [
['starts-with', '$key', 'users/'],
{'bucket':'cloudb-users'},
{'acl':'public-read
```

See how we are closing the previous ```condition``` with ```]```, and opening a new one, with the ```cloud-users``` as allowed bucket. This returned the error ```Invalid according to Policy: Policy Condition failed: ["starts-with", "$key", "profilepics/"]```

Hmmm, our ```starts-with``` directive is being overwritted by the original one, which is after our injection point.

### The magic of the patata... again.
We need to find a way to invalidate the second ```starts-with: profilepics/``` directive, we can do this by creating a new JSON block at the end of our injection, like this:

``` (our injection) ... ], 'new-block': [{'acl': 'public-read```, so the second ```starts-with``` is not going to be inside the ```conditions``` block anymore. BUUUUUUT, we just can't declare blocks with  names other than ```conditions``` or ```expiration``` or we get an error like this ```Invalid Policy: Unexpected: 'new-block'```. 

This is terrible, we can only use two directives, the first one, ```conditions```, will overwrite our injected condition again, so we do not win anything, and the second, ```expiration```, only supports a single string as value.

After a bit of try, error, try, error, our team mate @HackingPatatas, made it again. He wrotes on team's chat: 
```
DarkPatatas, [6 abr 2019 15:29:10]:
ostia.. un sec (the hell... wait a second...)

JAJASDJASJASODJASOJDAOSJDAOSJdas (laughts in spanish)

ME MATO (I'll kill myself)

lo tengo (I got it)
```

What? How?

He just fucking tested ```Conditions``` instead of ```conditions```, and Amazon take it as a valid Policy key, but not applying it as a condition for the policy, so we successfully bypassed al the restrictions.

The next step is do the same but this time, uploading an ```info.json``` to /users/idiotsctf@idiots.com/info.json, with the "admin" flag set to ```true```. And...

![cloud1](https://raw.githubusercontent.com/dreadlocked/ctf-writeups/master/images/cloudb/cloudb_final.png)

Ding ding ding!!! We are admin!!! And, of course, now we can go to ```/admin``` endpoint, authenticate and read the flag.

### Final thoughts

What the hell Amazon?

Thanks to all the team, specially @phiber_int3 and @HackingPatatas to help a lot on solving this challenge. It was really funny and challenging!

