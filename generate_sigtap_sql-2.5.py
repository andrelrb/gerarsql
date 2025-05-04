
# Versao do Arquivo: v2.5 - Integração de Comentários de Colunas via Excel
# Descrição: Gerar o script para criação do banco de dados {Versão Instavel}
# Nome do arquivo: generate_sigtap_sql.py
import os
import csv
import datetime
import pandas as pd # Adicionado para leitura do Excel

# --- Configurações ---
CAMINHO_PASTA_LAYOUTS = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202504_v2504031832'
CAMINHO_SAIDA_SQL = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\GerarSQL\createDB'
NOME_ARQUIVO_SAIDA_SCHEMA = 'create_sigtap_tables_schema_v2_5.sql' # Versão atualizada

SUFIXO_LAYOUT = '_layout.txt'
TABELA_VERSION = 'tb_version'
COLUNA_VERSION_FK = 'version_id'
CODIFICACAO_LAYOUT = 'latin-1'


# --- Configurações para Descrições do Excel ---
# ATENÇÃO: Ajuste os valores abaixo conforme a estrutura do seu arquivo Excel!
CAMINHO_ARQUIVO_DESCRICOES_EXCEL = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202504_v2504031832\DATASUS - Tabela de Procedimentos - Lay-out.xls'
                                     
# Nome da planilha/aba no arquivo Excel que contém as descrições das colunas.
NOME_PLANILHA_DESCRICOES = 'Layout dos Arquivos' # << AJUSTE SE NECESSÁRIO (Ex: 'Lay-out', 'Descrições')
# Nome da coluna na planilha Excel que contém o nome da TABELA (deve corresponder ao nome base do arquivo de layout, ex: 'tb_procedimento').
COLUNA_EXCEL_NOME_TABELA = 'Tabela'        # << AJUSTE SE NECESSÁRIO
# Nome da coluna na planilha Excel que contém o NOME ORIGINAL DO CAMPO (como no arquivo _layout.txt, ex: 'CO_PROCEDIMENTO').
COLUNA_EXCEL_NOME_CAMPO_LAYOUT = 'Campo'   # << AJUSTE SE NECESSÁRIO
# Nome da coluna na planilha Excel que contém a DESCRIÇÃO do campo.
COLUNA_EXCEL_DESCRICAO = 'Descrição'      # << AJUSTE SE NECESSÁRIO
# ----------------------------------------------------------------------------------

# DICIONÁRIO DE CONTROLE DE UNICIDADE COMPOSTA (coluna_co, version_id)
# (Mantido como na versão anterior)
COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION = {
    'tb_procedimento': 'co_procedimento',
    'tb_grupo': 'co_grupo',
    'tb_cid': 'co_cid',
    'tb_ocupacao': 'co_ocupacao',
    'tb_servico': 'co_servico',
    'tb_financiamento': 'co_financiamento',
    'tb_rubrica': 'co_rubrica',
    'tb_detalhe': 'co_detalhe',
    'tb_habilitacao': 'co_habilitacao',
    'tb_rede_atencao': 'co_rede_atencao',
    'tb_componente_rede': 'co_componente_rede',
    'tb_registro': 'co_registro',
    'tb_tipo_leito': 'co_tipo_leito',
    'tb_regra_condicionada': 'co_regra_condicionada',
    'tb_tuss': 'co_tuss',
}

UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION = {
    'tb_servico_classificacao': ['co_servico', 'co_classificacao']
}

sql_tb_version = f"""
-- Script SQL gerado para o banco SIGTAP (Schema v2.5 - Comentários via Excel)
-- Data de geração: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CREATE TABLE IF NOT EXISTS public."{TABELA_VERSION}" (
    id BIGSERIAL PRIMARY KEY,
    competencia VARCHAR(6) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE public."{TABELA_VERSION}" IS 'Tabela para versionamento das competências dos dados do SIGTAP.';
COMMENT ON COLUMN public."{TABELA_VERSION}".id IS 'Identificador sequencial único da versão (competência).';
COMMENT ON COLUMN public."{TABELA_VERSION}".competencia IS 'Competência no formato AAAAMM (ex: 202401).';
COMMENT ON COLUMN public."{TABELA_VERSION}".created_at IS 'Timestamp da criação do registro da versão.';
"""

