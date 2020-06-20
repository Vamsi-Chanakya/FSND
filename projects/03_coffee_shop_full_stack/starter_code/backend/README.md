# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

# Post, Patch, Delete Request body and respective responses only for BARISTA Role which has read only access

##Payload for Barista Role:
```
{
  "iss": "https://vamsichanakya.auth0.com/",
  "sub": "auth0|5ecd5b766c12610c84980ae1",
  "aud": "coffeeshop",
  "iat": 1592676036,
  "exp": 1592683236,
  "azp": "GaBE90m9mMs90YQY0K7UIOAyiTBarsXU",
  "scope": "",
  "permissions": [
    "get:drinks-detail"
  ]
}
```

##Post New Drink:
###Response:
```
{
  "error": 401,
  "message": {
    "code": "not_authorized",
    "description": "Permission not found."
  },
  "success": false
}
```

##Patch Existing Drink:
###Response:
```
{
  "error": 401,
  "message": {
    "code": "not_authorized",
    "description": "Permission not found."
  },
  "success": false
}
```
##Delete Existing Drink:
### Response
```
{
  "error": 401,
  "message": {
    "code": "not_authorized",
    "description": "Permission not found."
  },
  "success": false
}
```

##Payload for Manager Role after JWT Decode :
```
{
  "iss": "https://vamsichanakya.auth0.com/",
  "sub": "auth0|5ecd5b8c6c12610c84980b5a",
  "aud": "coffeeshop",
  "iat": 1592675055,
  "exp": 1592682255,
  "azp": "GaBE90m9mMs90YQY0K7UIOAyiTBarsXU",
  "scope": "",
  "permissions": [
    "delete:drinks",
    "get:drinks-detail",
    "patch:drinks",
    "post:drinks"
  ]
}
```

##Post New Drink:
###Request :
```
{
    "title": "Vamsi8",
    "recipe": [
        {
            "name": "item1",
            "color": "yellow", 
            "parts": 1
        },
        {
        "name": "item2", 
        "color": "black", 
        "parts": 1
        }
    ]
}
```

###Response:
```
{
  "drinks": [
    {
      "id": 8,
      "recipe": [
        {
          "color": "yellow",
          "name": "item1",
          "parts": 1
        },
        {
          "color": "black",
          "name": "item2",
          "parts": 1
        }
      ],
      "title": "Vamsi8"
    }
  ],
  "success": true
}
```

##Patch Existing Drink:
###Request:
```
{
    "title": "Vamsi7",
    "recipe": [
        {
            "name": "item1",
            "color": "blue", 
            "parts": 1
        },
        {
        "name": "item2", 
        "color": "yellow", 
        "parts": 1
        },
        {
        "name": "item3", 
        "color": "red", 
        "parts": 1
        }
    ]
}
```
###Response:
```
{
  "drinks": [
    {
      "id": 7,
      "recipe": [
        {
          "color": "blue",
          "name": "item1",
          "parts": 1
        },
        {
          "color": "yellow",
          "name": "item2",
          "parts": 1
        },
        {
          "color": "red",
          "name": "item3",
          "parts": 1
        }
      ],
      "title": "Vamsi7"
    }
  ],
  "success": true
}
```

##Delete Drink:
###Response:
```
{
  "delete": "3",
  "success": true
}
```