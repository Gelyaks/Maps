import requests


def geocode(address):
    toponym_to_find = address
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        'kind': 'district',
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    return toponym


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_lattitude), float(toponym_longitude)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    # Собираем координаты в параметр ll (строка)
    ll = ",".join([toponym_longitude, toponym_lattitude])
    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]
    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    # Собираем размеры в параметр span
    span = f"{dx},{dy}"
    # Воpвращаем координаты ll и размеры объекта span
    return ll, span