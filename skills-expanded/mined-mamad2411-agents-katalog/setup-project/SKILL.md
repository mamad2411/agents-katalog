---
name: setup-project
description: Create a new ReadMe Docs project, including new account creation for those without an existing account.
---

# Set up a ReadMe project

This skill walks through the steps to setup a new ReadMe project, including the available options and required MCP configuration.

## Requirements

- This skill assumes that the ReadMe MCP server has been configured. If you do not have the ReadMe MCP available, you must first follow the steps in the `mcp-auth` skill for the specific client and setup the ReadMe MCP server before you can setup a new ReadMe project. Note that you don't need to connect up to an actual project if the user is creating a new account.
- Currently new project setup is only allowed if the user does not have an existing ReadMe account. If the user has an existing account, they must create their new project in the ReadMe UI, and follow the instructions in `mcp-auth` to get their project API key loaded into configuration.

**Done**
- You are connected to the ReadMe MCP server
- You have confirmed that the user is creating this project with a new account, OR if they have an existing account they've manually created it in the UI and have set you up with the API Key:
  - You should have used `execute-request` on the `/v2/projects/me` endpoint and have confirmed that the configuration is correct

## Workflow

### 1. Gather Required Information

Before creating the account and project for the user, you should verify that you have all of the required information to seed their project with some initial content for them to view. Having a project with some details already configured is a much better experience than putting them into an empty, generic project setup.

You should clarify the following with the user:

#### Information Source

What information will you be provided to create the docs for this user? Options include but are not limited to:

- An existing documentation repository that they want to connect via BiDi Sync (see #bidi-sync)
- An existing documentation site that they want to copy verbatim (see #docs-site-import)
- A non docs-website that has relevant information (ie their marketing site)
- Local files that they want to use as information to create a new docs site
- A summary that they will type out for what they want to configure
- An existing code repository that you will read to create docs from
- An existing OAS spec (see #oas-upload)

Note that the user may have one or more of these, and it is not an exhaustive list.

**Done**
You have the information that will be used to create at least the first few pages in the project, and you have verified that you can read these. If you cannot access, tell the user that you cannot and ask if they can provide or whether they would prefer to continue without this information.

#### Branding/Styling

Does the user have an existing color system/style guide? May include but not be limited to:

- Logo(s) and favicon
- Color systems - there are colors available for:
  - Brand (primary) color
  - Links color (if not given use the brand color they give)
  - Backgrount (if not given don't specify)
  - Sidebar Border (if not given don't specify)
  - Borders color (if not given don't specify)
  - BreadCrumts (use brand color if not specified)
  - Tint (accent color)
  - Ask AI (if not given don't specify)
  However, to keep it simple it is usually good to just get the primary/accent colors.

Note that its fine if the user doesn't have anything for this, since its styling that they can configure later via UI.

**Done**
When the user has either:

- Provided styling content; or
- Has said that they don't have any content to give you

#### Gather Account + Project Information (Optional)

IF the user is creating a new account + project, then you also need:

- The user's name
- The user's email
- The project's name

Instruct the user its VERY important that they have access to this email:

- This email owns the project and is the one used for account recovery. If they lose access to it, they may lose access to the project and all progress on it.
- They will need to verify this email before they can publish the project. This does not block setup, so they can do it later.

Use the email exactly as the user gives it. Never change, correct, or invent an email on their behalf - for example adding a `+` alias or fixing what looks like a typo. If you think there is a typo, ask the user to confirm the email instead.

**Done**
You have gathered all required information

### 2. Create initial content plan

Create a plan for the first bits of work you will do with the user - these should focus on the first few actions that you will perform so that the user can inspect their content in the UI as soon as possible.

This may include but not be limited to:

- Starting a docs site import (#docs-site-import)
- Configuring styling
- Creating the first few guide pages/all guide pages in a category for them
- Uploading an OAS spec/manually creating some API reference docs for them.

Unless the user pushes back, you should just focus on a smaller, horizontal across content piece of work (ie not just 5 guides, 3 guides and 2 api references are better) is better.

If the user is not importing from an existing docs site, and isn't uploading OAS specs, recommend to start with 5 pages to the user to get started so they can familiarize themselves with ReadMe, and that you can come back to this afterwards.

It is recommended to read the `manage-navigation` skill to understand how ReadMe does categorization for this, and the `edit-page-content` skill to understand how pages themselves can be formatted.

**Done**
The user has agreed to the initial content plan.

### 3. Execute on the plan

Execute on the content plan that you have agreed on with the user. Ensure that you understand whether the user needs a new account created, or if they have provided you with a project access key.

#### If Creating a new Project + Account

Only create an account if the user has confirmed they want to create a new account/they don't have a ReadMe account. If they have an existing account they must create their project via the UI and provide the API Key.

Follow these steps in order, before doing any of the content plan:

1. **Create the account.** Execute a POST `/v2/projects/ai_onboarding` via the `execute-request` tool from the ReadMe MCP.
   - If the request rejects the email, do NOT retry with an email you have changed or made up. Stop and ask the user, and only retry with the exact email they give you. ReadMe returns the same error for both causes, so tell the user both possibilities:
     - An account already exists for this email. They must sign in via the ReadMe UI to create their new project, then follow the `mcp-auth` skill to give you its API key.
     - The email is invalid. They must give you a different email that they have access to.
2. **Give the user their sign-in URL straight away.** Ask them to sign in with it and tell you once they have. Tell them:
   - The URL can only be used once, and expires after 1 week.
   - The project is empty for now, and they will see content appear as you work on it.
   - They will eventually need to verify their email before publishing the project, but this does not block anything now.
3. **Wait** until the user confirms they have signed in successfully.
4. **Connect the MCP to the new project.** Follow the steps in the `mcp-auth` skill using the API key returned when the account was created.
5. **Execute the content plan.**

## Intake branches

### BiDi Sync

A user can setup bi-directional sync with a local docs repository if that is their prefered method of setup. They cannot configure the git project connection via the server, however you should assist them with the correct formatting of content, folder structure, and more.

If they are creating a project, create their project, setup their styling (if provided) and then ask them to navigate to the `#/settings/git-connection` from any page on their docs domain to setup their BiDi sync.

Refer to the `manage-navigation` skill for how to handle BiDi sync navigation and folder structure.

### Docs Site Import

When importing from an existing documentation site - you may actually import from up to 2x individual projects in parallel. You MUST verify that these are indeed documentation site URLs - marketing site URLs and more will be rejected outright.

For those urls, you should import by doing a POST against the `v2/import` endpoint - find this via MCP and make a request against it.

To find information on all imports for a project you must use the GET `v2/import` as that will give you the list of all imports. For more information on individual imports, use the GET `v2/import/{runId}` endpoint with the runId from the list call.

### OAS Upload

If the user has an existing OAS spec - it can be uploaded to the POST `v2/branches/{branch}/apis` endpoint.
