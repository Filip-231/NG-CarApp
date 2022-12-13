# Django REST API 
REST API to add, delete, update the car information if it exists in external online catalogue.
The car can be rated and all information can be viewed and manage.

There is a configuration which allow serving static files using `NginX` and `/help` page with documented all of the enpoints.

![Demo](Demo-NG-CarApp.gif)

## Table of contents
  - [Description](#description)
  - [Technologies](#technologies)
  - [Environment](#environment)
  - [How to run](#how-to-run)
  - [Documentation](#documentation-cars-api)
  - [Cars management](#-collection-cars-management)
  - [Dashboard](#-collection-dashboard)


## Description
Database contain models of Cars and Ratings.  

- Car:  
    - make - make name, string field
    - model - model name, string field
  
- Rating:  
    - Car - car object foregin key relation, cascade delete   
    - value - rating value, integer field  
 
New rating card will be created after each rate.
This allows to easy remove or update posted rating.    

- Catalogue:  
   - make - cached make
   - available_models - cached models for a given make 

My App can only add the car to database if it exist in API catalogue.
After the first successful check if model exist, for the specific make, it is saved to database.   
That ruduce time spending for requesting the same endpoint for the same data.  
If later the same model will be added, instead of requesting car API, I check it in my database.  
If the online car API would be changed, I would need to refresh the database status.  


## Technologies
- django
- rest_framework
- django tests
- serializers
- SQLite
- requests
- random
- docker
- docker-compose
- AWS
- NginX
- UWSGI

App was deployed and maintained on AWS cloud services EC2:  

`ec2-54-246-230-82.eu-west-1.compute.amazonaws.com:8080`    

Pass this link without: `https://`  

Page with all endpoints and documentation: `help/`    

## Environment

| **Variable**             | **Description**                | **Value**                  |
|--------------------------|--------------------------------|----------------------------|
| SECRET_KEY               | Django secret key              |    sjdlkadsasndkjasdnkasdn |
| ALLOWED_HOSTS            | Host of this app               |  0.0.0.0                   |


## How to run

### Debug mode:   
```
git clone git@github.com:Filip-231/NG-CarApp.git 
sudo docker-compose build  
sudo docker-compose up    
```


### Production mode:  
```
git clone git@github.com:Filip-231/NG-CarApp.git
sudo docker-compose -f docker-compose-deploy.yml build  
sudo docker-compose -f docker-compose-deploy.yml up  
```

### Pull production version directly from ***DockerHub*** account:  
```
download docker-compose-deploy-from-dockerhub.yml  
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml pull  
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml up  
```

App is using nginx as proxy:    
- [container with app](https://hub.docker.com/repository/docker/filip231/projectmyapi)  
- [container with proxy](https://hub.docker.com/repository/docker/filip231/projectproxy)
  
### Debug mode Django configuration:  
```
python -m venv env

source env/bin/activate

cd App

pip install -r requirements.txt

python manage.py test myapp/ #for tests

python manage.py runserver
```	
	
When starting with `python manage.py runserver`, add to file: `app/myapi/settings.py` option `DEBUG=1`.  
This app is prepared for deployment `DEBUG=1` is exported to environment values in docker-compose.yml file.  

# Documentation Cars API
## 📁 Collection Cars management


## End-point: Add car
Adding car to database.
### Method: POST
>```
>{{URL}}cars/
>```
### Headers

|Content-Type|Value|
|---|---|
|Content-Type|application/json|


### Body (**raw**)

```json
{
    "make":"bmw",
    "model":"m2"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Delete car with id
Deleting car from database.
### Method: DELETE
>```
>{{URL}}cars/21/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Rate car
Adding rating to car with id.
### Method: POST
>```
>{{URL}}rate/
>```
### Headers

|Content-Type|Value|
|---|---|
|Content-Type|application/json|


### Body (**raw**)

```json
{
    "car_id":24,
    "rating":1
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: List cars
List every car in database with their current average rate.
### Method: GET
>```
>{{URL}}cars/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Popular
Get most popular cars in database
### Method: GET
>```
>{{URL}}popular/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
## 📁 Collection Dashboard 


## End-point: Index
Hello page.
### Method: GET
>```
>{{URL}}
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Catalogue list
Listing already downloaded catalogue.
### Method: GET
>```
>{{URL}}raw/catalogue/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Ratings list
List all ratings in database.
### Method: GET
>```
>{{URL}}rate/
>```
### Headers

|Content-Type|Value|
|---|---|
|Content-Type|application/json|



⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Help
Help page with all queries.
### Method: GET
>```
>{{URL}}help/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
_________________________________________________













