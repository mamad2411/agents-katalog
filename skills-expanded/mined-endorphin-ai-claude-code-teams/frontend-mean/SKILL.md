---
name: frontend-mean
description: "React frontend development for MEAN stack apps. Use when implementing React components, pages, hooks, API integration, routing, state management, and responsive UI."
---

# Frontend Mean

## Purpose

Implement React frontends for MEAN stack applications. Translate React architecture designs into working code: components, pages, custom hooks, API client, routing, context providers, forms, and responsive layouts.

## Key Patterns

### Component Pattern
```jsx
// components/common/Button.jsx
import styles from './Button.module.css';

const Button = ({ children, variant = 'primary', size = 'md', loading = false, disabled, onClick, type = 'button' }) => {
  return (
    <button
      type={type}
      className={`${styles.btn} ${styles[variant]} ${styles[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? <Spinner size="sm" /> : children}
    </button>
  );
};
export default Button;
```

### Page Pattern
```jsx
// pages/DashboardPage.jsx
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import PageWrapper from '../components/layout/PageWrapper';
import StatCards from '../components/features/StatCards';
import ActivityFeed from '../components/features/ActivityFeed';
import Spinner from '../components/common/Spinner';
import ErrorMessage from '../components/common/ErrorMessage';

const DashboardPage = () => {
  const { user } = useAuth();
  const { data: stats, loading, error, refetch } = useFetch('/api/dashboard/stats');

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;

  return (
    <PageWrapper title="Dashboard">
      <h1>Welcome, {user.name}</h1>
      <StatCards stats={stats} />
      <ActivityFeed userId={user.id} />
    </PageWrapper>
  );
};
export default DashboardPage;
```

### Custom Hook Patterns
```javascript
// hooks/useAuth.js -- Authentication hook
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

// hooks/useFetch.js -- Data fetching hook
import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get(url, options);
      setData(response.data.data);
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  }, [url]);
  useEffect(() => { fetch(); }, [fetch]);
  return { data, loading, error, refetch: fetch };
};

// hooks/useForm.js -- Form management hook
import { useState } from 'react';
export const useForm = (initialValues, validate) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };
  const handleSubmit = async (onSubmit) => {
    const validationErrors = validate ? validate(values) : {};
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length > 0) return;
    setIsSubmitting(true);
    try { await onSubmit(values); } catch (err) { setErrors({ submit: err.message }); }
    finally { setIsSubmitting(false); }
  };
  return { values, errors, isSubmitting, handleChange, handleSubmit, setValues, setErrors };
};
```

### API Client Pattern
```javascript
// services/api.js
import axios from 'axios';
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' }
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
export default api;
```

### Auth Context Pattern
```jsx
// context/AuthContext.jsx
import { createContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';
export const AuthContext = createContext(null);
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) { api.get('/api/auth/me').then(res => setUser(res.data.data)).catch(() => localStorage.removeItem('token')).finally(() => setLoading(false)); }
    else setLoading(false);
  }, []);
  const login = useCallback(async (email, password) => {
    const res = await api.post('/api/auth/login', { email, password });
    localStorage.setItem('token', res.data.data.token);
    setUser(res.data.data.user);
    return res.data.data;
  }, []);
  const register = useCallback(async (userData) => {
    const res = await api.post('/api/auth/register', userData);
    localStorage.setItem('token', res.data.data.token);
    setUser(res.data.data.user);
    return res.data.data;
  }, []);
  const logout = useCallback(() => { localStorage.removeItem('token'); setUser(null); }, []);
  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};
```

## Conventions

- Vite as build tool (NOT Create React App -- CRA is deprecated)
- Functional components only with hooks
- CSS Modules for styling (`Component.module.css`) or Tailwind CSS
- File naming: PascalCase for components, camelCase for hooks/utils/services
- Props destructured in function signature
- Every async operation: loading state + error state + success state
- Forms: controlled components with useForm hook
- API calls only through `services/api.js` -- never raw axios/fetch in components
- Token stored in localStorage (simple) -- HttpOnly cookie for production security
- Lazy load pages with `React.lazy` + `Suspense` for bundle splitting
- All user-facing text should be easy to extract for i18n later

## Knowledge Strategy

- **Patterns to capture:** Component implementations that worked well, hook patterns, form handling approaches
- **Examples to collect:** Complete page implementations, auth flow code, API integration patterns
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
