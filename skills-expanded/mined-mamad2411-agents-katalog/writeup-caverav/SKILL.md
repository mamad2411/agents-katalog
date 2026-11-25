<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-caverav
description: CTF writeups and security challenges by caverav.
---

# Writeups by caverav

Source repository: `/repos/caverav`

## Repository Index

- auditforge/LICENSE.md
- auditforge/.github/PULL_REQUEST_TEMPLATE.md
- auditforge/backend/README.md
- auditforge/docs/README.md
- auditforge/docs/_sidebar.md
- auditforge/docs/audits.md
- auditforge/docs/data.md
- auditforge/docs/debug.md
- auditforge/docs/docxtemplate.md
- auditforge/docs/installation.md
- auditforge/docs/roles.md
- auditforge/docs/vulnerabilities.md
- auditforge/frontend/README.md
- auditforge/.github/ISSUE_TEMPLATE/bug_report.md
- auditforge/.github/ISSUE_TEMPLATE/feature_request.md

## Writeup Content


### File: auditforge/backend/README.md

# Installation for developpment environnment

*Source code can be modified live and application will automatically reload on changes.*

Build and run Docker containers
```
docker-compose -f ./docker-compose.dev.yml up -d --build
```

Display container logs
```
docker-compose logs -f
```

Stop/Start container
```
docker-compose stop
docker-compose start
```

API is accessible through https://localhost:5252/api


### File: auditforge/docs/README.md

<p align="center">
  <img src="https://auditforge.feriadesoftware.cl/logo.svg" alt="AuditForge Logo" width="200"/>
</p>

<h1 align="center">AuditForge</h1>

<p align="center">
  <a href="https://img.shields.io/github/license/caverav/auditforge">
    <img src="https://img.shields.io/github/license/caverav/auditforge" alt="License">
  </a>
  <a href="https://github.com/caverav/auditforge/actions/workflows/frontend.yml">
    <img src="https://github.com/caverav/auditforge/actions/workflows/frontend.yml/badge.svg" alt="Build Status">
  </a>
  <a href="https://img.shields.io/website-up-down-green-red/https/auditforge.feriadesoftware.cl.svg">
    <img src="https://img.shields.io/website-up-down-green-red/https/auditforge.feriadesoftware.cl.svg" alt="Website Status">
  </a>
</p>

<p align="center">
  AuditForge (PwnDoc fork) is a pentest reporting application making it simple and easy to write your findings and generate a customizable Docx report.  
  The main goal is to have more time to search vulnerabilities and less time to write documentation by mutualizing data like vulnerabilities between users.
</p>

<p align="center">
  <a href="https://auditforge.feriadesoftware.cl">Website</a>
</p>

