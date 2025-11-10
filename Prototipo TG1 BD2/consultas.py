from sqlalchemy.orm import Session
from sqlalchemy import func
from tabelas import *

def consulta_ordens_em_andamento(db: Session):
    #1: Ordens de serviço em andamento
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
    #2: Itens com estoque baixo
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

def consulta_tecnicos_mais_produtivos(db: Session, limite: int = 10):
    #3: Técnicos com mais ordens concluídas
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
    #4: Clientes com mais dispositivos cadastrados
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

