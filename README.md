# 🤖 Larizinha Store Bot

Sistema completo de vendas automáticas via Telegram, com entrega de produtos digitais, carteira de saldo, recargas via PIX, programa de afiliados, rankings, alertas e painel administrativo — tudo dentro do próprio Telegram.

---

## 📋 Visão Geral

O **Larizinha Store** é um bot para Telegram desenvolvido em Python que automatiza a venda de produtos digitais (logins, contas, ativações). Os clientes podem navegar pelo catálogo, comprar com saldo ou PIX, receber os produtos automaticamente, recarregar a carteira, participar do programa de afiliados e muito mais — sem intervenção humana.

O administrador gerencia tudo por um painel exclusivo dentro do próprio bot: produtos, estoque, categorias, mensagens, usuários, pagamentos, gift cards, afiliados, estatísticas, broadcasts e configurações.

---

## ✨ Funcionalidades

### Cliente
- 🛍 **Catálogo** de produtos organizado por categorias
- 💰 **Carteira de saldo** com recargas via PIX (QR Code e copia-e-cola)
- ⚡ **Entrega automática** de produtos após aprovação do pagamento
- 🎁 **Gift Cards** para resgate de saldo
- 👤 **Perfil** com informações e histórico de compras
- 📧 **Envio por Email/WhatsApp** dos dados da compra
- 🤝 **Programa de afiliados** com link exclusivo e comissões
- 🏆 **Rankings** (serviços mais vendidos, maiores recarregadores, etc.)
- 🔔 **Alertas de reabastecimento** de produtos
- 🔍 **Pesquisa inline** no Telegram
- ⚙️ **Mensagens personalizáveis** (tudo editável pelo admin)

### Administrador
- 📦 **CRUD de produtos** (criar, editar, excluir, ativar/desativar)
- 📁 **Gerenciamento de categorias**
- 📋 **Controle de estoque** (adicionar itens manualmente ou via arquivo)
- 👥 **Gerenciamento de usuários** (saldo, bloqueio, mensagens diretas)
- 💬 **Editor de mensagens** (todas as mensagens do bot editáveis)
- 🎁 **Gerador de gift cards** (lote, validade, revogação)
- 💰 **Afiliados e saques** (aprovar/recusar solicitações)
- 💳 **Pagamentos PIX** (visualizar, verificar, cancelar)
- 📊 **Estatísticas** (faturamento, vendas, usuários)
- 📨 **Broadcast** (envio de mensagens em massa)
- ⚙️ **Configurações gerais** (gateway, bônus, comissões, limites, etc.)

---

## 🏗️ Arquitetura e Tecnologias

| Camada       | Tecnologia            | Justificativa                                      |
|--------------|----------------------|---------------------------------------------------|
| Linguagem    | Python 3.10+         | Ecossistema maduro, bibliotecas assíncronas       |
| Framework    | Aiogram 3.x          | Suporte a FSM, inline keyboards, callbacks, async |
| Banco de dados | PostgreSQL         | Robusto, transações, concorrência, JSON           |
| Cache/Filas  | Redis + Celery       | Tarefas assíncronas (expiração PIX, alertas)      |
| Pagamento    | Mercado Pago (ou Efí)| API oficial de PIX imediato, webhooks             |
| Hospedagem   | VPS Ubuntu 22.04     | Controle total, execução contínua                 |
| Armazenamento| Disco local (ou S3)  | QR codes, comprovantes, backups                   |
| Monitoramento| Logs + notificações  | Auditoria e depuração                             |

---

## 📁 Estrutura de Diretórios
