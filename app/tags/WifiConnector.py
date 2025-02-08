import nfc
import ndef
import os

class WifiConnector:
    def __init__(self):
        self.security_type = os.environ.get("SECURITY_TYPE")
        self.wifi_ssid = os.environ.get("WIFI_SSID")
        self.wifi_password = os.environ.get("WIFI_PASSWORD")


    def setup_wifi(self):
        wifi_data = f"WIFI:T:{self.security_type};S:{self.wifi_ssid};P:{self.wifi_password};;"

        # contactlessfrontend: an object that represents the NFC reader/writer device connected to your computer
        clf = nfc.ContactlessFrontend('usb')

        if clf:
            print("NFC reader connected. Waiting for tag...")

            # callback method
            def on_connect(tag):
                # check that the tag support NDEF format
                if tag.ndef:
                    # creates a new record to store the WiFi credentials
                    record = ndef.TextRecord(wifi_data.encode("utf-8"))
                    # assigns the NDEF message to the NFC tag
                    tag.ndef.message = nfc.ndef.Message(record)

                    print(f"Successfully wrote Wi-Fi credentials for {self.wifi_ssid} to NFC tag!")
                else:
                    print("Tag does not support NDEF.")
                return True # disconnect after writing

            clf.connect(rdwr={'on-connect': on_connect})
            clf.close()

        else:
            print("Failed to connect to NFC reader.")


if __name__ == '__main__':
    WifiConnector().setup_wifi()