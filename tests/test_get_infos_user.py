##
## PERSONAL PROJECT, 2024
## Python_SSH_Honeypot
## File description:
## test_get_infos_user
##

import unittest

import pytest
from src.get_infos_user import get_location_info, is_private_ip, lat_lon_to_address


def test_is_private_ip():
    assert is_private_ip("127.0.0.1")
    assert is_private_ip("10.1.2.3")
    assert is_private_ip("172.17.0.2")
    assert not (is_private_ip("8.8.8.8"))
    assert not (is_private_ip("31.34.65.12"))


def test_get_location_info_OK():
    ip = "24.48.0.1"
    expected_infos_result = {
        "status": "success",
        "country": "Canada",
        "countryCode": "CA",
        "region": "QC",
        "regionName": "Quebec",
        "city": "Montreal",
        "zip": "H1K",
        "lat": 45.6085,
        "lon": -73.5493,
        "isp": "Le Groupe Videotron Ltee",
        "query": "24.48.0.1",
    }
    infos = get_location_info(ip)
    assert infos == expected_infos_result


@pytest.mark.parametrize(
    "ip, expected",
    [
        (
            "127.0.0.1",
            {
                "status": "fail",
                "country": "",
                "countryCode": "",
                "region": "",
                "regionName": "",
                "city": "",
                "zip": "",
                "lat": 0,
                "lon": 0,
                "isp": "",
                "query": "127.0.0.1",
            },
        ),
        (
            "fake_ip",
            {
                "status": "fail",
                "country": "",
                "countryCode": "",
                "region": "",
                "regionName": "",
                "city": "",
                "zip": "",
                "lat": 0,
                "lon": 0,
                "isp": "",
                "query": "fake_ip",
            },
        ),
    ],
)
def test_get_location_info_KO(ip, expected):
    infos = get_location_info(ip)
    assert infos == expected


def lat_lon_to_address_OK():
    lat = 45.6085
    lon = -73.5493
    expected = "Rue de la Roche, Villeray, H2R Montreal, Canada"
    addr = lat_lon_to_address(lat, lon)
    assert addr == expected


@pytest.mark.parametrize("lat, lon, expected", [(0, 0, "")])
def lat_lon_to_address_KO(lat, lon, expected):
    expected = ""
    addr = lat_lon_to_address(lat, lon)
    assert addr == expected
