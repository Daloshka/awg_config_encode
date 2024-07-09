from PyQt5.QtCore import *


def config_to_url(config_path: str = 'client.conf') -> str:
    with open('client.conf', 'r') as file:
        data = file.read().strip()
    encoded_data = qCompress(QByteArray(data.encode()))
    encoded_data = encoded_data.toBase64(QByteArray.Base64Option.Base64UrlEncoding | QByteArray.Base64Option.OmitTrailingEquals)
    return 'vpn://' + str(encoded_data, 'utf-8')

print(config_to_url())
