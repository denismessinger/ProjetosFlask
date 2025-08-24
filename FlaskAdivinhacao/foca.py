def jogar_foca():
    print("Apenas um jogo")
    palavra_secreta = "teste"
    forca = False
    acertou = False
    while(not forca and not acertou):
        chute = input("Informe uma letra: ")
        chute = chute.strip()
        index = 0
        for letra in palavra_secreta:
            if(chute.upper() == letra.upper()):
                print("Encontrei a letra {} na posicao {}".format(letra,index))

            index = index + 1

    print("Fim de jogo")

if __name__ == '__main__':
    jogar_foca()
