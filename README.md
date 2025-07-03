O projeto atual contém os seguintes scripts principais:

1- generate_sigtap_sql.py: Gera o schema do banco de dados (as tabelas).

2- gerador_arquivos_sql.py: Lê os arquivos de layout e os dados brutos (.txt) para gerar os scripts de INSERT em SQL.

3- executor_scripts_sql.py: Executa os scripts SQL gerados contra o banco de dados PostgreSQL.

-----------------------------------------------------------
generate_sigtap_sql.py: Para a criação do schema do banco de dados (tabelas, colunas, etc.).

gerador_arquivos_sql.py: Para ler os arquivos de layout e dados, e gerar os arquivos INSERT.

executor_scripts_sql.py: Para executar os scripts SQL gerados contra o banco de dados.
