import json,sqlite3
from pathlib import Path
from contextlib import contextmanager
from app.config import get_settings
SCHEMA="""
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password_hash TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS recommendation_history(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,planner_type TEXT NOT NULL,request_json TEXT NOT NULL,response_json TEXT NOT NULL,created_at TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
"""
def init_db():
 p:Path=get_settings().db_file;p.parent.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(p) as c:c.executescript(SCHEMA);c.execute('PRAGMA foreign_keys=ON')
@contextmanager
def get_db():
 p=get_settings().db_file;p.parent.mkdir(parents=True,exist_ok=True);c=sqlite3.connect(p);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON')
 try: yield c;c.commit()
 finally:c.close()
def create_user(name,email,password_hash):
 from datetime import datetime,timezone
 with get_db() as db:
  cur=db.execute('INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)',(name,email.lower().strip(),password_hash,datetime.now(timezone.utc).isoformat()))
  return dict(db.execute('SELECT id,name,email,created_at FROM users WHERE id=?',(cur.lastrowid,)).fetchone())
def find_user_by_email(email):
 with get_db() as db:
  r=db.execute('SELECT * FROM users WHERE email=?',(email.lower().strip(),)).fetchone();return dict(r) if r else None
def find_user_by_id(user_id):
 with get_db() as db:
  r=db.execute('SELECT id,name,email,created_at FROM users WHERE id=?',(user_id,)).fetchone();return dict(r) if r else None
def save_history(user_id,planner_type,request_data,response_data):
 from datetime import datetime,timezone
 with get_db() as db: db.execute('INSERT INTO recommendation_history(user_id,planner_type,request_json,response_json,created_at) VALUES(?,?,?,?,?)',(user_id,planner_type,json.dumps(request_data,ensure_ascii=False),json.dumps(response_data,ensure_ascii=False),datetime.now(timezone.utc).isoformat()))
def get_history(user_id,limit=20):
 with get_db() as db: rows=db.execute('SELECT id,planner_type,request_json,response_json,created_at FROM recommendation_history WHERE user_id=? ORDER BY id DESC LIMIT ?',(user_id,limit)).fetchall()
 return [{'id':r['id'],'planner_type':r['planner_type'],'request':json.loads(r['request_json']),'response':json.loads(r['response_json']),'created_at':r['created_at']} for r in rows]
