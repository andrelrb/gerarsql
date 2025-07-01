# Versao do Arquivo v2.9.0 (Assume 'id' como BIGSERIAL no DB para tabelas de dados)
# Descrição: Gera arquivos insert.sql. NÃO inclui a coluna 'id' nos inserts,
#            pois se espera que ela seja BIGSERIAL no banco de dados.
#            Cada 'competencia' terá um único 'version_id' em tb_version.
#            ⚠️ REQUER que 'competencia' em 'tb_version' SEJA UNIQUE. ⚠️
#            ⚠️ REQUER que 'id' nas tabelas de dados SEJA BIGSERIAL. ⚠️
# Nome do arquivo: generate_insert_sql.py
import os
import csv
import datetime
import re
import sys

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("--------------------------------------------------------------------")
    print("ERRO CRÍTICO: A biblioteca 'psycopg2' não está instalada.")
    # ... (mensagem de erro completa)
    print("--------------------------------------------------------------------")
    psycopg2 = None
    # sys.exit(1)

# --- Configurações --- (Mantidas como na v2.8.4)

CAMINHO_PASTA_DADOS = os.environ.get('SIGTAP_CAMINHO_PASTA_DADOS', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202501_v2501172128')
#CAMINHO_PASTA_DADOS = os.environ.get('SIGTAP_CAMINHO_PASTA_DADOS', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202502_v2502131336')
#CAMINHO_PASTA_DADOS = os.environ.get('SIGTAP_CAMINHO_PASTA_DADOS', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202503_v2503101901')
#CAMINHO_PASTA_DADOS = os.environ.get('SIGTAP_CAMINHO_PASTA_DADOS', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202504_v2504031832')
#CAMINHO_PASTA_DADOS = os.environ.get('SIGTAP_CAMINHO_PASTA_DADOS', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202505_v2505061938')
CAMINHO_BASE_SAIDA_SQL = os.environ.get('SIGTAP_CAMINHO_BASE_SAIDA_SQL', r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\GerarSQL_v2')
SUFIXO_LAYOUT = '_layout.txt'
COLUNA_VERSION_FK = 'version_id'
CODIFICACAO_ARQUIVOS_DADOS = 'latin-1'
ARQUIVOS_RECONSTRUIR_LINHA = ['tb_componente_rede.txt']
ORDEM_PROCESSAMENTO_TABELAS = [ # Ajuste esta lista conforme necessário
    'tb_detalhe', 'tb_ocupacao', 'tb_financiamento', 'tb_habilitacao',
    'tb_tipo_leito', 'tb_grupo', 'tb_registro', 'tb_rede_atencao',
    'tb_renases', 'tb_regra_condicionada', 'tb_rubrica',
    'tb_cid', 'tb_modalidade', 'tb_grupo_habilitacao', 'tb_servico', 'tb_tuss',
    'tb_sub_grupo', 'tb_componente_rede', 'tb_servico_classificacao',
    'tb_descricao_detalhe', 'tb_forma_organizacao', 'tb_procedimento',
    'tb_descricao', 'rl_procedimento_sia_sih', 'tb_sia_sih',
    'rl_procedimento_habilitacao', 'rl_procedimento_renases',
    'rl_procedimento_tuss', 'rl_procedimento_comp_rede',
    'rl_procedimento_cid', 'rl_procedimento_modalidade', 'rl_procedimento_ocupacao',
    'rl_procedimento_servico', 'rl_procedimento_leito', 'rl_procedimento_detalhe',
    'rl_excecao_compatibilidade', 'rl_procedimento_registro',
    'rl_procedimento_compativel', 'rl_procedimento_regra_cond',
    'rl_procedimento_origem', 'rl_procedimento_incremento'
]
DB_CONFIG = {
    'host': os.environ.get('DB_HOST_SIGTAP', 'localhost'),
    'port': os.environ.get('DB_PORT_SIGTAP', '5432'),
    'dbname': os.environ.get('DB_NAME_SIGTAP', 'sigtap'),
    'user': os.environ.get('DB_USER_SIGTAP', 'postgres'),
    'password': os.environ.get('DB_PASSWORD_SIGTAP', 'root')
}

# (Função extrair_competencia e get_or_create_version_id permanecem idênticas à v2.8.4)
def extrair_competencia(caminho_pasta_dados):
    nome_base_pasta = os.path.basename(caminho_pasta_dados)
    match = re.search(r'_(\d{6})_v', nome_base_pasta)
    if match: return match.group(1)
    else:
        print(f"AVISO: Não foi possível extrair competência de '{nome_base_pasta}'. Digite (AAAAMM):")
        val = input(); return val if re.fullmatch(r'\d{6}', val) else "000000"

def get_or_create_version_id(db_params, competencia_ano_mes):
    if not psycopg2: return None
    conn = None; version_id = None; cursor = None
    try:
        print(f"Conectando a '{db_params['dbname']}' em '{db_params['host']}'...")
        conn_params_with_encoding = db_params.copy()
        conn_params_with_encoding['client_encoding'] = 'utf8' 
        conn = psycopg2.connect(**conn_params_with_encoding)
        cursor = conn.cursor(cursor_factory=RealDictCursor); print("Conexão bem-sucedida.")
        print(f"Verificando version_id para competência: {competencia_ano_mes}...")
        cursor.execute(sql.SQL("SELECT id FROM public.tb_version WHERE competencia = %s"), [competencia_ano_mes])
        result = cursor.fetchone()
        if result:
            version_id = result['id']
            print(f"  Competência {competencia_ano_mes} já existe. Usando version_id existente: {version_id}")
        else:
            print(f"  Competência {competencia_ano_mes} não encontrada. Criando novo registro...")
            cursor.execute(sql.SQL("INSERT INTO public.tb_version (competencia) VALUES (%s) RETURNING id"), [competencia_ano_mes])
            new_version_result = cursor.fetchone()
            if new_version_result and 'id' in new_version_result:
                version_id = new_version_result['id']; conn.commit()
                print(f"  Novo registro criado para competência {competencia_ano_mes} com version_id: {version_id}")
            else: print(f"  ERRO: Falha ao obter ID da nova versão."); conn.rollback()
    except psycopg2.OperationalError as op_err: print(f"  ERRO DE CONEXÃO: {op_err}")
    except psycopg2.Error as e:
        error_message = str(e)
        # (Lógica de formatação de erro psycopg2 mantida)
        try:
            if hasattr(e, 'diag') and e.diag and hasattr(e.diag, 'message_primary'):
                 error_message = f"{e.diag.message_primary} (Detalhe: {e.diag.message_detail}, SQLSTATE: {e.pgcode})"
            elif hasattr(e, 'pgerror') and e.pgerror: 
                if isinstance(e.pgerror, bytes): error_message = f"Erro DB (bytes): {e.pgerror.decode('latin1', errors='replace')} (CODE: {e.pgcode})"
                else: error_message = f"Erro DB: {e.pgerror} (CODE: {e.pgcode})"
        except: pass
        print(f"  ERRO DE BANCO (psycopg2.Error): {error_message}");
        if conn: conn.rollback()
    except UnicodeDecodeError as ude: print(f"  ERRO DE DECODIFICAÇÃO UNICODE: {ude}\n    INFORME: SHOW SERVER_ENCODING; e SELECT datname, pg_encoding_to_char(encoding) FROM pg_database WHERE datname = '{db_params['dbname']}';");
    except Exception as e_gen: print(f"  ERRO INESPERADO: {type(e_gen).__name__} - {e_gen}");
    finally:
        if cursor: cursor.close()
        if conn: conn.close(); print("Conexão com o banco fechada." if version_id else "")
    return version_id

def parse_layout(layout_filepath):
    colunas_layout = []
    try:
        with open(layout_filepath, 'r', encoding=CODIFICACAO_ARQUIVOS_DADOS) as f_layout:
            reader_layout = csv.reader(f_layout); next(reader_layout) 
            for i, row_layout in enumerate(reader_layout):
                if len(row_layout) >= 5: 
                    nome_coluna = row_layout[0].strip().lower().replace(' ', '_').replace('-', '_')
                    try:
                        inicio = int(row_layout[2]) - 1; fim = int(row_layout[3])
                        colunas_layout.append({'nome': nome_coluna, 'inicio': inicio, 'fim': fim, 'raw_name': row_layout[0].strip()})
                    except ValueError: print(f"Aviso: Pulando linha {i+2} no layout {os.path.basename(layout_filepath)} (erro conversão início/fim): {row_layout}")
                else: print(f"Aviso: Pulando linha {i+2} no layout {os.path.basename(layout_filepath)} (menos de 5 colunas): {row_layout}")
    except FileNotFoundError: print(f"Erro: Layout não encontrado: {layout_filepath}"); return None
    except Exception as e: print(f"Erro ao parsear layout {layout_filepath}: {e}"); return None
    return colunas_layout

def gerar_sql_para_arquivo_dados(data_filepath, layout_filepath, caminho_saida_sql, tabela_nome_base, actual_version_id):
    colunas_layout = parse_layout(layout_filepath)
    if not colunas_layout:
        print(f"Não foi possível processar o layout {layout_filepath} para {data_filepath}. Arquivo pulado.")
        return False

    nome_arquivo_sem_ext = os.path.splitext(os.path.basename(data_filepath))[0]
    nome_arquivo_sql = f"{nome_arquivo_sem_ext}_insert.sql"
    caminho_completo_sql = os.path.join(caminho_saida_sql, nome_arquivo_sql)

    # MODIFICAÇÃO AQUI: NÃO inclui 'id'. Apenas colunas do layout e version_id.
    # Assume-se que 'id' é BIGSERIAL no banco de dados e será auto-preenchido.
    # As tabelas de relacionamento puras podem precisar de tratamento especial se suas colunas FK formam a PK
    # e não possuem um 'id' próprio. Se elas tiverem 'id' BIGSERIAL, esta lógica está OK.
    # Se a tabela for de relacionamento e NÃO tiver 'id' (PK = FK1, FK2, version_id),
    # então esta lógica pode precisar de ajuste para essas tabelas específicas.
    # Por ora, esta lógica é para tabelas de dados que TÊM um 'id' BIGSERIAL.
    
    # Verifica se é uma tabela de relacionamento que não tem 'id' próprio (PK composta apenas de FKs)
    # A lista TABELAS_RELACIONAMENTO_SEM_ID_PROPRIO foi definida no generate_sigtap_sql.py
    # Precisaríamos de uma lista similar aqui, ou uma forma de inferir.
    # Por simplicidade, vamos assumir que todas as tabelas processadas aqui TÊM um 'id' auto-gerado
    # ou que as de relacionamento são tratadas de forma que o INSERT não precise de 'id'.
    # Esta versão do script omite 'id' do INSERT, esperando que o DB o gere.

    colunas_para_insert_lista = [col['nome'] for col in colunas_layout] + [COLUNA_VERSION_FK]
    colunas_sql_str = ", ".join([f'"{col_nome}"' for col_nome in colunas_para_insert_lista])
    table_name_for_sql = f"public.\"{tabela_nome_base}\""

    try:
        with open(data_filepath, 'r', encoding=CODIFICACAO_ARQUIVOS_DADOS) as f_dados, \
             open(caminho_completo_sql, 'w', encoding='utf-8') as f_sql:
            
            print(f"Processando dados de: {os.path.basename(data_filepath)} -> Gerando: {nome_arquivo_sql}")
            f_sql.write(f"-- INSERTS para a tabela {table_name_for_sql} com version_id = {actual_version_id}\n")
            f_sql.write(f"-- Coluna 'id' deve ser BIGSERIAL e será auto-preenchida pelo banco.\n")
            f_sql.write(f"-- Arquivo de origem: {os.path.basename(data_filepath)}\n\n")

            linhas_inseridas = 0
            for num_linha, linha_raw in enumerate(f_dados, 1):
                linha = linha_raw.rstrip('\n')

                if os.path.basename(data_filepath) in ARQUIVOS_RECONSTRUIR_LINHA:
                    if len(linha) < 206 and nome_arquivo_sem_ext == "tb_componente_rede":
                        try: linha += next(f_dados).rstrip('\n')
                        except StopIteration: pass

                # MODIFICAÇÃO AQUI: NÃO adiciona valor para 'id'.
                valores_linha_para_sql = []
                for col_info in colunas_layout:
                    valor_raw = linha[col_info['inicio']:col_info['fim']].strip()
                    if valor_raw == '': valores_linha_para_sql.append("NULL")
                    else: valores_linha_para_sql.append(f"'{valor_raw.replace("'", "''")}'")
                
                valores_linha_para_sql.append(str(actual_version_id)) # Valor para version_id
                
                valores_sql_str = ", ".join(valores_linha_para_sql)
                f_sql.write(f"INSERT INTO {table_name_for_sql} ({colunas_sql_str}) VALUES ({valores_sql_str});\n")
                linhas_inseridas += 1
            
            print(f"  {linhas_inseridas} linhas de INSERT geradas para {nome_arquivo_sql}.")
            return True

    except UnicodeDecodeError as ude:
        print(f"Erro de Encoding ao processar {os.path.basename(data_filepath)}: {ude}.")
        with open(caminho_completo_sql.replace(".sql", ".err.txt"), "w", encoding='utf-8') as f_err:
            f_err.write(f"Erro: {ude}\n")
        return False
    except Exception as e:
        print(f"Erro ao gerar SQL para {os.path.basename(data_filepath)}: {e}")
        import traceback; traceback.print_exc()
        return False

def main():
    if psycopg2 is None: sys.exit(1)

    print(f"--- Iniciando Geração de Scripts SQL de INSERT (v2.9.0) ---")
    print("--- Esta versão assume que a coluna 'id' nas tabelas de dados é BIGSERIAL no DB. ---")
    print("--- 'competencia' em 'tb_version' DEVE ter RESTRIÇÃO UNIQUE. ---")
    
    print(f"Usando CAMINHO_PASTA_DADOS: {CAMINHO_PASTA_DADOS}")
    print(f"Usando CAMINHO_BASE_SAIDA_SQL: {CAMINHO_BASE_SAIDA_SQL}")
    
    if not os.path.isdir(CAMINHO_PASTA_DADOS): print(f"ERRO CRÍTICO: CAMINHO_PASTA_DADOS '{CAMINHO_PASTA_DADOS}' não encontrado."); sys.exit(1)
    if not os.path.isdir(CAMINHO_BASE_SAIDA_SQL): print(f"ERRO CRÍTICO: CAMINHO_BASE_SAIDA_SQL '{CAMINHO_BASE_SAIDA_SQL}' não encontrado."); sys.exit(1)
        
    competencia_atual = extrair_competencia(CAMINHO_PASTA_DADOS)

    if competencia_atual == "000000":
        if not input("Competência '000000'. Continuar? (s/N): ").lower() == 's': print("Geração abortada."); return
    print(f"Competência para esta execução: {competencia_atual}")

    actual_version_id = get_or_create_version_id(DB_CONFIG, competencia_atual)

    if actual_version_id is None:
        print("--------------------------------------------------------------------")
        print("ERRO CRÍTICO: Não foi possível obter/criar 'version_id' do DB.")
        # ... (mensagem de erro completa)
        print("--------------------------------------------------------------------")
        return
    
    print(f"--- VERSION_ID OBTIDO/CRIADO: {actual_version_id} (para competência ÚNICA '{competencia_atual}') ---")

    data_hoje_str = datetime.date.today().strftime('%Y%m%d')
    nome_pasta_saida_customizado = f"insert_{data_hoje_str}_versaoID_{actual_version_id}_competencia_{competencia_atual}"
    caminho_pasta_saida_final = os.path.join(CAMINHO_BASE_SAIDA_SQL, nome_pasta_saida_customizado)
    
    if not os.path.exists(caminho_pasta_saida_final):
        try: os.makedirs(caminho_pasta_saida_final); print(f"Pasta de saída criada: {caminho_pasta_saida_final}")
        except OSError as e: print(f"Erro ao criar pasta de saída {caminho_pasta_saida_final}: {e}."); return
    else: print(f"Pasta de saída já existe: {caminho_pasta_saida_final}")

    processed_files_count = 0; tabelas_com_erro = []
    for nome_tabela_base in ORDEM_PROCESSAMENTO_TABELAS: 
        data_filename = f"{nome_tabela_base}.txt"; layout_filename = f"{nome_tabela_base}{SUFIXO_LAYOUT}"
        data_filepath = os.path.join(CAMINHO_PASTA_DADOS, data_filename)
        layout_filepath = os.path.join(CAMINHO_PASTA_DADOS, layout_filename)
        if not os.path.exists(data_filepath): continue
        if not os.path.exists(layout_filepath):
            if os.path.exists(data_filepath): 
                 print(f"  AVISO: Layout {layout_filename} não encontrado para dados {data_filename}. Pulando.")
                 tabelas_com_erro.append(f"{nome_tabela_base} (Layout Ausente p/ Dados)")
            continue
        
        sucesso = gerar_sql_para_arquivo_dados(
            data_filepath, layout_filepath, caminho_pasta_saida_final, 
            nome_tabela_base, actual_version_id 
        )
        if sucesso: processed_files_count += 1
        else:
            if not any(nome_tabela_base in erro for erro in tabelas_com_erro):
                 tabelas_com_erro.append(f"{nome_tabela_base} (Erro Geração SQL/Dados)")

    print(f"\n--- Geração de scripts SQL finalizada. ---")
    print(f"Competência: {competencia_atual}, Version_id usado: {actual_version_id}")
    print(f"Arquivos processados com sucesso: {processed_files_count}.")
    
    if caminho_pasta_saida_final and processed_files_count > 0 : print(f"Verifique os arquivos SQL em: {caminho_pasta_saida_final}")
    elif processed_files_count == 0 and os.path.exists(CAMINHO_PASTA_DADOS) and any(f.endswith(".txt") and not f.endswith(SUFIXO_LAYOUT) for f in os.listdir(CAMINHO_PASTA_DADOS)):
        print("Nenhum arquivo de dados processado com sucesso, apesar de existirem arquivos .txt na pasta de dados.")
        
    if tabelas_com_erro:
        print("\nTabelas com erros/avisos no processamento:")
        for tabela_info in sorted(list(set(tabelas_com_erro))): print(f"  - {tabela_info}")
    print("----------------------------------------------------")

if __name__ == '__main__':
    main()