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
#lista5facil = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista5facil.txt"
#lista5dificil = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista5.txt"
#lista6 = "/home/javier/Personal/scripts/Scripts/Python/games/wordle/lista6.txt"
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
def generateRandomWord(lista, word_length=5):
    with open(lista, encoding="utf-8") as f:
        words = [word.strip().lower() for word in f if len(word.strip()) == word_length]
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
    result = [RED] * len(realWord)
    realWordList = list(realWord)

    # Marcamos las letras correctas en la posición correcta (verdes)
    for i in range(len(realWord)):
        if playerWord[i] == realWord[i]:
            result[i] = GREEN
            realWordList[i] = None  # Marcamos la letra como usada

    # Verificamos letras correctas en posiciones incorrectas (amarillas)
    for i in range(len(realWord)):
        if playerWord[i] in realWordList and result[i] == RED:
            result[i] = YELLOW
            realWordList[realWordList.index(playerWord[i])] = None  # Marcamos la letra como usada

    return result

# FUNCIÓN QUE MANEJA LAS RONDAS DE CADA PALABRA
def game_round(lista, word_length=5):
    words, randomWord = generateRandomWord(lista, word_length=word_length)
    randomWord = randomWord.lower()
    attempt = 0

    # Initialize alphabet tracking (A-Z as WHITE)
    alphabet_status = {chr(i): "\033[97m" for i in range(ord('a'), ord('z') + 1)}  # White color

    while attempt < 6:
        print(f"Round {attempt + 1}/6")
        playerWord = input(">> ").strip().lower()[:word_length]

        if isInList(words, playerWord.lower()):
            resultList = wordchecker(randomWord, playerWord)

            # Mostrar resultado con colores
            for i in range(word_length):
                print(f"{BOLD}{resultList[i]}{playerWord[i].upper()}{RESET}", end=" ")
            print("\n")

            # Update alphabet tracking
            for i, letter in enumerate(playerWord):
                if resultList[i] == GREEN:
                    alphabet_status[letter] = GREEN
                elif resultList[i] == YELLOW and alphabet_status[letter] != GREEN:
                    alphabet_status[letter] = YELLOW
                elif resultList[i] == RED and alphabet_status[letter] not in [GREEN, YELLOW]:
                    alphabet_status[letter] = RED

            # Print updated alphabet
            print_alphabet_status(alphabet_status)

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

# NUEVAS FUNCIONES PARA LOS MODOS DE JUEGO ADICIONALES

# FUNCIÓN PARA EL MODO HARD
def hard_mode(diccionario):
    score = 0
    while True:
        if game_round(diccionario):
            score += 1
        else:
            break
    print(f"SCORE: {score}")
    check_and_update_record(score)

# FUNCIÓN PARA EL MODO 2 JUGADORES
def two_player_mode(diccionario):
    players = ["Player 1", "Player 2"]
    turn = 0
    while True:
        print(f"{players[turn % 2]}'s turn:")
        if not game_round(diccionario):
            print(f"{RED}{players[(turn + 1) % 2]} wins!{RESET}")
            break
        turn += 1

"""
# FUNCIÓN PARA EL MODO COMPETITIVO
def competitive_mode(diccionario):
    num_words = int(input("Enter the number of words to guess: "))
    players = ["Player 1", "Player 2"]
    players[0] = input(f"Enter player 1 name:\n>> ")
    players[1] = input(f"Enter player 2 name:\n>> ")
    scores = [0, 0]
    for i in range(num_words):
        print(f"Word {i + 1}/{num_words}")
        turn = i % 2
        while True:
            print(f"{players[turn % 2]}'s turn:")
            #if game_round(diccionario, word_length=6):
            if game_round(diccionario, word_length=5):
                scores[turn % 2] += 1
                break
            turn += 1
    print(f"Final Scores: {players[0]}: {scores[0]}, {players[1]}: {scores[1]}")
    if scores[0] > scores[1]:
        print(f"{GREEN}{players[0]} wins!{RESET}")
    elif scores[1] > scores[0]:
        print(f"{GREEN}{players[1]} wins!{RESET}")
    else:
        print(f"{YELLOW}It's a tie!{RESET}")
"""
"""
# Competitive mode with unlimited attempts and alternating turns
def competitive_mode(diccionario):
    print("")
    num_words = int(input("Enter the number of words to guess: "))
    players = [input(f"Enter player 1 name:\n>> "), input(f"Enter player 2 name:\n>> ")]
    scores = [0, 0]

    for word_index in range(num_words):
        print(f"{BOLD}\nWORD {word_index + 1}/{num_words}{RESET}\n")
        words, randomWord = generateRandomWord(diccionario, word_length=5)
        randomWord = randomWord.lower()

        guess_count = 0
        while True:
            current_player = guess_count % 2  # Alternate between players
            print(f"{players[current_player]}'s turn:")
            playerWord = input(">> ").strip().lower()[:5]

            if not isInList(words, playerWord):
                print(f"{RED}Word not in list. Try again.{RESET}")
                continue

            resultList = wordchecker(randomWord, playerWord)

            # Display colored feedback
            for i in range(5):
                print(f"{BOLD}{resultList[i]}{playerWord[i].upper()}{RESET}", end=" ")
            print("\n")

            if playerWord == randomWord:
                print(f"{GREEN}{players[current_player]} guessed the word correctly!{RESET}")
                scores[current_player] += 1
                break

            guess_count += 1

    # Final scores
    print(f"\nFinal Scores: {players[0]}: {scores[0]}, {players[1]}: {scores[1]}")
    if scores[0] > scores[1]:
        print(f"{GREEN}{players[0]} wins!{RESET}")
    elif scores[1] > scores[0]:
        print(f"{GREEN}{players[1]} wins!{RESET}")
    else:
        print(f"{YELLOW}It's a tie!{RESET}")
"""

