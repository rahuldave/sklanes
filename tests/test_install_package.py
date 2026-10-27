"""Install the package into disposable target repositories and check every rule of the installer."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
RECORD = Path('.agents/sklanes-install.json')


def run(*args, cwd=None, check=True):
    return subprocess.run([str(arg) for arg in args], cwd=cwd, check=check, capture_output=True, text=True)


def git(path, *args):
    return run('git', '-C', path, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', *args).stdout.strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.source = root / 'source'
        shutil.copytree(REPO, self.source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        git(self.source, 'init', '-q')
        git(self.source, 'add', '-A')
        git(self.source, 'commit', '-q', '-m', 'source')
        self.target = root / 'target'
        self.target.mkdir()
        git(self.target, 'init', '-q')

    def tearDown(self):
        self.temp.cleanup()

    def install(self, *args, check=True):
        return run('bash', self.source / 'scripts/install.sh', self.target, *args, check=check)

    def record(self):
        return json.loads((self.target / RECORD).read_text())

    def commit_source(self):
        git(self.source, 'add', '-A')
        git(self.source, 'commit', '-q', '-m', 'change')

    def test_installs_the_skill_and_records_the_revision(self):
        self.install()
        record = self.record()
        self.assertEqual(record['package'], 'sklanes')
        self.assertEqual(record['skills'], ['lanes'])
        self.assertEqual(record['source_revision'], git(self.source, 'rev-parse', 'HEAD'))
        cli = self.target / '.agents/skills/lanes/scripts/lanes.mjs'
        self.assertEqual(record['managed_files'][cli.relative_to(self.target).as_posix()], sha(cli))

    def test_dry_run_writes_nothing(self):
        self.assertIn('Would install', self.install('--dry-run').stdout)
        self.assertFalse((self.target / '.agents').exists())

    def test_refuses_to_overwrite_an_edited_file(self):
        self.install()
        skill = self.target / '.agents/skills/lanes/SKILL.md'
        skill.write_text('edited\n')
        (self.source / '.agents/skills/lanes/SKILL.md').write_text('---\nname: lanes\ndescription: new\n---\n')
        self.commit_source()
        self.assertNotEqual(self.install(check=False).returncode, 0)
        self.assertEqual(skill.read_text(), 'edited\n')

    def test_takes_over_the_copy_that_agent_gest_git_skills_installed(self):
        old = self.target / '.agents/skills/lanes/references/setup.md'
        old.parent.mkdir(parents=True)
        old.write_text('old setup from agent_gest_git_skills\n')
        record = {'managed_files': {'.agents/skills/lanes/references/setup.md': sha(old)}}
        (self.target / '.agents/gest-git-install.json').write_text(json.dumps(record))
        self.install()
        self.assertEqual(old.read_bytes(), (self.source / '.agents/skills/lanes/references/setup.md').read_bytes())
        self.assertIn('.agents/skills/lanes/references/setup.md', self.record()['managed_files'])

    def test_removes_an_unchanged_file_that_the_source_dropped(self):
        self.install()
        (self.source / '.agents/skills/lanes/agents/openai.yaml').unlink()
        self.commit_source()
        self.install()
        self.assertFalse((self.target / '.agents/skills/lanes/agents').exists())

    def test_rejects_a_recorded_path_outside_the_skills(self):
        victim = Path(self.temp.name) / 'victim.txt'
        victim.write_text('keep me\n')
        (self.target / '.agents').mkdir()
        (self.target / RECORD).write_text(json.dumps({'managed_files': {'../victim.txt': sha(victim)}}))
        self.assertNotEqual(self.install(check=False).returncode, 0)
        self.assertTrue(victim.exists())


    def test_a_case_only_rename_keeps_the_new_file(self):
        self.install()
        git(self.source, 'mv', '.agents/skills/lanes/references/setup.md', '.agents/skills/lanes/references/Setup.md')
        self.commit_source()
        self.install()
        names = os.listdir(self.target / '.agents/skills/lanes/references')
        self.assertEqual(names, ['Setup.md'])
        self.assertIn('.agents/skills/lanes/references/Setup.md', self.record()['managed_files'])
        self.assertNotIn('.agents/skills/lanes/references/setup.md', self.record()['managed_files'])

    def test_never_removes_files_of_a_skill_that_is_not_in_the_package(self):
        other = self.target / '.agents/skills/mine/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('a skill of the user\n')
        (self.target / '.agents').mkdir(exist_ok=True)
        (self.target / RECORD).write_text(json.dumps({'managed_files': {'.agents/skills/mine/SKILL.md': sha(other)}}))
        self.install()
        self.assertEqual(other.read_text(), 'a skill of the user\n')
        self.assertNotIn('.agents/skills/mine/SKILL.md', self.record()['managed_files'])


if __name__ == '__main__':
    unittest.main()
