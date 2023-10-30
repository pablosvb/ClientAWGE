import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import ctypes

from src.application.Logger import Logger
from src.application.view import View
from src.domain.cabecera import __header_AWGE__, __header_W__, __header_PMC__, __header_sxplain__, __header_line__

logger = Logger()

class Conection:

    def __init__(self):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)  # SW_MINIMIZE = 6
        self.setup_ui()
        
    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title("Cliente YNART")
        self.window.config(bg="black")

        # Estilo de terminal
        terminal_font = ("Courier", 12)
        terminal_fg = "limegreen"

        #carga de imagenes
        self.logo_image = ImageTk.PhotoImage(Image.open("logo_w_v1.png"))

        original_image = Image.open("pmcDesign_Poweredby.png")
        # Define las nuevas dimensiones (por ejemplo, 100x100)
        new_width = 130  
        new_height = 66
        
        # Redimensiona la imagen
        resized_image = original_image.resize((new_width, new_height))


        self.logo_image_pmc = ImageTk.PhotoImage(resized_image)

        # Área de entrada de Host y Port
        self.entry_frame = tk.Frame(self.window, bg="black")
        self.entry_frame.pack(pady=20, fill=tk.X, padx=20)

        self.host_label = tk.Label(self.entry_frame, text="Host:", bg="black", fg=terminal_fg, font=terminal_font)
        self.host_label.grid(row=0, column=0)

        self.host_entry = tk.Entry(self.entry_frame, width=25, bg="black", fg=terminal_fg, font=terminal_font, insertbackground=terminal_fg)
        self.host_entry.grid(row=0, column=1)

        self.port_label = tk.Label(self.entry_frame, text="Port:", bg="black", fg=terminal_fg, font=terminal_font)
        self.port_label.grid(row=0, column=2)
        self.port_entry = tk.Entry(self.entry_frame, width=10, bg="black", fg=terminal_fg, font=terminal_font, insertbackground=terminal_fg)
        self.port_entry.grid(row=0, column=3)

        self.connect_button = tk.Button(self.entry_frame, text="Conectar", command=self.start_socket, bg="black", fg=terminal_fg, font=terminal_font, bd=0, activebackground="black", activeforeground=terminal_fg)
        self.connect_button.grid(row=0, column=4, padx=20)

         # Área superior
        self.header_frame = tk.Frame(self.window, height=50, bg="black")
        self.header_frame.pack(fill=tk.X)
        image_label = tk.Label(self.header_frame, image=self.logo_image,bg="black")
        image_label.pack()
        

        # Área de mensajes recibidos
        self.received_area = scrolledtext.ScrolledText(self.window, width=60, height=20, bg="black", fg=terminal_fg, font=terminal_font)
        self.received_area.pack(pady=20)

        # Área de entrada de texto
        self.message_entry = tk.Entry(self.window, width=50, bg="black", fg=terminal_fg, font=terminal_font, insertbackground=terminal_fg)
        self.message_entry.pack(pady=20, ipady=10)
        self.message_entry.config(state=tk.DISABLED)
        self.message_entry.bind("<Return>", lambda event=None: self.send_message())

        self.center_frame = tk.Frame(self.window, bg="black")
        self.center_frame.pack(pady=10)
        # Botón para enviar mensaje
        self.send_button = tk.Button(self.window, text="Enviar", command=self.send_message, bg="black", fg=terminal_fg, font=terminal_font, bd=0, activebackground="black", activeforeground=terminal_fg)
        self.send_button.pack(in_=self.center_frame, side=tk.LEFT ,padx=(260,0))
        self.send_button.config(state=tk.DISABLED)

        
        self.image_label2 = tk.Label(self.window, image=self.logo_image_pmc,bg="black")
        self.image_label2.pack(in_=self.center_frame, side=tk.LEFT,padx=(120,0),pady=(0,10))

        self.window.mainloop()

    def start_socket(self):
        # Si estamos conectados, desconectamos
        if self.connect_button.cget("text") == "Desconectar":
            self.disconnect_socket()
            return

        self.host = self.host_entry.get()
        self.port = int(self.port_entry.get())

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
        except socket.gaierror:
            logger.error(f"Error: El nombre del host {self.host} no pudo ser resuelto.")
            self.show_error_message("Error de conexión", f"El nombre del host {self.host} no pudo ser resuelto.")
            return
        except ConnectionRefusedError:
            logger.error(f"Error: Conexión rechazada por el servidor.")
            self.show_error_message("Error de conexión", "Conexión rechazada por el servidor.")
            return
        except Exception as e:
            logger.error(f"Error desconocido conectando al servidor: {e}")
            self.show_error_message("Error de conexión", f"Error desconocido: {e}")
            return

        # Cambiamos el texto del botón a "Desconectar"
        self.connect_button.config(text="Desconectar")

        # Una vez conectado, reconfiguramos la UI
        self.host_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)

        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

        self.listen_thread = threading.Thread(target=self.listen_server, args=(self.s,))
        self.listen_thread.start()

    def show_error_message(self, title, message):
        messagebox.showerror(title, message)

    def disconnect_socket(self):
        try:
            self.s.shutdown(socket.SHUT_RDWR)  # Detiene ambas transferencias de datos
            self.s.close()
        except Exception as e:
            logger.error(f"Error desconectando del servidor: {e}")

        # Cambiamos el texto del botón de vuelta a "Conectar"
        self.connect_button.config(text="Conectar")

        # Actualizamos la UI a estado desconectado
        self.host_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

    def listen_server(self, sock):
        while True:
            data = sock.recv(1024)
            if data:
                self.update_received_area(f"Server: {data.decode()}\n")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.s.sendall(message.encode())
            self.message_entry.delete(0, tk.END)

    def update_received_area(self, message):
        self.received_area.insert(tk.END, message)
        self.received_area.see(tk.END)  # Autoscroll al último mensaje

Conection()