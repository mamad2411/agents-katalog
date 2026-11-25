# Email & Report Canvas Builders from GitHub

**Skill Name:** email-canvas-github-builders  
**Type:** Canvas Designer | Drag-Drop Builder | GitHub Reference  
**Version:** 1.0  
**Updated:** 2026-08-23  

---

## 📋 Description

Comprehensive reference skill for building email templates & manufacturing reports using top open-source canvas designers from GitHub. Includes 5 popular projects with detailed setup, feature comparison, and Samsung manufacturing-specific implementations.

**Use this skill when:**
- Need to select canvas email/report builder for your project
- Want to implement drag-drop email composer
- Building manufacturing report designer
- Need GitHub reference with code examples
- Comparing open-source builder frameworks
- Integrating with FastAPI backend
- Customizing blocks for Samsung reports

---

## 🏆 TOP 5 GitHub Projects

### **1. GrapesJS** ⭐⭐⭐ (25,800+ stars)
**GitHub:** https://github.com/grapesjs/grapesjs  
**Website:** https://grapesjs.com  
**License:** BSD 2-Clause  

**Best For:** Full-featured email + reports + landing pages

```javascript
// Installation
npm install grapesjs grapesjs-plugin-email

// Basic Setup
import grapesjs from 'grapesjs';
import gjsEmailPlugin from 'grapesjs-plugin-email';

const editor = grapesjs.init({
  container: '#gjs',
  height: '100%',
  width: '100%',
  plugins: [gjsEmailPlugin],
  pluginsOpts: {
    [gjsEmailPlugin]: {}
  }
});

// Export HTML
const html = editor.getHtml();
const css = editor.getCss();

// Custom Block - Production Metrics
editor.BlockManager.add('production-metrics', {
  label: 'Production Metrics',
  content: {
    type: 'production-metrics'
  }
});

editor.DomComponents.addType('production-metrics', {
  isComponent: el => el.getAttribute?.('class') === 'metrics-block',
  model: {
    defaults: {
      tagName: 'div',
      attributes: { class: 'metrics-block' },
      traits: [
        { name: 'rate', label: 'Production Rate (%)', value: '98.5' },
        { name: 'units', label: 'Units Produced', value: '2,450' },
        { name: 'defects', label: 'Defects', value: '12' }
      ]
    }
  },
  view: {
    onRender() {
      const model = this.model;
      const data = model.getAttributes();
      this.el.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
          <div style="padding: 12px; background: #d4edda; border-radius: 6px; text-align: center;">
            <div style="font-size: 22px; font-weight: 600;">${data.rate}%</div>
            <div style="font-size: 12px;">Production Rate</div>
          </div>
          <div style="padding: 12px; background: #cce5ff; border-radius: 6px; text-align: center;">
            <div style="font-size: 22px; font-weight: 600;">${data.units}</div>
            <div style="font-size: 12px;">Units</div>
          </div>
          <div style="padding: 12px; background: #fff3cd; border-radius: 6px; text-align: center;">
            <div style="font-size: 22px; font-weight: 600;">${data.defects}</div>
            <div style="font-size: 12px;">Defects</div>
          </div>
        </div>
      `;
    }
  }
});

// React Integration
import React, { useEffect, useRef } from 'react';

export function GrapesJSEditor() {
  const editorContainer = useRef(null);
  const editorRef = useRef(null);

  useEffect(() => {
    editorRef.current = grapesjs.init({
      container: editorContainer.current,
      height: '100vh',
      width: '100%',
      plugins: [gjsEmailPlugin]
    });

    return () => editorRef.current?.destroy();
  }, []);

  return <div ref={editorContainer} />;
}
```

**Pros:**
- ✅ Most powerful (25.8k stars)
- ✅ Email + Reports + Landing Pages
- ✅ Custom block system
- ✅ Plugin ecosystem
- ✅ White-label capable
- ✅ Large community

**Cons:**
- ❌ Learning curve (medium)
- ❌ Setup more complex
- ❌ More dependencies

**Setup Time:** 2-4 hours

---

### **2. react-email-editor** ⭐⭐⭐ (5,100+ stars)
**GitHub:** https://github.com/unlayer/react-email-editor  
**Website:** https://www.unlayer.com  
**License:** Proprietary (React component open)  

**Best For:** Production-ready React email component

```javascript
// Installation
npm install react-email-editor

