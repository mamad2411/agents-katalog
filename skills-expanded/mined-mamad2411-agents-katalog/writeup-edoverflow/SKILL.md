<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-edoverflow
description: CTF writeups and security challenges by EdOverflow.
---

# Writeups by EdOverflow

Source repository: `/repos/EdOverflow`

## Repository Index

- bug-bounty-responses/README.md
- bug-bounty-responses/all_responses.md
- bug-bounty-responses/tpls/CSP_uses_unsafe-inline.md
- bug-bounty-responses/tpls/CSRF_with_minimal_security_implications.md
- bug-bounty-responses/tpls/CSV_injection.md
- bug-bounty-responses/tpls/IDN_homograph_attack.md
- bug-bounty-responses/tpls/JavaScript_error.md
- bug-bounty-responses/tpls/SPF_misconfiguration.md
- bug-bounty-responses/tpls/ability_to_create_external_links.md
- bug-bounty-responses/tpls/brute-force_attack.md
- bug-bounty-responses/tpls/clickjacking_on_static_website.md
- bug-bounty-responses/tpls/content_injection.md
- bug-bounty-responses/tpls/cross-site_tracing.md
- bug-bounty-responses/tpls/disclosure_of_robots.txt_file.md
- bug-bounty-responses/tpls/email_spoofing.md
- bug-bounty-responses/tpls/error_message.md
- bug-bounty-responses/tpls/leaking_non-sensitive_information_on_search_engine_results.md
- bug-bounty-responses/tpls/missing_security_headers.md
- bug-bounty-responses/tpls/no_notification_on_event.md
- bug-bounty-responses/tpls/no_proof_of_concept.md
- bug-bounty-responses/tpls/no_rate_limiting.md
- bug-bounty-responses/tpls/non-sensitive_file_disclosure.md
- bug-bounty-responses/tpls/open_redirect_using_Host_header.md
- bug-bounty-responses/tpls/outdated_library.md
- bug-bounty-responses/tpls/reverse_tabnabbing.md
- bug-bounty-responses/tpls/server_version_disclosure.md
- bug-bounty-responses/tpls/specific_HTTP_method_enabled.md
- bug-bounty-responses/tpls/sub-domain_takeover_false_positive.md
- bug-bounty-responses/tpls/target_does_not_belong_to_bug_bounty_program.md
- bug-bounty-responses/tpls/weak_password_policy.md

## Writeup Content


### File: bug-bounty-responses/README.md

# Bug bounty responses

