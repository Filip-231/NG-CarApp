# Django REST API 
database with Car and Rating models.    

App was deployed and maintained on AWS cloud services EC2:  
	`ec2-54-246-230-82.eu-west-1.compute.amazonaws.com:8080`    

Remember pass this link without: "https://"  

Main page:  `'help/'`    

## Environment:
- SECRET_KEY= #random key  
- ALLOWED_HOSTS= #hosts which uses this application (localhost)  


## Run the application locally

### Debug mode:   
```
git clone git@github.com:Filip-231/NG-CarApp.git 
sudo docker-compose build  
sudo docker-compose up    
```


### Run deployment version:  
```
git clone git@github.com:Filip-231/NG-CarApp.git
sudo docker-compose -f docker-compose-deploy.yml build  
sudo docker-compose -f docker-compose-deploy.yml up  
```

### Pull deployment version directly from ***DockerHub*** account:  
```
download docker-compose-deploy-from-dockerhub.yml  
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml pull  
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml up  
```


App is using nginx as proxy:    
- container with app: https://hub.docker.com/repository/docker/filip231/projectmyapi  
- container with proxy: https://hub.docker.com/repository/docker/filip231/projectproxy    
  
Debug mode Django configuration:  
```
	python -m venv env

	source env/bin/activate

	cd App

	pip install -r requirements.txt

	python manage.py test myapp/ #for tests

	python manage.py runserver
```	
	

For running with command "python manage.py runserver", remember to add in file: "app/myapi/settings.py" option DEBUG=1.  
This app is prepared for deployment.   
I added DEBUG=1 to environment values in docker-compose.yml file.  
To run it via python manage.py runserver that value need to be set.  

# Description
Application containing models of Cars and Ratings.  

Car:  
    make = models.CharField(max_length=100)  
    model = models.CharField(max_length=100)  
  
Rating:  
    Car = models.ForeignKey(Car, blank=True, null=True,on_delete=models.CASCADE)  
    value = models.IntegerField(blank=True, null=True)  
I decided to create new rating card for after each rate.
After scalling up this application to manage access of multiply users, they would be able to remove / update posted rating.    

Catalogue:  
    make=models.CharField(max_length=100)  
    available_models=models.CharField(max_length=10000)  

If I check first time avaliable models for specyfic make I save it to database.   
I did that for ruducing time wasted for accessing the same web page for the same data.  
If I want to add the same make one more time, instead of accessing once more time the web page, I check it in my downloaded catalogue.  

I know that, if the internet catalogue would be changed, during my application working, I would need to download one more time catalogue for already seen makes, or just delete records.  













