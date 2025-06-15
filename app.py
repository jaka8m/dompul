# Lokasi: my-kuota-api/app.py

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/cek_kuota', methods=['GET'])
def cek_kuota():
    msisdn = request.args.get('msisdn')

    if not msisdn:
        return jsonify({
            'status': 'error',
            'message': 'Parameter "msisdn" is required in the URL query.'
        }), 400

    api_url = f'https://apigw.kmsp-store.com/sidompul/v4/cek_kuota?msisdn={msisdn}&isJSON=true'

    headers = {
        'Authorization': 'Basic c2lkb21wdWxhcGl6YXBpZ3drbXNw',
        'X-API-Key': '60ef29aa-a648-4668-90ae-20951ef90c55',
        'X-App-Version': '4.0.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Ini akan memunculkan HTTPError untuk status kode 4xx/5xx

        data = response.json()
        return jsonify({
            'status': 'success',
            'msisdn': msisdn,
            'data': data
        }), 200

    except requests.exceptions.HTTPError as e:
        print(f"Error from external API: {e.response.status_code} - {e.response.text}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch data from XL API. Status: {e.response.status_code}',
            'details': e.response.text
        }), e.response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error checking XL package: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error while checking XL package.',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(port=PORT)
