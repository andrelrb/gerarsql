# Versao do Arquivo: v2.4 - Controle Fino de UNIQUEs
# Descrição: Gerar o script para criação do banco de dados {Versão Instavel}
# Nome do arquivo: generate_sigtap_sql.py
import os
import csv
import datetime

# --- Configurações ---
CAMINHO_PASTA_LAYOUTS = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\TabelaUnificada_202504_v2504031832'
CAMINHO_SAIDA_SQL = r'G:\Meu Drive\Indra company\SECRETARIA DE SAUDE - RECIFE\CAPS\GerarSQL\createDB'
NOME_ARQUIVO_SAIDA_SCHEMA = 'create_sigtap_tables_schema_v2_4.sql' 

SUFIXO_LAYOUT = '_layout.txt'
TABELA_VERSION = 'tb_version'
COLUNA_VERSION_FK = 'version_id' 
CODIFICACAO_LAYOUT = 'latin-1' 

# ----------------------------------------------------------------------------------
# DICIONÁRIO DE CONTROLE DE UNICIDADE COMPOSTA (coluna_co, version_id)
# ----------------------------------------------------------------------------------
# Chave: nome da tabela (ex: 'tb_procedimento')
# Valor: nome da coluna 'co_' principal que, COMBINADA COM version_id, DEVE SER ÚNICA.
#        Se uma tabela não está aqui, ou seu valor é None/string vazia,
#        nenhuma UNIQUE(co_X, version_id) automática será criada para ela.
#
# REVISE ESTA LISTA CUIDADOSAMENTE COM BASE NAS SUAS REGRAS DE NEGÓCIO!
# Se (co_X, version_id) PODE SE REPETIR numa tabela, NÃO coloque a entrada aqui.
# Se for referenciada por uma FK composta, ela PRECISA estar aqui.
# ----------------------------------------------------------------------------------
COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION = {
    'tb_procedimento': 'co_procedimento', # Provavelmente essencial para FKs
    'tb_grupo': 'co_grupo',               # Provavelmente essencial para FKs
    'tb_cid': 'co_cid',                   # Provavelmente essencial para FKs
    'tb_ocupacao': 'co_ocupacao',         # Provavelmente essencial para FKs
    'tb_servico': 'co_servico',           # Provavelmente essencial para FKs
    'tb_financiamento': 'co_financiamento',
    'tb_rubrica': 'co_rubrica',
    'tb_detalhe': 'co_detalhe',
    'tb_habilitacao': 'co_habilitacao',
    'tb_rede_atencao': 'co_rede_atencao',
    'tb_componente_rede': 'co_componente_rede', # Chave desta tabela
    'tb_registro': 'co_registro',
    'tb_tipo_leito': 'co_tipo_leito',
    'tb_regra_condicionada': 'co_regra_condicionada',
    'tb_tuss': 'co_tuss',
    # 'tb_sia_sih': 'co_procedimento_sia_sih', # REMOVA SE (co_procedimento_sia_sih, version_id) PODE REPETIR
                                              # O erro no log indica que esta constraint existe e causa problemas.
    # 'tb_sub_grupo': 'co_sub_grupo',       # REMOVA SE (co_sub_grupo, version_id) PODE REPETIR
                                              # O erro no log indica que esta constraint existe.
    # 'tb_servico_classificacao' é tratado separadamente para chave múltipla
}

# Chaves Únicas Compostas Especiais (mais de uma coluna 'co_' + version_id)
# Chave: nome_tabela
# Valor: lista de nomes de colunas que formam a UNIQUE com version_id
UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION = {
    'tb_servico_classificacao': ['co_servico', 'co_classificacao'] 
    # Adicione outras se necessário, ex:
    # 'rl_procedimento_compativel': ['co_procedimento_principal', 'co_procedimento_compativel']
}
# Se rl_procedimento_compativel precisa de UNIQUE (co_procedimento_principal, version_id), 
# adicione a 'tb_procedimento_compativel' (ou o nome correto da tabela) em COLUNAS_CO_PARA_UNIQUE_COMPOSTA,
# ou se a constraint é (co_procedimento_principal, co_procedimento_compativel, version_id), adicione a UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION


