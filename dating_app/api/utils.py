import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Рассчитывает дистанцию между двумя точками на сфере (земной поверхности)
    с использованием формулы Great Circle Distance.
    Аргументы:
    lat1, lon1: Широта и долгота первой точки в градусах.
    lat2, lon2: Широта и долгота второй точки в градусах.
    Возвращает:
    Дистанцию между двумя точками в километрах.
    """
    # Преобразование градусов в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Радиус Земли в километрах
    earth_radius = 6371.0

    # Разница долготы и широты
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Расчет расстояния по формуле Great Circle Distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(
        lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance
