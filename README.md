# CCI Tasks

The purpose of this repository is to hold a library of cci tasks and workflows.

## Setup

1. Add the following to your cumulusci.yml

```
sources:
    cci-tasks:
        github: https://github.com/Candoris/cci-tasks
```

2. Copy tasks directory into into your target cci project

You do not need to copy any tasks that are not used for a particular project.

## Executing tasks through vscode

1. Merge tasks.json from this repository into your target cci project
2. Launch command pallet and select `Tasks: Run Task`.
3. Select task and complete prompts.

## Executing tasks through command line

Examples:

```
cci task run cci-tasks:resolve_dependencies --org dev
```

```
cci task run cci-tasks:set_default --org dev -o dir force-app
```
