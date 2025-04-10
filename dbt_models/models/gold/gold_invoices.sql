WITH cte_silver_invoice_jornada AS (
    SELECT
        cv,
        n_nota,
        data_de_pregao,
        qted,
        mercadoria,
        txop,
        tx_corretagem,
        cotacao,
        movimentacao
    FROM
        {{ ref('silver_invoice_jornada') }}
),

cte_silver_invoice_redrex AS (
    SELECT
        cv,
        n_nota,
        data_de_pregao,
        qted,
        mercadoria,
        txop,
        tx_corretagem,
        cotacao,
        movimentacao
    FROM
        {{ ref('silver_invoice_redrex') }}
)

SELECT * 
FROM cte_silver_invoice_jornada

UNION ALL

SELECT * 
FROM cte_silver_invoice_redrex