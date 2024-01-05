import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных:
    функция возвращает словарь с информацией о городе, времени, текущей температуре и т.д.
    В качестве параметров передаются широта и долгота искомого места.
    """
    token = 'e52ab137-6069-462b-9862-5aa61de5d28a'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = {
        'city': data['geo_object']['locality']['name'],  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'temp': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': data['fact']['pressure_mm'],  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
    }
    return f'Данные из API "Яндекс-Погоды": {result}'

# Реализация функции получения информации о погоде с использованием WeatherAPI
def api_weather(lat, lon):
    token = 'e99605d1304a499195a233849231612'
    lang = 'ru'
    url = f"http://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}&lang={lang}"
    response = requests.get(url)
    data = response.json()

    result = {
        'city': data['location']['name'],
        'time': data['current']['last_updated'],
        'temp': data['current']['temp_c'],
        'feels_lide_temp': data['current']['feelslike_c'],
        'pressure': round(data['current']['pressure_mb'] * 0.75, 1),
        'humidity': data['current']['humidity'],
        'wind_speed': round(data['current']['wind_kph'] / 3.6, 1),
        'wind_gust': round(data['current']['gust_kph'] / 3.6, 1),
        'wind_dir': DIRECTION_TRANSFORM.get(data['current']['wind_dir'].lower())
    }
    return f'Данные из WeatherAPI: {result}'

if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
    print(api_weather(59.93, 30.31))