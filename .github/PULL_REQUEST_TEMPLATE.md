## What this does

<!-- Clear description of the change. Link related issues, e.g. "Related to #15" or "Closes #N" -->

## What this doesn't do

<!-- Explicit non-goals. Especially important if this is one step of a larger staged effort. -->

## Does this touch production code paths?

<!-- chains.py, prompts.py, lawglance_main.py, or anything else on the live request path.
     If yes, explain the behavior change and any risk. If no, say so explicitly. -->

- [ ] Yes — production code path changed (describe impact below)
- [ ] No — this is eval-only / docs-only / test-only / tooling

## Test plan

- [ ] Tests added/updated and passing locally (`uv run pytest tests/ -v`)
- [ ] Manually verified (describe how)
- [ ] N/A — explain why

## Checklist

- [ ] No secrets, API keys, or credentials in this diff
- [ ] New dependencies (if any) are justified in the description above
- [ ] Lint passes (`uv run ruff check .`)