import requests

API_KEY = "d053f8e4-fb49-498a-8dbe-0ba34403c7c4"
BASE_URL = "https://geocode-maps.yandex.ru/1.x/"

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

def get_federal_district(city):
    data = geocode(city)
    try:
        district = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        return district
    except:
        return "Не удалось определить"

def get_postal_code(address):
    data = geocode(address)
    try:
        postal_code = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        print(postal_code)
        return postal_code
    except:
        return "Не удалось определить"

yakutsk_lat, yakutsk_lon = get_coordinates("Якутск")
magadan_lat, magadan_lon = get_coordinates("Магадан")

print("\na) Координаты:")
print(f"Якутск: {yakutsk_lat}° с.ш., {yakutsk_lon}° в.д.")
print(f"Магадан: {magadan_lat}° с.ш., {magadan_lon}° в.д.")

if yakutsk_lat and magadan_lat:
    if yakutsk_lat > magadan_lat:
        print("Якутск находится севернее Магадана")
    else:
        print("Магадан находится севернее Якутска")

native_city = "Кемерово"
native_lat, native_lon = get_coordinates(native_city)
toronto_lat, toronto_lon = get_coordinates("Торонто, Канада")

print("\nb) Координаты:")
print(f"{native_city}: {native_lat}° с.ш., {native_lon}° в.д.")
print(f"Торонто: {toronto_lat}° с.ш., {toronto_lon}° з.д.")

if native_lat and toronto_lat:
    if native_lat < toronto_lat:
        print(f"{native_city} находится южнее Торонто")
    else:
        print("Торонто находится южнее")

cities = ["Хабаровск", "Уфа", "Нижний Новгород", "Калининград", native_city]
print("\nc) Федеральные округа:")
for city in cities:
    district = get_federal_district(city)
    print(f"{city}: {district}")

kemgu_postal = get_postal_code("КемГУ, Кемерово")
print("\nd) Почтовый индекс КемГУ:", kemgu_postal)