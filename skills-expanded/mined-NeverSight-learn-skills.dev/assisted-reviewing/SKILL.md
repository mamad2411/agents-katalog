---
name: assisted-reviewing
description: Review the pull request at a high level of detail taking account the skills (if any) defined in the project, rules defined in .cursor/rules and basic standard levels of code style and structure. Use when user wants to review a pull request, or mentions "assisted reviewing".
---

Review the pull request at a high level of detail taking account the skills (if any) defined in the project, rules defined in .cursor/rules and basic standard levels of code style and structure. For reviewing a pull request you will analyze the pull request description and files to completely understand what's the PR about, once you are done analyzing the whole code you will diff it with the main branch and go file by file creating a summary of what was well done what needs improvement and what's breaking the rules defined for the project. When defining what needs improvement we will define it in three levels:

- Level 1: minor adjustments, when the naming conventions are odd and small code style adjustments that don't affect the code.

- Level 2: moderate adjustments, when the code is not efficient because the big o notation is high, incorrect use of semantic html, incorrect/inefficient CSS, incorrect use of the guidelines of the project defined in ./cursor/rules. Also check for unused libraries, typescript types and files if there happens to be any in this particular pull request.

- Level 3: major adjustments, when the code is not following any of the architecture, code is breaking due to a potential bugs, cybersecurity breaches could get introduced with this code, bad usage of typescript, bypassing the creation of tests.

You will walk me file by file so I can completely understand each file and how they integrate into the feature. You will allow me to add my input on each file we are reviewing once you finish printing the output stated below so we can later build a strong feedback. The expected output is the following:

example output
```md
// periop-embed-clinic/src/features/SchedulingForm/SelectCptCode/SelectCptCode.tsx

## SelectCptCode.tsx

### File overview:

{make a summary of the file and explain how it integrates into the codebase, and how it contributes to the actual feature}

---

### ✅ What was well done:

{Highlight the parts where the developer showed a high level of understanding, showing the parts where the component shows a level of reasoning put by the developer}

---

### ❌ What needs improvement:

Level 1 - minor adjustments:

{Show the parts where the developer performed poorly according to the description of the defined reviewing level (feel free to skip this level 1 section if you don't find anything)}

Level 2 - moderate adjustments:

{Show the parts where the developer performed poorly according to the description of the defined reviewing level (feel free to skip this level 2 section if you don't find anything)}

Level 3 - major adjustments:

{Show the parts where the developer performed poorly according to the description of the defined reviewing level (feel free to skip this level 3 section if you don't find anything)}

---

### Recommendations:

{Write the recommendations for this file to pass the levels of adjustments, fix bug and inefficiencies, take into consideration every aspect that needs to be reviewed stated above. Place these recommendations in a numerated list format and don't doubt of adding code examples with the solutions}

```

 If I don't provide any feedback we will fill the feedback with the recommendations you add in the output. There will be a final output with the whole summary of files once we finish going each by each but for the final output we will only print a summary of what was well done, what needs improvement and the recommendation we left.