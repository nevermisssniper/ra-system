"""New starter: a local task/evidence workspace, with no account integrations."""
import argparse,json,sqlite3,uuid
from datetime import datetime,timezone

class Workspace:
    def __init__(self,path='workspace.sqlite3'):
        self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,title TEXT NOT NULL,status TEXT NOT NULL,priority INTEGER NOT NULL,evidence TEXT NOT NULL,created_at TEXT NOT NULL)')
    def add(self,title,priority=2,evidence=''):
        if not title.strip() or priority not in (1,2,3):raise ValueError('Title and priority 1-3 required')
        key=str(uuid.uuid4())
        with self.db:self.db.execute('INSERT INTO tasks VALUES(?,?,?,?,?,?)',(key,title.strip(),'inbox',priority,evidence,datetime.now(timezone.utc).isoformat()))
        return key
    def move(self,key,status):
        if status not in ('inbox','doing','done'):raise ValueError('Invalid status')
        with self.db:
            result=self.db.execute('UPDATE tasks SET status=? WHERE id=?',(status,key))
            if result.rowcount!=1:raise KeyError(key)
    def list(self):
        return [dict(zip(('id','title','status','priority','evidence','created_at'),r)) for r in self.db.execute('SELECT * FROM tasks ORDER BY priority,created_at')]
    def close(self):self.db.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--database',default='workspace.sqlite3');p.add_argument('--add');p.add_argument('--priority',type=int,default=2);a=p.parse_args();w=Workspace(a.database)
    if a.add:w.add(a.add,a.priority)
    print(json.dumps(w.list(),indent=2));w.close()
