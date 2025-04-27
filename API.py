import requests
from geopy.distance import geodesic
API_KEY = "d053f8e4-fb49-498a-8dbe-0ba34403c7c4"
BASE_URL = "https://geocode-maps.yandex.ru/1.x/"
STATIC_MAPS_URL = "https://static-maps.yandex.ru/1.x/"


def geocode(address):
    params = {
        "apikey": API_KEY,
        "format": "json",
        "geocode": address
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def get_coordinates(city):
    data = geocode(city)
    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    longitude, latitude = pos.split()
    return float(latitude), float(longitude)


def get_point_coordinates(address):
    data = geocode(address)
    try:
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return pos.replace(' ', ',')
    except IndexError:
        return None


def get_federal_district(city):
    data = geocode(city)
    try:
        district = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        return district
    except IndexError:
        return "Не удалось определить"


def get_postal_code(address):
    data = geocode(address)
    try:
        postal_code = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['Address']['postal_code']
        return postal_code
    except IndexError:
        return "Не удалось определить"


def get_full_address(address):
    data = geocode(address)
    try:
        full_address = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['Address']['formatted']
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return full_address, pos
    except IndexError:
        return None, None


def get_region(city):
    data = geocode(city)
    try:
        region = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        return region
    except IndexError:
        return "Не удалось определить"


def save_map_image(filename, params):
    response = requests.get(STATIC_MAPS_URL, params=params)
    with open(filename, 'wb') as f:
        f.write(response.content)


def get_southernmost_city(cities):
    min_lat = 90
    southern_city = None
    for city in cities:
        data = geocode(city)
        try:
            pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            lat = float(pos.split()[1])
            if lat < min_lat:
                min_lat = lat
                southern_city = city
        except IndexError:
            continue
    return southern_city


# 3
print("\nИсторический музей Москвы:")
address, coords = get_full_address("Красная площадь, 1, Москва")
print(f"Адрес: {address}")
print(f"Координаты: {coords}")

# 4
print("\nОбласти городов:")
cities = ["Барнаул", "Мелеуз", "Йошкар-Ола"]
for city in cities:
    region = get_region(city)
    print(f"{city}: {region}")

# 5
print("\nПочтовый индекс МУРа:")
postal_code = get_postal_code("Петровка, 38, Москва")
print(f"Почтовый индекс: {postal_code}")

# 6
print("\nСохранение снимка Австралии:")
params = {
    "ll": "133.7751,-25.2744",
    "spn": "40,40",
    "l": "sat",
    "size": "650,450"
}
save_map_image("australia.jpg", params)
print("Снимок сохранен в australia.jpg")

# 7
print("\nКарта Кемерово с отметками")
points = {
    ("ЖД Вокзал", "Кемерово, Кемерово-Пасс."),
    ("Кардиодиспансер", "Кемерово, Кардиоцентр"),
    ("Красная Горка") 
}
# 8
print("\nКарта области с маршрутом")
route_coords = []
for city in ["Кемерово", "Ленинск-Кузнецкий", "Новокузнецк", "Шерегеш"]:
    coords = get_point_coordinates(city)
    print(coords)
    if coords:
        route_coords.append(coords)

params = {
    # "ll": "86.569349,54.136101",
    # "z": "7",
    "l": "map",
    "pl": ",".join(route_coords),
    "size": "650,450"
}
save_map_image("kemerovo_region.jpg", params)
print("Карта сохранена в kemerovo_region.jpg")

# 9
input_cities = input("Введите города через запятую: ").split(',')
cities = [city.strip() for city in input_cities if city.strip()]
southern_city = get_southernmost_city(cities)
print(f"Самый южный город: {southern_city}")

#10
print("\nДлина пути:")
points = [
    "86.102792,55.358422",  # Кемерово
    "86.379429,54.947760",  # Панфилово
    "86.161708,54.663875",  # Ленинск-Кузнецкий
    "86.749251,53.885196"  # Прокопьевск
]

distance = 0.0
for i in range(len(points) - 1):
    point1 = points[i]
    point2 = points[i + 1]
    distance += geodesic(point1, point2).kilometers

print(f"Общая длина маршрута: {distance:.2f} км")

midpoint_index = len(points) // 2
pt_params = []
pt_params.append(f"{points[midpoint_index]},pm2rdm")

params = {
    "l": "map",
    "pl": ",".join(points),
    "pt": "~".join(pt_params),
    "size": "650,450"
}
print(params.get("pt"))
save_map_image("route.jpg", params)