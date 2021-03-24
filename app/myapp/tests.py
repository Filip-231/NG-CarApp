from collections import OrderedDict
from django.test import TestCase, Client
from myapp.models import Car, Rating
from myapp.views import create_car, update_rating
import json
import requests
import random as r


def get_sample(test_makes_models):
    """Generating random ordered dict from given dict with test_makes_models"""
    order_input = OrderedDict()

    i = r.randint(0, len(test_makes_models))
    for make in r.sample(test_makes_models.keys(), i):
        models = test_makes_models[make]
        models = r.sample(models, r.randint(0, len(models)))

        if models:
            order_input[make] = models

    return order_input


def generate_random_database(order_input):
    """Given random order_input generate database"""
    for make, models in order_input.items():
        for model in models:
            print("Adding car with make: {} model: {}.".format(make, model))
            create_car(make, model)


def retrive_wanted_response(order_input):
    """Retriving proper server answer after adding cars from ordered dict"""
    id_num = 1
    wanted_response = []
    for make, models in order_input.items():
        for model in models:
            wanted_response.append({
                "id": id_num,
                "make": make,
                "model": model,
                "avg_rating": 0.0
            })
            id_num += 1

    return wanted_response


def rate_random_cars(wanted_response,
                     max_number_of_randomly_generated_rates_per_car, test):
    """Rating random choosen cars from database"""
    rate_trace = {}
    random_number_cars_rated = r.randint(1, len(wanted_response))
    random_cars_ids = r.sample(range(1,
                                     len(wanted_response) + 1),
                               random_number_cars_rated)

    for random_id in random_cars_ids:
        random_rates_number = r.randint(
            1, max_number_of_randomly_generated_rates_per_car)

        rate_trace[random_id] = {'sum': 0, 'count': 0}

        print("Rating car with id: {} number of times: {}.".format(
            random_id, random_rates_number))

        for _ in range(0, random_rates_number):
            random_rate = r.randint(1, 5)
            rate_message = json.dumps({
                "car_id": random_id,
                "rating": random_rate
            })

            response = test.client.generic('POST', '/rate/', rate_message)
            test.assertEqual(response.status_code, 200)

            rate_trace[random_id]['sum'] += random_rate
            rate_trace[random_id]['count'] += 1

    return rate_trace


class test_functions(TestCase):
    """
    Testing functions which creates views and updates ratings.
    """
    def setUp(self):
        self.make1 = "Volkswagen"
        self.model1 = "Golf"
        self.make2 = "BMW"
        self.model2 = "M5"

    def test_create(self):
        create_car(self.make1, self.model1)
        create_car(self.make2, self.model2)
        car = Car.objects.get(model=self.model1)
        self.assertEqual(car.make, self.make1)

        car = Car.objects.get(model=self.model2)
        self.assertEqual(car.make, self.make2)

    def test_update_rating(self):
        car1_id = create_car(self.make1, self.model1)
        car2_id = create_car(self.make2, self.model2)

        update_rating(car1_id, 1)
        update_rating(car1_id, 1)
        update_rating(car2_id, 5)
        update_rating(car2_id, 1)

        avg_rating1 = Car.objects.get(id=car1_id).avg_rating
        avg_rating2 = Car.objects.get(id=car2_id).avg_rating

        self.assertEqual(avg_rating1, 1.0)
        self.assertEqual(avg_rating2, 3.0)


