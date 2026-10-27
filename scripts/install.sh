#!/usr/bin/env bash
# Copy the lanes skill into a target repository: scripts/install.sh TARGET [--dry-run] [--source-commit REV]
# For the global CLI and native skill copies, run node .agents/skills/lanes/scripts/install.mjs instead.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for tool in python3 git; do # git --version and python3 run the repository installer
  if ! command -v "$tool" >/dev/null 2>&1; then
    printf 'Missing executable for the installer: %s\n' "$tool" >&2
    exit 1
  fi
done
if ! command -v node >/dev/null 2>&1; then
  echo 'Required executable not on PATH: node. The lanes command needs Node.js 22 or newer.' >&2
fi
exec python3 "$repo_root/scripts/install_package.py" --source "$repo_root" "$@"
