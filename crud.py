from sqlalchemy.orm import Session
from tabelas import *
from datetime import datetime

def criar_pessoa(db: Session, nome: str, email: str, telefone: str, endereco_id: int, tipo: str):
    pessoa = Pessoa(
        nome=nome,
        email=email,
        telefone=telefone,
        endereco_id=endereco_id,
        tipo=tipo
    )
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return pessoa

def criar_endereco(db: Session, cep: str, rua: str, bairro: str, cidade: str, estado: str, logradouro: str = None):
    endereco = Endereco(
        cep=cep,
        rua=rua,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        logradouro=logradouro
    )
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco

def criar_cliente(db: Session, nome: str, email: str, telefone: str, cpf: str, endereco_id: int):
    pessoa = criar_pessoa(db, nome, email, telefone, endereco_id, 'cliente')
    
    cliente = Cliente(
        id=pessoa.id,
        cpf=cpf,
        dataCadastro=datetime.utcnow()
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def criar_funcionario(db: Session, nome: str, email: str, telefone: str, matricula: str, 
                     data_admissao: datetime, endereco_id: int):
    pessoa = criar_pessoa(db, nome, email, telefone, endereco_id, 'funcionario')
    
    funcionario = Funcionario(
        id=pessoa.id,
        matricula=matricula,
        dataAdmissao=data_admissao
    )
    db.add(funcionario)
    db.commit()
    db.refresh(funcionario)
    return funcionario

def criar_atendente(db: Session, nome: str, email: str, telefone: str, matricula: str, 
                   data_admissao: datetime, salario: float, endereco_id: int):
    funcionario = criar_funcionario(db, nome, email, telefone, matricula, data_admissao, endereco_id)
    
    atendente = Atendente(
        id=funcionario.id,
        salario=salario
    )
    db.add(atendente)
    db.commit()
    db.refresh(atendente)
    return atendente

def criar_tecnico(db: Session, nome: str, email: str, telefone: str, matricula: str, 
                 data_admissao: datetime, salario: float, especialidade: str, endereco_id: int):
    funcionario = criar_funcionario(db, nome, email, telefone, matricula, data_admissao, endereco_id)
    
    tecnico = TecnicoInformatica(
        id=funcionario.id,
        salario=salario,
        especialidade=especialidade
    )
    db.add(tecnico)
    db.commit()
    db.refresh(tecnico)
    return tecnico

def criar_dispositivo(db: Session, tipo: TipoDispositivo, marca: str, modelo: str, 
                     numero_serie: str, problema: str, cliente_id: int):
    dispositivo = Dispositivo(
        tipo=tipo,
        marca=marca,
        modelo=modelo,
        numeroSerie=numero_serie,
        problema=problema,
        cliente_id=cliente_id
    )
    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def criar_orcamento(db: Session, metodo_pagamento: MetodoPagamento, preco_total: float, 
                   dispositivo_id: int, atendente_id: int):
    orcamento = Orcamento(
        metodoPagamento=metodo_pagamento,
        precoTotal=preco_total,
        dispositivo_id=dispositivo_id,
        atendente_id=atendente_id
    )
    db.add(orcamento)
    db.commit()
    db.refresh(orcamento)
    return orcamento

def criar_ordem_servico(db: Session, dispositivo_id: int, tecnico_id: int, 
                       orcamento_id: int, data_previsao: datetime, diagnostico: str):
    ordem = OrdemServico(
        dispositivo_id=dispositivo_id,
        tecnico_id=tecnico_id,
        orcamento_id=orcamento_id,
        dataPrevisao=data_previsao,
        diagnostico=diagnostico
    )
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    return ordem

def atualizar_status_ordem(db: Session, ordem_id: int, status: StatusOrdem):
    ordem = db.query(OrdemServico).filter(OrdemServico.id == ordem_id).first()
    if ordem:
        ordem.status = status
        if status == StatusOrdem.CONCLUIDA:
            ordem.dataConclusao = datetime.utcnow()
        db.commit()
        db.refresh(ordem)
    return ordem

def criar_fornecedor(db: Session, nome: str, cnpj: str, material_fornecido: str):
    fornecedor = Fornecedor(
        nome=nome,
        cnpj=cnpj,
        material_fornecido=material_fornecido,
        dataCadastro=datetime.utcnow()
    )
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

def criar_estoque(db: Session, nome: str, descricao: str, quantidade: int, 
                 valor_unitario: float, fornecedor_id: int):
    estoque = Estoque(
        nome=nome,
        descricao=descricao,
        quantidade=quantidade,
        valorUnitario=valor_unitario,
        fornecedor_id=fornecedor_id
    )
    db.add(estoque)
    db.commit()
    db.refresh(estoque)
    return estoque

def atualizar_estoque(db: Session, item_id: int, nova_quantidade: int):
    item = db.query(Estoque).filter(Estoque.id == item_id).first()
    if item:
        item.quantidade = nova_quantidade
        db.commit()
        db.refresh(item)
    return item