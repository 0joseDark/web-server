# pip install flask

from flask import Flask, request, send_from_directory, render_template_string
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <title>File Server</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; }
            .controls { display: grid; grid-template-rows: repeat(3, 60px); grid-template-columns: repeat(3, 60px); gap: 10px; margin-top: 20px; }
            .controls button { width: 100%; height: 100%; font-size: 16px; cursor: pointer; }
            .controls button:active { background-color: yellow; }
            .empty { background-color: transparent; border: none; }
        </style>
    </head>
    <body>
        <h1>Escolha uma pasta ou ficheiro para servir</h1>
        <form method="POST" action="/serve_folder">
            <input type="text" name="folder" placeholder="Pasta">
            <button type="submit">Servir Pasta</button>
        </form>
        <form method="POST" action="/serve_file">
            <input type="text" name="file" placeholder="Ficheiro">
            <button type="submit">Servir Ficheiro</button>
        </form>
        <h1>Controles</h1>
        <div class="controls">
            <button class="empty"></button>
            <button onclick="sendCommand('up')">↑</button>
            <button class="empty"></button>
            <button onclick="sendCommand('left')">←</button>
            <button class="empty"></button>
            <button onclick="sendCommand('right')">→</button>
            <button class="empty"></button>
            <button onclick="sendCommand('down')">↓</button>
            <button class="empty"></button>
        </div>
        <div class="controls">
            <button class="empty"></button>
            <button onclick="sendCommand('jump')">Saltar</button>
            <button class="empty"></button>
            <button onclick="sendCommand('crouch')">Baixar</button>
            <button class="empty"></button>
        </div>

        <script>
            function sendCommand(command) {
                fetch('/command', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({command: command}),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/serve_folder', methods=['POST'])
def serve_folder():
    folder = request.form['folder']
    # Aqui você pode adicionar a lógica para servir a pasta
    return f"Servindo a pasta: {folder}"

@app.route('/serve_file', methods=['POST'])
def serve_file():
    file = request.form['file']
    # Aqui você pode adicionar a lógica para servir o ficheiro
    return f"Servindo o ficheiro: {file}"

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    command = data['command']
    # Substitua "your_program.exe" pelo caminho do seu programa ou script
    if command == 'up':
        subprocess.run(["your_program.exe", "up"])
    elif command == 'down':
        subprocess.run(["your_program.exe", "down"])
    elif command == 'left':
        subprocess.run(["your_program.exe", "left"])
    elif command == 'right':
        subprocess.run(["your_program.exe", "right"])
    elif command == 'jump':
        subprocess.run(["your_program.exe", "jump"])
    elif command == 'crouch':
        subprocess.run(["your_program.exe", "crouch"])
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
