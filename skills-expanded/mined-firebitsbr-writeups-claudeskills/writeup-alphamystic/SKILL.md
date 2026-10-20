<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-alphamystic
description: CTF writeups and security challenges by alphamystic.
---

# Writeups by alphamystic

Source repository: `/repos/alphamystic`

## Repository Index

- wheagle/TODO.md
- wheagle/beacon/README.md
- wheagle/random/README.md
- wheagle/server/static/vendors/tinymce/readme.md
- wheagle/server/static/vendors/iconfonts/flag-icon-css/README.md
- wheagle/server/static/vendors/iconfonts/font-awesome/README.md
- wheagle/server/static/vendors/iconfonts/mdi/README.md
- wheagle/server/static/vendors/iconfonts/mdi/license.md
- wheagle/server/static/vendors/iconfonts/simple-line-icon/CODE_OF_CONDUCT.md
- wheagle/server/static/vendors/iconfonts/simple-line-icon/CONTRIBUTING.md
- wheagle/server/static/vendors/iconfonts/simple-line-icon/History.md
- wheagle/server/static/vendors/iconfonts/simple-line-icon/LICENSE.md
- wheagle/server/static/vendors/iconfonts/simple-line-icon/README.md
- wheagle/server/static/vendors/iconfonts/themify/README.md

## Writeup Content


### File: wheagle/beacon/README.md

# Description fo proto files

## Tasks
This are commands that are assigned to  all agents rather all installed minions:
can be a ransomware,exfill,ddos

## Commands
Are assigned to a particular session or agent



### File: wheagle/random/README.md

# RANDOM STUFF

This package contains various stuff I love to implement or testing on the side for official main implementation



### File: wheagle/server/static/vendors/iconfonts/flag-icon-css/README.md

# flag-icon-css

