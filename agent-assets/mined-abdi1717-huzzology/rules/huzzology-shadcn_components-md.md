---
description: Best practices for using ShadCN UI components in Next.js applications
globs: components/**/*.tsx, app/**/*.tsx
alwaysApply: true
---

# ShadCN UI Component Best Practices

- **Select Component Rules**
  - **Always use non-empty string values for SelectItem**
    - The ShadCN Select component requires non-empty values for proper functionality
    - An empty string value `""` will cause runtime errors
    ```tsx
    <Select value={filter} onValueChange={setFilter}>
      <SelectContent>
        {/* ✅ DO: Use a non-empty string like "all" */}
        <SelectItem value="all">All Categories</SelectItem>
        
        {/* ❌ DON'T: Use empty string values */}
        <SelectItem value="">All Categories</SelectItem>
      </SelectContent>
    </Select>
    ```
  - **Match state handling with your SelectItem values**
    ```tsx
    // Initialize with a valid value, matching your "all" SelectItem
    const [filter, setFilter] = useState('all');
    
    // Then update your filtering logic accordingly
    const filtered = useMemo(() => {
      return items.filter(item => 
        filter === 'all' ? true : item.category === filter
      );
    }, [items, filter]);
    ```

- **Toast Component Integration**
  - **Import from hooks, not components**
    ```tsx
    // ✅ DO: Import from hooks
    import { useToast } from '@/hooks/use-toast';
    
    // ❌ DON'T: Import from components
    import { useToast } from '@/components/ui/use-toast';
    ```