// React Component
import React, { useRef } from 'react';
import { EmailEditor } from 'react-email-editor';

export default function EmailComposer() {
  const editorRef = useRef();

  const exportHTML = () => {
    editorRef.current.exportHtml((data) => {
      const { html, design } = data;
      console.log('HTML:', html);
      console.log('Design:', design);
      
      // Send to backend
      fetch('/api/email/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ html, design })
      });
    });
  };

  const exportJSON = () => {
    editorRef.current.exportJson((data) => {
      console.log(data);
    });
  };

  return (
    <div>
      <button onClick={exportHTML}>Export HTML</button>
      <button onClick={exportJSON}>Export JSON</button>
      <EmailEditor ref={editorRef} />
    </div>
  );
}

// With Options
<EmailEditor
  ref={editorRef}
  options={{
    features: {
      preview: true,
      colorPicker: true,
      fontSize: true,
      fontFamily: true
    }
  }}
/>
```

**Pros:**
- ✅ Production-ready
- ✅ Single React component
- ✅ Easy integration
- ✅ Good documentation
- ✅ Maintained (Unlayer)
- ✅ Fast setup (30 mins)

**Cons:**
- ❌ Email-focused only
- ❌ Limited customization
- ❌ No open plugin system
- ❌ Freemium model

**Setup Time:** 30 minutes

---

### **3. EmailBuilder.js** ⭐⭐⭐ (1,700+ stars)
**GitHub:** https://github.com/usewaypoint/email-builder-js  
**Website:** https://emailbuilderjs.com  
**License:** MIT  

**Best For:** Lightweight, zero-dependency builder

```javascript
// Installation
git clone https://github.com/usewaypoint/email-builder-js.git
npm install

// Basic Usage
import { renderToStaticMarkup } from '@usewaypoint/email-builder-parser';

const designJson = {
  root: {
    type: 'EmailLayout',
    data: { fontSize: 16, fontFamily: 'Arial' },
    children: ['block-1']
  },
  'block-1': {
    type: 'Text',
    data: { value: 'Hello World' }
  }
};

// Render to HTML
const html = renderToStaticMarkup(designJson);

// React Component
import { EmailEditor } from '@usewaypoint/email-editor-react';

export function MyEditor() {
  const [design, setDesign] = React.useState(defaultDesign);

  return (
    <EmailEditor
      design={design}
      onDesignChange={setDesign}
      onExport={() => {
        const html = renderToStaticMarkup(design);
        console.log(html);
      }}
    />
  );
}

// Playground
// https://usewaypoint.github.io/email-builder-js/

// Save to PostgreSQL
async function saveTemplate(design) {
  const response = await fetch('/api/templates', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'template-1',
      design_json: design,
      html_output: renderToStaticMarkup(design)
    })
  });
  return response.json();
}
```

**Pros:**
- ✅ Zero dependencies
- ✅ MIT license (true open-source)
- ✅ Lightweight (~80KB)
- ✅ Clean JSON output
- ✅ Offline support
- ✅ Easy customization

**Cons:**
- ❌ Smaller community (1.7k stars)
- ❌ Fewer built-in blocks
- ❌ Limited documentation
- ❌ Newer project

**Setup Time:** 1 hour

---

### **4. Easy Email** ⭐⭐⭐ (2,400+ stars)
**GitHub:** https://github.com/easy-email-com/easy-email  
**Website:** https://easy-email.com  
**License:** MIT  

**Best For:** MJML support + feature-rich

```bash
# Installation
git clone https://github.com/easy-email-com/easy-email.git
npm install

# Development
npm run dev
# http://localhost:8001

