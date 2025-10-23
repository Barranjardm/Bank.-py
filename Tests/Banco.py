menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar cliente
[cc] Criar conta corrente
[q] Sair

=> """

saldo = 0.0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# estruturas para clientes e contas
clientes = []
contas = []
_next_account_number = 1

def obter_valor(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Entrada inválida. Digite um número válido.")
        return None

def depositar(saldo, extrato, valor):
    if valor is None:
        return saldo, extrato
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print("Depósito realizado com sucesso.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, valor, limite, limite_saques):
    if valor is None:
        return saldo, extrato, numero_saques
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques
    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato, numero_saques
    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1
    print("Saque realizado com sucesso.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato, end="")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# --- funções novas: cadastrar cliente e criar conta corrente ---

def cadastrar_cliente(clientes_list):
    """
    Lê nome, cpf e número do banco e registra um novo cliente.
    Retorna (clientes_list, cliente) — cliente é o dict criado ou None se falhar.
    """
    nome = input("Nome do cliente: ").strip()
    cpf = input("CPF (somente números): ").strip()
    banco = input("Número do banco: ").strip()

    if not nome or not cpf or not banco:
        print("Dados incompletos. Cadastro cancelado.")
        return clientes_list, None

    if any(c["cpf"] == cpf for c in clientes_list):
        print("CPF já cadastrado.")
        return clientes_list, None

    cliente = {"nome": nome, "cpf": cpf, "banco": banco}
    clientes_list.append(cliente)
    print(f"Cliente '{nome}' cadastrado com sucesso.")
    return clientes_list, cliente

def criar_conta_corrente(contas_list, clientes_list, agencia="0001"):
    """
    Cria uma conta corrente vinculada a um cliente existente (busca por CPF).
    Retorna (contas_list, conta) — conta é o dict criado ou None se falhar.
    """
    global _next_account_number

    cpf = input("CPF do cliente para criar a conta: ").strip()
    cliente = next((c for c in clientes_list if c["cpf"] == cpf), None)
    if cliente is None:
        print("Cliente não encontrado. Cadastre o cliente antes de criar a conta.")
        return contas_list, None

    numero = f"{_next_account_number:06d}"
    _next_account_number += 1

    conta = {
        "agencia": agencia,
        "numero": numero,
        "tipo": "corrente",
        "cliente": cliente
    }
    contas_list.append(conta)
    print(f"Conta corrente criada: Agência {agencia} Conta {numero} — Titular: {cliente['nome']}")
    return contas_list, conta

# --- fim das funções novas ---

def main():
    global saldo, extrato, numero_saques, clientes, contas
    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            valor = obter_valor("Informe o valor do depósito: ")
            saldo, extrato = depositar(saldo, extrato, valor)

        elif opcao == "s":
            valor = obter_valor("Informe o valor do saque: ")
            saldo, extrato, numero_saques = sacar(
                saldo, extrato, numero_saques, valor, limite, LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "c":
            clientes, _ = cadastrar_cliente(clientes)

        elif opcao == "cc":
            contas, _ = criar_conta_corrente(contas, clientes)

        elif opcao == "q":
            print("Encerrando.")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
