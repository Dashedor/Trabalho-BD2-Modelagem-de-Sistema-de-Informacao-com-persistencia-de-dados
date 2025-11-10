from database import create_tables, get_db
from consultas import *
from tabelas import *
from crud import *
from datetime import datetime

class Menu:
    def __init__(self):
        self.db = next(get_db())

    def pausar(self):
        input("\nPressione Enter para continuar...")

    def mostrar(self,titulo):
        print("=" * 50)
        print(titulo)
        print("=" * 50)

    def inicializar_dados(self):
        self.mostrar("Inicializar Dados")

        try:
            print("Esta operação irá criar dados de exemplo no banco.")
            confirmacao = input("Deseja continuar? (s/n): ")
            
            if confirmacao.lower() != 's':
                print("Operação cancelada.")
                self.pausar()
                return
            
            print("\nCriando dados de exemplo...")
            
            endereco = criar_endereco(
                self.db, "65000000", "Rua das Flores", "Centro", 
                "São Luís", "MA"
            )
            
            cliente = criar_cliente(
                self.db, "João Silva", "joao@email.com", 
                "98999999999", "12345678901", endereco.idEndereco
            )
            
            atendente = criar_atendente(
                self.db, "Maria Santos", "maria@email.com", 
                "98988887777", "ATD001",  
                2500.00, endereco.idEndereco
            )
            
            tecnico = criar_tecnico(
                self.db, "Carlos Oliveira", "carlos@email.com", 
                "98977776666", "TEC001", 
                3500.00, "Hardware", endereco.idEndereco
            )
            
            dispositivo = criar_dispositivo(
                self.db, TipoDispositivo.NOTEBOOK, "Dell", 
                "Inspiron 15", "DEL123456", "Não liga", cliente.id
            )
            
            orcamento = criar_orcamento(
                self.db, MetodoPagamento.CARTAO_CREDITO, 350.50,
                dispositivo.id, atendente.id
            )
            
            ordem = criar_ordem_servico(
                self.db, dispositivo.id, tecnico.id, orcamento.id, data_previsao=datetime.utcnow(), diagnostico="Problema na fonte de alimentação"
            )
            
            fornecedor = Fornecedor(
                nome="TechParts Ltda",
                cnpj="12345678000195",
                material_fornecido="Componentes de hardware"
            )
            self.db.add(fornecedor)
            self.db.commit()
            self.db.refresh(fornecedor)
            
            itens_estoque = [
                {"nome": "Fonte de Alimentação 500W", "descricao": "Fonte ATX 500W", "quantidade": 15, "valor": 189.90},
                {"nome": "Memória RAM 8GB DDR4", "descricao": "Memória Kingston", "quantidade": 25, "valor": 199.90},
                {"nome": "SSD 240GB SATA", "descricao": "SSD Kingston A400", "quantidade": 3, "valor": 159.90},
                {"nome": "Teclado Mecânico", "descricao": "Teclado Redragon", "quantidade": 2, "valor": 249.90},
                {"nome": "Mouse Gamer", "descricao": "Mouse Redragon Cobra", "quantidade": 0, "valor": 89.90},
            ]
            
            for item in itens_estoque:
                estoque_item = criar_estoque(
                    self.db, item["nome"], item["descricao"], 
                    item["quantidade"], item["valor"], fornecedor.id
                )
            
            print(" Dados criados com sucesso!")
            print("\nDados criados:")
            print("- 1 Cliente: João Silva")
            print("- 1 Atendente: Maria Santos") 
            print("- 1 Técnico: Carlos Oliveira")
            print("- 1 Dispositivo: Dell Inspiron 15")
            print("- 1 Ordem de serviço")
            print("- 1 Fornecedor")
            print("- 5 Itens no estoque")
            
        except Exception as e:
            print(f"Erro ao criar dados de exemplo: {e}")
            self.db.rollback()

        self.pausar()
        
    def verificar_dados_existentes(self):
        try:
            result = self.db.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'cliente'
                )
            """)
            tabela_existe = result.scalar()
            
            if not tabela_existe:
                return False
                
            total_clientes = self.db.query(Cliente).count()
            return total_clientes() > 0
            
        except Exception:
            return False
    
    def menu_principal(self):
        while True:
            self.mostrar("SISTEMA ASSISTÊNCIA TÉCNICA")
        
            try:
                tem_dados = self.verificar_dados_existentes()
                if not tem_dados:
                    print("💡 Use a opção 6 para criar dados de exemplo.")
                    print("=" * 50)
            except Exception:
                pass

            print("1. Criar Objetos")
            print("2. Listar Objetos") 
            print("3. Atualizar Objetos")
            print("4. Deletar Objetos")
            print("5. Consultas")
            print("6. Inicializar Dados de Exemplo")
            print("0. Sair")
            print("=" * 50)

            opcao = input(" Escolha uma opção: ")

            if opcao == "1":
                self.menu_criar()
            elif opcao == "2":
                self.menu_listar()
            elif opcao == "3":
                self.menu_atualizar()
            elif opcao == "4":
                self.menu_deletar()
            elif opcao == "5":
                self.menu_consultas()
            elif opcao == "6":
                self.inicializar_dados()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")
                self.pausar()
            
    def menu_criar(self):
        while True:
            self.mostrar("Criar objetos")
            print("1. Criar Cliente")
            print("2. Criar Dispositivo")
            print("3. Criar Ordem de Serviço")
            print("4. Criar Item no Estoque")
            print("0. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.criar_cliente_menu()
            elif opcao == "2":
                self.criar_dispositivo_menu()
            elif opcao == "3":
                self.criar_ordem_servico_menu()
            elif opcao == "4":
                self.criar_estoque_menu()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.pausar()

    def criar_cliente_menu(self):
        self.mostrar("Cria Cliente")

        try:
            print("\n--- Dados do Endereço ---")
            cep = input("CEP: ")
            rua = input("Rua: ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            
            endereco = criar_endereco(self.db, cep, rua, bairro, cidade, estado)
            
            print("\n--- Dados do Cliente ---")
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            cpf = input("CPF: ")
            
            cliente = criar_cliente(self.db, nome, email, telefone, cpf, endereco.idEndereco)
            print(f"Cliente {nome} criado com ID: {cliente.id}")
            
        except Exception as e:
            print(f"Erro: {e}")
        
        self.pausar()

    def criar_dispositivo_menu(self):
        self.mostrar("CRIAR DISPOSITIVO")
        
        try:
            clientes = self.db.query(Cliente).join(Pessoa).all()
            if not clientes:
                print(" Nenhum cliente cadastrado.")
                self.pausar()
                return
            
            print("Clientes disponíveis:")
            for i, cliente in enumerate(clientes, 1):
                print(f"{i}. {cliente.pessoa.nome}")
            
            idx = int(input("Selecione o cliente: ")) - 1
            if idx < 0 or idx >= len(clientes):
                print(" Seleção inválida.")
                self.pausar()
                return
            
            cliente_selecionado = clientes[idx]
            
            print("\nTipos: DESKTOP, NOTEBOOK, TABLET, SMARTPHONE, SERVIDOR")
            tipo = input("Tipo: ").upper()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            numero_serie = input("Número de série: ")
            problema = input("Problema: ")
            
            dispositivo = criar_dispositivo(
                self.db, TipoDispositivo[tipo], marca, modelo, 
                numero_serie, problema, cliente_selecionado.id
            )
            print(f" Dispositivo {marca} {modelo} criado!")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def criar_ordem_servico_menu(self):
        self.mostrar("CRIAR ORDEM DE SERVIÇO")
        
        try:
            dispositivos = self.db.query(Dispositivo).all()
            if not dispositivos:
                print(" Nenhum dispositivo cadastrado.")
                self.pausar()
                return
            
            print("Dispositivos disponíveis:")
            for i, dispositivo in enumerate(dispositivos, 1):
                print(f"{i}. {dispositivo.marca} {dispositivo.modelo} - {dispositivo.cliente.pessoa.nome}")
            
            disp_idx = int(input("Selecione o dispositivo: ")) - 1
            if disp_idx < 0 or disp_idx >= len(dispositivos):
                print(" Seleção inválida.")
                self.pausar()
                return
            
            dispositivo_selecionado = dispositivos[disp_idx]
            
            tecnicos = self.db.query(TecnicoInformatica).join(Funcionario).join(Pessoa).all()
            if not tecnicos:
                print(" Nenhum técnico cadastrado.")
                self.pausar()
                return
            
            print("\nTécnicos disponíveis:")
            for i, tecnico in enumerate(tecnicos, 1):
                print(f"{i}. {tecnico.funcionario.pessoa.nome}")
            
            tec_idx = int(input("Selecione o técnico: ")) - 1
            if tec_idx < 0 or tec_idx >= len(tecnicos):
                print(" Seleção inválida.")
                self.pausar()
                return
            
            tecnico_selecionado = tecnicos[tec_idx]
            
            atendentes = self.db.query(Atendente).join(Funcionario).join(Pessoa).all()
            if not atendentes:
                print(" Nenhum atendente cadastrado.")
                self.pausar()
                return
            
            print("\nAtendentes disponíveis:")
            for i, atendente in enumerate(atendentes, 1):
                print(f"{i}. {atendente.funcionario.pessoa.nome}")
            
            atd_idx = int(input("Selecione o atendente: ")) - 1
            if atd_idx < 0 or atd_idx >= len(atendentes):
                print(" Seleção inválida.")
                self.pausar()
                return
            
            atendente_selecionado = atendentes[atd_idx]
            
            diagnostico = input("Diagnóstico: ")
            preco_total = float(input("Preço total do orçamento: "))
            data_previsao = datetime.now()
            
            orcamento = criar_orcamento(
                self.db, MetodoPagamento.DINHEIRO, preco_total,
                dispositivo_selecionado.id, atendente_selecionado.id
            )
            

            ordem = criar_ordem_servico(
                self.db, dispositivo_selecionado.id, 
                tecnico_selecionado.id, orcamento.id, data_previsao, diagnostico
            )
            print(f" Ordem de serviço #{ordem.id} criada!")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def criar_estoque_menu(self):
        self.mostrar("CRIAR ITEM NO ESTOQUE")
        
        try:
            fornecedor = self.db.query(Fornecedor).first()
            if not fornecedor:
                print(" Nenhum fornecedor cadastrado. Criando fornecedor padrão...")
                fornecedor = criar_fornecedor(
                    self.db, "Fornecedor Padrão", "00000000000191", "Diversos"
                )
                print(" Fornecedor padrão criado.")
            
            nome = input("Nome do item: ")
            descricao = input("Descrição: ")
            quantidade = int(input("Quantidade: "))
            valor_unitario = float(input("Valor unitário: "))
            
            item = criar_estoque(
                self.db, nome, descricao, quantidade, valor_unitario, fornecedor.id
            )
            print(f" Item {nome} adicionado ao estoque!")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def menu_listar(self):
        while True:
            self.mostrar("LISTAR OBJETOS")
            print("1. Listar Clientes")
            print("2. Listar Dispositivos")
            print("3. Listar Ordens de Serviço")
            print("4. Listar Estoque")
            print("5. Listar Funcionários")
            print("0. Voltar")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.listar_clientes()
            elif opcao == "2":
                self.listar_dispositivos()
            elif opcao == "3":
                self.listar_ordens()
            elif opcao == "4":
                self.listar_estoque()
            elif opcao == "5":
                self.listar_funcionarios()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.pausar()
    
    def listar_clientes(self):
        self.mostrar("LISTA DE CLIENTES")
        
        clientes = self.db.query(Cliente).join(Pessoa).all()
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"ID: {cliente.id} | Nome: {cliente.pessoa.nome} | CPF: {cliente.cpf}")
                print(f"Email: {cliente.pessoa.email} | Telefone: {cliente.pessoa.telefone}")
                print("-" * 40)
        
        self.pausar()
    
    def listar_funcionarios(self):
        self.mostrar("LISTA DE FUNCIONÁRIOS")
        
        funcionarios = self.db.query(Funcionario).join(Pessoa).all()
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
        else:
            for func in funcionarios:
                atendente = self.db.query(Atendente).filter(Atendente.id == func.id).first()
                tecnico = self.db.query(TecnicoInformatica).filter(TecnicoInformatica.id == func.id).first()
                
                cargo = "Técnico" if tecnico else "Atendente" if atendente else "Funcionário"
                
                print(f"ID: {func.id} | Nome: {func.pessoa.nome} | Cargo: {cargo}")
                print(f"Matrícula: {func.matricula} | Email: {func.pessoa.email}")
                print("-" * 40)
        
        self.pausar()
    
    def listar_dispositivos(self):
        self.mostrar("LISTA DE DISPOSITIVOS")
        
        dispositivos = self.db.query(Dispositivo).join(Cliente).join(Pessoa).all()
        if not dispositivos:
            print("Nenhum dispositivo cadastrado.")
        else:
            for dispositivo in dispositivos:
                print(f"ID: {dispositivo.id} | {dispositivo.marca} {dispositivo.modelo}")
                print(f"Tipo: {dispositivo.tipo.value} | Cliente: {dispositivo.cliente.pessoa.nome}")
                print(f"Problema: {dispositivo.problema}")
                print("-" * 40)
        
        self.pausar()
    
    def listar_ordens(self):
        self.mostrar("LISTA DE ORDENS DE SERVIÇO")
        
        ordens = self.db.query(OrdemServico).all()
        if not ordens:
            print("Nenhuma ordem de serviço.")
        else:
            for ordem in ordens:
                print(f"ID: {ordem.id} | Status: {ordem.status.value}")
                print(f"Dispositivo: {ordem.dispositivo.marca} {ordem.dispositivo.modelo}")
                print(f"Técnico: {ordem.tecnico.funcionario.pessoa.nome}")
                print(f"Entrada: {ordem.dataEntrada.strftime('%d/%m/%Y')}")
                print("-" * 40)
        
        self.pausar()
    
    def listar_estoque(self):
        self.mostrar("LISTA DE ESTOQUE")
        
        estoque = self.db.query(Estoque).all()
        if not estoque:
            print("Estoque vazio.")
        else:
            for item in estoque:
                status = "ESGOTADO" if item.quantidade == 0 else "BAIXO" if item.quantidade <= 5 else "OK"
                print(f"ID: {item.id} | {item.nome} | Qtd: {item.quantidade} ({status})")
                print(f"Valor: R$ {item.valorUnitario:.2f}")
                print("-" * 40)
        
        self.pausar()
    
    def menu_atualizar(self):
        while True:
            self.mostrar("ATUALIZAR OBJETOS")
            print("1. Atualizar Status da Ordem")
            print("2. Atualizar Quantidade no Estoque")
            print("0. Voltar")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.atualizar_status_ordem_menu()
            elif opcao == "2":
                self.atualizar_quantidade_estoque_menu()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.pausar()
    
    def atualizar_status_ordem_menu(self):
        self.mostrar("ATUALIZAR STATUS DA ORDEM")
        
        try:
            ordens = self.db.query(OrdemServico).all()
            if not ordens:
                print("Nenhuma ordem de serviço.")
                self.pausar()
                return
            
            print("Ordens disponíveis:")
            for i, ordem in enumerate(ordens, 1):
                print(f"{i}. Ordem #{ordem.id} - {ordem.dispositivo.marca} {ordem.dispositivo.modelo} - Status: {ordem.status.value}")
            
            idx = int(input("Selecione a ordem: ")) - 1
            if idx < 0 or idx >= len(ordens):
                print("Seleção inválida.")
                self.pausar()
                return
            
            ordem_selecionada = ordens[idx]
            
            print("\nStatus disponíveis:")
            status_list = list(StatusOrdem)
            for i, status in enumerate(status_list, 1):
                print(f"{i}. {status.value}")
            
            status_idx = int(input("Selecione o novo status: ")) - 1
            if status_idx < 0 or status_idx >= len(status_list):
                print("Seleção inválida.")
                self.pausar()
                return
            
            novo_status = status_list[status_idx]
            
            ordem_atualizada = atualizar_status_ordem(self.db, ordem_selecionada.id, novo_status)
            print(f" Status da ordem #{ordem_atualizada.id} atualizado para: {ordem_atualizada.status.value}")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def atualizar_quantidade_estoque_menu(self):
        self.mostrar("ATUALIZAR QUANTIDADE NO ESTOQUE")
        
        try:
            estoque = self.db.query(Estoque).all()
            if not estoque:
                print("Estoque vazio.")
                self.pausar()
                return
            
            print("Itens disponíveis:")
            for i, item in enumerate(estoque, 1):
                print(f"{i}. {item.nome} - Quantidade atual: {item.quantidade}")
            
            idx = int(input("Selecione o item: ")) - 1
            if idx < 0 or idx >= len(estoque):
                print("Seleção inválida.")
                self.pausar()
                return
            
            item_selecionado = estoque[idx]
            nova_quantidade = int(input(f"Nova quantidade para '{item_selecionado.nome}': "))
            
            item_atualizado = atualizar_estoque(self.db, item_selecionado.id, nova_quantidade)
            print(f" Quantidade de '{item_atualizado.nome}' atualizada para: {item_atualizado.quantidade}")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def menu_deletar(self):
        while True:
            self.mostrar("DELETAR OBJETOS")
            print("1. Deletar Cliente")
            print("2. Deletar Dispositivo")
            print("0. Voltar")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.deletar_cliente_menu()
            elif opcao == "2":
                self.deletar_dispositivo_menu()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.pausar()
    
    def deletar_cliente_menu(self):
        self.mostrar("DELETAR CLIENTE")
        
        try:
            clientes = self.db.query(Cliente).join(Pessoa).all()
            if not clientes:
                print("Nenhum cliente cadastrado.")
                self.pausar()
                return
            
            print("Clientes disponíveis:")
            for i, cliente in enumerate(clientes, 1):
                print(f"{i}. {cliente.pessoa.nome} - CPF: {cliente.cpf}")
            
            idx = int(input("Selecione o cliente para deletar: ")) - 1
            if idx < 0 or idx >= len(clientes):
                print("Seleção inválida.")
                self.pausar()
                return
            
            cliente_selecionado = clientes[idx]
            confirmacao = input(f"Tem certeza que deseja deletar {cliente_selecionado.pessoa.nome}? (s/n): ")
            
            if confirmacao.lower() == 's':
                if deletar_cliente(self.db, cliente_selecionado.id):
                    print(" Cliente deletado com sucesso!")
                else:
                    print(" Erro ao deletar cliente.")
            else:
                print("Operação cancelada.")
                
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def deletar_dispositivo_menu(self):
        self.mostrar("DELETAR DISPOSITIVO")
        
        try:
            dispositivos = self.db.query(Dispositivo).all()
            if not dispositivos:
                print("Nenhum dispositivo cadastrado.")
                self.pausar()
                return
            
            print("Dispositivos disponíveis:")
            for i, dispositivo in enumerate(dispositivos, 1):
                print(f"{i}. {dispositivo.marca} {dispositivo.modelo} - {dispositivo.cliente.pessoa.nome}")
            
            idx = int(input("Selecione o dispositivo para deletar: ")) - 1
            if idx < 0 or idx >= len(dispositivos):
                print("Seleção inválida.")
                self.pausar()
                return
            
            dispositivo_selecionado = dispositivos[idx]
            confirmacao = input(f"Tem certeza que deseja deletar {dispositivo_selecionado.marca} {dispositivo_selecionado.modelo}? (s/n): ")
            
            if confirmacao.lower() == 's':
                if deletar_dispositivo(self.db, dispositivo_selecionado.id):
                    print(" Dispositivo deletado com sucesso!")
                else:
                    print("Erro ao deletar dispositivo.")
            else:
                print("Operação cancelada.")
                
        except Exception as e:
            print(f"Erro: {e}")
        
        self.pausar()

    def menu_consultas(self):
        while True:
            self.mostrar("CONSULTAS")
            print("1. Ordens em Andamento")
            print("2. Estoque Baixo")
            print("3. Técnicos Mais Produtivos")
            print("4. Clientes com Mais Dispositivos")
            print("5. Relatório Completo")
            print("0. Voltar")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.consulta_ordens_andamento_menu()
            elif opcao == "2":
                self.consulta_estoque_baixo_menu()
            elif opcao == "3":
                self.consulta_tecnicos_produtivos_menu()
            elif opcao == "4":
                self.consulta_clientes_fieis_menu()
            elif opcao == "5":
                self.relatorio_completo_menu()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.pausar()
    
    def consulta_ordens_andamento_menu(self):
        self.mostrar("ORDENS EM ANDAMENTO")
        
        try:
            # Usar função do queries.py
            ordens = consulta_ordens_em_andamento(self.db)
            if not ordens:
                print("Nenhuma ordem em andamento.")
            else:
                for ordem in ordens:
                    print(f"Ordem #{ordem.id}: {ordem.nome_cliente} - {ordem.marca} {ordem.modelo}")
                    print(f"Status: {ordem.status} | Previsão: {ordem.dataPrevisao.strftime('%d/%m/%Y')}")
                    print("-" * 40)
                    
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def consulta_estoque_baixo_menu(self):
        self.mostrar("ESTOQUE BAIXO")
        
        try:
            estoque_baixo = consulta_estoque_baixo(self.db, limite=5)
            if not estoque_baixo:
                print("Nenhum item com estoque baixo.")
            else:
                for item in estoque_baixo:
                    print(f"{item.nome}: {item.quantidade} unidades")
                    print(f"Valor: R$ {item.valorUnitario:.2f} | Fornecedor: {item.fornecedor}")
                    print("-" * 40)
                    
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def consulta_tecnicos_produtivos_menu(self):
        self.mostrar("TÉCNICOS MAIS PRODUTIVOS")
        
        try:
            tecnicos = consulta_tecnicos_mais_produtivos(self.db)
            if not tecnicos:
                print("Nenhum técnico com ordens concluídas.")
            else:
                for i, tecnico in enumerate(tecnicos, 1):
                    print(f"{i}. {tecnico.nome}: {tecnico.ordens_concluidas} ordens")
                    
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def consulta_clientes_fieis_menu(self):
        self.mostrar("CLIENTES COM MAIS DISPOSITIVOS")
        
        try:
            clientes = consulta_clientes_fieis(self.db)
            if not clientes:
                print("Nenhum cliente com dispositivos.")
            else:
                for i, cliente in enumerate(clientes, 1):
                    print(f"{i}. {cliente.nome}: {cliente.total_dispositivos} dispositivos")
                    
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()
    
    def relatorio_completo_menu(self):
        self.mostrar("RELATÓRIO COMPLETO")
        
        try:
            total_clientes = self.db.query(Cliente).count()
            total_dispositivos = self.db.query(Dispositivo).count()
            total_ordens = self.db.query(OrdemServico).count()
            total_estoque = self.db.query(Estoque).count()
            total_funcionarios = self.db.query(Funcionario).count()
            
            print("=== ESTATÍSTICAS GERAIS ===")
            print(f" Clientes: {total_clientes}")
            print(f" Funcionários: {total_funcionarios}")
            print(f" Dispositivos: {total_dispositivos}")
            print(f" Ordens de serviço: {total_ordens}")
            print(f" Itens no estoque: {total_estoque}")
            
            valor_total = consulta_valor_total_estoque(self.db)
            print(f" Valor total em estoque: R$ {valor_total:.2f}")
            
            print("\n=== STATUS DAS ORDENS ===")
            status_ordens = self.db.query(
                OrdemServico.status, 
                func.count(OrdemServico.id)
            ).group_by(OrdemServico.status).all()
            
            for status, count in status_ordens:
                print(f"{status.value}: {count} ordens")
            
        except Exception as e:
            print(f" Erro: {e}")
        
        self.pausar()

def main():
    try:
        menu = Menu()
        menu.menu_principal()
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    create_tables()
    main()