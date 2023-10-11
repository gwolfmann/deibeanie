dei0 project using beanie and mongodb

Run with:

 uvicorn --reload server.app:app

1) Register

POST in /auth/register with:

{
    "email": "yourmail@mail.com",
    "password": "yourpass",
    "name": "yourname",
    "surname": "yoursurname",
    "alias": "youralias",
    "role": "yourrole"
}

2) Get your JWT

POST in /auth/jwt/login with 
username : yourmail@mail.com
password : yourpassw

as answer it returns your jwt token

3) use the jwt token as bearer auth for the rest of calls

4) logout
