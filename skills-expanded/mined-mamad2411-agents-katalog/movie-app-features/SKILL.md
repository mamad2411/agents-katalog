---
name: movie-app-features
description: Implementa features y componentes para Movie App siguiendo patrones establecidos. Usa cuando necesites crear funcionalidades como búsqueda, filtros, detalles de películas, favoritos, autenticación, o cualquier componente específico de la aplicación.
---

# Movie App - Implementación de Features

## Patrones de Implementación

### Estructura de Componente

```tsx
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import type { Movie } from "@/types/movie.types";

interface ComponentProps {
  // Props tipadas
}

export const ComponentName = ({ prop1, prop2 }: ComponentProps) => {
  // Estado local
  const [state, setState] = useState<Type>(initialValue);

  // Efectos
  useEffect(() => {
    // Lógica
  }, [dependencies]);

  // Handlers
  const handleAction = () => {
    // Lógica
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="..."
    >
      {/* JSX */}
    </motion.div>
  );
};
```

## Features Core

### 1. Catálogo con Grid/Lista

**MovieGrid.tsx:**

```tsx
import { MovieCard } from "./MovieCard";
import { SkeletonCard } from "@/components/ui/SkeletonCard";

interface MovieGridProps {
  movies: Movie[];
  loading?: boolean;
  viewMode?: "grid" | "list";
}

export const MovieGrid = ({
  movies,
  loading,
  viewMode = "grid",
}: MovieGridProps) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4 md:gap-6">
        {[...Array(12)].map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  return (
    <div
      className={`${
        viewMode === "grid"
          ? "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4 md:gap-6"
          : "flex flex-col gap-4"
      }`}
    >
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} viewMode={viewMode} />
      ))}
    </div>
  );
};
```

### 2. Búsqueda con Sugerencias

**useSearch.ts:**

```tsx
import { useState, useEffect } from "react";
import { useDebounce } from "./useDebounce";
import { searchMovies } from "@/services/movies.service";

export const useSearch = () => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery.length > 2) {
      setLoading(true);
      searchMovies(debouncedQuery)
        .then(setSuggestions)
        .finally(() => setLoading(false));
    } else {
      setSuggestions([]);
    }
  }, [debouncedQuery]);

  return { query, setQuery, suggestions, loading };
};
```

**MovieSearch.tsx:**

```tsx
import { useSearch } from "@/hooks/useSearch";
import { Search, X } from "lucide-react";

export const MovieSearch = () => {
  const { query, setQuery, suggestions, loading } = useSearch();

  return (
    <div className="relative w-full max-w-2xl">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Buscar películas..."
          className="w-full pl-12 pr-12 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-50"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-h-96 overflow-y-auto z-50">
          {suggestions.map((movie) => (
            <a
              key={movie.id}
              href={`/movie/${movie.id}`}
              className="flex items-center gap-4 p-4 hover:bg-slate-700 transition-colors"
            >
              <img
                src={movie.poster}
                alt={movie.title}
                className="w-12 h-16 object-cover rounded"
              />
              <div>
                <h4 className="text-slate-50 font-medium">{movie.title}</h4>
                <p className="text-slate-400 text-sm">{movie.year}</p>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
};
```

### 3. Filtros (Género, Año, Calificación)

**MovieFilters.tsx:**

```tsx
import { useState } from "react";
import { Filter } from "lucide-react";

interface Filters {
  genre: string;
  year: string;
  rating: string;
  language: string;
}

export const MovieFilters = ({
  onFilterChange,
}: {
  onFilterChange: (filters: Filters) => void;
}) => {
  const [filters, setFilters] = useState<Filters>({
    genre: "",
    year: "",
    rating: "",
    language: "",
  });
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (key: keyof Filters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg hover:bg-slate-700 transition-colors"
      >
        <Filter size={20} />
        Filtros
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 p-4 bg-slate-800 border border-slate-700 rounded-lg shadow-xl z-50 min-w-[300px]">
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-400 mb-2">
                Género
              </label>
              <select
                value={filters.genre}
                onChange={(e) => handleChange("genre", e.target.value)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded text-slate-50"
              >
                <option value="">Todos</option>
                {/* Opciones de géneros */}
              </select>
            </div>
            {/* Más filtros... */}
          </div>
        </div>
      )}
    </div>
  );
};
```

