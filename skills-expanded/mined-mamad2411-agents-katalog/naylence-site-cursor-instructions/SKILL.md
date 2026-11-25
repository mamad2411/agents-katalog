# Naylence Website - Development Instructions

## Getting Started

### Prerequisites
- Node.js (v18 or higher recommended)
- npm or yarn
- Git
- Code editor (VS Code or Cursor recommended)

### Initial Setup
1. Clone the repository (if applicable)
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`
4. Open browser to `http://localhost:5173` (or port shown in terminal)

## Project Structure

### Current Files
- `index.html` - Main React component (contains entire website)
- `vercel.json` - Vercel deployment configuration
- `.cursorrules` - Cursor AI rules and guidelines
- `.cursor/` - Cursor-specific documentation

### Recommended Structure (Future)
```
naylence/
├── public/
│   ├── dark-swirl.png
│   ├── swirl-original.png
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Logo.jsx
│   │   ├── Navigation.jsx
│   │   └── Footer.jsx
│   ├── sections/
│   │   ├── Hero.jsx
│   │   ├── Architecture.jsx
│   │   └── Blog.jsx
│   ├── hooks/
│   │   └── useScroll.js
│   ├── utils/
│   │   └── constants.js
│   └── App.jsx
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── vercel.json
└── README.md
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the design system and code patterns
   - Test on multiple screen sizes
   - Ensure accessibility

3. **Test locally**
   ```bash
   npm run dev
   # Test in browser
   npm run build
   # Verify build succeeds
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

### Code Review Checklist

- [ ] Follows design system (colors, spacing, typography)
- [ ] Responsive on mobile, tablet, desktop
- [ ] Accessible (ARIA labels, keyboard navigation, contrast)
- [ ] No console errors or warnings
- [ ] Performance optimized (images, re-renders)
- [ ] Code follows established patterns
- [ ] Comments added for complex logic
- [ ] Tested in multiple browsers

## Component Development

### Creating a New Component

1. **Create component file**
   ```jsx
   // components/NewComponent.jsx
   import React from 'react';
   
   const NewComponent = ({ prop1, prop2 }) => {
     return (
       <div className="bg-[#020808] p-6 rounded-xl border border-teal-900/30">
         {/* Component content */}
       </div>
     );
   };
   
   export default NewComponent;
   ```

2. **Follow naming conventions**
   - PascalCase for components
   - Descriptive, clear names
   - Match file name to component name

3. **Use established patterns**
   - State management with hooks
   - Tailwind CSS for styling
   - Lucide React for icons
   - Proper prop types/documentation

### Styling Guidelines

1. **Use Tailwind utility classes**
   - Prefer composition over custom CSS
   - Use responsive prefixes (sm:, md:, lg:)
   - Group related classes logically

2. **Color usage**
   - Backgrounds: `bg-[#020808]` or `bg-[#030c0c]`
   - Text: `text-white` (headings), `text-slate-400` (body)
   - Accents: `text-teal-400`, `border-teal-900/30`

3. **Spacing**
   - Consistent padding: `p-6`, `p-8`
   - Consistent gaps: `gap-4`, `gap-6`, `gap-8`
   - Section padding: `py-24`

4. **Effects**
   - Transitions: `transition-all duration-200`
   - Hover: `hover:border-teal-500/50 hover:-translate-y-1`
   - Shadows: Custom teal-tinted shadows

## Content Management

### Updating Blog Posts

Blog posts are defined in the `blogs` array:
```jsx
const blogs = [
  {
    title: "Post Title",
    desc: "Description text",
    date: "Oct 3, 2025",
    link: "https://medium.com/@naylencedev"
  }
];
```

### Updating Features

Features are defined in the `features` array:
```jsx
const features = [
  {
    icon: <IconComponent className="w-6 h-6 text-teal-400" />,
    title: "Feature Title",
    desc: "Feature description"
  }
];
```

### Adding New Sections

1. Create section component or add to main component
2. Use section wrapper: `<section id="section-id" className="py-24">`
3. Follow established layout patterns
4. Add navigation link if needed
5. Test responsive behavior

