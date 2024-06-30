import os

def send_logs(mensaje):
    try:
        if not os.path.exists("log_macro.txt"):
            with open("log_macro.txt", "w"):
                pass  # Crea el archivo si no existe

        with open("log_macro.txt", "a") as file:
            file.write(mensaje + "\n")
        print("Mensaje registrado correctamente en el archivo de log.")
    except Exception as e:
        print(f"Error al registrar el mensaje en el archivo de log: {e}")
