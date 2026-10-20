# Initialize parallel git worktree directories

## Variables
FEATURE_NAME: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## Execute these commands
> Execute the loop in parallel with the Batch and Task tool

- create a new dir `trees/`

- for i in NUMBER_OF_PARALLEL_WORKTREES
  - RUN `git worktree add -b FEATURE_NAME-i ./trees/FEATURE_NAME-i`
  - RUN `cp ./.env ./trees/FEATURE_NAME-i/.env`
  - Perform development environment initialization tasks (install necessary packages, libraries, etc.).
  - UPDATE `./trees/FEATURE_NAME-i/config.ts`: 
    - `port: 5173+(i),`
  - RUN `cat ./trees/FEATURE_NAME-i/config.ts` to verify the client port is set correctly
  - RUN `cd trees/FEATURE_NAME-i`, `git ls-files` to validate

- RUN `git worktree list` to verify all trees were created properly
