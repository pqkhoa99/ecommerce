#### ASSIGNMENT 1       

### You must install Python3 and Pip3 to run this project
    > I suggest using Python 3.9.10 and Pip 21.3.1

### DATABASE: PostgreSQL
    > username: admin
    > password: admin
    > database_name: exe1

### CREATE AND ACTIVATE VITURAL ENVIROMENT
    > python3 -m venv env
    > source env/bin/activate

### INSTALL LIBRARY
    > pip3 install -r requirements.txt

### Make sure to run the initial migration commands to update the database.
    > flask db init
    > flask db migrate --message 'initial database migration'
    > flask db upgrade

### To run the project:
    > flask run

### NOTE: you need to create a user first (must be admin)
    > You can view all APIs on http://127.0.0.1:5000
    > To use other API, you need to run the login API first to get Authorization Token
# ecommerce
