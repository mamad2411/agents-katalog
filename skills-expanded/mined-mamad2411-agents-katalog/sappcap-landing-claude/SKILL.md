# CLAUDE.md - Project Context for AI Assistant

## Project Overview
Sapp Capital Advisors landing page - Commercial Real Estate advisory services

## Key Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run linting
- `npm run typecheck` - Check TypeScript types

## Git Workflow
- Work on `staging` branch, merge to `main` for production
- **"sync main"** or **"pull main"** = fetch/pull main, stay on staging

## TODO List

### High Priority
- [ ] **Lead Magnet Implementation** - Create downloadable resource "7 Fatal Modeling Errors That Kill Deals" with email capture form
  - Add email capture modal/popup
  - Create PDF resource
  - Set up email automation
  - Add exit-intent trigger
  - Track conversion rates

### Future Enhancements
- [ ] Add case studies section (anonymized)
- [ ] Implement A/B testing for headlines
- [x] Add client testimonials
- [ ] Create tiered service offerings page
- [ ] Add blog integration from blog.sapp.capital

## Adding Client Testimonials

Source files are stored in OneDrive:
- **Logos:** `/Users/Ed/Library/CloudStorage/OneDrive-SharedLibraries-DemographIQ/SCA - Documents/Admin Register/client logos/`
- **URLs CSV:** Same folder, `client URLs.csv`

### Steps to add a new testimonial:

1. **Add logo to source folder** - Any format (PNG, WEBP, etc.). White-on-transparent works best for dark mode.

2. **Update the CSV** with client name and website URL

3. **Copy logo to project:**
   ```bash
   cp "/Users/Ed/Library/CloudStorage/OneDrive-SharedLibraries-DemographIQ/SCA - Documents/Admin Register/client logos/[logo-file]" public/clients/[client-name]-logo.[ext]
   ```

4. **Append an entry to the `testimonials` array at the top of `app/page.tsx`:**
   ```ts
   {
     quote: "The testimonial quote text",
     name: "Contact Name",
     title: "Their Title",
     company: "Company Name",
     logo: "/clients/[client-name]-logo.[ext]",
     url: "https://their-website.com/",
   },
   ```
   The array is rendered by `<TestimonialCarousel>` — no grid-column or `FadeIn` wrapping needed.

## Project Structure
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Dark mode support
- Mobile responsive
- Cal.com integration for booking

## Key Metrics to Track
- Booking conversion rate
- Email capture rate
- Time on page
- Bounce rate
- Mobile vs desktop conversions