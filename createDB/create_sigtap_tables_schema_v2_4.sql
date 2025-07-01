
-- Script SQL gerado para o banco SIGTAP (Schema v2.4 - Controle Fino de UNIQUEs)
-- Data de geração: 2025-05-12 21:20:48
-- Funcionando todos os INSERT, com essa versão do codigo.

CREATE TABLE IF NOT EXISTS "tb_version" (
    id BIGSERIAL PRIMARY KEY,
    competencia VARCHAR(6) UNIQUE NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);



-- Criação da tabela "rl_excecao_compatibilidade"
CREATE TABLE IF NOT EXISTS "rl_excecao_compatibilidade" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento_restricao" VARCHAR(10),
    "co_procedimento_principal" VARCHAR(10),
    "co_registro_principal" VARCHAR(2),
    "co_procedimento_compativel" VARCHAR(10),
    "co_registro_compativel" VARCHAR(2),
    "tp_compatibilidade" VARCHAR(1),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_excecao_compatibilidade_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_cid"
CREATE TABLE IF NOT EXISTS "rl_procedimento_cid" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_cid" VARCHAR(4),
    "st_principal" CHAR(1),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_cid_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_comp_rede"
CREATE TABLE IF NOT EXISTS "rl_procedimento_comp_rede" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_componente_rede" VARCHAR(10),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_comp_rede_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_compativel"
CREATE TABLE IF NOT EXISTS "rl_procedimento_compativel" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento_principal" VARCHAR(10),
    "co_registro_principal" VARCHAR(2),
    "co_procedimento_compativel" VARCHAR(10),
    "co_registro_compativel" VARCHAR(2),
    "tp_compatibilidade" VARCHAR(1),
    "qt_permitida" NUMERIC,
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_compativel_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_detalhe"
CREATE TABLE IF NOT EXISTS "rl_procedimento_detalhe" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_detalhe" VARCHAR(3),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_detalhe_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_habilitacao"
CREATE TABLE IF NOT EXISTS "rl_procedimento_habilitacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_habilitacao" VARCHAR(4),
    "nu_grupo_habilitacao" VARCHAR(4),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_habilitacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_incremento"
CREATE TABLE IF NOT EXISTS "rl_procedimento_incremento" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_habilitacao" VARCHAR(4),
    "vl_percentual_sh" NUMERIC,
    "vl_percentual_sa" NUMERIC,
    "vl_percentual_sp" NUMERIC,
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_incremento_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_leito"
CREATE TABLE IF NOT EXISTS "rl_procedimento_leito" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_tipo_leito" VARCHAR(2),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_leito_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_modalidade"
CREATE TABLE IF NOT EXISTS "rl_procedimento_modalidade" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_modalidade" VARCHAR(2),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_modalidade_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_ocupacao"
CREATE TABLE IF NOT EXISTS "rl_procedimento_ocupacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_ocupacao" CHAR(6),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_ocupacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_origem"
CREATE TABLE IF NOT EXISTS "rl_procedimento_origem" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_procedimento_origem" VARCHAR(10),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_origem_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_registro"
CREATE TABLE IF NOT EXISTS "rl_procedimento_registro" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_registro" VARCHAR(2),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_registro_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_regra_cond"
CREATE TABLE IF NOT EXISTS "rl_procedimento_regra_cond" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_regra_condicionada" VARCHAR(4),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_regra_cond_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_renases"
CREATE TABLE IF NOT EXISTS "rl_procedimento_renases" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_renases" VARCHAR(10),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_renases_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_servico"
CREATE TABLE IF NOT EXISTS "rl_procedimento_servico" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_servico" VARCHAR(3),
    "co_classificacao" VARCHAR(3),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_servico_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_sia_sih"
CREATE TABLE IF NOT EXISTS "rl_procedimento_sia_sih" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_procedimento_sia_sih" VARCHAR(10),
    "tp_procedimento" VARCHAR(1),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_sia_sih_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "rl_procedimento_tuss"
CREATE TABLE IF NOT EXISTS "rl_procedimento_tuss" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "co_tuss" VARCHAR(10),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_rl_procedimento_tuss_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_cid"
CREATE TABLE IF NOT EXISTS "tb_cid" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_cid" VARCHAR(4),
    "no_cid" VARCHAR(100),
    "tp_agravo" CHAR(1),
    "tp_sexo" CHAR(1),
    "tp_estadio" CHAR(1),
    "vl_campos_irradiados" NUMERIC,
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_cid_cid_0 UNIQUE ("co_cid", "version_id"),
    CONSTRAINT fk_tb_cid_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_componente_rede"
