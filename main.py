from fastapi import FastAPI, Request, Body, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/pawradise", StaticFiles(directory="frontend"), name="frontend")

list_usernames=list()
templates=Jinja2Templates(directory="frontend")


class nameValue(BaseModel):
    Name: str
    Phone:int
    Email:str
    Age:int
    Vaccination:str


@app.get("/pawradise/main.html",response_class=HTMLResponse)
def write_home(request: Request):
    return templates.TemplateResponse("main.html",{"request":request})

@app.post("/submitform")
async def handle_form(Name: str = Form(...),Phone: int=Form(...),Email:str=Form(...),Age:int=Form(...),Vaccination: str=Form(...),intro:str=Form(...),Image:UploadFile=Form(...)):
    print(Name," ",Phone," ",Email," ",Age," ",Vaccination)
    print(intro)
    print(Image.filename)

# @app.get("/main/register.html",response_class=HTMLResponse)
# def write_register(request: Request):
#     return templates.TemplateResponse("register.html",{"request":request})

# @app.put("/username/{username}")
# def put_data(username:str):
#     print(username)
#     list_usernames.append(username)
#     return{
#         "usernames": username
#     }

# @app.post("/postData")
# def post_data(username:nameValue):
#     list_usernames.append(username)
#     return{
#         "usernames": username.name
#     }

# @app.delete("/deleteData/{username}")
# def delete_data(username:str):
#     print(username)
#     list_usernames.remove(username)
#     return{
#         "usernames": list_usernames
#     }

# @app.api_route("/homedata",methods=['GET','POST','PUT','DELETE'])
# def handle_data(username:str):
#     print(username)
#     return{
#         "name": username
#     }

    # content_assignment= await Image.read()
    # print (content_assignment)

# @app.post("/login/")
# async def login(username: str = Form(), password: str = Form()):
#     return {"username": username}

# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}