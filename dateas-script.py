import requests
import re
from colorama import init, Fore
import os

init(autoreset=True)

def limpiar_pantalla():
	os.system('clear')

def credits():
	print(" ---------------------------")
	print("|                           |")
	print("|     MADE BY PraPra123     |")
	print("|___________________________|")

def obtener_nombre_completo():
    while True:
        nombre_completo = input(f"\n{Fore.GREEN}Ingrese el nombre completo: {Fore.RESET}").lower().replace(" ", "-")

        if len(nombre_completo.split("-")) <= 2:
            print(f"\n{Fore.RED}Por favor, ingrese un nombre completo junto con el apellido.{Fore.RESET}\n")
        elif not re.match("^[a-zA-Z0-9-]*$", nombre_completo):
            print(f"\n{Fore.RED}Por favor, vuelva a escribir el nombre sin caracteres especiales ni acentos.{Fore.RESET}\n")
        else:
            return nombre_completo

def obtener_cuit():
    while True:
        cuit = input(f"{Fore.GREEN}Ingrese el CUIT (sin guiones): {Fore.RESET}")

        if "-" in cuit:
            print(f"{Fore.RED}No se admiten guiones en el CUIT. Por favor, ingréselo sin guiones.{Fore.RESET}")
        elif not re.match("^[0-9]*$", cuit):
            print(f"{Fore.RED}Por favor, ingrese solo números en el CUIT.{Fore.RESET}")
        else:
            return cuit

def filtrar_contenido_web(contenido_web, etiqueta_inicio, etiqueta_fin):
    inicio = contenido_web.find(f"{etiqueta_inicio}</th><td>") + len(f"{etiqueta_inicio}</th><td>")
    fin = contenido_web.find("<", inicio)
    resultado_filtrado = contenido_web[inicio:fin]
    return resultado_filtrado

def imprimir_resultado(etiqueta, contenido):
    print(f"{Fore.YELLOW}> {etiqueta}: {Fore.RESET}{contenido}\n")

def realizar_peticion_web(nombre_completo, cuit):
    url = f"https://www.dateas.com/es/persona/{nombre_completo}-{cuit}"
    response = requests.get(url)

    if response.status_code == 200:
        contenido_web = response.text

        # Filtrar por las etiquetas especificadas
        etiquetas = ["Apellido y Nombre", "Posible DNI", "CUIT/CUIL", "Edad Estimada",
                     "Homónimos", "Actividad u Ocupación", "Ganancias", "IVA",
                     "Monotributo", "Integra Sociedades", "Empleador"]

        for etiqueta in etiquetas:
            resultado_filtrado = filtrar_contenido_web(contenido_web, etiqueta, "<")
            if etiqueta == "Apellido y Nombre":
                print("\n" + "="*50 + "\n")
            imprimir_resultado(etiqueta, resultado_filtrado)

    else:
        print(f"{Fore.RED}Los datos introducidos no son válidos. Error: {response.status_code}{Fore.RESET}")

def main():
    limpiar_pantalla()
    credits()
    nombre_completo = obtener_nombre_completo()
    cuit = obtener_cuit()
    
    realizar_peticion_web(nombre_completo, cuit)

if __name__ == "__main__":
    main()
