---
name: d2-02-api-service
description: "Generates an Angular service that calls the up-api CRUD endpoints for a given entity (getAll, getById, save, update, delete). Use when the user asks for Day 2 step 3 of the CRUD drill, or asks to create the Angular service that talks to up-api. Needs the same entity used on Day 1."
compatibility: "Requires an existing up-app Angular project (from earlier drill steps) and a running up-api with CRUD endpoints for the target entity."
---

# Day 2 · Step 2 — API service

If the entity isn't already established in this conversation, ask which entity (it must match the one
exposed by up-api's CRUD endpoints).

`up-app/src/app/services/<entity>.service.ts`:
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface <Entity> {
  id?: number;
  // one field per column from the Day 1 entity spec
}

@Injectable({ providedIn: 'root' })
export class <Entity>Service {
  private base = 'http://localhost:8080/api/<entity>s';
  constructor(private http: HttpClient) {}

  getAll(): Observable<<Entity>[]> { return this.http.get<<Entity>[]>(this.base); }
  getById(id: number): Observable<<Entity>> { return this.http.get<<Entity>>(`${this.base}/detail/${id}`); }
  save(item: <Entity>): Observable<<Entity>> { return this.http.post<<Entity>>(`${this.base}/save`, item); }
  update(id: number, item: <Entity>): Observable<<Entity>> { return this.http.put<<Entity>>(`${this.base}/update/${id}`, item); }
  delete(id: number): Observable<void> { return this.http.delete<void>(`${this.base}/${id}`); }
}
```

Register `provideHttpClient()` in `app.config.ts` if it isn't already there. No redeploy needed for this step.
