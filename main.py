import io
import requests
from PIL import Image


# Путь к папке на Яндекс Диске
FOLDER_PATH = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg.'


# Получаем содержимое
url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={FOLDER_PATH}'
response = requests.get(url)
response.raise_for_status()

files = response.json()['_embedded']['items']
# Перебираем вложенные папки в цикле
for item in files:
    # Список изображений для записи в .tiff файл
    images = []
    path_pack = item["path"]
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={FOLDER_PATH}&path={path_pack}'
    response = requests.get(url)
    
    files_pack = response.json()['_embedded']['items']
    # Фильтруем только изображения
    image_files = [item['name'] for item in files_pack if item['type'] == 'file' and item['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Перебираем вложенные изображения в цикле
    for image_file in image_files:
        image_url = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={FOLDER_PATH}&path={path_pack}/{image_file}'
        response = requests.get(image_url)
        response.raise_for_status()

        # Скачиваем содердимое
        download_link = response.json()['href'] # Достаем ссылку
        download_response = requests.get(download_link)
        download_response.raise_for_status()

        # Открываем изображение из полученных данных
        image_data = io.BytesIO(download_response.content)
        image = Image.open(image_data)
        
        images.append(image)
        print(f'Загружено изображение: {item["name"]}/{image_file}')
    output_tiff = f'Result_{item["name"]}.tiff' 
    images[0].save(output_tiff, save_all=True, append_images=images[1:], format='TIFF')