# Build
npm run build
```

**Features:**
- ✅ MJML rendering
- ✅ Responsive design
- ✅ Dark mode preview
- ✅ Rich component library
- ✅ TypeScript support
- ✅ Template library

**Pros:**
- ✅ MJML support
- ✅ Feature-rich
- ✅ Responsive emails
- ✅ Good community

**Cons:**
- ❌ More dependencies
- ❌ Larger bundle

**Setup Time:** 1-2 hours

---

### **5. SendWithSES Drag-and-Drop Designer** ⭐⭐ (1,000+ stars)
**GitHub:** https://github.com/SendWithSES/Drag-and-Drop-Email-Designer  
**Website:** https://designer.sendune.com  
**License:** MIT  

**Best For:** Angular + production testing

```bash
# Installation
git clone https://github.com/SendWithSES/Drag-and-Drop-Email-Designer.git
npm install

# Run
npm start
# http://localhost:4200

# Features
# - HTML code editor
# - Drag-drop canvas
# - Test email send
# - Cloud storage (S3, GCP)
# - Plain text emails
```

**Pros:**
- ✅ Angular native
- ✅ Live demo: https://designer.sendune.com
- ✅ Code editor view
- ✅ Cloud storage support

**Cons:**
- ❌ Angular-only
- ❌ Smaller community

**Setup Time:** 1-2 hours

---

## 📊 Feature Comparison Table

| Feature | GrapesJS | react-email-editor | EmailBuilder.js | Easy Email | SendWithSES |
|---------|----------|------------------|-----------------|-----------|------------|
| **⭐ Stars** | 25,800 | 5,100 | 1,700 | 2,400 | 1,000 |
| **📧 Email** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **📊 Reports** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **🌐 Landing Page** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **💻 Framework** | Vanilla JS | React | React | React | Angular |
| **🔷 TypeScript** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **📦 Dependencies** | Moderate | 0 | 0 | Moderate | Moderate |
| **📦 Bundle Size** | ~200KB | ~100KB | ~80KB | ~150KB | ~180KB |
| **🎨 Custom Blocks** | ✅ Easy | ⚠️ Hard | ✅ Easy | ✅ Easy | ✅ Easy |
| **🔌 Plugin System** | ✅ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| **🏷️ White-Label** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **📤 Export JSON** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **📤 Export HTML** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **📤 Export MJML** | ⚠️ | ❌ | ❌ | ✅ | ❌ |
| **⏱️ Setup Time** | 2-4h | 30m | 1h | 1-2h | 1-2h |
| **📚 Learning Curve** | Medium | Easy | Easy | Easy | Easy |
| **💰 Free** | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| **☁️ SaaS** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **🔒 No Vendor Lock** | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## 🎯 Decision Guide for Samsung Manufacturing

### **Scenario 1: Email + Reports + Custom Blocks**
```
Requirements:
✓ Email templates
✓ Manufacturing reports (Production, Defect, PLC)
✓ Custom blocks
✓ Full control
✓ Self-hosted

→ BEST: GrapesJS (25.8k stars)
```

**Setup:**
```bash
git clone https://github.com/grapesjs/grapesjs.git
npm install grapesjs grapesjs-plugin-email
npm run dev
```

---

### **Scenario 2: Quick Email Designer**
```
Requirements:
✓ Email only
✓ Fast setup (< 1 hour)
✓ Production-ready
✓ React component

→ BEST: react-email-editor (5.1k stars)
```

**Setup:**
```bash
npx create-react-app email-designer
npm install react-email-editor
# Use <EmailEditor> component
```

---

### **Scenario 3: Lightweight + Self-Hosted**
```
Requirements:
✓ Email templates
✓ Zero dependencies
✓ PostgreSQL integration
✓ Custom implementation

→ BEST: EmailBuilder.js (1.7k stars)
```

**Setup:**
```bash
git clone https://github.com/usewaypoint/email-builder-js.git
npm install
cd packages/editor-sample
npm run dev
```

---

### **Scenario 4: Responsive + MJML**
```
Requirements:
✓ MJML support
✓ Responsive design
✓ Component library

→ BEST: Easy Email (2.4k stars)
```

---

### **Scenario 5: Angular Integration**
```
Requirements:
✓ Angular app
✓ Drag-drop builder
✓ Live preview

