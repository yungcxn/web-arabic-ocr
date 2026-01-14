
from flask import Flask, request, jsonify, render_template_string
import requests
import base64

app = Flask(__name__)

#API_KEY = ""
HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arabic OCR</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        #pasteArea {
            border: 3px dashed #ccc;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            border-radius: 8px;
            background: #fafafa;
            cursor: pointer;
        }
        #pasteArea:hover {
            border-color: #4CAF50;
            background: #f0f8f0;
        }
        #preview {
            max-width: 100%;
            margin: 20px 0;
            display: none;
            border-radius: 4px;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 4px;
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.8;
            direction: rtl;
            text-align: right;
            display: none;
        }
        .loading {
            text-align: center;
            color: #666;
            display: none;
        }
        .error {
            color: #d32f2f;
            padding: 10px;
            background: #ffebee;
            border-radius: 4px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Arabic OCR - التعرف على النص العربي</h1>
        <div id="pasteArea">
            <p>انقر هنا والصق الصورة (Ctrl+V)</p>
            <p>Click here and paste image (Ctrl+V)</p>
        </div>
        <img id="preview" alt="Preview">
        <div class="loading">جاري معالجة الصورة... Processing image...</div>
        <div class="error" id="error"></div>
        <div id="result"></div>
    </div>

    <script>
        const pasteArea = document.getElementById('pasteArea');
        const preview = document.getElementById('preview');
        const result = document.getElementById('result');
        const loading = document.querySelector('.loading');
        const error = document.getElementById('error');

        pasteArea.addEventListener('click', () => {
            pasteArea.focus();
        });

        document.addEventListener('paste', async (e) => {
            e.preventDefault();

            const items = e.clipboardData.items;
            for (let item of items) {
                if (item.type.indexOf('image') !== -1) {
                    const blob = item.getAsFile();
                    const reader = new FileReader();

                    reader.onload = async (event) => {
                        const base64Image = event.target.result;

                        preview.src = base64Image;
                        preview.style.display = 'block';
                        result.style.display = 'none';
                        error.style.display = 'none';
                        loading.style.display = 'block';

                        try {
                            const response = await fetch('/ocr', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ image: base64Image })
                            });

                            const data = await response.json();
                            loading.style.display = 'none';

                            if (data.success) {
                                result.textContent = data.text;
                                result.style.display = 'block';
                            } else {
                                error.textContent = 'Error: ' + data.error;
                                error.style.display = 'block';
                            }
                        } catch (err) {
                            loading.style.display = 'none';
                            error.textContent = 'Error: ' + err.message;
                            error.style.display = 'block';
                        }
                    };

                    reader.readAsDataURL(blob);
                    break;
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        data = request.json
        base64_image = data['image']

        payload = {
            'base64Image': base64_image,
            'OCREngine': 3,
            'isOverlayRequired': False
        }

        headers = {
            'apikey': API_KEY
        }

        response = requests.post(
            'https://api.ocr.space/parse/image',
            data=payload,
            headers=headers
        )

        result = response.json()

        if result.get('IsErroredOnProcessing'):
            return jsonify({
                'success': False,
                'error': result.get('ErrorMessage', 'Unknown error')
            })

        parsed_text = result['ParsedResults'][0]['ParsedText']

        return jsonify({
            'success': True,
            'text': parsed_text
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("\n=== Arabic OCR Web App ===")
    print("IMPORTANT: Replace 'helloworld' with your API key!")
    print("Get your free API key at: https://ocr.space/ocrapi")
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
