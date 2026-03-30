import random
LETTERS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0","!", "£", "$","%","^","&","*","(",")","-","_","+","=","]","[","{","}",":",";","@","'","#","~","<",",",">",".","?","/","|","\\"]

def encrypt(word: str):
    n,c,s = len(LETTERS), random.randint(0,1000), random.randint(0,1000)

    og_s = s

    def split_s_times(deck, c):
        left = deck[0:len(deck)//2]
        right = deck[(len(deck)//2)::]
        combined = []
        for i in range(0, len(left)):
            combined.append(right[i])
            combined.append(left[i])
        
        counter = 1
        while counter < c:
            letter = combined.pop(0)
            combined.append(letter)
            counter += 1

        return combined


    def encrypt_letter(alpha, beta, letter):
        new_letter = ""
        while True:
            if alpha[0] == letter:
                new_letter += beta[0]
                al = alpha.pop(1)
                alpha.insert((len(alpha)//2), al)
                bl = beta.pop(0)
                beta.append(bl)
                bl2 = beta.pop(2)
                beta.insert((len(beta)//2), bl2)
                break
            elif alpha[0] != letter:
                shuffle_al = alpha.pop(0)
                alpha.append(shuffle_al)
                shuffle_bl = beta.pop(0)
                beta.append(shuffle_bl)

        return new_letter

    counter = 0
    start = []
    while counter < n: #makes og list
        start.append(LETTERS[counter])
        start.append(LETTERS[counter])
        counter+=1 

    while s > -1: #makes new list
        output = split_s_times(start, c)
        start = output
        s -= 1

    alpha = []
    beta = []

    seen = []
    for i in range(len(start)): #makes A and B lists
        if start[i] in seen:
            beta.append(start[i])
        else:
            seen.append(start[i])
            alpha.append(start[i])

    output = ""

    for letter in word: #encrypts word
        e_letter = encrypt_letter(alpha, beta, letter)
        output += e_letter

    return output,c, og_s

def decrypt(text: str, c: int, s: int):
    n = len(LETTERS)

    def split_s_times(deck, c):
        left = deck[0:len(deck)//2]
        right = deck[(len(deck)//2)::]
        combined = []
        for i in range(0, len(left)):
            combined.append(right[i])
            combined.append(left[i])
        
        counter = 1
        while counter < c:
            letter = combined.pop(0)
            combined.append(letter)
            counter += 1

        return combined

    counter = 0
    start = []
    while counter < n:
        start.append(LETTERS[counter])
        start.append(LETTERS[counter])
        counter += 1

    while s > -1:
        output = split_s_times(start, c)
        start = output
        s -= 1

    alpha = []
    beta = []
    seen = []
    for i in range(len(start)):
        if start[i] in seen:
            beta.append(start[i])
        if start[i] not in seen:
            seen.append(start[i])
            alpha.append(start[i])

    def decrypt_letter(alpha, beta, letter):
        while True:
            if beta[0] == letter:
                new_letter = alpha[0]
                al = alpha.pop(1)
                alpha.insert((len(alpha)//2), al)
                bl = beta.pop(0)
                beta.append(bl)
                bl2 = beta.pop(2)
                beta.insert((len(beta)//2), bl2)
                return new_letter
            else:
                shuffle_al = alpha.pop(0)
                alpha.append(shuffle_al)
                shuffle_bl = beta.pop(0)
                beta.append(shuffle_bl)

    output = ""
    for letter in text:
        output += decrypt_letter(alpha, beta, letter)

    return output
