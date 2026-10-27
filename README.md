# sklanes

sklanes is a package with one agent skill, `lanes`. The skill reports requests
for human attention to a Lanes inbox, and it manages ordinary todos there. An
agent uses it before it stops to wait for an answer, a decision, a review or an
action from a person. Lanes is a cloud inbox, and its product source is a
separate repository.

The skill and its `lanes` command need Node.js 22 or newer. They do not need
Gest, a Lanes checkout, hooks or a local server. Read
`.agents/skills/lanes/SKILL.md` for the rules of reporting.

## Install the command and the global skills

Run the bundled installer from a clone of this repository:

```bash
node .agents/skills/lanes/scripts/install.mjs --dry-run
node .agents/skills/lanes/scripts/install.mjs
```

The installer copies the command to `~/.local/bin/lanes` and the skill to the
skill folders of Codex and Claude. It records hashes and the source revision in
`~/.local/share/lanes/install.json`. It changes no hooks, settings or
credentials. Read `.agents/skills/lanes/references/setup.md` for project
binding and credentials.

## Install the skill into one repository

```bash
scripts/install.sh ../my-project --dry-run
scripts/install.sh ../my-project
```

The repository installer copies the skill to `.agents/skills/lanes/` in the
target. It records the source revision in `.agents/sklanes-install.json`. It
never overwrites or removes a file that you edited after an install. It takes
over an unchanged copy that an older agent_gest_git_skills install left.
The repository installer needs `python3` and `git`.

## Use with the other skill packages

sklanes is the optional part of a combined install:

- **agent_gest_git_skills** has the Gest `g*` workflow skills.
- **jnterfaces** has the skills for the Justfile, jagt packets and cx.
- **sklanes** has the `lanes` skill.

The stack installer of agent_gest_git_skills installs all three. Each package
records its own source revision in the target:

```bash
../agent_gest_git_skills/scripts/install_stack.sh ../my-project --with-lanes
```

## Work on this repository

| Command | What it does |
|---|---|
| `just lint` | Checks the syntax of the scripts and the JSON. |
| `just test` | Runs the tests of the client and both installers. |
| `just check` | Runs `just lint` and `just test`. Every commit must pass it. |
| `just package-lint` | Checks `skill-package.json` with skill-package-maker. |

The skill came from agent_gest_git_skills, where it was added in pull request
49. This repository is now its source.
