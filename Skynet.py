import threading
import socket
import sys
import mysql.connector

compromissos = []
usuarios = []
atual = ""
conn = mysql.connector.Connect(host='127.0.0.1',user='skynet',\
                        password='t-800',database='skynetdb')

#DEFINE O USUARIO
class user:
   login = ""
   senha = ""
   nome = ""
   server_adrr = []

   def __init__(self,nome,server_adrr,login,senha):
      self.nome = nome
      self.server_adrr = server_adrr
      self.login = login
      self.senha = senha


def make_user(nome,server_adrr,login,senha):
   user1 = user(nome,server_adrr,login,senha)
   return user1

#DEFINE O COMPROMISSO
class compromisso(object):
   date = ""
   descricao = ""
   login = ""
   def __init__(self,date,descricao,login):
      self.date = date
      self.login = login
      self.descricao = descricao
      

def make_compromisso(date,descricao,login):
   compromisso1 = compromisso(date,descricao,login)
   return compromisso1


def salvaCompromisso(login,data1):
   data = data1[12:]                      #12 � o tamanho de "COMPROMISSO "
   date = data[0:16]                      #10 � o tamanho da data
   descricao = data[17:len(data)]         #o resto � a descricao

   c = conn.cursor()
   c.execute("INSERT INTO compromisso(data, descricao) VALUES (STR_TO_DATE('%s','%%d/%%m/%%Y %%H:%%i'),'%s')" % (date, descricao))
   # Salva (commit) as mudan�as
   conn.commit()

   compromissos.append(make_compromisso(date,descricao,login))
   arquivo = open('compromisso.txt', 'r')
   comps = arquivo.readlines()
   comps.append("\n"+ date +","+ descricao +","+ login)
   arquivo = open('compromisso.txt', 'w')
   arquivo.writelines(comps)
   arquivo.close()

def lerCompromisso():
   arquivo = open('compromisso.txt', 'r')
   comps = arquivo.readlines()
   for i in range(len(comps)):
      comp = comps[i].split(',')
      comp[2] = comp[2].replace("\n","")
      compromissos.append(make_compromisso(comp[0],comp[1],comp[2]))
      comp = ""

def lerUsuario():
   userList = []
   arquivo = open('login.txt', 'r')
   users = arquivo.readlines()
   users[0] = users[0].replace("[","")
   users[0] = users[0].replace("]","")
   users[0] = users[0].replace("\"","")
   user = users[0].split(',')
   userList.append(user[1])
   userList.append(user[2])
   usuarios.append(make_user(user[0],userList,user[3],user[4]))


def esperandoConexao():
   #while True:
       # Esperando por conexão
       
       try:
           print >> sys.stderr, 'Conexao de', client_address

           # Receber os dados em pequenos "pacotes" e reenvia-los
           while True:
               data = connection.recv(32000)
               print >> sys.stderr, 'Recebeu "%s"' % data
               if data:
                   #Valida login do user
                   if(data.find("VALIDAR") > -1):
                           separator = data.find("/")
                           login = data[8:separator]
                           senha = data[separator+1:]
                           print login
                           print senha

                           # Inicializa
                           c = conn.cursor()
                           c.execute("SELECT * FROM conta WHERE login = '%s' AND password = '%s'" % (login, senha))
                           t = c.fetchone()
                           #print t

                           if t is not None:
                              atual = login
                              connection.sendall("VALIDUSER")
                                       
                           else:
                              connection.sendall("INVALIDUSER")
                                   
                   if(data.find("COMPROMISSO") != -1):
                       salvaCompromisso(atual,data)
                       connection.sendall("SALVO")
                   if(data.find("VISUALIZAR") > -1):
                       visu = []
                       gambis = ""
                       print len(compromissos)
                       for i in range(len(compromissos)):
                           if compromissos[i].login == atual:
                               gambis = gambis + compromissos[i].date + "-" + compromissos[i].descricao + "\n"
                       connection.sendall(gambis)         
                       
               else:
                   print >> sys.stderr, 'Sem mais dados de', client_address
                   break

       finally:
           # Fecha a conexão
           connection.close()
           return


lerUsuario()
lerCompromisso()
#usuarios.append(make_user("alex", ['localhost',10005], "alex","alex"))


# Criando socket  TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# "Colocando" socket na porta
server_address = ('localhost', 10006)
print >>sys.stderr, 'iniciando em %s na porta %s' % server_address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Ouvindo na porta
sock.listen(1)

while True:
   print >>sys.stderr, 'Esperando conexao'
   connection, client_address = sock.accept()
   t1 = threading.Thread(target = esperandoConexao, args = [])
   t1.start()
#t1.join()

