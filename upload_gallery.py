import requests
import os

images = [
    r'd:\Screenshots\Screenshot 2026-06-14 205356.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205413.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205435.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205454.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205517.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205539.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205559.png',
    r'd:\Screenshots\Screenshot 2026-06-14 205617.png'
]

files_to_upload = []
for image_path in images:
    if os.path.exists(image_path):
        files_to_upload.append(('images', open(image_path, 'rb')))
        print(f'Added: {os.path.basename(image_path)}')
    else:
        print(f'Not found: {image_path}')

if files_to_upload:
    try:
        print(f'\nUploading {len(files_to_upload)} images...')
        response = requests.post(
            'http://localhost:5010/api/v1/gallery',
            files=files_to_upload
        )
        print(f'Upload response: {response.status_code}')
        print(f'Response: {response.text}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        for _, file in files_to_upload:
            file.close()
else:
    print('No images found to upload')
