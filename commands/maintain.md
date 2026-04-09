---
description: Wiki health check — find orphans, stale items, missing links
disable-model-invocation: true
---

# Context Maintain

Health check the context vault. Find structural issues and propose fixes.

## Checks

### 1. Orphan entities

Scan all entity files in `decisions/`, `action-items/`, `strategies/`, `requirements/`. For each, grep across `context-vault/projects/*/overview.md` to check if linked from any project overview.

Report unlinked entities.

### 2. Stale action items

Find action items where `status: "open"` and `created` date is older than 14 days. Present as candidates for status update.

### 3. Missing wikilinks

For each entity page, check:
- Does it have a source wikilink to a meeting doc?
- If action item, does it have an assignee wikilink to a person page?
- Does the source meeting doc link back to this entity?

Report missing bidirectional links.

### 4. Duplicate people

Check `context-vault/people/` for potential duplicates (similar names, same first name with different slugs).

### 5. Contradictory decisions

Read all decision pages. Flag any that appear to contradict without superseding.

### 6. Broken wikilinks

Extract all `[[...]]` patterns from entity pages. Check that the target file exists.

## Workflow

1. Run all checks
2. Present findings grouped by check type
3. For each issue, propose a specific fix
4. **Wait for approval** before making any changes
5. Apply approved fixes
6. Report what was changed
