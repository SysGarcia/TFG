from flask import Flask, request, jsonify
import csv
import os

APP = Flask(__name__) #Instancia de FLASK (necesario para que Flask sepa sobre archivos estaticos, plantillas...)

PATH_ARCHIVO_CSV = 'Server_App/datos.csv'

def comprobacion_archivo_csv_equipos():
    """ Verifica si el archivo CSV existe y escribe el encabezado si no existe """
    if not os.path.exists(PATH_ARCHIVO_CSV):
        with open(PATH_ARCHIVO_CSV, 'w', newline='') as archivo_csv:
            campos = ['Nombre_Equipo', 'Direccion_IP', 'Direccion_MAC']
            writer = csv.DictWriter(archivo_csv, fieldnames=campos)
            writer.writeheader()

@APP.route('/', methods=['POST'])
def accion_datos():
    """ Función principal para manejar los datos recibidos """
    datos = request.json  # Recibe los datos JSON enviados
    print("Recepción de datos:", datos)  # Imprime los datos en consola

    # Verifica si los campos 'Equipo' y 'Rendimiento' están presentes en los datos recibidos
    if 'Nombre_Equipo' in datos and 'Direccion_IP' and 'Direccion_MAC' in datos:
        return campos_correctos_equipos(datos)
    else:
        return jsonify({'message': 'Datos incorrectos'}), 400

def campos_correctos_equipos(datos):
    """ Escribe los datos en el archivo CSV y devuelve una respuesta JSON """
    with open(PATH_ARCHIVO_CSV, 'a', newline='') as archivo_csv:
        campos = ['Nombre_Equipo', 'Direccion_IP', 'Direccion_MAC']
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writerow(datos)
    return jsonify({'message': 'Datos recibidos correctamente'}), 200

if __name__ == '__main__':
    comprobacion_archivo_csv_equipos()
    APP.run(host='0.0.0.0', port=8080)