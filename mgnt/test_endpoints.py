import requests

print('Testing Contact creation...')
contact_data = {
    'address': 'Kasangati, Wakiso District, Uganda',
    'phone_number': '+256 771 234 567',
    'email': 'info@hilltopjunior.ug',
    'working_hours': 'Monday - Friday: 7:00 AM - 5:00 PM',
    'additional_notes': 'Office hours: 8:00 AM - 4:00 PM'
}

footer_data = {
    'address': 'Kasangati, Wakiso District, Uganda',
    'phone_number': '+256 771 234 567',
    'email': 'info@hilltopjunior.ug',
    'working_hours': 'Monday - Friday: 7:00 AM - 5:00 PM',
    'additional_notes': 'P.O. Box 12345, Kampala'
}

# Try creating/updating contact
print('\n=== CONTACT INFO ===')
response = requests.get('http://localhost:5010/api/v1/contact_info')
print(f'GET /contact_info: {response.status_code}')
print(f'Response type: {type(response.json())}')
print(f'Response: {response.text[:300]}')

if response.status_code == 200:
    result = response.json()
    # Handle nested response structure
    if isinstance(result, dict) and 'data' in result:
        contacts = result['data'] if isinstance(result['data'], list) else [result['data']]
    elif isinstance(result, list):
        contacts = result
    else:
        contacts = [result] if result else []
    
    print(f'Contacts count: {len(contacts)}')
    
    if contacts and len(contacts) > 0:
        contact_id = contacts[0]['id']
        print(f'Updating contact {contact_id}...')
        response = requests.put(f'http://localhost:5010/api/v1/contact_info/{contact_id}', json=contact_data)
        print(f'PUT /contact_info/{contact_id}: {response.status_code}')
        print(f'Response: {response.text[:200]}')
    else:
        print('Creating new contact...')
        response = requests.post('http://localhost:5010/api/v1/contact_info', json=contact_data)
        print(f'POST /contact_info: {response.status_code}')
        print(f'Response: {response.text[:200]}')
else:
    print('Creating new contact...')
    response = requests.post('http://localhost:5010/api/v1/contact_info', json=contact_data)
    print(f'POST /contact_info: {response.status_code}')
    print(f'Response: {response.text[:200]}')

# Try creating/updating footer
print('\n=== FOOTER INFO ===')
response = requests.get('http://localhost:5010/api/v1/footer')
print(f'GET /footer: {response.status_code}')

if response.status_code == 200:
    result = response.json()
    # Handle nested response structure
    if isinstance(result, dict) and 'data' in result:
        footers = result['data'] if isinstance(result['data'], list) else [result['data']]
    elif isinstance(result, list):
        footers = result
    else:
        footers = [result] if result else []
    
    print(f'Footers count: {len(footers)}')
    
    if footers and len(footers) > 0:
        footer_id = footers[0]['id']
        print(f'Updating footer {footer_id}...')
        response = requests.put(f'http://localhost:5010/api/v1/footer/{footer_id}', json=footer_data)
        print(f'PUT /footer/{footer_id}: {response.status_code}')
        print(f'Response: {response.text[:200]}')
    else:
        print('Creating new footer...')
        response = requests.post('http://localhost:5010/api/v1/footer', json=footer_data)
        print(f'POST /footer: {response.status_code}')
        print(f'Response: {response.text[:200]}')
else:
    print('Creating new footer...')
    response = requests.post('http://localhost:5010/api/v1/footer', json=footer_data)
    print(f'POST /footer: {response.status_code}')
    print(f'Response: {response.text[:200]}')

print('\n✅ Done!')