def load_column_descriptions(excel_filepath, sheet_name, col_tabela_excel, col_campo_excel, col_descricao_excel):
    """
    Carrega as descrições das colunas de um arquivo Excel.
    Retorna um dicionário no formato: {'nome_tabela_normalizado': {'nome_campo_raw': 'descricao'}}
    """
    descriptions_map = {}
    try:
        df = pd.read_excel(excel_filepath, sheet_name=sheet_name, dtype=str) # Ler tudo como string inicialmente

        required_excel_cols = {col_tabela_excel, col_campo_excel, col_descricao_excel}
        if not required_excel_cols.issubset(df.columns):
            missing = required_excel_cols - set(df.columns)
            print(f"Erro: Planilha '{sheet_name}' no arquivo Excel '{excel_filepath}' não contém todas as colunas necessárias. Faltando: {missing}. Colunas encontradas: {list(df.columns)}")
            return {}

        for index, row in df.iterrows():
            table_name_excel_raw = row[col_tabela_excel]
            column_name_raw_excel = row[col_campo_excel]
            description = row[col_descricao_excel]

            if pd.isna(table_name_excel_raw) or pd.isna(column_name_raw_excel) or pd.isna(description):
                continue

            # Normaliza o nome da tabela (minúsculas, remove sufixos comuns se necessário)
            # Ex: "TB_PROCEDIMENTO" -> "tb_procedimento"
            table_name_normalized = str(table_name_excel_raw).strip().lower()
            # Se os nomes das tabelas no Excel tiverem sufixos como "_layout", remova-os para corresponder
            # à forma como os nomes das tabelas são gerados a partir dos nomes dos arquivos de layout.
            # Exemplo: table_name_normalized = table_name_normalized.replace('_layout', '')

            column_name_key = str(column_name_raw_excel).strip() # Este deve ser o nome original do campo, ex: 'CO_PROCEDIMENTO'
            desc_text = str(description).strip()

            if not table_name_normalized or not column_name_key or not desc_text:
                continue

            if table_name_normalized not in descriptions_map:
                descriptions_map[table_name_normalized] = {}
            descriptions_map[table_name_normalized][column_name_key] = desc_text
            
        print(f"Descrições carregadas para {len(descriptions_map)} tabelas do arquivo Excel: '{excel_filepath}'.")
    except FileNotFoundError:
        print(f"Erro: Arquivo Excel de descrições não encontrado: '{excel_filepath}'")
    except ValueError as ve: # Trata o caso de planilha não encontrada pelo pandas
        if "No sheet named" in str(ve) or "Worksheet named" in str(ve): # Mensagens comuns de erro do pandas/openpyxl
             print(f"Erro: Planilha '{sheet_name}' não encontrada no arquivo Excel '{excel_filepath}'. Verifique NOME_PLANILHA_DESCRICOES.")
        else:
            print(f"Erro de valor ao ler o Excel '{excel_filepath}', planilha '{sheet_name}': {ve}")
    except Exception as e:
        print(f"Erro inesperado ao carregar descrições do Excel '{excel_filepath}', planilha '{sheet_name}': {e}")
    return descriptions_map

