# skillz

Agent skills package manager — install, manage, and discover AI agent skills from GitHub.

## Install

```bash
# Zero-install via uvx (like npx for Python):
uvx skillz add kayaman/skills@semver

# Or install globally:
uv tool install skillz
skillz add kayaman/skills@semver
```

## Commands

### `skillz add <source>`

Install a skill from GitHub or a local path.

```bash
# Install a specific skill from a repo
skillz add kayaman/skills@semver

# Install all skills from a repo
skillz add kayaman/skills

# Install globally (to ~/.agents/skills/)
skillz add kayaman/skills@semver -g

# Install from a local directory
skillz add ./my-local-skill

# Skip confirmation
skillz add kayaman/skills@semver -y
```

### `skillz list`

Show installed skills (project + global).

```bash
skillz list            # Table output
skillz list --json     # JSON output
skillz list -g         # Global only
skillz ls              # Alias
```

### `skillz remove <name>`

Uninstall a skill and clean the lockfile.

```bash
skillz remove semver
skillz rm semver -g    # Remove from global
```

### `skillz update [name]`

Check for upstream changes and re-fetch updated skills.

```bash
skillz update          # Update all skills
skillz update semver   # Update a specific skill
```

### `skillz init [name]`

Scaffold a new `SKILL.md` template.

```bash
skillz init my-skill
skillz init my-skill --dir ./skills
```

### `skillz find <query>`

Search GitHub for repos containing agent skills.

```bash
skillz find "react testing"
skillz find deploy --limit 5
```

## Skill format

A skill is a directory containing a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: What this skill does and when to use it.
---

# My Skill

Instructions for the AI agent...
```

Skills are typically organized in a GitHub repo under a `skills/` directory:

```
my-repo/
└── skills/
    ├── skill-a/
    │   └── SKILL.md
    └── skill-b/
        ├── SKILL.md
        └── references/
            └── extra-context.md
```

## Lockfile

Installed skills are tracked in `.skill-lock.json` (v3 format, compatible with
[vercel-labs/skills](https://github.com/vercel-labs/skills)). Skills installed
by either tool are visible to the other.

## Supported agents

skillz detects and works with: Cursor, Claude Code, Codex, GitHub Copilot,
Amp, Cline, Continue, and Kiro.

## Development

```bash
uv sync                  # Install deps
uv run pytest -v         # Run tests
uv run ruff check src/   # Lint
uv run ruff format src/  # Format
uv run skillz --help     # Run locally
```

## License

Apache-2.0
