import json
import math
import csv

# Função para calcular a distância euclidiana de uma coordenada ao ponto [50:50]
def calcular_distancia(coordenada):
    x, y = map(int, coordenada.strip('[]').split(':'))
    return math.sqrt((x - 50) ** 2 + (y - 50) ** 2)

# Carregando os dados do arquivo JSON
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Ignorando a linha de cabeçalho
data = data[1:]

# Dicionário para armazenar as ilhas e suas equipes e jogadores
ilhas = {}

# Processando os dados
for entry in data:
    if len(entry) < 9:
        continue  # Ignorar entradas que não têm todos os campos necessários

    nome_jogador = entry[0]
    aliança = entry[1]
    nome_cidade = entry[2]
    coordenada = entry[4]
    nome_ilha = entry[8]

    jogador_info = f"{nome_cidade} ({nome_jogador} - {aliança})"

    if coordenada not in ilhas:
        ilhas[coordenada] = {'nome_ilha': nome_ilha, 'equipes': set(), 'jogadores': {}}
    
    ilhas[coordenada]['equipes'].add(aliança)
    if aliança not in ilhas[coordenada]['jogadores']:
        ilhas[coordenada]['jogadores'][aliança] = []
    ilhas[coordenada]['jogadores'][aliança].append(jogador_info)

# Filtrando as ilhas que têm membros de mais de uma equipe
ilhas_com_multiplas_equipes = {coord: info for coord, info in ilhas.items() if len(info['equipes']) > 1}

# Ordenando as ilhas pela proximidade ao ponto [50:50]
ilhas_ordenadas = sorted(ilhas_com_multiplas_equipes.items(), key=lambda item: calcular_distancia(item[0]))

# Identificando as alianças presentes nas ilhas com múltiplas equipes
alianças = set()
for info in ilhas_com_multiplas_equipes.values():
    alianças.update(info['equipes'])

# Convertendo o conjunto de alianças em uma lista para facilitar a formatação do título
alianças = sorted(list(alianças))

# Escrevendo os resultados em um arquivo CSV
with open('analise.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    header = ['Ilha', 'Coordenada'] + [f'Cidades (Nome Jogador) da {equipe}' for equipe in sorted(ilhas_ordenadas[0][1]['equipes'])]
    csvwriter.writerow(header)
    for coordenada, info in ilhas_ordenadas:
        row = [info['nome_ilha'], coordenada]
        for equipe in sorted(info['equipes']):
            row.append('; '.join(info['jogadores'][equipe]))
        csvwriter.writerow(row)

# Escrevendo os resultados em um arquivo HTML com Bootstrap
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Ilhas {alianças[0]} vs {alianças[1]}</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Análise de Ilhas {alianças[0]} vs {alianças[1]}</h1>
        <table class="table table-striped mt-3">
            <thead>
                <tr>
                    <th>Ilha</th>
                    <th>Coordenada</th>
'''

for equipe in sorted(ilhas_ordenadas[0][1]['equipes']):
    html_content += f'<th>Cidades (Nome Jogador) da {equipe}</th>'

html_content += '''
                </tr>
            </thead>
            <tbody>
'''

for coordenada, info in ilhas_ordenadas:
    html_content += f'''
                <tr>
                    <td>{info['nome_ilha']}</td>
                    <td>{coordenada}</td>
    '''
    for equipe in sorted(info['equipes']):
        html_content += '<td><ul>'
        for jogador in info['jogadores'][equipe]:
            html_content += f'<li>{jogador}</li>'
        html_content += '</ul></td>'
    html_content += '</tr>'

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

with open('analise.html', 'w', encoding='utf-8') as htmlfile:
    htmlfile.write(html_content)

print("Resultados salvos em analise.csv e analise.html")