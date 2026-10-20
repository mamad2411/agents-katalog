<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-anlominus
description: CTF writeups and security challenges by AnLoMinus.
---

# Writeups by AnLoMinus

Source repository: `/repos/AnLoMinus`

## Repository Index

- Diablo/CHANGELOG.md
- Diablo/CODE_OF_CONDUCT.md
- Diablo/CONTRIBUTING.md
- Diablo/README.md
- Diablo/SECURITY.md
- Diablo/.github/PULL_REQUEST_TEMPLATE.md
- Diablo/docs/ARCHITECTURE.md
- Diablo/docs/BEST_PRACTICES.md
- Diablo/docs/FAQ.md
- Diablo/docs/GETTING_STARTED.md
- Diablo/docs/INDEX.md
- Diablo/docs/ROADMAP_NEXT_STEPS.md
- Diablo/docs/SECURITY_MODEL.md
- Diablo/docs/USAGE.md
- Diablo/.github/ISSUE_TEMPLATE/bug_report.md
- Diablo/.github/ISSUE_TEMPLATE/feature_request.md

## Writeup Content


### File: Diablo/README.md

> בס״ד

<div align="center">

<h2 align="center"><a href="https://github.com/Anlominus">⚜️ AnLoMinus ⚜️</a></h2>

<img align="center" width="100" src="https://user-images.githubusercontent.com/51442719/172729066-1293d382-4a31-4f03-8c23-ab0ea5f611a0.png">

