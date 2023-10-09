import os
import socket

# --> Configuración del servidor
HOST = '127.0.0.1'
PORT = 12345

# --> Carpeta que contendrá los archivos recibidos
carpeta_destino = "archivos_recibidos"

# --> Crear carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.mkdir(carpeta_destino)
    print(f"[+] Carpeta '{carpeta_destino}' creada.")

# --> Iniciar conexión UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

    # --> Enlazar el socket a la dirección y puerto especificados
    server_socket.bind((HOST, PORT))
    print(f"[+]Servidor escuchando en {HOST}:{PORT}")

    while True:
        # --> Recibir el nombre del archivo y su longitud
        data, addr = server_socket.recvfrom(1024)
        if not data:
            break

        # --> Decodificar los datos recibidos
        file_info = data.decode().split(":")
        if len(file_info) != 2:
            print("Formato incorrecto.")
            continue

        # --> Obtener el nombre y tamaño del archivo
        file_name, file_size = file_info[0], int(file_info[1])
        print(f"\n[+]Recibiendo archivo: {file_name}, Tamaño: {file_size} bytes")

        # --> Crear el archivo en la carpeta de destino
        file_path = os.path.join(carpeta_destino, file_name)

        # --> Crear un conjunto para almacenar los datos recibidos
        received_data_set = set()

        # --> Recibir el archivo en fragmentos
        with open(file_path, 'wb') as file:
            total_received = 0
            while total_received < file_size:
                # --> Recibir paquetes de 1024 bytes
                data, _ = server_socket.recvfrom(1024)

                # --> Si no se reciben datos, salir del bucle
                if not data:
                    break

                # --> Comparar si no hay duplicados
                if data in received_data_set:
                    print("\tPaquete duplicado. Enviando confirmación al cliente...")
                    server_socket.sendto(b"OK", addr)
                    continue

                # --> Escribir los datos recibidos en el archivo
                file.write(data)

                # --> Agregar los datos al conjunto de datos recibidos
                received_data_set.add(data)

                # --> Mandar confirmación al cliente
                print("\tMandando confirmación al cliente...")
                server_socket.sendto(b"OK", addr)

                # --> Actualizar el número de bytes recibidos
                total_received += len(data)

        print(f"[+]Archivo '{file_name}' recibido y guardado con éxito en '{carpeta_destino}'.")
        
        # Salir 
        break
