<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-4elta
description: CTF writeups and security challenges by 4elta.
---

# Writeups by 4elta

Source repository: `/repos/4elta`

## Repository Index

- report-generator/README.md
- report-generator/src/limitations.md
- report-generator/src/summary.md
- report-generator/src/tools-english.md
- report-generator/src/tools-german.md
- report-generator/src/issues/issue.md
- report-generator/src/issues/issue2.md
- report-generator/src/issues/1 - EXAMPLE/issue.md
- report-generator/res/issues/english/generic vulnerability.md

## Writeup Content


### File: report-generator/README.md

# report generator

Create beautiful pentest reports from Markdown documents.

<a href="out/report.pdf"><img src="res/images/report.png" width="80%"></a>

## motivation

> I really don't like writing reports.
>
> --generic pentester

Have you ever wondered why so many pentesters agree with this?

When a tool constantly gets in the way instead of helping you, even fun tasks can become dreadful.
I'm not saying that writing documentation is everyone's favorite pastime.
But I've noticed that when I have to use this one particular word processor (I don't think I need to name it), my stress level increases with the amount of time I spend using it.
On the other hand, when I use a text editor (there is a difference between "text editor" and "word processor") and Markdown (or some other lightweight markup language), I can happily write for hours.

Using plain text (e.g. Markdown, LaTeX, etc.) as the basis for the final output (i.e. PDF) allows us to use Git itself for collaboration.
Most Git services (e.g. [Gitea](https://gitea.io/en-us/), [GitLab](https://about.gitlab.com/), etc.) provide all the necessary tools for this (e.g. groups, access permissions, comments, etc.).

## requirements

Install Jinja2, TeX Live (full) and Pandoc:

```text
$ sudo apt install python3-jinja2 texlive-full pandoc
```

## usage

1. modify [`project.yaml`](project.yaml)
2. conduct pentest
3. document findings in [`src/issues/`](src/issues/)
   * put screenshots right next to the issue file
   * you can structure a pentest into groups: put the issues into folders
4. add issue templates to [`res/issues/`](res/issues/)
5. adapt `tools-{language}.md`, `limitations.md` and `summary.md`
6. create the PDF report

```text
$ ./report.py -h
usage: report.py [-h] [-o] [-v]

options:
  -h, --help       show this help message and exit
  -o, --overwrite  overwrite the LaTeX document. WARNING: providing this flag causes the output directory
                   ('out/') to be cleared
  -v, --verbose    be very verbose
```

## credits

* [image for the title page](https://www.oldbookillustrations.com/illustrations/microscope/)



### File: report-generator/res/issues/english/generic vulnerability.md

# id

* class b
* aenean

# title

Aenean Gravida Pulvinar Lacus

# description

Nullam gravida urna eget massa sagittis sodales.
Aenean venenatis convallis diam.
Nulla eu nulla eget ligula bibendum placerat in vel nisi.
Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

**Curibatur**

Curabitur quis lectus nisi.
Duis eu auctor nulla.
Etiam non velit quam.
Nunc et lectus sagittis, mattis ligula ut, sodales lectus.
Fusce dignissim nisi non dolor suscipit mattis.
Quisque hendrerit egestas quam.

**Rhoncus**

Aenean rhoncus rhoncus elit.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Integer ac massa non sapien congue hendrerit vel ac augue.
Pellentesque eros mi, sagittis in metus vestibulum, pretium iaculis est.
Ut euismod tortor in quam iaculis tempus.
Vestibulum sed consequat sem. 

# recommendations

* Mauris at nisi finibus velit.
* Sed ut ligula hendrerit orci elementum luctus.
* Fusce dignissim nisi non dolor suscipit mattis.

# references

* [Example Reference](https://example.com/)
* [Another Reference](https://example.com/)



### File: report-generator/src/issues/1 - EXAMPLE/issue.md

# id

* class a
* lorem

# title

Lorem Ipsum Dolor sit Amet

# description

Repellat corporis aut odio veniam non autem vel.
Repudiandae rerum et unde. Accusamus quae et repellat.
Quod deserunt facilis voluptate dignissimos quidem ut iste.
Accusantium sed et maiores deleniti.
Officia eaque ad est amet.

**Blanditiis**

Blanditiis reprehenderit aspernatur aliquam qui.
Ut quisquam et a cupiditate.
Eum quaerat adipisci in cum esse reiciendis laborum.

Possimus facilis aliquid consequatur consequuntur quos perferendis quia.
Magni eveniet quas omnis culpa assumenda doloribus voluptas.
Vero repellat sed vero facere error ducimus et.

**Laudantium**

Qui quia et aut officiis laudantium possimus possimus.
Alias velit cumque sit.
Et hic ipsum dolores et porro voluptatem.
Non sunt quaerat sit cum error dolorem sapiente.

**Omnis**

Dolorem omnis unde itaque sit architecto autem sequi.
Ut nemo ratione fugiat.
Veniam incidunt voluptatum cumque aut.
Rerum est odio cupiditate id esse sed rerum.

# evidence

## vulnerable.example.com

Repellat corporis aut odio veniam non autem vel.
Repudiandae rerum et unde. Accusamus quae et repellat.
Quod deserunt facilis voluptate dignissimos quidem ut iste.

```
$ curl -iks https://vulnerable.example.com/ | grep -i 'server:'
Server: Apache 2.14
```

Ut quisquam et a cupiditate (see Figure !REF:1:EXAMPLE:issue.md:issue.jpg!).

**Severity: critical**
      
## POST api.example.com/v2/resource

Possimus facilis aliquid consequatur consequuntur quos perferendis quia.
Magni eveniet quas omnis culpa assumenda doloribus voluptas.
Vero repellat sed vero facere error ducimus et.

**Severity: low**

# affected assets

* vulnerable.example.com
* api.example.com

# severity

6.4
CVSS:2/AV:N/AC:L/Au:N/C:P/I:P/A:N

# recommendations

* Alias velit cumque sit.
* Ut quisquam et a cupiditate.
* Ut nemo ratione fugiat.

# references

* [Reference A](https://example.com/)
* [Reference B](https://example.com/)
* [Reference C](https://example.com/)

# images

* ![Vero repellat sed vero facere error ducimus et.](issue.jpg)



### File: report-generator/src/issues/issue.md

# id

* class a
* lorem

# title

Lorem Ipsum Dolor sit Amet

# description

Repellat corporis aut odio veniam non autem vel.
Repudiandae rerum et unde. Accusamus quae et repellat.
Quod deserunt facilis voluptate dignissimos quidem ut iste.
Accusantium sed et maiores deleniti.
Officia eaque ad est amet.

**Blanditiis**

Blanditiis reprehenderit aspernatur aliquam qui.
Ut quisquam et a cupiditate.
Eum quaerat adipisci in cum esse reiciendis laborum.

Possimus facilis aliquid consequatur consequuntur quos perferendis quia.
Magni eveniet quas omnis culpa assumenda doloribus voluptas.
Vero repellat sed vero facere error ducimus et.

**Laudantium**

Qui quia et aut officiis laudantium possimus possimus.
Alias velit cumque sit.
Et hic ipsum dolores et porro voluptatem.
Non sunt quaerat sit cum error dolorem sapiente.

**Omnis**

Dolorem omnis unde itaque sit architecto autem sequi.
Ut nemo ratione fugiat.
Veniam incidunt voluptatum cumque aut.
Rerum est odio cupiditate id esse sed rerum.

# evidence

## vulnerable.example.com

Repellat corporis aut odio veniam non autem vel.
Repudiandae rerum et unde. Accusamus quae et repellat.
Quod deserunt facilis voluptate dignissimos quidem ut iste.

```
$ curl -iks https://vulnerable.example.com/ | grep -i 'server:'
Server: Apache 2.14
```

You can link to images: see Figure !REF:issue.md:issue.png!.

**Severity: critical**
      
## POST api.example.com/v2/resource

Possimus facilis aliquid consequatur consequuntur quos perferendis quia.
Magni eveniet quas omnis culpa assumenda doloribus voluptas.
Vero repellat sed vero facere error ducimus et.

You can also link to other issues: see Section !REF:1:EXAMPLE:issue.md!.

**Severity: low**

# affected assets

* vulnerable.example.com
* api.example.com

# severity

9.8 (Critical)
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

# recommendations

* Alias velit cumque sit.
* Ut quisquam et a cupiditate.
* Ut nemo ratione fugiat.

# references

* [Reference A](https://example.com/)
* [Reference B](https://example.com/)
* [Reference C](https://example.com/)

# images

* ![Vero repellat sed vero facere error ducimus et.](issue.png)



### File: report-generator/src/issues/issue2.md

# id

* class b
* aenean

# evidence

## GET api.example.com/v2/resource

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Integer ac massa non sapien congue hendrerit vel ac augue.
Pellentesque eros mi, sagittis in metus vestibulum, pretium iaculis est.

**Severity: medium**

# affected assets

* api.example.com

# severity

6 (medium)
D:M/R:H/E:H/A:L/D:M

# recommendations

* Do something specific, not mentioned in the issue template.

# references

* Some Additional Reference Not Mentioned in the Issue Template



### File: report-generator/src/limitations.md

**Dapibus**

In dapibus est nec elit fermentum, et lacinia ipsum auctor.
Praesent rhoncus, metus a tempor ultricies, ex ligula consequat elit, non sollicitudin massa libero vel odio.
Duis blandit cursus metus.
Quisque ac tincidunt lorem.
Cras laoreet urna sed mi sagittis, et sagittis enim mattis.
Praesent porttitor, dolor sagittis egestas hendrerit, ex neque sagittis sapien, vel tincidunt dui libero et sem.
Fusce a odio faucibus, finibus augue non, aliquam augue.

**Convallis**

Nulla vitae nunc at magna molestie sodales convallis non libero.
Pellentesque nec lectus lacinia, ultricies nulla in, laoreet lectus.
Mauris eget urna efficitur, hendrerit diam eu, gravida mi.
Phasellus porta lacinia ligula, ut dictum mi viverra at.
Nullam dictum eros vitae massa ultrices, ac iaculis ante rhoncus.
Donec pellentesque nec est sed porta.



### File: report-generator/src/summary.md

Quisque ut finibus mauris.
Etiam mattis nisl nulla, eu iaculis urna tincidunt vitae.
Etiam pellentesque metus vel luctus malesuada.
Phasellus auctor scelerisque nisi sed semper.
Aliquam vel molestie nulla, nec lacinia mi.
In a feugiat erat, at laoreet lorem.

Nunc sit amet tristique sem.
Fusce arcu erat, mollis sit amet velit ac, tincidunt porta lorem.
Suspendisse at augue aliquet, sodales tellus et, molestie lorem.
Phasellus id pharetra tellus.
Phasellus vel condimentum justo.
Maecenas sem ligula, tincidunt quis scelerisque quis, ultrices ut quam.



### File: report-generator/src/tools-english.md

* Nmap: network scanner
* cURL: command-line tool for transferring data using various network protocols
* testssl.sh: TLS scanning tool
* Nessus: vulnerability scanner
* Burp Suite: web application security scanner
* Git: collaboration tool
* \LaTeX: document preparation



### File: report-generator/src/tools-german.md

* Nmap: Netzwerk-Scanner
* cURL: Command-Line-Werkzeug zum Daten-Transport über verschiedene Netzwerkprotokolle
* testssl.sh: TLS-Scanner
* Nessus: Schwachstellen-Scanner
* Burp Suite: Web-Applikations-Scanner
* Git: Kollaborationswerkzeug
* \LaTeX: Dokumentenerstellung

