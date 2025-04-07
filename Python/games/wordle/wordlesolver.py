import random

# Listas de palabras por dificultad
# lista = "lista5facil.txt"
lista = "lista5.txt"

BOLD = "\033[1m"  # Negrita
RESET = "\033[0m"  # Restablecer color

def getList(lista):
    with open(lista, encoding="utf-8") as f:
        words = [word.strip().lower() for word in f if len(word.strip()) == 5]
    return words

def filtrar_palabras(palabra_intento, resultado, lista_palabras):
    listaValidos = []
    for palabra in lista_palabras:
        if not palabra_intento == palabra:
            es_posible = True
            for i in range(5):
                # Si la letra está en la posición correcta (B)
                if resultado[i] == 'B':
                    if palabra[i] != palabra_intento[i]:
                        es_posible = False
                        break
                # Si la letra está en la palabra pero no en la posición correcta (C)
                elif resultado[i] == 'C':
                    if palabra[i] == palabra_intento[i] or palabra_intento[i] not in palabra:
                        es_posible = False
                        break
                # Si la letra no está en la palabra (M)
                elif resultado[i] == 'M':
                    if palabra_intento[i] in palabra:
                        es_posible = False
                        break
            if es_posible:
                listaValidos.append(palabra)
    return listaValidos

def obtener_resultado():
    palabra_intento = input("\nIntroduce la palabra de 5 letras que intentaste:\n>> ").strip().lower()

    if len(palabra_intento) != 5 or not palabra_intento.isalpha():
        print("La palabra debe tener exactamente 5 letras.")
        return None, None

    resultado = input("Introduce el resultado (B = bien, C = cambiar de sitio, M = mal) para cada letra:\n>> ").strip().upper()

    if len(resultado) != 5 or any(c not in "BCM" for c in resultado):
        print("El resultado debe ser de 5 caracteres, solo 'B', 'C' o 'M'.")
        return None, None

    return palabra_intento, resultado

def deducir_palabras(palabras_posibles):
    palabra_intento, resultado = obtener_resultado()

    if palabra_intento is None or resultado is None:
        return True, None

    posibles = filtrar_palabras(palabra_intento, resultado, palabras_posibles)

    if posibles:
        print(f"Prueba con la palabra {BOLD}{random.choice(posibles)}{RESET}")
    else:
        print("\nNo se encontraron palabras posibles que cumplan con las condiciones dadas.")

    return False, posibles

if __name__ == "__main__":
    palabras_posibles = getList(lista)
    encontrado = False

    print("###################################\n# Deductor de palabras del Wordle #\n###################################")

    while not encontrado:
        error, nuevalista = deducir_palabras(palabras_posibles)
        if not nuevalista is None:
            palabras_posibles = nuevalista
        if not error:
            respuesta = "a"
            while respuesta != "s" and respuesta != "n":
                respuesta = input("¿Has conseguido encontrar la palabra? (s/n): ")
            if respuesta == "s":
                encontrado = True

    print("Cerrando programa...\n")