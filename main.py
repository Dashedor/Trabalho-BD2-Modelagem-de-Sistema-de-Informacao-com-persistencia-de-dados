from database import create_tables, get_db
from crud import *
from consultas import *
from tabelas import *
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inicializar_dados():
    db = next(get_db())
    
    try:
        print("🔄 Criando endereço...")
        endereco = criar_endereco(
            db=db,
            cep="65000000",
            rua="Rua das Flores",
            bairro="Centro",
            cidade="São Luís",
            estado="MA",
            logradouro="Próximo ao mercado"
        )

        print("🔄 Criando cliente...")
        cliente = criar_cliente(
            db=db,
            nome="João Silva",
            email="joao@email.com",
            telefone="98999999999",
            cpf="12345678901",
            endereco_id=endereco.idEndereco
        )

        print("🔄 Criando atendente...")
        atendente = criar_atendente(
            db=db,
            nome="Maria Santos",
            email="maria@email.com",
            telefone="98988887777",
            matricula="ATD001",
            data_admissao=datetime.utcnow(),
            salario=2500.00,
            endereco_id=endereco.idEndereco
        )

        print("🔄 Criando técnico...")
        tecnico = criar_tecnico(
            db=db,
            nome="Carlos Oliveira",
            email="carlos@email.com",
            telefone="98977776666",
            matricula="TEC001",
            data_admissao=datetime.utcnow(),
            salario=3500.00,
            especialidade="Hardware",
            endereco_id=endereco.idEndereco
        )

        print("🔄 Criando dispositivo...")
        dispositivo = criar_dispositivo(
            db=db,
            tipo=TipoDispositivo.NOTEBOOK,
            marca="Dell",
            modelo="Inspiron 15",
            numero_serie="DEL123456",
            problema="Não liga",
            cliente_id=cliente.id
        )

        print("🔄 Criando orçamento...")
        orcamento = criar_orcamento(
            db=db,
            metodo_pagamento=MetodoPagamento.CARTAO_CREDITO,
            preco_total=350.50,
            dispositivo_id=dispositivo.id,
            atendente_id=atendente.id
        )

        print("🔄 Criando ordem de serviço...")
        ordem = criar_ordem_servico(
            db=db,
            dispositivo_id=dispositivo.id,
            tecnico_id=tecnico.id,
            orcamento_id=orcamento.id,
            data_previsao=datetime.utcnow() + timedelta(days=7),
            diagnostico="Problema na fonte de alimentação"
        )

        print("🔄 Criando fornecedores...")
        fornecedor1 = Fornecedor(
            nome="TechParts Ltda",
            cnpj="12345678000195",
            material_fornecido="Componentes de hardware",
            dataCadastro=datetime.utcnow()
        )
        db.add(fornecedor1)
        
        fornecedor2 = Fornecedor(
            nome="EletroMega Distribuidora",
            cnpj="98765432000186",
            material_fornecido="Peças e acessórios",
            dataCadastro=datetime.utcnow()
        )
        db.add(fornecedor2)
        db.commit()
        db.refresh(fornecedor1)
        db.refresh(fornecedor2)

        print("🔄 Criando itens no estoque...")
        estoque1 = Estoque(
            nome="Fonte de Alimentação 500W",
            descricao="Fonte ATX 500W 80 Plus Bronze",
            quantidade=15,
            valorUnitario=189.90,
            fornecedor_id=fornecedor1.id
        )
        db.add(estoque1)
        
        estoque2 = Estoque(
            nome="Memória RAM 8GB DDR4",
            descricao="Memória Kingston 8GB 2666MHz",
            quantidade=25,
            valorUnitario=199.90,
            fornecedor_id=fornecedor1.id
        )
        db.add(estoque2)
        
        estoque3 = Estoque(
            nome="SSD 240GB SATA",
            descricao="SSD Kingston A400 240GB",
            quantidade=3,  # Estoque baixo
            valorUnitario=159.90,
            fornecedor_id=fornecedor1.id
        )
        db.add(estoque3)
        
        estoque4 = Estoque(
            nome="Teclado Mecânico",
            descricao="Teclado Redragon Kumara",
            quantidade=2,  # Estoque baixo
            valorUnitario=249.90,
            fornecedor_id=fornecedor2.id
        )
        db.add(estoque4)
        
        estoque5 = Estoque(
            nome="Mouse Gamer",
            descricao="Mouse Redragon Cobra",
            quantidade=0,  # Estoque zerado
            valorUnitario=89.90,
            fornecedor_id=fornecedor2.id
        )
        db.add(estoque5)
        
        db.commit()

        logger.info("✅ Dados iniciais criados com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar dados iniciais: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

def demonstrar_consultas():
    db = next(get_db())
    
    try:
        print("\n" + "="*50)
        print("CONSULTAS COMPLEXAS")
        print("="*50)
        
        print("\n1. Ordens em andamento:")
        ordens = consulta_ordens_em_andamento(db)
        if ordens:
            for ordem in ordens:
                print(f"  Ordem {ordem.id}: {ordem.nome_cliente} - {ordem.marca} {ordem.modelo} - {ordem.status}")
        else:
            print("  Nenhuma ordem em andamento")
        
        print("\n2. Estoque baixo (≤ 5 unidades):")
        estoque_baixo = consulta_estoque_baixo(db, limite=5)
        if estoque_baixo:
            print(f"  ⚠️  {len(estoque_baixo)} itens com estoque baixo:")
            for item in estoque_baixo:
                status = "⛔ ESGOTADO" if item.quantidade == 0 else "⚠️  BAIXO"
                print(f"  {status} {item.nome}: {item.quantidade} unidades - R$ {item.valorUnitario:.2f} - Fornecedor: {item.fornecedor}")
        else:
            print("  ✅ Estoque normal")
        
        print("\n3. Estoque zerado:")
        estoque_zerado = consulta_estoque_zerado(db)
        if estoque_zerado:
            print(f"  ⛔ {len(estoque_zerado)} itens esgotados:")
            for item in estoque_zerado:
                print(f"  {item.nome}: {item.quantidade} unidades - Fornecedor: {item.fornecedor}")
        else:
            print("  ✅ Nenhum item esgotado")

        print("\n4. Resumo completo do estoque:")
        estoque_total = consulta_estoque_total(db)
        if estoque_total:
            print(f"  📦 Total de {len(estoque_total)} itens no estoque:")
            for item in estoque_total:
                status = "⛔" if item.quantidade == 0 else "⚠️ " if item.quantidade <= 5 else "✅"
                print(f"  {status} {item.nome}: {item.quantidade} unidades - R$ {item.valorUnitario:.2f}")
        else:
            print("  Nenhum item no estoque")
        
        print("\n5. Valor total do estoque:")
        valor_total = consulta_valor_total_estoque(db)
        print(f"  💰 Valor total em estoque: R$ {valor_total:.2f}")
        
        print("\n6. Técnicos mais produtivos:")
        tecnicos = consulta_tecnicos_mais_produtivos(db)
        if tecnicos:
            for tecnico in tecnicos:
                print(f"  {tecnico.nome}: {tecnico.ordens_concluidas} ordens concluídas")
        else:
            print("  Nenhum técnico com ordens concluídas")
        
        print("\n7. Clientes fiéis:")
        clientes = consulta_clientes_fieis(db)
        if clientes:
            for cliente in clientes:
                print(f"  {cliente.nome}: {cliente.total_dispositivos} dispositivos")
        else:
            print("  Nenhum cliente com dispositivos cadastrados")
            
            
    except Exception as e:
        logger.error(f"❌ Erro nas consultas: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    try:
        print("🔄 Criando tabelas...")
        create_tables()
        
        print("🔄 Inicializando dados...")
        inicializar_dados()
        
        print("🔄 Executando consultas...")
        demonstrar_consultas()
        
        print("\n✅ Sistema executado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")