# Competitive mode with unlimited attempts and alternating turns

def print_alphabet_status(alphabet_status):
    """Prints the alphabet with colors indicating known statuses."""
    #print("Alphabet status:")
    for letter, color in alphabet_status.items():
        print(f"{BOLD}{color}{letter.upper()}{RESET}", end=" ")
    print("\n")

def competitive_mode(diccionario):
    print("")
    num_words = int(input("Enter the number of words to guess: "))
    players = [input(f"Enter player 1 name:\n>> "), input(f"Enter player 2 name:\n>> ")]
    scores = [0, 0]

    for word_index in range(num_words):
        print(f"\nWord {word_index + 1}/{num_words}")
        words, randomWord = generateRandomWord(diccionario, word_length=5)
        randomWord = randomWord.lower()

        # Initialize alphabet tracking (A-Z as WHITE)
        alphabet_status = {chr(i): "\033[97m" for i in range(ord('a'), ord('z') + 1)}  # White color

        guess_count = 0
        while True:
            current_player = guess_count % 2
            print(f"{players[current_player]}'s turn:")
            playerWord = input(">> ").strip().lower()[:5]

            if not isInList(words, playerWord):
                print(f"{RED}Word not in list. Try again.{RESET}")
                continue

            resultList = wordchecker(randomWord, playerWord)

            # Display colored feedback
            for i in range(5):
                print(f"{BOLD}{resultList[i]}{playerWord[i].upper()}{RESET}", end=" ")
            print("\n")

            # Update alphabet tracking
            for i, letter in enumerate(playerWord):
                if resultList[i] == GREEN:
                    alphabet_status[letter] = GREEN
                elif resultList[i] == YELLOW and alphabet_status[letter] != GREEN:
                    alphabet_status[letter] = YELLOW
                elif resultList[i] == RED and alphabet_status[letter] not in [GREEN, YELLOW]:
                    alphabet_status[letter] = RED

            # Print updated alphabet
            print_alphabet_status(alphabet_status)

            if playerWord == randomWord:
                print(f"{GREEN}{players[current_player]} guessed the word correctly!{RESET}")
                scores[current_player] += 1
                break

            guess_count += 1

    # Final scores
    print(f"\nFinal Scores: {players[0]}: {scores[0]}, {players[1]}: {scores[1]}")
    if scores[0] > scores[1]:
        print(f"{GREEN}{players[0]} wins!{RESET}")
    elif scores[1] > scores[0]:
        print(f"{GREEN}{players[1]} wins!{RESET}")
    else:
        print(f"{YELLOW}It's a tie!{RESET}")

# PROGRAMA PRINCIPAL
words = []

printMenu()
gamemode = int(input(f"SELECT A GAME MODE:\n1 - Default mode\n2 - Hard mode\n3 - Two player mode\n4 - Competitive mode\n>> "))

if gamemode < 1 or gamemode > 4:
    print(f"{RED}Invalid selection, default game mode selected{RESET}\n")
    gamemode = 1

if gamemode == 1:
    victory = game_round(diccionario)
elif gamemode == 2:
    hard_mode(diccionario)
elif gamemode == 3:
    two_player_mode(diccionario)
elif gamemode == 4:
    competitive_mode(diccionario)