→ BEST: SendWithSES (1k stars)
```

---

## 💡 RECOMMENDED FOR SAMSUNG

### **Option A: Full Solution (Recommended)**

```
┌─────────────────────────────────────┐
│  Frontend: Hybrid Approach          │
├─────────────────────────────────────┤
│                                     │
│  Email Templates:                   │
│  → react-email-editor (5.1k ⭐)   │
│    Fast, production-ready          │
│                                     │
│  Complex Reports:                   │
│  → GrapesJS (25.8k ⭐)            │
│    Full-featured, custom blocks    │
│                                     │
└─────────────────────────────────────┘
         ↓ (Export JSON/HTML)
┌─────────────────────────────────────┐
│  Backend: FastAPI + PostgreSQL      │
├─────────────────────────────────────┤
│  - Save templates (JSON)            │
│  - Render to HTML                   │
│  - SMTP sending                     │
│  - Schedule reports                 │
│  - Track metrics                    │
└─────────────────────────────────────┘
```

### **Option B: Lightweight Solution**

```
┌─────────────────────────────────────┐
│  Frontend: EmailBuilder.js          │
│           (1.7k ⭐)                │
├─────────────────────────────────────┤
│  - Drag-drop designer               │
│  - Zero dependencies                │
│  - Clean JSON output                │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Backend: FastAPI + PostgreSQL      │
│  (Minimal, self-hosted)             │
└─────────────────────────────────────┘
```

---

## 🔧 Integration with FastAPI Backend

### **Save Template Endpoint**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()

class TemplateRequest(BaseModel):
    name: str
    template_json: dict
    subject: str
    recipients: list[str]

@app.post("/api/templates/save")
async def save_template(request: TemplateRequest):
    template = {
        'id': str(uuid.uuid4()),
        'name': request.name,
        'template_json': request.template_json,
        'subject': request.subject,
        'recipients': request.recipients,
        'created_at': datetime.now().isoformat()
    }
    
    # Save to PostgreSQL
    # db.templates.insert(template)
    
    return {'id': template['id'], 'status': 'saved'}
```

### **Render Template Endpoint**
```python
@app.get("/api/templates/{template_id}/render")
async def render_template(template_id: str):
    # Get from DB
    # template = db.templates.find_one({'id': template_id})
    
    # Render JSON to HTML
    # Use email-builder-parser or similar
    
    return {'html': rendered_html}
```

### **Send Email Endpoint**
```python
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@app.post("/api/email/send")
async def send_email(template_id: str, recipients: list[str]):
    # Get template
    # template = db.templates.find_one({'id': template_id})
    
    # Render HTML
    # html = render(template['template_json'])
    
    # Send via SMTP
    msg = MIMEMultipart('alternative')
    msg['Subject'] = template['subject']
    msg['From'] = 'no-reply@samsung.com'
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    
    async with aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587) as smtp:
        await smtp.starttls()
        await smtp.login(username, password)
        await smtp.send_message(msg)
    
    return {'status': 'sent', 'recipients': len(recipients)}
```

---

## 📚 Code Examples

### **GrapesJS Custom Block for PLC Events**
```javascript
editor.BlockManager.add('plc-event-log', {
  label: 'PLC Event Log',
  content: { type: 'plc-event' }
});

editor.DomComponents.addType('plc-event', {
  model: {
    defaults: {
      tagName: 'div',
      attributes: { class: 'event-log' },
      traits: [
        {
          name: 'events',
          label: 'Events (JSON)',
          type: 'text',
          value: JSON.stringify([
            { time: '14:32', type: 'error', msg: 'Motor overload - Line A' },
            { time: '11:20', type: 'success', msg: 'System recovered' }
          ])
        }
      ]
    }
  }
});
```

### **react-email-editor Export to Backend**
```jsx
const exportAndSave = () => {
  editorRef.current.exportHtml(async (data) => {
    const response = await fetch('/api/templates/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'daily-report',
        html: data.html,
        design: data.design,
        subject: 'Daily Production Report'
      })
    });
    
    const result = await response.json();
    alert(`Saved: ${result.id}`);
  });
};
```