CREATE TABLE IF NOT EXISTS "tb_componente_rede" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_componente_rede" VARCHAR(10),
    "no_componente_rede" VARCHAR(150),
    "co_rede_atencao" VARCHAR(3),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_componente_rede_componente_rede_0 UNIQUE ("co_componente_rede", "version_id"),
    CONSTRAINT fk_tb_componente_rede_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_descricao_detalhe"
CREATE TABLE IF NOT EXISTS "tb_descricao_detalhe" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_detalhe" VARCHAR(3),
    "ds_detalhe" VARCHAR(4000),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_descricao_detalhe_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_descricao"
CREATE TABLE IF NOT EXISTS "tb_descricao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "ds_procedimento" VARCHAR(4000),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_descricao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_detalhe"
CREATE TABLE IF NOT EXISTS "tb_detalhe" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_detalhe" VARCHAR(3),
    "no_detalhe" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_detalhe_detalhe_0 UNIQUE ("co_detalhe", "version_id"),
    CONSTRAINT fk_tb_detalhe_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_financiamento"
CREATE TABLE IF NOT EXISTS "tb_financiamento" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_financiamento" VARCHAR(2),
    "no_financiamento" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_financiamento_financiamento_0 UNIQUE ("co_financiamento", "version_id"),
    CONSTRAINT fk_tb_financiamento_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_forma_organizacao"
CREATE TABLE IF NOT EXISTS "tb_forma_organizacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_grupo" VARCHAR(2),
    "co_sub_grupo" VARCHAR(2),
    "co_forma_organizacao" VARCHAR(2),
    "no_forma_organizacao" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_forma_organizacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_grupo_habilitacao"
CREATE TABLE IF NOT EXISTS "tb_grupo_habilitacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "nu_grupo_habilitacao" VARCHAR(4),
    "no_grupo_habilitacao" VARCHAR(20),
    "ds_grupo_habilitacao" VARCHAR(250),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_grupo_habilitacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_grupo"
CREATE TABLE IF NOT EXISTS "tb_grupo" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_grupo" VARCHAR(2),
    "no_grupo" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_grupo_grupo_0 UNIQUE ("co_grupo", "version_id"),
    CONSTRAINT fk_tb_grupo_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_habilitacao"
CREATE TABLE IF NOT EXISTS "tb_habilitacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_habilitacao" VARCHAR(4),
    "no_habilitacao" VARCHAR(150),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_habilitacao_habilitacao_0 UNIQUE ("co_habilitacao", "version_id"),
    CONSTRAINT fk_tb_habilitacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_modalidade"
CREATE TABLE IF NOT EXISTS "tb_modalidade" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_modalidade" VARCHAR(2),
    "no_modalidade" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_modalidade_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_ocupacao"
CREATE TABLE IF NOT EXISTS "tb_ocupacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_ocupacao" CHAR(6),
    "no_ocupacao" VARCHAR(150),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_ocupacao_ocupacao_0 UNIQUE ("co_ocupacao", "version_id"),
    CONSTRAINT fk_tb_ocupacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_procedimento"
CREATE TABLE IF NOT EXISTS "tb_procedimento" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento" VARCHAR(10),
    "no_procedimento" VARCHAR(250),
    "tp_complexidade" VARCHAR(1),
    "tp_sexo" VARCHAR(1),
    "qt_maxima_execucao" NUMERIC,
    "qt_dias_permanencia" NUMERIC,
    "qt_pontos" NUMERIC,
    "vl_idade_minima" NUMERIC,
    "vl_idade_maxima" NUMERIC,
    "vl_sh" NUMERIC,
    "vl_sa" NUMERIC,
    "vl_sp" NUMERIC,
    "co_financiamento" VARCHAR(2),
    "co_rubrica" VARCHAR(6),
    "qt_tempo_permanencia" NUMERIC,
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_procedimento_procedimento_0 UNIQUE ("co_procedimento", "version_id"),
    CONSTRAINT fk_tb_procedimento_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_rede_atencao"