sql_tb_version = f"""
-- Script SQL gerado para o banco SIGTAP (Schema v2.4 - Controle Fino de UNIQUEs)
-- Data de geração: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CREATE TABLE IF NOT EXISTS "{TABELA_VERSION}" (
    id BIGSERIAL PRIMARY KEY,
    competencia VARCHAR(6) UNIQUE NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

def parse_layout_metadata(layout_filepath):
    # (Mantida a mesma função parse_layout_metadata da resposta anterior)
    column_definitions = []
    table_name = None
    try:
        filename = os.path.basename(layout_filepath)
        table_name = filename.replace(SUFIXO_LAYOUT, '').lower()
        if not table_name: return None, None
        with open(layout_filepath, 'r', encoding=CODIFICACAO_LAYOUT) as f:
            reader = csv.reader(f)
            try: header_line = next(reader)
            except StopIteration: return table_name, [] 
            header = [h.strip().lower() for h in header_line]
            header_map = {h: i for i, h in enumerate(header)}
            required_cols = ['coluna', 'tamanho', 'inicio', 'fim', 'tipo']
            missing_cols = [rc for rc in required_cols if rc not in header_map]
            if missing_cols:
                print(f"Erro: Layout {filename} sem colunas: {', '.join(missing_cols)}. Cabeçalho: {header}")
                return table_name, None 
            for i, row in enumerate(reader):
                if not row or not any(field.strip() for field in row) or len(row) < len(required_cols): continue 
                try:
                    col_name_raw = row[header_map['coluna']].strip()
                    col_name = col_name_raw.lower().replace(' ', '_').replace('-', '_')
                    tam_str = row[header_map['tamanho']].strip()
                    col_type_raw = row[header_map['tipo']].strip().upper()
                    if not col_name: continue
                    tam = int(tam_str) if tam_str.isdigit() else 0
                    if col_type_raw == 'VARCHAR2': col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT'
                    elif col_type_raw == 'CHAR': col_type = f'CHAR({tam})' if tam > 0 else 'CHAR(1)'
                    elif col_type_raw.startswith('NUMBER'): col_type = 'NUMERIC' 
                    elif col_type_raw == 'DATE' : col_type = 'DATE'
                    elif col_type_raw == 'ALFA' : col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT'
                    elif col_type_raw == 'NUM' : 
                        if tam > 9: col_type = 'BIGINT' 
                        elif tam > 4: col_type = 'INTEGER' 
                        elif tam > 0: col_type = 'SMALLINT' 
                        else: col_type = 'NUMERIC' 
                    else: col_type = f'VARCHAR({tam})' if tam > 0 else 'TEXT' 
                    column_definitions.append({'name': col_name, 'type': col_type, 'raw_name': col_name_raw})
                except (IndexError, ValueError) as e: print(f"Aviso: Pulando linha (índice/valor) layout {filename}, linha {i+2}: {row} - Erro: {e}")
                except KeyError as e: print(f"Aviso: Pulando linha (KeyError: {e}) layout {filename}, linha {i+2}: {row}")
        return table_name, column_definitions
    except UnicodeDecodeError as ude: print(f"Erro encoding layout {layout_filepath} com {CODIFICACAO_LAYOUT}: {ude}"); return None, None
    except FileNotFoundError: print(f"Erro: Layout não encontrado: {layout_filepath}"); return None, None
    except Exception as e: print(f"Erro ao ler/parsear layout {layout_filepath}: {e}"); return None, None

def main():
    print(f"--- Gerador de Scripts SQL CREATE TABLE (Schema v2.4 - Controle Fino de UNIQUEs) ---")
    all_sql_scripts = [sql_tb_version]
    # Estrutura: {table_name: {'cols': [col_names], 'unique_keys': [ ('col1', 'col2', ...), ... ] }}
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
            table_name, raw_col_defs = parse_layout_metadata(filepath)
            if table_name and raw_col_defs is not None: 
                if raw_col_defs: parsed_layouts[table_name] = raw_col_defs
            elif table_name and raw_col_defs is None:
                 print(f"Aviso: Definições para {table_name} não parseadas. Tabela pulada.")
        
        ordem_para_criar_final = []
        if 'ORDEM_PROCESSAMENTO_TABELAS_BASE' in globals() and isinstance(ORDEM_PROCESSAMENTO_TABELAS_BASE, list): 
            referencia_ordem = [tbl.lower() for tbl in ORDEM_PROCESSAMENTO_TABELAS_BASE]
            for tbl_base_name in referencia_ordem:
                if tbl_base_name in parsed_layouts and tbl_base_name not in ordem_para_criar_final:
                    ordem_para_criar_final.append(tbl_base_name)
        for tbl_base_name in parsed_layouts:
            if tbl_base_name not in ordem_para_criar_final:
                ordem_para_criar_final.append(tbl_base_name)

        for table_name in ordem_para_criar_final:
            if table_name not in parsed_layouts : continue
            raw_col_defs = parsed_layouts[table_name]
            column_sql_lines = [f"    id BIGINT NOT NULL", f"    \"{COLUNA_VERSION_FK}\" BIGINT NOT NULL"]
            unique_constraints_definitions = [] # Lista de tuplas de colunas para UNIQUE
            current_table_all_col_names = ['id', COLUNA_VERSION_FK]

            for col_def in raw_col_defs:
                col_name = col_def['name']
                col_type = col_def['type']
                if col_name.lower() in ['id', COLUNA_VERSION_FK.lower()]: continue
                line = f"    \"{col_name}\" {col_type}"
                column_sql_lines.append(line)
                current_table_all_col_names.append(col_name)

            # Adicionar UNIQUE (col_name, version_id) SELETIVAMENTE
            if table_name in COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION:
                col_co_principal = COLUNAS_CO_PARA_UNIQUE_COMPOSTA_COM_VERSION[table_name]
                if col_co_principal and col_co_principal in current_table_all_col_names: # Verifica se a coluna existe
                    unique_constraints_definitions.append( (col_co_principal, COLUNA_VERSION_FK) )
            
            # Adicionar UNIQUEs Compostas Especiais
            if table_name in UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION:
                cols_para_unique_especial = UNIQUE_COMPOSTAS_ESPECIAIS_COM_VERSION[table_name]
                # Verificar se todas as colunas da unique especial existem na tabela
                if all(c in current_table_all_col_names for c in cols_para_unique_especial):
                    unique_constraints_definitions.append( tuple(list(cols_para_unique_especial) + [COLUNA_VERSION_FK]) )
            
            column_sql_lines.append(f"    PRIMARY KEY (id, \"{COLUNA_VERSION_FK}\")")
            
            # Criar as strings de constraint UNIQUE
            for i, uk_cols_tuple in enumerate(unique_constraints_definitions):
                uk_cols_quoted = [f'"{c}"' for c in uk_cols_tuple]
                constraint_name_suffix = "_".join(c.replace('co_','').replace('rl_','').replace('tb_','') for c in uk_cols_tuple if c != COLUNA_VERSION_FK) # Nome mais curto
                column_sql_lines.append(f"    CONSTRAINT uq_{table_name}_{constraint_name_suffix}_{i} UNIQUE ({', '.join(uk_cols_quoted)})")

            column_sql_lines.append(f"    CONSTRAINT fk_{table_name}_{COLUNA_VERSION_FK} FOREIGN KEY (\"{COLUNA_VERSION_FK}\") REFERENCES \"{TABELA_VERSION}\" (id)")

            column_definitions_string = ",\n".join(column_sql_lines)
            sql_script = f"""\n-- Criação da tabela "{table_name}"\nCREATE TABLE IF NOT EXISTS "{table_name}" (\n{column_definitions_string}\n);"""
            all_sql_scripts.append(sql_script)
            table_metadata[table_name] = {'cols': current_table_all_col_names, 'unique_keys': unique_constraints_definitions}
            print(f"Gerado CREATE TABLE para: \"{table_name}\"")

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
                    fk_target_columns = None

                    for pt_name in possible_target_names:
                        if pt_name in table_metadata and pt_name != source_table_name:
                            target_meta = table_metadata[pt_name]
                            # A FK deve apontar para uma UNIQUE KEY ou PK na tabela alvo
                            # Tentativa 1: Apontar para (col_name_source, version_id) se for UNIQUE na alvo
                            if (col_name_source, COLUNA_VERSION_FK) in target_meta['unique_keys']:
                                target_table_found = pt_name
                                fk_target_columns = (col_name_source, COLUNA_VERSION_FK)
                                break
                            # Tentativa 2 (para tb_servico_classificacao): Apontar para (co_servico, co_classificacao, version_id)
                            elif pt_name == 'tb_servico_classificacao' and \
                                 ('co_servico', 'co_classificacao', COLUNA_VERSION_FK) in target_meta['unique_keys'] and \
                                 col_name_source == 'co_servico' and 'co_classificacao' in source_col_names:
                                target_table_found = pt_name
                                fk_target_columns = ('co_servico', 'co_classificacao', COLUNA_VERSION_FK)
                                break
                    
                    if target_table_found and fk_target_columns:
                        fk_source_columns = (col_name_source, COLUNA_VERSION_FK)
                        if target_table_found == 'tb_servico_classificacao' and len(fk_target_columns) == 3:
                            fk_source_columns = ('co_servico', 'co_classificacao', COLUNA_VERSION_FK)
                        
                        fk_constraint_name = f"fk_{source_table_name}_{'_'.join(fk_source_columns)}_comp"
                        fk_signature_tuple = tuple(sorted(fk_source_columns)) # Para a assinatura, normalizar a ordem
                        fk_signature = (source_table_name, fk_signature_tuple, target_table_found, tuple(sorted(fk_target_columns)))

                        if fk_signature not in added_fks_signatures:
                            fk_source_cols_quoted = [f'"{c}"' for c in fk_source_columns]
                            fk_target_cols_quoted = [f'"{c}"' for c in fk_target_columns]
                            
                            fk_sql = f"""\n-- FK de "{source_table_name}" para "{target_table_found}"
