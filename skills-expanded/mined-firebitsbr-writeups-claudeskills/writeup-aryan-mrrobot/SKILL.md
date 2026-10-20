<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aryan-mrrobot
description: CTF writeups and security challenges by aryan-mrrobot.
---

# Writeups by aryan-mrrobot

Source repository: `/repos/aryan-mrrobot`

## Repository Index

- Bug-Bounty-Tracker/README.md

## Writeup Content


### File: Bug-Bounty-Tracker/README.md

<h1 align="center"><img width="512" height="512" alt="image" src="https://github.com/user-attachments/assets/eca5642d-ca2a-4cde-9723-ae76f447a07a" />
 Bug Bounty Tracker</h1>

<p align="center">
  A modern <b>Electron desktop application</b> for bug bounty hunters to track progress, manage bug reports,
  and analyze hunting time — fully offline and privacy-friendly.
</p>

<hr/>

<h2>✨ Features</h2>

<h3>📊 Dashboard</h3>
<ul>
  <li>Yearly progress tracker (days completed vs remaining)</li>
  <li>Earnings progress with goal visualization</li>
  <li>Quick stats: total bugs, critical bugs, daily & weekly hours</li>
</ul>

<h3>🐞 Bug Reports</h3>
<ul>
  <li>Add and manage bug bounty reports</li>
  <li>Sort by newest, oldest, highest, or lowest payout</li>
  <li>Export reports for backup or sharing</li>
  <li>Severity-based visualization</li>
</ul>

<h3>⏱️ Time Tracker</h3>
<ul>
  <li>Start / Pause / Stop hunting sessions</li>
  <li>Activity-based tracking (Bug Hunting, Recon, Learning, etc.)</li>
  <li>Daily and weekly analytics</li>
  <li>Session notes support</li>
</ul>

<h3>💾 Local & Private</h3>
<ul>
  <li>100% offline usage</li>
  <li>No accounts, no cloud, no tracking</li>
  <li>All data stored locally</li>
</ul>

<hr/>

<h2>🖼️ Screenshots</h2>

<h3>Dashboard</h3>
<img width="1381" height="887" alt="image" src="https://github.com/user-attachments/assets/d2379ed2-b6e2-407b-9f3a-cb81fa63f48e" />


<h3>Bug Reports</h3>
<img width="1374" height="871" alt="image" src="https://github.com/user-attachments/assets/bf050335-1fe8-43f5-a897-d505d9abe69e" />


<h3>Time Tracker</h3>
<img width="1901" height="1023" alt="image" src="https://github.com/user-attachments/assets/0f853e6f-3bcf-4faa-86ea-9620f858126d" />


<hr/>

<h2>🧰 Tech Stack</h2>
<ul>
  <li><b>Electron</b> – Desktop framework</li>
  <li><b>HTML, CSS, Vanilla JavaScript</b></li>
  <li><b>LocalStorage</b> – Persistent offline storage</li>
</ul>

<hr/>

<h2>📦 Download & Install</h2>

<h3>Option 1: Run from Source (Recommended)</h3>

<h4>Prerequisites</h4>
<ul>
  <li>Node.js <b>v18+</b></li>
  <li>Git</li>
</ul>

<pre><code>git clone https://github.com/YOUR_USERNAME/Bug-Bounty-Tracker.git
cd Bug-Bounty-Tracker
npm install
npm start
</code></pre>

<p>The application will launch as a <b>desktop app</b>.</p>

<h3>Option 2: Windows Installer (if available)</h3>
<ol>
  <li>Go to the <b>Releases</b> section</li>
  <li>Download <code>Bug Bounty Tracker Setup.exe</code></li>
  <li>Install and run 🎉</li>
</ol>

<hr/>

<h2>🛠️ Build the Application</h2>

<h3>Windows</h3>
<pre><code>npm run build:win
</code></pre>

<p>
<b>Note:</b> If you encounter a symlink error on Windows,
enable <b>Developer Mode</b> from:
<br/>
<code>Settings → Privacy & Security → For developers → Developer Mode</code>
</p>

<hr/>

<h2>📁 Project Structure</h2>

<pre><code>Bug-Bounty-Tracker/
│
├── main.js        # Electron main process
├── preload.js    # Secure IPC bridge
├── index.html    # UI
├── styles.css    # Styling
├── app.js        # App logic
├── icon.png
├── package.json
├── README.md
└── screenshots/
</code></pre>

<hr/>

<h2>🚀 Roadmap</h2>
<ul>
  <li>SQLite database support</li>
  <li>Encrypted local storage</li>
  <li>Tray mode & background timer</li>
  <li>Auto backup & restore</li>
  <li>CSV / JSON export</li>
  <li>Multi-profile support</li>
</ul>

<hr/>

<h2>🤝 Contributing</h2>
<ol>
  <li>Fork the repository</li>
  <li>Create a feature branch</li>
  <li>Commit your changes</li>
  <li>Open a Pull Request</li>
</ol>

<hr/>

<h2>📄 License</h2>
<p>MIT License — free to use, modify, and distribute.</p>

<hr/>

<p align="center">
  Built with ❤️ for bug bounty hunters
</p>

