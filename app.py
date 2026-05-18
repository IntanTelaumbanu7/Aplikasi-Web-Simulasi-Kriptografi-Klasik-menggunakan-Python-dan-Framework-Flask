from flask import Flask, render_template, request, session, redirect, url_for
import secrets
import os
from crypto import process_caesar, process_vigenere, process_affine, process_hill, process_playfair

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def add_to_history(algo, mode, input_text, key_display, result):
    if 'history' not in session:
        session['history'] = []
    
    # Keep last 20 items
    history = session['history']
    history.insert(0, {
        "algo": algo,
        "mode": mode.capitalize(),
        "input": input_text,
        "key": key_display,
        "result": result
    })
    session['history'] = history[:20]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html', history=session.get('history', []))

@app.route('/clear_history')
def clear_history():
    session.pop('history', None)
    return redirect(url_for('history'))

@app.route('/caesar', methods=['GET', 'POST'])
def caesar():
    if request.method == 'POST':
        text = request.form.get('text', '')
        mode = request.form.get('mode', 'encrypt')
        try:
            key = int(request.form.get('key', 0))
            if key < 1 or key > 25:
                raise ValueError("Key must be between 1 and 25")
            
            res = process_caesar(text, key, mode)
            if res['result'] != "Error":
                add_to_history('Caesar', mode, text, str(key), res['result'])
            
            return render_template('cipher.html', title='Caesar Cipher', algo='caesar', result=res, text=text, key=key, mode=mode)
        except ValueError as e:
            error = {"result": "Error", "steps": [f"<span class='text-red-500'>Error: {str(e)}</span>"]}
            return render_template('cipher.html', title='Caesar Cipher', algo='caesar', result=error, text=text, key=request.form.get('key'), mode=mode)
            
    return render_template('cipher.html', title='Caesar Cipher', algo='caesar')

@app.route('/vigenere', methods=['GET', 'POST'])
def vigenere():
    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        mode = request.form.get('mode', 'encrypt')
        
        res = process_vigenere(text, key, mode)
        if res['result'] != "Error":
            add_to_history('Vigenère', mode, text, key, res['result'])
            
        return render_template('cipher.html', title='Vigenère Cipher', algo='vigenere', result=res, text=text, key=key, mode=mode)
            
    return render_template('cipher.html', title='Vigenère Cipher', algo='vigenere')

@app.route('/affine', methods=['GET', 'POST'])
def affine():
    if request.method == 'POST':
        text = request.form.get('text', '')
        mode = request.form.get('mode', 'encrypt')
        try:
            a = int(request.form.get('key_a', 1))
            b = int(request.form.get('key_b', 0))
            
            res = process_affine(text, a, b, mode)
            if res['result'] != "Error":
                add_to_history('Affine', mode, text, f"a={a}, b={b}", res['result'])
                
            return render_template('cipher.html', title='Affine Cipher', algo='affine', result=res, text=text, key_a=a, key_b=b, mode=mode)
        except ValueError as e:
            error = {"result": "Error", "steps": [f"<span class='text-red-500'>Error: Invalid input for a or b.</span>"]}
            return render_template('cipher.html', title='Affine Cipher', algo='affine', result=error, text=text, key_a=request.form.get('key_a'), key_b=request.form.get('key_b'), mode=mode)
            
    return render_template('cipher.html', title='Affine Cipher', algo='affine')

@app.route('/hill', methods=['GET', 'POST'])
def hill():
    if request.method == 'POST':
        text = request.form.get('text', '')
        mode = request.form.get('mode', 'encrypt')
        size = int(request.form.get('matrix_size', 2))
        
        matrix = []
        try:
            for i in range(size):
                row = []
                for j in range(size):
                    val = int(request.form.get(f'm_{i}_{j}', 0))
                    row.append(val)
                matrix.append(row)
                
            res = process_hill(text, matrix, mode)
            if res['result'] != "Error":
                add_to_history('Hill', mode, text, f"{size}x{size} Matrix", res['result'])
                
            return render_template('cipher.html', title='Hill Cipher', algo='hill', result=res, text=text, matrix_size=size, matrix=matrix, mode=mode)
        except Exception as e:
            error = {"result": "Error", "steps": [f"<span class='text-red-500'>Error: Invalid matrix input.</span>"]}
            return render_template('cipher.html', title='Hill Cipher', algo='hill', result=error, text=text, matrix_size=size, mode=mode)
            
    return render_template('cipher.html', title='Hill Cipher', algo='hill')

@app.route('/playfair', methods=['GET', 'POST'])
def playfair():
    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        mode = request.form.get('mode', 'encrypt')
        
        res = process_playfair(text, key, mode)
        if res['result'] != "Error":
            add_to_history('Playfair', mode, text, key, res['result'])
            
        return render_template('cipher.html', title='Playfair Cipher', algo='playfair', result=res, text=text, key=key, mode=mode)
            
    return render_template('cipher.html', title='Playfair Cipher', algo='playfair')

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cryptosim-secret-key")