CREATE TABLE IF NOT EXISTS "tb_rede_atencao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_rede_atencao" VARCHAR(3),
    "no_rede_atencao" VARCHAR(50),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_rede_atencao_rede_atencao_0 UNIQUE ("co_rede_atencao", "version_id"),
    CONSTRAINT fk_tb_rede_atencao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_registro"
CREATE TABLE IF NOT EXISTS "tb_registro" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_registro" VARCHAR(2),
    "no_registro" VARCHAR(50),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_registro_registro_0 UNIQUE ("co_registro", "version_id"),
    CONSTRAINT fk_tb_registro_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_regra_condicionada"
CREATE TABLE IF NOT EXISTS "tb_regra_condicionada" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_regra_condicionada" VARCHAR(4),
    "no_regra_condicionada" VARCHAR(150),
    "ds_regra_condicionada" VARCHAR(4000),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_regra_condicionada_regra_condicionada_0 UNIQUE ("co_regra_condicionada", "version_id"),
    CONSTRAINT fk_tb_regra_condicionada_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_renases"
CREATE TABLE IF NOT EXISTS "tb_renases" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_renases" VARCHAR(10),
    "no_renases" VARCHAR(150),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_renases_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_rubrica"
CREATE TABLE IF NOT EXISTS "tb_rubrica" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_rubrica" VARCHAR(6),
    "no_rubrica" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_rubrica_rubrica_0 UNIQUE ("co_rubrica", "version_id"),
    CONSTRAINT fk_tb_rubrica_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_servico_classificacao"
CREATE TABLE IF NOT EXISTS "tb_servico_classificacao" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_servico" VARCHAR(3),
    "co_classificacao" VARCHAR(3),
    "no_classificacao" VARCHAR(150),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_servico_classificacao_servico_classificacao_0 UNIQUE ("co_servico", "co_classificacao", "version_id"),
    CONSTRAINT fk_tb_servico_classificacao_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_servico"
CREATE TABLE IF NOT EXISTS "tb_servico" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_servico" VARCHAR(3),
    "no_servico" VARCHAR(120),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_servico_servico_0 UNIQUE ("co_servico", "version_id"),
    CONSTRAINT fk_tb_servico_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_sia_sih"
CREATE TABLE IF NOT EXISTS "tb_sia_sih" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_procedimento_sia_sih" VARCHAR(10),
    "no_procedimento_sia_sih" VARCHAR(100),
    "tp_procedimento" VARCHAR(1),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_sia_sih_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_sub_grupo"
CREATE TABLE IF NOT EXISTS "tb_sub_grupo" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_grupo" VARCHAR(2),
    "co_sub_grupo" VARCHAR(2),
    "no_sub_grupo" VARCHAR(100),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT fk_tb_sub_grupo_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_tipo_leito"
CREATE TABLE IF NOT EXISTS "tb_tipo_leito" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_tipo_leito" VARCHAR(2),
    "no_tipo_leito" VARCHAR(60),
    "dt_competencia" CHAR(6),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_tipo_leito_tipo_leito_0 UNIQUE ("co_tipo_leito", "version_id"),
    CONSTRAINT fk_tb_tipo_leito_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- Criação da tabela "tb_tuss"
CREATE TABLE IF NOT EXISTS "tb_tuss" (
    id BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "co_tuss" VARCHAR(10),
    "no_tuss" VARCHAR(450),
    PRIMARY KEY (id, "version_id"),
    CONSTRAINT uq_tb_tuss_tuss_0 UNIQUE ("co_tuss", "version_id"),
    CONSTRAINT fk_tb_tuss_version_id FOREIGN KEY ("version_id") REFERENCES "tb_version" (id)
);


-- FK de "rl_procedimento_cid" para "tb_procedimento"
ALTER TABLE "rl_procedimento_cid" ADD CONSTRAINT "fk_rl_procedimento_cid_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_cid" para "tb_cid"
ALTER TABLE "rl_procedimento_cid" ADD CONSTRAINT "fk_rl_procedimento_cid_co_cid_version_id_comp"
FOREIGN KEY ("co_cid", "version_id") 
REFERENCES "tb_cid" ("co_cid", "version_id");


