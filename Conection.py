import socket
from src.application.Logger import Logger
from src.application.view import View

logger = Logger()


class Conection:

    def __init__(self):
        View.clear()
        View.cabecera()
        self.mensaje = ""
        self.host = input("[38;5;20m Introduce el Host:[92;5;20m")
        self.port = int (input("[38;5;20m Introduce el Puerto:[92;5;154m"))
        self.conexion()
    
  
    
    def conexion(self):
        
        def escuchar_servidor(sock):
            self.mensaje = input("[38;5;20m Introduzca el Comando , help para visualizar las opciones o 'salir' para terminar):[92;5;154m ")
            s.sendall(self.mensaje.encode())
            while True:
                data = sock.recv(1024)
                if data:
                    print(f'[38;5;33m Server: [92;5;92m{data.decode()}')
                    self.mensaje = input("[38;5;20m Introduzca el Comando , help para visualizar las opciones o 'salir' para terminar):[92;5;154m ")
                    if self.mensaje.lower() == 'salir':
                        s.close()
                        Conection()
                        break
                    if self.mensaje == "":
                        self.mensaje = "vacio"
                    s.sendall(self.mensaje.encode())

                

        try:
            error = False
            logger.debug("Conectando...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            logger.debug(f'Conectado al servidor: {self.host}:{self.port}')
            View.clear()
            View.cabecera()
            escuchar_servidor(s)
                    
                

        except socket.gaierror as e:
            error = True
            if e.errno == 11001:
                logger.debug('ERROR 11001: Los Datos de HOST Y PUERTO introducidos no son correctos')
            else:
                logger.debug(f'Error gaierror: {e}')
        except socket.timeout as e:
            error = True
            if e.errno == 10060:
                logger.debug('ERROR 10060: Se ha agotado el tiempo de espera para la conexión. El servidor no ha respondido a tiempo., puede que introduzca mal el HOST u/o el PORT')
            elif e.errno == 10061:
                logger.debug("ERROR 10061: No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión, puede que introduzca mal el HOST u/o el PORT")
        except Exception as e:  
            s.close()
            error = True
            logger.debug(f'ERROR: {e}')
        finally:
            try:
                if (error == True):
                    Conection()
            except:
                pass
    
Conection()
