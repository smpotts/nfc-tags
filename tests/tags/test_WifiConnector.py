import pytest
from unittest.mock import patch, MagicMock

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

@patch("nfc.ContactlessFrontend", return_value=None)
def test_nfc_reader_not_connected(clf, wifi_connector, capsys):
    wifi_connector.setup_wifi()

    # captures the printed output
    captured = capsys.readouterr() 

    assert "Failed to connect to NFC reader." in captured.out

@patch("nfc.ContactlessFrontend")
def test_tag_no_ndef(clf, wifi_connector, capsys):
    mock_reader = MagicMock()
    clf.return_value = mock_reader  # mock NFC reader instance

    mock_tag = MagicMock()
    mock_tag.ndef = False  # simulates a tag that does not support NDEF

    def simulate_connect(rdwr):
        rdwr["on-connect"](mock_tag)  # simulate detecting the tag

    # this sets the side effect of the connect method on the mock_reader object. 
    # The side effect tells the mock to call the simulate_connect function when mock_reader.connect() is called, 
    # which will simulate the detection of the NFC tag and trigger the on-connect callback
    mock_reader.connect.side_effect = simulate_connect

    wifi_connector.setup_wifi()

    # capture the printed output
    captured = capsys.readouterr()

    assert "Tag does not support NDEF." in captured.out

@patch("nfc.ContactlessFrontend")
def test_nfc_tag_written_successfully(clf, wifi_connector, capsys):
    # create a mock NFC reader instance
    mock_reader = MagicMock()
    clf.return_value = mock_reader  # mock NFC reader instance

    # create a mock tag
    mock_tag = MagicMock()
    mock_tag.ndef = True  # simulates a tag that does support NDEF

    # Define the expected Wi-Fi credentials that will be written to the tag
    wifi_data = f"WIFI:T:WPA;S:changeme;P:strongpassword;;"

    # simulate the connection of the tag
    def simulate_connect(rdwr):
        rdwr["on-connect"](mock_tag)  # simulate NFC reader detecting the mock tag

    mock_reader.connect.side_effect = simulate_connect  # make connect() call the simulate_connect function

    # run the setup_wifi() method to trigger writing to the tag
    wifi_connector.setup_wifi()

    # capture the printed output
    captured = capsys.readouterr()
    print(captured)
    # assert the success message is printed
    assert "Successfully wrote Wi-Fi credentials for changeme to NFC tag!" in captured.out
    
    # verify that the NFC tag's NDEF message was set with the Wi-Fi data
    assert mock_tag.ndef.message == wifi_data



