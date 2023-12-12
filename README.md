# Processo ETL de Arquivo JSON com Lambda e Consulta com Athena

Este projeto demonstra um processo ETL (Extract, Transform, Load) automatizado na AWS, utilizando funções Lambda para manipular arquivos JSON. 
O processo envolve a leitura de dados de um bucket S3, a transformação desses dados e, em seguida, o carregamento em um novo bucket S3 em formato CSV.

## Sobre os Dados

Os dados de entrada deste projeto estão no formato JSON e consistem em uma lista de agendamentos para serviços de pet shop. 
Cada agendamento contém informações sobre o pet, o dono do pet e detalhes do agendamento.

### Estrutura dos Dados

Os dados são estruturados da seguinte forma:

- **agendamentos**: Uma lista de objetos, onde cada objeto representa um agendamento único e contém:
  - **pet**: Informações sobre o pet, incluindo:
    - `nome`: Nome do pet.
    - `informacoes`: Detalhes do pet, como espécie, raça, cor e gênero.
    - `peso`: Peso do pet em Kg.
  - **dono**: Informações sobre o dono do pet, incluindo:
    - `nome`: Nome do dono.
    - `endereco`: Endereço do dono.
    - `email`: E-mail do dono.
    - `telefone`: Telefone do dono.
  - **agendamento**: Detalhes do agendamento, incluindo:
    - `hora`: Hora do agendamento.
    - `data`: Data do agendamento.
    - `servico`: Tipo de serviço agendado (banho, tosa, banho&tosa)

## Arquitetura
A Arquitetura para esse projeto na AWS segue a imagem abaixo :

![arq](https://github.com/cinthialet/aws-json-athena/blob/main/img/arquitetura-aws3.png)

O projeto é estruturado da seguinte forma:

1. **Buckets S3**: 
    - `aws-bucket-input`: Recebe o arquivo JSON. Este evento dispara a função Lambda.
    - `aws-bucket-output`: Armazena o arquivo CSV após a transformação ETL.
    - `dependencias-scripts`: Contém as dependências dos scripts Python.

2. **Função Lambda**: 
    - Monitora o bucket de entrada para o disparo do processo ETL.
    - Extrai os dados, realiza a transformação dos dados e os carrega no bucket de saída (ETL).
    - Monitora o processo ETL pelos logs no Cloudwatch.
    - Aqui se encontram o [Código](https://github.com/cinthialet/aws-json-athena/blob/main/codigos/lambda_function.py) e o processo de geração e carregamento das [Dependências](https://github.com/cinthialet/aws-json-athena/blob/main/doc/processo-dependencia-lambda-aws) do projeto

3. **Integração com o Athena**: 
    - Consulta os dados transformados armazenados no bucket de saída. [Query Athena](https://github.com/cinthialet/aws-json-athena/blob/main/codigos/sql-athena)
    - O resultado das consultas são salvos em `aws-bucket-output/athena`
![athena-result](https://github.com/cinthialet/aws-json-athena/blob/main/img/resultado-query-athena.png)

## Nota
Foi identificado um erro de parsing durante o processo, pela natureza dos dados e o modo como o arquivo csv foi gerado:
![erro-parsing](https://github.com/cinthialet/aws-json-athena/blob/main/img/erro_parsing.png)

- A solução pode ser encontrada nessa [Documentação](https://github.com/cinthialet/aws-json-athena/blob/main/doc/Implementa%C3%A7%C3%A3o%20projeto%20AWS%20pipe)
