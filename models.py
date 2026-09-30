from typing import Literal
from pydantic import BaseModel,Field
Currency=Literal['INR','USD','EUR','GBP']
class RegisterRequest(BaseModel): name:str=Field(min_length=2,max_length=80);email:str=Field(min_length=5,max_length=160);password:str=Field(min_length=8,max_length=128)
class LoginRequest(BaseModel): email:str;password:str
class UserPublic(BaseModel): id:int;name:str;email:str;created_at:str
class TokenResponse(BaseModel): access_token:str;token_type:str='bearer';user:UserPublic
class ItemRequest(BaseModel): name:str=Field(min_length=1,max_length=100);quantity:int=Field(default=1,ge=1,le=100)
class RoomRequest(BaseModel): room_type:str=Field(min_length=1,max_length=80);quantity:int=Field(default=1,ge=1,le=20);items:list[ItemRequest]=Field(default_factory=list)
class HomeRequest(BaseModel): budget:float=Field(gt=0,le=100_000_000);currency:Currency='INR';rooms:list[RoomRequest]=Field(min_length=1,max_length=20);style:str=Field(default='Modern',max_length=80);notes:str=Field(default='',max_length=1000)
class PartyRequest(BaseModel): budget:float=Field(gt=0,le=100_000_000);currency:Currency='INR';guest_count:int=Field(gt=0,le=100000);event_type:str=Field(min_length=2,max_length=80);venue:str=Field(default='',max_length=200);food_preference:str=Field(default='Mixed',max_length=100);notes:str=Field(default='',max_length=1000)
class JewelryRequest(BaseModel): budget:float=Field(gt=0,le=100_000_000);currency:Currency='INR';occasion:str=Field(min_length=2,max_length=100);style:str=Field(default='Elegant',max_length=100);outfit_description:str=Field(default='',max_length=1000);notes:str=Field(default='',max_length=1000)
class RecommendationItem(BaseModel): name:str;category:str;estimated_price:float;currency:str;platform:str;reason:str;search_url:str
class BudgetAllocation(BaseModel): category:str;amount:float;percentage:float
class RecommendationResponse(BaseModel): planner:str;title:str;summary:str;budget:float;currency:str;allocations:list[BudgetAllocation]=Field(default_factory=list);recommendations:list[RecommendationItem]=Field(default_factory=list);tips:list[str]=Field(default_factory=list);ai_generated:bool=False;disclaimer:str='Prices and availability are estimates; verify them on the linked platform.'
