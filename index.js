const express = require('express');
const fetch = require('node-fetch'); // Pastikan ini adalah node-fetch v2.x jika menggunakan CommonJS tanpa 'type: module'

const app = express();
// Vercel akan otomatis mengatur PORT-nya, jadi tidak perlu mendefefinisikan secara eksplisit
// const PORT = process.env.PORT || 3000; 

app.use(express.json());

app.get('/cek_kuota', async (req, res) => {
    const msisdn = req.query.msisdn;

    if (!msisdn) {
        return res.status(400).json({
            status: 'error',
            message: 'Parameter "msisdn" is required in the URL query.'
        });
    }

    const apiUrl = `https://apigw.kmsp-store.com/sidompul/v4/cek_kuota?msisdn=${msisdn}&isJSON=true`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': 'Basic c2lkb21wdWxhcGk6YXBpZ3drbXNw',
                'X-API-Key': '60ef29aa-a648-4668-90ae-20951ef90c55',
                'X-App-Version': '4.0.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Error from external API: ${response.status} - ${errorText}`);
            return res.status(response.status).json({
                status: 'error',
                message: `Failed to fetch data from XL API. Status: ${response.status}`,
                details: errorText
            });
        }

        const data = await response.json();
        res.status(200).json({
            status: 'success',
            msisdn: msisdn,
            data: data
        });

    } catch (error) {
        console.error('Error checking XL package:', error);
        res.status(500).json({
            status: 'error',
            message: 'Internal server error while checking XL package.',
            details: error.message
        });
    }
});

// Untuk Vercel, Anda tidak perlu secara eksplisit memanggil app.listen()
// Vercel menangani server booting di lingkungannya sendiri untuk serverless functions.
// Jika Anda ingin menguji secara lokal, Anda bisa mengaktifkan kembali bagian ini:
/*
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Contoh penggunaan: http://localhost:${PORT}/cek_kuota?msisdn=087765101308`);
});
*/

// Penting: Ekspor aplikasi Express untuk Vercel sebagai Serverless Function
module.exports = app;
