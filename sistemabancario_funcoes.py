import textwrap

# Função para exibir o menu principal e pegar a opção selecionada pelo usuário
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para realizar depósito, atualizando saldo e extrato
def depositar(saldo, valor, extrato, /):    # Argumento posicional
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== O depósito foi realizado com sucesso! ===")  # === = Mensagem de sucesso
    else:
        print("\n@@@ A operação falhou! O valor informado é inválido. @@@")  #  @@@ = Mensagem de erro

    return saldo, extrato

# Função para realizar saque, verificando limites de saldo, valor e número de saques
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):   # Argumento nomeado
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ A operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ A operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ A operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ A operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

# Função para exibir o extrato das transações realizadas e o saldo atual
def exibir_extrato(saldo, /, *, extrato): # Argumentos posicionais e nnomeados 
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Função para criar um novo usuário e armazená-lo na lista de usuários
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (digite apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ O CPF informado já está cadastrado no nosso sistema! ! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

# Função para buscar um usuário existente pelo CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta, associada a um usuário existente
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n===  A conta foi criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, a conta não pode ser criada! @@@")

# Função para listar todas as contas cadastradas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\ 
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função principal que controla o fluxo do programa
def main():
    LIMITE_SAQUES = 3  # Limite de saques diários
    AGENCIA = "0001"  # Código da agência padrão

    saldo = 0  # Saldo inicial da conta
    limite = 500  # Limite máximo para saques
    extrato = ""  # Extrato vazio no início
    numero_saques = 0  # Contador de saques
    usuarios = []  # Lista de usuários cadastrados
    contas = []  # Lista de contas criadas

    # Loop principal para interagir com o menu e executar as operações
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor que deseja depositar: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor que você deseja sacar: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, selecione novamente uma operação válida.")

# Executa o programa principal
main()