-- FK de "rl_procedimento_comp_rede" para "tb_procedimento"
ALTER TABLE "rl_procedimento_comp_rede" ADD CONSTRAINT "fk_rl_procedimento_comp_rede_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_comp_rede" para "tb_componente_rede"
ALTER TABLE "rl_procedimento_comp_rede" ADD CONSTRAINT "fk_rl_procedimento_comp_rede_co_componente_rede_version_id_comp"
FOREIGN KEY ("co_componente_rede", "version_id") 
REFERENCES "tb_componente_rede" ("co_componente_rede", "version_id");


-- FK de "rl_procedimento_detalhe" para "tb_procedimento"
ALTER TABLE "rl_procedimento_detalhe" ADD CONSTRAINT "fk_rl_procedimento_detalhe_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_detalhe" para "tb_detalhe"
ALTER TABLE "rl_procedimento_detalhe" ADD CONSTRAINT "fk_rl_procedimento_detalhe_co_detalhe_version_id_comp"
FOREIGN KEY ("co_detalhe", "version_id") 
REFERENCES "tb_detalhe" ("co_detalhe", "version_id");


-- FK de "rl_procedimento_habilitacao" para "tb_procedimento"
ALTER TABLE "rl_procedimento_habilitacao" ADD CONSTRAINT "fk_rl_procedimento_habilitacao_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_habilitacao" para "tb_habilitacao"
ALTER TABLE "rl_procedimento_habilitacao" ADD CONSTRAINT "fk_rl_procedimento_habilitacao_co_habilitacao_version_id_comp"
FOREIGN KEY ("co_habilitacao", "version_id") 
REFERENCES "tb_habilitacao" ("co_habilitacao", "version_id");


-- FK de "rl_procedimento_incremento" para "tb_procedimento"
ALTER TABLE "rl_procedimento_incremento" ADD CONSTRAINT "fk_rl_procedimento_incremento_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_incremento" para "tb_habilitacao"
ALTER TABLE "rl_procedimento_incremento" ADD CONSTRAINT "fk_rl_procedimento_incremento_co_habilitacao_version_id_comp"
FOREIGN KEY ("co_habilitacao", "version_id") 
REFERENCES "tb_habilitacao" ("co_habilitacao", "version_id");


-- FK de "rl_procedimento_leito" para "tb_procedimento"
ALTER TABLE "rl_procedimento_leito" ADD CONSTRAINT "fk_rl_procedimento_leito_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_leito" para "tb_tipo_leito"
ALTER TABLE "rl_procedimento_leito" ADD CONSTRAINT "fk_rl_procedimento_leito_co_tipo_leito_version_id_comp"
FOREIGN KEY ("co_tipo_leito", "version_id") 
REFERENCES "tb_tipo_leito" ("co_tipo_leito", "version_id");


-- FK de "rl_procedimento_modalidade" para "tb_procedimento"
ALTER TABLE "rl_procedimento_modalidade" ADD CONSTRAINT "fk_rl_procedimento_modalidade_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_ocupacao" para "tb_procedimento"
ALTER TABLE "rl_procedimento_ocupacao" ADD CONSTRAINT "fk_rl_procedimento_ocupacao_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_ocupacao" para "tb_ocupacao"
ALTER TABLE "rl_procedimento_ocupacao" ADD CONSTRAINT "fk_rl_procedimento_ocupacao_co_ocupacao_version_id_comp"
FOREIGN KEY ("co_ocupacao", "version_id") 
REFERENCES "tb_ocupacao" ("co_ocupacao", "version_id");


-- FK de "rl_procedimento_origem" para "tb_procedimento"
ALTER TABLE "rl_procedimento_origem" ADD CONSTRAINT "fk_rl_procedimento_origem_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_registro" para "tb_procedimento"
ALTER TABLE "rl_procedimento_registro" ADD CONSTRAINT "fk_rl_procedimento_registro_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_registro" para "tb_registro"
ALTER TABLE "rl_procedimento_registro" ADD CONSTRAINT "fk_rl_procedimento_registro_co_registro_version_id_comp"
FOREIGN KEY ("co_registro", "version_id") 
REFERENCES "tb_registro" ("co_registro", "version_id");


-- FK de "rl_procedimento_regra_cond" para "tb_procedimento"
ALTER TABLE "rl_procedimento_regra_cond" ADD CONSTRAINT "fk_rl_procedimento_regra_cond_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_regra_cond" para "tb_regra_condicionada"
ALTER TABLE "rl_procedimento_regra_cond" ADD CONSTRAINT "fk_rl_procedimento_regra_cond_co_regra_condicionada_version_id_comp"
FOREIGN KEY ("co_regra_condicionada", "version_id") 
REFERENCES "tb_regra_condicionada" ("co_regra_condicionada", "version_id");


