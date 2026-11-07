import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/caffrey-prd-plus/scripts/make_bundle.py'
spec = importlib.util.spec_from_file_location('make_bundle', SCRIPT)
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class BundleTest(unittest.TestCase):
    def test_render_failure_does_not_create_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'bundle'
            (root / 'pages').mkdir(parents=True)
            (root / 'pages/01.md').write_text('# 示例\n\n```mermaid\ngraph TD\nA-->B\n```\n', encoding='utf-8')
            with patch.object(bundle, 'mermaid_to_png', return_value=''), \
                 patch.object(sys, 'argv', ['make_bundle.py', str(root)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    bundle.main()
            self.assertFalse(root.with_suffix('.zip').exists())


if __name__ == '__main__':
    unittest.main()
