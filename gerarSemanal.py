import json
import os
from datetime import datetime

# Carregando os dados do arquivo JSON
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Ignorando a linha de cabeçalho
data = data[1:]

# Filtrando os membros da aliança BRICS
brics_members = [entry for entry in data if len(entry) > 2 and entry[2] == 'BRICS']

# Nome do arquivo do pseudobanco de dados
db_filename = 'dataBase.json'

# Carregando o pseudobanco de dados se existir, caso contrário, inicializando um novo
if os.path.exists(db_filename):
    with open(db_filename, 'r', encoding='utf-8') as db_file:
        pseudobanco = json.load(db_file)
else:
    pseudobanco = {'jogadores': {}}

# Data e hora atual
data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Atualizando o pseudobanco de dados com as novas leituras
for member in brics_members:
    nome = member[0]
    pontuacao = member[1]
    if nome not in pseudobanco['jogadores']:
        pseudobanco['jogadores'][nome] = {'pontuacoes': [], 'datas': []}
    pseudobanco['jogadores'][nome]['pontuacoes'].append(pontuacao)
    pseudobanco['jogadores'][nome]['datas'].append(data_hora_atual)
    # Mantendo apenas as últimas 5 leituras
    if len(pseudobanco['jogadores'][nome]['pontuacoes']) > 5:
        pseudobanco['jogadores'][nome]['pontuacoes'] = pseudobanco['jogadores'][nome]['pontuacoes'][-5:]
        pseudobanco['jogadores'][nome]['datas'] = pseudobanco['jogadores'][nome]['datas'][-5:]

# Salvando o pseudobanco de dados atualizado
with open(db_filename, 'w', encoding='utf-8') as db_file:
    json.dump(pseudobanco, db_file, indent=4, ensure_ascii=False)

# Criando o título e o nome do arquivo HTML dinamicamente
titulo = 'Relatório Semanal de Desenvolvimento - BRICS'
nome_arquivo_html = 'relatorio_semanal_BRICS.html'

# Escrevendo os resultados em um arquivo HTML com Bootstrap
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">{titulo}</h1>
        <table class="table table-striped mt-3">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Pontuação Atual</th>
                    <th>Cidades [Localização da Ilha]</th>
                    <th>Últimas 5 Pontuações</th>
                </tr>
            </thead>
            <tbody>
'''

for member in brics_members:
    nome = member[0]
    pontuacao = member[1]
    cidades = f"{member[3]} [{member[5]}]"
    ultimas_pontuacoes = pseudobanco['jogadores'][nome]['pontuacoes']
    ultimas_datas = pseudobanco['jogadores'][nome]['datas']
    html_content += f'''
                <tr>
                    <td>{nome}</td>
                    <td>{pontuacao}</td>
                    <td>{cidades}</td>
                    <td><ul>
    '''
    for p, d in zip(ultimas_pontuacoes, ultimas_datas):
        html_content += f'<li>{p} ({d})</li>'
    html_content += '''
                    </ul></td>
                </tr>
    '''

html_content += '''
            </tbody>
        </table>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

with open(nome_arquivo_html, 'w', encoding='utf-8') as htmlfile:
    htmlfile.write(html_content)

print(f"Resultados salvos em {nome_arquivo_html}")