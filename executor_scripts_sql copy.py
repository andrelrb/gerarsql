# Nome do arquivo: executor_scripts_sql.py
import os
import datetime
import psycopg2

# --- Configurações do Banco de Dados ---
DB_HOST = os.environ.get('DB_HOST_SIGTAP', 'localhost')
DB_NAME = os.environ.get('DB_NAME_SIGTAP', 'sigtap')
DB_USER = os.environ.get('DB_USER_SIGTAP', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD_SIGTAP', 'root') # LEMBRE-SE DE CONFIGURAR NO AMBIENTE!
DB_PORT = os.environ.get('DB_PORT_SIGTAP', '5432')

# --- Configurações Gerais do Script ---
# Caminho base onde as pastas 'insert_DDMMYYYY' com os scripts SQL estão
CAMINHO_BASE_PASTAS_SQL = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\GerarSQL'

# Ordem de processamento das tabelas (deve corresponder à ordem de geração dos scripts)
ORDEM_PROCESSAMENTO_TABELAS = [
    'tb_detalhe', 'tb_ocupacao', 'tb_financiamento', 'tb_habilitacao',
    'tb_tipo_leito', 'tb_grupo', 'tb_registro', 'tb_rede_atencao',
    'tb_renases', 'tb_regra_condicionada', 'tb_rubrica',
    'tb_cid', 'tb_modalidade', 'tb_grupo_habilitacao', 'tb_servico', 'tb_tuss',
    'tb_sub_grupo', 'tb_componente_rede', 'tb_servico_classificacao',
    'tb_descricao_detalhe', 'tb_forma_organizacao', 'tb_procedimento',
    'tb_descricao', 
    'rl_procedimento_sia_sih',
    'tb_sia_sih',
    'rl_procedimento_habilitacao', 'rl_procedimento_renases',
    'rl_procedimento_tuss', 'rl_procedimento_comp_rede',
    'rl_procedimento_cid', 'rl_procedimento_modalidade', 'rl_procedimento_ocupacao',
    'rl_procedimento_servico', 'rl_procedimento_leito', 'rl_procedimento_detalhe',
    'rl_excecao_compatibilidade', 'rl_procedimento_registro',
    'rl_procedimento_compativel', 'rl_procedimento_regra_cond',
    'rl_procedimento_origem', 'rl_procedimento_incremento'
]
# Codificação dos arquivos .sql gerados (geralmente utf-8 é seguro para SQL)
CODIFICACAO_ARQUIVOS_SQL = 'utf-8'


# --- Funções Auxiliares ---
def connect_db():
    conn_string = f"host='{DB_HOST}' dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}' port='{DB_PORT}'"
    try:
        conn = psycopg2.connect(conn_string)
        print(f"Conectado ao banco de dados '{DB_NAME}' em '{DB_HOST}'.")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def encontrar_pasta_scripts_sql(data_str):
    """
    Valida o formato da data e constrói o nome da pasta de scripts SQL.
    Retorna o caminho completo da pasta ou None se inválido/não encontrada.
    """
    try:
        datetime.datetime.strptime(data_str, '%d%m%Y') # Valida formato DDMMYYYY
        nome_pasta = f"insert_{data_str}"
        caminho_pasta = os.path.join(CAMINHO_BASE_PASTAS_SQL, nome_pasta)
        if os.path.isdir(caminho_pasta):
            return caminho_pasta
        else:
            print(f"Erro: Pasta de scripts SQL '{caminho_pasta}' não encontrada.")
            return None
    except ValueError:
        print(f"Erro: Formato da data '{data_str}' é inválido. Use DDMMYYYY (ex: 12052025).")
        return None

# --- Lógica Principal ---
def main():
    print(f"--- Executor de Scripts SQL Gerados (Codificação Leitura: {CODIFICACAO_ARQUIVOS_SQL}) ---")

    data_pasta_input = input("Digite a data da pasta de scripts SQL (formato DDMMYYYY, ex: 12052025): ").strip()
    caminho_pasta_scripts_selecionada = encontrar_pasta_scripts_sql(data_pasta_input)

    if not caminho_pasta_scripts_selecionada:
        return

    conn = connect_db()
    if not conn:
        return

    scripts_executados_com_sucesso = []
    scripts_com_falha = []
    erros_execucao_detalhados = []

    print(f"\nLendo scripts da pasta: {caminho_pasta_scripts_selecionada}")
    print("Ordem de execução dos scripts (baseada nas tabelas):")
    # Gerar lista de nomes de arquivos SQL esperados na ordem
    arquivos_sql_para_executar = []
    map_tabela_para_arquivo = {}

    for nome_tabela_base in ORDEM_PROCESSAMENTO_TABELAS:
        nome_arquivo_sql = f"insert_{nome_tabela_base.lower()}.sql"
        caminho_completo = os.path.join(caminho_pasta_scripts_selecionada, nome_arquivo_sql)
        map_tabela_para_arquivo[nome_tabela_base.lower()] = nome_arquivo_sql # Para referência
        if os.path.exists(caminho_completo):
            arquivos_sql_para_executar.append(caminho_completo)
        # else:
            # print(f"  Aviso: Script SQL '{nome_arquivo_sql}' esperado (para tabela '{nome_tabela_base}') não encontrado.")

    # Adicionar scripts encontrados na pasta que não estavam na ordem (serão executados por último)
    scripts_encontrados_na_pasta = set()
    for item in os.listdir(caminho_pasta_scripts_selecionada):
        if item.lower().startswith("insert_") and item.lower().endswith(".sql"):
            scripts_encontrados_na_pasta.add(os.path.join(caminho_pasta_scripts_selecionada, item))
    
    scripts_ja_ordenados_set = set(arquivos_sql_para_executar)
    scripts_nao_ordenados = sorted(list(scripts_encontrados_na_pasta - scripts_ja_ordenados_set))

    if scripts_nao_ordenados:
        print("\nAviso: Scripts SQL encontrados na pasta sem ordem definida (serão executados ao final):")
        for script_path in scripts_nao_ordenados:
            print(f"- {os.path.basename(script_path)}")
        arquivos_sql_para_executar.extend(scripts_nao_ordenados)

    if not arquivos_sql_para_executar:
        print("Nenhum script SQL encontrado na pasta especificada para executar.")
        if conn: conn.close()
        return

    for i, script_path in enumerate(arquivos_sql_para_executar):
        print(f"{i+1}. {os.path.basename(script_path)}")
    print("-" * 40)


    with conn.cursor() as cursor:
        for script_filepath in arquivos_sql_para_executar:
            script_filename = os.path.basename(script_filepath)
            print(f"\nExecutando script: {script_filename}...")
            
            try:
                with open(script_filepath, 'r', encoding=CODIFICACAO_ARQUIVOS_SQL) as f_sql:
                    sql_content = f_sql.read()
                
                if not sql_content.strip() or "INSERT INTO" not in sql_content.upper():
                    print(f"INFO: Script '{script_filename}' está vazio ou não contém INSERTs. Pulando.")
                    # Considerar se isso deve ser um "sucesso" ou "ignorado"
                    # scripts_executados_com_sucesso.append(script_filename) # Opcional
                    continue

                cursor.execute(sql_content) # Executa todo o conteúdo do arquivo .sql
                conn.commit() # Commit após a execução bem-sucedida de cada arquivo
                print(f"SUCESSO: Script '{script_filename}' executado e commit realizado.")
                scripts_executados_com_sucesso.append(script_filename)

            except psycopg2.Error as db_err:
                conn.rollback() # Rollback se qualquer parte do script SQL falhar
                print(f"ERRO: Falha ao executar script '{script_filename}'. Rollback realizado.")
                # print(f"  Detalhe do erro: {str(db_err).strip()}")
                scripts_com_falha.append(script_filename)
                erros_execucao_detalhados.append({
                    'script': script_filename,
                    'erro': str(db_err).strip()
                })
            except FileNotFoundError:
                print(f"ERRO: Arquivo de script '{script_filename}' não encontrado no momento da execução (deveria existir). Pulando.")
                scripts_com_falha.append(script_filename) # Considerar como falha
                erros_execucao_detalhados.append({'script': script_filename, 'erro': 'Arquivo não encontrado.'})
            except UnicodeDecodeError as ude:
                print(f"ERRO: Falha de encoding ao ler script '{script_filename}' com {CODIFICACAO_ARQUIVOS_SQL}: {ude}")
                scripts_com_falha.append(script_filename)
                erros_execucao_detalhados.append({'script': script_filename, 'erro': f"Erro de encoding: {ude}"})
            except Exception as e:
                try: conn.rollback() # Tenta rollback em caso de erro inesperado
                except psycopg2.Error: pass # Conexão pode estar ruim
                print(f"ERRO INESPERADO ao processar script '{script_filename}': {e}")
                scripts_com_falha.append(script_filename)
                erros_execucao_detalhados.append({'script': script_filename, 'erro': str(e)})

    # --- Fim do processamento ---
    if conn:
        conn.close()
        print("\nConexão com o banco de dados fechada.")

    # --- Relatório Final ---
    print("\n--- Relatório Final da Execução dos Scripts SQL ---")
    if scripts_executados_com_sucesso:
        print("\nScripts SQL executados com SUCESSO:")
        for script_name in scripts_executados_com_sucesso:
            print(f"  - {script_name}")
    
    if scripts_com_falha:
        print("\nScripts SQL com FALHA (rollback realizado para estes):")
        for script_name in scripts_com_falha:
            print(f"  - {script_name}")
    
    if not scripts_executados_com_sucesso and not scripts_com_falha:
        print("\nNenhum script SQL foi efetivamente tentado ou processado.")

    if erros_execucao_detalhados:
        print(f"\nTotal de {len(erros_execucao_detalhados)} erros detalhados durante a execução dos scripts:")
        log_erros_path = f"log_erros_execucao_sql_{data_pasta_input}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_erros_path, 'w', encoding='utf-8') as f_log:
            f_log.write(f"Log de Erros na Execução de Scripts SQL - Pasta: insert_{data_pasta_input} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for i, erro_info in enumerate(erros_execucao_detalhados):
                log_msg = (f"{i+1}. Script: {erro_info.get('script', 'N/A')}\n"
                           f"   Erro: {erro_info.get('erro', 'N/A')}\n"
                           "-------------------------------------\n")
                f_log.write(log_msg)
        print(f"\nDetalhes dos erros foram salvos em: {log_erros_path}")
    else:
        if scripts_executados_com_sucesso or scripts_com_falha: # Se houve alguma tentativa
             print("\nNenhum erro detalhado registrado durante a execução dos scripts que tentaram rodar.")

    print("--- Fim da Execução ---")

if __name__ == '__main__':
    main()