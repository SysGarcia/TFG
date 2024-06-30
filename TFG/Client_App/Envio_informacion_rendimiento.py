import subprocess
# https://stackoverflow.com/questions/9229333/how-to-get-overall-cpu-usage-e-g-57-on-linux

def Coger_uso_CPU():
    # Comando a ejecutar
    command = """awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1) "%"; }' \
<(grep 'cpu ' /proc/stat) <(sleep 1; grep 'cpu ' /proc/stat)"""

    # Ejecutar el comando usando bash
    process = subprocess.Popen(['bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Obtener la salida y los errores
    stdout, stderr = process.communicate()

    if stderr:
        print(f"Error: {stderr.decode('utf-8')}")

    cpu_usage = stdout.decode('utf-8').strip()    # Decodificar la salida

    return cpu_usage

print(Coger_uso_CPU())
