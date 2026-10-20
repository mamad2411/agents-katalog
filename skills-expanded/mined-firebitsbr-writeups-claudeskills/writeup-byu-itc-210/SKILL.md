<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-byu-itc-210
description: CTF writeups and security challenges by BYU-ITC-210.
---

# Writeups by BYU-ITC-210

Source repository: `/repos/BYU-ITC-210`

## Repository Index

- LabWriteupExample/README.md

## Writeup Content


### File: LabWriteupExample/README.md

*This sample is intended to show the expected layout and length of a lab writeup. The application is fictional and many of the described actors and protocols don't exist. The diagrams and the accompanying text don't necessarily match. In your writeups, all components should exist, and there should be coherence between the text and the images.*

## Introduction:
John Smith  
20 January 2023  
Lab 1  

## Executive Summary:

This lab implements an API for storing widgets in isolated or aggregated form. Authentication is delegated to Jupiter using the IA67 protocol. A self-test and diagnostics framework is also included.

## Design Overview:

The following UML diagram shows the basic architecture of the widget application. The swimlanes in the UML show the actions taken by the different actors in the system.

### Example UML Caption or Title
![Example UML](./img/example-UML.svg)

*Each lab instruction indicates the type of UML that is expected in the writeup. Ensure such UMLs are included.*

As indicated in the UML, all actions are initiated by the motivator which communicates with the front-end server. Each the server accesses the database by way of the biphasic louderberry protocol. Responses are then reformatted into JSON and returned to the motivator.

The following screenshots show the User Endpoint, the Tasks Endpoint, and the Google Login.

### User Endpoint
![Example Screenshots](./img/user.png)

### Tasks Endpoint
![Example Screenshots](./img/tasks.png)

### Google Login
![Example Screenshots](./img/auth.png)

### File Descriptions

* routes/auth.js - Contains the endpoints for logging the user in and out  
* routes/tasks.js - Contains all the endpoints to perform the CRUD functions for the tasks  
* routes/user.js - Contains the GET endpoint to get all the user data  
* models/Task.js - Contains the task model to interact with the Mongo database  
* mongoose.js - Creates the connection to the Mongo database  
* mssqldb.js - Creates the connection to the Azure database  
* passport.js - Creates the passport session

## Questions:

*The Questions to answer can be found at the bottom of each lab instruction. Ensure you have the questions from both part A and part B in your writeup*

1. List three advantages to using a web API.
    - The front end and back end can be developed at the same time
    - Multiple front ends can use the same API back end
    - Updates can be made to the front and or back end without affecting the other one

1. What are the differences between these four HTTP methods: GET, POST, PUT, and DELETE? Which ones are idempotent?  

    GET is used to fetch data and does not have a request body. It is used only to get data and does not modify it in any way. 
    
    POST sends new data in the body of a request and does something to add new data to the API such as creating a new database record. 
    
    PUT is used to update an existing piece of information using the data in the body of the request such as changing a value from true to false of a task. 
    
    DELETE is used to indicate that data needs to be removed such as removing a task from a database because it has been completed.
    
    GET, PUT and DELETE are idempotent whereas POST is not non-idempotent

## Lessons Learned:

### JavaScript Comparisons  

JavaScript does extremely loose comparisons. Therefore if (thisVar == 0) will evaluate true if thisVar = 0 or null or “” or false. This problem often arises when doing an if statement where you want to check if something is not blank but 0 is a good value. To solve this problem use === or !==. These mean an exact comparison, not a loose comparison. Therefore if (thisVar === “”) and thisVar = 0 it will be false. On the other hand if (thisVar == “”) and thisVar = 0 it will evaluate true.

*There should be 3 lessons learned in your write-up, not just one.*

## Conclusions :

- Use nodejs to create an API
- Install packages using npm
- Create an SSL certificate
- Create firewall rules to allow traffic

## References

https://nodejs.org/docs/latest/api/  
https://certbot.eff.org/  
https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups.html

