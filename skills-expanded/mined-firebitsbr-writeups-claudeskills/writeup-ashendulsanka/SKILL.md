<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ashendulsanka
description: CTF writeups and security challenges by AshenDulsanka.
---

# Writeups by AshenDulsanka

Source repository: `/repos/AshenDulsanka`

## Repository Index

- pentestportal/README.md
- pentestportal/client/README.md

## Writeup Content


### File: pentestportal/README.md

# PentestPortal

> Note: This is a personal learning project built to explore full-stack development with Node.js, Express, React, and PostgreSQL. Created as an open-source tool for anyone to use. The repo will be archived as I've moved on to other projects, but it's kept public for reference and learning purposes.

A comprehensive penetration testing management platform built with the PERN stack (PostgreSQL, Express.js, React.js, Node.js).

<div align="center">
  <div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/user-attachments/assets/16175d16-ee81-4352-b55b-a75579a8ec11" alt="Dashboard" width="32%" />
    <img src="https://github.com/user-attachments/assets/d7cf9d00-6abd-42d7-876a-a46c9b7b3032" alt="Reports List" width="32%" />
    <img src="https://github.com/user-attachments/assets/df2482fd-0f99-406a-af46-756872c1903d" alt="Report View" width="32%" />
  </div>
  <div>
    <em>Left to right: Dashboard, Reports List, Report View</em>
  </div>
</div>


## Tech Stack

- **Frontend**: React.js, Material-UI
- **Backend**: Node.js, Express.js
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Email**: SMTP Integration

## Installation

### Manual Setup

1. Clone the repository

    ```
    git clone https://github.com/AshenDulsanka/pentestportal
    cd pentestportal
    ```

2. Setup Database

    - Install PostgreSQL
    - Login as postgres
    - Copy and paste the SQL queries on the `assets/sql/db.sql`.

3. Setup Backend

    ```
    cd server
    npm install
    cp .env.example .env
    # Update .env with your credentials
    npm start
    ```

4. Setup Frontend

    ```
    cd client
    npm install
    npm start
    ```

### Docker Setup

1. Clone the repository

    ```
    git clone https://github.com/AshenDulsanka/pentestportal
    cd pentestportal
    ```

2. Configure Environment

    - Update the environment variables in docker-compose.yml
    - Default ports:
        - Frontend: 3006
        - Backend: 8089
        - Database: 5432

3. Run with Docker

    ```
    docker-compose up --build
    ```

## Default Access

There are some sample data added as well in the `assets/sql/sample_data.sql`. So it will be easier to test it out.

- Sample data account credentials:
    - `penadmin: gk2~3G]4;m5NCu`
    - `randomUser1: test1234`

## Environment Variables

### Backend (.env)

```
PORT=8089
JWT_SECRET=your_secret
SMTPMAIL=your_email
SMTPPASS=your_password
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=pentestportal
```

## Access Application

- Frontend: http://localhost:3006
- Backend API: http://localhost:8089

**NOTE:** The API documentation can be seen from the footer of the frontend. You can view it here with the below screenshot.

![API Documentation](https://github.com/user-attachments/assets/083fb17a-a2aa-4ba3-81bf-27ae5fd12f4f)
<div align="center"><em>API Documentation</em></div>



### File: pentestportal/client/README.md

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

