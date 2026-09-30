from fastapi import Depends,Header,HTTPException,status
from app.config import get_settings
from app.database import find_user_by_id
from app.security import decode_access_token
def get_current_user(authorization:str|None=Header(default=None)):
 if not authorization or not authorization.lower().startswith('bearer '): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Bearer token required')
 payload=decode_access_token(authorization.split(' ',1)[1],get_settings().secret_key)
 try: user_id=int(payload['sub'])
 except (KeyError,ValueError): raise HTTPException(status_code=401,detail='Invalid token subject')
 user=find_user_by_id(user_id)
 if not user: raise HTTPException(status_code=401,detail='User not found')
 return user
