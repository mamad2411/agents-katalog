# Deployment Instructions

## 🚀 Deployment Overview

This application is designed for deployment on **Vercel** (recommended) with Hygraph as the CMS backend.

## 🌐 Vercel Deployment (Recommended)

### Prerequisites:
- GitHub repository with your code
- Vercel account connected to GitHub
- Environment variables configured

### Step-by-Step Deployment:

#### 1. **Prepare Repository**
```bash
# Ensure all changes are committed
git add .
git commit -m "feat: prepare for deployment"
git push origin main
```

#### 2. **Vercel Project Setup**
```bash
# Option A: Vercel CLI (recommended)
npm install -g vercel
vercel

# Option B: Vercel Dashboard
# 1. Visit vercel.com
# 2. Import GitHub repository
# 3. Configure project settings
```

#### 3. **Environment Variables Setup**
```env
# Required environment variables for production:
NEXT_PUBLIC_MASTER_URL_KEY=your_hygraph_api_key
DESCOPE_API=your_descope_project_id
DESCOPE_CLIENT_ID=your_descope_client_id
NEXTAUTH_SECRET=your_nextauth_secret_key
NEXTAUTH_URL=https://yourdomain.vercel.app

# Optional (for future features):
MONGODB_URI=mongodb://your_mongodb_connection
STRIPE_SECRET_KEY=sk_live_your_stripe_key
SENDGRID_API_KEY=your_sendgrid_key
```

#### 4. **Build Configuration**
```javascript
// next.config.mjs (already configured)
const nextConfig = {
    reactStrictMode: false,
    images: {
        unoptimized: true,
        domains: ['media.graphassets.com', 'lh3.googleusercontent.com']
    }
};

export default nextConfig;
```

#### 5. **Deploy**
```bash
# Automatic deployment via GitHub integration
git push origin main
# Vercel will automatically build and deploy
```

## 🔧 Alternative Deployment Options

### Netlify Deployment:

#### 1. **Build Settings**
```bash
# Build command:
npm run build

# Publish directory:
out

# Node version:
18.x
```

#### 2. **Netlify Configuration**
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "out"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Self-Hosted Deployment:

#### 1. **Server Requirements**
```bash
# Minimum server specs:
- Node.js 18+
- 2GB RAM
- 10GB storage
- Ubuntu 20.04+ / CentOS 8+
```

#### 2. **Production Setup**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
npm install -g pm2

# Clone and setup project
git clone https://github.com/yourusername/home-service-app-web.git
cd home-service-app-web
npm install
npm run build

# Start with PM2
pm2 start npm --name "home-service-app" -- start
pm2 startup
pm2 save
```

## 🔒 Environment Configuration

### Development Environment:
```env
# .env.local
NEXT_PUBLIC_MASTER_URL_KEY=your_development_key
DESCOPE_API=your_descope_project_id
DESCOPE_CLIENT_ID=your_descope_client_id
NEXTAUTH_SECRET=development_secret
NEXTAUTH_URL=http://localhost:3000
```

### Production Environment:
```env
# Vercel Environment Variables
NEXT_PUBLIC_MASTER_URL_KEY=your_production_key
DESCOPE_API=your_descope_project_id
DESCOPE_CLIENT_ID=your_descope_client_id
NEXTAUTH_SECRET=super_secure_production_secret
NEXTAUTH_URL=https://yourdomain.vercel.app

# Future additions:
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/database
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
SENDGRID_API_KEY=SG.your_sendgrid_key
```

## 🧪 Pre-Deployment Testing

### Production Build Test:
```bash
# 1. Test production build locally
npm run build
npm run start

# 2. Test all core functionality:
□ Home page loads
□ Authentication works
□ API calls function
□ Navigation works
□ Mobile responsive
□ Images load correctly
```

### Deployment Checklist:
```
□ All environment variables configured
□ Build passes without errors
□ No console errors in production
□ Authentication provider configured for production domain
□ Hygraph API permissions set correctly
□ Images and assets load from CDN
□ Performance audit passes (Lighthouse score >80)
□ SEO meta tags configured
□ Error pages configured (404, 500)
```

## 🔧 Domain Configuration

### Custom Domain Setup (Vercel):

#### 1. **Add Domain in Vercel Dashboard**
```
1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
```

#### 2. **DNS Configuration**
```dns
# Add these DNS records:
Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: A
Name: @
Value: 76.76.19.61
```

#### 3. **Update Environment Variables**
```env
# Update NEXTAUTH_URL to your custom domain
NEXTAUTH_URL=https://yourdomain.com
```

## 📊 Performance Optimization

### Pre-Deployment Optimizations:

#### 1. **Image Optimization**
```javascript
// Already configured in next.config.mjs
images: {
    unoptimized: true,
    domains: ['media.graphassets.com', 'lh3.googleusercontent.com']
}
```

#### 2. **Bundle Analysis**
```bash
# Analyze bundle size
npm install --save-dev @next/bundle-analyzer

