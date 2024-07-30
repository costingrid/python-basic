import concurrent.futures
import os

import requests

API_KEY = "bolQumtweWITyIz1kJgaUda3MjVcLPWqPW6zfkBm"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    metadata = []
    response = requests.get(f"{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}")
    if response.status_code == 200:
        metadata = response.json()
    return metadata


def download_image(data):
    image_url = data['url']
    image_name = image_url.split('/')[-1]
    response = requests.get(image_url)
    if response.status_code == 200 and image_name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
        with open(f"{OUTPUT_IMAGES}/{image_name}", 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {image_name}")


def download_apod_images(metadata: list):
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    workers = 8 if len(metadata) > 8 else len(metadata)
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(download_image, data)
            for data in metadata
        ]


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)

    # response = requests.get(f"{APOD_ENDPOINT}?api_key={API_KEY}&date=2024-07-26")
    # print(response)


if __name__ == '__main__':
    main()