### 4. Página de Detalles

**MovieDetails.tsx:**

```tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getMovieById } from "@/services/movies.service";
import type { Movie } from "@/types/movie.types";

export const MovieDetails = () => {
  const { id } = useParams<{ id: string }>();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      getMovieById(id)
        .then(setMovie)
        .finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) return <div>Cargando...</div>;
  if (!movie) return <div>Película no encontrada</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid md:grid-cols-2 gap-8">
        <img src={movie.poster} alt={movie.title} className="rounded-lg" />
        <div>
          <h1 className="text-4xl font-bold mb-4">{movie.title}</h1>
          <p className="text-slate-400 mb-6">{movie.overview}</p>
          {/* Más detalles... */}
        </div>
      </div>
    </div>
  );
};
```

### 5. Sistema de Favoritos

**FavoritesContext.tsx:**

```tsx
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import type { Movie } from "@/types/movie.types";

interface FavoritesContextType {
  favorites: Movie[];
  addFavorite: (movie: Movie) => void;
  removeFavorite: (movieId: number) => void;
  isFavorite: (movieId: number) => boolean;
}

const FavoritesContext = createContext<FavoritesContextType | undefined>(
  undefined,
);

export const FavoritesProvider = ({ children }: { children: ReactNode }) => {
  const [favorites, setFavorites] = useState<Movie[]>(() => {
    const stored = localStorage.getItem("favorites");
    return stored ? JSON.parse(stored) : [];
  });

  useEffect(() => {
    localStorage.setItem("favorites", JSON.stringify(favorites));
  }, [favorites]);

  const addFavorite = (movie: Movie) => {
    setFavorites((prev) => [...prev, movie]);
  };

  const removeFavorite = (movieId: number) => {
    setFavorites((prev) => prev.filter((m) => m.id !== movieId));
  };

  const isFavorite = (movieId: number) => {
    return favorites.some((m) => m.id === movieId);
  };

  return (
    <FavoritesContext.Provider
      value={{ favorites, addFavorite, removeFavorite, isFavorite }}
    >
      {children}
    </FavoritesContext.Provider>
  );
};

export const useFavorites = () => {
  const context = useContext(FavoritesContext);
  if (!context)
    throw new Error("useFavorites must be used within FavoritesProvider");
  return context;
};
```

## Tipos TypeScript

**src/types/movie.types.ts:**

```tsx
export interface Movie {
  id: number;
  title: string;
  overview: string;
  poster: string;
  backdrop: string;
  releaseDate: string;
  year: number;
  rating: number;
  genres: Genre[];
  language: string;
  cast?: CastMember[];
  trailer?: string;
}

export interface Genre {
  id: number;
  name: string;
}

export interface CastMember {
  id: number;
  name: string;
  character: string;
  profilePath?: string;
}
```

## Servicios API

**src/services/movies.service.ts:**

```tsx
import api from "./api";
import type { Movie } from "@/types/movie.types";

export const getMovies = async (params?: {
  page?: number;
  genre?: string;
  year?: string;
  rating?: string;
}): Promise<{ movies: Movie[]; totalPages: number }> => {
  const response = await api.get("/movies", { params });
  return response.data;
};

export const getMovieById = async (id: string): Promise<Movie> => {
  const response = await api.get(`/movies/${id}`);
  return response.data;
};

export const searchMovies = async (query: string): Promise<Movie[]> => {
  const response = await api.get("/movies/search", { params: { q: query } });
  return response.data;
};
```

## Hooks Personalizados

**useDebounce.ts:**

```tsx
import { useEffect, useState } from "react";

export const useDebounce = <T,>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

## Checklist de Implementación

Al implementar una feature, verifica:

- [ ] Componente tipado con TypeScript
- [ ] Estados de carga (loading) implementados
- [ ] Manejo de errores
- [ ] Animaciones con Framer Motion
- [ ] Responsive en todos los breakpoints
- [ ] Accesibilidad (ARIA labels, keyboard nav)
- [ ] Optimización (memo, useMemo, useCallback cuando sea necesario)
- [ ] Integración con servicios API
- [ ] Persistencia (localStorage si aplica)
- [ ] Tests básicos (opcional pero recomendado)