class test_views(TestCase):
    """Testing views"""
    def setUp(self):
        self.test_makes_models={"Volkswagen": {'Euro Van', 'ID.4', 'New Jetta', 'Atlas', 'Touareg', 'Jetta III', 'Tiguan Limited', 'Jetta', 'scirocco', 'KOMBI', 'e-Golf', 'Atlas Cross Sport', 'New Golf', 'GTI', 'Quantum', 'Arteon', 'Cabrio', 'Rabbit', 'Phaeton', 'MULTI-VAN', 'Corrado', 'CC', 'Golf', 'CABRIOLET', 'Eos', 'Golf III', 'Dasher', 'New GTI', 'Golf GTI', 'GLI', 'new Passat', 'New Cabrio', 'Vanagon', 'Tiguan', 'R32', 'Beetle', 'Passat', 'FOX', 'Golf R', 'Jetta SportWagen', 'Golf Alltrack', 'Jetta Wagon', 'Golf SportWagen', 'Routan'},\
                   "Honda": {'HR-V', 'NC700XDL/NC700X', 'ST1300', 'INTERCEPTOR', 'CBR954RR', 'NRX1800BA (VALKYRIE RUNE)', 'VT750 (Shadow Ace 750)', 'VTX1300T/VTX1300 (SPOKE)', 'VTX1800C2 (VTX)', 'SB50P', 'VT1100C2 (SHADOW ACE)', 'VTX1300S', 'PCX125', 'VTX1800R3/VTX1800R', 'TRX250', 'CB750 (Nighthawk 750)', 'SE50H', 'TRX400FW (FourTrax Foreman 400)', 'CH150', 'CRF250', 'Tourist Trophy', 'VTX1800R/VTX1800 RETRO', 'TRX500 (Foreman)', 'CB550', 'XR500R', 'XR200R', 'XL350R', 'CR500R', 'CRF100F', 'CB300', 'NC700XD (NC700X DCT)', 'VT1300', 'NSS250AS (REFLEX SPORT)', 'XL250R', 'VTX1800R2/VTX1800R', 'TRX450ERB (SportTrax 450)', 'VTX1800C2/VTX1800C', 'VTX1800T1/VTX1800T', 'TRX450S', 'CB750', 'CRF150', 'ELITE 80', 'CB700', 'TRX350FM (FourTrax Rancher)', 'VTX1800C', 'NX250', 'VFR 750F', 'TRX250 (Recon)', 'VF1000R', 'CM250C', 'VT600C (SHADOW VLX)', 'VT750 (Shadow Phantom)', 'ST1300A/ST1300', 'TRX400FA', 'TRX500 (Rubicon)', 'VTX1800N2 (VTX)', 'Clarity', 'ELITE', 'CMX450C', 'NSA700A/DN-01', 'CR-Z', 'TRX650FGA (FourTrax Rincon)', 'NRX1800BB (VALKYRIE RUNE)', 'VTX1800S3 (VTX)', 'VFR1200FA', 'Shadow', 'CH250', 'VF500F', 'XL200R', 'FIREBLADE', 'CBR250', 'GL1500CF (VALKYRIE INTERSTATE)', 'CB1000', 'CBX', 'TRX400FGA (FourTrax Rancher AT)', 'VT1300 (Fury)', 'NPS50 (Ruckus)', 'VF750S', 'VTX1300T/VTX', 'TRX500', 'CBF1000A', 'TRX250 (FourTrax 250)', 'XR100R', 'CH80 (Elite)', 'TRX450FE (FourTrax Foreman)', 'SE50PH', 'VF750C2 (MAGNA)', 'CTX1300', 'CMX300 (Rebel 300)', 'Honda Utility Vehicle', 'GROM125', 'VTX1800N/VTX1800 NEO RETRO', 'RC 45', 'SA50', 'TRX300X', 'GL1500SE (GOLD WING SE)', 'CHF50 (Metropolitan)', 'VT1100D2', 'NC750X', 'VFR800A (INTERCEPTOR)', 'RVT1000R (RC51)', 'VT750 (Shadow)', 'Z125 (Monkey)', 'CHF50 (Jazz)', 'TRX400FG', 'TRX200D', 'VT750 (Aero)', 'TRX500 (Foreman Rubicon)', 'VTX1800F1 (VTX)', 'CG150ESD', 'VFR1200XD', 'TRX250 (FourTrax Recon)', 'TRX200DN', 'VTX1800N1/VTX1800N', 'TRX90 (Fourtrax 90)', 'VFR1200FAD/VFR1200FD', 'CHF50 (Metropolitan II)', 'VTX1800F', 'VTX1800R (VTX)', 'Ridgeline', 'XR400R', 'CBR1100XX', 'CRF110', 'CBR500', 'TRX90', 'VTX1800S1/VTX1800S', 'VT1300 (Sabre)', 'VFR800A', 'GL1500CT (VALKYRIE TOURER)', 'Pacific Coast', 'RC1000VS (RC213V-S)', 'NRX1800EA (VALKYRIE RUNE)', 'VT750 (Shadow Ace/Aero)', 'TRX350TE (FourTrax Rancher)', 'ADV150', 'VT600CD (SHADOW VLX DELUXE)', 'VFR800Fi (INTERCEPTOR)', 'TG50', 'XL1000V (VARADERO)', 'ST1300A', 'Odyssey', 'CMX500 (Rebel500)', 'TRX350FE (FourTrax Rancher)', 'CRF125', 'PC800 (PACIFIC COAST)', 'VTX1300T', 'GL1500A (GOLD WING ASPENCADE)', 'NH80', 'TRX650FG (Rincon)', 'CB250 (Nighthawk)', 'VFR800', 'FCX Clarity', 'VT750 (Shadow Spirit 750)', 'CB900 (919)', 'NT650J', 'CRF1000', 'TRX650FA (Rincon)', 'VTX1800C3 (VTX)', 'VT1300 (Stateline)', 'TRX650FA (FourTrax Rincon)', 'ST1100', 'TRX90 (SportTrax 90)', 'VF1100S', 'XR80R', 'FSC600 (Silver Wing)', 'XR250L', 'VTX1300R/VTX1300 (RETRO)', 'Z50R', 'TRX350TE', 'CB650', 'NT700V', 'VTR1000S (RC51)', 'TRX500 (FourTrax)', 'VTX1300R', 'Accord', 'CBR125', 'TRX300EXN', 'VTX1800R1 (VTX)', 'Civic', 'VTX1800R1/VTX1800R', 'TRX450ES', 'CRF450', 'NC700JD (NM4)', 'TRX400FG (FourTrax 400)', 'Shadow 1100', 'CRF70F', 'NSS250A (REFLEX)', 'GOLDWING', 'VTR1000F (SUPERHAWK)', 'Accord Crosstour', 'NSR50MIN', 'TRX250X', 'TRX450FM', 'CB599', 'TRX350TM', 'ST1100A', 'A1', 'VTX1300TL/VTX', 'TRX300FW', 'TLR200', 'GL1100 (GOLDWING)', 'NC700XL (NC700X)', 'VT1100C2 (SHADOW SABRE)', 'RVF750R (RC45)', 'CB125', 'TRX680 (Rincon)', 'VFR1200FAD', 'VTX1300RL/VTX1300R', 'TRX420 (Rancher)', 'CX650', 'CBF300', 'NX650',
                                        'VTX1800T/VTX1800T TOURER', 'MUV700 (Big Red)', 'CB-1', 'VT700C', 'CN250', 'VTX1300S (VTX)', 'VFR800F', 'Silverwing', 'XR250R', 'VTX1800F3 (VTX)', 'SE50PI', 'VTX1800F2 (VTX)', 'TRX700EX', 'CB450', 'CRF1000 (Africa Twin)', 'VFR800AT', 'METROPOLITAN', 'VTX1800F1/VTX1800F', 'VF700', 'TRX400EX', 'CB1100', 'TRX680 (FourTrax Rincon)', 'ELITE 250', 'NT700VA/NT700V', 'CB900 (Hornet)', 'VT600CD2', 'TRX350FM', 'NB50', 'VT1300 (Interstate)', 'CBF600SA', 'PCX150', 'VFR800 (INTERCEPTOR)', 'XL500S', 'TRX400FWN', 'VTX1800S (VTX)', 'CBR600', 'VF1000F', 'TRX420', 'Pilot', 'SXS1000 (Pioneer 1000)', 'VT1100T (SHADOW ACE TOURER)', 'VFR1200X', 'VTX1800C1 (VTX)', 'CX500', 'SXS10S2 (Talon 1000)', 'CTX700', 'CM450', 'Fit', 'TRX700XX', 'XL600R', 'CRF50', 'CBR300', 'VTX1800S2/VTX1800S', 'VT750 (A.C.E.)', 'VT1100C (SHADOW SPIRIT 1100)', 'CR-V', 'VFR800 (SPORT TOURER)', 'CBR900/CBR929', 'Hawk GT', 'Insight', 'XR650', 'NB50M', 'SH150I', 'TRX420 (FourTrax Rancher)', 'CR80', 'CRF80F', 'ST1300P', 'TRX300EX', 'VTX1800N3/VTX1800N', 'CBR900/CBR954', 'Pioneer', 'SXS700 (Pioneer 700)', 'VTX1800R3 (VTX)', 'CH125', 'TRX450ERB', 'Crosstour', 'NC700XD/NC700X', 'VTX1800N1 (VTX)', 'Cota 300RR (MRT300)', 'NSS300A (FORZA)', 'ELITE 50', 'XR200', 'Trail 125', 'TRX400FA (FourTrax Rancher AT)', 'VF750C (MAGNA)', 'NC750SA', 'CN250 (Helix)', 'Sportrax', 'VR700FII', 'CT70', 'GL1500 (Valkyrie)', 'TRX400EX (SportTrax 400)', 'TRX250 (SportTrax 250)', 'NCH50 (METROPOLITAN)', 'SH150D/SH150i', 'VT750 (Shadow Aero)', 'TRX500 (FourTrax Foreman)', 'MSX125/Grom', 'VTX1800S3/VTX1800S', 'VTX1300C (VTX)', 'VTX1800S2 (VTX)', 'VFR1200FD/VFR1200F', 'TRX450ER', 'CBR900', 'CR85', 'VTX1800F2/VTX1800F', 'NHX110 (ELITE 110)', 'CR125', 'NIGHTHAWK 750', 'NRX1800 (VALKYRIE RUNE)', 'XR70R', 'CBR650', 'NSS250S (REFLEX SPORT)', 'PS250 (BIG RUCKUS)', 'NQ50', 'VTX1800C1/VTX1800C', 'VTX1800C3/VTX1800C', 'XR50', 'NSS300 (FORZA)', 'Shadow VLX', 'TRX450R/TRX450ER', 'VFR1200FD/VFR1200FA', 'VF1100C', 'TRX450FM (FourTrax Foreman)', 'GL1500i', 'TRANSALP', 'VTX1800FD', 'XL600V', 'VTX1800ND', 'GL1500C (VALKYRIE)', 'SA50P', 'Passport', 'TRX450R', 'del Sol', 'NX125', 'TRX350TM (FourTrax Rancher)', 'MRT260/COTA 4RT/4RT 260', 'TRX500 (FourTrax Foreman Rubicon)', 'VT1100C', 'VTX1800N3 (VTX)', 'ST1300PA', 'VTX1800T2/VTX1800T', 'VTX1800S/VTX1800 SPOKE', 'CB500', 'S2000', 'TRX400FGA', 'EZ90', 'Element', 'CRF230', 'NRX1800EB (VALKYRIE RUNE)', 'VTX1800TD', 'XL80', 'TRX300FWN', 'MRT260/COTA 4RT260', 'CM200', 'VFR750R (RC30)', 'NN50MD', 'VT750', 'NC700X', 'VTX1800N2/VTX1800N', 'TRX400FW', 'CB900', 'CMX1100D (REBEL1100 DCT)', 'VT500C', 'NSS250 (REFLEX)', 'TRX350FE', 'GL1200 (GOLDWING)', 'Prelude', 'CBR1000', 'VF700C', 'XL100S', 'NRX1800DB (VALKYRIE RUNE)', 'VFR800AT (INTERCEPTOR ABS)', 'VT600C (VLX)', 'TRX300EX (SportTrax 300)', 'VTX1300RL/VTX', 'TRX450ER (SportTrax 450)', 'VF500C', 'CRF1100 (Africa Twin)', 'CMX250 (Rebel)', 'VTR', 'VTX1300C', 'VT1100C3 (SHADOW AERO)', 'WW150/PCX150', 'XL125', 'TRX400X', 'Helix', 'NC700XD', 'FourTrax', 'VTX1800R2 (VTX)', 'VFR800A (SPORT TOURER)', 'EV Plus', 'VTX1800C (VTX)', 'CMX1100A (REBEL1100)', 'XR600R', 'VTX1800F3/VTX1800F', 'ST1100P', 'TRX300', 'NS50F', 'NC700XDL (NC700X DCT)', 'CB600 (599)', 'NC750JD/NM4', 'NC700SA/NC700S', 'GL1800', 'GL1500CD (VALKYRIE TOURER)', 'CR250', 'NCW50/Metropolitan', 'NCH50 (GIORNO)', 'VT1100C2D (SABRE)', 'VFR800F (INTERCEPTOR)', 'Cota 300RR', 'VFR1200F', 'VTX1800S1 (VTX)', 'C125 (Super Cub)', 'NRX1800DA (VALKYRIE RUNE)', 'SXS500 (Pioneer 500)', 'TRX300N', 'VT800C'},\
                   "BMW":{'K1', '535i/535is', '750i / ALPINA B7', 'R 100 GS', 'R 1200 GS', 'HP2', 'R 1150 RS', '650i / ALPINA B6', '640i', '733i', '335xi', '633 csi', 'M4', '328i', '328xi', 'R 1100 S', 'C 650', 'R 80 RT', 'R 1250 RS', 'K 1200 RS', 'M760i', 'K 1600 B', 'R 1200 RS', 'F 650 GS', '428i', '735i', 'M2', 'F 650 CS', 'F 900', '535d', 'F 800 GS', 'K 1600 GT', '528xi', '325i', '525iA', 'M3', 'M6', '850CSi', '530iA', '750Li', '335d', '335i', 'B7', '730i', 'X7', '228i', '323i', '525xi', '740iL', 'F 650', 'K 1300 S', '340i', '135i', '325iC', 'C 400 GT', 'R 1200 C', '440i', '330xi', 'G 310 GS', '530i', 'K 1100 RS', 'F 750 GS', '745Li', '325e', 'R 80 ST', 'S 1000 RR', 'G 450 X', '535xi', '325iS', '540iA', '640xi', 'R 100 RT', 'M5', '430i', '524td', '533i', 'F 800 ST', 'F 800 S', 'R 1250 R', 'F 800 GT', 'i3', '545i', 'R 18 Classic', 'C 400 X', 'K100', '320i', 'R 65', '750xi', 'F 800 R', '528i', 'C 600', '760i', '325iT', 'K75RT', '530iT', 'Z8', '325ix', '740e', '328iS', 'R 100', '750Li / ALPINA B7', 'R 80', 'S 1000 XR', '540i', 'R 1250 RT', 'C Evolution', 'X4', '760Li', '645Cic', 'R 1200 ST', '750iL', '325/325e', 'R 80 GS', '750Lxi / ALPINA B7', '318iS', 'F 700 GS',
                                           'K 1200 R', 'K75S', '750Lxi', '323iC', 'M850i', '435i', 'G 310 R', 'M3Cic', 'ActiveHybrid 5', '540iAT', 'X2', 'R 18', '335is', 'X5', '330Cic', 'K 1600 GTL', '325i/325is', 'i8', 'M240i', 'K 100 RT', 'R 1150 R', 'C 650 GT', 'L7', '1M', 'M340i', '328Ci', '328iC', '530e', 'M440i', 'K 1100 LT', '328d', '230i', '550i', 'R 100 CS', '325Cic', '318iC', '850i', 'S 1000 R', 'R 1100 RS', '318ti', '735iL', '335', '750i', 'F 650 S', '740Li', 'R 1100 RT', 'R nineT', '330e', '650i / B6', 'G 650', '745i', 'R 1150 RT', '530xi', 'R 1200 R', 'R 1150 GS', '525i', 'K75', 'R 100 GSPD', '745e', 'M3Ci', '535i', '330i', '645Ci', '750xi / ALPINA B7', '325xiT', 'F 850 GS', 'Z3', '645i', 'R 850 R', 'R 1200 RT', 'Active E', 'Alpina', 'K 1200 GT', 'R 1100 GS', 'X6', 'K 1200 S', '635CSi', '525iAT', 'K 1200 LT', 'R 65 LS', 'K 1300 R', 'R 1250 GS', '650xi', 'R 100 RS', '128i', 'ActiveHybrid 3', 'K 100 LT', '650i', 'K 100 RS', '318i', 'K 1300 GT', 'G 650 GS', 'R 1100 R', '840Ci', '840i', 'R 900 RT', 'M8', '325xi', 'X3', '525iT', '530xiT', '323is', '740i', '325Ci', '330Ci', '528e', 'HP4', '540d', 'M235i', 'R 1200 CL', 'M550i', 'Z4', 'R 1200 S', 'R 100 R', '750i / B7', 'X1', '850Ci'}}

        self.sample = get_sample(self.test_makes_models)
        self.max_number_of_randomly_generated_rates_per_car = r.randint(0, 200)

    def test_list_cars(self):
        generate_random_database(self.sample)

        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)

        wanted_response = retrive_wanted_response(self.sample)
        response = json.loads(response.content)

        self.assertEqual(response, wanted_response)

    def test_deleting_car(self):
        car_id = create_car("Volkswagen", "Golf")
        response = self.client.generic('DELETE', '/cars/{}/'.format(car_id))
        self.assertEqual(response.status_code, 200)

    def test_rating_car(self):
        car_id = create_car("Volkswagen", "Golf")
        rate_message = json.dumps({"car_id": 1, "rating": car_id})
        response = self.client.generic('POST', '/rate/', rate_message)
        self.assertEqual(response.status_code, 200)

    def test_rating_cars(self):
        generate_random_database(self.sample)
        wanted_response = retrive_wanted_response(self.sample)

        if not wanted_response: return  #if randomly generated empty database

        rate_trace = rate_random_cars(
            wanted_response,
            self.max_number_of_randomly_generated_rates_per_car, self)

        cars_with_ratings = []
        for car in Car.objects.all():
            cars_with_ratings.append({
                'id': car.id,
                'make': car.make,
                'model': car.model,
                'avg_rating': car.avg_rating
            })

        for elem in rate_trace:
            avg_rating = rate_trace[elem]['sum'] / rate_trace[elem]['count']
            wanted_response[elem - 1]['avg_rating'] = round(avg_rating, 1)

        self.assertEqual(cars_with_ratings, wanted_response)

    def test_popular_cars(self):
        generate_random_database(self.sample)
        wanted_response = retrive_wanted_response(self.sample)

        if not wanted_response: return

        rate_trace = rate_random_cars(
            wanted_response,
            self.max_number_of_randomly_generated_rates_per_car, self)

        top_cars = sorted(rate_trace.items(),
                          key=lambda x: x[1]['count'],
                          reverse=True)[:2]

        wanted_response_popular_cars = []
        for elem in top_cars:
            car = Car.objects.get(id=elem[0])
            wanted_response_popular_cars.append({
                'id':
                car.id,
                'make':
                car.make,
                'model':
                car.model,
                'rates_number':
                car.rates_number
            })

        response = self.client.generic('GET', '/popular/')
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content)

        for i in range(0, len(wanted_response_popular_cars)):
            self.assertEqual(response[i]['rates_number'],
                             wanted_response_popular_cars[i]['rates_number'])

    def test_adding_cars(self):
        existing_car = json.dumps({"make": "Volkswagen", "model": "Golf"})
        not_existing_car = json.dumps({"make": "Volkswagen", "model": "M3"})

        response = self.client.generic('POST', '/cars/', existing_car)
        self.assertEqual(response.status_code, 200)

        response = self.client.generic('POST', '/cars/', not_existing_car)
        self.assertEqual(response.status_code, 400)