def parse_layout_metadata(layout_filepath, all_descriptions_excel):
    """
    Analisa um arquivo de layout e extrai definições de colunas, incluindo suas descrições do Excel.
    'all_descriptions_excel' é o mapa carregado pela função load_column_descriptions.
    Retorna (nome_da_tabela, lista_de_definicoes_de_coluna)
    Cada definição de coluna é um dict: {'name', 'type', 'raw_name', 'description'}
    """
    column_definitions = []
    table_name_from_layout = None
    try:
        filename = os.path.basename(layout_filepath)
        # Gera o nome da tabela a partir do nome do arquivo de layout (ex: "tb_procedimento_layout.txt" -> "tb_procedimento")
        table_name_from_layout = filename.replace(SUFIXO_LAYOUT, '').lower()
        if not table_name_from_layout:
            return None, None

        # Obtém as descrições específicas para esta tabela, se existirem
        current_table_column_descriptions = all_descriptions_excel.get(table_name_from_layout, {})

        with open(layout_filepath, 'r', encoding=CODIFICACAO_LAYOUT) as f:
            reader = csv.reader(f)
            try:
                header_line = next(reader)
            except StopIteration:
                return table_name_from_layout, [] # Arquivo vazio após cabeçalho

            header = [h.strip().lower() for h in header_line]
            header_map = {h: i for i, h in enumerate(header)}
            required_cols = ['coluna', 'tamanho', 'inicio', 'fim', 'tipo']
            missing_cols = [rc for rc in required_cols if rc not in header_map]
            if missing_cols:
                print(f"Erro: Layout '{filename}' não possui as colunas obrigatórias: {', '.join(missing_cols)}. Cabeçalho encontrado: {header}")
                return table_name_from_layout, None # Indica falha no parse

            for i, row in enumerate(reader):
                if not row or not any(field.strip() for field in row) or len(row) < len(required_cols):
                    continue
                try:
                    col_name_raw = row[header_map['coluna']].strip() # Nome original da coluna, ex: 'CO_PROCEDIMENTO'
                    col_name_normalized = col_name_raw.lower().replace(' ', '_').replace('-', '_')
                    tam_str = row[header_map['tamanho']].strip()
                    col_type_raw = row[header_map['tipo']].strip().upper()

                    if not col_name_normalized:
                        continue

                    # Busca a descrição no mapa carregado do Excel usando o nome original da coluna (col_name_raw)
                    description = current_table_column_descriptions.get(col_name_raw)

                    tam = int(tam_str) if tam_str.isdigit() else 0
                    
                    # Mapeamento de tipos (mantido da versão anterior)
                    if col_type_raw == 'VARCHAR2': col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT'
                    elif col_type_raw == 'CHAR': col_type = f'CHAR({tam})' if tam > 0 else 'CHAR(1)'
                    elif col_type_raw.startswith('NUMBER'): col_type = 'NUMERIC'
                    elif col_type_raw == 'DATE' : col_type = 'DATE'
                    elif col_type_raw == 'ALFA' : col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT'
                    elif col_type_raw == 'NUM' :
                        if tam > 18: col_type = 'NUMERIC' # Para números muito grandes, NUMERIC é mais seguro
                        elif tam > 9: col_type = 'BIGINT'
                        elif tam > 4: col_type = 'INTEGER'
                        elif tam > 0: col_type = 'SMALLINT'
                        else: col_type = 'NUMERIC' # Caso de tamanho 0 ou não especificado para NUM
                    else: col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT' # Padrão

                    column_definitions.append({
                        'name': col_name_normalized,
                        'type': col_type,
                        'raw_name': col_name_raw, # Mantém o nome original para referência (e lookup de descrição)
                        'description': description # Adiciona a descrição
                    })
                except (IndexError, ValueError) as e:
                    print(f"Aviso: Pulando linha (erro de índice/valor) no layout '{filename}', linha {i+2}: {row} - Erro: {e}")
                except KeyError as e:
                    print(f"Aviso: Pulando linha (KeyError: {e}, coluna de cabeçalho ausente?) no layout '{filename}', linha {i+2}: {row}")
        return table_name_from_layout, column_definitions
    except UnicodeDecodeError as ude:
        print(f"Erro de encoding ao ler layout '{layout_filepath}' com '{CODIFICACAO_LAYOUT}': {ude}")
        return None, None
    except FileNotFoundError:
        print(f"Erro: Arquivo de layout não encontrado: '{layout_filepath}'")
        return None, None
    except Exception as e:
        print(f"Erro inesperado ao ler/parsear o arquivo de layout '{layout_filepath}': {e}")
        return None, None

