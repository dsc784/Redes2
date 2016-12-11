# coding=utf-8
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
try:
    server_address = ('localhost', 10000)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
except:
    print "Nao foi possivel conectar ao servidor."
    raw_input()
    sys.exit(0)
cont = 0


def login():
    loginerr = -1
    while loginerr != 0:
        print "Sistema de agendas compartilhadas\n" \
              "Insira seu login: "
        login = str(raw_input())
        print "Insira sua senha: "
        senha = str(raw_input())
        sock.sendall("VALIDAR " + login + "/" + senha)
        # Look for the response
        amount_received = 0
        amount_expected = len(login)

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            if data == "VALIDUSER":
                print "Login realizado com sucesso\n"
                loginerr = 0
            elif data == "INVALIDUSER":
                print "Login ou senha invalidos\n"


def menu():
    opt = 1
    while opt != 3:
        print "Interface Usuário:\n" \
              "1. Marcar Compromisso\n" \
              "2. Visualizar Compromissos\n" \
              "3. Sair\n"
        while True:
            try:
                opt = int(raw_input(': '))  # recebe a opção
                break
            except:
                print "Opção inexistente."
        if opt == 1:
            marcaCompromisso()
        elif opt == 2:
            visualCompromisso()
        elif opt == 3:
            sock.close()


def marcaCompromisso():
    dataerr = -1
    while dataerr != 0:
        print "Insira a data para marcar o compromisso (DD/MM/AAAA DESCRICAO):"
        date = str(raw_input(': '))
        checkdia = date[0:2]
        checkmes = date[3:5]
        checkano = date[6:10]
        print date[0:10]
        if int(checkano) < 2016:
            print "Ano impossivel\n"
        else:
            if int(checkmes) > 12 or int(checkmes) < 0:
                print checkmes + ": Mes impossivel\n"
            elif int(checkmes) == 2:
                if not (29 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel1\n"
                else:
                    dataerr = 0
            elif int(checkmes) == 1 or 3 or 5 or 6 or 8 or 10 or 12:
                if not (31 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel2\n"
                else:
                    dataerr = 0
            elif int(checkmes) == 2 or 4 or 6 or 9 or 11:
                if not (30 >= int(checkdia) >= 1):
                    print checkdia + ": dia impossivel3\n"
                else:
                    dataerr = 0

    sock.sendall("COMPROMISSO " + date)
    # Look for the response
    amount_received = 0
    amount_expected = len(date)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print >> sys.stderr, 'received "%s"' % data


def visualCompromisso():
    sock.sendall("VISUALIZAR")
    amount_received = 0
    amount_expected = len("VISUALIZAR")

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)

    print data


login()
menu()