import requests
import json

# URL y headers para interactuar con la API
url = "http://127.0.0.1:5000/v1/completions"  # Asegúrate de que coincide con tu configuración local
headers = {"Content-Type": "application/json"}

def obtener_datos_usuario():
    print("Bienvenido al generador de historias!")
    personaje_principal = input("Introduce el nombre del personaje principal: ")
    personaje_secundario = input("Introduce el nombre del personaje secundario: ")
    lugar = input("Introduce el lugar donde ocurre la historia: ")
    accion = input("Introduce una acción importante que debe suceder: ")
    return personaje_principal, personaje_secundario, lugar, accion

def ajustar_creatividad():
    print("\nSelecciona el nivel de creatividad:")
    print("1. Alta")
    print("2. Media")
    print("3. Baja")
    opcion = input("Opción (1/2/3): ")
    if opcion == "1":
        return 0.9  # Temperatura alta
    elif opcion == "2":
        return 0.7  # Temperatura media
    elif opcion == "3":
        return 0.5  # Temperatura baja
    else:
        print("Opción no válida, seleccionando creatividad media por defecto.")
        return 0.7

def generar_historia(url, headers, datos_usuario, temperatura):
    personaje_principal, personaje_secundario, lugar, accion = datos_usuario
    print("Generando historia...")
    prompt = (
        f"Write an engaging story with the following elements:\n"
        f"Main character: {personaje_principal}\n"
        f"Secondary character: {personaje_secundario}\n"
        f"Setting: {lugar}\n"
        f"Important action: {accion}\n"
        f"Make the story detailed and creative."
    )
    body = {
        "prompt": prompt,
        "temperature": temperatura,
        "max_tokens": 750,  # Ajusta este valor según sea necesario
    }
    response = requests.post(url=url, headers=headers, json=body, verify=False)
    if response.status_code == 200:
        message_response = json.loads(response.content.decode("utf-8"))
        historia = message_response["choices"][0]["text"].strip()
        return historia
    else:
        print(f"Error: {response.status_code}")
        return None

def traducir_historia(url, headers, historia, temperatura):
    print("\nTraduciendo historia al español...")
    prompt = (
    f"Please translate this text into Spanish without adding or modifying its meaning:\n\n{historia}\n\n"
    "Translation:"
    )
    body = {
        "prompt": prompt,
        "temperature": 0.3,
        "max_tokens": 750,  # Ajusta según el tamaño de la historia 
    }
    response = requests.post(url=url, headers=headers, json=body, verify=False)
    if response.status_code == 200:
        message_response = json.loads(response.content.decode("utf-8"))
        traduccion = message_response["choices"][0]["text"].strip()
        return traduccion
    else:
        print(f"Error al traducir: {response.status_code}")
        return historia  # Devuelve el texto original en caso de error

def main():
    datos_usuario = obtener_datos_usuario()
    temperatura = ajustar_creatividad()
    historia = generar_historia(url, headers, datos_usuario, temperatura)
    if historia:
        print("\nHistoria generada en inglés:\n")
        print(historia)

        # Traducir la historia al español usando el modelo
        traduccion = traducir_historia(url, headers, historia, temperatura)
        print("\nHistoria traducida al español:\n")
        print(traduccion)

if __name__ == "__main__":
    main()
