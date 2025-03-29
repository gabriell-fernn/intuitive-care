CREATE TABLE operadoras (
    registro_ans INT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(25),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_de_comercializacao INT,
    data_registro_ans DATE
);

CREATE TABLE transacoes (
	id SERIAL PRIMARY KEY,
	data DATE,
	reg_ans INT,
	cd_conta_contabil VARCHAR(15),
	descricao VARCHAR(250),
	vl_saldo_inicial VARCHAR(30) NOT NULL,
    vl_saldo_final VARCHAR(30) NOT NULL
)

COPY transacoes (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
FROM 'C:/Users/Public/4T2023.csv' 
DELIMITER ';' CSV HEADER;

COPY transacoes (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
FROM 'C:/Users/Public/4T2024.csv' 
DELIMITER ';' CSV HEADER;

ALTER TABLE transacoes
  ALTER COLUMN vl_saldo_inicial TYPE NUMERIC USING REPLACE(vl_saldo_inicial, ',', '.')::NUMERIC;
  ALTER COLUMN vl_saldo_final TYPE NUMERIC USING REPLACE(vl_saldo_final, ',', '.')::NUMERIC;

COPY operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans) 
FROM 'C:/Users/Public/operadoras.csv' 
DELIMITER ';' CSV HEADER;

WITH despesas_filtradas AS (
    SELECT
        registro AS operadora,
        SUM(vl_saldo_final - vl_saldo_inicial) AS total_despesa
    FROM transacoes
    WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
      AND data BETWEEN DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'
                  AND DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '1 day'
    GROUP BY registro
)
SELECT 
    operadora,
    total_despesa,
    RANK() OVER (ORDER BY total_despesa DESC) AS ranking
FROM despesas_filtradas
LIMIT 10;

SELECT
    registro,
    SUM(vl_saldo_inicial - vl_saldo_final) AS despesas_totais
FROM
    transacoes
WHERE
    data >= CURRENT_DATE - INTERVAL '1 year'
	AND descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY
    registro
ORDER BY
    despesas_totais DESC
LIMIT 10;