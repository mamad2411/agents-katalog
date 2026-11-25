---
name: headrick7-login
description: Log in to headrick7.com (CSN site) using browser automation via Playwright. Use when the user asks to sign in, log in, or access their account on headrick7.com.
---

# headrick7-login

Log into headrick7.com using a headless Playwright browser.

## Login

Run the script with the user's credentials:

```bash
node scripts/login.js <username> <password>
```

Output is JSON: `{ success, message, title, url }`

- On success: reports the page title and URL after login
- On failure: reports the error or reason

## Credentials

- **Username:** goldbot325@gmail.com
- **Password:** goldbot325

## Notes

- The site appears to be a Moodle/CSN-based platform; login path is `/login/index.php`
- Always use `headless: true` (no visible browser window)
- Script lives at: `scripts/login.js`
