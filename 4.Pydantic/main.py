from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List,Dict,Optional,Annotated

class patient(BaseModel):
    name: Annotated[str,Field(max_length=25,title="name of the person",description="Give the name of the patient less then 25 characters",examples=['Maaz','khan'])]
    email: EmailStr
    linkdin_url: AnyUrl
    age: int = Field(gt=20,lt=50)
    weight: float = Field(gt=0)
    married: Annotated[bool,Field(default=False,description="The patient is married or not")]
    allergies: Optional[List[str]] = None
    contact_details: Dict[str,str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['htc.com','tech.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise TypeError("Not a valid domain")
        return value
    
    @field_validator('name')
    @classmethod
    def name_transformer(cls,value):
        return value.upper()
    
def insert(pat):
    print(pat.name)
    print(pat.email)
    print(pat.age)
    print(pat.weight)
    print(pat.allergies)
    for key,value in pat.contact_details.items():
        print(key+" => "+value)
    print("Inserted")

data = {'name':"Maaz",'email':'muhammadmaaz724@htc.com','linkdin_url':'https://www.youtube.com/watch?v=lRArylZCeOs&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&index=5','age':24,'weight':3,"contact_details":{'email':'abc@gmail.com','Phone':'4230489'}}

pat = patient(**data)

insert(pat)