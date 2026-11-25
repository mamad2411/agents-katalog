# InfiniteCalc

## Before every build

Run the unit tests before submitting a build job:

    ./gradlew :calculator-logic:test -q

If any tests fail, fix them before building. Do not submit a build with failing tests.

## Building

The build server pulls from GitHub — commit and push before triggering a build.

    git push origin main
    ~/bin/buildserver.sh build InfiniteCalc

Add `--clean` when `build.json` dependencies change or the scaffold looks corrupt.

## Notes

- `app/src/test` does not run anywhere — only `calculator-logic/src/test` is executed.
- AAPT2 requires x86_64; the `app` module cannot be tested on this machine.
