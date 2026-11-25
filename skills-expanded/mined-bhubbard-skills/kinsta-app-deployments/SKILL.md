---
name: kinsta-app-deployments
description: "Instructions for deploying applications to Kinsta App Hosting. Use this when the user needs to deploy Web Applications, Static Sites, or Background Services to Kinsta App Hosting."
---

# Kinsta Application Deployments

Kinsta provides Application Hosting for web applications, static sites, background workers, and more. When deploying applications to Kinsta, keep the following in mind:

## 1. Connecting a Repository
- Kinsta supports deploying directly from GitHub, GitLab, and Bitbucket.
- Ensure the appropriate permissions are granted to the Kinsta app within the Git provider.

## 2. Choosing an Environment
- Select the region closest to your users for the lowest latency.
- Determine the resource requirements (Standard vs. CPU-Optimized vs. Memory-Optimized).

## 3. Deployment Methods
- **Automatic Deployments**: Any commit to the designated branch will trigger a deployment automatically.
- **Manual Deployments**: Trigger deployments manually through the MyKinsta dashboard.

## 4. Web Processes and Start Commands
- Ensure the start command is correctly defined (e.g., `npm start`, `python manage.py runserver`, or `yarn start`).
- For Node.js apps, `package.json` should have a `start` script defined.
- Listen on the `PORT` environment variable provided by Kinsta.

## 5. Environment Variables
- Store sensitive configuration (like API keys and Database URIs) securely as environment variables in the MyKinsta dashboard.
- Do not hardcode secrets into the source code.

## 6. Logs and Troubleshooting
- Use Kinsta's Runtime Logs to monitor your application for errors.
- Build logs will tell you if there is an issue during the build step (e.g., missing dependencies).