def main():
    print(f"--- Gerador de Scripts SQL CREATE TABLE (Schema v2.5 - Comentários via Excel) ---")
    
    # Carrega as descrições do arquivo Excel uma vez
    all_excel_descriptions = load_column_descriptions(
        CAMINHO_ARQUIVO_DESCRICOES_EXCEL,
        NOME_PLANILHA_DESCRICOES,
        COLUNA_EXCEL_NOME_TABELA,
        COLUNA_EXCEL_NOME_CAMPO_LAYOUT,
        COLUNA_EXCEL_DESCRICAO
    )
    if not all_excel_descriptions:
        print("Aviso: Nenhuma descrição foi carregada do Excel. Os comentários de coluna não serão gerados a partir dele.")

    all_sql_scripts = [sql_tb_version]
    table_metadata = {}

    try:
        if not os.path.isdir(CAMINHO_PASTA_LAYOUTS):
            print(f"Erro: Pasta de layouts não encontrada: {CAMINHO_PASTA_LAYOUTS}"); return
        print(f"Lendo layouts de: {CAMINHO_PASTA_LAYOUTS}")
        layout_files = sorted([f for f in os.listdir(CAMINHO_PASTA_LAYOUTS) if f.lower().endswith(SUFIXO_LAYOUT.lower())])
        if not layout_files: print("Nenhum arquivo de layout (*_layout.txt) encontrado."); return

        parsed_layouts = {}
        for filename in layout_files:
            filepath = os.path.join(CAMINHO_PASTA_LAYOUTS, filename)
            # Passa o dicionário de descrições para a função de parsing
            table_name, raw_col_defs = parse_layout_metadata(filepath, all_excel_descriptions)
            
            if table_name and raw_col_defs is not None:
                if raw_col_defs: # Verifica se a lista de colunas não está vazia
                    parsed_layouts[table_name] = raw_col_defs
                # Se raw_col_defs for uma lista vazia (arquivo de layout sem colunas válidas, mas parseado),
                # ainda pode ser útil manter table_name para ordenação, mas não gerará CREATE TABLE.
                # No entanto, a lógica atual já lida com isso.
            elif table_name and raw_col_defs is None: # Erro durante o parse do layout
                print(f"Aviso: Definições para a tabela '{table_name}' (arquivo '{filename}') não puderam ser completamente parseadas. Tabela possivelmente pulada.")
        
        # Lógica de ordenação de tabelas (mantida)
        ordem_para_criar_final = []
        if 'ORDEM_PROCESSAMENTO_TABELAS_BASE' in globals() and isinstance(ORDEM_PROCESSAMENTO_TABELAS_BASE, list):
            referencia_ordem = [tbl.lower() for tbl in ORDEM_PROCESSAMENTO_TABELAS_BASE]
            for tbl_base_name in referencia_ordem:
                if tbl_base_name in parsed_layouts and tbl_base_name not in ordem_para_criar_final:
                    ordem_para_criar_final.append(tbl_base_name)
        for tbl_base_name in parsed_layouts: # Adiciona tabelas restantes
            if tbl_base_name not in ordem_para_criar_final:
                ordem_para_criar_final.append(tbl_base_name)

        for table_name in ordem_para_criar_final:
            if table_name not in parsed_layouts or not parsed_layouts[table_name]:
                print(f"Aviso: Pulando geração de CREATE TABLE para '{table_name}' pois não possui definições de coluna válidas.")
                continue
            
            raw_col_defs = parsed_layouts[table_name] # Contém {'name', 'type', 'raw_name', 'description'}
            column_sql_lines = [f"    id BIGINT NOT NULL", f"    \"{COLUNA_VERSION_FK}\" BIGINT NOT NULL"]
            unique_constraints_definitions = []
            current_table_all_col_names = ['id', COLUNA_VERSION_FK] # Nomes normalizados

            for col_def in raw_col_defs:
                col_name = col_def['name'] # Nome normalizado para SQL
                col_type = col_def['type']
                if col_name.lower() in ['id', COLUNA_VERSION_FK.lower()]: continue # Já adicionados
                
                line = f"    \"{col_name}\" {col_type}"
                column_sql_lines.append(line)
                current_table_all_col_names.append(col_name)

            # Lógica de UNIQUE constraints (mantida)
            if table_name in COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION:
                col_co_principal = COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION[table_name]
                if col_co_principal and col_co_principal in current_table_all_col_names:
                    unique_constraints_definitions.append( (col_co_principal, COLUNA_VERSION_FK) )
            
            if table_name in UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION:
                cols_para_unique_especial = UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION[table_name]
                if all(c in current_table_all_col_names for c in cols_para_unique_especial):
                    unique_constraints_definitions.append( tuple(list(cols_para_unique_especial) + [COLUNA_VERSION_FK]) )
            
            column_sql_lines.append(f"    PRIMARY KEY (id, \"{COLUNA_VERSION_FK}\")")
            
            for i, uk_cols_tuple in enumerate(unique_constraints_definitions):
                uk_cols_quoted = [f'"{c}"' for c in uk_cols_tuple]
                constraint_name_suffix = "_".join(c.replace('co_','').replace('rl_','').replace('tb_','') for c in uk_cols_tuple if c != COLUNA_VERSION_FK)
                column_sql_lines.append(f"    CONSTRAINT uq_{table_name}_{constraint_name_suffix}_{i} UNIQUE ({', '.join(uk_cols_quoted)})")

            column_sql_lines.append(f"    CONSTRAINT fk_{table_name}_{COLUNA_VERSION_FK} FOREIGN KEY (\"{COLUNA_VERSION_FK}\") REFERENCES public.\"{TABELA_VERSION}\" (id)")

            column_definitions_string = ",\n".join(column_sql_lines)
            sql_script_create_table = f"""\n-- Criação da tabela "public.{table_name}"
CREATE TABLE IF NOT EXISTS public."{table_name}" (\n{column_definitions_string}\n);"""
            all_sql_scripts.append(sql_script_create_table)
            
            # --- GERAÇÃO DOS COMENTÁRIOS ---
            comment_sql_lines = []
            # Comentário para a tabela (se você tiver uma fonte para isso, ex: uma coluna "Descrição da Tabela" no Excel)
            # table_description = all_excel_descriptions.get(table_name, {}).get('_TABLE_DESCRIPTION_', None) # Chave especial
            # if table_description:
            #     escaped_table_desc = table_description.replace("'", "''")
            #     comment_sql_lines.append(f'COMMENT ON TABLE public."{table_name}" IS \'{escaped_table_desc}\';')

            # Comentários para colunas 'id' e 'version_id' (pode vir do Excel se mapeado ou ser genérico)
            id_desc = all_excel_descriptions.get(table_name, {}).get('id', # Tenta pegar 'id' do Excel
                                                                     'Identificador principal da linha, parte da chave primária composta com version_id.')
            version_id_desc = all_excel_descriptions.get(table_name, {}).get(COLUNA_VERSION_FK, # Tenta pegar 'version_id' do Excel
                                                                            f'Chave estrangeira para a tabela public."{TABELA_VERSION}", referenciando a competência dos dados.')
            
            if id_desc:
                 comment_sql_lines.append(f'COMMENT ON COLUMN public."{table_name}"."id" IS \'{id_desc.replace("'", "''")}\';')
            if version_id_desc:
                 comment_sql_lines.append(f'COMMENT ON COLUMN public."{table_name}"."{COLUNA_VERSION_FK}" IS \'{version_id_desc.replace("'", "''")}\';')

            for col_def in raw_col_defs:
                col_name_sql = col_def['name'] # Nome da coluna normalizado para SQL
                description = col_def.get('description') # Descrição vinda do Excel (via parse_layout_metadata)
                
                if col_name_sql.lower() in ['id', COLUNA_VERSION_FK.lower()]: # Já tratados acima
                    continue

                if description:
                    escaped_description = description.replace("'", "''") # Escapa aspas simples para SQL
                    comment_sql_lines.append(f'COMMENT ON COLUMN public."{table_name}"."{col_name_sql}" IS \'{escaped_description}\';')
            
            if comment_sql_lines:
                all_sql_scripts.append(f"\n-- Comentários para a tabela public.\"{table_name}\"")
                all_sql_scripts.extend(comment_sql_lines)
            # --- FIM DA GERAÇÃO DOS COMENTÁRIOS ---

            table_metadata[table_name] = {'cols': current_table_all_col_names, 'unique_keys': unique_constraints_definitions}
            print(f"Gerado CREATE TABLE e COMENTÁRIOS para: public.\"{table_name}\"")

        # Geração de FKs (ALTER TABLE) - mantida, mas referenciando tabelas com schema public.
        print("\nGerando restrições FOREIGN KEY (ALTER TABLE)...")
        fk_scripts_alter = []
        added_fks_signatures = set()
        for source_table_name, meta_source in table_metadata.items():
            source_col_names = meta_source['cols']
            for col_name_source in source_col_names:
                if col_name_source.startswith('co_') and col_name_source not in [COLUNA_VERSION_FK, 'id']:
                    potential_target_base = col_name_source.replace('co_', '', 1)
                    possible_target_names = [f"tb_{potential_target_base}", f"rl_{potential_target_base}"]
                    target_table_found = None
                    fk_target_columns_tuple = None

                    for pt_name in possible_target_names:
                        if pt_name in table_metadata and pt_name != source_table_name:
                            target_meta = table_metadata[pt_name]
                            # FK deve apontar para uma UNIQUE KEY composta com version_id na tabela alvo
                            
                            # Caso padrão: (col_name_source, version_id)
                            candidate_target_key = (col_name_source, COLUNA_VERSION_FK)
                            if candidate_target_key in target_meta['unique_keys']:
                                target_table_found = pt_name
                                fk_target_columns_tuple = candidate_target_key
                                break 
                            
                            # Caso especial: tb_servico_classificacao (co_servico, co_classificacao, version_id)
                            # Verifica se a coluna fonte é 'co_servico' e se 'co_classificacao' também existe na fonte
                            if pt_name == 'tb_servico_classificacao' and \
                               'co_servico' in source_col_names and 'co_classificacao' in source_col_names and \
                               col_name_source == 'co_servico': # A FK é baseada em co_servico
                                special_target_key = ('co_servico', 'co_classificacao', COLUNA_VERSION_FK)
                                if special_target_key in target_meta.get('unique_keys', []):
                                    target_table_found = pt_name
                                    fk_target_columns_tuple = special_target_key 
                                    # As colunas fonte para esta FK especial serão (co_servico, co_classificacao, version_id)
                                    break 
                    
                    if target_table_found and fk_target_columns_tuple:
                        # Determina as colunas da FK na tabela de origem
                        if len(fk_target_columns_tuple) == 3 and target_table_found == 'tb_servico_classificacao':
                             # Para o caso especial de tb_servico_classificacao
                            fk_source_columns_tuple = ('co_servico', 'co_classificacao', COLUNA_VERSION_FK)
                        else:
                            # Caso padrão
                            fk_source_columns_tuple = (col_name_source, COLUNA_VERSION_FK)

                        # Verifica se todas as colunas de origem realmente existem na tabela de origem
                        if not all(src_col in source_col_names for src_col in fk_source_columns_tuple):
                            # print(f"Aviso: Pulando FK de {source_table_name} para {target_table_found}. Colunas fonte {fk_source_columns_tuple} não encontradas completamente em {source_col_names}.")
                            continue
                        
                        fk_constraint_name = f"fk_{source_table_name}_{'_'.join(str(c) for c in fk_source_columns_tuple)}_comp"
                        # Normaliza a ordem das colunas para a assinatura, para evitar duplicatas se a ordem variar mas o conjunto for o mesmo
                        fk_signature = (source_table_name, tuple(sorted(fk_source_columns_tuple)), 
                                        target_table_found, tuple(sorted(fk_target_columns_tuple)))

                        if fk_signature not in added_fks_signatures:
                            fk_source_cols_quoted = [f'"{c}"' for c in fk_source_columns_tuple]
                            fk_target_cols_quoted = [f'"{c}"' for c in fk_target_columns_tuple]
                            
                            fk_sql = f"""\n-- FK de "public.{source_table_name}" para "public.{target_table_found}"
ALTER TABLE public."{source_table_name}" ADD CONSTRAINT "{fk_constraint_name}"
FOREIGN KEY ({', '.join(fk_source_cols_quoted)}) 
REFERENCES public."{target_table_found}" ({', '.join(fk_target_cols_quoted)});"""
                            
                            fk_scripts_alter.append(fk_sql)
                            added_fks_signatures.add(fk_signature)
                            print(f"  FK: public.\"{source_table_name}\"({', '.join(fk_source_columns_tuple)}) -> public.\"{target_table_found}\"({', '.join(fk_target_columns_tuple)})")
        all_sql_scripts.extend(fk_scripts_alter)

    except Exception as e:
        print(f"Erro inesperado durante a execução principal: {e}"); import traceback; traceback.print_exc()

    full_sql_output = "\n\n".join(all_sql_scripts)
    if not os.path.isdir(CAMINHO_SAIDA_SQL):
        try: os.makedirs(CAMINHO_SAIDA_SQL, exist_ok=True); print(f"Pasta de saída criada: {CAMINHO_SAIDA_SQL}")
        except OSError as e: print(f"Erro ao criar pasta de saída {CAMINHO_SAIDA_SQL}: {e}"); return
    
    final_output_path = os.path.join(CAMINHO_SAIDA_SQL, NOME_ARQUIVO_SAIDA_SCHEMA)
    try:
        with open(final_output_path, "w", encoding='utf-8') as f: f.write(full_sql_output)
        print(f"\nScript de schema SQL gerado em {final_output_path}")
        print(f"Total de tabelas (CREATE TABLE): {len(parsed_layouts) + 1 if parsed_layouts else 1}") # +1 para tb_version
        print(f"Total de FKs (ALTER TABLE): {len(fk_scripts_alter)}")
    except IOError as e: print(f"Erro ao salvar script SQL em {final_output_path}: {e}")

if __name__ == '__main__':
    main()