import random
import os
from operator import length_hint

# Códigos de escape ANSI
RESET = "\033[0m"  # Restablecer color
BOLD = "\033[1m"  # Negrita
GREEN = "\033[92m"  # Verde
RED = "\033[91m"  # Rojo
YELLOW = "\033[93m"  # Amarillo

# Listas de palabras por dificultad
lista5facil = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista5facil.txt"
lista5dificil = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista5.txt"
lista6 = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista6.txt"
diccionario = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/diccionario.txt"

# FUNCIÓN PARA IMPRIMIR EL TÍTULO Y LA EXPLICACIÓN
def printMenu():
    os.system("clear")
    os.system("figlet 'Wordle' -c | lolcat")
    print(f"\nHow does this game work?\n{GREEN} > A green letter means it is correct and in the correct place{RESET}"
          f"\n{YELLOW} > A yellow letter means it is correct but in the wrong place{RESET}"
          f"\n{RED} > A red letter means it is not in the word{RESET}"
          f"\n Remember that the words can only have {BOLD}5 letters{RESET}!\n")


# FUNCIÓN PARA GENERAR LA PALABRA ALEATORIA
def generateRandomWord(lista):
    with open(lista, encoding="utf-8") as f:
        words = [word.strip().lower() for word in f if len(word.strip()) == 5]
    for i in range (0, len(words)):
        words[i] = words[i].replace("á", "a")
        words[i] = words[i].replace("é", "e")
        words[i] = words[i].replace("í", "i")
        words[i] = words[i].replace("ó", "o")
        words[i] = words[i].replace("ú", "u")
        words[i] = words[i].replace("ü", "u")
    return words, random.choice(words)

# FUNCIÓN PARA COMPROBAR QUE LA PALABRA ESTÉ EN LA LISTA
def isInList(lista, seleccion):
    for word in lista:
        if word == seleccion:
            return True
    return False

# FUNCIÓN PARA COMPROBAR LA PALABRA INTRODUCIDA POR EL JUGADOR
def wordchecker(realWord, playerWord):
    result = [RED, RED, RED, RED, RED]
    realWordList = list(realWord)

    # Marcamos las letras correctas en la posición correcta (verdes)
    for i in range(5):
        if playerWord[i] == realWord[i]:
            result[i] = GREEN
            realWordList[i] = None  # Marcamos la letra como usada

    # Verificamos letras correctas en posiciones incorrectas (amarillas)
    for i in range(5):
        if playerWord[i] in realWordList and result[i] == RED:
            result[i] = YELLOW
            realWordList[realWordList.index(playerWord[i])] = None  # Marcamos la letra como usada

    return result


# FUNCIÓN QUE MANEJA LAS RONDAS DE CADA PALABRA
def game_round(lista):
    words, randomWord = generateRandomWord(lista)
    randomWord = randomWord.lower()
    attempt = 0

    while attempt < 6:
        print(f"Round {attempt + 1}/6")
        playerWord = input(">> ").strip().lower()[:5]

        if isInList(words, playerWord.lower()):
            resultList = wordchecker(randomWord, playerWord)

            # Mostrar resultado con colores
            for i in range(5):
                print(f"{BOLD}{resultList[i]}{playerWord[i].upper()}{RESET}", end=" ")
            print("\n")

            # Si el jugador acierta, termina el juego
            if playerWord == randomWord:
                print(f"{GREEN}Congratulations! You guessed the word!{RESET}\n")
                return True

            attempt = attempt + 1

    print(f"{RED}Game over! The word was: {randomWord}{RESET}\n")
    return False


# FUNCIÓN PARA MANEJAR EL RÉCORD
def check_and_update_record(new_score):
    record_file = "record.txt"

    # Intentar leer el récord actual
    try:
        with open(record_file, "r") as file:
            record_score = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        record_score = 0  # Si no existe el archivo o tiene valores inválidos, el récord es 0

    # Comparar y actualizar si es un nuevo récord
    if new_score > record_score:
        with open(record_file, "w") as file:
            file.write(str(new_score))
        print(f"{GREEN}New record! Your score: {new_score}{RESET}")
    else:
        print(f"{YELLOW}Your score: {new_score}. Record to beat: {record_score}{RESET}")


# FUNCIÓN QUE MANEJA EL MODO COMPETITIVO
def competitive(player1, player2, roundNumber):
    for i in range (0, roundNumber):
        pass


# PROGRAMA PRINCIPAL

words = []

printMenu()
gamemode = int(input(f"SELECT A GAME MODE:\n1 - Default mode\n2 - Hard mode\n3 - Two player mode\n4 - COMPETITIVE\n>> "))

if gamemode < 1 or gamemode > 3:
    print(f"{RED}Invalid selection, default game mode selected{RESET}\n")
    gamemode = 1

if gamemode == 1:
    victory = game_round(diccionario)

elif gamemode == 2:
    victory = game_round(diccionario)
    """
    victory = True
    score = -1
    while victory:
        score += 1
        victory = game_round(diccionario)

    print(f"SCORE: {score}")
    check_and_update_record(score)
    """

elif gamemode == 4:
    player1 = input(f"Enter player 1 name\n>> ")
    player2 = input(f"Enter player 2 name\n>> ")
    roundNumber = int(input(f"How many rounds do you want to play?\n>> "))
    competitive(player1, player2, roundNumber)