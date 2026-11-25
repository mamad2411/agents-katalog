---
name: search-filtering
description: |
  Search, filtering, and sorting patterns for APIs and frontends. Apply when implementing
  product search, user search, admin filters, or any data listing with query parameters.
  Covers PostgreSQL full-text, Elasticsearch basics, filter builders, and React filter UI.
---

# Search & Filtering Patterns

## Django Filter Backend
```python
# filters.py
import django_filters
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    search = django_filters.CharFilter(method='filter_search')

    def filter_in_stock(self, queryset, name, value):
        return queryset.filter(stock__gt=0) if value else queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(sku__iexact=value)
        )

    class Meta:
        model = Product
        fields = ['category', 'is_active', 'min_price', 'max_price']

# ViewSet usage
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name', 'stock']
    ordering = ['-created_at']
```

## PostgreSQL Full-Text Search
```python
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def full_text_search(query: str, language: str = 'russian'):
    """For Uzbek, use 'simple' or 'russian' config"""
    search_vector = (
        SearchVector('name', weight='A', config=language) +
        SearchVector('description', weight='B', config=language) +
        SearchVector('tags', weight='C', config=language)
    )
    search_query = SearchQuery(query, config=language, search_type='websearch')
    
    return Product.objects.annotate(
        rank=SearchRank(search_vector, search_query, cover_density=True)
    ).filter(rank__gte=0.05).order_by('-rank')

def fuzzy_search(query: str):
    """Trigram similarity for typo-tolerance"""
    return Product.objects.annotate(
        similarity=TrigramSimilarity('name', query)
    ).filter(similarity__gte=0.3).order_by('-similarity')
```

## React Filter State
```typescript
interface ProductFilters {
  search: string;
  category: string | null;
  minPrice: number | null;
  maxPrice: number | null;
  inStock: boolean;
  sortBy: 'price_asc' | 'price_desc' | 'newest' | 'popular';
}

const DEFAULT_FILTERS: ProductFilters = {
  search: '',
  category: null,
  minPrice: null,
  maxPrice: null,
  inStock: false,
  sortBy: 'newest',
};

function useProductFilters() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const filters = useMemo(() => ({
    search: searchParams.get('search') || '',
    category: searchParams.get('category'),
    minPrice: searchParams.get('min_price') ? Number(searchParams.get('min_price')) : null,
    maxPrice: searchParams.get('max_price') ? Number(searchParams.get('max_price')) : null,
    inStock: searchParams.get('in_stock') === 'true',
    sortBy: (searchParams.get('sort') || 'newest') as ProductFilters['sortBy'],
  }), [searchParams]);

  const setFilter = useCallback(<K extends keyof ProductFilters>(key: K, value: ProductFilters[K]) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (value === null || value === false || value === '') {
        next.delete(key);
      } else {
        next.set(key, String(value));
      }
      next.delete('page'); // Reset pagination on filter change
      return next;
    });
  }, [setSearchParams]);

  const resetFilters = () => setSearchParams(new URLSearchParams());
  const activeFilterCount = Object.entries(filters).filter(([k, v]) =>
    v !== DEFAULT_FILTERS[k as keyof ProductFilters]
  ).length;

  return { filters, setFilter, resetFilters, activeFilterCount };
}
```
