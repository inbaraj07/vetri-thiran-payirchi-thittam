from pathlib import Path
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.database import init_db
from app.routes.api import router
BASE_DIR=Path(__file__).resolve().parent
app=FastAPI(title='PocketSmart AI',description='Smart budget and recommendation assistant',version='1.0.0')
s=get_settings();app.add_middleware(CORSMiddleware,allow_origins=s.origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.mount('/static',StaticFiles(directory=BASE_DIR/'static'),name='static');templates=Jinja2Templates(directory=BASE_DIR/'templates');app.include_router(router)
@app.on_event('startup')
def startup(): init_db()
def page(name):
 def f(request:Request): return templates.TemplateResponse(name,{'request':request})
 return f
@app.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse('index.html',{'request':request})
app.add_api_route('/login',page('login.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/register',page('register.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/dashboard',page('dashboard.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/planner/home',page('home_planner.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/planner/party',page('party_planner.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/planner/jewelry',page('jewelry_planner.html'),methods=['GET'],response_class=HTMLResponse)
app.add_api_route('/history',page('history.html'),methods=['GET'],response_class=HTMLResponse)
