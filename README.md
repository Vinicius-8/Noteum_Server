# Noteum_Server
![FastAPI](https://img.shields.io/badge/FastAPI-0.54.1-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.7.7-yellow?style=flat-square)

A REST API Server to be cosumed by [Noteum](https://github.com/Vinicius-8/Noteum)

## Installation
Clone the repo and install the dependencies in requirements.txt

```
$ git clone https://github.com/Vinicius-8/Noteum_Server.git
$ pip install -r requirements.txt
```

## Requirements  
Create a file called __credentials.py__ and put your OAUTH 2.0 client ID to use the google API for authentication, as follows:  
```py
ANDROID_CLIENT_ID = "<yourid>"
```

## Run

```bash
$ uvicorn main:app --reload --host 0.0.0.0
```