A collection of response templates for invalid bug bounty reports. This project is designed to work well with [@fransr](https://github.com/fransr)'s [*Template generator*](https://github.com/fransr/template-generator).

# Installation & setup process

```
$ git clone https://github.com/fransr/template-generator.git
$ git clone https://github.com/EdOverflow/bug-bounty-responses.git
$ cp -a bug-bounty-responses/tpls/. template-generator/tpls/
$ cd template-generator
$ php -S localhost:8000
```

# Contributing

I welcome contributions from the public.

### Using the issue tracker 💡

The issue tracker is the preferred channel for bug reports and features requests. [![GitHub issues](https://img.shields.io/github/issues/EdOverflow/bug-bounty-responses.svg?style=flat-square)](https://github.com/EdOverflow/bug-bounty-responses/issues)

### Issues and labels 🏷

I use several labels to help organise and identify issues.

### Guidelines for bug reports 🐛

Use the GitHub issue search — check if the issue has already been reported.

# Style Guide

I like to keep the Markdown files as uniform as possible. So if you submit a PR make sure to use this base template:

```
Hi {{username}},

...

{{triager}}
```

# Donations

If you would like to support my work, you can use any of the addresses below:

**Liberapay:** https://liberapay.com/EdOverflow

**Bitcoin:** `1E2fZRNrrkCKPnWpKZAsJzByBoyoBURADN`

**Ethereum:** `0xe98FC23fB4A8762d700c0354979dA5Db6c29Acc3`



### File: bug-bounty-responses/all_responses.md

# Ability to create external links
```
Thank you for reporting a potential issue to us. Currently, we do not plan on changing this behaviour. The ability to create external links is a fundamental part of the web and users are educated to wary of what they click on while browsing.

Keep up the good work and we look forward to more reports from you in the future!
```

# Brute-force attack
```
Thank you very much for your report. We generally do not accept these type of reports. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that brute-force attacks pose.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# Clickjacking on static website
```
Thank you for reporting this to us. The page in question is static, therefore clickjacking does not pose any risk. Clickjacking becomes an issue whenever the page is dynamic and enable a user/attacker to perform sensitive actions such as deleting one's account.

One good way of finding valid clickjacking vulnerabilities is to create a map of the various functionality and then checking the actions that could have a significant impact on the user.

Keep up the good work and we look forward to more reports from you in the future!
```

# Content injection
```
Thank you very much for your report. We generally do not accept content injection reports. The severity of this issue is so low that it does not warrant an immediate fix. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that content injection poses.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# Cross-site tracing
```
In order for Cross-Site Tracing (XST) to really be a significant issue you would need to find an endpoint vulnerable to Cross-site Scripting (XSS). If you do find XSS, please notify us, and we will accept this report.

Keep up the good work and we look forward to seeing what you find in the future!
```

# CSP uses `unsafe-inline`
```
Thank you for submitting a report. The fact that our CSP includes `unsafe-inline` is not an issue in itself. In order for you to demonstrate the actual impact of this value, I highly recommend you look for an XSS vulnerability. Try to trigger `alert(document.domain)`. We will accept this report if you can find a way of actually exploiting this potential issue with XSS.

Keep up the good work and we look forward to seeing what you find in the future!
```

# CSRF with minimal security implications
```
Thank you for reporting this to us. In order for CSRF to be a valid issue it must affect some important action such as deleting one's account. The CSRF that you have reported to us does not affect anything important, therefore we do not believe that this requires an immediate fix.

One good way of finding valid CSRF vulnerabilities is to create a map of the various functionality and then checking the actions that could have a significant impact on the user.

When constructing the proof of concept always make sure the code is clear and well formatted. Something along these lines allows the team to easily verify the impact of the issue:

~~~html
<form action="http://example.com/settings" method="POST">
   
   <!-- Victim's username -->
   <input type="hidden" name="username" value="example"/>

   <!-- Victim's password -->
   <input type="hidden" name="password" value="password1234"/>
	
   <!-- Click this button to perform the action -->   
   <input type="submit" value="Click me"/>

</form>
~~~

Then when designing a real-world example, either hide the form (`style="display:none;"`) and make it auto submit, or design it so that it resembles a component from the target's page.

Good luck and keep up the good work!
```

# CSV injection
```
Thank you for the report. We do not believe that this issue has a sufficient impact on our users. In our view, this is an issue that products such as Excel should take care of. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that CSV injection poses.

Keep up the good work and we look forward to more reports from you in the future!
```

# Disclosure of `robots.txt` file
```
Thank you for reporting this to us. We are aware that in some cases robots.txt files have been known to disclose sensitive information. In our case we have determined that our robots.txt file does not contain any information that poses a potential security risk. That being said, keep up the good work and we look forward to more reports from you in the future!
```

# Email spoofing
```
Thank you for notifying use about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

Keep up the good work and we look forward to more reports from you in the future!
```

# Error message
```
We have determined that the error message does not contain information that poses a potential security risk. We really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of an error message to ensure that it really is a security issue. If you are not very familiar with the error message or the technology being used, a quick Google search can usually help.

Keep up the good work and we look forward to more reports from you in the future!
```

# IDN homograph attack
```
While this is a classis phishing technique, we do not consider IDN homograph attacks to be a significant threat and do not plan on addressing this concern at the moment.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

We look forward to more reports from you in the future!
```

# JavaScript error
```
We appreciate the fact that you took the time to report this to us. The JavaScript error does not disclose any sensitive information, therefore we do not plan on fixing this anytime soon. Always make sure that when you believe you have encountered some form of information disclosure to double-check that the information is in fact sensitive. If you are not very familiar with the error message or the technology being used, a quick Google search can usually help.

Keep up the good work and we look forward to more reports from you in the future!
```

# Leaking non-sensitive information on search engine results
```
The result does not appear to disclose any sensitive information that could potentially affect us or our customers. That being said, we really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of what you find to ensure that it really is a security issue.

Keep up the good work and we look forward to more reports from you in the future!
```

# Missing security headers
```
The missing header in question does not pose a significant risk, therefore we do not plan on addressing this issue at the moment.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# No notification on event
```
We have determined that this event does not require any notifications and that the risk of having no notification is not significant enough to warrant an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Happy hacking and make sure to report back if you find anything interesting.
```

# Non-sensitive file disclosure
```
The file that you listed above does not appear to disclose any sensitive information that could potentially affect us or our customers. That being said, we really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of a file to ensure that it really is a security issue.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# No proof of concept
```
Thank you very much for your report. Would it be possible to provide us with a detailed proof of concept (preferably code) that demonstrates the issue? Unfortunately, without a proof of concept it is very difficult for us to determine what the actual issue is.
```

# No rate limiting
```
Thank you for notifying us about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# Open redirect using `Host` header
```
Thank you for reporting this to us. Open redirects in the `Host` header are not exploitable therefore currently we do not see a reason to change this behaviour. That being, said if you do find a way to really exploit this in a way that could affect us and/or our users, please do report back to us.

Keep up the good work and we look forward to more reports from you in the future!
```

# Outdated library
```
Thank you very much for your report. Would it be possible to provide us a proof of concept (preferably code) that exploits the issue(s) found in this library? We are struggling to determine the severity of this issue and a proof of concept would be a big help.
```

# Reverse tabnabbing
```
Thank you for notifying use about this potential issue. We have accepted the risk that this issue poses, since the attack you described does not affect most modern browsers. Therefore, we do not plan on changing this behaviour at the moment.

Keep up the good work and we look forward to more reports from you in the future!
```

# Server version disclosure
```
Thank you very much for your report. We do not plan on changing this behaviour since we are perfectly happy with disclosing details about what web server we are running.

Keep up the good work and we look forward to more reports from you in the future!
```

# Specific HTTP method enabled
```
We would like to thank you for reporting this potential issue to us. Based on our assessment of your finding, we believe that the severity of this issue does not warrant an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!
```

# SPF misconfiguration
```
Thank you for notifying us about this potential issue. We have accepted the risk that the SPF misconfiguration poses and do not believe that it warrants an immediate fix.

Keep up the good work and we look forward to more reports from you in the future!
```

# Sub-domain takeover false positive
```
Thank you for the report. Unfortunately, this appears to be a false positive. We are currently unable to find a way of claiming this sub-domain. You have our permission to attempt to take over the sub-domain. To verify the issue, simply upload the following proof of concept: https://github.com/EdOverflow/bugbountyguide/blob/master/files/sub-domain_takeover.html. If you are able to find a way, please report back and we will accept your report.

Have fun!
```

# Target does not belong to bug bounty program
```
It appears that you have found a potential issue on an endpoint that does not belong to us. We highly recommend trying to get in touch with {{vendor}}'s security team about your finding. Their security policy can be found here: {{security_page}}.
```

# Weak password policy
```
Thank you for notifying us about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the
future!
```



### File: bug-bounty-responses/tpls/CSP_uses_unsafe-inline.md

Hi {{username}},

Thank you for submitting a report. The fact that our CSP includes `unsafe-inline` is not an issue in itself. In order for you to demonstrate the actual impact of this value, I highly recommend you look for an XSS vulnerability. Try to trigger `alert(document.domain)`. We will accept this report if you can find a way of actually exploiting this potential issue with XSS.

Keep up the good work and we look forward to seeing what you find in the future!

{{triager}}


### File: bug-bounty-responses/tpls/CSRF_with_minimal_security_implications.md

Hi {{username}},

Thank you for reporting this to us. In order for CSRF to be a valid issue it must affect some important action such as deleting one's account. The CSRF that you have reported to us does not affect anything important, therefore we do not believe that this requires an immediate fix.

One good way of finding valid CSRF vulnerabilities is to create a map of the various functionality and then checking the actions that could have a significant impact on the user.

When constructing the proof of concept always make sure the code is clear and well formatted. Something along these lines allows the team to easily verify the impact of the issue:

```
<form action="http://example.com/settings" method="POST">
   
   <!-- Victim's username -->
   <input type="hidden" name="username" value="example"/>

   <!-- Victim's password -->
   <input type="hidden" name="password" value="password1234"/>
	
   <!-- Click this button to perform the action -->   
   <input type="submit" value="Click me"/>

</form>
```

Then when designing a real-world example, either hide the form (`style="display:none;"`) and make it auto submit, or design it so that it resembles a component from the target's page.

Good luck and keep up the good work!

{{triager}}


### File: bug-bounty-responses/tpls/CSV_injection.md

Hi {{username}},

Thank you for the report. We do not believe that this issue has a sufficient impact on our users. In our view, this is an issue that products such as Excel should take care of. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that CSV injection poses.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/IDN_homograph_attack.md

Hi {{username}},

We do not consider IDN homograph attacks to be a significant threat and do not plan on addressing this concern at the moment.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

We look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/JavaScript_error.md

Hi {{username}},

We appreciate the fact that you took the time to report this to us. The JavaScript error does not disclose any sensitive information, therefore we do not plan on fixing this anytime soon. Always make sure that when you believe you have encountered some form of information disclosure to double-check that the information is in fact sensitive. If you are not very familiar with the error message or the technology being used, a quick Google search can usually help.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/SPF_misconfiguration.md

Hi {{username}},

Thank you for notifying us about this potential issue. We have accepted the risk that the SPF misconfiguration poses and do not believe that it warrants an immediate fix.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/ability_to_create_external_links.md

Hi {{username}},

Thank you for reporting a potential issue to us. Currently, we do not plan on changing this behaviour. The ability to create external links is a fundamental part of the web and users are educated to wary of what they click on while browsing.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/brute-force_attack.md

Hi {{username}},

Thank you very much for your report. We generally do not accept these type of reports. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that brute-force attacks pose.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/clickjacking_on_static_website.md

Hi {{username}},

Thank you for reporting this to us. The page in question is static, therefore clickjacking does not pose any risk. Clickjacking becomes an issue whenever the page is dynamic and enable a user/attacker to perform sensitive actions such as deleting one's account.

One good way of finding valid clickjacking vulnerabilities is to create a map of the various functionality and then checking the actions that could have a significant impact on the user.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/content_injection.md

Hi {{username}},

Thank you very much for your report. We generally do not accept content injection reports. The severity of this issue is so low that it does not warrant an immediate fix. We are aware that other bug bounty programs might interpret this issue differently, but we have accepted the low risk that content injection poses.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/cross-site_tracing.md

Hi {{username}},

In order for Cross-Site Tracing (XST) to really be a significant issue you would need to find an endpoint vulnerable to Cross-site Scripting (XSS). If you do find XSS, please notify us, and we will accept this report.

Keep up the good work and we look forward to seeing what you find in the future!

{{triager}}


### File: bug-bounty-responses/tpls/disclosure_of_robots.txt_file.md

Hi {{username}},

Thank you for reporting this to us. We are aware that in some cases robots.txt files have been known to disclose sensitive information. In our case we have determined that our robots.txt file does not contain any information that poses a potential security risk. That being said, keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/email_spoofing.md

Hi {{username}},

Thank you for notifying use about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/error_message.md

Hi {{username}},

We have determined that the error message does not contain information that poses a potential security risk. We really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of an error message to ensure that it really is a security issue. If you are not very familiar with the error message or the technology being used, a quick Google search can usually help.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/leaking_non-sensitive_information_on_search_engine_results.md

Hi {{username}},

The result does not appear to disclose any sensitive information that could potentially affect us or our customers. That being said, we really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of what you find to ensure that it really is a security issue.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/missing_security_headers.md

Hi {{username}},

The missing header in question does not pose a significant risk, therefore we do not plan on addressing this issue at the moment.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/no_notification_on_event.md

Hi {{username}},

We have determined that this event does not require any notifications and that the risk of having no notification is not significant enough to warrant an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Happy hacking and make sure to report back if you find anything interesting.

{{triager}}


### File: bug-bounty-responses/tpls/no_proof_of_concept.md

Hi {{username}},

Thank you very much for your report. Would it be possible to provide us with a detailed proof of concept (preferably code) that demonstrates the issue? Unfortunately, without a proof of concept it is very difficult for us to determine what the actual issue is.

{{triager}}



### File: bug-bounty-responses/tpls/no_rate_limiting.md

Hi {{username}},

Thank you for notifying us about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}



### File: bug-bounty-responses/tpls/non-sensitive_file_disclosure.md

Hi {{username}},

The file that you listed above does not appear to disclose any sensitive information that could potentially affect us or our customers. That being said, we really appreciate you taking the time to report something to us and we highly recommend to always verify the contents of a file to ensure that it really is a security issue.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/open_redirect_using_Host_header.md

Hi {{username}},

Thank you for reporting this to us. Open redirects in the *Host* header are not exploitable therefore currently we do not see a reason to change this behaviour. That being, said if you do find a way to really exploit this in a way that could affect us and/or our users, please do report back to us.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/outdated_library.md

Hi {{username}},

Thank you very much for your report. Would it be possible to provide us a proof of concept (preferably code) that exploits the issue(s) found in this library? We are struggling to determine the severity of this issue and a proof of concept would be a big help.

{{triager}}


### File: bug-bounty-responses/tpls/reverse_tabnabbing.md

Hi {{username}},

Thank you for notifying use about this potential issue. We have accepted the risk that this issue poses, since the attack you described does not affect most modern browsers. Therefore, we do not plan on changing this behaviour at the moment.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/server_version_disclosure.md

Hi {{username}},

Thank you very much for your report. We do not plan on changing this behaviour since we are perfectly happy with disclosing details about what web server we are running.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}



### File: bug-bounty-responses/tpls/specific_HTTP_method_enabled.md

Hi {{username}},

We would like to thank you for reporting this potential issue to us. Based on our assessment of your finding, we believe that the severity of this issue does not warrant an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the future!

{{triager}}


### File: bug-bounty-responses/tpls/sub-domain_takeover_false_positive.md

Hi {{username}},

Thank you for the report. Unfortunately, this appears to be a false positive. We are currently unable to find a way of claiming this sub-domain. You have our permission to attempt to take over the sub-domain. To verify the issue, simply upload the following proof of concept: https://github.com/EdOverflow/bugbountyguide/blob/master/files/sub-domain_takeover.html. If you are able to find a way, please report back and we will accept your report.

Have fun!

{{triager}}


### File: bug-bounty-responses/tpls/target_does_not_belong_to_bug_bounty_program.md

Hi {{username}},

It appears that you have found a potential issue on an endpoint that does not belong to us. We highly recommend trying to get in touch with {{vendor}}'s security team about your finding. Their security policy can be found here: {{security_page}}.

{{triager}}


### File: bug-bounty-responses/tpls/weak_password_policy.md

Hi {{username}},

Thank you for notifying us about this potential issue. We have accepted the risk that this issue poses and do not believe that it warrants an immediate fix.

On a side note, we highly recommend you take a look at _["Web Hacking 101"](https://leanpub.com/web-hacking-101)_ by Peter Yaworski and _["Breaking into Information Security: Learning the Ropes 101"](https://leanpub.com/ltr101-breaking-into-infosec)_ by Andy Gill to get a better idea of the type of issues that we are looking for.

Keep up the good work and we look forward to more reports from you in the
future!

{{triager}}
