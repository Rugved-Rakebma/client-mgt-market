---
description: Initialize the context system in a client project
disable-model-invocation: true
---

# Context Init

Set up the client context system in the current project. Idempotent — safe to run on both fresh projects and projects with existing context vaults.

## Workflow

### 1. Detect existing state

Check what already exists:
- Does `context-vault/` exist?
- Does `.claude/rules/context-vault.md` exist?
- Does `CLAUDE.md` contain a "## Context Vault" section?
- What projects exist in `context-vault/projects/`?
- Which projects already have `.claude/rules/project-{slug}.md`?

Report what was found.

### 2. Scaffold context vault (if missing)

If `context-vault/` does not exist, create:

```
context-vault/
├── index.md              # Empty master index with header
├── log.md                # Empty log with header
├── projects/
├── decisions/
├── action-items/
├── strategies/
├── requirements/
├── people/
├── docs/
│   ├── meetings/
│   ├── client-docs/
│   └── deliverables/
├── config.yaml           # From template, with project name filled in
└── .gitignore            # Excludes raw/
```

If `context-vault/` already exists, skip and report "vault already exists."

### 3. Install the always-loaded rule

If `.claude/rules/context-vault.md` does not exist, copy from the plugin template. This rule has empty frontmatter (no `paths:`) so it loads every session.

If it already exists, skip.

### 4. Install project-level rules

Scan `context-vault/projects/` for existing project directories. For each project that does NOT already have `.claude/rules/project-{slug}.md`:

- Read the project overview to get the title
- Write `.claude/rules/project-{slug}.md` with `paths:` scoped to `projects/{slug}/**/*`

Report how many project rules were created.

### 5. Update CLAUDE.md

If `CLAUDE.md` does not contain a "## Context Vault" section:
- Append the section from the plugin template

If it already contains the section, skip.

### 6. Report

Summary of what was done:
- Vault: created / already existed
- Rules: N created, N already existed
- CLAUDE.md: updated / already current
- Remind user to run `/ctx:project <name>` to add new projects
