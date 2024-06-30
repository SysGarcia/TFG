import requests
import json
import socket
import fcntl
import struct
import os
import utils as utils

def Coger_Nombre_equipo():
    nombre_equipo = socket.gethostname()
    return nombre_equipo

def Coger_MAC(nombre_interfaz):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(nombre_interfaz[:15], 'utf-8')))
        return ':'.join(['%02x' % b for b in info[18:24]])
    except OSError as e:
        utils.send_logs(f"Error al obtener la dirección MAC de {nombre_interfaz}: {e}")
        return None

def obtener_MAC_de_interfaz_principal(interfaces):
    for interfaz in interfaces:
        direccion_mac = Coger_MAC(interfaz)
        if direccion_mac:
            print(f"Dirección MAC de {interfaz}: {direccion_mac}")
            return direccion_mac
    utils.send_logs("No se pudo obtener la dirección MAC de ninguna de las interfaces especificadas.")
    return None

def Coger_IP(interfaces):
    try:
        for interfaz in interfaces:
            ipv4 = os.popen(f'ip addr show {interfaz} | grep "\<inet\>" | awk \'{{ print $2 }}\' | awk -F "/" \'{{ print $1 }}\'').read().strip()
            if ipv4:
                return ipv4
        utils.send_logs("No se pudo obtener la dirección IP de ninguna de las interfaces especificadas.")
        return None
    except Exception as e:
        utils.send_logs(f"Error al obtener la dirección IP: {e}")
        return None
    
def ENVIAR_INFORMACION_EQUIPO(url):
    INTERFACES = ['eth0', 'enp0s3', 'wlan0']  # Lista de interfaces a verificar

    nombre_equipo = Coger_Nombre_equipo()
    Direccion_IP = Coger_IP(INTERFACES)
    Direccion_MAC = obtener_MAC_de_interfaz_principal(INTERFACES)

    if Direccion_IP is None or Direccion_MAC is None:
        utils.send_logs("No se pueden enviar los datos porque no se obtuvo la dirección IP o MAC.")
        return

    # Datos JSON sobre el equipo
    datos = {
        'Nombre_Equipo': nombre_equipo,
        'Direccion_IP': Direccion_IP,
        'Direccion_MAC': Direccion_MAC
    }

    datos_json = json.dumps(datos)
    # Cabeceras para indicar que los datos son JSON
    cabecera = {'Content-Type': 'application/json'}

    # Realizar la solicitud POST al servidor Flask
    try:
        response = requests.post(url, data=datos_json, headers=cabecera)
        response.raise_for_status()  # Lanza una excepción si no se obtiene un código de estado 2xx
        utils.send_logs('Datos enviados correctamente!')
    except requests.exceptions.RequestException as e:
        utils.send_logs(f'Error al enviar los datos al servidor Flask: {e}')

# Ejemplo de llamada a la función para enviar información al servidor Flask
url_servidor = 'http://ejemplo.com/api/datos'
ENVIAR_INFORMACION_EQUIPO(url_servidor)
