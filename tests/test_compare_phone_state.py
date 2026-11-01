"""对拍驱动自己管基线 worktree：未知 SHA 要报错，且不留下 worktree。"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests" / "compare_phone_state.py"


class BaselineTests(unittest.TestCase):
    def worktrees(self):
        return subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout

    def test_unknown_sha_fails_without_leaving_a_worktree(self):
        before = self.worktrees()
        proc = subprocess.run([sys.executable, str(SCRIPT), "--baseline", "0" * 40],
                              capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("找不到提交", proc.stderr)     # 守卫：走到了「拉基线失败」这一支
        self.assertEqual(self.worktrees(), before)


if __name__ == "__main__":
    unittest.main()
