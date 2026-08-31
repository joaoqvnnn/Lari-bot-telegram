# Migrações do Banco de Dados

Esta pasta contém as migrações do banco de dados gerenciadas pelo **Alembic**.

## 📌 O que são migrações?

Migrações são scripts versionados que alteram a estrutura do banco de dados (criação de tabelas, colunas, índices, etc.) de forma controlada e reproduzível.

Em vez de criar/modificar tabelas manualmente, usamos migrações para versionar o esquema e aplicar mudanças de forma consistente em qualquer ambiente (desenvolvimento, testes, produção).

---

## 🚀 Como usar

### 1. Inicializar o Alembic (apenas uma vez)

```bash
alembic init migrations
