Simple Api with django containing database with car and rating models.

Link to public host:
	ec2-54-246-230-82.eu-west-1.compute.amazonaws.com:8080/

Rember without: "https://" 

For avaliable links go to: 'help/'  

-------------------------------RUNNING APP locally-------------------------------------

To run it locally for debug mode:/ 
git clone this-repository/
sudo docker-compose build/
sudo docker-compose up/
/

To run it locally deployment version using files:/
git clone this-repository/
sudo docker-compose -f docker-compose-deploy.yml build/
sudo docker-compose -f docker-compose-deploy.yml up/


To pull it directly from my dockerhub for deployment:/
download docker-compose-deploy-from-dockerhub.yml/
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml pull/
sudo docker-compose -f docker-compose-deploy-from-dockerhub.yml up/

app is runing with nginx as proxy:/
/
container with app: https://hub.docker.com/repository/docker/filip231/projectmyapi/
container with proxy: https://hub.docker.com/repository/docker/filip231/projectproxy/
/
Or for debug mode using virtual env:/

	python -m venv env

	source env/bin/activate

	cd App

	pip install -r requirements.txt

	
	python manage.py test myapp/ #for tests

	python manage.py runserver
	
	

For running with python manage.py runserver - emember to add in app/myapi/settings.py/ option DEBUG=1./
This app is prepared for deployment,/
I added DEBUG=1 to environment values in docker-compose.yml file./
To run it via python manage.py runserver that value need to be set./

------------------------------------Short description-----------------------------------/
Application containing models of Cars and Ratings./

Car:/
    make = models.CharField(max_length=100)/
    model = models.CharField(max_length=100)/
/
Rating:/
    Car = models.ForeignKey(Car, blank=True, null=True,on_delete=models.CASCADE)/
    rates_number = models.IntegerField(blank=True, null=True)/
    rates_sum = models.IntegerField(blank=True, null=True)/

Catalogue:/
    make=models.CharField(max_length=100)
    available_models=models.CharField(max_length=10000)

If I check avialable models for make for the first time i decided to save it to database. 
I did that for ruducing time accessing that web page for the same data.
If I want to add the same make one more time: 
instead of accessing once more time the web page I check it in my catalogue.

I know that if the internet catalogue would change, during my application working, I would need to download one more time catalogue for already seen makes, or just delete records.