ALTER TABLE "{source_table_name}" ADD CONSTRAINT "{fk_constraint_name}"
FOREIGN KEY ({', '.join(fk_source_cols_quoted)}) 
REFERENCES "{target_table_found}" ({', '.join(fk_target_cols_quoted)});"""
                            
                            fk_scripts_alter.append(fk_sql)
                            added_fks_signatures.add(fk_signature)
                            print(f"  FK: \"{source_table_name}\"({', '.join(fk_source_columns)}) -> \"{target_table_found}\"({', '.join(fk_target_columns)})")
        all_sql_scripts.extend(fk_scripts_alter)

    except Exception as e:
        print(f"Erro inesperado: {e}"); import traceback; traceback.print_exc()

    full_sql_output = "\n\n".join(all_sql_scripts)
    if not os.path.isdir(CAMINHO_SAIDA_SQL):
        try: os.makedirs(CAMINHO_SAIDA_SQL, exist_ok=True); print(f"Pasta de saída criada: {CAMINHO_SAIDA_SQL}")
        except OSError as e: print(f"Erro ao criar pasta de saída {CAMINHO_SAIDA_SQL}: {e}"); return
    final_output_path = os.path.join(CAMINHO_SAIDA_SQL, NOME_ARQUIVO_SAIDA_SCHEMA)
    try:
        with open(final_output_path, "w", encoding='utf-8') as f: f.write(full_sql_output)
        print(f"\nScript de schema SQL gerado em {final_output_path}")
        print(f"Total de tabelas (CREATE TABLE): {len(parsed_layouts) + 1 if parsed_layouts else 1}")
        print(f"Total de FKs (ALTER TABLE): {len(fk_scripts_alter)}")
    except IOError as e: print(f"Erro ao salvar script SQL em {final_output_path}: {e}")

if __name__ == '__main__':
    main()