⫷ [**`HacKingPro`**](https://github.com/Anlominus/HacKingPro) ⫸
<br>
⫷ [**`TryHackMe`**](https://github.com/Anlominus/TryHackMe) | [**`KoTH`**](https://github.com/Anlominus/TryHackMe/tree/main/King%20of%20the%20Hill/KoTH) ⫸
<br>
⫷ [**`Privilege-Escalation`**](https://github.com/Anlominus/Privilege-Escalation)⫸
<br>
⫷ [**`ScanPro`**](https://github.com/Anlominus/ScanPro) | [**`Linfo`**](https://github.com/Anlominus/Linfo) | [**`Diablo`**](https://github.com/Anlominus/Diablo) ⫸
<br>
⫷ [**`Offensive-Security`**](https://github.com/Anlominus/Offensive-Security) | [**`PenTest`**](https://github.com/Anlominus/PenTest) ⫸
<br>
⫷ [**`Goals`**](https://github.com/Anlominus/Goals) | [**`Studies`**](https://github.com/Anlominus/Studies) | [**`HacKing`**](https://github.com/Anlominus/HacKing) | [**`AnyTeam`**](https://github.com/Anlominus/AnyTeam) ⫸

</div>

---

<div align="center">

# [Diablo](https://github.com/Anlominus/Diablo) 🎯

<a href=""><br><img title="Made in ISRAEL" src="https://img.shields.io/badge/MADE%20IN-ISRAEL-blue?style=for-the-badge"></a>

**Diablo ~ Pentesting / Hacking & Reporting Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Anlominus/Diablo/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/Anlominus/Diablo)](https://github.com/Anlominus/Diablo/issues)
[![GitHub stars](https://img.shields.io/github/stars/Anlominus/Diablo)](https://github.com/Anlominus/Diablo/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Anlominus/Diablo)](https://github.com/Anlominus/Diablo/network)

```shell
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo; chmod 777 Diablo; ./Diablo
```

<img width="801" alt="Diablo Preview" src="https://user-images.githubusercontent.com/51442719/170010336-39176f7e-b5dc-4f31-81ca-4b4144e6938c.png">

**🔴 השתמש באחריות - רק בבדיקות מאושרות!**

</div>

---

## 📋 תוכן עניינים

- [📖 אודות](#-אודות)
- [✨ תכונות](#-תכונות)
- [🚀 התקנה מהירה](#-התקנה-מהירה)
- [📚 תיעוד](#-תיעוד)
- [🎯 שימוש](#-שימוש)
- [🤝 תרומה](#-תרומה)
- [🔐 אבטחה](#-אבטחה)
- [📜 Roadmap](#-roadmap)
- [🙏 קרדיטים](#-קרדיטים)

## 📖 אודות

**Diablo** הוא כלי PenTesting ו-Hacking מדויק שמיועד לביצוע בדיקות חדירה מובנות ויצירת דוחות מפורטים בפורמט Markdown.

### 🎯 מטרות
- **אוטומציה** של תהליכי Reconnaissance
- **ארגון** של כלי PenTest רבים בממשק אחד
- **דוחות** אוטומטיים בפורמט Markdown
- **פשטות** בשימוש ובהוראה

---

## ✨ תכונות

### 🎯 תפריט ראשי

- ✅ **[a] - Anonymity Surfing**
  - Anonimity Surfing status/start/stop
  - Network Manager Menu (ifconfig/ip a)
  
- ✅ **[1] - Planning and Scoping**
  - הגדרת Target IP
  - הגדרת שם הפרויקט
  - הגדרת Domain Name
  - יצירת קובץ דוח ראשוני

- ✅ **[2] - Reconnaissance & Vulnerability Assessment**
  - **Network Analysis:** arp, traceroute, ping, masscan
  - **Port Scanning:** nmap (-sV -sC -O -p-)
  - **DNS Enumeration:** dig, nslookup, whois, dnsenum, fierce, dnsrecon
  - **Web Enumeration:** dirb, nikto
  - **OSINT:** enum4linux

- 🔜 **[3] - Gaining Access & Maintaining Access** (בפיתוח)
- 🔜 **[4] - Covering tracks** (בפיתוח)
- 🔜 **[5] - Analysis & Reporting** (בפיתוח)

### 🔧 תכונות טכניות

- ✅ תמיכה במספר מערכות הפעלה (Linux, macOS, Termux)
- ✅ זיהוי אוטומטי של Package Manager
- ✅ מערכת צבעים עשירה ו-UI מעוצב
- ✅ דוחות אוטומטיים בפורמט Markdown
- ✅ מבנה RepoCraft מלא

---

## 🚀 התקנה מהירה

### Linux / macOS
```bash
# הורד והפעל
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo
chmod +x Diablo
./Diablo
```

### Termux (Android)
```bash
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo
chmod +x Diablo
./Diablo
```

### דרישות
```bash
# Ubuntu/Debian
sudo apt-get install masscan nmap dnsutils whois nikto enum4linux dirb

# macOS
brew install masscan nmap
```

---

## 📚 תיעוד

📖 **תיעוד מלא** זמין ב-[docs/](./docs/INDEX.md)

- [🚀 Getting Started](./docs/GETTING_STARTED.md)
- [🏗️ Architecture](./docs/ARCHITECTURE.md)
- [❓ FAQ](./docs/FAQ.md)

---

## 🎯 שימוש

### דוגמה בסיסית

```bash
./Diablo

# בתפריט:
# [p] → Planning and Scoping
#   1. הזן IP: 192.168.1.1
#   2. הזן שם פרויקט: TestProject
#   3. הזן Domain: example.com

# [2] → Reconnaissance & Vulnerability Assessment
#   כל הסריקות יתבצעו אוטומטית
#   דוח ייווצר: TestProject-Diablo-Log.md
```

### דוגמה לאנונימיות
```bash
# בתפריט בחר [a]
[a] → Anonymity Surfing
[2] → Start anonsurf
```

---

## 🤝 תרומה

תרומות מוערכות מאוד! ראה את [CONTRIBUTING.md](./CONTRIBUTING.md) לפרטים.

### איך לתרום?
1. 🍴 Fork את הפרויקט
2. 🌿 צור branch חדש (`git checkout -b feature/AmazingFeature`)
3. ✅ עשה commit (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push (`git push origin feature/AmazingFeature`)
5. 🔄 פתח Pull Request

---

## 🔐 אבטחה

⚠️ **חשוב: שימוש אתי וחוקי בלבד!**

- 🔴 השתמש **רק** בבדיקות מאושרות
- 🔴 ציית לכל חוק מקומי
- ✅ דווח על פרצות אבטחה: ראה [SECURITY.md](./SECURITY.md)

---

## 📜 Roadmap

### ✅ הושלם
- [x] Planning and Scoping
- [x] Reconnaissance & Vulnerability Assessment
- [x] Anonymity Surfing
- [x] מבנה RepoCraft מלא
- [x] CI/CD ו-workflows
- [x] תיעוד מקיף

### 🔄 בפיתוח
- [ ] Gaining Access & Maintaining Access
- [ ] Covering tracks
- [ ] Analysis & Reporting
- [ ] תיקון תלות ב-HacKingPro
- [ ] ממשק Web UI

> למפת דרכים מפורטת וסעיפים מעשיים לכל פרק, עיין ב-[🌟 המשך Roadmap](./docs/ROADMAP_NEXT_STEPS.md).

---

## 🙏 קרדיטים

### יוצר
- **Moshe Leon Yaakubov (AnLoMinus)** - [GitHub](https://github.com/Anlominus)

### מקורות השראה
- [RapidScan](https://github.com/skavngr/rapidscan)
- [Reconnoitre](https://github.com/codingo/Reconnoitre)
- [OSCP Report Template](https://github.com/noraj/OSCP-Exam-Report-Template-Markdown)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [HacKingPro](https://github.com/Anlominus/HacKingPro)
- [PenTest](https://github.com/Anlominus/PenTest)

### RepoCraft Framework
בנייה על פי [RepoCraft](https://github.com/AnLoMinus/RepoCraft/) framework

---

## 📊 סטטוס הפרויקט

![GitHub Repo stars](https://img.shields.io/github/stars/Anlominus/Diablo?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Anlominus/Diablo?style=social)

![Repobeats analytics](https://repobeats.axiom.co/api/embed/dd90ce889645a0528ddedbb71d7310ab3ec30393.svg "Repobeats analytics image")

---

## 📄 רישיון

פרויקט זה מפורסם תחת [MIT License](./LICENSE)

---

## 🌐 קישורים

- 🌍 [GitHub Repository](https://github.com/Anlominus/Diablo)
- 🐛 [Report Bugs](https://github.com/Anlominus/Diablo/issues)
- 💡 [Request Features](https://github.com/Anlominus/Diablo/issues)
- 📖 [Documentation](./docs/)
- 🤝 [Contributing](./CONTRIBUTING.md)
- ⚠️ [Purification Grid](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221a_XBsk_mXP_0iSBqYimXo7HbavNZ-uJW%22%5D,%22action%22:%22open%22,%22userId%22:%22103930013484441813523%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing
)

---

<div align="center">

**תודה לשימוש ב-Diablo!** 🎯

### ⚠️ אזכור חשוב
**שימוש באחריות בלבד - רק בבדיקות מאושרות!**

---

> בס״ד - מגדל בסייעתא דשמיא

**נוצר עם ❤️ בישראל** 🇮🇱

![Made with Love](https://img.shields.io/badge/Made%20With-Love-red)

</div>




### File: Diablo/.github/ISSUE_TEMPLATE/bug_report.md

---
name: 🐞 דיווח על באג
about: דווח על באג כדי לעזור לנו לשפר
title: "[BUG] "
labels: bug
assignees: ''
---

## 🔍 תיאור הבאג
תיאור קצר ומדויק של הבאג.

## 🔄 צעדים לשחזור הבאג
1. עבור ל'...'
2. לחץ על '...'
3. גלול עד '...'
4. צפה בשגיאה

## ✅ התנהגות צפויה
תיאור קצר ומדויק של מה שהיית מצפה שיקרה.

## 📸 צילומי מסך
אם רלוונטי, הוסף צילומי מסך כדי לעזור להסביר את הבעיה שלך.

## 💻 סביבה
- מערכת הפעלה: [למשל macOS, Linux, Windows]
- גרסה של Diablo: [למשל 1.0.0]
- פלטפורמה: [למשל Termux, macOS, Linux]

## 📋 הקשר נוסף
הוסף כל הקשר אחר על הבאג כאן.

## 🔗 קישורים רלוונטיים
- [קישור 1](URL)
- [קישור 2](URL)




### File: Diablo/.github/ISSUE_TEMPLATE/feature_request.md

---
name: 💡 בקשת תכונה חדשה
about: הצע רעיון לפרויקט
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## 🚀 תיאור התכונה המבוקשת
תיאור קצר ומדויק של התכונה שברצונך לראות.

## 💭 מה המניע לבקשה?
מה הבעיה שהתכונה הזו תפתור?

## 🔧 פתרון מוצע
תיאור קצר ומדויק של מה שברצונך שיקרה.

## 🎯 חלופות שנשקלו
תיאור קצר ומדויק של כל חלופות או תכונות שעשו בחשיבה.

## 📋 מימוש אפשרי
כיצד לדעתך ניתן לממש את התכונה?

## 🔗 דוגמאות
אם התכונה קיימת בכלים אחרים, שתף קישורים או דוגמאות.

## 📋 מידע נוסף
הוסף כל הקשר אחר או צילומי מסך על בקשת התכונה כאן.




### File: Diablo/.github/PULL_REQUEST_TEMPLATE.md

> בס״ד

## 🎯 תיאור השינוי
תיאור קצר ותמציתי של השינויים המבוצעים ב-PR זה.

## 🔗 סוג שינוי
בחר את סוג השינוי שמתאר את ה-PR:

- [ ] 🐛 תיקון באג (שינוי שאינו שובר הקיימים)
- [ ] ✨ תכונה חדשה (שינוי שלא שובר הקיימים)
- [ ] 💥 שינוי שובר (שינוי שישבור פונקציונליות קיימת)
- [ ] 📚 תיעוד (שינויים בתיעוד בלבד)
- [ ] 🎨 שיפור עיצוב/עיצוב UI
- [ ] ⚡️ שיפור ביצועים
- [ ] ♻️ refactor (שינוי קוד שלא משנה פונקציונליות)
- [ ] ✅ בדיקות (הוספת/שיפור בדיקות)
- [ ] 🔧 רכיבי בנייה (שינוי במערכת הבנייה או תלויות חיצוניות)

## 🧪 איך לבדוק?
תיאור הפירוט איך לבדוק את השינויים:
1. שלב 1...
2. שלב 2...
3. צפוי...

## ✅ בדיקות
רשום את הבדיקות שביצעת:
- [ ] בדיקה A
- [ ] בדיקה B

## 📸 צילומי מסך (אם רלוונטי)
הוסף צילומי מסך אם השינוי משפיע על UI.

## 📋 רשימת בדיקה
- [ ] הקוד שלי עומד בהנחיות הפרויקט
- [ ] ביצעתי סקירה עצמית של הקוד שלי
- [ ] ציינתי הערות על קוד מורכב במיוחד
- [ ] הקוד שלי יוצר אזהרות חדשות
- [ ] הבדיקות שלי עוברות
- [ ] כל קבצי תיעוד מעודכנים

## 📝 מידע נוסף
הוסף כל מידע נוסף שיכול לעזור למאשר את ה-PR.

## 🔗 קישורים רלוונטיים
- עונה על: #(מספר issue)
- קשור ל: #(מספר issue)

---

**הערות:**
- נא לשמור על נימוס וכבוד במהלך ביקורת הקוד
- נא להסביר החלטות קוד מורכבות באמצעות הערות
- נא לוודא שכל הבדיקות עוברות לפני הגשה




### File: Diablo/CHANGELOG.md

# 📜 Changelog

כל השינויים המשמעותיים בפרויקט Diablo מתועדים בקובץ זה.

הפורמט מבוסס על [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
והפרויקט עוקב אחר [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🎨 Added
- Structure נבנה על פי RepoCraft framework
- GitHub Actions workflows (CI/CD, linting, security scanning)
- תבניות Issues ו-Pull Requests
- תיעוד מקיף ב-`docs/`
- LICENSE (MIT)
- SECURITY.md
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- .gitignore
- .gitattributes
- .editorconfig

### 🔧 Changed
- שדרוג המבנה הכללי של הפרויקט

### 📚 Documentation
- מסמכי INDEX, GETTING_STARTED, ARCHITECTURE, FAQ
- מדריכים ותיעוד מפורט

## [BETA] - 2022-06-10

### 🎨 Added
- תפריט ראשי בסיסי עם אפשרויות בסיסיות
- [a] - Anonymity Surfing עם תמיכה ב-anonsurf
- [1] - Planning and Scoping - הגדרת מטרות ופרמטרים
- [2] - Reconnaissance & Vulnerability Assessment עם כלים רבים:
  - masscan
  - enum4linux
  - nikto
  - arp scan
  - traceroute
  - ping
  - dig
  - nslookup
  - whois
  - nmap
  - dnsenum
  - fierce
  - dnsrecon
  - dirb
- יצירת דוחות Markdown אוטומטיים
- תמיכה במספר package managers:
  - pkg (Termux)
  - brew (macOS)
  - apt/apt-get (Debian/Ubuntu)
  - apk (Alpine)
  - yum (Fedora)
- מערכת צבעים עשירה
- לוגו ASCII מעוצב
- Network Manager Menu
- התאמה למערכות שונות

### 🔧 Changed
- תלות ב-HacKingPro (טעינה מתוך פרויקט אחר)

### 📝 Planned
- [ ] [3] - Gaining Access & Maintaining Access
- [ ] [4] - Covering tracks
- [ ] [5] - Analysis & Reporting

### 📚 Documentation
- README.md בסיסי עם תכונות ומידע כללי

## [v0.1.0] - 2022-01-XX

### 🎨 Added
- גרסה ראשונית של הפרויקט
- סקריפט Bash בסיסי
- לוגו ASCII ראשוני

---

## 📊 מבנה גרסאות

### גרסה - Format
**Major.Minor.Patch**

- **Major** - שינויים שוברים API
- **Minor** - תכונות חדשות, תואמות אחורה
- **Patch** - תיקוני באגים

### תוויות
- `Added` - תכונות חדשות
- `Changed` - שינויים בקוד קיים
- `Deprecated` - תכונות שיוחלפו
- `Removed` - תכונות שהוסרו
- `Fixed` - תיקוני באגים
- `Security` - שינויים הקשורים לאבטחה

---

## 🔗 קישורים

- [מאגר GitHub](https://github.com/Anlominus/Diablo)
- [Issues](https://github.com/Anlominus/Diablo/issues)
- [Releases](https://github.com/Anlominus/Diablo/releases)

---

> בס״ד

**נוצר בישראל** 🇮🇱 ❤️




### File: Diablo/CODE_OF_CONDUCT.md

# Contributor Covenant Code of Conduct

## 📜 הבטחת התורמים שלנו

כדי לקדם סביבה מקבלת וידידותית, אנחנו חותמים ומתחייבים לסוגיה המשתתפים בפרויקט ולוודא את חוויית הקהילה שלנו נטולת הטרדה לכולם, ללא קשר לגיל, מימד, מוגבלות, מוצא אתני, יישור מגדר, זהות, ביטוי, ניסיון, לאום, זהות אישית, מביאיה ורווח, עמדה פוליטית, נטייה מינית, מעמד חברתי-כלכלי או כל תכונה אחרת.

## 🎯 הסטנדרטים שלנו

### דוגמאות להתנהגות התורמת:

- ✅ שימוש בלשון קבלה וכללה
- ✅ כיבוד נקודות מבט וחוויות שונות
- ✅ קבלת ביקורת בונה באופן מכובד
- ✅ התמקדות במה שטוב ביותר לקהילה
- ✅ הצגת אמפתיה לחברי הקהילה

### דוגמאות להתנהגות בלתי מקובלת:

- ❌ שימוש בשפה או תמונות בעלות אופי מיני ולא מבוקרות, והטרדות מיניות
- ❌ טרול, הערות מעליבות/מזלזלות, והתקפות פולמיות או פוליטיות
- ❌ הטרדה ציבורית או פרטית
- ❌ פרסום מידע פרטי אחר ללא הרשאה
- ❌ התנהגות אחרת שיכולה להחשב כבלתי הולמת בהקשר מקצועי

## 📍 תחום אחריותנו

צוות הפרויקט מחויב:

- ✅ הבהרת הסטנדרטים של ההתנהגות המקובלת
- ✅ נקיטת צעדים נאותים ומגיבים בתגובה לכל מקרה של התנהגות בלתי מקובלת
- ✅ הבהרה והצדקה של סנקציות בפני עוברי עבירה, במטרה להציל את הקהילה
- ✅ קידום סולנות ולביאנה חברתית בקהילה

## 👮 אכיפה

תלונות על התנהגות בלתי מקובלת ניתן לדווח לצוות הפרויקט ב-
**[GitHub Issues](https://github.com/Anlominus/Diablo/issues)** עם תוית "conduct".

הצוות יחויב:

1. לטפל בהקדם
2. לבחון את הבעיה בזהירות
3. לנקוט אמצעים מתאימים

כל התלונות ייבדקו ולחקרן. הצוות מחויב לשמירה על סודיות ביחס לדיווח על אירוע.

## 🌟 הכרה

**זהו קוד התנהגות מבוסס על**
[Contributor Covenant](https://www.contributor-covenant.org),
**גרסה 2.1, זמינה ב-**
https://www.contributor-covenant.org/version/2/1/code_of_conduct.html

---

## 🇮🇱 רקע עברי

פרויקט זה נוצר בישראל, ומקדם ערכים של:
- כבוד הדדי (כבוד)
- סיוע (חסד)
- קדושה בעבודה טכנית

**למה להגיד בס״ד?** "סיעתא דשמיא" - הנסיעה מהשמים. אנחנו מאמינים שיש ערך רוחני גם בעבודה טכנית.

---

> בס״ד - מגדל בסייעתא דשמיא

**קהילה מכבדת - פרויקטים טובים יותר** ✨




### File: Diablo/CONTRIBUTING.md

> בס״ד

# 🤝 מדריך תרומה ל-Diablo

תודה על העניין שלך בתרומה ל-Diablo! מסמך זה מתאר כיצד תוכל לתרום לפרויקט.

## 📋 תוכן עניינים

- [קוד התנהגות](#קוד-התנהגות)
- [איך לתרום?](#איך-לתרום)
- [תהליך פיתוח](#תהליך-פיתוח)
- [הנחיות קוד](#הנחיות-קוד)
- [פתיחת Issues](#פתיחת-issues)
- [יצירת Pull Requests](#יצירת-pull-requests)

## 👥 קוד התנהגות

פרויקט זה מציית ל-[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). על ידי השתתפות, אתה מצפה לקוד התנהגות זה.

## 🚀 איך לתרום?

### דרכים לתרום

1. **🐛 דיווח על באגים** - פתח Issues לבעיות שזיהית
2. **💡 הצעת תכונות** - שתף רעיונות לשיפור
3. **📚 שיפור תיעוד** - עזור לנו לשפר את המדריכים
4. **💻 כתיבת קוד** - תיקן באגים או הוסף תכונות
5. **✅ ביקורת קוד** - בדוק Pull Requests של אחרים
6. **🌍 תרגום** - תרגם תיעוד לשפות אחרות

## 🔧 תהליך פיתוח

### 1️⃣ Fork והכנה

```bash
# Fork את הפרויקט ב-GitHub
# Clone המקומי
git clone https://github.com/[YOUR_USERNAME]/Diablo.git
cd Diablo

# הוסף remote של המקור
git remote add upstream https://github.com/Anlominus/Diablo.git
```

### 2️⃣ יצירת Branch

```bash
# צור branch חדש לתכונה/תיקון
git checkout -b feature/your-feature-name
# או
git checkout -b fix/your-bug-fix
```

### 3️⃣ כתיבת קוד

- עקוב אחר [הנחיות הקוד](#הנחיות-קוד)
- בדוק את הקוד שלך
- כתוב בדיקות אם רלוונטי

### 4️⃣ Commit

```bash
# עשה commit עם הודעה ברורה
git add .
git commit -m "feat: add new scanning feature"
# או
git commit -m "fix: resolve syntax error in menu loop"
```

**Conventional Commits:**
- `feat:` - תכונה חדשה
- `fix:` - תיקון באג
- `docs:` - שינוי תיעוד
- `style:` - שינוי פורמט
- `refactor:` - שינוי קוד ללא שינוי פונקציונליות
- `test:` - הוספת בדיקות
- `chore:` - משימות תחזוקה

### 5️⃣ Push ו-Pull Request

```bash
# Push את ה-branch שלך
git push origin feature/your-feature-name

# לאחר מכן פתח Pull Request ב-GitHub
```

## 💻 הנחיות קוד

### סגנון Bash

```bash
# ✅ טוב
function my_function() {
    local var_name="value"
    if [ condition ]; then
        echo "Success"
    fi
}

# ❌ לא טוב
my_function(){
local var=value
if [ condition ]
then
echo Success
fi
}
```

### כללים

1. **השתמש במיקרו מקומי** - `local` ל-variables פנימיים
2. **צבעים עקביים** - שימוש בפונקציית `DiabloColors()`
3. **הודעות ברורות** - הודעות שגיאה בעברית או אנגלית ברורה
4. **הערות קוד** - הסבר לוגיקה מורכבת
5. **זיהוי מערכת** - בדוק package manager נכון

### דוגמה מלאה

```bash
#!/bin/bash
# Name: Feature Name
# Description: What this feature does

###############################################
# Example function with best practices
###############################################
run_example_scan() {
    local target_ip="$1"
    
    # Check if target is provided
    if [ -z "$target_ip" ]; then
        echo "${BRed}[!]${Color_Off} Target IP is required"
        return 1
    fi
    
    echo "${BGreen}[+]${Color_Off} Running scan on $target_ip"
    # ... actual scan command
    
    return 0
}
```

## 🐛 פתיחת Issues

### דיווח על באגים

כאשר מדווחים על באג, כלול:

1. **תיאור** - מה הבעיה?
2. **שחזור** - צעדים לשחזור
3. **התנהגות צפויה** - מה היה אמור לקרות?
4. **התנהגות בפועל** - מה קרה בפועל?
5. **סביבה** - OS, גרסה, כלים מותקנים
6. **צילומי מסך** - אם רלוונטי

השתמש בתבנית [BUG_REPORT.md](.github/ISSUE_TEMPLATE/bug_report.md).

### בקשת תכונות

כאשר מבקשים תכונה:

1. **בעיה** - איזה בעיה זה פותר?
2. **פתרון** - מה אתה מציע?
3. **חלופות** - מה שקלת?
4. **דוגמאות** - דוגמאות מ-tools אחרים?

השתמש בתבנית [FEATURE_REQUEST.md](.github/ISSUE_TEMPLATE/feature_request.md).

## 🔄 יצירת Pull Requests

### הכנה

```bash
# ודא שאתה מעודכן עם main
git checkout main
git pull upstream main

# Merge את השינויים שלך
git checkout feature/your-feature-name
git rebase main  # או merge
```

### תיאור ה-PR

כתוב תיאור ברור הכולל:

1. **מה** - מה השינוי?
2. **למה** - למה זה נחוץ?
3. **איך** - איך זה עובד?
4. **בדיקות** - איך לבדוק?

השתמש בתבנית [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).

### ביקורת קוד

- נענה לפידבק במהירות
- ערוך על פי הערות המבקרים
- שאל אם משהו לא ברור

## 📝 שיפור תיעוד

עזרה בתיעוד מוערכת מאוד!

### קבצים רלוונטיים

- `README.md` - מסמך עיקרי
- `docs/` - כל התיעוד
- `CONTRIBUTING.md` - זה
- תגובות בקוד Bash

### טיפים

- השתמש בעברית או אנגלית ברורה
- כלול דוגמאות
- בדוק קישורים
- עקוב אחר פורמט Markdown

## ✅ בדיקות

לפני PR:

```bash
# בדיקת syntax
bash -n Diablo

# בדיקת styles
shellcheck Diablo

# ריץ manual tests
./Diablo
# נסה את התכונה החדשה
```

## 🏆 הכרה

תורמים פעילים יוכרו ב:
- `CONTRIBUTORS.md` (עתידי)
- Release notes
- README (אם רלוונטי)

## ❓ שאלות?

- פתח [Issue](https://github.com/Anlominus/Diablo/issues)
- ודא תבנית Issue מתאימה
- השתמש בתוויות נכונות

---

**תודה על התרומה שלך! יחד נבנה כלי PenTesting מעולה** 🚀

---

> בס״ד - מגדל בסייעתא דשמיא




### File: Diablo/SECURITY.md

# 🔐 Security Policy

## 🛡️ מדיניות אבטחה

### ⚠️ שימוש אתי וחוקי

**Diablo** מיועד רק לשימוש בבדיקות חדירה **מוסמכות ומאושרות בלבד**. שימוש בכלי זה במטרה לבצע פעילות בלתי חוקית או בלתי מוסמכת הוא אסור לחלוטין.

### ✅ יישומים מותרים
- בדיקות חדירה בהרשאה מראש
- סביבות בדיקה בבעלותך או בהרשאה מפורשת
- הערכת אבטחה של רשתות ותשתיות משלך
- מחקר ופיתוח בתחום אבטחת מידע

### ❌ יישומים אסורים
- חדירה לרשתות ללא הרשאה
- גישה למידע ללא רשות
- כל פעילות בלתי חוקית
- פגיעה בפרטיות או בנתונים

## 🚨 דיווח על פרצות אבטחה

אם מצאת בעיית אבטחה ב-Diablo עצמו:

### 📧 איך לדווח
1. **אל תפתח Issue ציבורי** מיד
2. שלח דוא"ל ל: **security@anlominus.github.io**
3. תאר את הבעיה בפירוט
4. נתונים מדויקים/צעדים לשחזור
5. הודע לפני פרסום ציבורי

### ⏱️ זמן תגובה
- **24 שעות** - אישור קבלת הדיווח
- **7 ימים** - הערכת חומרת הבעיה
- **30 ימים** - תיקון או תוכנית צעדים

### 🏆 הכרה
תורמים שמדווחים על בעיות אבטחה משמעותיות יוכרו (אם רצונם בכך) ב-CONTRIBUTORS.md.

## 🔒 אבטחה בקוד

### Best Practices
- ✅ בדיקות קוד אוטומטיות (CI/CD)
- ✅ סריקות אבטחה שבועיות
- ✅ עדכוני תלויות אוטומטיים
- ✅ ביקורת קוד בפני הציבור

### כלי אבטחה
- **Gitleaks** - סריקת סודות בקוד
- **ShellCheck** - בדיקות איכות Bash
- **Dependabot** - עדכוני תלויות

## ⚖️ אחריות משפטית

### שימוש זהירות
```
משתמשים ב-Diablo עושים זאת על אחריותם הבלעדית.
יוצרי הכלי לא יהיו אחראים לנזק או שימוש בלתי הולם בכלי.
```

### חוקים מקומיים
ודא שהשימוש שלך ב-Diablo תואם את:
- חוקי המדינה שלך
- תקנות הרגולציה המקומיות
- מדיניות הארגון שלך

## 🌍 קהילה

### סיוע ועדכונים
- 📖 עקוב אחר כל חידושי תיעוד
- 🔄 התקן גרסאות עדכניות
- 🤝 שתף ידע עם הקהילה (בזהירות)

### קוד התנהגות
אנא עקוב אחר [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

---

**נשארות לך שאלות?** שלח [Issue](https://github.com/Anlominus/Diablo/issues) עם תג "security".

**מדיניות זו מתעדכנת מעת לעת.** גרסה אחרונה: 2025




### File: Diablo/docs/ARCHITECTURE.md

> בס״ד

# 🏗️ Architecture

מסמך זה מתאר את הארכיטקטורה הכללית של Diablo ואת החלטות התכנון.

## 📐 סקירה כללית

Diablo הוא כלי PenTesting מבוסס Bash שמארגן תהליכי בדיקות חדירה בצורה מובנית ומפיקה דוחות מפורטים בפורמט Markdown.

## 🗂️ מבנה הקוד

```
Diablo/
├── Diablo                    # סקריפט ראשי
├── README.md                 # מסמך עיקרי
├── CONTRIBUTING.md           # מדריך תרומה
├── SECURITY.md               # מדיניות אבטחה
├── CODE_OF_CONDUCT.md        # קוד התנהגות
├── .github/                  # הגדרות GitHub
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                     # תיעוד
│   ├── INDEX.md
│   ├── GETTING_STARTED.md
│   └── ARCHITECTURE.md
└── assets/                   # משאבים
```

## 🔄 זרימת עבודה (Workflow)

### 1️⃣ אתחול (Initialization)
```
System Check → Package Manager Detection → Color Setup
```

### 2️⃣ תפריט ראשי (Main Menu)
```
Target Status Display → Menu Options → User Selection
```

### 3️⃣ תהליכי PenTest

#### Planning & Scoping
```
User Input → Target Variables → Report File Setup → File Header Creation
```

#### Reconnaissance
```
Individual Scan Tools → Output Capture → Markdown Report Append
```

## 🧩 רכיבים מרכזיים

### DiabloLogo1()
- תצוגת לוגו ASCII
- עיצוב חזותי

### DiabloColors()
- הגדרת צבעי טרמינל
- תמיכה בריבוי פלטפורמות

### TargetStatus()
- ניהול מצב יעד
- משתני יעד:
  - `targetIP`
  - `targetDns`
  - `targetNAME`
  - `targetEmail`
  - `targetPhone`

### MainMenu()
- לולאת תפריט ראשית
- רישות בקשות משתמש

### AnonMainMenu()
- תפריט אנונימיות
- ניהול anonsurf

## 🔧 כלי סריקה

### Network Analysis
- **arp** - טבלת ARP
- **traceroute** - מסלול IP
- **ping** - בדיקת שירותיות
- **masscan** - סריקת פורטים מהירה

### Port Scanning
- **nmap** - סריקת פורטים מפורטת
  ```
  nmap -sV -sC -O -p- $targetIP
  ```

### DNS Enumeration
- **dig** - בירורי DNS
- **nslookup** - בדיקות DNS
- **whois** - מידע WHOIS
- **dnsenum** - חילוץ תת-דומיינים
- **fierce** - סריקת DNS אגרסיבית
- **dnsrecon** - חקירת DNS מקיפה

### Web Enumeration
- **dirb** - גילוי דירקטוריות
  ```
  dirb http://$targetDNS
  ```
- **nikto** - סריקת אבטחת אתרים

### OSINT
- **enum4linux** - חילוץ מידע Windows/Samba

## 📊 מערכת דוחות

### פורמט דוח
```markdown
---
AnLoMinus Diablo PenTest Report [Project Name]
#### Date: [Timestamp]

---

# 📜 Menu
[a] - Anonymity Surfing
[1] - Planning and Scoping
[2] - Reconnaissance & Vulnerability Assessment
[3] - Gaining Access & Maintaining Access
[4] - Covering tracks
[5] - Analysis & Reporting

---

# [1] - Planning and Scoping
### Planning Log [Target IP]:

---

# [2] - Reconnaissance & Vulnerability Assessment
### [Scan Type] Scan Log [Target]:
[Scan Output]
```

## 🔐 מודל אבטחה

### הרשאות מערכת
- אין צורך בהרשאות root ברוב המקרים
- סריקות מסוימות עשויות לדרוש הרשאות מיוחדות

### ניהול נתונים רגישים
- לא נשמרים credentials
- נתונים רגישים רק בקובץ דוח מקומי

## 🚀 הרחבה עתידית

### תכונות מתוכננות
- [ ] Gaining Access & Maintaining Access
- [ ] Covering tracks
- [ ] Analysis & Reporting
- [ ] ממשק Web UI
- [ ] API לבדיקות אוטומטיות
- [ ] תמיכה ב-Containers

## 📝 Best Practices

### כתיבת קוד
- שימוש בצבעים עקביים
- הודעות שגיאה ברורות
- עיצוב ASCII מעוצב

### ביצועים
- סריקות מקבילות (עתידי)
- ניהול זיכרון יעיל
- הגבלת משאבי רשת

---

**מומלץ לקרוא:** [Security Model](./SECURITY_MODEL.md)




### File: Diablo/docs/BEST_PRACTICES.md

> בס״ד

# ⭐ Best Practices

מדריך שיטות עבודה מומלצות לשימוש יעיל ואתי ב-Diablo.

## 📋 תוכן עניינים

- [אתיקה ומשפטיות](#אתיקה-ומשפטיות)
- [תכנון וביצוע](#תכנון-וביצוע)
- [אבטחת מידע](#אבטחת-מידע)
- [תיעוד ודוחות](#תיעוד-ודוחות)
- [אופטימיזציה](#אופטימיזציה)

## ⚖️ אתיקה ומשפטיות

### רכישת הרשאות

#### לפני התחלה
✅ **הכרחי:**
- הרשאה בכתב מהבעלים
- תיאום מול צוות IT
- הסכם SOW (Statement of Work)
- הגדרת scope מדויק

❌ **אסור:**
- סריקות ללא הרשאה
- חריגה מ-scope
- גישה למידע לא רלוונטי

### דוגמאות להסכמים

```markdown
PenTest Agreement Example:
- Target: 192.168.1.0/24
- Scope: Web servers, API endpoints
- Excluded: Database servers, backup systems
- Duration: Oct 28 - Oct 30, 2025
- Team: AnLoMinus, 2 analysts
- Deliverable: Report by Nov 5
```

### הפרות אבטחה

```bash
# אם מוצאת בעיה בינונית/גבוהה:
1. תיעוד מיידי
2. דיווח ללקוח
3. בדיקת אם exploitation אפשרי
4. ניטור logs
```

## 🎯 תכנון וביצוע

### שלב התכנון

#### 1. Information Gathering
```bash
# לפני סריקות חזקות
./Diablo
[p] → Planning
# תעד:
# - IP ranges
# - Domains
# - Technologies
# - Business context
```

#### 2. Scope Definition
```yaml
In-Scope:
  - Web applications
  - API endpoints
  - Network infrastructure
  - End user systems

Out-of-Scope:
  - Social engineering
  - Physical security
  - Third-party services
  - Production databases
```

#### 3. Time Management
```
Day 1: Planning + Initial reconnaissance
Day 2: Network + Web scanning
Day 3: Vulnerability assessment + Exploitation testing
Day 4: Reporting + Review
```

### שלב הביצוע

#### סדר עדיפויות
```bash
# 1. Quick reconnaissance
ping + traceroute + basic nmap

# 2. Deep scanning
Full nmap + DNS enumeration

# 3. Service-specific
Web enumeration + API testing
```

#### ניהול זמן
```bash
# צור תיקיות לפי תאריך
mkdir -p 2025-10-28/{morning,afternoon,evening}

# כל 2 שעות
# [p] → New sub-project
# בהמשך: merge reports
```

## 🔐 אבטחת מידע

### נתונים רגישים

#### איך לזהות?
```bash
# בדוח Markdown
grep -i "password\|secret\|key\|token\|credential" \
  *.md

# הסר או השחלף
sed -i 's/password:.*/password: [REDACTED]/g' report.md
```

#### שמירה בטוחה
```bash
# הצפנה
gpg -c ClientWebsite-Diablo-Log.md
# Delete original
rm ClientWebsite-Diablo-Log.md

# או
# tar + encryption
tar czf - ClientWebsite-Diablo-Log.md | \
  gpg -c > report.tar.gz.gpg
```

### אבטחת תקשורת

```bash
# VPN + Diablo anonymity
./Diablo
[a] → [2]  # Start anonsurf

# או VPN נפרד
sudo openvpn client.ovpn
./Diablo
```

### הצפנת דוחות

```bash
# GPG Encryption
# Generate key if needed
gpg --generate-key

# Encrypt report
gpg --encrypt --recipient your@email.com \
  ClientWebsite-Diablo-Log.md

# Decrypt later
gpg --decrypt \
  ClientWebsite-Diablo-Log.md.gpg > report.md
```

## 📝 תיעוד ודוחות

### מבנה דוח אידיאלי

```markdown
# Executive Summary
- מה נבדק?
- תקציר ממצאים
- המלצות עיקריות

# Methodology
- כלים ותהליכים
- Scope מתואר

# Findings
- High/Medium/Low
- CVSS scores
- Proof of concept

# Recommendations
- תיקון קצר טווח
- שיפורי אבטחה
- בדיקות המשך

# Appendix
- Raw scan results
- Screenshots
- Logs
```

### כתיבה מקצועית

#### Do ✅
```markdown
Vulnerability: SQL Injection in Login Form
Severity: High (CVSS 8.5)
Impact: Full database compromise
Evidence: [screenshot]
Recommendation: Parameterized queries
```

#### Don't ❌
```markdown
This is broken and can be hacked!
```

### ויזואליזציה

```bash
# Charts from data
# Extract open ports
grep -E "^\d+/tcp" report.md | \
  awk '{print $3}' | sort | uniq -c | \
  sort -rn | head -10

# או Python + matplotlib
python3 visualize-port-data.py report.md
```

## ⚡ אופטימיזציה

### ביצועים

#### סריקות מקבילות
```bash
# בסיס: sequential
nmap target1; nmap target2

# מתקדם: parallel
nmap target1 &
nmap target2 &
wait
```

#### Rate Limiting
```bash
# להגנה על רשתות
nmap --max-rate 1000 target

# masscan
masscan target -p0-65535 --max-rate 500
```

### אוטומציה

#### סקריפטי wrapper
```bash
#!/bin/bash
# auto-pentest.sh

TARGETS=("192.168.1.1" "192.168.1.2")

for TARGET in "${TARGETS[@]}"; do
    echo "Scanning $TARGET..."
    nmap -sV $TARGET >> report.log
    sleep 60  # Rate limiting
done
```

#### Cron Jobs
```bash
# שבועי
0 2 * * 1 /path/to/weekly-scan.sh

# חשוב: רק עם הרשאה!
```

### ניהול משאבים

#### זיכרון
```bash
# Clean old reports
find ~/pentest-reports -mtime +90 -delete

# Compress
tar czf old-reports.tar.gz ~/old-reports/
```

#### דיסק
```bash
# Monitor space
df -h

# Clean logs
journalctl --vacuum-time=7d
```

## 🔄 תהליך איכות

### Review דוח

```bash
# Checklist
- [ ] כל ממצא מתועד
- [ ] CVSS scores מדויקים
- [ ] ללא נתונים רגישים
- [ ] המלצות מעשיות
- [ ] Executive summary ברור
```

### Peer Review

```bash
# לפני מסירה ללקוח
# 1. Self-review
# 2. Peer review
# 3. Manager sign-off
```

### עדכון כלים

```bash
# Weekly
sudo apt update && sudo apt upgrade

# Check CVE databases
# Update wordlists
```

## 📊 מטריקות

### מדידת הצלחה

```yaml
Metrics:
  Reconnaissance:
    - Targets discovered
    - Services identified
    - Technologies mapped
  
  Vulnerabilities:
    - Total findings
    - By severity
    - By category
  
  Remediation:
    - Acceptance rate
    - Time to fix
    - Re-scan results
```

## 🌍 סביבות

### Dev/Staging/Prod

```bash
# תמיד בדוק בסביבות נכונות
if [[ $TARGET == *"prod"* ]]; then
    echo "⚠️ Production target - extra caution!"
    read -p "Confirm: " confirm
fi
```

## 📚 משאבים

### למידה מתמשכת

- **OWASP** - מדריכי אבטחה
- **PTES** - Penetration Testing Execution Standard
- **NIST** - Cybersecurity Framework
- **Bug Bounty** platforms

### קהילה

- GitHub Discussions
- Reddit /r/netsec
- Information Security forums
- Local meetups

---

## 🎓 סיכום

✅ **תמיד:**
- קיבל הרשאה מראש
- תיעד הכל
- שמור מידע רגיש
- עבוד מובנה
- למד מתמיד

❌ **לעולם לא:**
- סריקות לא מורשות
- חסר מידע חשוב בדוחות
- חשוף מידע ללקוחות
- עבוד חסר סדר
- תמנע מלעדכן ידע

---

**זכור: PenTest הוא אחריות, לא רק תפקיד** ⚖️

> בס״ד - מגדל בסייעתא דשמיא




### File: Diablo/docs/FAQ.md

> בס״ד

# ❓ שאלות נפוצות (FAQ)

## 🤔 שאלות כלליות

### מה זה Diablo?
Diablo הוא כלי PenTesting ו-Hacking מדויק שמיועד לביצוע בדיקות חדירה מסודרות ויצירת דוחות מפורטים בפורמט Markdown.

### מי יכול להשתמש ב-Diablo?
כל אחד, אבל חשוב לזכור:
- ✅ השתמש רק על מטרות שרשת לצאת
- ✅ ציית לכל חוק מקומי
- ❌ אל תבצע התקפות בלתי חוקיות

### האם Diablo חינמי?
כן! Diablo הוא פרויקט Open Source תחת רישיון MIT.

## 🔧 שאלות טכניות

### באילו מערכות הפעלה Diablo עובד?
- Linux (Ubuntu, Debian, Kali Linux)
- macOS (10.14+)
- Termux (Android)

### אילו כלים נדרשים?
```bash
masscan, nmap, dig, nslookup, whois, nikto, enum4linux, dirb, anonsurf
```

### איך מתקינים את כל כלי התלויות?
**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install masscan nmap dnsutils whois nikto enum4linux dirb
```

**macOS:**
```bash
brew install masscan nmap
# יתר הכלים בדרך כלל מותקנים מראש
```

**Kali Linux:**
```bash
sudo apt-get update && sudo apt-get install -y masscan nmap dnsutils nikto dirb
```

### למה צריך תלות ב-HacKingPro?
קטע הקוד הבא:
```bash
. ../HacKingPro/HacKingPro-Parts/Main/HacKingPro-Planning
```
מנסה לטעון פונקציות מתוך פרויקט HacKingPro שקשור. אם אין לך את HacKingPro, תוכל להסיר או להחליף את השורה הזו.

## 🐛 פתרון בעיות

### "Permission denied"
```bash
chmod +x Diablo
./Diablo
```

### "command not found: masscan"
התקן את masscan:
```bash
# Ubuntu/Debian
sudo apt-get install masscan

# macOS
brew install masscan
```

### הסריקות לא רצות
וודא שהכתובת IP שלך נכונה ושהרשת זמינה:
```bash
ping [your-target-ip]
```

### הדוח לא נוצר
וודא שיש הרשאות כתיבה בתיקייה הנוכחית:
```bash
ls -la
mkdir -p reports
```

## 📊 שאלות על דוחות

### איפה נשמרים הדוחות?
בתיקייה שבה הפעלת את Diablo:
```
[Project-Name]-Diablo-Log.md
```

### מה הפורמט של הדוחות?
Markdown - ניתן לצפות בכל עורך טקסט או ב-GitHub.

### איך מייצאים לדוחות אחרים?
Diablo יוצר Markdown. תוכל להמיר ל-PDF, HTML וכדומה באמצעות כלים כמו:
- pandoc
- Markdown-to-PDF
- GitHub Pages

## 🔐 שאלות אבטחה

### האם Diablo אוסף נתונים?
לא. הכלי פועל באופן מקומי ולא שולח נתונים החוצה.

### האם אנונימי לי שישתמשו ב-Diablo לבדיקות שלי?
אם מישהו משתמש בכלי הזה לבדיקת הרשת שלך בלי הרשאה, זה בלתי חוקי. זה לא עובדה שמקורה ב-Diablo עצמו.

### איך משתמשים באנונימיות?
אם יש לך anonsurf:
```bash
./Diablo
# בחר [a] → Anonymity Surfing
# [2] - Anonimity Surfing start
```

## 🚀 תכונות

### מה זה "Planning and Scoping"?
זה שלב ההתחלה שבו מוגדרים מטרות הבדיקה, IP, שם פרויקט, domain וכו'.

### מה זה "Reconnaissance & Vulnerability Assessment"?
סריקות נרחבות לאיסוף מידע וזיהוי פגיעויות:
- חילוץ DNS
- סריקת פורטים
- סריקת שירותי Web
- חקירת רשת

### מתי יתווספו תכונות 3, 4, 5?
גישת Gaining Access, Covering tracks ו-Analysis & Reporting מוגדרות כעת כמקומות-מצייצים (placeholders) והן מתוכננות להתפתח בחליפות עתידיות.

## 🤝 תרומה

### איך תורמים?
ראה את [CONTRIBUTING.md](../CONTRIBUTING.md) לפרטים מלאים.

### איך מדווחים על באג?
פתח Issue חדש ב-GitHub עם תגיף "bug".

### איך מבקשים תכונה?
פתח Issue חדש עם תגיף "enhancement".

## 📞 קישורים והפניות

- GitHub: https://github.com/Anlominus/Diablo
- Issues: https://github.com/Anlominus/Diablo/issues
- Discussions: https://github.com/Anlominus/Diablo/discussions

---

**שאלות נוספות?** פתח Issue ב-GitHub!




### File: Diablo/docs/GETTING_STARTED.md

> בס״ד

# 🚀 Getting Started with Diablo

ברוכים הבאים ל-Diablo! מדריך זה יעזור לך להתחיל להשתמש בכלי PenTesting המדויק הזה תוך דקות.

## 📋 דרישות מוקדמות

### מערכת הפעלה נתמכת
- **Linux** (Ubuntu, Debian, Kali Linux, etc.)
- **macOS** (10.14+)
- **Termux** (Android)

### כלים נדרשים
```bash
# כלים בסיסיים
- masscan
- nmap
- dig, nslookup
- whois
- nikto
- enum4linux
- dirb
- anonsurf (לפונקציית אנונימיות)

# בחלק מהמערכות
- traceroute
- arp
- ping
```

## 🔧 התקנה מהירה

### Linux / macOS
```bash
# הורד את הקובץ
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo

# הפוך לקובץ הרצה
chmod +x Diablo

# הפעל
./Diablo
```

### Termux (Android)
```bash
# בטרמינל Termux
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo
chmod +x Diablo
./Diablo
```

## 🎯 שימוש בסיסי

### 1️⃣ הפעלה ראשונית
```bash
./Diablo
```

### 2️⃣ תכנון וטווח (Planning and Scoping)
בחר אפשרות `[p]` או `[P]` או הקלד `plan` בתפריט הראשי:
- הזן את כתובת ה-IP של המטרה
- הזן את שם הפרויקט
- הזן את ה-Domain של המטרה

### 3️⃣ הגדרת יעד (Target Setup)
התפריט יכין עבורך קובץ דוח Markdown:
```
${targetNAME}-Diablo-Log.md
```

### 4️⃣ ביצוע סריקות
בחר אפשרות `[2]` לביצוע Reconnaissance:
- Arp Scan
- TraceRoute Scan
- Ping Scan
- Nmap Scan
- Dig Scan
- Nslookup Scan
- WhoIs Scan
- Dirb Scan
- ועוד...

## 📊 דוגמאות שימוש

### דוגמה בסיסית
```bash
# הפעלת הכלי
./Diablo

# בתפריט:
# [p] → Planning and Scoping
# 1. הזן IP: 192.168.1.1
# 2. הזן שם פרויקט: TestProject
# 3. הזן Domain: example.com

# [2] → Reconnaissance & Vulnerability Assessment
# כל הסריקות יתבצעו וייכתבו ל-TestProject-Diablo-Log.md
```

## 🔐 אנונימיות

אם יש לך anonsurf מותקן, תוכל להשתמש בתכונות אנונימיות:
```bash
# בתפריט בחר [a]
[a] → Anonymity Surfing

# תפריט משני:
# [1] - Anonimity Surfing status
# [2] - Anonimity Surfing start
# [3] - Anonimity Surfing stop
```

## 📝 יצירת דוחות

לאחר כל סריקה, דוח מפורט נוצר בפורמט Markdown:
```markdown
# AnLoMinus Diablo PenTest Report TestProject
#### Date: [תאריך]

---

# [1] - Planning and Scoping
### Planning Log 192.168.1.1:

---

# [2] - Reconnaissance & Vulnerability Assessment
### masscan Scan Log 192.168.1.1:
### enum4linux Scan Log 192.168.1.1:
### nikto Scan Log 192.168.1.1:
### Arp Scan Log 192.168.1.1:
### ... ועוד
```

## ⚠️ שימוש אתי

**חשוב מאוד:**
- השתמש ב-Diablo רק בהרשאה מפורשת
- עבוד רק על מטרות שבבעלותך או שקיבלת הרשאה לבדוק
- שמור על כללי האתיקה והחוק המקומי

## 🆘 בעיות נפוצות

### בעיה: "command not found: masscan"
**פתרון:**
```bash
# Ubuntu/Debian
sudo apt-get install masscan

# macOS
brew install masscan

# Kali Linux (בדרך כלל מותקן מראש)
sudo apt-get update && sudo apt-get install masscan
```

### בעיה: "Permission denied"
**פתרון:**
```bash
chmod +x Diablo
```

### בעיה: תלות ב-HacKingPro
**פתרון:**
הכלי מנסה לטעון קובץ מ-HacKingPro. אם אין, ודא שהתיקייה הנכונה נמצאת בנתיב היחסי.

## 📚 המשך הלאה

עכשיו כשהכל עובד, תוכל לחקור:
- [📖 Usage Guide](./USAGE.md) - מדריך שימוש מתקדם
- [⭐ Features](./FEATURES.md) - כל התכונות
- [🔐 Best Practices](./BEST_PRACTICES.md) - שיטות עבודה מומלצות

---

**הערות:** אם נתקלת בבעיות, אנא דווח ב-[Issues](https://github.com/Anlominus/Diablo/issues)




### File: Diablo/docs/INDEX.md

> בס״ד

# 📚 Diablo Documentation

ברוכים הבאים לתיעוד המלא של **Diablo** - כלי PenTesting ו-Hacking מדויק וידידותי.

## 📖 תוכן עניינים

### 🚀 התחלה מהירה
- [Getting Started](./GETTING_STARTED.md) - כיצד להתחיל עם Diablo

### 🎯 שימוש
- [Usage Guide](./USAGE.md) - מדריך שימוש מפורט

### 🏗️ ארכיטקטורה
- [Architecture](./ARCHITECTURE.md) - מבנה הקוד והתכנון

### 🔐 אבטחה
- [Security Model](./SECURITY_MODEL.md) - מודל האבטחה
- [Best Practices](./BEST_PRACTICES.md) - שיטות עבודה מומלצות

### 🤝 תרומה
- [Contributing Guide](../CONTRIBUTING.md) - כיצד לתרום לפרויקט

### 📝 מידע נוסף
- [FAQ](./FAQ.md) - שאלות נפוצות

---

**תאריך עדכון אחרון:** {{ date }}




### File: Diablo/docs/ROADMAP_NEXT_STEPS.md

# 🌟 המשך Roadmap

מסמך זה מפורט את הצעדים המעשיים להשלמת המשימות שבסטטוס "בפיתוח" ב־Roadmap הראשי.

## 🔐 Gaining Access & Maintaining Access
- [ ] הוספת מודולי ניצול נפוצים (SMB, SSH, RDP, Web) עם תרחישי הפעלה מודולריים.
- [ ] שילוב כלים מוכנים (metasploit, hydra, medusa) בממשק התפריט, כולל תצורות ברירת מחדל בטוחות.
- [ ] רישום לוגים מפורט (קלט/פלט) בכל הרצה לתמיכה ב־post-mortem ו־evidence collection.
- [ ] מעטפת rollback שמחזירה קבצי קונפיגורציה למצב מקורי לאחר הפעלה.

## 🧹 Covering Tracks
- [ ] פקודות לניקוי לוגים לפי מערכת (Debian/RHEL/macOS/Termux) תוך שמירה על auditing סטנדרטי.
- [ ] רוטינת "dry-run" שמדגימה מה ינוקה לפני מחיקה בפועל.
- [ ] אינטגרציית Tor/Proxy מובנית לכלי כיסוי עקבות ברשת.
- [ ] הוספת תיעוד אזהרות שימוש אתי והגבלת זמינות הפיצ'רים למצב "lab" בלבד.

## 📑 Analysis & Reporting
- [ ] מחולל דוחות Markdown/PDF עם טמפלייטים ל־Executive Summary, טבלאות CVSS, ו־Appendix טכני.
- [ ] יצוא תוצאות סריקה (nmap/masscan/nikto) לפורמט JSON כדי להזינם למחולל הדוחות.
- [ ] תיוג ממצאים אוטומטי לפי CWE/OWASP Top 10.
- [ ] הוספת צ'קליסט "Validation" לקראת שליחה ללקוח.

## 🔧 תיקון תלות ב־HacKingPro
- [ ] ניתוק הקריאות ל־HacKingPro בלוגיקת האתחול והחלפתן במודולים מקומיים.
- [ ] הוספת בדיקות smoke (bash) שמוודאות שכל תפריט נטען גם ללא HacKingPro מותקן.
- [ ] ניהול גרסאות עם fallback: במקרה שתלות חיצונית חסרה, הצגת אזהרה ופעולה חלופית.
- [ ] הפיכת כל קבצי העזר ל־vendored בתוך המאגר למניעת שבירות עתידיות.

## 🌐 ממשק Web UI
- [ ] קביעת ארכיטקטורה (backend bash wrapper או שרת קליל ב־Python) שמריץ את הסקריפטים הקיימים.
- [ ] מסכים ראשונים: Dashboard להרצות, הצגת לוגים בזמן אמת, וטופס להוספת יעדים.
- [ ] חיבור למנוע הדיווח כדי להוריד דוחות שנוצרו מתוך ה־UI.
- [ ] שכבת הרשאות בסיסית (token או Basic Auth) כדי למנוע שימוש לא מורשה.

---

## ✅ צעדים מהירים להתחלה
1. לדרג עדיפויות בין הפרקים לפי שיקולי אבטחה/ערך ללקוח.
2. לפתוח issues לכל סעיף משנה ולחברם ל־milestone "Roadmap - In Progress".
3. להריץ POC קצר לכל מודול חדש במעבדת בדיקה לפני שילוב לתפריט הראשי.



### File: Diablo/docs/SECURITY_MODEL.md

> בס״ד

# 🔐 Security Model

מסמך זה מתאר את מודל האבטחה של Diablo ואת ההתחשבויות האבטחתיות בעת שימוש בכלי.

## 📋 תוכן עניינים

- [מודל האמון](#מודל-האמון)
- [הרשאות מערכת](#הרשאות-מערכת)
- [פרטיות ומניעת חשיפה](#פרטיות-ומניעת-חשיפה)
- [אבטחת תקשורת](#אבטחת-תקשורת)
- [ניהול נתונים](#ניהול-נתונים)
- [אחריות משתמש](#אחריות-משתמש)

## 🤝 מודל האמון

### דגם ארכיטקטוני

```
┌─────────────────────────────────────┐
│         User (Pentester)             │
│                                      │
│         ./Diablo Script              │
│         (Local execution)            │
└───────────────┬──────────────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼──────┐  ┌──────▼────────┐
│ PenTesting   │  │  Local File   │
│  Tools       │  │  System       │
│  (nmap, etc) │  │               │
└──────────────┘  └───────────────┘
```

### הנחות אמון

#### ✅ נאמן לחלוטין
- **הקוד המקורי:** Repository זה
- **מקורות:** GitHub.com/Anlominus/Diablo

#### ⚠️ דורש בדיקה
- **כלי PenTest:** nmap, masscan, dirb ועוד
- **תלות חיצונית:** HacKingPro (אם קיים)
- **Package Managers:** apt, brew, pkg

### Threat Model

#### התקפות פוטנציאליות

```yaml
Threats:
  Supply_Chain:
    - Modified repository clone
    - Trojaned tools
    - Backdoored packages
    
  Execution:
    - Privilege escalation
    - Data leakage
    - Resource exhaustion
    
  Data:
    - Unauthorized access
    - Log exposure
    - Credential theft
```

## 🔑 הרשאות מערכת

### דרישות הרשאה

#### רגיל
```bash
# רוב הפונקציות
./Diablo  # No sudo needed
nmap -sV target  # Normal scan
```

#### מיוחד
```bash
# חלק מהסריקות
sudo nmap -sS target  # SYN scan
sudo masscan target  # Raw sockets
```

### עקרון Least Privilege

```bash
# ✅ נכון
sudo nmap -sV target

# ❌ לא נכון
sudo su
# ... הכל בתור root
```

## 🔒 פרטיות ומניעת חשיפה

### נתונים רגישים

#### מיושמים בכיף

```yaml
What_Diablo_Collects:
  - Target IP addresses
  - Scan results
  - Network topology
  - Service banners
  
What_Diablo_Does_NOT:
  - User credentials
  - Personal data
  - Credit cards
  - Internal communications
```

#### ניהול וחסימה

```markdown
# בדיוק כמו ב-Best Practices
- גילוי מיידי
- השחרה/מיון
- שמירה מוצפנת
- מחיקה בתום תקופה
```

### Logging & Tracing

```bash
# Diablo לא שולח נתונים חיצוניים
# כל העיבוד מקומי
```

## 📡 אבטחת תקשורת

### רשת

#### כמויות שמשתמשות

```bash
# DDoS protection
nmap --max-rate 1000 target  # Limit packets/sec
```

#### Anonymity

```bash
# עקב after check-anonsurf
./Diablo → [a] → [2]  # Start anonsurf
```

### VPN ו-NAT

```bash
# למקרה של proxy/VPN
# Diablo לא משנה הגדרות רשת
# כל כלי ש"נקרא" צריך הגדרת proxy משלו
```

## 💾 ניהול נתונים

### שמירה

```
┌──────────────────────────────────┐
│  ClientWebsite-Diablo-Log.md      │
│  (Unencrypted by default)        │
└──────────────────────────────────┘

אחריות המשתמש להצפין במידת הצורך
```

### מחיקה

```bash
# Cleanup scripts
find ~/pentest-reports -mtime +90 -delete
```

### גיבוי

```bash
# Secure backup
tar czf - *.md | gpg -c > backup.tar.gz.gpg
```

## ⚖️ אחריות משתמש

### חובות

```yaml
User_Responsibility:
  Legal:
    - Obtain written authorization
    - Comply with local laws
    - Respect scope boundaries
    
  Ethical:
    - No unauthorized testing
    - Responsible disclosure
    - Protect sensitive data
    
  Technical:
    - Verify tool sources
    - Keep tools updated
    - Secure generated reports
```

### מגבלות

```yaml
Limitations:
  Software:
    - Diablo is tool agnostic
    - No input validation for targets
    - No built-in encryption
    
  Legal:
    - No warranties
    - Use at own risk
    - Author not liable for misuse
```

## 🔐 Best Security Practices

### התקנה

```bash
# Verify checksums
wget https://github.com/Anlominus/Diablo/releases/download/v1.0.0/Diablo
wget https://github.com/Anlominus/Diablo/releases/download/v1.0.0/checksums.txt

# Verify
sha256sum -c checksums.txt
```

### שימוש יומיומי

```bash
# 1. Check integrity
git clone https://github.com/Anlominus/Diablo.git
cd Diablo
git verify-commit HEAD

# 2. Review before use
head -50 Diablo  # Quick review

# 3. Use safely
./Diablo  # With authorization only
```

### תחזוקה

```bash
# Weekly updates
cd Diablo
git pull origin main

# Tool updates
sudo apt update && sudo apt upgrade
```

## 🚨 Incident Response

### אם מופיעה בעיה באבטחה

```bash
1. Stop using Diablo immediately
2. Isolate affected systems
3. Check GitHub Issues for known problems
4. Report to security@anlominus.github.io
5. Review recent changes
```

### Recovery

```bash
# Clean system
rm -rf /path/to/Diablo

# Reinstall from verified source
wget https://raw.githubusercontent.com/Anlominus/Diablo/main/Diablo
chmod +x Diablo
```

## 📊 Security Metrics

### Tracking

```yaml
Metrics:
  Vulnerability_Reports: 0
  Security_Incidents: 0
  Code_Reviews: Monthly
  Dependency_Updates: Automated
```

### Compliance

```yaml
Standards:
  - OWASP ASVS
  - ISO 27001 (tool usage)
  - NIST Cybersecurity Framework
  - PenTest guidelines
```

## 🔗 References

- [SECURITY.md](../SECURITY.md) - Security policy
- [README.md](../README.md) - Main documentation
- [Best Practices](./BEST_PRACTICES.md) - Usage guidelines

---

## ✅ Checklist

לפני שימוש ב-Diablo:

- [ ] קראתי SECURITY.md
- [ ] הבנתי את מודל האמון
- [ ] יש לי הרשאה מפורשת
- [ ] כלי PenTest מקוריים
- [ ] תיקנתי את סביבתי
- [ ] יש לי backup strategy
- [ ] אני מבין את הסיכונים

---

**אבטחה היא תהליך, לא תוצאה** 🔐

> בס״ד - מגדל בסייעתא דשמיא




### File: Diablo/docs/USAGE.md

> בס״ד

# 📖 Usage Guide

מדריך שימוש מפורט לכל התכונות של Diablo.

## 🎯 תוכן עניינים

- [תפריט ראשי](#תפריט-ראשי)
- [Planning and Scoping](#planning-and-scoping)
- [Reconnaissance](#reconnaissance)
- [Anonymity Surfing](#anonymity-surfing)
- [דוחות](#דוחות)
- [טיפים מתקדמים](#טיפים-מתקדמים)

## 📜 תפריט ראשי

לאחר הפעלת `./Diablo`, תראה תפריט עם האפשרויות הבאות:

```
┌──[ AnLoMinus 👽 Diablo $~]
└──╼

[#] 📜 Menu

[#] 📜 Target IP: 
[#] 📜 Target Project Name: 
[#] 📜 Target Domain Name: 

[a] - Anonymity Surfing
[1] - Planning and Scoping
[2] - Reconnaissance & Vulnerability Assessment
[3] - Gaining Access & Maintaining Access
[4] - Covering tracks
[5] - Analysis & Reporting

[x] - Exit / Quit / Close
```

## 🎯 Planning and Scoping

### אתחול פרויקט חדש

בחר `[p]` או `[P]` או הקלד `plan`:

```bash
./Diablo
# בתפריט בחר: p
```

### הגדרת מטרה

תתבקש להזין:
1. **Target IP** - כתובת IP של המטרה
2. **Project Name** - שם הפרויקט/דוח
3. **Domain Name** - Domain (אם רלוונטי)

דוגמה:
```
Target IP: 192.168.1.100
Project Name: ClientWebsite
Domain: client.example.com
```

### יצירת דוח

לאחר הגדרת הפרמטרים, נוצר קובץ דוח:
```
ClientWebsite-Diablo-Log.md
```

## 🔍 Reconnaissance & Vulnerability Assessment

לאחר הגדרת מטרה, בחר `[2]` לתחילת סריקות.

### Network Analysis

#### Arp Scan
```bash
arp -an
```
- טבלת ARP מקומית

#### Traceroute
```bash
traceroute 192.168.1.100
```
- מסלול IP
- זיהוי נתבים

#### Ping
```bash
ping 192.168.1.100 -c4
```
- בדיקת שירותיות
- זיהוי latency

#### Masscan
```bash
masscan 192.168.1.100 -p0-65535 --max-rate 1000
```
- סריקת פורטים מהירה
- נוח למטרות גדולות

### Port Scanning

#### Nmap Full Scan
```bash
nmap -sV -sC -O -p- 192.168.1.100
```
- זיהוי שירותים וגרסאות
- בדיקות אבטחה בסיסיות
- זיהוי OS

### DNS Enumeration

#### Basic DNS
```bash
dig 192.168.1.100 all
nslookup 192.168.1.100
whois 192.168.1.100
```

#### Advanced DNS
```bash
dnsenum client.example.com
fierce --domain client.example.com
dnsrecon -d client.example.com
```
- חילוץ תת-דומיינים
- חקירת DNS מקיפה

### Web Enumeration

#### Dirb
```bash
dirb http://client.example.com
```
- גילוי דירקטוריות
- מציאת קבצים חשופים

#### Nikto
```bash
nikto -h 192.168.1.100
```
- סריקת אבטחת אתרים
- זיהוי פגיעויות ידועות

#### Enum4linux
```bash
enum4linux 192.168.1.100
```
- חקירת Windows/Samba
- חילוץ משתמשים, shares

## 🔐 Anonymity Surfing

לחיפוי זהות בעת סריקה.

### תפריט אנונימיות

בחר `[a]` בתפריט הראשי:

```
[#] 📜 Anonimity Surfing Menu

[1] - Anonimity Surfing status
[2] - Anonimity Surfing start
[3] - Anonimity Surfing stop

[#] 📜 Network Manager Menu

[4] - ifconfig -a
[5] - ip a

[x] - Exit / Quit / Close
```

### שימוש

```bash
[a] → [2]  # Start anonsurf
# ...בצע סריקות...
[a] → [3]  # Stop anonsurf
```

## 📊 דוחות

### מבנה דוח

כל הדוחות נוצרים בפורמט Markdown:

```markdown
---
AnLoMinus Diablo PenTest Report ClientWebsite
#### Date: Mon Oct 28 22:37:00 IST 2025

---

# 📜 Menu

[a] - Anonymity Surfing
[1] - Planning and Scoping
[2] - Reconnaissance & Vulnerability Assessment
[3] - Gaining Access & Maintaining Access
[4] - Covering tracks
[5] - Analysis & Reporting

---

# [1] - Planning and Scoping
### Planning Log 192.168.1.100:

---

# [2] - Reconnaissance & Vulnerability Assessment
### masscan Scan Log 192.168.1.100:
[scan output]

### nmap Scan Log 192.168.1.100:
[scan output]
```

### עיבוד דוחות

#### המרה ל-PDF
```bash
# עם pandoc
pandoc ClientWebsite-Diablo-Log.md -o ClientWebsite-Report.pdf

# או GitHub Flavored Markdown
# העלה ל-GitHub וצפה
```

#### עיבוד נוסף
```bash
# צירוף דוחות
cat *-Diablo-Log.md > Combined-Report.md

# חיפוש מידע רגיש
grep -i "password\|secret\|key" *-Diablo-Log.md
```

## 💡 טיפים מתקדמים

### עבודה עם מטרות מרובות

```bash
# תיקייה ייעודית לכל פרויקט
mkdir -p ~/pentest-reports
cd ~/pentest-reports

# הפעל Diablo
./Diablo
# [p] → define project → perform scans
```

### אוטומציה חלקית

```bash
#!/bin/bash
# quick-scan.sh

echo "Target IP?"
read TARGET

# Edit Diablo script temporarily
# Or use expect for automation
```

### אינטגרציה עם כלים אחרים

#### Burp Suite
```bash
# Export targets from Diablo report
grep -E "^http://\|^https://" ClientWebsite-Diablo-Log.md > targets.txt

# Import to Burp
```

#### Metasploit
```bash
# Find vulnerabilities
grep -i "vulnerability\|CVE" ClientWebsite-Diablo-Log.md
```

### סקריפטים מותאמים

#### סריקה קלה
```bash
# light-scan.sh
echo "Target?"
read TARGET
echo "Running light scan on $TARGET..."
nmap -sV -p 80,443,22,21 $TARGET
dig $TARGET all
```

#### סריקה עמוקה
```bash
# deep-scan.sh
# הפעל את כל הבדיקות ב-Diablo
# תהליך ארוך אבל מקיף
```

## ⚠️ מומלץ לזכור

### לפני סריקה
- ✅ קבל הרשאה מפורשת
- ✅ ודא שהמטרה שייכת לך/לקוח
- ✅ הגדר שעוני timeout
- ✅ בדוק תצורת Firewall

### במהלך סריקה
- ⏱️ תיזמם נכון - חלק מהסריקות ארוכות
- 📊 שמור פלט ביניים
- ⚠️ היזהר משימוש במשאבים

### אחרי סריקה
- 📝 סקור את הדוח
- 🔒 החסר מידע רגיש
- 📤 שתף רק עם מי שצריך
- 🗑️ הסר דוחות ישנים

## 🆘 פתרון בעיות

### סריקות לא פועלות
```bash
# בדוק כלים מותקנים
which nmap dig masscan

# בדוק הרשאות
sudo nmap -sV target

# בדוק רשת
ping target
```

### דוח גדול מדי
```bash
# סריקות בסיסיות בלבד
# סנן output
nmap target 2>&1 | grep -v "Nmap scan report"
```

### עדכון כלים
```bash
# Kali Linux
sudo apt update && sudo apt upgrade -y

# macOS
brew update && brew upgrade
```

## 📚 משאבים נוספים

- [Getting Started](./GETTING_STARTED.md)
- [Architecture](./ARCHITECTURE.md)
- [FAQ](./FAQ.md)
- [Best Practices](./BEST_PRACTICES.md)

---

**שימוש באחריות ועשייה קודשת** 🔐


