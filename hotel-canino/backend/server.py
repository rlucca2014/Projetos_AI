from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sqlite3, json, datetime, os
from decimal import Decimal, InvalidOperation
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parent.parent
DB=Path(os.environ.get('HOTEL_DB_PATH', str(ROOT/'backend'/'hotel.db')))
@contextmanager
def connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 try:
  with c: yield c
 finally: c.close()
def init():
 DB.parent.mkdir(parents=True,exist_ok=True)
 with connect() as c:
  c.executescript('CREATE TABLE IF NOT EXISTS dogs(id INTEGER PRIMARY KEY,name TEXT NOT NULL,breed TEXT,owner TEXT NOT NULL,phone TEXT NOT NULL,tag TEXT UNIQUE,notes TEXT); CREATE TABLE IF NOT EXISTS stays(id INTEGER PRIMARY KEY,dog_id INTEGER NOT NULL,start TEXT NOT NULL,end TEXT NOT NULL,status TEXT NOT NULL DEFAULT "reserved",checkin TEXT,checkout TEXT); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,tag TEXT,message TEXT,created TEXT);')
  c.execute('CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY,rate_cents INTEGER NOT NULL)')
  c.execute('INSERT OR IGNORE INTO settings VALUES(1,11000)')
  if 'rate_cents' not in [r['name'] for r in c.execute('PRAGMA table_info(stays)')]:
   c.execute('ALTER TABLE stays ADD COLUMN rate_cents INTEGER NOT NULL DEFAULT 11000')
def state(c):
 data={k:[dict(r) for r in c.execute(q)] for k,q in {'dogs':'SELECT * FROM dogs ORDER BY id DESC','stays':'SELECT stays.*,dogs.name,dogs.owner FROM stays JOIN dogs ON dogs.id=stays.dog_id ORDER BY stays.id DESC','events':'SELECT * FROM events ORDER BY id DESC LIMIT 10'}.items()}
 data['rate_cents']=c.execute('SELECT rate_cents FROM settings WHERE id=1').fetchone()[0]
 for stay in data['stays']:
  stay['nights']=(datetime.date.fromisoformat(stay['end'])-datetime.date.fromisoformat(stay['start'])).days
  stay['total_cents']=stay['nights']*stay['rate_cents']
 return data

class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/'frontend'),**kw)
 def send_json(self,data,status=200):
  b=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=='/api/state':
   with connect() as c: self.send_json(state(c))
  else: super().do_GET()
 def do_POST(self):
  try:
   size=int(self.headers.get('Content-Length','0'))
   if size>20000: raise ValueError('Dados excedem o limite.')
   d=json.loads(self.rfile.read(size)); now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
   with connect() as c:
    if self.path=='/api/dogs':
     for f in ['name','owner','phone']:
      if not str(d.get(f,'')).strip(): raise ValueError('Preencha nome do cão, tutor e telefone.')
     c.execute('INSERT INTO dogs(name,breed,owner,phone,tag,notes) VALUES(?,?,?,?,?,?)',[str(d.get(k,'')).strip() or None for k in ['name','breed','owner','phone','tag','notes']])
    elif self.path=='/api/stays':
     start=datetime.date.fromisoformat(d['start']);end=datetime.date.fromisoformat(d['end'])
     if end<=start: raise ValueError('A saída deve ser posterior à entrada.')
     if not c.execute('SELECT id FROM dogs WHERE id=?',(d['dog_id'],)).fetchone(): raise ValueError('Cão não encontrado.')
     if c.execute('SELECT id FROM stays WHERE dog_id=? AND status!="departed" AND start<? AND end>?',(d['dog_id'],str(end),str(start))).fetchone(): raise ValueError('Este cão já tem uma estadia no período.')
     rate=c.execute('SELECT rate_cents FROM settings WHERE id=1').fetchone()[0]
     c.execute('INSERT INTO stays(dog_id,start,end,rate_cents) VALUES(?,?,?,?)',(d['dog_id'],str(start),str(end),rate))
    elif self.path=='/api/transition':
     s=c.execute('SELECT * FROM stays WHERE id=?',(d['id'],)).fetchone()
     if not s: raise ValueError('Estadia não encontrada.')
     if s['status']=='reserved':
      if c.execute('SELECT id FROM stays WHERE dog_id=? AND status="present"',(s['dog_id'],)).fetchone(): raise ValueError('Este cão já está hospedado.')
      c.execute('UPDATE stays SET status="present",checkin=? WHERE id=?',(now,s['id']))
     elif s['status']=='present': c.execute('UPDATE stays SET status="departed",checkout=? WHERE id=?',(now,s['id']))
     else: raise ValueError('Esta estadia já foi encerrada.')
    elif self.path=='/api/rate':
     try: rate=Decimal(str(d['rate']).replace(',','.'))
     except InvalidOperation: raise ValueError('Informe uma diária válida.')
     if not rate.is_finite() or rate<=0 or rate>100000 or rate!=rate.quantize(Decimal('0.01')): raise ValueError('Informe valor positivo com até duas casas decimais e no máximo R$ 100.000.')
     c.execute('UPDATE settings SET rate_cents=? WHERE id=1',(int(rate*100),))
    elif self.path=='/api/scan':
     dog=c.execute('SELECT * FROM dogs WHERE tag=?',(d.get('tag','').strip(),)).fetchone()
     if not dog: raise ValueError('Coleira não cadastrada. Vincule o código no cadastro do cão.')
     msg='Identificado: '+dog['name']+' · leitura simulada; confirme a operação na estadia.'
     c.execute('INSERT INTO events(tag,message,created) VALUES(?,?,?)',(dog['tag'],msg,now))
    else: self.send_json({'error':'Rota não encontrada'},404);return
   self.send_json({'ok':True})
  except sqlite3.IntegrityError: self.send_json({'error':'Este código de coleira já está vinculado a outro cão.'},409)
  except (ValueError,KeyError,TypeError) as e: self.send_json({'error':str(e)},400)
if __name__=='__main__':
 init();print('Hotel canino: http://localhost:4180',flush=True);ThreadingHTTPServer((os.environ.get('HOST','127.0.0.1'),int(os.environ.get('PORT','4180'))),Handler).serve_forever()


