# Demaaiassignment

## Development Steps

1. DBeaver to connect mysql database, set up password and the settings
2. Create a database called DemaAI
3. Import two given datasets into the database
4. Use fastapi to develope two required endpoints

## How to run
1. git clone https://github.com/youshikyou/Demaaiassignment.git to local folder
2. cd to the folder
3. pip install -r requirements.txt
4. cd to app folder
5. uvicorn main:app --reload
6. go to http://127.0.0.1:8000/docs#/ to try out the endpoint

#### Note: there is no password in the database.py, so it cannot run if you don't set it up


## To improve
1. Use docker container to set up the python env
2. Integrate logging and monitoring to track API usage and error
3. Asynchronous database calls to handle requests to improve the performance under load
4. Enhance data validation logic in Pydantic models:page value contraints to not less than 0 , 
   category fields that should only accept a specific set of values
5. Environment configuration to use configuration files for managing files like database password