### **EmailBuilder.js with PostgreSQL**
```javascript
import { renderToStaticMarkup } from '@usewaypoint/email-builder-parser';

async function saveToDatabase(design) {
  const html = renderToStaticMarkup(design);
  
  const response = await fetch('/api/templates', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      design_json: design,
      html_output: html,
      name: 'template-' + Date.now(),
      subject: 'Manufacturing Report'
    })
  });
  
  return response.json();
}
```

---

## 🚀 Quick Start Commands

```bash
# GrapesJS
git clone https://github.com/grapesjs/grapesjs.git
cd grapesjs && npm install && npm run dev

# react-email-editor
npx create-react-app email-app && npm install react-email-editor

# EmailBuilder.js
git clone https://github.com/usewaypoint/email-builder-js.git
cd email-builder-js && npm install
cd packages/editor-sample && npm run dev

# Easy Email
git clone https://github.com/easy-email-com/easy-email.git
cd easy-email && npm install && npm run dev

# SendWithSES
git clone https://github.com/SendWithSES/Drag-and-Drop-Email-Designer.git
npm install && npm start
```

---

## 📋 Implementation Checklist

### **Phase 1: Choose Framework**
- [ ] GrapesJS (full-featured)
- [ ] react-email-editor (quick email)
- [ ] EmailBuilder.js (lightweight)
- [ ] Easy Email (MJML)
- [ ] SendWithSES (Angular)

### **Phase 2: Setup Frontend**
- [ ] Clone repository
- [ ] Install dependencies
- [ ] Configure build
- [ ] Test locally

### **Phase 3: Setup Backend (FastAPI)**
- [ ] Create template endpoints
- [ ] Setup PostgreSQL schema
- [ ] Configure SMTP
- [ ] Implement rendering

### **Phase 4: Integration**
- [ ] Connect frontend → backend
- [ ] Test save/load templates
- [ ] Test email sending
- [ ] Test schedule/cron jobs

### **Phase 5: Customization**
- [ ] Add Samsung blocks
- [ ] Customize themes
- [ ] Setup permissions
- [ ] Deploy to production

---

## 🔗 Resources

| Project | GitHub | Website | Docs | Stars |
|---------|--------|---------|------|-------|
| **GrapesJS** | [Link](https://github.com/grapesjs/grapesjs) | https://grapesjs.com | https://grapesjs.com/docs | 25.8k ⭐ |
| **react-email-editor** | [Link](https://github.com/unlayer/react-email-editor) | https://www.unlayer.com | https://react-email-editor.readthedocs.io/ | 5.1k ⭐ |
| **EmailBuilder.js** | [Link](https://github.com/usewaypoint/email-builder-js) | https://emailbuilderjs.com | Repo | 1.7k ⭐ |
| **Easy Email** | [Link](https://github.com/easy-email-com/easy-email) | https://easy-email.com | Repo | 2.4k ⭐ |
| **SendWithSES** | [Link](https://github.com/SendWithSES/Drag-and-Drop-Email-Designer) | https://sendune.com | Repo | 1k ⭐ |

---

## ✅ Summary

| Solution | Best For | Setup Time | Complexity | Community |
|----------|----------|-----------|-----------|-----------|
| **GrapesJS** | Email + Reports + Landing Pages | 2-4h | Medium | 25.8k ⭐ |
| **react-email-editor** | Quick Email Designer | 30m | Easy | 5.1k ⭐ |
| **EmailBuilder.js** | Lightweight Self-Hosted | 1h | Easy | 1.7k ⭐ |
| **Easy Email** | MJML + Features | 1-2h | Easy | 2.4k ⭐ |
| **SendWithSES** | Angular Integration | 1-2h | Easy | 1k ⭐ |

**Recommended:** GrapesJS (25.8k stars) for full capability + react-email-editor (5.1k stars) for quick email templates

---

**Skill Type:** Reference | Implementation Guide  
**Target Users:** Samsung Manufacturing Engineers, Full-Stack Developers  
**Last Updated:** 2026-08-23
