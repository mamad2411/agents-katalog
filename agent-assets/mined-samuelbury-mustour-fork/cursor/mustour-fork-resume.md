---
description: most important rules
globs: 
---
You are inside a NextJs project version 15 with the App router

Do not use any type always try to find the best type to use

for the back end always use a controller, service, repository pattern, the controller can be a route or a server action.
DO NOT CALL DB OUTSIDE OF A REPOSITORY, always use a service that call a repository to call the db
- For any routes interacting with Prisma via service and reporitories, wrap them using the `@/lib/handlers/withErrorHandling.ts` middleware. 
 
the repository have to be inside a folder with 2 files one queries and one mutations

TO call the db use this import { db } from "@/lib/database/db";

for react component do not mix the logic with the vue, use hooks for the logic in another file of course

Always search if the components exist before creating new one.

TO use toast import it like this: import { toast } from "@/components/ui/use-toast";
and use it like this:  toast({
      title: "Opération réussie!",
      description: "Le type d'âge a été créé avec succès",
    });


