from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from app.config import get_settings
from app.database import create_user,find_user_by_email,get_history,save_history
from app.dependencies import get_current_user
from app.models import RegisterRequest,LoginRequest,TokenResponse,UserPublic,HomeRequest,PartyRequest,JewelryRequest,RecommendationResponse
from app.security import hash_password,verify_password,create_access_token
from app.services.gemini import GeminiService
router=APIRouter(prefix='/api',tags=['PocketSmart AI']);gemini=GeminiService()
def make_token(user): return create_access_token(user['id'],user['email'],get_settings().secret_key,get_settings().access_token_expire_minutes)
@router.post('/register',response_model=TokenResponse,status_code=201)
def register(p:RegisterRequest):
 if find_user_by_email(p.email): raise HTTPException(status_code=409,detail='An account with this email already exists')
 u=create_user(p.name.strip(),p.email,hash_password(p.password));return TokenResponse(access_token=make_token(u),user=UserPublic(**u))
@router.post('/login',response_model=TokenResponse)
def login(p:LoginRequest):
 u=find_user_by_email(p.email)
 if not u or not verify_password(p.password,u['password_hash']): raise HTTPException(status_code=401,detail='Invalid email or password')
 public={k:u[k] for k in ('id','name','email','created_at')};return TokenResponse(access_token=make_token(u),user=UserPublic(**public))
@router.post('/token',response_model=TokenResponse)
def token(p:LoginRequest): return login(p)
@router.get('/session-info')
def session_info(user=Depends(get_current_user)): return {'authenticated':True,'user_id':user['id'],'email':user['email'],'name':user['name']}
@router.get('/session-data')
def session_data(user=Depends(get_current_user)): return {'user':user,'recent_recommendations':get_history(user['id'],10)}
@router.get('/history')
def history(user=Depends(get_current_user)): return {'items':get_history(user['id'],50)}
@router.get('/recommendations-details/{history_id}')
def details(history_id:int,user=Depends(get_current_user)):
 items=[x for x in get_history(user['id'],100) if x['id']==history_id]
 if not items: raise HTTPException(status_code=404,detail='Recommendation not found')
 return items[0]
@router.post('/generate-home',response_model=RecommendationResponse)
def home(p:HomeRequest,user=Depends(get_current_user)):
 d=p.model_dump();r=gemini.generate('home',d);save_history(user['id'],'home',d,r.model_dump());return r
@router.post('/generate-party',response_model=RecommendationResponse)
def party(p:PartyRequest,user=Depends(get_current_user)):
 d=p.model_dump();r=gemini.generate('party',d);save_history(user['id'],'party',d,r.model_dump());return r
@router.post('/generate-jewelry',response_model=RecommendationResponse)
async def jewelry(budget:float=Form(...),currency:str=Form('INR'),occasion:str=Form(...),style:str=Form('Elegant'),outfit_description:str=Form(''),notes:str=Form(''),outfit_image:UploadFile|None=File(default=None),user=Depends(get_current_user)):
 p=JewelryRequest(budget=budget,currency=currency,occasion=occasion,style=style,outfit_description=outfit_description,notes=notes);image_bytes=None;mime=None
 if outfit_image:
  if outfit_image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(status_code=400,detail='Only JPEG, PNG or WebP images are supported')
  image_bytes=await outfit_image.read()
  if len(image_bytes)>get_settings().max_upload_mb*1024*1024: raise HTTPException(status_code=413,detail=f"Image must be <= {get_settings().max_upload_mb} MB")
  mime=outfit_image.content_type
 d=p.model_dump();r=gemini.generate('jewelry',d,image_bytes,mime);save_history(user['id'],'jewelry',{**d,'has_image':bool(image_bytes)},r.model_dump());return r
@router.get('/health')
def health(): return {'status':'ok','gemini_enabled':gemini.enabled,'model':get_settings().gemini_model}
