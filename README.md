# Django REST API 
Simple API which allow to add the car to database if it exists in online catalogue, 
the car can be rated and all information can be viewed.

App was deployed and maintained on AWS cloud services EC2: `ec2-54-246-230-82.eu-west-1.compute.amazonaws.com:8080`    
Pass this link without: `https://`  

Page with all possible endpoints and documentations: `help/`    

## Environment

| **Variable**             | **Description**                | **Value**                  |
|--------------------------|--------------------------------|----------------------------|
| SECRET_KEY               | Django secret key              |    sjdlkadsasndkjasdnkasdn |
| ALLOWED_HOSTS            | Host of this app               |  0.0.0.0                   |


# How to run

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

# Description
Database contain models of Cars and Ratings.  

- Car:  
    - make = models.CharField(max_length=100)  
    - model = models.CharField(max_length=100)  
  
- Rating:  
    - Car = models.ForeignKey(Car, blank=True, null=True,on_delete=models.CASCADE)  
    - value = models.IntegerField(blank=True, null=True)  
 
I decided to create new rating card for after each rate.
After scalling up this application to manage access of multiply users, they would be able to remove / update posted rating.    

- Catalogue:  
   - make=models.CharField(max_length=100)  
   - available_models=models.CharField(max_length=10000)  

My App can only add the car to database if it exist in API catalogue.
After the first successful check if model exist, for the specific make, it is saved to database.   
That ruduce time spending for requesting the same endpoint for the same data.  
If later the same model will be added, instead of requesting car API, I check it in my database.  
If the online car API would be changed, I would need to refresh the database status.  













