import json
import base64
import zlib

# AMNEZIA-AWG converter to conf file
example_data = "vpn://AAAG_3jalVXLcqJAFN3n"

def decode_and_uncompress(data):
    # Удаляем первые 6 символов
    data = data[6:]
    
    # Дополняем строку до корректной длины для base64
    if len(data) % 4 == 3:
        data += '='
    elif len(data) % 4 == 2:
        data += '=='
    
    # Заменяем символы для корректной обработки base64
    data = data.replace('-', '+').replace('_', '/')
    
    # Декодируем данные из base64
    decoded_data = base64.b64decode(data)
    
    # Пропускаем первые 4 байта
    decoded_data = decoded_data[4:]
    
    # Распаковываем данные
    uncompressed_data = zlib.decompress(decoded_data)
    
    # Преобразуем распакованные байты в строку UTF-8
    uncompressed_str = uncompressed_data.decode('utf-8')
    
    # Преобразуем строку в JSON-объект
    return json.loads(uncompressed_str)

def compress_and_encode(data):
    # Преобразуем данные в JSON-строку
    json_str = json.dumps(data)

    # Преобразуем JSON-строку в байты с использованием кодировки UTF-8
    utf8_bytes = json_str.encode('utf-8')

    # Сжимаем данные с помощью zlib
    compressed_data = zlib.compress(utf8_bytes)

    # Добавляем 4 байта в начало сжатых данных (это может быть любые 4 байта, которые вы используете в вашем коде)
    compressed_data_with_padding = b'\x00\x00\x00\x00' + compressed_data

    # Кодируем данные в формате base64
    base64_encoded_data = base64.b64encode(compressed_data_with_padding)

    # Преобразуем данные в строку и возвращаем
    return "vpn://" + base64_encoded_data.decode('utf-8')

result = decode_and_uncompress(example_data)

print(result)  # Выведет результат без 'b'


# Извлекаем и парсим last_config
last_config_str = result['containers'][0]['awg']['last_config']
last_config = json.loads(last_config_str)

# Формируем и выводим конфигурационный файл wg0.conf
wg0_conf = f"""
[Interface]
Address = {last_config['client_ip']}/32
DNS = {result['dns1']}, {result['dns2']}
PrivateKey = {last_config['client_priv_key']}
Jc = {last_config['Jc']}
Jmin = {last_config['Jmin']}
Jmax = {last_config['Jmax']}
S1 = {last_config['S1']}
S2 = {last_config['S2']}
H1 = {last_config['H1']}
H2 = {last_config['H2']}
H3 = {last_config['H3']}
H4 = {last_config['H4']}

[Peer]
PublicKey = {last_config['server_pub_key']}
PresharedKey = {last_config['psk_key']}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {result['hostName']}:{last_config['port']}
PersistentKeepalive = 25
""".strip()

print(wg0_conf)

