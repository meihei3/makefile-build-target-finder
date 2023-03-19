# Makefile Build Target Finder

This application is a GitHub Action that analyzes Makefiles and returns the targets that depend on the input file.

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
            makefile: 'tests/actions.mk'
            dependencies: 'hello.c'

        - id: check
          needs: [ makefile-build-target-finder ]
          shell: bash
          run: echo ${{ steps.makefile-build-target-finder.outputs.targets }}
```
