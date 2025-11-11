from database import get_db
from crud import *
from tabelas import *
from datetime import datetime, timedelta
import random

def criar_dados():
    db = next(get_db())
    
    try:
        print("Criando dados de exemplo completos...")
        
        enderecos = [
            {
                "cep": "65000000", "rua": "Rua das Flores", "bairro": "Centro",
                "cidade": "São Luís", "estado": "MA", "logradouro": "Próximo ao mercado"
            },
            {
                "cep": "68503150", "rua": "Avenida Brasil", "bairro": "Nova Marabá",
                "cidade": "Marabá", "estado": "PA", "logradouro": "Ao lado do shopping"
            },
            {
                "cep": "76804234", "rua": "Rua das Palmeiras", "bairro": "Industrial",
                "cidade": "Porto Velho", "estado": "RO", "logradouro": "Próximo à fábrica"
            },
            {
                "cep": "69900000", "rua": "Travessa da Paz", "bairro": "Bosque",
                "cidade": "Rio Branco", "estado": "AC", "logradouro": "Em frente à praça"
            },
            {
                "cep": "77000000", "rua": "Alameda dos Anjos", "bairro": "Plano Diretor",
                "cidade": "Palmas", "estado": "TO", "logradouro": "Condomínio Solar"
            }
        ]
        
        enderecos_criados = []
        for endereco_data in enderecos:
            endereco = criar_endereco(
                db, endereco_data["cep"], endereco_data["rua"], 
                endereco_data["bairro"], endereco_data["cidade"], 
                endereco_data["estado"], endereco_data["logradouro"]
            )
            enderecos_criados.append(endereco)
            print(f"Endereço: {endereco_data['rua']}, {endereco_data['cidade']}")
        
        print("Criando clientes...")
        clientes_data = [
            {"nome": "João Silva", "email": "joao.silva@email.com", "telefone": "98999999999", "cpf": "12345678901"},
            {"nome": "Maria Santos", "email": "maria.santos@email.com", "telefone": "98988887777", "cpf": "98765432100"},
            {"nome": "Carlos Oliveira", "email": "carlos.oliveira@email.com", "telefone": "98977776666", "cpf": "45678912345"},
            {"nome": "Ana Pereira", "email": "ana.pereira@email.com", "telefone": "98966665555", "cpf": "32165498700"},
            {"nome": "Pedro Costa", "email": "pedro.costa@email.com", "telefone": "98955554444", "cpf": "65412398700"}
        ]
        
        clientes_criados = []
        for i, cliente_data in enumerate(clientes_data):
            cliente = criar_cliente(
                db, cliente_data["nome"], cliente_data["email"], 
                cliente_data["telefone"], cliente_data["cpf"], 
                enderecos_criados[i % len(enderecos_criados)].idEndereco
            )
            clientes_criados.append(cliente)
            print(f"Cliente: {cliente_data['nome']}")
        
        print("Criando funcionários...")
        
        atendentes_data = [
            {"nome": "Fernanda Lima", "email": "fernanda.lima@empresa.com", "telefone": "98944443333", "matricula": "ATD001", "salario": 2500.00},
            {"nome": "Ricardo Alves", "email": "ricardo.alves@empresa.com", "telefone": "98933332222", "matricula": "ATD002", "salario": 2700.00}
        ]
        
        atendentes_criados = []
        for atendente_data in atendentes_data:
            atendente = criar_atendente(
                db, atendente_data["nome"], atendente_data["email"], 
                atendente_data["telefone"], atendente_data["matricula"], 
                atendente_data["salario"], enderecos_criados[0].idEndereco
            )
            atendentes_criados.append(atendente)
            print(f"Atendente: {atendente_data['nome']}")
        
        tecnicos_data = [
            {"nome": "Bruno Souza", "email": "bruno.souza@empresa.com", "telefone": "98922221111", "matricula": "TEC001", "salario": 3500.00, "especialidade": "Hardware"},
            {"nome": "Juliana Martins", "email": "juliana.martins@empresa.com", "telefone": "98911110000", "matricula": "TEC002", "salario": 3800.00, "especialidade": "Software"},
            {"nome": "Lucas Ferreira", "email": "lucas.ferreira@empresa.com", "telefone": "98900009999", "matricula": "TEC003", "salario": 3200.00, "especialidade": "Redes"},
            {"nome": "Patrícia Rocha", "email": "patricia.rocha@empresa.com", "telefone": "98999998888", "matricula": "TEC004", "salario": 4000.00, "especialidade": "Segurança"}
        ]
        
        tecnicos_criados = []
        for tecnico_data in tecnicos_data:
            tecnico = criar_tecnico(
                db, tecnico_data["nome"], tecnico_data["email"], 
                tecnico_data["telefone"], tecnico_data["matricula"],  tecnico_data["salario"], 
                tecnico_data["especialidade"], enderecos_criados[0].idEndereco
            )
            tecnicos_criados.append(tecnico)
            print(f"Tecnico: {tecnico_data['nome']} - {tecnico_data['especialidade']}")
        
        print("Criando dispositivos...")
        dispositivos_data = [
            {"tipo": TipoDispositivo.NOTEBOOK, "marca": "Dell", "modelo": "Inspiron 15", "numero_serie": "DEL123456", "problema": "Não liga"},
            {"tipo": TipoDispositivo.SMARTPHONE, "marca": "Samsung", "modelo": "Galaxy S21", "numero_serie": "SAM789012", "problema": "Tela quebrada"},
            {"tipo": TipoDispositivo.DESKTOP, "marca": "HP", "modelo": "Pavilion", "numero_serie": "HP345678", "problema": "Lentidão extrema"},
            {"tipo": TipoDispositivo.TABLET, "marca": "Apple", "modelo": "iPad Air", "numero_serie": "APP901234", "problema": "Bateria não carrega"},
            
            {"tipo": TipoDispositivo.NOTEBOOK, "marca": "Lenovo", "modelo": "ThinkPad", "numero_serie": "LEN567890", "problema": "Teclado não funciona"},
            {"tipo": TipoDispositivo.SMARTPHONE, "marca": "Apple", "modelo": "iPhone 13", "numero_serie": "APP345678", "problema": "Câmera traseira"},
            {"tipo": TipoDispositivo.DESKTOP, "marca": "Acer", "modelo": "Aspire", "numero_serie": "ACE123456", "problema": "Não conecta à internet"},
            {"tipo": TipoDispositivo.SERVIDOR, "marca": "Dell", "modelo": "PowerEdge", "numero_serie": "DEL789012", "problema": "Superaquecimento"},
            
            {"tipo": TipoDispositivo.NOTEBOOK, "marca": "Apple", "modelo": "MacBook Pro", "numero_serie": "APP567890", "problema": "SSD corrompido"},
            {"tipo": TipoDispositivo.SMARTPHONE, "marca": "Xiaomi", "modelo": "Redmi Note 10", "numero_serie": "XIA123456", "problema": "Audio não funciona"},
            {"tipo": TipoDispositivo.DESKTOP, "marca": "Positivo", "modelo": "Master", "numero_serie": "POS789012", "problema": "Placa de vídeo queimada"},
            {"tipo": TipoDispositivo.TABLET, "marca": "Samsung", "modelo": "Galaxy Tab S7", "numero_serie": "SAM345678", "problema": "WiFi instável"},
            
            {"tipo": TipoDispositivo.NOTEBOOK, "marca": "Asus", "modelo": "VivoBook", "numero_serie": "ASU901234", "problema": "Tela azul"},
            {"tipo": TipoDispositivo.SMARTPHONE, "marca": "Motorola", "modelo": "Moto G100", "numero_serie": "MOT567890", "problema": "Microfone não funciona"},
            {"tipo": TipoDispositivo.DESKTOP, "marca": "CCE", "modelo": "Expert", "numero_serie": "CCE123456", "problema": "Fonte queimada"},
            {"tipo": TipoDispositivo.SERVIDOR, "marca": "HP", "modelo": "ProLiant", "numero_serie": "HP789012", "problema": "RAID corrompido"},
            
            {"tipo": TipoDispositivo.NOTEBOOK, "marca": "LG", "modelo": "Gram", "numero_serie": "LG345678", "problema": "Bateria inchada"},
            {"tipo": TipoDispositivo.SMARTPHONE, "marca": "Nokia", "modelo": "G50", "numero_serie": "NOK901234", "problema": "Não reconhece SIM"},
            {"tipo": TipoDispositivo.DESKTOP, "marca": "Itautec", "modelo": "Infoway", "numero_serie": "ITA567890", "problema": "Memória RAM defeituosa"},
            {"tipo": TipoDispositivo.TABLET, "marca": "Multilaser", "modelo": "Pro", "numero_serie": "MUL123456", "problema": "Touchscreen não responde"}
        ]
        
        dispositivos_criados = []
        for i, dispositivo_data in enumerate(dispositivos_data):
            cliente_idx = i // 4
            dispositivo = criar_dispositivo(
                db, dispositivo_data["tipo"], dispositivo_data["marca"], 
                dispositivo_data["modelo"], dispositivo_data["numero_serie"], 
                dispositivo_data["problema"], clientes_criados[cliente_idx].id
            )
            dispositivos_criados.append(dispositivo)
            print(f"Dispositivo: {dispositivo_data['marca']} {dispositivo_data['modelo']} - {clientes_criados[cliente_idx].pessoa.nome}")
        
        print("Criando fornecedores...")
        fornecedores_data = [
            {"nome": "TechParts Ltda", "cnpj": "12345678000195", "material_fornecido": "Componentes de hardware em geral"},
            {"nome": "EletroMega Distribuidora", "cnpj": "98765432000186", "material_fornecido": "Peças e acessórios eletrônicos"},
            {"nome": "PC Componentes Brasil", "cnpj": "45678912000134", "material_fornecido": "Hardware e periféricos"},
            {"nome": "Suprimentos Informática", "cnpj": "32165498000167", "material_fornecido": "Materiais de informática diversos"},
            {"nome": "Global Tech Supplies", "cnpj": "65412398000123", "material_fornecido": "Importação de componentes"}
        ]
        
        fornecedores_criados = []
        for fornecedor_data in fornecedores_data:
            fornecedor = criar_fornecedor(
                db, fornecedor_data["nome"], fornecedor_data["cnpj"], 
                fornecedor_data["material_fornecido"]
            )
            fornecedores_criados.append(fornecedor)
            print(f"Fornecedor: {fornecedor_data['nome']}")
        
        print("Criando estoque...")
        estoque_data = [
            {"nome": "Fonte de Alimentação 500W", "descricao": "Fonte ATX 500W 80 Plus Bronze", "quantidade": 15, "valor": 189.90},
            {"nome": "Memória RAM 8GB DDR4", "descricao": "Memória Kingston 8GB 2666MHz", "quantidade": 25, "valor": 199.90},
            {"nome": "SSD 240GB SATA", "descricao": "SSD Kingston A400 240GB", "quantidade": 3, "valor": 159.90},
            {"nome": "Placa Mãe AMD B450", "descricao": "Placa Mãe ASUS Prime B450M", "quantidade": 8, "valor": 499.90},
            
            {"nome": "Teclado Mecânico", "descricao": "Teclado Redragon Kumara", "quantidade": 2, "valor": 249.90},
            {"nome": "Mouse Gamer", "descricao": "Mouse Redragon Cobra", "quantidade": 0, "valor": 89.90},
            {"nome": "Monitor 24'' LED", "descricao": "Monitor Samsung 24'' Full HD", "quantidade": 6, "valor": 799.90},
            {"nome": "Webcam Full HD", "descricao": "Webcam Logitech C920", "quantidade": 4, "valor": 349.90},
            
            {"nome": "Processador Intel i5", "descricao": "Processador Intel Core i5 10400F", "quantidade": 12, "valor": 899.90},
            {"nome": "Placa de Vídeo GTX 1660", "descricao": "Placa de Vídeo NVIDIA GTX 1660 Super", "quantidade": 5, "valor": 1499.90},
            {"nome": "Gabinete Gamer", "descricao": "Gabinete Rise Mode Glass", "quantidade": 10, "valor": 199.90},
            {"nome": "Cooler para Processador", "descricao": "Cooler Master Hyper 212", "quantidade": 7, "valor": 159.90},
            
            {"nome": "Cabo HDMI 2.0", "descricao": "Cabo HDMI 2.0 2 metros", "quantidade": 50, "valor": 29.90},
            {"nome": "Fonte de Notebook", "descricao": "Fonte Universal para Notebook", "quantidade": 15, "valor": 89.90},
            {"nome": "Pasta Térmica", "descricao": "Pasta Térmica Arctic MX-4", "quantidade": 30, "valor": 24.90},
            {"nome": "Kit Ferramentas", "descricao": "Kit de Ferramentas para Informática", "quantidade": 8, "valor": 149.90},
            
            {"nome": "SSD NVMe 1TB", "descricao": "SSD WD Black SN850 1TB", "quantidade": 4, "valor": 899.90},
            {"nome": "Memória RAM 16GB DDR5", "descricao": "Memória Corsair Vengeance 16GB", "quantidade": 6, "valor": 699.90},
            {"nome": "Water Cooler 240mm", "descricao": "Water Cooler Corsair H100i", "quantidade": 3, "valor": 799.90},
            {"nome": "Placa de Captura", "descricao": "Placa de Captura Elgato HD60 S", "quantidade": 2, "valor": 899.90}
        ]
        
        for i, item_data in enumerate(estoque_data):
            fornecedor_idx = i // 4
            item = criar_estoque(
                db, item_data["nome"], item_data["descricao"], 
                item_data["quantidade"], item_data["valor"], 
                fornecedores_criados[fornecedor_idx].id
            )
            print(f"Estoque: {item_data['nome']} - {fornecedores_criados[fornecedor_idx].nome}")
        
        print("Criando orcamentos e ordens de servico...")
        
        diagnosticos = [
            "Problema na fonte de alimentacao - necessaria substituicao",
            "Tela LCD quebrada - requer substituicao completa",
            "Superaquecimento - necessaria limpeza interna e troca de pasta termica",
            "Virus e malware - necessaria formatacao e reinstalacao do sistema",
            "Problema na placa-mae - diagnostico avancado necessario",
            "HD corrompido - necessaria recuperacao de dados",
            "Problemas de conectividade WiFi - substituicao do modulo wireless",
            "Bateria nao segura - necessaria substituicao urgente"
        ]
        
        status_options = list(StatusOrdem)
        metodo_pagamento_options = list(MetodoPagamento)
        
        for i in range(8):
            dispositivo = random.choice(dispositivos_criados)
            tecnico = random.choice(tecnicos_criados)
            atendente = random.choice(atendentes_criados)
            
            preco_total = round(random.uniform(100.0, 800.0), 2)
            orcamento = criar_orcamento(
                db, random.choice(metodo_pagamento_options), preco_total,
                dispositivo.id, atendente.id
            )
            
            data_entrada = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            data_previsao = data_entrada + timedelta(days=random.randint(3, 10))
            
            ordem = criar_ordem_servico(
                db, dispositivo.id, tecnico.id, orcamento.id,
                data_previsao, random.choice(diagnosticos)
            )
            
            if i < 4:
                ordem.status = StatusOrdem.CONCLUIDA
                ordem.dataConclusao = data_previsao - timedelta(days=1)
            elif i < 6:
                ordem.status = StatusOrdem.EM_ANDAMENTO
            else:
                ordem.status = StatusOrdem.AGUARDANDO_PECAS
            
            db.commit()
            
            print(f"Ordem #{ordem.id}: {dispositivo.marca} {dispositivo.modelo} - Status: {ordem.status.value}")
        
        print("DADOS DE EXEMPLO CRIADOS COM SUCESSO!")
        print("=" * 60)
        print("RESUMO DOS DADOS CRIADOS:")
        print(f"Enderecos: {len(enderecos_criados)}")
        print(f"Clientes: {len(clientes_criados)}")
        print(f"Atendentes: {len(atendentes_criados)}")
        print(f"Tecnicos: {len(tecnicos_criados)}")
        print(f"Dispositivos: {len(dispositivos_criados)}")
        print(f"Fornecedores: {len(fornecedores_criados)}")
        print(f"Itens no Estoque: {len(estoque_data)}")
        print(f"Ordens de Servico: 8")
        print("=" * 60)
        
    except Exception as e:
        print(f"Erro ao criar dados de exemplo: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    criar_dados()