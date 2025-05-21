# Configurações do banco de dados PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'monitoramento_agricola',
    'user': 'postgres',
    'password': 'pgsql1234'
}

SEQUENCES = {
    'cultura': 'cultura_seq',
    'lote': 'lote_seq',
    'sensor': 'sensor_seq',
    'leitura': 'leitura_seq',
    'ajuste': 'ajuste_seq',
    'leitura_solo': 'leitura_solo_seq'
}

# Configurações das tabelas
TABLES = {
    'cultura': {
        'name': 'cultura',
        'columns': [
            'id_cultura SERIAL PRIMARY KEY',
            'nome VARCHAR(100) NOT NULL',
            'tipo VARCHAR(50) NOT NULL',
            'data_plantio DATE NOT NULL',
            'data_colheita_prevista DATE',
            'status VARCHAR(20) NOT NULL',
            'necessidade_agua_min NUMERIC(5,2) NOT NULL',
            'necessidade_agua_max NUMERIC(5,2) NOT NULL',
            'necessidade_ph_min NUMERIC(4,2) NOT NULL',
            'necessidade_ph_max NUMERIC(4,2) NOT NULL',
            'necessidade_fosforo_min NUMERIC(5,2) NOT NULL',
            'necessidade_fosforo_max NUMERIC(5,2) NOT NULL',
            'necessidade_potassio_min NUMERIC(5,2) NOT NULL',
            'necessidade_potassio_max NUMERIC(5,2) NOT NULL'
        ]
    },
    'lote': {
        'name': 'lote',
        'columns': [
            'id_lote SERIAL PRIMARY KEY',
            'id_cultura INTEGER NOT NULL',
            'area NUMERIC(10,2) NOT NULL',
            'localizacao VARCHAR(200) NOT NULL',
            'status VARCHAR(20) NOT NULL',
            'FOREIGN KEY (id_cultura) REFERENCES cultura(id_cultura)'
        ]
    },
    'sensor': {
        'name': 'sensor',
        'columns': [
            'id_sensor SERIAL PRIMARY KEY',
            'id_lote INTEGER NOT NULL',
            'tipo VARCHAR(50) NOT NULL',
            'modelo VARCHAR(100) NOT NULL',
            'data_instalacao DATE NOT NULL',
            'status VARCHAR(20) NOT NULL',
            'FOREIGN KEY (id_lote) REFERENCES lote(id_lote)'
        ]
    },
    'leitura_sensor': {
        'name': 'leitura_sensor',
        'columns': [
            'id_leitura SERIAL PRIMARY KEY',
            'id_sensor INTEGER NOT NULL',
            'data_hora TIMESTAMP NOT NULL',
            'valor NUMERIC(10,2) NOT NULL',
            'unidade VARCHAR(20) NOT NULL',
            'FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor)'
        ]
    },
    'ajuste': {
        'name': 'ajuste',
        'columns': [
            'id_ajuste SERIAL PRIMARY KEY',
            'id_lote INTEGER NOT NULL',
            'tipo VARCHAR(50) NOT NULL',
            'data_hora TIMESTAMP NOT NULL',
            'descricao VARCHAR(500)',
            'status VARCHAR(20) NOT NULL',
            'FOREIGN KEY (id_lote) REFERENCES lote(id_lote)'
        ]
    },
    'leitura_solo': {
        'name': 'leitura_solo',
        'columns': [
            'id_leitura_solo SERIAL PRIMARY KEY',
            'id_sensor INTEGER NOT NULL',
            'data_hora TIMESTAMP NOT NULL',
            'fosforo_ok BOOLEAN NOT NULL',
            'potassio_ok BOOLEAN NOT NULL',
            'ph NUMERIC(6,2) NOT NULL',
            'ph_status VARCHAR(20) NOT NULL',
            'umidade NUMERIC(8,2) NOT NULL',
            'umidade_status VARCHAR(20) NOT NULL',
            'irrigacao VARCHAR(20) NOT NULL',
            'FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor)'
        ]
    }
}
