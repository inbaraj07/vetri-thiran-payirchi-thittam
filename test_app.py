import os
from pathlib import Path
TEST_DB=Path('/tmp/pocketsmart_test.db')
if TEST_DB.exists(): TEST_DB.unlink()
os.environ['DATABASE_PATH']=str(TEST_DB);os.environ['SECRET_KEY']='test-secret';os.environ['GEMINI_API_KEY']=''
from fastapi.testclient import TestClient
from app.main import app
import pytest
@pytest.fixture
def client():
 with TestClient(app) as c: yield c
def auth(c):
 r=c.post('/api/register',json={'name':'Test User','email':'test@example.com','password':'password123'})
 if r.status_code==409:r=c.post('/api/login',json={'email':'test@example.com','password':'password123'})
 return {'Authorization':'Bearer '+r.json()['access_token']}
def test_health(client): assert client.get('/api/health').json()['status']=='ok'
def test_session(client): assert client.get('/api/session-info',headers=auth(client)).status_code==200
def test_home(client):
 r=client.post('/api/generate-home',headers=auth(client),json={'budget':50000,'currency':'INR','rooms':[{'room_type':'Living Room','quantity':1,'items':[{'name':'sofa','quantity':1}]}],'style':'Modern','notes':''});assert r.status_code==200 and r.json()['planner']=='home'
def test_party(client):
 r=client.post('/api/generate-party',headers=auth(client),json={'budget':30000,'currency':'INR','guest_count':25,'event_type':'Birthday','venue':'Vellore','food_preference':'Vegetarian','notes':''});assert r.status_code==200
def test_jewelry(client):
 r=client.post('/api/generate-jewelry',headers=auth(client),data={'budget':'20000','currency':'INR','occasion':'Wedding','style':'Elegant','outfit_description':'Blue saree','notes':''});assert r.status_code==200 and r.json()['planner']=='jewelry'
def test_history(client): assert isinstance(client.get('/api/history',headers=auth(client)).json()['items'],list)
