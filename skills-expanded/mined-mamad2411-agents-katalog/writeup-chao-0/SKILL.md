<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-chao-0
description: CTF writeups and security challenges by ChaO-0.
---

# Writeups by ChaO-0

Source repository: `/repos/ChaO-0`

## Repository Index

- WriteUps/README.md
- WriteUps/unity/2020/web/backdoor/assets/vendor/owl.carousel/README.md
- WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/CHANGELOG.md
- WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/ISSUE_TEMPLATE.md
- WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/README.md
- WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/jquery/README.md
- WriteUps/sunshineCTF/Web_Exploitation/WrestlerNameGenerator/README.md
- WriteUps/ifest/2020/web/proxy/README.md
- WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/CHANGELOG.md
- WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/ISSUE_TEMPLATE.md
- WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/README.md
- WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/jquery/README.md
- WriteUps/TAMUCTF/2020/web/too_many_credits_2/README.md
- WriteUps/Hacktoday/PWn/Leakless/README.md
- WriteUps/Hacktoday/PWn/ezrop/README.md
- WriteUps/GKSK/2019/Crypto/WannaPIE/README.md

## Writeup Content


### File: WriteUps/GKSK/2019/Crypto/WannaPIE/README.md

# 1. Executive Summary 

Someone send me WannaPIE and accidentally run the script and encrypted all my data. Now i can't recover my home files but luckly i have stat.info of the encrypted files, and i think it would be usefull for you as an cyber security researcher.

WARNING!
Don't run the script unless you have analyzing it and if you do, be carefull of using it. WannaPIE will encrypt your /home data recursively. If you don't want any harm activity, leave it there and try another challanges. We're not responible for any loss of data. Thankyou :) 

md5sum:
4a255c4d621f37387397f6c20e392a2d MY_DRIVE.zip 
9beb4ca1c4b715d88a2bf0023154c42 wannapie.py 

# 2. Technical Report

Given a python script below

![Python Script](img/1.png)
![Python Script](img/2.png)
![Python Script](img/3.png)

From the script above, i knew that the encryption is using **AES-CBC** and the key is gotten from a random function.
But the random function has a seed in it so it's not actually random. In the script above, the random seed is gotten from the time epoch of change time of the encrypted file, to know the timestamp of an time epoch, i used [online epoch converter](https://epochconverter.com) to find the timestamp.
Oh right, the change time of encrypted file is in **stat.info**

Okay, we got the random seed and now we could find the **key** and **iv** for the **AES-CBC** and decrypt the encrypted file

*remember to use python 3 for the random seed because the encryption is using python 3 for the random seed*

The script that i used to find the **key** and **iv** and decrypting encrypted file is on below
![Python Script](img/4.png)

Run the script and decrypt files, flag is on png file, the flag is looks like this

![Flag](img/realflagpart1.png)
![Flag](img/realflagpart2.png)

# 3. Flag
Flag : GKSK{\_\_i-gave_y0u_th3_PIE_Because__y0u_br1ng_me_th3-correct_seed\_\_}



### File: WriteUps/Hacktoday/PWn/Leakless/README.md

# leaklees
no `view()`, no surrender!


### File: WriteUps/Hacktoday/PWn/ezrop/README.md

# ezrop

key is the new val. yo.

```
nc not.codepwnda.id 30000
```




### File: WriteUps/README.md

# WriteUps
Just a bunch of write ups



### File: WriteUps/TAMUCTF/2020/web/too_many_credits_2/README.md

# SerializationDumper
A tool to dump and rebuild Java serialization streams and Java RMI packet contents in a more human readable form.

The tool does not deserialize the stream (i.e. objects in the stream are not instantiated), so it does not require access to the classes that were used in the stream*.

This tool was developed to support research into Java deserialization vulnerabilities after spending many hours manually decoding raw serialization streams to debug code!

