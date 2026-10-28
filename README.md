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

If `node` is not on the machine, uv runs it. Put
`uvx --from 'nodejs-wheel==24.*'` in front of each command, for example
`uvx --from 'nodejs-wheel==24.*' node .agents/skills/lanes/scripts/install.mjs`.

The installer copies the command to `~/.local/bin/lanes` and the skill to the
skill folders of Codex and Claude. It records hashes and the source revision in
`~/.local/share/lanes/install.json`. It changes no hooks, settings or
credentials. Read `.agents/skills/lanes/references/setup.md` for project
binding and credentials.

## Install the skill into one repository

jnterfaces installs the skill in the role `reporter`. In a project with
jnterfaces, run this command:

```bash
just install reporter
```

The installer of jnterfaces clones this repository and copies the skill to
`.agents/skills/lanes/`. It records the source revision in
`.agents/sklanes-install.json`. It never overwrites or removes a file that you
edited after an install. `just uninstall reporter` takes the skill out again.
This repository has no installer of its own for a repository.

## Use with the other skill packages

sklanes is the optional part of a combined install:

- **agent_gest_git_skills** has the Gest `g*` workflow skills.
- **jnterfaces** has the skills for the Justfile, jagt packets and cx.
- **sklanes** has the `lanes` skill.

The `just install` recipe of jnterfaces installs all three. Each package
records its own source revision in the target:

```bash
just install tasker reporter
```

## Work on this repository

| Command | What it does |
|---|---|
| `just lint` | Checks the syntax of the scripts and the JSON. |
| `just test` | Runs the tests of the client and of its global installer. |
| `just check` | Runs `just lint` and `just test`. Every commit must pass it. |
| `just package-lint` | Checks `skill-package.json` with skill-package-maker. |

The skill came from agent_gest_git_skills, where it was added in pull request
49. This repository is now its source.

## License

MIT. See [LICENSE](LICENSE).
