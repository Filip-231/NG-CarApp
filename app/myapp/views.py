from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from myapp.models import Car, Rating, Catalogue
import json
import requests as req


@ensure_csrf_cookie
@csrf_exempt
def index(request):
    """Starting page"""
    # response = [{"Welcome message": "Hello!"}]
    # return JsonResponse(response, safe=False)
    return render(request,'myapp/index.html')

def help_view(request):
    "Returning page with documentation"
    return render(request, "myapp/documentation.html")




@ensure_csrf_cookie
@csrf_exempt
def get_car(request, id):
    """ Finding a car in database by id """
    if request.method == 'GET':

        try:
            car = Car.objects.get(id=id)
            rating = Rating.objects.get(Car=car)
            avg_rating=avg_rating_of_rating(rating)
            response = [{'id': car.id, 'Make': car.make,
                         'Model': car.model, 'avg_rating': avg_rating}]
            return JsonResponse(response, safe=False)
        except:
            response = [{"Error": "No car in database with that id!"}]
            return JsonResponse(response, status=404, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        print(response)
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def list_cars(request):
    """ Listing all cars with their ratings from database"""

    if request.method == 'GET':
        results = []

        for car in list(Car.objects.values()):
            rating = Rating.objects.get(Car=car['id'])
            avg_rating=avg_rating_of_rating(rating)
            results.append({'id': car['id'], 'make': car['make'], 'model': car['model'], 'avg_rating': avg_rating})
        return JsonResponse(results, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        print(response)
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def get_popular(request):
    """ List top two cars from database based on rates_number"""
    num_popular_cars=2
    
    if request.method == 'GET':
        results = []

        ratings=Rating.objects.order_by('-rates_number')[0:num_popular_cars]
        
        for rating in ratings:
            results.append({"id":rating.Car.id,"make":rating.Car.make,"model":rating.Car.model,"rates_number":rating.rates_number})
        
        return JsonResponse(results, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def delete_car(request, id):
    """Deleting car with given id"""
    if request.method == 'DELETE':
        try:
            car = Car.objects.get(id=id)
            car.delete()

            # to list cars after deleting:
            # data = list(Car.objects.values())
            # return JsonResponse(data, safe=False)

            response = [{"Success:": "Car successfuly deleted from database!"}]
            return JsonResponse(response, safe=False)

        except:
            response = [{'Error': 'No car with that ID'}]
            return JsonResponse(response, status=400, safe=False)

    else:
        response = [{"Error": "Method not allowed"}]
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def add_car(request, checkincatalogue=True):
    """
    Adding car with given make and model
    If you do not want to check in the catalogue set:
    checkincatalogue=False
    """

    if request.method == 'POST':

        try:
            payload = json.loads(request.body)
            make = payload['make']
            model = payload['model']

            if checkincatalogue:

                if not check_car(make.lower(), model.lower()):
                    response = [{'Error': 'Car does not exist in catalogue!'}]
                    return JsonResponse(response, status=400, safe=False)

                else:
                    print("Car is available in catalogue, adding to database!")

            try:
                Car.objects.get(make__iexact=make, model__iexact=model)
                response = [{"Error": "Car is already in database!"}]
                return JsonResponse(response, status=400, safe=False)
            except:
                create_car(make, model)
                response = [{"Success": "Car added successfully!"}]
            return JsonResponse(response, safe=False)
        
        except:
            response = [{"Error": "Car could not be added!"}]
            return JsonResponse(response, status=400, safe=False)

    elif(request.method == 'GET'):  # if we want to list all cars in database
        results = []
        for car in list(Car.objects.values()):
            rating = Rating.objects.get(Car=car['id'])

            avg_rating=avg_rating_of_rating(rating)
            results.append({'id': car['id'], 'make': car['make'],
                            'model': car['model'], 'avg_rating': avg_rating})

        return JsonResponse(results, safe=False)

    else:
        response = [{"Error": "Method not allowed"}]
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def rate_car(request):
    """Rating car with given id with integer number from 1 to 5"""
    if request.method == 'POST':

        # If not proper json entry data:
        # #{
        #    "car_id":28,
        #     "rating":1,
        #     }

        # payload=str(request.body)
        # print("converting payload: {}".format(payload[2:len(payload)-1]))
        # arr=format_string(payload[2:len(payload)-1])

        # if type(arr)!=list:
        #     response = [{ "Error": "Wrong Request"}]
        #     return JsonResponse(response,status=400,safe=False)

        # car_id=arr[0]
        # cur_rating=arr[1]

        try:
            # If normal json format data:
            payload = json.loads(request.body)
            car_id = payload['car_id']
            cur_rating = payload['rating']

            if not (type(cur_rating) == int and cur_rating >= 1 and cur_rating <= 5):
                response = [
                    {"Error": "Rating must integer bigger than 1 and smaller than 5!"}]
                return JsonResponse(response, status=400, safe=False)

            update_rating(car_id, cur_rating)

            rating = Rating.objects.get(Car=car_id)

            response = [{'car_id': car_id, 'rates_sum': rating.rates_sum,
                         'rates_number': rating.rates_number}]
            return JsonResponse(response, safe=False)
        
        except:
            response = [{'Error': 'Car could not be rated!'}]
            return JsonResponse(response, status=400, safe=False)

    else:
        response = [{"Error": "Method not allowed"}]
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def list_ratings(request):
    """ List all ratings in database """
    if request.method == 'GET':
        data = list(Rating.objects.values())
        return JsonResponse(data, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        print(response)
        return JsonResponse(response, status=405, safe=False)


@ensure_csrf_cookie
@csrf_exempt
def list_catalogue(request):
    """ List all ratings in database """
    if request.method == 'GET':
        data = list(Catalogue.objects.values())
        return JsonResponse(data, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        print(response)
        return JsonResponse(response, status=405, safe=False)


def create_car(make, model):
    """ creating new object in database with avg_rating and number_rates set to 0"""
    car = Car(make=make, model=model)
    car.save()
    rating = Rating(Car=car,rates_number=0, rates_sum=0)
    rating.save()


def update_rating(car_id, cur_rating):
    """ updating rating of car with id by cur_rating"""

    car = Car.objects.get(id=car_id)
    obj = Rating.objects.get(Car=car_id)

    # Can't do this that way: setting new avg_rating and updating rates_number
    #print("(rates*rating({}) + cur({}) )/ rates+1({}) == avg ({})".format(obj.rates_number*obj.avg_rating, cur_rating,obj.rates_number+1,(obj.rates_number*obj.avg_rating +cur_rating)/(obj.rates_number+1)))
    #obj.avg_rating=(obj.rates_number*obj.avg_rating +cur_rating)/(obj.rates_number+1)

    obj.rates_sum = obj.rates_sum+cur_rating
    obj.rates_number = obj.rates_number+1

    # proper calculation need to store data about rates_sum and rates_number
    #print("rates_sum :{} /  rates_numer:{}  = avg_rating {}".format(obj.rates_sum, obj.rates_number,obj.avg_rating))

    obj.save()


def check_car(make, model):
    """Checking in online catalogue form page: https://vpic.nhtsa.dot.gov/api/ if car exists"""
    # Firstly i will check if I maybe already checked that make?
    num_attempts=5
    try:
        data = Catalogue.objects.get(make=make.lower())
        available_models = data.available_models

        print("You checked that make already!")
        if model.lower() in available_models:  # return this
            return True
        else:
            return False
    except:
        print("I need to check in web catalogue, please be patient.")

    url = "https://vpic.nhtsa.dot.gov/api//vehicles/GetModelsForMake/" + \
        str(make)+"?format=json"


    while(num_attempts>0):
        try:
            print("accessing: {}".format(url))
            resp = req.get(url)
            if resp.status_code == 200:
                break
        except:
            print("Can't connect to page.. trying one more")
        num_attempts=num_attempts-1
    print("Status: {} - OK".format(resp.status_code))

    models_makes = resp.json()['Results']

    models = {elem['Model_Name'].lower() for elem in models_makes}
    print("new")
    print(models)

    #models={'golf iii', 'jetta sportwagen', 'new gti', 'golf gti', 'cabrio', 'gli', 'routan', 'gti', 'atlas', 'phaeton', 'corrado', 'new jetta', 'fox', 'arteon', 'new cabrio', 'quantum', 'kombi', 'rabbit', 'jetta iii', 'cabriolet', 'cc', 'passat', 'scirocco', 'e-golf', 'golf', 'golf r', 'euro van', 'vanagon', 'id.4', 'touareg', 'beetle', 'jetta wagon', 'multi-van', 'new passat', 'jetta', 'r32', 'tiguan limited', 'new golf', 'atlas cross sport', 'eos', 'golf sportwagen', 'dasher', 'golf alltrack', 'tiguan'}

    record = Catalogue(make=make, available_models=models)
    record.save()
    print(model in models)
    print("zwracam to nademna")
    return model in models



def avg_rating_of_rating(rating):
    """Counting average rating value for specific car"""
    avg_rating = 0.0
    if(rating.rates_number > 0):
        avg_rating = round(rating.rates_sum/rating.rates_number, 1)
    return(avg_rating)



def format_string(string):
    """ Getting data from not proper json format """
    string = string.replace(' ', '')
    try:
        s = string.split(":")
        s1 = s[1]
        s1 = int(s1.split(",")[0])
        s2 = s[2]
        s2 = int(s2.split(",")[0])
        return [s1, s2]
    except:
        print("Cannot find two values.")
