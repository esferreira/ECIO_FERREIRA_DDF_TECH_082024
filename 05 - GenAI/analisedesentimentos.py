import os
import pandas as pd
import openai
from tqdm import tqdm

# Diretório onde seus arquivos CSV estão localizados
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio = os.path.join(diretorio_atual, '..', 'olist')

# Configurar a chave da API da OpenAI
openai.api_key = 'seu_token'

# Loop para processar cada arquivo no diretório
for nome_arquivo in os.listdir(diretorio):
    if nome_arquivo == "olist_order_reviews_dataset.csv":
        # Caminho completo para o arquivo
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Carregar os dados em um DataFrame do Pandas
        df = pd.read_csv(caminho_arquivo)

        # Limitar a quantidade de registros para analisar
        df = df.head(10)

        # Lista para armazenar os sentimentos
        sentimentos = []

        # Loop através das linhas do dataframe
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            # Se houver um comentário, analise o sentimento
            if pd.notnull(row['review_comment_message']):
                response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": row['review_comment_message']}
                    ]
                )
                sentiment = response['choices'][0]['message']['content']
                sentimentos.append(sentiment)
            else:
                sentimentos.append('')

        # Adicione a lista de sentimentos ao dataframe como uma nova coluna
        df['sentiment'] = sentimentos

        # Salve o dataframe em um novo arquivo CSV
        df.to_csv('olist_order_reviews_with_sentiment.csv', index=False)