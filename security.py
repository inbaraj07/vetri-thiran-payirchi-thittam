from datetime import datetime,timedelta,timezone
import hashlib,hmac,secrets,jwt
from fastapi import HTTPException,status
ALGORITHM='HS256'
def hash_password(password):
 salt=secrets.token_bytes(16); digest=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,310000)
 return f'pbkdf2_sha256$310000${salt.hex()}${digest.hex()}'
def verify_password(password,stored):
 try:
  algorithm,rounds,salt_hex,digest_hex=stored.split('$')
  if algorithm!='pbkdf2_sha256': return False
  digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt_hex),int(rounds))
  return hmac.compare_digest(digest.hex(),digest_hex)
 except (ValueError,TypeError): return False
def create_access_token(user_id,email,secret_key,expires_minutes):
 now=datetime.now(timezone.utc); payload={'sub':str(user_id),'email':email,'iat':now,'exp':now+timedelta(minutes=expires_minutes)}
 return jwt.encode(payload,secret_key,algorithm=ALGORITHM)
def decode_access_token(token,secret_key):
 try: return jwt.decode(token,secret_key,algorithms=[ALGORITHM])
 except jwt.PyJWTError as exc: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid or expired access token',headers={'WWW-Authenticate':'Bearer'}) from exc
