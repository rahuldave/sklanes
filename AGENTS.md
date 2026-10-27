# Working on sklanes

This repository is the source of the `lanes` skill. Other repositories and the
global skill folders hold installed copies.

- Work on a `codex/*` topic branch, and open a reviewed pull request to `main`.
- Run `just check` before every commit.
- Write Markdown by the nossaifd writing guide, and check it with `just prose`.
- Do not add hooks, a daemon or credentials to the skill or its installers.
- A merge publishes the source only. Installed copies change only when someone
  runs an installer again.
