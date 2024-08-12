import os
import json

# Diretório onde seus arquivos JSON estão localizados
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Loop para processar cada arquivo no diretório
for nome_arquivo in os.listdir(diretorio_atual):
    if nome_arquivo.startswith("relatorio_") and nome_arquivo.endswith(".txt"):
        # Caminho completo para o arquivo JSON
        caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)

        # Carregar o conteúdo do arquivo JSON
        with open(caminho_arquivo, "r") as f:
            resultados = json.load(f)

        # Extrair o nome da tabela do nome do arquivo
        nome_tabela = nome_arquivo.replace("relatorio_", "").replace(".json", "")

        # Abrir um arquivo TXT para o relatório formatado
        with open(f"relatorio_formatado_{nome_tabela}.txt", "w", encoding="utf-8") as f_relatorio:
            # Escrever o cabeçalho do relatório
            f_relatorio.write(f"Relatório de Validação de Dados - Tabela: {nome_tabela}\n\n")

            # Iterar sobre os resultados de cada expectativa
            for resultado in resultados["results"]:
                # Extrair informações relevantes
                nome_coluna = resultado["expectation_config"]["kwargs"]["column"]
                tipo_expectativa = resultado["expectation_config"]["expectation_type"]
                sucesso = resultado["success"]
                valores_inesperados = resultado["result"].get("unexpected_count", 0)
                valores_ausentes = resultado["result"].get("missing_count", 0)

                # Escrever uma linha formatada no relatório
                f_relatorio.write(f"Coluna: {nome_coluna}, Expectativa: {tipo_expectativa}, Sucesso: {sucesso}, Valores Inesperados: {valores_inesperados}, Valores Ausentes: {valores_ausentes}\n")

        # Indicar que o relatório foi gerado
        print(f"Relatório formatado gerado para a tabela: {nome_tabela}")