[![npm version](https://badge.fury.io/js/flag-icon-css.svg)](https://badge.fury.io/js/flag-icon-css)

A collection of all country flags in SVG — plus the CSS for easier integration.
See the [demo](http://lipis.github.io/flag-icon-css/).

## Install

You can either [download](https://github.com/lipis/flag-icon-css/archive/master.zip)
the whole project as is or install it via Bower or NPM:

```bash
$ bower install flag-icon-css
$ npm install flag-icon-css
```

## Usage

For using the flags inline with text add the classes `.flag-icon` and
`.flag-icon-xx` (where `xx` is the
[ISO 3166-1-alpha-2 code](https://www.iso.org/obp/ui/#search/code/)
of a country) to an empty `<span>`. If you want to have a squared version flag
then add the class `flag-icon-squared` as well. Example:

```html
<span class="flag-icon flag-icon-gr"></span>
<span class="flag-icon flag-icon-gr flag-icon-squared"></span>
```

You could also apply this to any element, but in that case you'll have to use the
`flag-icon-background` instead of `flag-icon` and you're set. This will add the
correct background with the following CSS properties:

```css
background-size: contain;
background-position: 50%;
background-repeat: no-repeat;
```

Which means that the flag is just going to appear in the middle of an element, so
you will have to set manually the correct size of 4 by 3 ratio or if it's squared
add also the `flag-icon-squared` class.

## Development

Run the `npm install` to install the dependencies after cloning the project and
you'll be able to:

To watch for changes and live reload if served

```bash
$ grunt
```

To build `*.less` files

```bash
$ grunt build
```

To serve it on `localhost:8000`

```bash
$ grunt connect
```

To have only specific countries in the css file, remove the ones that you don't
need from the
[`flag-icon-list.less`](https://github.com/lipis/flag-icon-css/blob/master/less/flag-icon-list.less)
file and build it again.

## Credits

This project wouldn't exist without the awesome and now deleted collection of
SVG flags by [koppi](https://github.com/koppi).



### File: wheagle/server/static/vendors/iconfonts/font-awesome/README.md

# [Font Awesome v4.7.0](http://fontawesome.io)
### The iconic font and CSS framework

Font Awesome is a full suite of 675 pictographic icons for easy scalable vector graphics on websites,
created and maintained by [Dave Gandy](https://twitter.com/davegandy).
Stay up to date with the latest release and announcements on Twitter:
[@fontawesome](http://twitter.com/fontawesome).

Get started at http://fontawesome.io!

## License
- The Font Awesome font is licensed under the SIL OFL 1.1:
  - http://scripts.sil.org/OFL
- Font Awesome CSS, LESS, and Sass files are licensed under the MIT License:
  - https://opensource.org/licenses/mit-license.html
- The Font Awesome documentation is licensed under the CC BY 3.0 License:
  - http://creativecommons.org/licenses/by/3.0/
- Attribution is no longer required as of Font Awesome 3.0, but much appreciated:
  - `Font Awesome by Dave Gandy - http://fontawesome.io`
- Full details: http://fontawesome.io/license/

## Changelog
- [v4.7.0 GitHub pull request](https://github.com/FortAwesome/Font-Awesome/pull/10012)
- [v4.6.3 GitHub pull request](https://github.com/FortAwesome/Font-Awesome/pull/9189)
- [v4.6.3 GitHub pull request](https://github.com/FortAwesome/Font-Awesome/pull/9189)
- [v4.6.2 GitHub pull request](https://github.com/FortAwesome/Font-Awesome/pull/9117)
- [v4.6.1 GitHub pull request](https://github.com/FortAwesome/Font-Awesome/pull/8962)
- [v4.6.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?q=milestone%3A4.6.0+is%3Aclosed)
- [v4.5.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?q=milestone%3A4.5.0+is%3Aclosed)
- [v4.4.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?q=milestone%3A4.4.0+is%3Aclosed)
- [v4.3.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?q=milestone%3A4.3.0+is%3Aclosed)
- [v4.2.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=12&page=1&state=closed)
- [v4.1.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=6&page=1&state=closed)
- [v4.0.3 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=9&page=1&state=closed)
- [v4.0.2 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=8&page=1&state=closed)
- [v4.0.1 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=7&page=1&state=closed)
- [v4.0.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=2&page=1&state=closed)
- [v3.2.1 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=5&page=1&state=closed)
- [v3.2.0 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=3&page=1&state=closed)
- [v3.1.1 GitHub milestones](https://github.com/FortAwesome/Font-Awesome/issues?milestone=4&page=1&state=closed)
- v3.1.0 - Added 54 icons, icon stacking styles, flipping and rotating icons, removed Sass support
- v3.0.2 - much improved rendering and alignment in IE7
- v3.0.1 - much improved rendering in webkit, various bug fixes
- v3.0.0 - all icons redesigned from scratch, optimized for Bootstrap's 14px default

## Contributing

Please read through our [contributing guidelines](https://github.com/FortAwesome/Font-Awesome/blob/master/CONTRIBUTING.md).
Included are directions for opening issues, coding standards, and notes on development.

## Versioning

Font Awesome will be maintained under the Semantic Versioning guidelines as much as possible. Releases will be numbered
with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions, including new icons, without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes, changes to brand logos, and misc changes bumps the patch

For more information on SemVer, please visit http://semver.org.

## Author
- Email: dave@fontawesome.io
- Twitter: http://twitter.com/davegandy
- GitHub: https://github.com/davegandy

## Component
To include as a [component](https://github.com/componentjs/component), just run

    $ component install FortAwesome/Font-Awesome

Or add

    "FortAwesome/Font-Awesome": "*"

to the `dependencies` in your `component.json`.

## Hacking on Font Awesome

**Before you can build the project**, you must first have the following installed:

- [Ruby](https://www.ruby-lang.org/en/)
- Ruby Development Headers
  - **Ubuntu:** `sudo apt-get install ruby-dev` *(Only if you're __NOT__ using `rbenv` or `rvm`)*
  - **Windows:** [DevKit](http://rubyinstaller.org/)
- [Bundler](http://bundler.io/) (Run `gem install bundler` to install).
- [Node Package Manager (AKA NPM)](https://docs.npmjs.com/getting-started/installing-node)
- [Less](http://lesscss.org/) (Run `npm install -g less` to install).
- [Less Plugin: Clean CSS](https://github.com/less/less-plugin-clean-css) (Run `npm install -g less-plugin-clean-css` to install).

From the root of the repository, install the tools used to develop.

    $ bundle install
    $ npm install

Build the project and documentation:

    $ bundle exec jekyll build

Or serve it on a local server on http://localhost:7998/Font-Awesome/:

    $ bundle exec jekyll -w serve



### File: wheagle/server/static/vendors/iconfonts/mdi/README.md

> *Note:* Please use the main [MaterialDesign](https://github.com/Templarian/MaterialDesign/issues) repo to report issues. This repo is for distribution of the Webfont files only.

# Webfont - Material Design Icons

Webfont distribution for the [Material Design Icons](https://materialdesignicons.com).

```
npm install @mdi/font
bower install mdi
```

## Related Packages

[NPM @MDI Organization](https://npmjs.com/org/mdi)

- JavaScript/Typescript: [MaterialDesign-JS](https://github.com/Templarian/MaterialDesign-JS)
- SVG: [MaterialDesign-SVG](https://github.com/Templarian/MaterialDesign-SVG)

## Learn More

- [MaterialDesignIcons.com](https://materialdesignicons.com)
- https://github.com/Templarian/MaterialDesign



### File: wheagle/server/static/vendors/iconfonts/simple-line-icon/README.md

Simple line icons
====

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/thesabbir/simple-line-icons?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Simple line icons with CSS, SAAS, LESS & Web-fonts files.

Preview & Docs
===
[https://thesabbir.github.io/simple-line-icons](https://thesabbir.github.io/simple-line-icons)


Installation
====
via [cdnjs](http://cdnjs.com/libraries/simple-line-icons)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/simple-line-icons/2.4.1/css/simple-line-icons.css">
```
via [bower](http://bower.io/search/?q=simple-line-icons)

```shell

bower install simple-line-icons --save

```
via [npm](https://www.npmjs.com/package/simple-line-icons)

```shell

npm install simple-line-icons --save

```

Or, you can also clone or [download this repository](https://github.com/thesabbir/simple-line-icons/archive/master.zip) as zip.


If you are a designers you can use [this creative cloud library](http://adobe.ly/2bQ48wl).

Customizing LESS/SASS variables
====

### LESS:

```less
@simple-line-font-path        : "/path/to/font/files";
@simple-line-font-family      : "desired-name-font-family";
@simple-line-icon-prefix      : prefix-;
```

### SASS:

```sass
$simple-line-font-path        : "/path/to/font/files";
$simple-line-font-family      : "desired-name-font-family";
$simple-line-icon-prefix      : "prefix-";
```


Credits
===
[Jamal Jama](https://twitter.com/byjml) for creating this awesome webfont & [Ahmad Firoz](https://twitter.com/firoz_usf) for extending it further.

Contributors
====
[Check Here](https://github.com/thesabbir/simple-line-icons/graphs/contributors)

Contributions
====
Contributions are more then welcome. Keep them coming!
Please make sure you have read our [guide line](/CONTRIBUTING.md).

License
====
You're free to use the web-font in a template/theme intended for sale on marketplaces like Themeforest.

CSS, SCSS & LESS files are under [MIT License](/LICENSE.md).



### File: wheagle/server/static/vendors/iconfonts/themify/README.md

Themify Icons
=============
[![Tips](https://img.shields.io/gratipay/lykmapipo.svg)](https://gratipay.com/lykmapipo/)

[![Support via Gratipay](https://cdn.rawgit.com/gratipay/gratipay-badge/2.3.0/dist/gratipay.svg)](https://gratipay.com/lykmapipo/)

Themify Icons is a complete set of icons for use in web design and apps, consisting of 320+ pixel-perfect, hand-crafted icons that draw inspiration from Apple iOS 7 - available to the public, 100% FREE! You may use or distribute it for any purpose, whether personal or commercial. This icon set is a must have tool for web designers and developers.

All icons can be viewed at [http://themify.me/themify-icons](http://themify.me/themify-icons)

## Install
```sh
$ bower install --save themify-icons
```

## Usage
- Include `themify-icions` into your app `index.html` 
```html
<!doctype html>
<html ng-app="app">
<head>
    <!-- build:css(.) styles/vendor.css -->
    <!-- bower:css -->
    <link rel="stylesheet" href="bower_components/bootstrap/dist/css/bootstrap.css" />
    <link rel="stylesheet" href="bower_components/themify-icons/themify-icons.css" />
    <!-- endbower -->
    <!-- endbuild -->
    ...
</head>
<body>
    ...

</body>
</html>
```

- Add the icon markup in your page
```html
<span class="ti-download"></span>
```

## LICENSE

- Themify Icons font licensed under: [http://scripts.sil.org/OFL](http://scripts.sil.org/OFL)
- Code licensed under: [http://opensource.org/licenses/mit-license.html](http://opensource.org/licenses/mit-license.html)
- All brand icons are copyright/trademarks of their respective owners.


## VERSIONS

Version 1.0.1 (May 27, 2014)
- Added SVG format
- Fixed some icon naming issues
- Added rss icon

Version 1.0.0 (May 16, 2014)
- Initial release


### File: wheagle/TODO.md

## What I need to implement in what oder.

*Funny thing is I have already done all this but porting and I just keep refactoring the whole framework as it's purely a library. Aanyway :), Let's do this.*

0. Create A CLI (admin,operator,soc) and some login functionality for each
1. Finish on all DB Persistence for the server
2. Create a session
3. Create an Implant Generator
4. Create a Session manager
5. Create a Listener and a Handler for each to identify the clients
6. Get the edr data coz you can (you just have to open windows clone this repo and git add. Literary that but I am just so.....)
7. Create a simple UI for both Operator and SOC
8. Build the libraries for the plugins.



### File: wheagle/server/static/vendors/iconfonts/mdi/license.md

Copyright (c) 2014, Austin Andrews (http://materialdesignicons.com/),
with Reserved Font Name Material Design Icons.

Copyright (c) 2014, Google (http://www.google.com/design/)
uses the license at https://github.com/google/material-design-icons/blob/master/LICENSE

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL


-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded, 
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.


### File: wheagle/server/static/vendors/iconfonts/simple-line-icon/CODE_OF_CONDUCT.md

# Contributor Code of Conduct

As contributors and maintainers of this project, we pledge to respect all people who contribute through reporting issues, posting feature requests, updating documentation, submitting pull requests or patches, and other activities.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, age, or religion.

Examples of unacceptable behavior by participants include the use of sexual language or imagery, derogatory comments or personal attacks, trolling, public or private harassment, insults, or other unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct. Project maintainers who do not follow the Code of Conduct may be removed from the project team.

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by opening an issue or contacting one or more of the project maintainers.

This Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org), version 1.0.0, available at [http://contributor-covenant.org/version/1/0/0/](http://contributor-covenant.org/version/1/0/0/)



### File: wheagle/server/static/vendors/iconfonts/simple-line-icon/CONTRIBUTING.md

# Contributing to Simple Line Icons

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to Simple Line Icons. These are just guidelines, not rules, use your best judgment and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to mail@thesabbir.com.

## How Can I Contribute?

 - [Reporting bugs](#reporting-bugs)
 - [Suggestion enhancement](#suggestion-enhancement)
 - [Pull request](#pull-request)
 - [Improving documentations](#documentations)


## Reporting bugs

Bugs are tracked as GitHub issues. Explain the problem and include additional details to help maintainers reproduce the problem.

 - Use a clear and descriptive title for the issue to identify the problem.
 - Describe the exact steps which reproduce the problem.
 - Explain which behavior you expected to see instead and why.
 - For visual problems include screenshots which clearly demonstrates the problem.

Do not forget to mention:

 - Which version of the package are you using.
 - If the issue is related to installation please mention which method or package manager did you use.

## Suggestion Enhancement

Before creating enhancement suggestions, please check out if a proposal already exists.

 - Mention why you this enhancement is useful.
 - You can list some other packages where this enhancement exists.


## Pull Request

Pull requests are always welcome. We love those!

  - Include screenshot/image if you have added or modified new icon.
  - We follow [github flow](https://guides.github.com/introduction/flow/) for our development model.
  - Nice commit messages are always helpful.
  - Reference issues and pull requests liberally.
  - If you changed any one styleheet please make sure it reflects all styles file(LESS, CSS, SCSS).

## Documentations

Documentation is currently generated using `generate.php` file from `gh-pages` brunch.

  - Modify `generate.php`.
  - Run `php generate.php > index.html`.
  - Do not edit `index.html`.
  - Documentation should be up-to-date with master.

  ___

  Unsure where to begin contributing? You can start by looking through these beginner, help-wanted, enhancement labels issues.

  You can [checkout our very cool contributors graph now](https://github.com/thesabbir/simple-line-icons/graphs/contributors).



### File: wheagle/server/static/vendors/iconfonts/simple-line-icon/History.md

2.4.0 / 2016-09-18
==================

  * Add social-steam icon
  * Rename vkontakte to social-vkontakte icon

2.3.3 / 2016-09-17
==================

  * Add event icon, fix #57
  * Add vkontakte icon, fix #56

2.3.2 / 2016-06-13
==================

  * Add exclamation icon, fix #50
  * Use woff2, ttf, woff, svg order.

2.3.1 / 2016-05-04
==================

  * CSS, use woff before ttf
  * CSS, google instead of gplus
  * Gitignore, ignore .files
  * CSS, add organization, update readme
  * Add organization icon, fix #45



### File: wheagle/server/static/vendors/iconfonts/simple-line-icon/LICENSE.md

The MIT License (MIT)
Copyright (c) 2016 Sabbir Ahmed & All Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



### File: wheagle/server/static/vendors/tinymce/readme.md

TinyMCE - JavaScript Library for Rich Text Editing
===================================================

Building TinyMCE
-----------------
Install [Node.js](https://nodejs.org/en/) on your system.
Clone this repository on your system
```
$ git clone https://github.com/tinymce/tinymce.git
```
Open a console and go to the project directory.
```
$ cd tinymce/
```
Install `grunt` command line tool globally.
```
$ npm i -g grunt-cli
```
Install all package dependencies.
```
$ npm install
```
Now, build TinyMCE by using `grunt`.
```
$ grunt
```


Build tasks
------------
`grunt`
Lints, compiles, minifies and creates release packages for TinyMCE. This will produce the production ready packages.

`grunt start`
Starts a webpack-dev-server that compiles the core, themes, plugins and all demos. Go to `localhost:3000` for a list of links to all the demo pages.

`grunt dev`
Runs tsc, webpack and less. This will only produce the bare essentials for a development build and is a lot faster.

`grunt test`
Runs all tests on PhantomJS.

`grunt bedrock-manual`
Runs all tests manually in a browser.

`grunt bedrock-auto:<browser>`
Runs all tests through selenium browsers supported are chrome, firefox, ie, MicrosoftEdge, chrome-headless and phantomjs.

`grunt webpack:core`
Builds the demo js files for the core part of tinymce this is required to get the core demos working.

`grunt webpack:plugins`
Builds the demo js files for the plugins part of tinymce this is required to get the plugins demos working.

`grunt webpack:themes`
Builds the demo js files for the themes part of tinymce this is required to get the themes demos working.

`grunt webpack:<name>-plugin`
Builds the demo js files for the specific plugin.

`grunt webpack:<name>-theme`
Builds the demo js files for the specific theme.

`grunt --help`
Displays the various build tasks.

Bundle themes and plugins into a single file
---------------------------------------------
`grunt bundle --themes=modern --plugins=table,paste`

Minifies the core, adds the modern theme and adds the table and paste plugin into tinymce.min.js.

Contributing to the TinyMCE project
------------------------------------
TinyMCE is an open source software project and we encourage developers to contribute patches and code to be included in the main package of TinyMCE.

__Basic Rules__

* Contributed code will be licensed under the LGPL license but not limited to LGPL
* Copyright notices will be changed to Ephox Corporation, contributors will get credit for their work
* All third party code will be reviewed, tested and possibly modified before being released
* All contributors will have to have signed the Contributor License Agreement

These basic rules ensures that the contributed code remains open source and under the LGPL license.

__How to Contribute to the Code__

The TinyMCE source code is [hosted on Github](https://github.com/tinymce/tinymce). Through Github you can submit pull requests and log new bugs and feature requests.

When you submit a pull request, you will get a notice about signing the __Contributors License Agreement (CLA)__.
You should have a __valid email address on your GitHub account__, and you will be sent a key to verify your identity and digitally sign the agreement.

After you signed your pull request will automatically be ready for review & merge.

__How to Contribute to the Docs__

Docs are hosted on Github in the [tinymce-docs](https://github.com/tinymce/tinymce-docs) repo.

[How to contribute](https://www.tinymce.com/docs/advanced/contributing-docs/) to the docs, including a style guide, can be found on the TinyMCE website.

