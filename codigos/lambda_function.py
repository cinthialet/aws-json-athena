import json
import boto3
import pandas as pd
from io import StringIO
import os

# Funções auxiliares
print('Carregando funcoes auxiliares...')
def determinar_turno(hora):
    hora_int = int(hora.split(':')[0])
    if 7 <= hora_int < 12:
        return 'manhã'
    elif 12 <= hora_int < 18:
        return 'tarde'
    else:
        return 'noite'

def formatar_servico(servico):
    servico_formatado = servico.replace(' + ', '&').title()
    return servico_formatado

def determinar_porte(peso):
    if peso < 5:
        return 'PEQ'
    elif 5 <= peso < 10:
        return 'MED'
    else:
        return 'GRAN'

def formatar_telefone(telefone):
    return telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
print('Funcoes auxiliares carregadas com sucesso')


def lambda_handler(event, context):
    try:
        # Inicializa o cliente S3
        s3 = boto3.client('s3')

        # Nome do bucket de entrada e chave do arquivo JSON recebido
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        print('Extraindo dados...')
        # Baixa o arquivo JSON do S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read()
        dados_json = json.loads(content)['agendamentos']
        print('Dados extraidos com sucesso')
        
        # Transformando os dados
        print('Iniciando as transformacoes dos dados...')
        df = pd.DataFrame({
            'agendamento': [f"{item['agendamento']['data']} {item['agendamento']['hora']}" for item in dados_json],
            'turno': [determinar_turno(item['agendamento']['hora']) for item in dados_json],
            'servico': [formatar_servico(item['agendamento']['servico']) for item in dados_json],
            'nome_pet': [item['pet']['nome'].title() for item in dados_json],
            'tipo': [item['pet']['informacoes'].split('.')[0].upper() for item in dados_json],
            'raca': [item['pet']['informacoes'].split('.')[1].replace('_', ' ').title() for item in dados_json],
            'cor': [item['pet']['informacoes'].split('.')[2].upper() for item in dados_json],
            'genero': [item['pet']['informacoes'].split('.')[3][0].upper() for item in dados_json],
            'peso_kg': [float(item['pet']['peso']) for item in dados_json],
            'porte': [determinar_porte(float(item['pet']['peso'])) for item in dados_json],
            'nome_tutor': [item['dono']['nome'].title() for item in dados_json],
            'endereco': [item['dono']['endereco'] for item in dados_json],
            'email': [item['dono']['email'] for item in dados_json],
            'telefone': [formatar_telefone(item['dono']['telefone']) for item in dados_json]
        })
        print("Dados tranformados com sucesso")
        
        print('Salvando os dados em um arquivo csv')
        # Salvando o df em um arquivo CSV com ponto e vírgula como delimitador
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig') #falta explicar

        # Nome do bucket de saída obtido da variável de ambiente
        output_bucket = os.environ['RESULT_PIPELINE_BUCKET']
        output_file_key = 'resultado_etl.csv'

        # Fazendo o upload do CSV para o bucket de saída
        s3.put_object(Bucket=output_bucket, Key=output_file_key, Body=csv_buffer.getvalue())
        print('Dados salvos com sucesso')

        return 'Processo de ETL concluído com sucesso'

    except Exception as e:
        print(e)
        return 'Erro durante o processamento do ETL'


