import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    spec=importlib.util.spec_from_file_location('workbench_subject',ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
m=load('workspace.py')
class Tests(unittest.TestCase):
    def test_persist_and_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'tasks.db';w=m.Workspace(path);key=w.add('Check evidence',1,'source note');w.move(key,'done');w.close()
            w=m.Workspace(path);rows=w.list();self.assertEqual(rows[0]['status'],'done');self.assertEqual(rows[0]['evidence'],'source note');w.close()
    def test_invalid_transitions(self):
        w=m.Workspace(':memory:')
        with self.assertRaises(ValueError):w.add(' ',2)
        with self.assertRaises(ValueError):w.move('missing','invalid')
        with self.assertRaises(KeyError):w.move('missing','done')
        w.close()

if __name__=='__main__':unittest.main()