-- FK de "rl_procedimento_renases" para "tb_procedimento"
ALTER TABLE "rl_procedimento_renases" ADD CONSTRAINT "fk_rl_procedimento_renases_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_servico" para "tb_procedimento"
ALTER TABLE "rl_procedimento_servico" ADD CONSTRAINT "fk_rl_procedimento_servico_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_servico" para "tb_servico"
ALTER TABLE "rl_procedimento_servico" ADD CONSTRAINT "fk_rl_procedimento_servico_co_servico_version_id_comp"
FOREIGN KEY ("co_servico", "version_id") 
REFERENCES "tb_servico" ("co_servico", "version_id");


-- FK de "rl_procedimento_sia_sih" para "tb_procedimento"
ALTER TABLE "rl_procedimento_sia_sih" ADD CONSTRAINT "fk_rl_procedimento_sia_sih_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_tuss" para "tb_procedimento"
ALTER TABLE "rl_procedimento_tuss" ADD CONSTRAINT "fk_rl_procedimento_tuss_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "rl_procedimento_tuss" para "tb_tuss"
ALTER TABLE "rl_procedimento_tuss" ADD CONSTRAINT "fk_rl_procedimento_tuss_co_tuss_version_id_comp"
FOREIGN KEY ("co_tuss", "version_id") 
REFERENCES "tb_tuss" ("co_tuss", "version_id");


-- FK de "tb_componente_rede" para "tb_rede_atencao"
ALTER TABLE "tb_componente_rede" ADD CONSTRAINT "fk_tb_componente_rede_co_rede_atencao_version_id_comp"
FOREIGN KEY ("co_rede_atencao", "version_id") 
REFERENCES "tb_rede_atencao" ("co_rede_atencao", "version_id");


-- FK de "tb_descricao_detalhe" para "tb_detalhe"
ALTER TABLE "tb_descricao_detalhe" ADD CONSTRAINT "fk_tb_descricao_detalhe_co_detalhe_version_id_comp"
FOREIGN KEY ("co_detalhe", "version_id") 
REFERENCES "tb_detalhe" ("co_detalhe", "version_id");


-- FK de "tb_descricao" para "tb_procedimento"
ALTER TABLE "tb_descricao" ADD CONSTRAINT "fk_tb_descricao_co_procedimento_version_id_comp"
FOREIGN KEY ("co_procedimento", "version_id") 
REFERENCES "tb_procedimento" ("co_procedimento", "version_id");


-- FK de "tb_forma_organizacao" para "tb_grupo"
ALTER TABLE "tb_forma_organizacao" ADD CONSTRAINT "fk_tb_forma_organizacao_co_grupo_version_id_comp"
FOREIGN KEY ("co_grupo", "version_id") 
REFERENCES "tb_grupo" ("co_grupo", "version_id");


-- FK de "tb_procedimento" para "tb_financiamento"
ALTER TABLE "tb_procedimento" ADD CONSTRAINT "fk_tb_procedimento_co_financiamento_version_id_comp"
FOREIGN KEY ("co_financiamento", "version_id") 
REFERENCES "tb_financiamento" ("co_financiamento", "version_id");


-- FK de "tb_procedimento" para "tb_rubrica"
ALTER TABLE "tb_procedimento" ADD CONSTRAINT "fk_tb_procedimento_co_rubrica_version_id_comp"
FOREIGN KEY ("co_rubrica", "version_id") 
REFERENCES "tb_rubrica" ("co_rubrica", "version_id");


-- FK de "tb_servico_classificacao" para "tb_servico"
ALTER TABLE "tb_servico_classificacao" ADD CONSTRAINT "fk_tb_servico_classificacao_co_servico_version_id_comp"
FOREIGN KEY ("co_servico", "version_id") 
REFERENCES "tb_servico" ("co_servico", "version_id");


-- FK de "tb_sub_grupo" para "tb_grupo"
ALTER TABLE "tb_sub_grupo" ADD CONSTRAINT "fk_tb_sub_grupo_co_grupo_version_id_comp"
FOREIGN KEY ("co_grupo", "version_id") 
REFERENCES "tb_grupo" ("co_grupo", "version_id");