## Asset Management

### Images

1. **Place images in `public/` folder**
   - Logo: `public/dark-swirl.png`
   - Background: `public/swirl-original.png`

2. **Reference in code**
   ```jsx
   <img src="/dark-swirl.png" alt="Description" />
   ```

3. **Optimize images**
   - Use WebP format when possible
   - Compress images before adding
   - Use appropriate sizes for different screens

### Icons

- Use Lucide React icons
- Import: `import { IconName } from 'lucide-react'`
- Size: `className="w-6 h-6"` (adjust as needed)
- Color: `className="text-teal-400"`

## Testing

### Manual Testing Checklist

- [ ] Navigation works (desktop and mobile)
- [ ] All links work correctly
- [ ] Images load properly
- [ ] Responsive on mobile (375px)
- [ ] Responsive on tablet (768px)
- [ ] Responsive on desktop (1024px+)
- [ ] Hover effects work
- [ ] Smooth scrolling works
- [ ] Code preview tabs switch correctly
- [ ] Mobile menu opens/closes
- [ ] No console errors
- [ ] Accessibility (keyboard navigation, screen reader)

### Browser Testing

Test in:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS)
- Chrome Mobile (Android)

### Performance Testing

1. Run Lighthouse audit
2. Check Core Web Vitals:
   - LCP (Largest Contentful Paint) < 2.5s
   - FID (First Input Delay) < 100ms
   - CLS (Cumulative Layout Shift) < 0.1
3. Optimize images
4. Minimize bundle size
5. Use code splitting if needed

## Deployment

### Vercel Deployment

1. **Automatic deployment**
   - Push to main branch triggers deployment
   - Preview deployments for pull requests

2. **Manual deployment**
   ```bash
   vercel --prod
   ```

3. **Environment variables**
   - Add in Vercel dashboard
   - Or use CLI: `vercel env add VARIABLE_NAME`

4. **Custom domain**
   - Configure in Vercel dashboard
   - Update DNS records as instructed

### Pre-Deployment Checklist

- [ ] Build succeeds: `npm run build`
- [ ] No console errors
- [ ] All images optimized
- [ ] Environment variables set
- [ ] Analytics configured (if applicable)
- [ ] SEO meta tags added
- [ ] Favicon added
- [ ] 404 page configured (if needed)

## Troubleshooting

### Common Issues

**Images not loading**
- Check file path (should be in `public/`)
- Verify file name matches exactly
- Check browser console for 404 errors

**Styles not applying**
- Verify Tailwind config
- Check class names for typos
- Ensure Tailwind is processing correctly
- Clear browser cache

**Build errors**
- Check Node version compatibility
- Clear `node_modules` and reinstall
- Check for syntax errors
- Verify all imports are correct

**Vercel deployment fails**
- Check build logs in Vercel dashboard
- Verify `vercel.json` configuration
- Ensure build command is correct
- Check for environment variable issues

### Getting Help

1. Check error messages in console
2. Review Vercel deployment logs
3. Check browser DevTools
4. Review code for common mistakes
5. Consult documentation (React, Tailwind, Vercel)

## Best Practices

### Code Quality
- Write clean, readable code
- Use meaningful variable names
- Add comments for complex logic
- Follow established patterns
- Keep components focused and reusable

### Performance
- Optimize images
- Minimize re-renders
- Use React.memo when appropriate
- Lazy load below-fold content
- Minimize bundle size

### Accessibility
- Use semantic HTML
- Add ARIA labels
- Ensure keyboard navigation
- Maintain color contrast
- Test with screen readers

### SEO
- Use proper heading hierarchy
- Add meta descriptions
- Use alt text for images
- Implement structured data (if needed)
- Ensure fast load times

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and optimize performance quarterly
- Update content as needed
- Monitor analytics
- Review and fix accessibility issues
- Keep design system documentation updated

### Version Control

- Use descriptive commit messages
- Keep commits atomic
- Review code before merging
- Use feature branches
- Tag releases appropriately

## Resources

- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Lucide Icons](https://lucide.dev)
- [Vercel Documentation](https://vercel.com/docs)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

