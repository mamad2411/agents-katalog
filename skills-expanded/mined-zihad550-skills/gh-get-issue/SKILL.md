---
name: gh-get-issue
displayName: get github issue informations
description: get github issue information by using the provided issue id and the gh cli
version: 1.0.0
tags: [github, issues, management]
---


# Instructions
1. use the `gh` cli to get issue information. eg:
```bash
gh issue view 100 \
  --json author,body,comments,labels,title \
  --template "
Title: {{.title}}
Author: {{.author.login}}
Labels:
{{range .labels}}- {{.name}}
{{end}}
Body:
{{.body}}
Comments:
{{range .comments}}
[{{.author.login}}]: {{.body}}
{{end}}
"
``` 
2. Don't hasitate to ask user information if you are uncertain about something.


# Requirements
1. Only get the issue information. 
2. Ask user what they want to do with it.
