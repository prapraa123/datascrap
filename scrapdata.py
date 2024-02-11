import requests
from bs4 import BeautifulSoup
import time
import sys

# Definir códigos ANSI para colores de texto en la consola
GREEN = "\033[32m"
RED = "\033[91m"
RESET = "\033[0m"

# Pedir al usuario que ingrese el texto
usuario_texto = input(f"{GREEN}Ingrese el DNI o nombre completo: {RESET}")

# Construir la URL con el texto del usuario
url = f"https://www.cuitonline.com/search.php?q={usuario_texto}"

# Realizar la solicitud web
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Utilizar BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar el div específico que contiene la información
    div_resultado = soup.find('div', {'class': 'hit'})

    # Verificar si se encontró el div
    if div_resultado:
        # Extraer la información después de "Ver detalles de"
        detalles_texto = div_resultado.find('a', {'title': lambda t: t and "Ver detalles de" in t})
        
        # Extraer el texto dentro del span con clase "cuit"
        cuit_elemento = div_resultado.find('span', {'class': 'cuit'})
        cuit_texto = cuit_elemento.text.strip() if cuit_elemento else None
        
        # Extraer el texto después de <i> hasta </i>
        i_elemento = div_resultado.find('i')
        i_texto = i_elemento.text.strip() if i_elemento else None
        
        # Imprimir el texto de detalles con animación y color
        sys.stdout.write(RED + "\n\nNombre completo: ")
        for char in detalles_texto['title'].split("Ver detalles de ")[1].split('"')[0]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write(RESET + '\n')

        # Imprimir el texto de CUIT con animación y color
        sys.stdout.write(RED + "CUIT: ")
        for char in (cuit_texto := cuit_texto.split('</span>')[0]) if cuit_texto else "":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write(RESET + '\n')

        # Imprimir el texto después de <i> con animación y color
        sys.stdout.write(RED + "Sexo: ")
        for char in i_texto:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write(RESET + '\n')

    else:
        print("No se encontró el div específico en la respuesta.")
else:
    print(f"Error en la solicitud. Código de estado: {response.status_code}")
