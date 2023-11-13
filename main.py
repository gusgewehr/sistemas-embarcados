from flask import Flask, render_template, request
import csv

app = Flask(__name__)

dados_esp32 = []
nome_arquivo_csv = 'dados_esp32.csv'

@app.route('/')
def index():
    return render_template('/index.html', dados=dados_esp32)

@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    if request.method == 'POST':
        valor_adc = request.form['valor_adc']
        dados_esp32.append(valor_adc)
        print(valor_adc)  # Exibe os dados recebidos no console
        salvar_csv(nome_arquivo_csv, dados_esp32)
    return 'Sucesso', 200

def salvar_csv(nome_arquivo, dados):
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        # Escreve os dados no arquivo CSV
        for linha in dados:
            escritor_csv.writerow([linha])


# Função para carregar dados do arquivo CSV ao iniciar o servidor
def carregar_dados_csv(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            for linha in leitor_csv:
                dados_esp32.append(linha)
    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado. Criando um novo arquivo.")



    
carregar_dados_csv(nome_arquivo_csv)
app.run(debug=True, host='0.0.0.0', port=5000)