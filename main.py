from PyQt5.QtCore import *
import json


def config_to_url(config_path: str = 'client.conf') -> str:
    with open('client.conf', 'r') as file:
        data = file.read().strip()
    encoded_data = qCompress(QByteArray(data.encode()))
    encoded_data = encoded_data.toBase64(QByteArray.Base64Option.Base64UrlEncoding | QByteArray.Base64Option.OmitTrailingEquals)
    return 'vpn://' + str(encoded_data, 'utf-8')

#print(config_to_url())

def config_from_json():
    # Загрузка данных из JSON
    with open('data.json', 'r') as file:
        json_data = json.load(file)
    str_data = f"""
    [Interface]
    Address = {json_data['addresses'][0]}
    DNS = {', '.join(json_data['dns'])}
    PrivateKey = {json_data['client_private_key']}
    Jc = {json_data['jc']}
    Jmin = {json_data['jmin']}
    Jmax = {json_data['jmax']}
    S1 = {json_data['s1']}
    S2 = {json_data['s2']}
    H1 = {json_data['h1']}
    H2 = {json_data['h2']}
    H3 = {json_data['h3']}
    H4 = {json_data['h4']}

    [Peer]
    PublicKey = {json_data['server_public_key']}
    PresharedKey = {json_data['preshared_key']}
    AllowedIPs = {', '.join(json_data['allowed_ips'])}
    Endpoint = {json_data['endpoint']}
    PersistentKeepalive = {json_data['set_keep_alive']}
    """
    encoded_data = qCompress(QByteArray(str_data.encode()))
    encoded_data = encoded_data.toBase64(
        QByteArray.Base64Option.Base64UrlEncoding | QByteArray.Base64Option.OmitTrailingEquals)
    return 'vpn://' + str(encoded_data, 'utf-8')

print(config_from_json())
