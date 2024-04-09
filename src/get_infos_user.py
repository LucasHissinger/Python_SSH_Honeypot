##
## PERSONAL PROJECT, 2024
## Python_SSH_Honeypot
## File description:
## utils
##


def is_private_ip(ip):
    import re

    regex = r"(^(192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)\d{1,3}\.\d{1,3}$)|(^(10\.|127\.)\d{1,3}\.\d{1,3}\.\d{1,3}$)"
    return bool(re.match(regex, ip))


def get_location_info(ip_address: str):
    import requests

    infos = {
        "status": "",
        "country": "",
        "countryCode": "",
        "region": "",
        "regionName": "",
        "city": "",
        "zip": "",
        "lat": 0,
        "lon": 0,
        "isp": "",
        "query": "",
    }
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    for key in infos.keys():
        if key in data:
            infos[key] = data[key]
    return infos


def lat_lon_to_address(lat, lon):
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{lat}, {lon}")
    address = location.raw["address"]
    city = address.get("city", "")
    state = address.get("state", "")
    country = address.get("country", "")
    addr = (
        address.get("road", "")
        + " "
        + address.get("subrub", "")
        + " "
        + address.get("postcode", "")
    )
    return f"{addr}, {city}, {state}, {country}"


def get_infos_user(ip: str) -> tuple[dict, str] | tuple[None, None]:
    if is_private_ip(ip):
        return None, None
    infos = get_location_info(ip)
    addr = lat_lon_to_address(infos["lat"], infos["lon"])
    return infos, addr