## Table of Contents
- [Features](#features)
- [Documentation](#documentation)
- [Our Team](#our-team)

## Features

- 🌐 Multiple Language support

![Audit creation](gifs/create_audit.gif)

- 🤖 CWE and CVSS recommendations powered by AI

![Recommendation of CWE and CVSS](gifs/ia.gif)

- 📊 Dashboard generation

![Dashboards](gifs/dashboard.gif)

- 📁 Multiple Data support
- 🎨 Great Customization
  - Manage reusable Audit and Vulnerability Data
  - Create Custom Sections
  - Add custom fields to Vulnerabilities

- 🛠️ Vulnerabilities Management
- 👥 Multi-User reporting
- 📄 Docx and PDF Report Generation

![Report generation](gifs/exportar.gif)

- 📝 Docx Template customization

![Report document](gifs/reporte.gif)

## Documentation

You can find the documentation [here](https://caverav.github.io/auditforge/).

## Activity

<p align="center">
    <img src="https://repobeats.axiom.co/api/embed/9bc253cd7dda10f05535c3c8177f0166f0fd215b.svg" />
</p>

## Contributors

<p align="center">
  <a href="https://github.com/caverav/auditforge/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=caverav/auditforge" />
  </a>
</p>

<p align="center">
  <a href="https://www.buymeacoffee.com/auditforge" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200"/>
  </a>
</p>



### File: auditforge/frontend/README.md

# Frontend AUDITFORGE

### Para levantar (por ahora; proximamente en docker):

- Usar node lts/iron -> v20.x

- Instalar paquetes (solo primera vez):

  `$ npm install`

- Correr 🥵 el front

  `$ npm run dev`

## Documentación relevante

- [React Router](https://reactrouter.com/en/main/start/tutorial) permite gestionar las rutas de la aplicación. **Muy importante**.

- [Hero Icons](https://heroicons.com/) iconos astetik 👍👍👍

- [TailwindUI](https://tailwindui.com/) Hub de componentes prefabricados en tailwindcss.



### File: auditforge/.github/ISSUE_TEMPLATE/bug_report.md

---
name: Bug report
about: Plantilla para bugs
title: "[BUG]"
labels: bug
assignees: ''

---

**Descripción del bug**
Descripción breve del error a grandes rasgos

**Cómo reproducir**
Pasos para reproducir:
1. '...'
2. '....'
3. '....'
4. Ver error

**Comportamiento esperado**


**Screenshots**
Si aplica, agregar screenshots

**Entorno:**
 - OS: [e.g. Arch Linux]
 - Browser [e.g. chrome, firefox]
 - Version [e.g. 22]

**Contexto adicional**
Cualquier otra información adicional aquí



### File: auditforge/.github/ISSUE_TEMPLATE/feature_request.md

---
name: Feature request
about: Idea de feature
title: "[FEAT]"
labels: enhancement
assignees: ''

---

**Está relacionada a un problema? Descríbelo**
Ex. siempre me pasa esto, por lo que sería bueno....

**Describe la solución que te gustaría**
Comunica qué quieres que pase

**Describe alternativas que has considerado**
Has tenido algunas otras ideas de cómo solucionarlo?

**Contexto adicional**
Screenshots o cualquier información relevante aquí



### File: auditforge/.github/PULL_REQUEST_TEMPLATE.md

<!--- Proporciona un resumen general de tus cambios en el título -->

## Descripción

<!--- Describe tus cambios en detalle -->

## Motivación y Contexto

<!--- ¿Por qué es necesario este cambio? ¿Qué problema soluciona? -->
<!--- Si soluciona un ticket abierto, por favor, enlaza el ticket aquí. -->

## ¿Cómo ha sido probado?

<!--- Por favor, describe en detalle cómo probaste tus cambios. -->
<!--- Incluye detalles de tu entorno de prueba, y las pruebas que realizaste para -->
<!--- ver cómo tu cambio afecta otras áreas del código, etc. -->

## Capturas de pantalla (si es apropiado):

## Tipos de cambios

<!--- ¿Qué tipos de cambios introduce tu código? Pon una `x` en todas las casillas que apliquen: -->

- [ ] Bugfix (cambio que no interrumpe el funcionamiento y que soluciona un problema)
- [ ] New feature (cambio que no interrumpe el funcionamiento y que añade funcionalidad)
- [ ] Breaking change (corrección o funcionalidad que podría causar que la funcionalidad existente cambie)

## Lista de verificación:

<!--- Revisa todos los siguientes puntos, y pon una `x` en todas las casillas que apliquen. -->
<!--- Si no estás seguro sobre alguno de estos puntos, no dudes en preguntar. -->

- [ ] Mi código sigue el estilo de código de este proyecto.
- [ ] Mi cambio requiere una modificación en la documentación.
- [ ] He actualizado la documentación en consecuencia.
- [ ] Requiere nuevos tests.



### File: auditforge/LICENSE.md

MIT License

Copyright (c) 2024 Camilo Vera Vidales

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




### File: auditforge/docs/_sidebar.md

- [Installation](installation.md)
- [Data](data.md)
- [Roles](roles.md)
- [Vulnerabilities](vulnerabilities.md)
- [Audits](audits.md)
- [Docx Template](docxtemplate.md)
- [Debug](debug.md)
- [API Documentation](/auditforge/api/ ":ignore API Swagger File")



### File: auditforge/docs/audits.md

# Audits

Audits represent the core of the application.  
To create an Audit, it must have a Language and a Template, so they must be first created in the [Custom Data](/data?id=custom-data) menu.  

Audits can be edited by multiple users. Users that opened the Audit are listed at the bottom of the Sections sidebar and you can see the section they are on.  
If 2 users are editing the same section, the last one to save will be effective so be carefull not to edit the same section at the same time.

🚧 WIP 🚧
<!--| <span style="color:green">You can safely edit</span>  | <span style="color:red">You are stepping on each other toe</span> |-->
<!--|:-----------------------------------------------------:|:-----------------------------------------------------------------:| -->
<!--| ![Multi-User](_images/audit_multiuser_different.png) | ![Multi-User](_images/audit_multiuser_same.png)                  |-->

## General Information

This section is about all information relative to the Audit.

![General Information](_images/audits_general.png)

It's possible to add Collaborators to an Audit, this will give write access to all Collaborators selected.

## Network Scan

This section allows to import Nmap/Nessus Scans (only port scan).

🚧 WIP 🚧
<!--![Network Scan](_images/audits_network.png)-->

Before importing a scan at least one Audit scope must be defined.
Once the scope is created it will appear on Network Scan page.
At this point you may follow these steps: 

1. Import nmap/nessus scan
2. Select all the hosts associated with the scope
3. Click the + symbol to effectively associate hosts with the scope
4. Save

## Findings

### Create

Findings can be added either from saved Vulnerablities or by creating a new one.
![Finding add](_images/finding_add.png)

Findings are ordered by Severity and grouped by Category. There are 3 Tabs in a Finding :

**DEFINITION**

General definition of the vulnerability and custom fields of a specific Category if any.

**PROOFS**

Proof of Concept / Exploitation of the vulnerability.

**DETAILS**

Other details like affected assets, CVSS, etc.

### Actions

Toggle the `Completed` checkbox will mark the finding as done.

![Finding Completed](_images/finding_completed.png)

The ![Propose Creation / Update in Vulnerability Database](_images/finding_update_vuln_button.png) button will request creation of the finding as a Vulnerability if the Title don't exist or request a modification on the existing Vulnerability (based on the Title). It doesn't directly change the Vulnerability, so feel free to use it. The goal is to make it easier to improve the Vulnerability Database.

Saving can be done with the upper right button or by the most acclaimed feature: <kbd>Ctrl</kbd>+<kbd>S</kbd> or <kbd>&#8984;</kbd>+<kbd>S</kbd>

## Custom Sections

Add any Custom Section previously defined in [Custom Data](/data?id=custom-sections).

![Custom Sections](_images/audit_custom_section_add.png)

## Reviews

To be able to use the review process, the feature must first be activated in the settings. A role with the `audits:review` permission should also be added. This new role will be able to review audits and approve them. The roles page gives more details on the permissions of the application. During the whole audit review life cycle, the states, given that the user has enough permissions, can be changed using buttons located on the top left of the audit edit page. 

Once this is done, a reviewer can be added to an audit by the creator or a collaborator. This reviewer will then be able to read the content of the audit. The creator and the collaborators can also mark the audit as ready to be reviewed. This action will change the state of the audit from `EDIT` to `REVIEW`.

![Adding a reviewer](_images/adding_reviewer.png)

<!--![Marking as ready for review](_images/mark_for_review.png)-->

When an audit is in the `REVIEW` state, a reviewer can give his approval of an audit. The minimal number of approvals before an audit is approved is set in the application's settings page. To know who already approved an audit and how far along it is to be approved, it is possible to hover the mouse over the audit state icon. A tooltip will appear, giving you details on the audit's state. 

<!--![Approving an audit](_images/approving_report.png)-->

The tooltip giving information on the audit's current state. Here, two approvals are needed for an audit to be approved. The audit is still in the review phase, even if one person approved it already. 

<!--![Information in the tooltip](_images/audit_state_tooltip.png)-->

Once enough approvals are given for an audit to be approved, the audit passes to the `APPROVED` state. In this state, the report is ready to be downloaded and sent to the client. 

<!--![Audit is now approved](_images/approved_audit.png)-->

The states of the audits can also be seen from the audit list page. 

<!--![Audit list page](_images/audit_list_states.png)-->

🚧 WIP 🚧

The audit edit page, when then review mode is activated, follows the following state machine diagram. Different states show different UI elements. Keep in mind that the Report role here is viewing a report for which he is neither a the creator nor collaborator. Otherwise, on his own reports, his graph would be similar to the Collaborator shown here. Also, the reviewer role, here, has only `audits:review` permission, and not `audits:review-all`. 

![Audit edit view state diagram](_images/edit_state_graph.png)

## Retests

Retests can be created adding a retest template (Data -> Templates), with the following sections on the vulnerability context: 

```
{@retestStatus | convertHTML}

{#retestDescription}
    {@text | convertHTML}
    {#images}
    {%image}
    Image 6 – {caption}
    {/images}
{/retestDescription} 
```

Then, you can press Create retest on an existing Audit, and export a retest document.




### File: auditforge/docs/data.md

# Data

> Auditforge uses different kinds of data to improve and mutualize user experience. This allows to have reusable and customizable information across audits.

![Data](_images/collaborators.png)

## Collaborators

Collaborators are users of the application and can be part of an audit either as the creator or as a collaborative user.

A Collaborator is defined by:

- Username
- Lastname
- Firstname
- Role
- Password

There are 3 different roles:

**user**

- Read/Write on created and collaboration Audits
- Readonly on Vulnerabilities
- Read/Write on _Companies_ and _Clients_ Data

**report**

- Inherit from user role
- \+ Read/Write on all Audits

**admin**

- Read/Write on everything

## Companies

Companies that order an Audit.

A Company is defined by:

- Name
- Logo

## Clients

Specific clients of companies. Generally the point of contact during a mandate.

A Client is defined by:

- Company
- Lastname
- Firstname
- Email
- Function
- Phone
- Cell

## Templates

Templates are Word documents with special tags that are filled with Audit data when generating the report. See [Docx Template](/docxtemplate.md) section.

A Template is defined by:

- Name
- File

## Custom Data

Custom Data represent a way to fully customize Audits and Vulnerabilities. They are editable and their order can be changed to personalize how they will be displayed for users.

!> Values must match this regex: `/^[\p{Letter}\p{Mark}0-9 \[\]'()_-]+$/iu`

### Languages

Auditforge can handle multiple Languages when it comes to Custom Data or Vulnerabilities. It's one of the first things to create before being able to start an Audit.

A Language is defined by:

- Language: the displayed name in the application
- Locale: the value used to identify a language in API calls

> Example
>
> ```
> Language: English   Locale: en
> Language: French    Locale: fr
> ```

### Audit Types

Audit Types represent the nature of an Audit. They can be configured to define default parameters for an Audit.

An Audit Type is defined by:

- Name
- Templates: For each Language a default template can be configured
- Sections: Any Custom Section here will be added when creating an Audit with this Audit Type
- Hidden Sections: Hide built-in sections if not necessary (Network or Findings)

> Example
>
> ```
> Name: Web Application,
> Templates: [English Template, French Template],
> Sections: [Executive Summary, Nessus Scan],
> Hidden Sections: [Network]
> ```

### Vulnerability Types

Vulnerability Types represent the nature of a Vulnerability. They are multilinguale.

A Vulnerability Type is defined by:

- Name

> Example
>
> ```
> English
> ```

    Name: Wireless,
    Name: Mobile Application

French
Name: Réseau Sans Fil
Name: Application Mobile

> ```
>
> ```

### Vulnerability Categories

Vulnerability Categories are used to categorize a Vulnerability.

A Vulnerability Category is defined by:

- Name

> Example
>
> ```
> Name: Nessus Scan
> ```

### Custom Fields

Custom Fields allow to have additionnal Fields in an Audit or a Vulnerability. They are multilingual.

A Custom Field is defined by:

- View: The page on which Custom Fields will be added
  - Audit General
  - Audit Finding: A Vulnerability Category can be selected. If no Category is selected then every Findings will have Custom Fields
  - Audit Section: A specific Section can be selected. If no Section is selected then every Sections will have Custom Fields
  - Vulnerability: A Vulnerability Category can be selected. If no Category is selected then every Vulnerabilities will have Custom Fields
- Component: The Custom Field type to use
  - Checkbox
  - Date
  - Editor
  - Input
  - Radio
  - Select
  - Select Multiple
  - Space (an empty component used for inserting spaces between other components)
- Label: The displayed value in the GUI and lowercase + strip spaces to use in the docx template
- Description: A hint to be displayed under the component
- Size: The width of the field (1 to 12)
- Offset: The offset from which to start displaying the field (1 to 12)
- Required: The field is required and must not be empty
- Options: Used for multiple selection fields (multiple languages supported)

Each field can have a default value for each existing language.

> Example
>
> ```
> View: Audit Section
> Selected Section: Executive Summary
> Component: Editor
> Label: Text
> Size: 12
> Required: True
>
> -> This will display an additional HTML editor «Text» field in Executive Summary Sections
>
> View: Vulnerability
> Selected Category: None
> Component: Input
> Label: Id
> Size: 2
>
> -> This will display an additional input «Id» field in vulnerabilities that will also be displayed in findings
> ```

### Custom Sections

Custom Sections allow to have additionnal Sections in an Audit.

A Section is defined by:

- Name
- Name
- Field: Used in docx template
- Icon: material, mdi and font awesome are supported

> Example
>
> ```
> Name: Cleanup
> Field: cleanup
> Icon: mdi-broom
> ```



### File: auditforge/docs/debug.md

# Debug

## NoSQL Database

Attach a shell to the running mongoDB container:

```
docker exec -it mongo-auditforge /bin/sh
```

Then connect to the database:

```
mongo mongodb://127.0.0.1/auditforge
```

To list collections as described in [Data](data) you can use one of the following
commands from the DB shell:

- `show collections`
- `db.getCollectionNames()`
- `show tables`

For example:

```
> show collections
audits
audittypes
clients
companies
customfields
customsections
images
languages
templates
users
vulnerabilities
vulnerabilitycategories
vulnerabilitytypes
```

Then you can inspect the entries of each collection:

```
> db.<collection>.find()
```

Example for `users`:

```
> db.users.find()
{ "_id" : ObjectId("REDACTED"), "role" : "admin", "username" : "demo", "password" : "REDACTED", "firstname" : "demo", "lastname" : "demo", "createdAt" : ISODate("2020-08-21T15:45:18.999Z"), "updatedAt" : ISODate("2020-09-21T14:45:18.999Z"), "__v" : 0 }
...
```

You can access a specific entry using an array index, eg for a specific audit:

```
> db.audits.find()[1]
```

Of course you can continue to nest attributes/nodes, eg:

```
> db.audits.find()[1].findings[0].references[0]
```

Then you can use [db.collection.find](https://docs.mongodb.com/manual/reference/method/db.collection.find/) shell method
to query specific objects:

```
> db.users.find( { username: "demo" } )
```

It is possible to [filter the output](https://docs.mongodb.com/compass/current/query/project/):

```
> db.users.find( { role: "admin" }, {_id: 1} )
```

For example to get a synthetic view of custom fields:

```
> db.customfields.find( {}, {_id: 0, updatedAt: 0, size: 0, position: 0, createdAt: 0, __v: 0, offset: 0})
> db.customfields.find( {}, {label: 1, fieldType: 1, description: 1, display: 1, displaySub: 1, required: 1, _id: 0})
{ "displaySub" : "", "required" : true, "description" : "", "fieldType" : "input", "label" : "VulnID", "display" : "vulnerability" }
{ "displaySub" : "Orga", "required" : true, "description" : "", "fieldType" : "input", "label" : "RefID", "display" : "vulnerability" }
```



### File: auditforge/docs/docxtemplate.md

# Docx Template

Auditforge uses the nodejs library docxtemplater to generate a docx report. Specific documentation can be found on the official site documentation: https://docxtemplater.readthedocs.io/en/v3.1.0/tag_types.html

Check the [Default Template](https://github.com/caverav/auditforge/tree/master/backend/report-templates) for better understanding.

## Different Tags

There can be different tags depending on the value. In the following examples `data` is the object passed to the docxtemplater engine.

### Value

```
data = {key1: value1, key2: value2, key3: value3}
-> {key1} {key2} {key3}
```

### Array

```
// Simple Array
data = { array: ['value1', 'value2', 'value3'] }
-> {#array}{.}{/array}

// Array of objects
data = { array: [{name: 'value1'}, {name: 'value2'}, {name: 'value3'}]}
-> {#array}{name}{/array}
```

### Condition

```
data = {findings: [{title: 'vuln1', cvssSeverity: 'Critical'}, {title: 'vuln2', cvssSeverity: 'High'}, {title: 'vuln3', cvssSeverity: 'Medium'}]}
-> // List Vulnerabilities with cvssSeverity Critical
{#findings}
{#cvssSeverity == 'Critical'}
{title} : {cvssSeverity}
{/cvssSeverity == 'Critical'}
{/findings}
```

### HTML values (from text editors)

There is a tag filter _convertHTML_ that convert HTML to open office XML for direct use in the docx template.
To handle images, HTML values with images are converted into an array of text and images

```
// HTML without images (eg: affected scope in finding)
-> {@affected | convertHTML} // this must be the only thing in the paragraph

// HTML with images (eg: poc in a finding)
->
{-w:p poc}{@text | convertHTML}
                                            {-w:p images}{%image}
                                    Image 1 - {caption}{/images}{/poc}
```

## Audit Object

Docxtemplater requires an object containing data that will be used in the template document.

### name

Name of the audit

> Use in template document: `{name}`

### auditType

Type of the audit. See [Custom Data](/data?id=audit-types)

> Use in template document: `{auditType}`

### date

Redacting date

> Use in template document: `{date}`

### date_start

Start date of the test

> Use in template document: `{date_start}`

### date_end

End date of the test

> Use in template document: `{date_end}`

### language

Locale of Audit. [Custom Data](/data?id=languages)

> Use in template document
>
> ```
> // Example with conditional tag
> {#language == 'en'}English{/language == 'en'}
> ```

### company

Object containing:

- **company.name**
- **company.logo** (max width 400px)
- **company.logo_small** (height 37px)

> Use in template document
>
> ```
> {company.name}
> // Image tags must be the only thing in the paragraph
> {%company.logo} // OK
> Image: {%company.logo} // NOT OK
> ```

### client

Object containing:

- **client.email**
- **client.firstname**
- **client.lastname**
- **client.phone**
- **client.cell**
- **client.title**

> Use in template document
>
> ```
> Email: {client.email}
> Name: {client.firstname} {client.lastname}
> ```

### collaborators

Array of Objects:

- **collaborators[i].username**
- **collaborators[i].firstname**
- **collaborators[i].lastname**
- **collaborators[i].role**

> Use in template document
>
> ```
> List of collaborators:
> {#collaborators}
> Name: {firstname} {lastname}
> {/collaborators}
> ```

### creator

Object:

- **creator.username**
- **creator.firstname**
- **creator.lastname**
- **creator.role**

> Use in template document
>
> ```
> Creator: {creator.firstname} {creator.lastname}
> ```

### scope

Array of Objects:

- **scope[i].name**
- **scope[i].hosts**

> Use in template document
>
> ```
> Audit Scope:
> {-w:p scope}{name}{/scope}
>
> Network Scan:
> {#scope}{#hosts}
> {hostname} {ip} {os} :
> {#services}
> {port} {protocol} {name} {product} {version}
> {/services}
> {/hosts}{/scope}
> ```

### findings

List of findings. Array of Objects:

- **findings[i].title**
- **findings[i].vulnType**
- **findings[i].description** (HTML with images)
- **findings[i].observation** (HTML with images)
- **findings[i].remediation** (HTML with images)
- **findings[i].remediationComplexity** (Number 1-3)
- **findings[i].priority** (Number 1-4)
- **findings[i].references** (Array of String)
- **findings[i].cvssv3**
- **findings[i].cvssScore**
- **findings[i].cvssSeverity**
- **findings[i].cvssObj** (Object of cvss Criterias)
- **findings[i].poc** (HTML with images)
- **findings[i].affected** (HTML without images)
- **findings[i].status** (Number 0:done, 1:redacting)
- **findings[i].category**
- **findings[i].identifier**

#### Retest case

- **findings[i].retestStatus** (one of: `[ ok, ko, partial, unknown ]`)
- **findings[i].retestDescription** (HTML with images)

Identifier consists on a sequential id for the reported vulnerability pre-pended with 'IDX-'. Ex: IDX-001.
You can replace the prefix by using the filter `changeID`

Additional fields will also be added to the findings Array. The key will be lowercase + strip sapces of the label.
Eg. if Custom Field label is `Aggravating Factors` it will be added to the array as `findings[i].aggravatingfactors`.

> Use in template document
>
> ```
> List of Findings{#findings}
> {identifier | changeID: 'PROJ1-'}    {title}    {vulnType}
>
> Severity: {cvssSeverity}    Score: {cvssScore}
> Attack Vector: cvssObj.AV               Scope: cvssObj.S
> Attack Complexity: cvssObj.AC           Confidentiality: cvssObj.C
> Required Privileges: cvssObj.PR         Integrity: cvssObj.I
> User Interaction: cvssObj.UI            Availability: cvssObj.A
>
> Affected Scope
> {@affected | convertHTML}
>
> Description
> {-w:p description}{@text | convertHTML}
> ```

                                            {-w:p images}{%image}
                                    Image 1 - {caption}{/images}{/description}

{/findings}

> ```
>
> ```

### Custom Sections

Additional Sections can be added to an Audit. They are accessible in the docx template with the specific Field defined in [Custom Sections](/data?id=custom-sections)

> Use in template document
>
> ```
> // Example with a Cleanup Section: {name: 'Cleanup', field: 'cleanup', text: 'Default text for Cleanup Section'}
> CLEANUP SECTION (or use {cleanup.name} as title)
> {-w:p cleanup.text}{@text | convertHTML}
> ```

                                            {-w:p images}{%image}
                                    Image 1 - {caption}{/images}{/cleanup.text}

> ```
>
> ```

## Styles

Styles for simple text can be defined and applied directly in the Docx Template.

But in order to apply styles to the data from HTML editors, they must be defined in the Docx Template according to this :

| HTML Style |  Docx Style   |
| :--------: | :-----------: |
| paragraph  | HTMLTextStyle |
|     H1     |   Heading1    |
|     H2     |   Heading2    |
|     H3     |   Heading3    |
|     H4     |   Heading4    |
|     H5     |   Heading5    |
|     H6     |   Heading6    |
| code (<>)  |   CodeChar    |
| code block |     Code      |

For `bullet list` and `ordered list` they must be correctly set in the _numbering.xml_ file of the Docx Template.

Open the file with an archive manager

![Docx Archive](_images/docx_archive.png)

The _numbering.xml_ file contains definitions of numbering lists.
`<w:abstractNum w:abstractNumId=0>...</w:abstractNum>` tags represent the definition of a numbering with its different levels.
`<w:num w:numId="1"><w:abstractNumId w:val="0" /></w:num>` tags associate the effective `Id` used in the document with the `abstract Id` of the definition.

Auditforge uses `numId="1"` for `bullet list` and `numId="2"` for `ordered list`. So the only thing to change in the file is the value of the abstractNumId associated with those numId.

If there is no abstractNum definitions, this means that no numbering has been used in the document: open the document with Word, add bullet and ordered list, save, delete bullet and ordered list, save.
There should now be abstractNum definition for each one.

## Filters

Filters allow to apply functions on Audit data values.

### bookmarkCreate

Creates a text block or a location bookmark:

- _Text block bookmarks_ contain some text which can then be referenced in a clickable reference field using the `bookmarkRef` filter.
  These bookmarks can also be used as a hyperlink target using the `bookmarkLink` filter.
- _Location bookmark_ simply allow to point to a location within the document which cas be used as a hyperlink target using the `bookmarkLink` filter.

Bookmark identifiers need to begin with a letter and contain only letters, numbers, and underscore characters: non-conforming characters are automatically replaced by underscores.
Moreover, due to a limitation in MS-Word, identifiers longer than 40 characters are truncated.

> Use in template document
>
> ```
> // Example of text block bookmark, the bookmark identifier contains the name value:
> {@name | bookmarkCreate: identifier | p}
> // Example adding some other text in the same paragraph and using a custom paragraph style:
> {@'Some text: ' + (name | bookmarkCreate: identifier) | p: 'Heading 1'}
> // Example of location bookmark:
> {@identifier | bookmarkCreate | p}
> ```

### bookmarkLink

Creates a hyperlink to a text block or location bookmark usually created using the `bookmarkCreate` filter.

Bookmark identifiers need to begin with a letter and contain only letters, numbers, and underscore characters: non-conforming characters are automatically replaced by underscores.
Moreover, due to a limitation in MS-Word, identifiers longer than 40 characters are truncated.

> Use in template document
>
> ```
> {@input | bookmarkLink: identifier | p}
> // Example adding some other text in the same pargraph:
> {@'Some text: ' + (input | bookmarkLink: identifier) | p}
> ```

### bookmarkRef

Creates a clickable reference to a text block bookmark usually created using the `bookmarkCreate` filter.

Bookmark identifiers need to begin with a letter and contain only letters, numbers, and underscore characters: non-conforming characters are automatically replaced by underscores.
Moreover, due to a limitation in MS-Word, identifiers longer than 40 characters are truncated.

> Use in template document
>
> ```
> {@identifier | bookmarkRef | p}
> // Example adding some other text in the same pargraph:
> {@'Some text: ' + (identifier | bookmarkRef) | p}
> ```

### capfirst

Capitalizes input first letter.

> Use in template document
>
> ```
> // Example with "hello world"
> {input | capfirst} -> "Hello world"
> ```

### changeID

Replaces the default identifier prefix (IDX-) by the supplied prefix

> Use in template document
>
> ```
> {identifier | changeID: 'PROJ1-'}
> ```

### convertDate

Convert Date to proper format. Must be used on values with date format.

> Use in template document
>
> ```
> // Example with {date_start: '2020-10-29'}
> {date_start | convertDate: 'short'} -> 10/29/2020
> {date_start | convertDate: 'full'} -> Thursday, October 29, 2020
> ```

### convertDateLocale

Convert Date to proper format using locale. Must be used on values with date format.

> Use in template document
>
> ```
> // Example with {date_start: '2020-10-29'}
> {date_start | convertDateLocale: 'de-DE':'short'} -> 29.10.2020
> {date_start | convertDateLocale: 'fr':'full'} -> Jeudi 29 Octobre 2020
> ```

### convertHTML

Convert HTML values to OOXML format. See [HTML values](docxtemplate.md?id=html-values-from-text-editors) for usage.

> Use in template document
>
> ```
> {@value | convertHTML}
> ```

### count

Count the number of vulnerabilities by CVSS severity.

> Use in template document
>
> ```
> // Example counting 'Critical' vulnerabilities
> {findings | count: 'Critical'}
> ```

### d

Default value: returns input if it is truthy, otherwise its parameter.

> Use in template document
>
> ```
> // This generates a comma-separated list of affected systems, falling-back on the whole audit scope if left empty.
> {affected | lines | d: (scope | select: 'name') | join: ', '}
> ```

### fromTo

Display _"From ... to ..."_ dates nicely, removing redundant information when the start and end dates occur during the same month or year.

The resulting text can be typically used in a table summarizing the audit, audit perimeters or audits campaign properties, or inside a text paragraph such as a management summary.

To internationalize or customize the resulting string, associate the desired output to the strings `"from {0} to {1}"` and `"on {0}"` in your Auditforge translate file.
Date formating relies on the locale name provided as second parameter.

> Use in template document
>
> ```
> {date_start | fromTo: date_end:'en-UK' | capfirst}
> // Output varies automatically depending on the start and end dates:
> // - Same day        -> On 28/11/2022
> // - Same month      -> From 28 to 30/11/2022
> // - Same year       -> From 28/11 to 02/12/2022
> // - Different years -> From 28/11/2022 to 06/01/2023
> ```

### groupBy

Group input elements by an attribute.

The elements are returned as an objects set where:

- The 'key' property is the common attribute value,
- The 'value' property is the set of items from the input structure sharing this same value for this attribute.

> Use in template document
>
> ```
> {#findings | groupBy: 'severity'}
> Severity: {key}
> {#value}
> Title: {title}
> {/value}
> {/findings | groupBy: 'severity'}
> ```

### initials

Returns the initials from an input string (typically a firstname).

> Use in template document
>
> ```
> // Example with "Foo-Bar"
> {creator.firstname | initials} -> "F.-B."
> ```

### join

Returns a string which is a concatenation of input elements using an optional separator string.

Can also be used to build raw OOXML strings.

> Use in template document
>
> ```
> {references | join: ', '}
> ```

### length

Returns the length (ie. number of items for an array) of input.

Can also be used as a conditional to check the emptiness of a list.

> Use in template document
>
> ```
> // Display the number of elements:
> {findings | length}
> // Continue only if non-empty:
> {#input | length}Not empty{/input | length}
> ```

### lines

Takes a multilines input strings (either raw or simple HTML paragraphs) and returns each line as an ordered list.

> Use in template document
>
> ```
> {input | lines}
> ```

### linkTo

Takes a text to display and a URL to generate a hyperlink.

> Use in template document
>
> ```
> {@cvss.vectorString | linkTo: 'https://www.first.org/cvss/calculator/3.1#' + cvss.vectorString | p}
> ```

### loopObject

Loop over the input object, providing access to its keys and values.

> Use in template document
>
> ```
> {#findings | loopObject}
> {key}: {value.title}
> {/findings | loopObject}
> ```

### lower

Lowercases input.

> Use in template document
>
> ```
> // Example with "Hello WORLD"
> {input | lower} -> "hello world"
> ```

### mailto

Creates a clickable "mailto:" link, assumes that input is an email address if no other address has been provided as parameter.

The character style "Hyperlink" is applied to the generated hyperlink.

> Use in template document
>
> ```
> {@lastname | mailto: email | p}
> // Example adding some other text in the same pargraph and displaying the email address instead of the last name:
> {@'Some text: ' + (email | mailto) | p}
> ```

### map

Applies a filter on a sequence of objects.

> Use in template document
>
> ```
> {scope | select: 'name' | map: 'lower' | join: ', '}
> ```

### p

Embeds input within OOXML paragraph tags, applying an optional style name to it.

> Use in template document
>
> ```
> {@input | p: 'Some style'}
> ```

### reverse

Reverses the input array order.

> Use in template document
>
> ```
> {input | reverse}
> ```

### s

Add proper XML tags to embed raw string inside a docxtemplater raw expression.

> Use in template document
>
> ```
> // Example creating a text block bookmark containing the vulnerability title prefixed by the static string "Vulnerability: ":
> {@('Vulnerability: ' | s) + title | bookmarkCreate: identifier | p}
> ```

### select

Looks up an attribute from a sequence of objects, doted notation is supported.

> Use in template document
>
> ```
> {findings | select: 'cvss.environmentalSeverity'}
> ```

### sort

Sorts the input array according an optional given attribute, dotted notation is supported.

> Use in template document
>
> ```
> {#findings | sort 'cvss.environmentalSeverity'}{name}{/findings | sort 'cvss.environmentalSeverity'}
> ```

### sortArrayByField

Sort array by supplied field. S
Order can be 1 for ascending, or -1 for descending

> Use in template document
>
> ```
> {#findings | sortArrayByField: 'identifier':1}
> {identifier}
> {/}
> ```

### title

Capitalizes input first letter of each word, can be associated to 'lower' to normalize case.

> Use in template document
>
> ```
> // Example with "john DOE"
> {creator.lastname | lower | title} -> "John Doe"
> ```

### toJSON

Returns the JSON representation of the input value, useful to dump variables content while debugging a template.

> Use in template document
>
> ```
> {input | toJSON}
> ```

### upper

Upercases input.

> Use in template document
>
> ```
> // Example with "Hello World"
> {input | upper} -> "HELLO WORLD"
> ```

### where

Filters input elements using a free-form Angular statement.

> Use in template document
>
> ```
> {#findings | where: 'cvss.severity == "Critical"'}{title}{/findings | where: 'cvss.severity == "Critical"'}
> ```

Custom filters can also be created in `backend/src/lib/custom-generator.js`. As an example there are 2 filters defined for french reports.

### convertDateFR (custom)

Convert Date to proper format in French. Must be used on values with date format.

> Use in template document
>
> ```
> // Example with {date_start: '2020-10-29'}
> {date_start | convertDateFR: 'short'} -> 29/10/2020
> {date_start | convertDateFR: 'full'} -> Jeudi 29 Octobre 2020
> ```

### criteriaFR (custom)

Convert cvss Criteria to French.

> Use in template document
>
> ```
> // Example with cvssObj.AV === 'Network'
> {cvssObj.AV | criteriaFR} -> Réseau
> ```

### $pageBreakExceptLast

Creates Page Break

> Use in template document
>
> ```
> {@$pageBreakExceptLast}
> ```



### File: auditforge/docs/installation.md

# Installation

> AuditForge uses 4 containers: the backend, the frontend, the database and the AI model.

## Production

All 4 containers can be run at once using the docker-compose file in the root directory.

!> For production usage make sure to change the certificates in `backend/ssl` and `cwe_api/ssl` folders and optionally to set the JWT secret in `backend/src/lib/auth.js` (`jwtSecret` and `jwtRefreshSecret` in `backend/src/config/config.json`) if you don't want to use random ones.

Build and run Docker containers

```
docker-compose up -d --build
```

Display backend container logs

```
docker-compose logs -f auditforge-backend
```

Stop/Start containers

```
docker-compose stop
docker-compose start
```

Remove containers

```
docker-compose down
```

Update

```
docker-compose down
git pull
docker-compose up -d --build
```

Application is accessible through https://localhost:8443  
API is accessible through https://localhost:8443/api

## Development

For development purposes, specific docker-compose file can be used in each folder (backend/frontend).

> _Source code can be modified live and application will automatically reload on changes._

Build and run backend and database containers

```
docker-compose -f backend/docker-compose.dev.yml up -d --build
```

Display backend container logs

```
docker-compose -f backend/docker-compose.dev.yml logs -f auditforge-backend
```

Stop/Start container

```
docker-compose -f backend/docker-compose.dev.yml stop
docker-compose -f backend/docker-compose.dev.yml start
```

Remove containers

```
docker-compose -f backend/docker-compose.dev.yml down
```

Application is accessible through https://localhost:8081  
API is accessible through https://localhost:8081/api

## Tests

> For now only backend tests have been written (it's a continuous work in progress)

Test files are located in `backend/tests` using Jest testing framework

Script `run_tests.sh` at the root folder can be used to launch tests :

```
Usage:        ./run_tests.sh -q|-f [-h, --help]

Options:
  -h, --help  Display help
  -q          Run quick tests (No build)
  -f          Run full tests (Build with no cache)
```

!> **Don't use it in production as it will delete the production Database**

## Backup

It's possible, even recommended, to regularly backup the `backend/mongo-data` folder. It contains all the database.

To restore :

- Stop containers
- Replace the current `backend/mongo-data` folder with the backed up one
- Start containers



### File: auditforge/docs/roles.md

# Roles

> Auditforge can manage different user account roles to access different kind of data with some level of granularity<br>
> There are 2 builtins roles: user and admin. But additional custom roles can easily be added.

## List of permissions

Here is the list of available permissions to access data:

|      Audits       |       Vulnerabilities        |       Data       |           Custom Data           |       Settings       |   Classify   |
| :---------------: | :--------------------------: | :--------------: | :-----------------------------: | :------------------: | :--------:   |
|   audits:create   |    vulnerabilities:create    |   users:create   |        languages:create         |    settings:read     | classify:all | 
|    audits:read    |     vulnerabilities:read     |    users:read    |         languages:read          | settings:read-public |              |
|   audits:update   |    vulnerabilities:update    |   users:update   |        languages:update         |   settings:update    |              |
|   audits:delete   |    vulnerabilities:delete    |   users:delete   |        languages:delete         |                      |              |
|  audits:read-all  | vulnerability-updates:create |  clients:create  |       audit-types:create        |                      |              |
| audits:update-all |                              |   clients:read   |        audit-types:read         |                      |              |
| audits:delete-all |                              |  clients:update  |       audit-types:update        |                      |              |
|   audits:review   |                              |  clients:delete  |       audit-types:delete        |                      |              |
| audits:review-all |                              | companies:create |   vulnerability-types:create    |                      |              |
|                   |                              |  companies:read  |    vulnerability-types:read     |                      |              |
|                   |                              | companies:update |   vulnerability-types:update    |                      |              |
|                   |                              | companies:delete |   vulnerability-types:delete    |                      |              |
|                   |                              | templates:create | vulnerability-categories:create |                      |              |
|                   |                              |  templates:read  |  vulnerability-categories:read  |                      |              |
|                   |                              | templates:update | vulnerability-categories:update |                      |              |
|                   |                              | templates:delete | vulnerability-categories:delete |                      |              |
|                   |                              |    roles:read    |      custom-fields:create       |                      |              |
|                   |                              |                  |       custom-fields:read        |                      |              |
|                   |                              |                  |      custom-fields:update       |                      |              |
|                   |                              |                  |      custom-fields:delete       |                      |              |
|                   |                              |                  |         sections:create         |                      |              |
|                   |                              |                  |          sections:read          |                      |              |
|                   |                              |                  |         sections:update         |                      |              |
|                   |                              |                  |         sections:delete         |                      |              |

## Built-In Roles

### user

This role has following permissions:

- audits:create, audits:read, audits:update, audits:delete
- vulnerabilities:read, vulnerability-updates:create
- users:read, roles:read
- clients:create, clients:read, clients:update, clients:delete
- companies:create, companies:read, companies:update, companies:delete
- templates:read
- languages:read, audit-types:read, vulnerability-types:read, vulnerability-categories:read, sections:read, custom-fields:read
- settings:read-public
- classify:all

### admin

This role has full permissions access

## Create additional Roles

Custom roles can be defined in `backend/src/config/roles.json`
The format is:

```
role_name: {
  allows: [], // Array of allowed permissions to access or use '*' for all (admin)
  inherits: [] // Array of inherited users permissions
}
```

A default custom role is already defined as a `report` role for example:

```
"report": {
  "inherits": ["user"],
  "allows": [
    "audits:read-all"
  ]
}
```

This role inherits all `user` permissions but since `user` can only access and modify its own Audits, we add the `audits:read-all` permission to `report` to access all Audits.  
To update and delete all Audits additional `audits:update-all` and `audits:delete-all` would be required.

To be able to properly use the review feature of the application, a reviewer role should be added. This reviewer should have the `audits:review` or `audits:review-all` permissions to be able to review reports. A reviewer with only the `audits:review` permission can only review the reports on which they are assigned. The role could look like the following:

```
"reviewer": {
  "inherits": ["user"],
  "allows": [
    "audits:review"
  ]
}
```

A reviewer with the `audits:review-all` permission should also have the `audits:read-all` permission to be able to take full advantage of the first one. He could look like the following:

```
"reviewer": {
  "inherits": ["user"],
  "allows": [
    "audits:review-all",
    "audits:read-all"
  ]
}
```

Keep in mind that these two roles inherit their permissions from the `user` role, which means that they can also create their own audits. A reviewer cannot review an audit for which he is the creator or a collaborator.



### File: auditforge/docs/vulnerabilities.md

# Vulnerabilities

> Auditforge can manage Vulnerabilities in order to simplify redaction of an Audit. They can be added when editing an Audit as a Finding.<br>
> Each vulnerability can have multiple languages.

## Create

When creating a Vulnerability, a Category must be selected (or No Category)

A Vulnerability is defined by:

- Title
- Type
- Language
- Description
- Observation
- CVSS
- Remediation
- Remediation Complexity
- Remediation Priority
- CWEs
- References
- Category
- (Additional fields from Category)

!> Title must be unique since it's used for another functionality allowing users to request creation/modification of vulnerabilities when redacting an Audit.

There is also the possibility to search Audits containing the Vulnerability in its findings (search by Title) :<br>
![Search in Audits](_images/action_buttons.png)

## Import/Export

Vulnerabilities can be exported/imported in Data menu.

The export format is yaml.

**Example**

```
- references:
    - reference1
    - reference2
  cvssv3: 'CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N'
  cvssScore: '3.1'
  cvssSeverity: Low
  priority: 2
  remediationComplexity: 2
  details:
    - locale: fr
      title: Attributs des cookies
      vulnType: Application Web
      description: >-
        Les cookies permettent de stocker des informations relatives à
        l'utilisateur comme par exemple ses informations de session.

        Il est donc important qu'ils soient sécurisés au maximum afin de
        prévenir toute fuite d'informations. Pour cela il existe des «flags» à
        définir lors de la création d'un cookie:

        - le flag «Secure» indique que le cookie ne peut être transmis que si le
        canal de communication est chiffré (HTTPS)

        - le flag «HttpOnly» indique que le cookie ne peut être récupéré par du
        code JavaScript ce qui prévient sa récupération par des attaques de type
        XSS
      observation: null
      remediation: Définir les flags «Secure» et «HttpOnly» lors de la création de cookies
    - locale: en
      title: Cookie Without the HTTPOnly and Secure Flags
      vulnType: Web Application
      description: >-
        Session tokens stored in the “Cookie” headers can be protected from client-side attacks. Those protections are referred to as flags that the web server declares on each cookie it sets.
        Among those flags, the “HTTPOnly” flag restricts access to the cookie from the JavaScript code. The “secure” flag restricts the transmission of the protected cookie on a regular HTTP channel. Those two flags were not set for some cookies used by the application.
      observation: >-
        With a successful Cross-Site Scripting (XSS) exploitation, the attacker could access the cookies using JavaScript and steal the session token of the victim to impersonate him on the application. The “HTTPOnly” flag would prevent the attacker from accessing the cookie in this scenario.
        Another strategy an attacker could exploit is eavesdropping on web traffic and wait for the client to use resources over the HTTP cleartext protocol. If the resources reside on the same domain, the vulnerable cookie will be used over this channel and captured by the attacker. Also, a "man-in-the-middle" (MITM) technique called “SSL Stripping” could be performed by the attacker to force usage of the insecure HTTP protocol. Again, the session token could be captured when the “secure” flag is not set.
      remediation: |
        Ensure the “HTTPOnly” and “secure” flags are set on each cookie that is used by the application.
```

For import, the Serpico format is also accepted allowing easier transition or just to have a default set of vulnerabilities.

## Merge

It's possible to merge vulnerabilities for cases where 2 different vulnerabilities exist for 2 different languages. The goal is to avoid duplicates and better multilanguage management.

![Merge Vulns](_images/merge_vulns.png)

When both languages have been selected, only Vulnerabilities that don't have the other column language will be displayed.  
In this example :

- In the left column only Vulnerabilities having English language AND no French language are displayed
- In the right column only Vulnerabilities having French language AND no English language are displayed

The language details from the Vulnerability of the right column will be moved to the Vulnerability of the left column. So this is _CVSS_, _references_, _etc_ of the left column that will be kept.

## Validate

All users can request creation or modifications on a vulnerability when redacting findings in an Audit. Users with admin role can see and validate those modifications in Vulnerabilities menu.

🚧 WIP 🚧

<!--![Validate](_images/new_updates_vulns.png)-->

**New**

![New vuln](_images/new_vuln.png)

Before approving, it's possible to make changes to the Vulnerability including adding Languages.

**Updates**

![Updates vuln](_images/updates_vuln.png)

The left side is the current Vulnerability

The right side has multiple tabs, each representing change requests made by users. There is syntax highlighting to make it easier to spot differences.

The admin user must manually make changes in the left side with what he wants from the right side. When clicking the Update button the left side will be saved and all update requests from the right side will be deleted.