# Add to package.json scripts:
"analyze": "ANALYZE=true next build"

# Run analysis
npm run analyze
```

#### 3. **Performance Audit**
```bash
# Lighthouse audit checklist:
□ Performance score >80
□ Accessibility score >90
□ Best practices score >90
□ SEO score >80
```

## 🚨 Security Configuration

### Production Security Checklist:
```
□ HTTPS enabled (automatic with Vercel)
□ Environment variables secure
□ API keys not exposed in client-side code
□ Authentication provider configured for production
□ CORS policies configured
□ Rate limiting implemented (if needed)
□ Security headers configured
```

### Security Headers:
```javascript
// next.config.mjs additions for security
const nextConfig = {
    async headers() {
        return [
            {
                source: '/(.*)',
                headers: [
                    {
                        key: 'X-Frame-Options',
                        value: 'DENY'
                    },
                    {
                        key: 'X-Content-Type-Options',
                        value: 'nosniff'
                    },
                    {
                        key: 'Referrer-Policy',
                        value: 'origin-when-cross-origin'
                    }
                ]
            }
        ]
    }
}
```

## 📈 Monitoring & Analytics

### Post-Deployment Monitoring:

#### 1. **Vercel Analytics**
```bash
# Enable Vercel Analytics
npm install @vercel/analytics

# Add to layout.js
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

#### 2. **Error Monitoring**
```bash
# Recommended: Sentry for error tracking
npm install @sentry/nextjs

# Configure in sentry.client.config.js
```

#### 3. **Performance Monitoring**
```bash
# Monitor key metrics:
□ Page load times
□ API response times
□ Error rates
□ User engagement
□ Core Web Vitals
```

## 🔄 CI/CD Pipeline

### GitHub Actions Setup:

#### 1. **Create Workflow File**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm run test
    
    - name: Build project
      run: npm run build
```

#### 2. **Deployment Automation**
```bash
# Vercel automatically deploys on git push
# No additional configuration needed
```

## 🚀 Deployment Workflow

### Standard Deployment Process:

#### 1. **Pre-Deployment**
```bash
# Run all tests
npm run test

# Build and test locally
npm run build
npm run start

# Check lighthouse scores
# Verify all functionality
```

#### 2. **Deployment**
```bash
# Commit and push changes
git add .
git commit -m "feat: feature description"
git push origin main

# Vercel automatically builds and deploys
```

#### 3. **Post-Deployment Verification**
```bash
# Test production site:
□ All pages load correctly
□ Authentication works
□ API integration works
□ Mobile responsiveness
□ Performance acceptable
```

## 🛠️ Troubleshooting Deployment Issues

### Common Issues & Solutions:

#### 1. **Build Failures**
```bash
# Check build logs in Vercel dashboard
# Common causes:
- Missing environment variables
- TypeScript errors
- Import path issues
- Package dependency conflicts

# Solution:
- Fix errors locally first
- Test build command: npm run build
- Ensure all dependencies installed
```

#### 2. **Environment Variable Issues**
```bash
# Symptoms:
- API calls failing
- Authentication not working
- Features missing

# Solution:
- Verify all env vars in Vercel dashboard
- Check variable names match exactly
- Restart deployment after adding vars
```

#### 3. **Authentication Issues**
```bash
# Common causes:
- NEXTAUTH_URL incorrect
- Descope configuration mismatch
- Domain not configured in auth provider

# Solution:
- Update NEXTAUTH_URL to production domain
- Configure Descope for production domain
- Test authentication flow
```

## 📋 Deployment Completion Checklist

### Final Verification:
```
□ Site loads at production URL
□ All pages accessible
□ Authentication flow works
□ API integration functional
□ Mobile responsive design
□ Performance scores acceptable
□ SEO optimization complete
□ Error handling works
□ Analytics tracking active
□ Security headers configured
□ SSL certificate active
□ Custom domain configured (if applicable)
□ Monitoring alerts set up
```

## 🎯 Post-Deployment Tasks

### 1. **Performance Monitoring**
- Set up regular performance audits
- Monitor Core Web Vitals
- Track user engagement metrics

### 2. **User Testing**
- Conduct final user acceptance testing
- Gather feedback from real users
- Monitor error rates and user behavior

### 3. **Documentation Updates**
- Update README with production URLs
- Document deployment process
- Create user guides if needed

### 4. **Backup & Recovery**
- Set up database backups (when MongoDB added)
- Document recovery procedures
- Test backup restoration process

Remember: **Deployment is not the end - it's the beginning of the maintenance phase** 