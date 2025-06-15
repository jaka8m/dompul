from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Mengambil PORT dari variabel lingkungan, default ke 3000 jika tidak ada
# Vercel akan menyediakan PORT-nya sendiri, jadi ini lebih untuk pengembangan lokal
PORT = int(os.environ.get('PORT', 3000))

@app.route('/cek_kuota', methods=['GET'])
def cek_kuota():
    """
    Endpoint untuk memeriksa kuota menggunakan MSISDN yang disediakan.
    """
    msisdn = request.args.get('msisdn')

    if not msisdn:
        return jsonify({
            'status': 'error',
            'message': 'Parameter "msisdn" diperlukan dalam query URL.'
        }), 400

    api_url = f"https://apigw.kmsp-store.com/sidompul/v4/cek_kuota?msisdn={msisdn}&isJSON=true"

    headers = {
        'Authorization': 'Basic c2lkb21wdWxhcGl:YXBpZ3drbXNw',
        'X-API-Key': '60ef29aa-a648-4668-90ae-20951ef90c55',
        'X-App-Version': '4.0.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        # Melakukan permintaan GET ke API eksternal
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Memunculkan HTTPError untuk status kode 4xx/5xx

        # Menguraikan respons JSON
        data = response.json()
        return jsonify({
            'status': 'sukses',
            'msisdn': msisdn,
            'data': data
        }), 200

    except requests.exceptions.HTTPError as err:
        # Menangani kesalahan HTTP (misalnya, 404 Not Found, 500 Internal Server Error dari API eksternal)
        print(f"Kesalahan dari API eksternal: {err.response.status_code} - {err.response.text}")
        return jsonify({
            'status': 'error',
            'message': f"Gagal mengambil data dari XL API. Status: {err.response.status_code}",
            'details': err.response.text
        }), err.response.status_code
    except requests.exceptions.ConnectionError as err:
        # Menangani masalah koneksi jaringan
        print(f"Kesalahan koneksi saat memeriksa paket XL: {err}")
        return jsonify({
            'status': 'error',
            'message': 'Kesalahan jaringan saat terhubung ke XL API.',
            'details': str(err)
        }), 500
    except requests.exceptions.Timeout as err:
        # Menangani batas waktu (timeout) koneksi
        print(f"Kesalahan batas waktu saat memeriksa paket XL: {err}")
        return jsonify({
            'status': 'error',
            'message': 'Batas waktu habis saat terhubung ke XL API.',
            'details': str(err)
        }), 504 # Gateway Timeout
    except requests.exceptions.RequestException as err:
        # Menangani kesalahan lain yang mungkin terjadi dengan pustaka requests
        print(f"Kesalahan saat memeriksa paket XL: {err}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan tak terduga saat memeriksa paket XL.',
            'details': str(err)
        }), 500
    except ValueError as err:
        # Menangani jika respons JSON tidak valid atau gagal diuraikan
        print(f"Kesalahan decoding JSON: {err}")
        return jsonify({
            'status': 'error',
            'message': 'Gagal mendekode respons JSON dari XL API.',
            'details': str(err)
        }), 500

# Hanya jalankan server Flask saat skrip dieksekusi secara langsung (untuk pengembangan lokal)
# Vercel akan menggunakan WSGI server sendiri, jadi blok ini tidak akan dieksekusi di Vercel
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
    # Contoh penggunaan untuk pengujian lokal:
    # print(f"Server berjalan di port {PORT}")
    # print(f"Contoh penggunaan: http://localhost:{PORT}/cek_kuota?msisdn=087765101308")
