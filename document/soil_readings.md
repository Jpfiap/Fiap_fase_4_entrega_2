# Documentação das Leituras do Solo

## Estrutura da Tabela

A tabela `leitura_solo` foi criada para armazenar as leituras de sensores do solo. Ela possui a seguinte estrutura:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_leitura_solo | SERIAL | Chave primária |
| id_sensor | INTEGER | ID do sensor que fez a leitura (FK) |
| data_hora | TIMESTAMP | Data e hora da leitura |
| fosforo_ok | BOOLEAN | Status do fósforo (true = OK, false = Não) |
| potassio_ok | BOOLEAN | Status do potássio (true = OK, false = Não) |
| ph | NUMERIC(4,2) | Valor do pH do solo |
| ph_status | VARCHAR(20) | Status do pH (OK/Fora da faixa) |
| umidade | NUMERIC(5,2) | Valor da umidade do solo |
| umidade_status | VARCHAR(20) | Status da umidade (OK/Fora da faixa) |
| irrigacao | VARCHAR(20) | Status da irrigação (Ativa/Inativa) |

## Importação de Dados

Para importar dados de leituras do solo, use o script `scripts/import_soil_readings.py`. O script aceita dois parâmetros:

1. Caminho do arquivo CSV com as leituras
2. ID do sensor que fez as leituras

Exemplo de uso:
```bash
python scripts/import_soil_readings.py dados_leituras.csv 1
```

O arquivo CSV deve ter o seguinte formato:
```
Fósforo_OK,Potássio_OK,pH,pH_Status,Umidade,Umidade_Status,Irrigação
Não,Não,3.40,Fora da faixa,86.50,Fora da faixa,Inativa
...
```

## Valores de Referência

- **pH**: 
  - OK: 5.5 a 6.5
  - Fora da faixa: < 5.5 ou > 6.5

- **Umidade**:
  - OK: 45% a 65%
  - Fora da faixa: < 45% ou > 65%

- **Irrigação**:
  - Ativa: Quando a umidade está dentro da faixa ideal
  - Inativa: Quando a umidade está fora da faixa ideal

## Relacionamentos

- A tabela `leitura_solo` está relacionada com a tabela `sensor` através do campo `id_sensor`
- Cada leitura deve estar associada a um sensor válido
- O sensor deve estar associado a um lote válido
- O lote deve estar associado a uma cultura válida 