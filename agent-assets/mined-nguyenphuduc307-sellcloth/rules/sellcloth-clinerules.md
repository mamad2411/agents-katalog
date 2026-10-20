# SellCloth Project Rules & Patterns

## Communication & Language
- **Primary Language**: Vietnamese cho user communication
- **Code Language**: English cho code, comments, và technical docs
- **Data Language**: Vietnamese cho content (product names, categories, etc.)

## Development Patterns

### Laravel Best Practices
- Use Eloquent ORM, avoid raw SQL queries
- Follow Laravel naming conventions (CamelCase cho models, snake_case cho database)
- Use Artisan commands cho repetitive tasks
- Migrations only forward (no rollback trong production)

### Filament Patterns
- Auto-generate resources first, then customize
- Use Filament form components cho consistent UI
- Leverage Filament table features (filters, actions, etc.)
- Keep resource classes focused và readable
- **PROVEN**: Vietnamese labels work perfectly in Filament interface

### Database Design Decisions
- JSON fields cho arrays (sizes, colors, images) - simpler than pivot tables
- Embedded customer info trong orders (no separate customers table yet)
- Auto-generated order numbers với date prefix
- Boolean flags cho status management (is_active, is_featured)

## Code Organization
```
Models: Business logic và relationships
Resources: Admin interface definitions
Seeders: Consistent test data generation
Migrations: Schema evolution, always forward
```

## Data Patterns

### Vietnamese Product Categories
- "Áo nam", "Áo nữ", "Quần nam", "Quần nữ", "Phụ kiện", "Giày dép"
- Use Vietnamese names but English slugs
- Maintain slug uniqueness for SEO

### Product Variant Handling
- Sizes as array: ['S', 'M', 'L', 'XL'] cho clothing, ['39', '40', '41'] cho shoes
- Colors as array: ['Đen', 'Trắng', 'Xám'] in Vietnamese
- Prices in VND (Vietnamese Dong) với ₫ symbol

### Order Management Flow
```
pending → processing → shipped → delivered
cancelled (can happen from any state)
```

## User Preferences
- **Admin Panel Focus**: Priority on admin functionality first ✅ COMPLETED
- **Simplicity**: Keep features simple and functional ✅ PROVEN WORKING
- **Vietnamese UX**: User-facing content in Vietnamese ✅ IMPLEMENTED
- **Step-by-step**: Implement features incrementally ✅ FOLLOWING

## Development Workflow PROVEN EFFECTIVE
1. Database design first (migrations) ✅
2. Models với relationships ✅
3. Seeders cho test data ✅
4. Filament resources cho admin ✅
5. Test everything before moving forward ✅
6. **NEW**: Live testing với actual data creation ✅

## Image & File Handling
- Currently: JSON placeholders working perfectly
- Future: Proper file upload với Filament FileUpload component
- Pattern: Store file paths in JSON arrays
- Consider cloud storage for production

## Performance Considerations
- JSON queries acceptable cho small scale ✅ VERIFIED
- Plan for caching layer if scale increases
- Keep database normalized except for convenience arrays
- Monitor N+1 query problems với relationships

## Project Evolution Notes
- Started with basic e-commerce requirements ✅
- Focus on admin panel để manage inventory ✅ COMPLETED
- Public website là next priority 🎯 READY TO START
- Built for small to medium scale shops

## Testing Insights (Learned from Live Testing)
- **CRUD Operations**: All working flawlessly in admin panel
- **JSON Fields**: Sizes và colors arrays work perfectly
- **Relationships**: Category-Product links functional
- **Vietnamese Interface**: Labels và navigation work beautifully
- **Auto-generation**: Slug generation from Vietnamese names works
- **Data Integrity**: Foreign key constraints properly enforced

## Next Phase Readiness
- **Frontend Development**: Ready to start public website
- **Technology Stack**: Laravel Blade + TailwindCSS recommended
- **Architecture**: Separate public controllers from admin
- **Data Foundation**: Solid và tested, ready for frontend consumption
