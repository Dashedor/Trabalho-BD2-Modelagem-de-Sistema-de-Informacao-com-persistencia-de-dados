from sqlalchemy.orm import Session
from sqlalchemy import func
from tabelas import *

def consulta_ordens_em_andamento(db: Session):
    return db.query(
        OrdemServico.id,
        OrdemServico.dataEntrada,
        OrdemServico.dataPrevisao,
        OrdemServico.status,
        Pessoa.nome.label('nome_cliente'),
        Dispositivo.marca,
        Dispositivo.modelo
    ).join(Dispositivo)\
     .join(Cliente)\
     .join(Pessoa, Cliente.id == Pessoa.id)\
     .filter(OrdemServico.status.in_([StatusOrdem.ABERTA, StatusOrdem.EM_ANDAMENTO]))\
     .all()

def consulta_estoque_baixo(db: Session, limite: int = 5):
    return db.query(
        Estoque.id,
        Estoque.nome,
        Estoque.descricao,
        Estoque.quantidade,
        Estoque.valorUnitario,
        Fornecedor.nome.label('fornecedor')
    ).join(Fornecedor)\
     .filter(Estoque.quantidade <= limite)\
     .order_by(Estoque.quantidade.asc())\
     .all()

def consulta_estoque_zerado(db: Session):
    return db.query(
        Estoque.id,
        Estoque.nome,
        Estoque.descricao,
        Estoque.quantidade,
        Estoque.valorUnitario,
        Fornecedor.nome.label('fornecedor')
    ).join(Fornecedor)\
     .filter(Estoque.quantidade == 0)\
     .all()

def consulta_estoque_total(db: Session):
    return db.query(
        Estoque.id,
        Estoque.nome,
        Estoque.descricao,
        Estoque.quantidade,
        Estoque.valorUnitario,
        Fornecedor.nome.label('fornecedor')
    ).join(Fornecedor)\
     .order_by(Estoque.quantidade.asc())\
     .all()

def consulta_valor_total_estoque(db: Session):
    resultado = db.query(
        func.sum(Estoque.quantidade * Estoque.valorUnitario).label('valor_total')
    ).scalar()
    return resultado or 0.0

def consulta_faturamento_mensal(db: Session, mes: int, ano: int):
    return db.query(
        Orcamento.metodoPagamento,
        func.sum(Orcamento.precoTotal).label('total')
    ).filter(
        func.extract('month', Orcamento.dataHora) == mes,
        func.extract('year', Orcamento.dataHora) == ano
    ).group_by(Orcamento.metodoPagamento)\
     .all()

def consulta_tecnicos_mais_produtivos(db: Session, limite: int = 10):
    return db.query(
        Pessoa.nome,
        func.count(OrdemServico.id).label('ordens_concluidas')
    ).select_from(TecnicoInformatica)\
     .join(Funcionario, TecnicoInformatica.id == Funcionario.id)\
     .join(Pessoa, Funcionario.id == Pessoa.id)\
     .join(OrdemServico, TecnicoInformatica.id == OrdemServico.tecnico_id)\
     .filter(OrdemServico.status == StatusOrdem.CONCLUIDA)\
     .group_by(Pessoa.nome)\
     .order_by(func.count(OrdemServico.id).desc())\
     .limit(limite)\
     .all()

def consulta_clientes_fieis(db: Session, limite: int = 5):
    return db.query(
        Pessoa.nome,
        Pessoa.email,
        func.count(Dispositivo.id).label('total_dispositivos')
    ).select_from(Cliente)\
     .join(Pessoa, Cliente.id == Pessoa.id)\
     .join(Dispositivo, Cliente.id == Dispositivo.cliente_id)\
     .group_by(Pessoa.nome, Pessoa.email)\
     .order_by(func.count(Dispositivo.id).desc())\
     .limit(limite)\
     .all()