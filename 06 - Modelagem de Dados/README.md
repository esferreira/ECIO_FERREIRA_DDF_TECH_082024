## README - Modelagem Dimensional Olist

Este README descreve a estrutura do Data Warehouse (DW) `olist_dw` e suas tabelas, construído a partir da base de dados da Olist. O objetivo principal é fornecer informações sobre cada tabela, incluindo sua finalidade, colunas e relacionamentos, para facilitar a compreensão e utilização do DW em análises e visualizações de dados.

Tabelas de Dimensão:

 `dim_customer`
     Finalidade: Armazena informações sobre os clientes.
     Colunas:
         `customer_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `customer_id`: ID original do cliente na base de dados da Olist.
         `customer_unique_id`: ID único do cliente.
         `customer_zip_code_prefix`: CEP do cliente.
         `customer_city`: Cidade do cliente.
         `customer_state`: Estado do cliente.

 `dim_geolocation`
     Finalidade: Armazena informações geográficas sobre os CEPs, como cidade e estado.
     Colunas:
         `geolocation_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `geolocation_zip_code_prefix`: CEP.
         `geolocation_city`: Cidade.
         `geolocation_state`: Estado.

 `dim_geolocation_latlng`
     Finalidade: Armazena informações geográficas sobre os CEPs, como latitude e longitude.
     Colunas:
         `geolocation_latlng_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `geolocation_zip_code_prefix`: CEP.
         `geolocation_lat`: Latitude.
         `geolocation_lng`: Longitude.

 `dim_product`
     Finalidade: Armazena informações sobre os produtos.
     Colunas:
         `product_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `product_id`: ID original do produto na base de dados da Olist.
         `product_category_name`: Nome da categoria do produto.
         `product_name_lenght`: Comprimento do nome do produto.
         `product_description_lenght`: Comprimento da descrição do produto.
         `product_photos_qty`: Quantidade de fotos do produto.
         `product_weight_g`: Peso do produto em gramas.
         `product_length_cm`: Comprimento do produto em centímetros.
         `product_height_cm`: Altura do produto em centímetros.
         `product_width_cm`: Largura do produto em centímetros.

 `dim_seller`
     Finalidade: Armazena informações sobre os vendedores.
     Colunas:
         `seller_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `seller_id`: ID original do vendedor na base de dados da Olist
         `seller_zip_code_prefix`: CEP do vendedor.
         `seller_city`: Cidade do vendedor.
         `seller_state`: Estado do vendedor.

 `dim_data`
     Finalidade: Armazena informações sobre datas, permitindo análises temporais.
     Colunas:
         `date_sk`: Chave primária da tabela, gerada automaticamente (UUID).
         `data_completa`: Data completa.
         `ano`: Ano.
         `mes`: Mês.
         `dia`: Dia.
         `dia_do_ano`: Dia do ano.
         `semana_do_ano`: Semana do ano.
         `dia_da_semana`: Dia da semana (numérico).
         `nome_dia_da_semana`: Nome do dia da semana.
         `estacao`: Estação do ano.

Tabela de Fatos:

 `fact_order`
     Finalidade: Armazena informações sobre os pedidos, incluindo métricas de vendas, frete e datas.
     Colunas:
         `order_id`: ID original do pedido na base de dados da Olist
         `customer_sk`: Chave estrangeira para a dimensão `dim_customer`.
         `product_sk`: Chave estrangeira para a dimensão `dim_product`.
         `seller_sk`: Chave estrangeira para a dimensão `dim_seller`.
         `customer_geolocation_sk`: Chave estrangeira para a dimensão `dim_geolocation` (localização do cliente).
         `seller_geolocation_sk`: Chave estrangeira para a dimensão `dim_geolocation` (localização do vendedor).
         `shipping_limit_date`: Data limite para envio do pedido.
         `price`: Preço do pedido.
         `freight_value`: Valor do frete do pedido.
         `order_purchase_date_sk`: Chave estrangeira para a dimensão `dim_data` (data da compra).
         `order_approved_at_sk`: Chave estrangeira para a dimensão `dim_data` (data da aprovação).
         `order_delivered_carrier_date_sk`: Chave estrangeira para a dimensão `dim_data` (data de entrega à transportadora).
         `order_delivered_customer_date_sk`: Chave estrangeira para a dimensão `dim_data` (data de entrega ao cliente).
         `order_estimated_delivery_date_sk`: Chave estrangeira para a dimensão `dim_data` (data estimada de entrega).

Relacionamentos:

 `fact_order.customer_sk` -> `dim_customer.customer_sk`
 `fact_order.product_sk` -> `dim_product.product_sk`
 `fact_order.seller_sk` -> `dim_seller.seller_sk`
 `fact_order.customer_geolocation_sk` -> `dim_geolocation.geolocation_sk`
 `fact_order.seller_geolocation_sk` -> `dim_geolocation.geolocation_sk`
 `fact_order.order_purchase_date_sk` -> `dim_data.date_sk`
 `fact_order.order_approved_at_sk` -> `dim_data.date_sk`
 `fact_order.order_delivered_carrier_date_sk` -> `dim_data.date_sk`
 `fact_order.order_delivered_customer_date_sk` -> `dim_data.date_sk`
 `fact_order.order_estimated_delivery_date_sk` -> `dim_data.date_sk`
 `dim_geolocation.geolocation_zip_code_prefix` -> `dim_geolocation_latlng.geolocation_zip_code_prefix` 

Observações:

 A chave primária de cada tabela de dimensão é uma chave subsituta gerada automaticamente (UUID) para garantir a unicidade e facilitar a integração com outras fontes de dados.
 A tabela de fatos `fact_order` contém as chaves estrangeiras que estabelecem os relacionamentos com as tabelas de dimensão, permitindo análises que combinam informações de diferentes dimensões.
 A dimensão `dim_geolocation` foi dividida em duas tabelas para evitar problemas de chave composta em ferramentas de BI e otimizar o desempenho das consultas.
 As queries SQL apresentadas anteriormente demonstram como utilizar esse modelo dimensional para responder a perguntas de negócio relevantes, tanto em termos gerais quanto com foco em análises geográficas. 

Este README fornece uma visão geral da estrutura do DW `olist_dw`. Para mais detalhes sobre as queries SQL e as análises possíveis, consulte a documentação completa do projeto. 