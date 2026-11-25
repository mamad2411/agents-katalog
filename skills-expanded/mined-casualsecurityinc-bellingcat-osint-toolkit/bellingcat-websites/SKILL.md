---
name: bellingcat-websites
description: >
  Investigate domains, websites, IP addresses, and web infrastructure. WHOIS
  lookups, DNS history, IP geolocation, content archiving, and technology
  fingerprinting. Use when the user mentions a domain name, URL, IP address,
  website, or web infrastructure, even if they don't mention "OSINT."
compatibility: Requires internet access to fetch tool detail pages from bellingcat.gitbook.io
---

# Bellingcat Website Investigation Tools

Tools for investigating domains, websites, and web infrastructure. Covers registration data, DNS records, IP geolocation, content archiving, and technology profiling.

## Choosing Tools

- Use registration and DNS tools for ownership or infrastructure questions, archives for historical content, and scanners for observed web behavior.
- Separate current observations from historical records and corroborate links between domains before attributing ownership.

## Tools

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [Distill.io](https://distill.io/) | A website change monitoring tool that allows users to track changes on web pages. | Partially Free | Distill.io is a website change monitoring tool that allows users to track changes on web pages. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/distill) |
| [DNS History](http://completedns.com/) | Collection of historical DNS information. | Free | Collection of historical DNS information. |  |
| [Domain Research Suite](https://drs.whoisxmlapi.com/) | Tools to obtain registration and ownership data for domain names, along with historica... | Paid | Domain Research Suite provides tools to obtain registration and ownership data for domain names, along with historica... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/domain-research-suite) |
| [DomainTools Whois Lookup](https://whois.domaintools.com/) | DomainTools Whois provides detailed domain name registration information, and can be used… | Partially Free | DomainTools Whois provides detailed domain name registration information, and can be used to investigate details abou... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/domaintools-whois-lookup) |
| [Geo Data Tool](https://www.geodatatool.com/) | IP geolocation service to identify the location and other technical information associated… | Free | IP geolocation service to identify the location and other technical information associated to IP addresses. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/geo-data-tool) |
| [Grep.app](https://grep.app/) | Grep.app is a free web-based search engine that allows users to search the contents of… | Free | grep.app is a free web-based search engine that allows users to search the contents of public GitHub repositories. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/grep.app) |
| [ICANN Lookup](https://lookup.icann.org/) | This tool allows you to search for the current registration data of internet domains. | Free | This tool allows you to search for the current registration data of internet domains. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/icann-lookup) |
| [IDN Checker](https://holdintegrity.com/checker) | Detects visually similar versions of a domain. | Free | IDN Checker detects visually similar versions of a domain. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/idn-checker) |
| [Intelx.io](http://intelx.io/) | Find user details in data breaches | Partially Free | Find user details in data breaches | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/intelx.io) |
| [Wayback Machine](https://web.archive.org/) | The Internet Archive's Wayback Machine lets users view and archive web pages, aiding in… | Free | The Internet Archive's Wayback Machine lets users view and archive web pages, aiding in historical research and digit... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/internet-archive) |
| [Moz Link Explorer](http://moz.com/link-explorer) | Analyse the links of any website. | Free | Analyse the links of any website. |  |
| [PublicWWW](https://publicwww.com/) | A source code search engine that allows you to search for any alphanumeric snippet,… | Partially Free | PublicWWW is a source code search engine that allows you to search for any alphanumeric snippet, signature, or keywor... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/publicwww) |
| [Shodan](https://www.shodan.io/) | A search engine for internet-connected devices, from webcams to databases. | Partially Free | A search engine for internet-connected devices, from webcams to databases. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/shodan) |
| [The Information Laundromat](https://informationlaundromat.com) | A tool for analyzing content replication and site architecture to detect information… | Free | A tool for analyzing content replication and site architecture to detect information laundering. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/the-information-laundromat) |
| [Urlscan.io](https://urlscan.io/) | Urlscan.io is an online tool that allows investigators to analyse, monitor, and document… | Free | urlscan.io is an online tool that allows investigators to analyse, monitor, and document websites in real time. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/urlscan.io) |
| [Web Archives](https://github.com/dessant/web-archives) | A browser extension to view archived and cached versions of a website on multiple… | Partially Free | A browser extension to view archived and cached versions of a website on multiple archiving sites. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/web-archives) |
| [What CMS](https://whatcms.org/) | WhatCMS is a web-based tool for anyone needing information about the technologies behind… | Partially Free | WhatCMS is a web-based tool for anyone needing information about the technologies behind any website, including the c... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/what-cms) |
| [Whoxy](https://www.whoxy.com/) | A domain search engine or whois lookup" tool to find (the history of) registration… | such as the registrar | Whoxy is a domain search engine or whois lookup" tool to find (the history of) registration information on a domain |  |

## Investigation Tips

- Start with WHOIS lookup (ICANN Lookup, DomainTools, Whoxy) to find domain registration details
- Check historical DNS records (DNS History) and archived versions (Wayback Machine)
- Use urlscan.io to analyze a website's behavior, redirects, and connected domains
- Shodan reveals internet-connected devices and services associated with an IP range
- PublicWWW searches HTML/JS/CSS source code across millions of websites
- The Information Laundromat detects content replication patterns and information laundering
