# Makefile Build Target Finder

This application is a GitHub Action that analyzes Makefiles and returns the targets that depend on the input file.

## Features

- Retrieve targets as a list from dependent file names
- Find targets that depend on other targets

### Upcoming features

- Multiple targets
- Macros
- Suffixes rules

## Input & Output

```yaml
inputs:
    makefile:
        description: 'The Makefile to find build targets from'
        default: 'Makefile'
        required: false
    dependencies:
        description: 'Files to find with dependencies (separated by spaces)'
        required: true

outputs:
    targets:
        description: "Returns targets"
        value: ${{ steps.makefile-build-target-finder.outputs.targets }}
```

## Usage

Here's an example of how to write an action to retrieve the targets that depend on the file `hello.c` from the Makefile:

```
hello.o: hello.c
    gcc -c hello.c

world.o: world.c
    gcc -c world.c

helloWorld: hello.o world.o
    gcc -o helloWorld hello.o world.o
```

```yaml
jobs:
  runner:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - id: makefile-build-target-finder
        uses: meihei3/makefile-build-target-finder@main
        with:
          makefile: 'tests/usage.mk'
          dependencies: 'hello.c'

      - id: check
        needs: [ makefile-build-target-finder ]
        shell: bash
        run: echo ${{ steps.makefile-build-target-finder.outputs.targets }} # -> "helloWorld hello.o"
```

By combining it with tj-actions/changed-files, you can also retrieve targets that depend on git changed files.

```yaml
jobs:
  runner:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v35

      - id: makefile-build-target-finder
        uses: meihei3/makefile-build-target-finder@main
        with:
          dependencies: ${{ steps.changed-files.outputs.all_changed_files }}

      - id: check
        shell: bash
        run: echo ${{ steps.this.outputs.targets }}
```
