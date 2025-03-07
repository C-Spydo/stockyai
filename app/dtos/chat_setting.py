from pydantic import BaseModel

class ChatSetting(BaseModel):
    email: str
    prompt: str