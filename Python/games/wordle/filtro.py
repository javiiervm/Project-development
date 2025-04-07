def quitartildes(palabra):
    palabra = palabra.replace("á", "a")
    palabra = palabra.replace("é", "e")
    palabra = palabra.replace("í", "i")
    palabra = palabra.replace("ó", "o")
    palabra = palabra.replace("ú", "u")
    palabra = palabra.replace("ä", "a")
    palabra = palabra.replace("ë", "e")
    palabra = palabra.replace("ï", "i")
    palabra = palabra.replace("ö", "o")
    palabra = palabra.replace("ü", "u")
    return palabra

if __name__ == '__main__':
    with open("0_palabras_todas.txt", "r", encoding="utf-8") as f:
        words = set()
        for word in f:
            if len(word.strip()) == 6:
                words.add(quitartildes(word.strip().lower()))

    with open("lista6.txt", "a", encoding="utf-8") as f2:
        for word in words:
            f2.write(f"{word}\n")



