
-- Script SQL gerado automaticamente para o banco SIGTAP
-- Data de geração: 2025-05-08 16:50:46

-- Criação da tabela de versionamento
-- Esta tabela deve ser criada primeiro, pois outras tabelas referenciam ela.
CREATE TABLE tb_version (
    id BIGSERIAL PRIMARY KEY, -- BIGSERIAL gera IDs automaticamente
    competencia VARCHAR,   -- Campo para registrar a competência ou período da versão
    created_at BIGINT      -- Timestamp ou identificador de criação da versão
);




-- Criação da tabela tb_detalhe
CREATE TABLE tb_detalhe (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_detalhe VARCHAR(3) UNIQUE,
    no_detalhe VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_ocupacao
CREATE TABLE tb_ocupacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_ocupacao VARCHAR(6) UNIQUE,
    no_ocupacao VARCHAR(150)
);




-- Criação da tabela tb_financiamento
CREATE TABLE tb_financiamento (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_financiamento VARCHAR(2) UNIQUE,
    no_financiamento VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_habilitacao
CREATE TABLE rl_procedimento_habilitacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_habilitacao VARCHAR(4) UNIQUE,
    nu_grupo_habilitacao VARCHAR(4),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_habilitacao
CREATE TABLE tb_habilitacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_habilitacao VARCHAR(4) UNIQUE,
    no_habilitacao VARCHAR(150),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_procedimento
CREATE TABLE tb_procedimento (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    no_procedimento VARCHAR(250),
    tp_complexidade VARCHAR(1),
    tp_sexo VARCHAR(1),
    qt_maxima_execucao NUMERIC,
    qt_dias_permanencia NUMERIC,
    qt_pontos NUMERIC,
    vl_idade_minima NUMERIC,
    vl_idade_maxima NUMERIC,
    vl_sh NUMERIC,
    vl_sa NUMERIC,
    vl_sp NUMERIC,
    co_financiamento VARCHAR(2) UNIQUE,
    co_rubrica VARCHAR(6) UNIQUE,
    qt_tempo_permanencia NUMERIC,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_tipo_leito
CREATE TABLE tb_tipo_leito (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_tipo_leito VARCHAR(2) UNIQUE,
    no_tipo_leito VARCHAR(60),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_renases
CREATE TABLE rl_procedimento_renases (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_renases VARCHAR(10) UNIQUE
);




-- Criação da tabela rl_procedimento_sia_sih
CREATE TABLE rl_procedimento_sia_sih (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_procedimento_sia_sih VARCHAR(10) UNIQUE,
    tp_procedimento VARCHAR(1),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_grupo
CREATE TABLE tb_grupo (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_grupo VARCHAR(2) UNIQUE,
    no_grupo VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_sub_grupo
CREATE TABLE tb_sub_grupo (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_grupo VARCHAR(2) UNIQUE,
    co_sub_grupo VARCHAR(2) UNIQUE,
    no_sub_grupo VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_tuss
CREATE TABLE rl_procedimento_tuss (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_tuss VARCHAR(10) UNIQUE
);




-- Criação da tabela tb_registro
CREATE TABLE tb_registro (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_registro VARCHAR(2) UNIQUE,
    no_registro VARCHAR(50),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_comp_rede
CREATE TABLE rl_procedimento_comp_rede (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_componente_rede VARCHAR(10) UNIQUE
);




-- Criação da tabela rl_procedimento_cid
CREATE TABLE rl_procedimento_cid (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_cid VARCHAR(4) UNIQUE,
    st_principal VARCHAR(1),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_modalidade
CREATE TABLE rl_procedimento_modalidade (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_modalidade VARCHAR(2) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_componente_rede
CREATE TABLE tb_componente_rede (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_componente_rede VARCHAR(10) UNIQUE,
    no_componente_rede VARCHAR(150),
    co_rede_atencao VARCHAR(3) UNIQUE
);




-- Criação da tabela tb_rede_atencao
CREATE TABLE tb_rede_atencao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_rede_atencao VARCHAR(3) UNIQUE,
    no_rede_atencao VARCHAR(50)
);




-- Criação da tabela rl_procedimento_ocupacao
CREATE TABLE rl_procedimento_ocupacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_ocupacao VARCHAR(6) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_servico
CREATE TABLE rl_procedimento_servico (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_servico VARCHAR(3) UNIQUE,
    co_classificacao VARCHAR(3) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_servico_classificacao
CREATE TABLE tb_servico_classificacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_servico VARCHAR(3) UNIQUE,
    co_classificacao VARCHAR(3) UNIQUE,
    no_classificacao VARCHAR(150),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_leito
CREATE TABLE rl_procedimento_leito (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_tipo_leito VARCHAR(2) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_descricao_detalhe
CREATE TABLE tb_descricao_detalhe (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_detalhe VARCHAR(3) UNIQUE,
    ds_detalhe VARCHAR(4000),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_detalhe
CREATE TABLE rl_procedimento_detalhe (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_detalhe VARCHAR(3) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_renases
CREATE TABLE tb_renases (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_renases VARCHAR(10) UNIQUE,
    no_renases VARCHAR(150)
);




-- Criação da tabela rl_excecao_compatibilidade
CREATE TABLE rl_excecao_compatibilidade (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento_restricao VARCHAR(10) UNIQUE,
    co_procedimento_principal VARCHAR(10) UNIQUE,
    co_registro_principal VARCHAR(2) UNIQUE,
    co_procedimento_compativel VARCHAR(10) UNIQUE,
    co_registro_compativel VARCHAR(2) UNIQUE,
    tp_compatibilidade VARCHAR(1),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_registro
CREATE TABLE rl_procedimento_registro (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_registro VARCHAR(2) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_sia_sih
CREATE TABLE tb_sia_sih (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento_sia_sih VARCHAR(10) UNIQUE,
    no_procedimento_sia_sih VARCHAR(100),
    tp_procedimento VARCHAR(1),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_regra_condicionada
CREATE TABLE tb_regra_condicionada (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_regra_condicionada VARCHAR(4) UNIQUE,
    no_regra_condicionada VARCHAR(150),
    ds_regra_condicionada VARCHAR(4000)
);




-- Criação da tabela tb_rubrica
CREATE TABLE tb_rubrica (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_rubrica VARCHAR(6) UNIQUE,
    no_rubrica VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_descricao
CREATE TABLE tb_descricao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    ds_procedimento VARCHAR(4000),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_cid
CREATE TABLE tb_cid (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_cid VARCHAR(4) UNIQUE,
    no_cid VARCHAR(100),
    tp_agravo VARCHAR(1),
    tp_sexo VARCHAR(1),
    tp_estadio VARCHAR(1),
    vl_campos_irradiados NUMERIC
);




-- Criação da tabela tb_modalidade
CREATE TABLE tb_modalidade (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_modalidade VARCHAR(2) UNIQUE,
    no_modalidade VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_forma_organizacao
CREATE TABLE tb_forma_organizacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_grupo VARCHAR(2) UNIQUE,
    co_sub_grupo VARCHAR(2) UNIQUE,
    co_forma_organizacao VARCHAR(2) UNIQUE,
    no_forma_organizacao VARCHAR(100),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_grupo_habilitacao
CREATE TABLE tb_grupo_habilitacao (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    nu_grupo_habilitacao VARCHAR(4),
    no_grupo_habilitacao VARCHAR(20),
    ds_grupo_habilitacao VARCHAR(250)
);




-- Criação da tabela rl_procedimento_compativel
CREATE TABLE rl_procedimento_compativel (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento_principal VARCHAR(10) UNIQUE,
    co_registro_principal VARCHAR(2) UNIQUE,
    co_procedimento_compativel VARCHAR(10) UNIQUE,
    co_registro_compativel VARCHAR(2) UNIQUE,
    tp_compatibilidade VARCHAR(1),
    qt_permitida NUMERIC,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela tb_servico
CREATE TABLE tb_servico (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_servico VARCHAR(3) UNIQUE,
    no_servico VARCHAR(120),
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_regra_cond
CREATE TABLE rl_procedimento_regra_cond (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_regra_condicionada VARCHAR(4) UNIQUE
);




-- Criação da tabela tb_tuss
CREATE TABLE tb_tuss (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_tuss VARCHAR(10) UNIQUE,
    no_tuss VARCHAR(450)
);




-- Criação da tabela rl_procedimento_origem
CREATE TABLE rl_procedimento_origem (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_procedimento_origem VARCHAR(10) UNIQUE,
    dt_competencia VARCHAR(6)
);




-- Criação da tabela rl_procedimento_incremento
CREATE TABLE rl_procedimento_incremento (
    id BIGSERIAL PRIMARY KEY,
    version_id BIGINT REFERENCES tb_version (id),
    co_procedimento VARCHAR(10) UNIQUE,
    co_habilitacao VARCHAR(4) UNIQUE,
    vl_percentual_sh NUMERIC,
    vl_percentual_sa NUMERIC,
    vl_percentual_sp NUMERIC,
    dt_competencia VARCHAR(6)
);




ALTER TABLE rl_procedimento_habilitacao
ADD CONSTRAINT fk_rl_procedimento_habilitacao_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_habilitacao
ADD CONSTRAINT fk_rl_procedimento_habilitacao_co_habilitacao
FOREIGN KEY (co_habilitacao)
REFERENCES tb_habilitacao (co_habilitacao);




ALTER TABLE tb_procedimento
ADD CONSTRAINT fk_tb_procedimento_co_financiamento
FOREIGN KEY (co_financiamento)
REFERENCES tb_financiamento (co_financiamento);




ALTER TABLE tb_procedimento
ADD CONSTRAINT fk_tb_procedimento_co_rubrica
FOREIGN KEY (co_rubrica)
REFERENCES tb_rubrica (co_rubrica);




ALTER TABLE rl_procedimento_renases
ADD CONSTRAINT fk_rl_procedimento_renases_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_renases
ADD CONSTRAINT fk_rl_procedimento_renases_co_renases
FOREIGN KEY (co_renases)
REFERENCES tb_renases (co_renases);




ALTER TABLE rl_procedimento_sia_sih
ADD CONSTRAINT fk_rl_procedimento_sia_sih_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE tb_sub_grupo
ADD CONSTRAINT fk_tb_sub_grupo_co_grupo
FOREIGN KEY (co_grupo)
REFERENCES tb_grupo (co_grupo);




ALTER TABLE rl_procedimento_tuss
ADD CONSTRAINT fk_rl_procedimento_tuss_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_tuss
ADD CONSTRAINT fk_rl_procedimento_tuss_co_tuss
FOREIGN KEY (co_tuss)
REFERENCES tb_tuss (co_tuss);




ALTER TABLE rl_procedimento_comp_rede
ADD CONSTRAINT fk_rl_procedimento_comp_rede_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_comp_rede
ADD CONSTRAINT fk_rl_procedimento_comp_rede_co_componente_rede
FOREIGN KEY (co_componente_rede)
REFERENCES tb_componente_rede (co_componente_rede);




ALTER TABLE rl_procedimento_cid
ADD CONSTRAINT fk_rl_procedimento_cid_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_cid
ADD CONSTRAINT fk_rl_procedimento_cid_co_cid
FOREIGN KEY (co_cid)
REFERENCES tb_cid (co_cid);




ALTER TABLE rl_procedimento_modalidade
ADD CONSTRAINT fk_rl_procedimento_modalidade_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_modalidade
ADD CONSTRAINT fk_rl_procedimento_modalidade_co_modalidade
FOREIGN KEY (co_modalidade)
REFERENCES tb_modalidade (co_modalidade);




ALTER TABLE tb_componente_rede
ADD CONSTRAINT fk_tb_componente_rede_co_rede_atencao
FOREIGN KEY (co_rede_atencao)
REFERENCES tb_rede_atencao (co_rede_atencao);




ALTER TABLE rl_procedimento_ocupacao
ADD CONSTRAINT fk_rl_procedimento_ocupacao_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_ocupacao
ADD CONSTRAINT fk_rl_procedimento_ocupacao_co_ocupacao
FOREIGN KEY (co_ocupacao)
REFERENCES tb_ocupacao (co_ocupacao);




ALTER TABLE rl_procedimento_servico
ADD CONSTRAINT fk_rl_procedimento_servico_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_servico
ADD CONSTRAINT fk_rl_procedimento_servico_co_servico
FOREIGN KEY (co_servico)
REFERENCES tb_servico (co_servico);




ALTER TABLE tb_servico_classificacao
ADD CONSTRAINT fk_tb_servico_classificacao_co_servico
FOREIGN KEY (co_servico)
REFERENCES tb_servico (co_servico);




ALTER TABLE rl_procedimento_leito
ADD CONSTRAINT fk_rl_procedimento_leito_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_leito
ADD CONSTRAINT fk_rl_procedimento_leito_co_tipo_leito
FOREIGN KEY (co_tipo_leito)
REFERENCES tb_tipo_leito (co_tipo_leito);




ALTER TABLE tb_descricao_detalhe
ADD CONSTRAINT fk_tb_descricao_detalhe_co_detalhe
FOREIGN KEY (co_detalhe)
REFERENCES tb_detalhe (co_detalhe);




ALTER TABLE rl_procedimento_detalhe
ADD CONSTRAINT fk_rl_procedimento_detalhe_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_detalhe
ADD CONSTRAINT fk_rl_procedimento_detalhe_co_detalhe
FOREIGN KEY (co_detalhe)
REFERENCES tb_detalhe (co_detalhe);




ALTER TABLE rl_excecao_compatibilidade
ADD CONSTRAINT fk_rl_excecao_compatibilidade_co_procedimento_compativel
FOREIGN KEY (co_procedimento_compativel)
REFERENCES rl_procedimento_compativel (co_procedimento_compativel);




ALTER TABLE rl_procedimento_registro
ADD CONSTRAINT fk_rl_procedimento_registro_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_registro
ADD CONSTRAINT fk_rl_procedimento_registro_co_registro
FOREIGN KEY (co_registro)
REFERENCES tb_registro (co_registro);




ALTER TABLE tb_sia_sih
ADD CONSTRAINT fk_tb_sia_sih_co_procedimento_sia_sih
FOREIGN KEY (co_procedimento_sia_sih)
REFERENCES rl_procedimento_sia_sih (co_procedimento_sia_sih);




ALTER TABLE tb_descricao
ADD CONSTRAINT fk_tb_descricao_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE tb_forma_organizacao
ADD CONSTRAINT fk_tb_forma_organizacao_co_grupo
FOREIGN KEY (co_grupo)
REFERENCES tb_grupo (co_grupo);




ALTER TABLE tb_forma_organizacao
ADD CONSTRAINT fk_tb_forma_organizacao_co_sub_grupo
FOREIGN KEY (co_sub_grupo)
REFERENCES tb_sub_grupo (co_sub_grupo);




ALTER TABLE rl_procedimento_regra_cond
ADD CONSTRAINT fk_rl_procedimento_regra_cond_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_regra_cond
ADD CONSTRAINT fk_rl_procedimento_regra_cond_co_regra_condicionada
FOREIGN KEY (co_regra_condicionada)
REFERENCES tb_regra_condicionada (co_regra_condicionada);




ALTER TABLE rl_procedimento_origem
ADD CONSTRAINT fk_rl_procedimento_origem_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_incremento
ADD CONSTRAINT fk_rl_procedimento_incremento_co_procedimento
FOREIGN KEY (co_procedimento)
REFERENCES tb_procedimento (co_procedimento);




ALTER TABLE rl_procedimento_incremento
ADD CONSTRAINT fk_rl_procedimento_incremento_co_habilitacao
FOREIGN KEY (co_habilitacao)
REFERENCES tb_habilitacao (co_habilitacao);
