# CCI Tasks

The purpose of this repository is to hold a library of cci tasks for use with cci workflows.

Potential future improvements:

- Separate tasks into individual files as necessary when new tasks are added.
- Tasks for creating unlocked packages & versions.
- Automate how tasks are initialized from this library into new cci projects.

## Setup

1. Add contents of `cumulusci.snippet.yml` to `cumulusci.yml` of your cci project
2. Merge remaining content into your cci project

## Executing tasks through vscode

1. Launch command pallet and select `Tasks: Run Task`.
2. Select task and complete prompts.

## Executing tasks through command line

Examples:

```
cci task run resolve_dependencies --org dev
```

```
cci task run set_default --org dev -o dir force-app
```
