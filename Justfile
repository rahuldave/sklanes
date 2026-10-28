# sklanes: every task is a recipe here. `just` lists them.

# Each word after a recipe's name reaches its commands whole, as "$1", "$2" and so on; "$@" is all of them
set positional-arguments

[private]
default:
    @just --list --unsorted

# Check the shell scripts, the JavaScript, the Python and the JSON for syntax
lint:
    bash -n scripts/install.sh
    node --check .agents/skills/lanes/scripts/lanes.mjs
    node --check .agents/skills/lanes/scripts/install.mjs
    python3 -m py_compile scripts/install_package.py tests/test_install_package.py
    python3 -m json.tool skill-package.json > /dev/null

# Run the tests of the Lanes client, its global installer and the repository installer
test:
    node --test tests/test_lanes.mjs
    python3 -m unittest discover -s tests -q

# Check skill-package.json with skill-package-maker at the commit that CI uses
package-lint:
    #!/usr/bin/env bash
    set -euo pipefail
    tool_root="$(mktemp -d)"
    trap 'rm -rf -- "$tool_root"' EXIT
    git clone --quiet https://github.com/rahuldave/agent_skill_package_maker.git "$tool_root/package-maker"
    git -C "$tool_root/package-maker" checkout --quiet 6a5938c49ca71c374dc1a234a4d15134c484a741
    uv run --no-project python "$tool_root/package-maker/skills/skill-package-maker/scripts/lint_skill_bundle.py" .

# Check the prose of the Markdown with nossaifd check.py, without front matter: just prose ~/Projects/nossaifd/check.py
prose checker:
    #!/usr/bin/env bash
    set -uo pipefail
    work="$(mktemp -d)"; trap 'rm -rf -- "$work"' EXIT; status=0
    for page in README.md AGENTS.md; do
        python3 "$1" "$page" || status=1
    done
    exit "$status"

# Everything a commit must pass: the lint and the tests
check:
    just lint
    just test

# Copy the lanes skill into a target repository. Extra arguments go to the installer: just install ../app --dry-run
install target *args:
    scripts/install.sh "$@"

# Check that each link to a skill of another package has a fallback, with the checker of a jnterfaces clone: just links ../jnterfaces
links jnterfaces="../jnterfaces":
    find .agents/skills -type f \( -name '*.md' -o -name '*.mjs' -o -name '*.sh' -o -name '*.yaml' \) -exec python3 "$1/scripts/check_skill_links.py" --package . --resolve "$1" {} +
