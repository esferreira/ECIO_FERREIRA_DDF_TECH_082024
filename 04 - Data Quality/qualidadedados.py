import os
import pandas as pd
import great_expectations as ge

# Diretório onde seus arquivos CSV estão localizados
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio = os.path.join(diretorio_atual, '..', 'olist')

# Lista para armazenar os DataFrames
dataframes = []

# Loop para processar cada arquivo no diretório
for nome_arquivo in os.listdir(diretorio):
    if nome_arquivo.endswith(".csv"):
        # Caminho completo para o arquivo
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Carregar os dados em um DataFrame do Pandas
        df = pd.read_csv(caminho_arquivo)
        df_ge = ge.from_pandas(df)

    # Definir suas expectativas
    if nome_arquivo == "olist_customers_dataset.csv":
        # Todas as colunas são importantes para entender os clientes, portanto, verificamos se há valores nulos em todas elas
        df_ge.expect_column_values_to_not_be_null("customer_id")
        df_ge.expect_column_values_to_not_be_null("customer_unique_id")
        df_ge.expect_column_values_to_not_be_null("customer_zip_code_prefix")
        df_ge.expect_column_values_to_not_be_null("customer_city")
        df_ge.expect_column_values_to_not_be_null("customer_state")

    elif nome_arquivo == "olist_geolocation_dataset.csv":
        # Todas as colunas são importantes para entender a geolocalização
        df_ge.expect_column_values_to_not_be_null("geolocation_zip_code_prefix")
        df_ge.expect_column_values_to_not_be_null("geolocation_lat")
        df_ge.expect_column_values_to_not_be_null("geolocation_lng")
        df_ge.expect_column_values_to_not_be_null("geolocation_city")
        df_ge.expect_column_values_to_not_be_null("geolocation_state")

        # Verificar se as coordenadas geográficas estão dentro de intervalos esperados para o Brasil
        df_ge.expect_column_values_to_be_between("geolocation_lat", -33.75, 5.26)  # Latitude do Brasil
        df_ge.expect_column_values_to_be_between("geolocation_lng", -73.99, -34.79)  # Longitude do Brasil

    elif nome_arquivo == "olist_order_items_dataset.csv":
        # Verificar valores nulos em colunas chave
        df_ge.expect_column_values_to_not_be_null("order_id")
        df_ge.expect_column_values_to_not_be_null("order_item_id")
        df_ge.expect_column_values_to_not_be_null("product_id")
        df_ge.expect_column_values_to_not_be_null("seller_id")
        df_ge.expect_column_values_to_not_be_null("shipping_limit_date")

        # Verificar se os preços e frete são valores numéricos positivos
        df_ge.expect_column_values_to_be_of_type("price", "float64")
        df_ge.expect_column_values_to_be_between("price", 0, None)
        df_ge.expect_column_values_to_be_of_type("freight_value", "float64")
        df_ge.expect_column_values_to_be_between("freight_value", 0, None)

    elif nome_arquivo == "olist_order_payments_dataset.csv":
        # Verificar valores nulos e tipos de dados em colunas chave
        df_ge.expect_column_values_to_not_be_null("order_id")
        df_ge.expect_column_values_to_not_be_null("payment_sequential")
        df_ge.expect_column_values_to_not_be_null("payment_type")
        df_ge.expect_column_values_to_not_be_null("payment_installments")
        df_ge.expect_column_values_to_not_be_null("payment_value")

        df_ge.expect_column_values_to_be_of_type("payment_sequential", "int64")
        df_ge.expect_column_values_to_be_of_type("payment_installments", "int64")
        df_ge.expect_column_values_to_be_of_type("payment_value", "float64")

        # Verificar se o número de parcelas é um valor inteiro positivo
        df_ge.expect_column_values_to_be_between("payment_installments", 0, None)

        # Verificar se o valor do pagamento é um valor numérico positivo
        df_ge.expect_column_values_to_be_between("payment_value", 0, None)

        # Verificar se o tipo de pagamento está dentro dos valores esperados
        expected_payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined']
        df_ge.expect_column_values_to_be_in_set("payment_type", expected_payment_types)

    elif nome_arquivo == "olist_order_reviews_dataset.csv":
        # Verificar valores nulos em colunas chave
        df_ge.expect_column_values_to_not_be_null("review_id")
        df_ge.expect_column_values_to_not_be_null("order_id")
        df_ge.expect_column_values_to_not_be_null("review_score")
        df_ge.expect_column_values_to_not_be_null("review_creation_date")
        df_ge.expect_column_values_to_not_be_null("review_answer_timestamp")

        # Verificar se o review_score está dentro do intervalo esperado (1 a 5)
        df_ge.expect_column_values_to_be_between("review_score", 1, 5)

        # Verificar se as datas estão em formato válido
        df_ge.expect_column_values_to_match_strftime_format("review_creation_date", "%Y-%m-%d %H:%M:%S")
        df_ge.expect_column_values_to_match_strftime_format("review_answer_timestamp", "%Y-%m-%d %H:%M:%S")

    elif nome_arquivo == "olist_orders_dataset.csv":
        # Verificar valores nulos em colunas chave
        df_ge.expect_column_values_to_not_be_null("order_id")
        df_ge.expect_column_values_to_not_be_null("customer_id")
        df_ge.expect_column_values_to_not_be_null("order_status")
        df_ge.expect_column_values_to_not_be_null("order_purchase_timestamp")
        df_ge.expect_column_values_to_not_be_null("order_approved_at")
        df_ge.expect_column_values_to_not_be_null("order_delivered_carrier_date")
        df_ge.expect_column_values_to_not_be_null("order_delivered_customer_date")
        df_ge.expect_column_values_to_not_be_null("order_estimated_delivery_date")

        # Verificar se o status do pedido está dentro dos valores esperados
        expected_order_status = ['delivered', 'invoiced', 'shipped', 'processing', 'unavailable', 'canceled', 'created', 'approved']
        df_ge.expect_column_values_to_be_in_set("order_status", expected_order_status)

        # Verificar se as datas estão em formato válido
        df_ge.expect_column_values_to_match_strftime_format("order_purchase_timestamp", "%Y-%m-%d %H:%M:%S")
        df_ge.expect_column_values_to_match_strftime_format("order_approved_at", "%Y-%m-%d %H:%M:%S")
        df_ge.expect_column_values_to_match_strftime_format("order_delivered_carrier_date", "%Y-%m-%d %H:%M:%S")
        df_ge.expect_column_values_to_match_strftime_format("order_delivered_customer_date", "%Y-%m-%d %H:%M:%S")
        df_ge.expect_column_values_to_match_strftime_format("order_estimated_delivery_date", "%Y-%m-%d")

    elif nome_arquivo == "olist_products_dataset.csv":
        # Verificar valores nulos em colunas chave
        df_ge.expect_column_values_to_not_be_null("product_id")
        df_ge.expect_column_values_to_not_be_null("product_category_name")
        df_ge.expect_column_values_to_not_be_null("product_name_lenght")
        df_ge.expect_column_values_to_not_be_null("product_description_lenght")
        df_ge.expect_column_values_to_not_be_null("product_photos_qty")
        df_ge.expect_column_values_to_not_be_null("product_weight_g")
        df_ge.expect_column_values_to_not_be_null("product_length_cm")
        df_ge.expect_column_values_to_not_be_null("product_height_cm")
        df_ge.expect_column_values_to_not_be_null("product_width_cm")

        # Verificar se as dimensões e peso do produto são valores numéricos positivos
        df_ge.expect_column_values_to_be_of_type("product_weight_g", "int64")
        df_ge.expect_column_values_to_be_between("product_weight_g", 0, None)
        df_ge.expect_column_values_to_be_of_type("product_length_cm", "int64")
        df_ge.expect_column_values_to_be_between("product_length_cm", 0, None)
        df_ge.expect_column_values_to_be_of_type("product_height_cm", "int64")
        df_ge.expect_column_values_to_be_between("product_height_cm", 0, None)
        df_ge.expect_column_values_to_be_of_type("product_width_cm", "int64")
        df_ge.expect_column_values_to_be_between("product_width_cm", 0, None)

        # Verificar se a quantidade de fotos é um valor inteiro não negativo
        df_ge.expect_column_values_to_be_of_type("product_photos_qty", "int64")
        df_ge.expect_column_values_to_be_between("product_photos_qty", 0, None)

    elif nome_arquivo == "olist_sellers_dataset.csv":
        # Todas as colunas são importantes para entender os vendedores, portanto, verificamos se há valores nulos em todas elas
        df_ge.expect_column_values_to_not_be_null("seller_id")
        df_ge.expect_column_values_to_not_be_null("seller_zip_code_prefix")
        df_ge.expect_column_values_to_not_be_null("seller_city")
        df_ge.expect_column_values_to_not_be_null("seller_state")

    elif nome_arquivo == "product_category_name_translation.csv":
        # Verificar se há valores nulos nas colunas chave
        df_ge.expect_column_values_to_not_be_null("product_category_name")
        df_ge.expect_column_values_to_not_be_null("product_category_name_english")

    # Salvar suas expectativas
    caminho_expectativas = os.path.join(diretorio_atual, f"expectativas_{nome_arquivo}.json")
    df_ge.save_expectation_suite(caminho_expectativas)

    # Validar seus dados contra suas expectativas
    results = df_ge.validate(expectation_suite=caminho_expectativas)

    # Imprimir os resultados para um arquivo de texto
    caminho_relatorio = os.path.join(diretorio_atual, f"relatorio_{nome_arquivo}.txt")
    with open(caminho_relatorio, "w") as file:
        print(results, file=file)