Download v1.11 built and ready to run from here: [https://github.com/NickstaDB/SerializationDumper/releases/download/1.11/SerializationDumper-v1.11.jar](https://github.com/NickstaDB/SerializationDumper/releases/download/1.11/SerializationDumper-v1.11.jar "SerializationDumper-v1.11.jar")

\* See the limitations section below for more details.

**Update 19/12/2018:** SerializationDumper now supports rebuilding serialization streams so you can dump a Java serialization stream to a text file, modify the hex or string values, then convert the text file back into a binary serialization stream. See the section below on [Rebuilding Serialization Streams](#rebuilding-serialization-streams) for an example of this.

## Building
Run `build.sh` or `build.bat` to compile the JAR from the latest sources.

## Usage
SerializationDumper can take input in the form of hex-ascii encoded bytes on the command line, hex-ascii encoded bytes in a file, or a file containing raw serialized data. The following examples demonstrate its use:

    $ java -jar SerializationDumper-v1.1.jar aced0005740004414243447071007e0000
    STREAM_MAGIC - 0xac ed
    STREAM_VERSION - 0x00 05
    Contents
      TC_STRING - 0x74
        newHandle 0x00 7e 00 00
        Length - 4 - 0x00 04
        Value - ABCD - 0x41424344
      TC_NULL - 0x70
      TC_REFERENCE - 0x71
        Handle - 8257536 - 0x00 7e 00 00
    
    $ java -jar SerializationDumper-v1.1.jar -f hex-ascii-input-file.txt
    STREAM_MAGIC - 0xac ed
    STREAM_VERSION - 0x00 05
    Contents
      TC_NULL - 0x70
    
    $ java -jar SerializationDumper-v1.1.jar -r raw-input-file.bin
    STREAM_MAGIC - 0xac ed
    STREAM_VERSION - 0x00 05
    Contents
      TC_CLASSDESC - 0x72
        className
          Length - 11 - 0x00 0b
          Value - com.foo.Bar - 0x636f6d2e666f6f2e426172
        serialVersionUID - 0x01 02 03 04 05 06 07 08
        newHandle 0x00 7e 00 00
        classDescFlags - 0x02 - SC_SERIALIZABLE
        fieldCount - 0 - 0x00 00
        classAnnotations
          TC_ENDBLOCKDATA - 0x78
        superClassDesc
          TC_NULL - 0x70

## Rebuilding Serialization Streams
As of 19/12/2018, SerializationDumper can do the reverse operation and convert a dumped serialization stream back into a raw byte stream. This can be useful for working with raw serialized streams because modifications can be made to the dumped text and be "recompiled" back into a byte stream.

### Example Usage
To demonstrate the use of the stream rebuilding functionality, let's start with a simple serialization stream.

    aced0005740004414243447071007e0000

We can dump this using SerializationDumper, as shown above, to get the following:

    STREAM_MAGIC - 0xac ed
    STREAM_VERSION - 0x00 05
    Contents
      TC_STRING - 0x74
        newHandle 0x00 7e 00 00
        Length - 4 - 0x00 04
        Value - ABCD - 0x41424344
      TC_NULL - 0x70
      TC_REFERENCE - 0x71
        Handle - 8257536 - 0x00 7e 00 00

To modify the string value from `ABCD` to `AAAABBBB` we must update the hex-ascii values for both the string length and the string value as follows:

    STREAM_MAGIC - 0xac ed
    STREAM_VERSION - 0x00 05
    Contents
      TC_STRING - 0x74
        newHandle 0x00 7e 00 00
        Length - 4 - 0x00 08
        Value - ABCD - 0x4141414142424242
      TC_NULL - 0x70
      TC_REFERENCE - 0x71
        Handle - 8257536 - 0x00 7e 00 00

If we save this to the file `dumped.txt` then we can rebuild the stream as follows:

    $ java -jar SerializationDumper-v1.1.jar -b dumped.txt rebuilt.bin

The file `rebuilt.bin` will now contain the raw bytes of the modified serialization stream. If we encode that file as hex-ascii we get the following:

    aced000574000841414141424242427071007e0000

See the limitations section below for stream rebuilding limitations.

## Limitations

###Deserialization/Dump Mode
The tool cannot deserialize all Java serialized data streams and may not be fully compliant with the Java serialization specification. In particular, if the stream contains an *externalContents* element then it cannot be deserialized without using the original class. If you have something that cannot be dumped which does not include an `externalContents` element then please get in touch with some sample data so I can look at producing a fix!

***externalContents:*** If a class implements the interface `java.io.Externalizable` then it can use the `writeExternal` method  to write custom data to the serialization stream. This data can only be parsed by the corresponding `readExternal` method so it is not possible to read the data without access to the original class. Such classes will have the `SC_EXTERNALIZABLE` flag set in the `classDescFlags` field but they will not have the `SC_BLOCKDATA` flag set.

###Serialization/Rebuild Mode
The stream rebuild mode currently only operates on the hex-ascii encoded bytes from the dumped data. For that reason, changing the string "ABCD" to "AAAABBBB" won't have the desired effect of producing the bytes 0x4141414142424242 in the output file. A future update may improve this but for now you'll have to do your hex-ascii encoding of strings manually!

Length fields aren't updated automatically during stream rebuilding. This may be desirable or not, but if you modify a string value in a way that changes the length just be aware that you may also need to modify the length (hex-ascii) field accordingly. The same applies to arrays.

If the stream contains any `TC_REFERENCE` elements and you modify it to remove an element that includes a `newHandle` field then you may break the references in the stream unless you manually update them. Reference handles/IDs are incremental and start at `0x7e0000` so the first `newHandle` field is reference by `0x7e0000`, the second by `0x7e0001`, and so on. If the first element with a `newHandle` field is removed from the stream then any `TC_REFERENCE` elements in the stream must be modified to refer to a handle value one less than what they originally referred to.

## Bug Reports/Improvements
This tool was hacked together on the fly to support my own research but if you find the tool useful and have any bug reports or suggestions please get in touch either here or on Twitter ([@NickstaDB](http://twitter.com/NickstaDB "@NickstaDB on Twitter")).

**Please** include a sample of the data you were trying to dump when submitting bug reports, this makes it far easier for me to debug and work out what the problem is, cheers!



### File: WriteUps/ifest/2020/web/proxy/README.md


<center>
  
![](https://img.shields.io/packagist/dt/Athlon1600/php-proxy-app.svg) ![](https://img.shields.io/github/last-commit/Athlon1600/php-proxy-app.svg) ![](https://img.shields.io/github/license/Athlon1600/php-proxy-app.svg)

</center>


# php-proxy-app

Web Proxy Application built on [**php-proxy library**](https://github.com/Athlon1600/php-proxy) ready to be installed on your server

![alt text](http://i.imgur.com/KrtU5KE.png?1 "This is how PHP-Proxy looks when installed")

## To Do List

As of **March 25**, 2018:

* Plugin for facebook.com  
* Plugin for dailymotion.com
* Better support/documentation for Plugin Development
* Better Javascript support

## Web-Proxy vs Proxy Server

Keep in mind that sites/pages that are too script-heavy or with too many "dynamic parts", may not work with this proxy script.
That is a known limitation of web proxies. For such sites, you should use an actual proxy server to route your browser's HTTP requests through:  

https://www.proxynova.com/proxy-software/


## Installation

Keep in mind that this is a **project** and not a library. Installing this via *require* would do you not good.
A project such as this, should be installed straight into the public directory of your web server.

```bash
composer create-project athlon1600/php-proxy-app:dev-master /var/www/
```

If you do not have composer or trying to host this application on either a **shared hosting**, or a VPS hosting with limited permissions (dreamhost.com), then download a pre-installed version of this app as a ZIP archive from [**www.php-proxy.com**](https://www.php-proxy.com/).

**Direct Link:**  
https://www.php-proxy.com/download/php-proxy.zip

## Keep it up-to-date

Application itself rarely will change, vast majority of changes will be done to its requirement packages like php-proxy. Simply call this command once in a while to make sure your proxy is always using the latest versions.

```
composer update
```

#### config.php

This file will be loaded into the global Config class.

#### /templates/

This should have been named "views", but for historic purposes we keep it named as templates for now.

#### /plugins/

PHP-Proxy provides many of its own native plugins, but users are free to write their own custom plugins, which could then be automatically loaded from this very folder. See /plugins/TestPlugin.php for an example.



### File: WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/README.md

# [Bootstrap](http://getbootstrap.com)

[![Slack](https://bootstrap-slack.herokuapp.com/badge.svg)](https://bootstrap-slack.herokuapp.com)
![Bower version](https://img.shields.io/bower/v/bootstrap.svg)
[![npm version](https://img.shields.io/npm/v/bootstrap.svg)](https://www.npmjs.com/package/bootstrap)
[![Build Status](https://img.shields.io/travis/twbs/bootstrap/master.svg)](https://travis-ci.org/twbs/bootstrap)
[![devDependency Status](https://img.shields.io/david/dev/twbs/bootstrap.svg)](https://david-dm.org/twbs/bootstrap#info=devDependencies)
[![NuGet](https://img.shields.io/nuget/v/bootstrap.svg)](https://www.nuget.org/packages/Bootstrap)
[![Selenium Test Status](https://saucelabs.com/browser-matrix/bootstrap.svg)](https://saucelabs.com/u/bootstrap)

Bootstrap is a sleek, intuitive, and powerful front-end framework for faster and easier web development, created by [Mark Otto](https://twitter.com/mdo) and [Jacob Thornton](https://twitter.com/fat), and maintained by the [core team](https://github.com/orgs/twbs/people) with the massive support and involvement of the community.

To get started, check out <http://getbootstrap.com>!


## Table of contents

* [Quick start](#quick-start)
* [Bugs and feature requests](#bugs-and-feature-requests)
* [Documentation](#documentation)
* [Contributing](#contributing)
* [Community](#community)
* [Versioning](#versioning)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)


## Quick start

Several quick start options are available:

* [Download the latest release](https://github.com/twbs/bootstrap/archive/v3.3.7.zip).
* Clone the repo: `git clone https://github.com/twbs/bootstrap.git`.
* Install with [Bower](http://bower.io): `bower install bootstrap`.
* Install with [npm](https://www.npmjs.com): `npm install bootstrap@3`.
* Install with [Meteor](https://www.meteor.com): `meteor add twbs:bootstrap`.
* Install with [Composer](https://getcomposer.org): `composer require twbs/bootstrap`.

Read the [Getting started page](http://getbootstrap.com/getting-started/) for information on the framework contents, templates and examples, and more.

### What's included

Within the download you'll find the following directories and files, logically grouping common assets and providing both compiled and minified variations. You'll see something like this:

```
bootstrap/
├── css/
│   ├── bootstrap.css
│   ├── bootstrap.css.map
│   ├── bootstrap.min.css
│   ├── bootstrap.min.css.map
│   ├── bootstrap-theme.css
│   ├── bootstrap-theme.css.map
│   ├── bootstrap-theme.min.css
│   └── bootstrap-theme.min.css.map
├── js/
│   ├── bootstrap.js
│   └── bootstrap.min.js
└── fonts/
    ├── glyphicons-halflings-regular.eot
    ├── glyphicons-halflings-regular.svg
    ├── glyphicons-halflings-regular.ttf
    ├── glyphicons-halflings-regular.woff
    └── glyphicons-halflings-regular.woff2
```

We provide compiled CSS and JS (`bootstrap.*`), as well as compiled and minified CSS and JS (`bootstrap.min.*`). CSS [source maps](https://developer.chrome.com/devtools/docs/css-preprocessors) (`bootstrap.*.map`) are available for use with certain browsers' developer tools. Fonts from Glyphicons are included, as is the optional Bootstrap theme.


## Bugs and feature requests

Have a bug or a feature request? Please first read the [issue guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md#using-the-issue-tracker) and search for existing and closed issues. If your problem or idea is not addressed yet, [please open a new issue](https://github.com/twbs/bootstrap/issues/new).

Note that **feature requests must target [Bootstrap v4](https://github.com/twbs/bootstrap/tree/v4-dev),** because Bootstrap v3 is now in maintenance mode and is closed off to new features. This is so that we can focus our efforts on Bootstrap v4.


## Documentation

Bootstrap's documentation, included in this repo in the root directory, is built with [Jekyll](http://jekyllrb.com) and publicly hosted on GitHub Pages at <http://getbootstrap.com>. The docs may also be run locally.

### Running documentation locally

1. If necessary, [install Jekyll](http://jekyllrb.com/docs/installation) and other Ruby dependencies with `bundle install`.
   **Note for Windows users:** Read [this unofficial guide](http://jekyll-windows.juthilo.com/) to get Jekyll up and running without problems.
2. From the root `/bootstrap` directory, run `bundle exec jekyll serve` in the command line.
4. Open `http://localhost:9001` in your browser, and voilà.

Learn more about using Jekyll by reading its [documentation](http://jekyllrb.com/docs/home/).

### Documentation for previous releases

Documentation for v2.3.2 has been made available for the time being at <http://getbootstrap.com/2.3.2/> while folks transition to Bootstrap 3.

[Previous releases](https://github.com/twbs/bootstrap/releases) and their documentation are also available for download.


## Contributing

Please read through our [contributing guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

Moreover, if your pull request contains JavaScript patches or features, you must include [relevant unit tests](https://github.com/twbs/bootstrap/tree/master/js/tests). All HTML and CSS should conform to the [Code Guide](https://github.com/mdo/code-guide), maintained by [Mark Otto](https://github.com/mdo).

**Bootstrap v3 is now closed off to new features.** It has gone into maintenance mode so that we can focus our efforts on [Bootstrap v4](https://github.com/twbs/bootstrap/tree/v4-dev), the future of the framework. Pull requests which add new features (rather than fix bugs) should target [Bootstrap v4 (the `v4-dev` git branch)](https://github.com/twbs/bootstrap/tree/v4-dev) instead.

Editor preferences are available in the [editor config](https://github.com/twbs/bootstrap/blob/master/.editorconfig) for easy use in common text editors. Read more and download plugins at <http://editorconfig.org>.


## Community

Get updates on Bootstrap's development and chat with the project maintainers and community members.

* Follow [@getbootstrap on Twitter](https://twitter.com/getbootstrap).
* Read and subscribe to [The Official Bootstrap Blog](http://blog.getbootstrap.com).
* Join [the official Slack room](https://bootstrap-slack.herokuapp.com).
* Chat with fellow Bootstrappers in IRC. On the `irc.freenode.net` server, in the `##bootstrap` channel.
* Implementation help may be found at Stack Overflow (tagged [`twitter-bootstrap-3`](https://stackoverflow.com/questions/tagged/twitter-bootstrap-3)).
* Developers should use the keyword `bootstrap` on packages which modify or add to the functionality of Bootstrap when distributing through [npm](https://www.npmjs.com/browse/keyword/bootstrap) or similar delivery mechanisms for maximum discoverability.


## Versioning

For transparency into our release cycle and in striving to maintain backward compatibility, Bootstrap is maintained under [the Semantic Versioning guidelines](http://semver.org/). Sometimes we screw up, but we'll adhere to those rules whenever possible.

See [the Releases section of our GitHub project](https://github.com/twbs/bootstrap/releases) for changelogs for each release version of Bootstrap. Release announcement posts on [the official Bootstrap blog](http://blog.getbootstrap.com) contain summaries of the most noteworthy changes made in each release.


## Creators

**Mark Otto**

* <https://twitter.com/mdo>
* <https://github.com/mdo>

**Jacob Thornton**

* <https://twitter.com/fat>
* <https://github.com/fat>


## Copyright and license

Code and documentation copyright 2011-2016 Twitter, Inc. Code released under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE). Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).



### File: WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/jquery/README.md

# jQuery

> jQuery is a fast, small, and feature-rich JavaScript library.

For information on how to get started and how to use jQuery, please see [jQuery's documentation](http://api.jquery.com/).
For source files and issues, please visit the [jQuery repo](https://github.com/jquery/jquery).

If upgrading, please see the [blog post for 3.2.1](https://blog.jquery.com/2017/03/20/jquery-3-2-1-now-available/). This includes notable differences from the previous version and a more readable changelog.

## Including jQuery

Below are some of the most common ways to include jQuery.

### Browser

#### Script tag

```html
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
```

#### Babel

[Babel](http://babeljs.io/) is a next generation JavaScript compiler. One of the features is the ability to use ES6/ES2015 modules now, even though browsers do not yet support this feature natively.

```js
import $ from "jquery";
```

#### Browserify/Webpack

There are several ways to use [Browserify](http://browserify.org/) and [Webpack](https://webpack.github.io/). For more information on using these tools, please refer to the corresponding project's documention. In the script, including jQuery will usually look like this...

```js
var $ = require("jquery");
```

#### AMD (Asynchronous Module Definition)

AMD is a module format built for the browser. For more information, we recommend [require.js' documentation](http://requirejs.org/docs/whyamd.html).

```js
define(["jquery"], function($) {

});
```

### Node

To include jQuery in [Node](nodejs.org), first install with npm.

```sh
npm install jquery
```

For jQuery to work in Node, a window with a document is required. Since no such window exists natively in Node, one can be mocked by tools such as [jsdom](https://github.com/tmpvar/jsdom). This can be useful for testing purposes.

```js
require("jsdom").env("", function(err, window) {
	if (err) {
		console.error(err);
		return;
	}

	var $ = require("jquery")(window);
});
```



### File: WriteUps/sunshineCTF/Web_Exploitation/WrestlerNameGenerator/README.md

# 1.Executive Summary
Even better than the Wu-Tang name generator, legend has it that Hulk Hogan used this app to get his name.

http://ng.sunshinectf.org

# 2.Technical Report
Given a web that looks like below

![web](img/1.png)

It looks like asking for an input, if you input something it will return you to this

![Web](img/2.png)

Something is interesting, look at the **get** input parameter, it looks like encoded as **base 64**. So i started to read the source code and here's the interesting code

![Web](img/3.png)

Looks like our input is using **xml** and encoded **base 64** by the javascript **btoa** function, and the javascript code also encoded our input as **url**.

Hmm.... it's interesting, so our input in plaintext is like this , 
**<?xml version='1.0' encoding='UTF-8'?><input\><firstName\>asd</firstName\><lastName\>asd</lastName\></input\>**.
And the request method is **GET**, so why dont i just encode some **xxe injection** as **base64** and **urlencoded** as an input in the **get** parameter. So i started to try it with a simple **xxe injection**. Here's my payload

![Web](img/4.png)

Then i decoded it as **base 64** and **url encoded** on online tools, and pass that to the **get** parameter, and this happened

![Web](img/5.png)

So i started thinking of listing directories but it can't. Then i started to google everything and i got some interesting **php filter injection**. So here's my modified payload after a research on google

![Web](img/6.png)

Then i encoded my payload as **base 64** and **url encoded** again so i could pass it to the **get** parameter, and here's the interesting thing

![Web](img/7.png)

I got a long **base 64** encoded thing, i think it's the source code of **generate.php**?Let's just encode that

![Web](img/8.png)

Hippie ! i got the source code of **generate.php**, So the PHP code will print the flag if our **REMOTE ADDRESS** is in the **whitelist** and **127.0.0.1** is in the **whitelist**. After i got this information, i immidiately made a new payload. Here's the payload

![Web](img/9.png)

And i used python just to make myself cool, but it will be easier to read. Here's my python code

![Web](img/10.png)

Run the python script

![Web](img/11.png)

# 3.Flag
**sun{1_l0v3_hulk_7h3_3x73rn4l_3n717y_h064n}**


### File: WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/README.md

# [Bootstrap](http://getbootstrap.com)

[![Slack](https://bootstrap-slack.herokuapp.com/badge.svg)](https://bootstrap-slack.herokuapp.com)
![Bower version](https://img.shields.io/bower/v/bootstrap.svg)
[![npm version](https://img.shields.io/npm/v/bootstrap.svg)](https://www.npmjs.com/package/bootstrap)
[![Build Status](https://img.shields.io/travis/twbs/bootstrap/master.svg)](https://travis-ci.org/twbs/bootstrap)
[![devDependency Status](https://img.shields.io/david/dev/twbs/bootstrap.svg)](https://david-dm.org/twbs/bootstrap#info=devDependencies)
[![NuGet](https://img.shields.io/nuget/v/bootstrap.svg)](https://www.nuget.org/packages/Bootstrap)
[![Selenium Test Status](https://saucelabs.com/browser-matrix/bootstrap.svg)](https://saucelabs.com/u/bootstrap)

Bootstrap is a sleek, intuitive, and powerful front-end framework for faster and easier web development, created by [Mark Otto](https://twitter.com/mdo) and [Jacob Thornton](https://twitter.com/fat), and maintained by the [core team](https://github.com/orgs/twbs/people) with the massive support and involvement of the community.

To get started, check out <http://getbootstrap.com>!


## Table of contents

* [Quick start](#quick-start)
* [Bugs and feature requests](#bugs-and-feature-requests)
* [Documentation](#documentation)
* [Contributing](#contributing)
* [Community](#community)
* [Versioning](#versioning)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)


## Quick start

Several quick start options are available:

* [Download the latest release](https://github.com/twbs/bootstrap/archive/v3.3.7.zip).
* Clone the repo: `git clone https://github.com/twbs/bootstrap.git`.
* Install with [Bower](http://bower.io): `bower install bootstrap`.
* Install with [npm](https://www.npmjs.com): `npm install bootstrap@3`.
* Install with [Meteor](https://www.meteor.com): `meteor add twbs:bootstrap`.
* Install with [Composer](https://getcomposer.org): `composer require twbs/bootstrap`.

Read the [Getting started page](http://getbootstrap.com/getting-started/) for information on the framework contents, templates and examples, and more.

### What's included

Within the download you'll find the following directories and files, logically grouping common assets and providing both compiled and minified variations. You'll see something like this:

```
bootstrap/
├── css/
│   ├── bootstrap.css
│   ├── bootstrap.css.map
│   ├── bootstrap.min.css
│   ├── bootstrap.min.css.map
│   ├── bootstrap-theme.css
│   ├── bootstrap-theme.css.map
│   ├── bootstrap-theme.min.css
│   └── bootstrap-theme.min.css.map
├── js/
│   ├── bootstrap.js
│   └── bootstrap.min.js
└── fonts/
    ├── glyphicons-halflings-regular.eot
    ├── glyphicons-halflings-regular.svg
    ├── glyphicons-halflings-regular.ttf
    ├── glyphicons-halflings-regular.woff
    └── glyphicons-halflings-regular.woff2
```

We provide compiled CSS and JS (`bootstrap.*`), as well as compiled and minified CSS and JS (`bootstrap.min.*`). CSS [source maps](https://developer.chrome.com/devtools/docs/css-preprocessors) (`bootstrap.*.map`) are available for use with certain browsers' developer tools. Fonts from Glyphicons are included, as is the optional Bootstrap theme.


## Bugs and feature requests

Have a bug or a feature request? Please first read the [issue guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md#using-the-issue-tracker) and search for existing and closed issues. If your problem or idea is not addressed yet, [please open a new issue](https://github.com/twbs/bootstrap/issues/new).

Note that **feature requests must target [Bootstrap v4](https://github.com/twbs/bootstrap/tree/v4-dev),** because Bootstrap v3 is now in maintenance mode and is closed off to new features. This is so that we can focus our efforts on Bootstrap v4.


## Documentation

Bootstrap's documentation, included in this repo in the root directory, is built with [Jekyll](http://jekyllrb.com) and publicly hosted on GitHub Pages at <http://getbootstrap.com>. The docs may also be run locally.

### Running documentation locally

1. If necessary, [install Jekyll](http://jekyllrb.com/docs/installation) and other Ruby dependencies with `bundle install`.
   **Note for Windows users:** Read [this unofficial guide](http://jekyll-windows.juthilo.com/) to get Jekyll up and running without problems.
2. From the root `/bootstrap` directory, run `bundle exec jekyll serve` in the command line.
4. Open `http://localhost:9001` in your browser, and voilà.

Learn more about using Jekyll by reading its [documentation](http://jekyllrb.com/docs/home/).

### Documentation for previous releases

Documentation for v2.3.2 has been made available for the time being at <http://getbootstrap.com/2.3.2/> while folks transition to Bootstrap 3.

[Previous releases](https://github.com/twbs/bootstrap/releases) and their documentation are also available for download.


## Contributing

Please read through our [contributing guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

Moreover, if your pull request contains JavaScript patches or features, you must include [relevant unit tests](https://github.com/twbs/bootstrap/tree/master/js/tests). All HTML and CSS should conform to the [Code Guide](https://github.com/mdo/code-guide), maintained by [Mark Otto](https://github.com/mdo).

**Bootstrap v3 is now closed off to new features.** It has gone into maintenance mode so that we can focus our efforts on [Bootstrap v4](https://github.com/twbs/bootstrap/tree/v4-dev), the future of the framework. Pull requests which add new features (rather than fix bugs) should target [Bootstrap v4 (the `v4-dev` git branch)](https://github.com/twbs/bootstrap/tree/v4-dev) instead.

Editor preferences are available in the [editor config](https://github.com/twbs/bootstrap/blob/master/.editorconfig) for easy use in common text editors. Read more and download plugins at <http://editorconfig.org>.


## Community

Get updates on Bootstrap's development and chat with the project maintainers and community members.

* Follow [@getbootstrap on Twitter](https://twitter.com/getbootstrap).
* Read and subscribe to [The Official Bootstrap Blog](http://blog.getbootstrap.com).
* Join [the official Slack room](https://bootstrap-slack.herokuapp.com).
* Chat with fellow Bootstrappers in IRC. On the `irc.freenode.net` server, in the `##bootstrap` channel.
* Implementation help may be found at Stack Overflow (tagged [`twitter-bootstrap-3`](https://stackoverflow.com/questions/tagged/twitter-bootstrap-3)).
* Developers should use the keyword `bootstrap` on packages which modify or add to the functionality of Bootstrap when distributing through [npm](https://www.npmjs.com/browse/keyword/bootstrap) or similar delivery mechanisms for maximum discoverability.


## Versioning

For transparency into our release cycle and in striving to maintain backward compatibility, Bootstrap is maintained under [the Semantic Versioning guidelines](http://semver.org/). Sometimes we screw up, but we'll adhere to those rules whenever possible.

See [the Releases section of our GitHub project](https://github.com/twbs/bootstrap/releases) for changelogs for each release version of Bootstrap. Release announcement posts on [the official Bootstrap blog](http://blog.getbootstrap.com) contain summaries of the most noteworthy changes made in each release.


## Creators

**Mark Otto**

* <https://twitter.com/mdo>
* <https://github.com/mdo>

**Jacob Thornton**

* <https://twitter.com/fat>
* <https://github.com/fat>


## Copyright and license

Code and documentation copyright 2011-2016 Twitter, Inc. Code released under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE). Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).



### File: WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/jquery/README.md

# jQuery

> jQuery is a fast, small, and feature-rich JavaScript library.

For information on how to get started and how to use jQuery, please see [jQuery's documentation](http://api.jquery.com/).
For source files and issues, please visit the [jQuery repo](https://github.com/jquery/jquery).

If upgrading, please see the [blog post for 3.2.1](https://blog.jquery.com/2017/03/20/jquery-3-2-1-now-available/). This includes notable differences from the previous version and a more readable changelog.

## Including jQuery

Below are some of the most common ways to include jQuery.

### Browser

#### Script tag

```html
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
```

#### Babel

[Babel](http://babeljs.io/) is a next generation JavaScript compiler. One of the features is the ability to use ES6/ES2015 modules now, even though browsers do not yet support this feature natively.

```js
import $ from "jquery";
```

#### Browserify/Webpack

There are several ways to use [Browserify](http://browserify.org/) and [Webpack](https://webpack.github.io/). For more information on using these tools, please refer to the corresponding project's documention. In the script, including jQuery will usually look like this...

```js
var $ = require("jquery");
```

#### AMD (Asynchronous Module Definition)

AMD is a module format built for the browser. For more information, we recommend [require.js' documentation](http://requirejs.org/docs/whyamd.html).

```js
define(["jquery"], function($) {

});
```

### Node

To include jQuery in [Node](nodejs.org), first install with npm.

```sh
npm install jquery
```

For jQuery to work in Node, a window with a document is required. Since no such window exists natively in Node, one can be mocked by tools such as [jsdom](https://github.com/tmpvar/jsdom). This can be useful for testing purposes.

```js
require("jsdom").env("", function(err, window) {
	if (err) {
		console.error(err);
		return;
	}

	var $ = require("jquery")(window);
});
```



### File: WriteUps/unity/2020/web/backdoor/assets/vendor/owl.carousel/README.md

# Owl Carousel 2

Touch enabled [jQuery](https://jquery.com/) plugin that lets you create a beautiful, responsive carousel slider. **To get started, check out https://owlcarousel2.github.io/OwlCarousel2/.**

**Notice:** The old Owl Carousel site (owlgraphic [dot] com) is no longer in use. Please delete all references to this in bookmarks and your own products' documentation as it's being used for malicious purposes.

## Quick start

### Install

This package can be installed with:

- [npm](https://www.npmjs.com/package/owl.carousel): `npm install --save owl.carousel` or `yarn add owl.carousel jquery`
- [bower](http://bower.io/search/?q=owl.carousel): `bower install --save owl.carousel`

Or download the [latest release](https://github.com/OwlCarousel2/OwlCarousel2/releases).

### Load

#### Webpack

Add jQuery via the "webpack.ProvidePlugin" to your webpack configuration:
    
    const webpack = require('webpack');
    
    //...
    plugins: [
        new webpack.ProvidePlugin({
          $: 'jquery',
          jQuery: 'jquery',
          'window.jQuery': 'jquery'
        }),
    ],
    //...

Load the required stylesheet and JS:

```js
import 'owl.carousel/dist/assets/owl.carousel.css';
import 'owl.carousel';
```

#### Static HTML

Put the required stylesheet at the [top](https://developer.yahoo.com/performance/rules.html#css_top) of your markup:

```html
<link rel="stylesheet" href="/node_modules/owl.carousel/dist/assets/owl.carousel.min.css" />
```

```html
<link rel="stylesheet" href="/bower_components/owl.carousel/dist/assets/owl.carousel.min.css" />
```

**NOTE:** If you want to use the default navigation styles, you will also need to include `owl.theme.default.css`.


Put the script at the [bottom](https://developer.yahoo.com/performance/rules.html#js_bottom) of your markup right after jQuery:

```html
<script src="/node_modules/jquery/dist/jquery.js"></script>
<script src="/node_modules/owl.carousel/dist/owl.carousel.min.js"></script>
```

```html
<script src="/bower_components/jquery/dist/jquery.js"></script>
<script src="/bower_components/owl.carousel/dist/owl.carousel.min.js"></script>
```

### Usage

Wrap your items (`div`, `a`, `img`, `span`, `li` etc.) with a container element (`div`, `ul` etc.). Only the class `owl-carousel` is mandatory to apply proper styles:

```html
<div class="owl-carousel owl-theme">
  <div> Your Content </div>
  <div> Your Content </div>
  <div> Your Content </div>
  <div> Your Content </div>
  <div> Your Content </div>
  <div> Your Content </div>
  <div> Your Content </div>
</div>
```
**NOTE:** The `owl-theme` class is optional, but without it, you will need to style navigation features on your own.


Call the [plugin](https://learn.jquery.com/plugins/) function and your carousel is ready.

```javascript
$(document).ready(function(){
  $('.owl-carousel').owlCarousel();
});
```

## Documentation

The documentation, included in this repo in the root directory, is built with [Assemble](http://assemble.io/) and publicly available at https://owlcarousel2.github.io/OwlCarousel2/. The documentation may also be run locally.

## Building

This package comes with [Grunt](http://gruntjs.com/) and [Bower](http://bower.io/). The following tasks are available:

  * `default` compiles the CSS and JS into `/dist` and builds the doc.
  * `dist` compiles the CSS and JS into `/dist` only.
  * `watch` watches source files and builds them automatically whenever you save.
  * `test` runs [JSHint](http://www.jshint.com/) and [QUnit](http://qunitjs.com/) tests headlessly in [PhantomJS](http://phantomjs.org/).

To define which plugins are build into the distribution just edit `/_config.json` to fit your needs.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap

Please make sure to check out our [Roadmap Discussion](https://github.com/OwlCarousel2/OwlCarousel2/issues/1756).


## License

The code and the documentation are released under the [MIT License](LICENSE).



### File: WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/CHANGELOG.md

Bootstrap uses [GitHub's Releases feature](https://github.com/blog/1547-release-your-software) for its changelogs.

See [the Releases section of our GitHub project](https://github.com/twbs/bootstrap/releases) for changelogs for each release version of Bootstrap.

Release announcement posts on [the official Bootstrap blog](http://blog.getbootstrap.com) contain summaries of the most noteworthy changes made in each release.



### File: WriteUps/ifest/2020/web/weebs_diary_revenge/app/public/bower_components/bootstrap/ISSUE_TEMPLATE.md

Before opening an issue:

- [Search for duplicate or closed issues](https://github.com/twbs/bootstrap/issues?utf8=%E2%9C%93&q=is%3Aissue)
- [Validate](http://validator.w3.org/nu/) and [lint](https://github.com/twbs/bootlint#in-the-browser) any HTML to avoid common problems
- Prepare a [reduced test case](https://css-tricks.com/reduced-test-cases/) for any bugs
- Read the [contributing guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md)

When asking general "how to" questions:

- Please do not open an issue here
- Instead, ask for help on [StackOverflow, IRC, or Slack](https://github.com/twbs/bootstrap/blob/master/README.md#community)

When reporting a bug, include:

- Operating system and version (Windows, Mac OS X, Android, iOS, Win10 Mobile)
- Browser and version (Chrome, Firefox, Safari, IE, MS Edge, Opera 15+, Android Browser)
- Reduced test cases and potential fixes using [JS Bin](https://jsbin.com)

When suggesting a feature, include:

- As much detail as possible for what we should add and why it's important to Bootstrap
- Relevant links to prior art, screenshots, or live demos whenever possible



### File: WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/CHANGELOG.md

Bootstrap uses [GitHub's Releases feature](https://github.com/blog/1547-release-your-software) for its changelogs.

See [the Releases section of our GitHub project](https://github.com/twbs/bootstrap/releases) for changelogs for each release version of Bootstrap.

Release announcement posts on [the official Bootstrap blog](http://blog.getbootstrap.com) contain summaries of the most noteworthy changes made in each release.



### File: WriteUps/unity/2020/final/web/weebs_diary/public/bower_components/bootstrap/ISSUE_TEMPLATE.md

Before opening an issue:

- [Search for duplicate or closed issues](https://github.com/twbs/bootstrap/issues?utf8=%E2%9C%93&q=is%3Aissue)
- [Validate](http://validator.w3.org/nu/) and [lint](https://github.com/twbs/bootlint#in-the-browser) any HTML to avoid common problems
- Prepare a [reduced test case](https://css-tricks.com/reduced-test-cases/) for any bugs
- Read the [contributing guidelines](https://github.com/twbs/bootstrap/blob/master/CONTRIBUTING.md)

When asking general "how to" questions:

- Please do not open an issue here
- Instead, ask for help on [StackOverflow, IRC, or Slack](https://github.com/twbs/bootstrap/blob/master/README.md#community)

When reporting a bug, include:

- Operating system and version (Windows, Mac OS X, Android, iOS, Win10 Mobile)
- Browser and version (Chrome, Firefox, Safari, IE, MS Edge, Opera 15+, Android Browser)
- Reduced test cases and potential fixes using [JS Bin](https://jsbin.com)

When suggesting a feature, include:

- As much detail as possible for what we should add and why it's important to Bootstrap
- Relevant links to prior art, screenshots, or live demos whenever possible

