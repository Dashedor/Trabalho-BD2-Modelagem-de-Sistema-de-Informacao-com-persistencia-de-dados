from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from database import Base

class TipoDispositivo(enum.Enum):
    DESKTOP = "desktop"
    NOTEBOOK = "notebook"
    TABLET = "tablet"
    SMARTPHONE = "smartphone"
    SERVIDOR = "servidor"

class StatusOrdem(enum.Enum):
    ABERTA = "aberta"
    EM_ANDAMENTO = "em_andamento"
    AGUARDANDO_PECAS = "aguardando_pecas"
    CONCLUIDA = "concluida"
    ENTREGUE = "entregue"

class MetodoPagamento(enum.Enum):
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    DINHEIRO = "dinheiro"
    PIX = "pix"
    BOLETO = "boleto"

class Endereco(Base):
    __tablename__ = "endereco"
    
    idEndereco = Column(Integer, primary_key=True, index=True)
    cep = Column(String(8), nullable=False)
    rua = Column(String(100), nullable=False)
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(2), nullable=False)
    logradouro = Column(String(100), nullable=True)

# Vamos simplificar a herança - usar tabelas separadas sem herança complexa
class Pessoa(Base):
    __tablename__ = "pessoa"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.idEndereco"))
    tipo = Column(String(20), nullable=False)  # 'cliente', 'atendente', 'tecnico'
    
    endereco = relationship("Endereco")

class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    cpf = Column(String(11), unique=True, nullable=False)
    dataCadastro = Column(DateTime, default=datetime.utcnow)
    
    pessoa = relationship("Pessoa")

class Funcionario(Base):
    __tablename__ = "funcionario"
    
    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    matricula = Column(String(20), unique=True, nullable=False)
    dataAdmissao = Column(DateTime, nullable=False)
    
    pessoa = relationship("Pessoa")

class Atendente(Base):
    __tablename__ = "atendente"
    
    id = Column(Integer, ForeignKey("funcionario.id"), primary_key=True)
    salario = Column(Float, nullable=False)
    
    funcionario = relationship("Funcionario")

class TecnicoInformatica(Base):
    __tablename__ = "tecnico_informatica"
    
    id = Column(Integer, ForeignKey("funcionario.id"), primary_key=True)
    salario = Column(Float, nullable=False)
    especialidade = Column(String(50))
    
    funcionario = relationship("Funcionario")

class Dispositivo(Base):
    __tablename__ = "dispositivo"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoDispositivo), nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    numeroSerie = Column(String(50), unique=True, nullable=True)
    problema = Column(Text)
    cliente_id = Column(Integer, ForeignKey("cliente.id"))
    
    cliente = relationship("Cliente")

class Fornecedor(Base):
    __tablename__ = "fornecedor"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    material_fornecido = Column(String(100))
    dataCadastro = Column(DateTime, default=datetime.utcnow)

class Estoque(Base):
    __tablename__ = "estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    quantidade = Column(Integer, nullable=False)
    valorUnitario = Column(Float, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedor.id"))
    
    fornecedor = relationship("Fornecedor")

class Orcamento(Base):
    __tablename__ = "orcamento"
    
    id = Column(Integer, primary_key=True, index=True)
    dataHora = Column(DateTime, default=datetime.utcnow)
    metodoPagamento = Column(Enum(MetodoPagamento))
    precoTotal = Column(Float, nullable=False)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo.id"))
    atendente_id = Column(Integer, ForeignKey("atendente.id"))
    
    dispositivo = relationship("Dispositivo")
    atendente = relationship("Atendente")

class OrdemServico(Base):
    __tablename__ = "ordem_servico"
    
    id = Column(Integer, primary_key=True, index=True)
    dataEntrada = Column(DateTime, default=datetime.utcnow)
    dataPrevisao = Column(DateTime)
    dataConclusao = Column(DateTime)
    diagnostico = Column(Text)
    status = Column(Enum(StatusOrdem), default=StatusOrdem.ABERTA)
    dispositivo_id = Column(Integer, ForeignKey("dispositivo.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnico_informatica.id"))
    orcamento_id = Column(Integer, ForeignKey("orcamento.id"))
    
    dispositivo = relationship("Dispositivo")
    tecnico = relationship("TecnicoInformatica")
    orcamento = relationship("Orcamento")

class ItemUtilizado(Base):
    __tablename__ = "item_utilizado"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    valorTotal = Column(Float, nullable=False)
    ordem_servico_id = Column(Integer, ForeignKey("ordem_servico.id"))
    estoque_id = Column(Integer, ForeignKey("estoque.id"))
    
    ordem_servico = relationship("OrdemServico")
    estoque = relationship("Estoque")