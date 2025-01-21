from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    diffs = ""
    if request.method == "POST":
        # Upload de arquivos
        uploaded_files = request.files.getlist("files")
        arquivos = []
        
        for file in uploaded_files:
            if file:
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                arquivos.append(filepath)
        
        if len(arquivos) < 2:
            message = "Envie pelo menos dois arquivos para comparar."
        else:
            diffs = comparar_arquivos(arquivos)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comparador de Arquivos XML</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(120deg, #5cb85c, #0275d8);
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            h1 {
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            form {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                display: inline-block;
                max-width: 600px;
                width: 100%;
            }
            button {
                background-color: #0275d8;
                border: none;
                padding: 10px 20px;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #025aa5;
            }
            pre {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
                text-align: left;
            }
            .alert {
                text-align: center;
                color: #333;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>Comparador de Arquivos XML</h1>
        <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="files" class="form-label">Selecione até 4 arquivos XML:</label>
                <input type="file" class="form-control" name="files" multiple>
            </div>
            <button type="submit" class="btn btn-primary">Comparar Arquivos</button>
        </form>
        {% if message %}
            <div class="alert alert-danger mt-3">{{ message }}</div>
        {% endif %}
        {% if diffs %}
            <h2 class="mt-4">Diferenças:</h2>
            <pre>{{ diffs }}</pre>
        {% endif %}
    </body>
    </html>
    """, message=message, diffs=diffs)


def comparar_arquivos(arquivos):
    # Abrir os arquivos e ler as linhas
    linhas = []
    for arquivo in arquivos:
        with open(arquivo, 'r') as f:
            linhas.append(f.readlines())

    # Encontrar o número máximo de linhas entre os arquivos carregados
    max_linhas = max(len(linha) for linha in linhas)

    # Verificar as diferenças entre as linhas dos arquivos carregados
    linhas_diferentes = []
    for i in range(max_linhas):
        linhas_atual = [linhas[j][i] if i < len(linhas[j]) else "NULL\n" for j in range(len(arquivos))]
        
        # Verificar se as linhas são diferentes
        if not all(linha == linhas_atual[0] for linha in linhas_atual):
            linhas_diferentes.append(f"Linha {i+1}:\n")
            for idx, linha in enumerate(linhas_atual):
                linhas_diferentes.append(f"Arquivo {idx+1}: {linha}")
            linhas_diferentes.append("\n")

    return ''.join(linhas_diferentes) if linhas_diferentes else "Os arquivos são iguais."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
