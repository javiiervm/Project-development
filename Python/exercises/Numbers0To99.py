# Python code that prints all numbers from 0 to 99 in number and text

prefixes = ["twenty-", "thirty-", "fourty-", "fifty-", "sixty-", "seventy-", "eighty-", "ninety-"]
sufixes = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "teen"]
zero = "zero"
preteens = ["ten", "eleven", "twelve", "thir", "four", "fif"]

def makeNumber(number):
    prefixpos = (number // 10) - 2      # División entera
    sufixpos = number % 10              # Resto de la división
    if(sufixpos == 0):
        print(prefixes[prefixpos].rstrip("-"))
    else:
        print(f"{prefixes[prefixpos]}{sufixes[sufixpos-1]}")

def printNumber(number):
    print(number,end=". ")
    if(number == 0):
        print(zero)
    elif(number < 10):
        print(sufixes[number - 1])
    elif(number < 13):
        print(preteens[number - 10])
    elif(number < 16):
        print(f"{preteens[number - 10]}{sufixes[9]}")
    elif(number < 20):
        print(f"{sufixes[number - 11]}{sufixes[9]}")
    else:
        makeNumber(number)

for i in range(100):
    printNumber(i)