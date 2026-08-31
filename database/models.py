# ==============================================
# MODELOS DE DADOS (TABELAS) - SQLAlchemy 2.x
# ==============================================

import uuid
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # ID do Telegram
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    saldo: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    indicado_por: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    bloqueado: Mapped[bool] = mapped_column(Boolean, default=False)
    total_gasto: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    total_recargas: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    total_gifts: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(128))
    emoji: Mapped[str] = mapped_column(String(16), default="📁")
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    nome: Mapped[str] = mapped_column(String(255))
    emoji: Mapped[str] = mapped_column(String(16), default="🛒")
    descricao: Mapped[str] = mapped_column(Text, default="")
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estoque: Mapped[int] = mapped_column(Integer, default=0)
    vendidos: Mapped[int] = mapped_column(Integer, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    garantia_dias: Mapped[int] = mapped_column(Integer, default=30)
    mensagem_entrega: Mapped[str] = mapped_column(Text, default="")
    alerta_estoque_baixo: Mapped[int] = mapped_column(Integer, default=1)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class EstoqueItem(Base):
    __tablename__ = "estoque_itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    conteudo: Mapped[str] = mapped_column(Text)
    vendido: Mapped[bool] = mapped_column(Boolean, default=False)
    venda_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vendas.id"), nullable=True)


class Venda(Base):
    __tablename__ = "vendas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    quantidade: Mapped[int] = mapped_column(Integer, default=1)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    data_compra: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    vencimento: Mapped[date] = mapped_column(Date, nullable=True)
    forma_pagamento: Mapped[str] = mapped_column(String(20))  # 'saldo' ou 'pix'
    status: Mapped[str] = mapped_column(String(20), default="pago")  # 'pago', 'pendente', 'cancelado', 'expirado'
    itens_entregues: Mapped[list | None] = mapped_column(JSON, nullable=True)
    email_enviado: Mapped[str | None] = mapped_column(String(255), nullable=True)
    whatsapp_enviado: Mapped[str | None] = mapped_column(String(20), nullable=True)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)


class PagamentoPix(Base):
    __tablename__ = "pagamentos_pix"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    tipo: Mapped[str] = mapped_column(String(20))  # 'recarga' ou 'compra'
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    bonus: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    status: Mapped[str] = mapped_column(String(20), default="pendente")  # 'pendente', 'pago', 'expirado', 'cancelado'
    codigo_pix: Mapped[str] = mapped_column(Text, nullable=True)
    qr_code_base64: Mapped[str] = mapped_column(Text, nullable=True)
    txid: Mapped[str] = mapped_column(String(64), nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    data_expiracao: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    data_pagamento: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    referencia: Mapped[str | None] = mapped_column(String(255), nullable=True)


class GiftCard(Base):
    __tablename__ = "gift_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    usado: Mapped[bool] = mapped_column(Boolean, default=False)
    usado_por: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    data_uso: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expira_em: Mapped[date | None] = mapped_column(Date, nullable=True)


class Afiliado(Base):
    __tablename__ = "afiliados"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    comissao_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("10.00"))
    total_ganho: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    saldo_comissoes: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    total_indicacoes: Mapped[int] = mapped_column(Integer, default=0)
    nivel: Mapped[str] = mapped_column(String(50), default="Iniciante")
    meta_indicacoes: Mapped[int] = mapped_column(Integer, default=5)


class SaqueAfiliado(Base):
    __tablename__ = "saques_afiliados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    chave_pix: Mapped[str] = mapped_column(String(255))
    dados_bancarios: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pendente")  # 'pendente', 'aprovado', 'recusado', 'pago'
    data_solicitacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    data_processamento: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Alerta(Base):
    __tablename__ = "alertas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("user_id", "produto_id", name="uq_alerta_usuario_produto"),
    )


class MensagemPersonalizada(Base):
    __tablename__ = "mensagens_personalizadas"

    chave: Mapped[str] = mapped_column(String(64), primary_key=True)
    texto: Mapped[str] = mapped_column(Text)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class Configuracao(Base):
    __tablename__ = "configuracoes"

    chave: Mapped[str] = mapped_column(String(64), primary_key=True)
    valor: Mapped[str] = mapped_column(Text)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    acao: Mapped[str] = mapped_column(String(255))
    detalhes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
