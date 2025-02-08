import pytest

from app.tags.WifiConnector import WifiConnector

###################################################################
# test values
###################################################################
SECURITY_TYPE = "WPA"
WIFI_SSID = "changeme"
WIFI_PASSWORD = "strongpassword"

###################################################################
# pytest fixtures
###################################################################
@pytest.fixture
def wifi_connector(monkeypatch):
    monkeypatch.setenv("SECURITY_TYPE", SECURITY_TYPE)
    monkeypatch.setenv("WIFI_SSID", WIFI_SSID)
    monkeypatch.setenv("WIFI_PASSWORD", WIFI_PASSWORD)

    return WifiConnector()

###################################################################
# unit tests
###################################################################
def test_exists(wifi_connector):
    assert wifi_connector is not None

def test_environment_variables(wifi_connector):
    # test that the environment variables are being correctly read
    assert wifi_connector.security_type == SECURITY_TYPE
    assert wifi_connector.wifi_ssid == WIFI_SSID
    assert wifi_connector.wifi_password == WIFI_PASSWORD

def test_wifi_data_format(wifi_connector):
    # test that the Wi-Fi credentials are formatted correctly
    expected_wifi_data = f"WIFI:T:{SECURITY_TYPE};S:{WIFI_SSID};P:{WIFI_PASSWORD};;"
    wifi_data = f"WIFI:T:{wifi_connector.security_type};S:{wifi_connector.wifi_ssid};P:{wifi_connector.wifi_password};;"
    assert wifi_data == expected_wifi_data




