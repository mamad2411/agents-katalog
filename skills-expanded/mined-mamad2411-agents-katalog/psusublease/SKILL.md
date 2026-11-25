# PSU Leases Design Rules

## Design Principles
- Follow Outlier's clean, minimalist aesthetic
- Use generous whitespace (min 2rem between sections)
- Keep UI components minimal and functional
- Use a limited color palette (primarily white, with deep blue/purple accents)
- Maintain consistent padding (1.5-2rem) across components
- Create clear visual hierarchy with typography
- Design for both desktop and mobile views

## Layout
- Card-based layout for listings and requests
- Full-width header with navigation
- Centered content with max-width containers
- Clear section breaks between different functional areas

## Typography
- Sans-serif font family (system-ui or Inter)
- Limited font sizes (3-4 only)
- Consistent line heights (1.5-1.7)
- Bold headings, regular body text

## Database Structure
- apartments table: Store default apartment information (name, location, amenities, etc.)
- listings table: Store actual lease listings (apartment_id, price, duration, description, etc.)
- requests table: Store lease requests (location_preference, price_range, duration, etc.)
- users table: Store user information (manage through Supabase Auth)

## Architecture
- Use Supabase for database and authentication
- Access Supabase through MCP
- Implement client-side filtering for listings
- Ensure proper data validation before submission

## Components
- Navigation bar with logo and links
- Search/filter interface for listings
- Listing cards with consistent layout
- Simple forms for posting listings/requests
- User account management interface
- Authentication modals

## Interactions
- Minimize clicks to complete key actions
- Provide immediate feedback on user actions
- Implement simple animations for state changes
- Enable direct messaging between users