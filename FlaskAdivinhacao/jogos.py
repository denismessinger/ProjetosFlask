import main
import foca

if __name__ == '__main__':
    print("Menu de jogos:")
    print("{1} Foca {2} Adivinhar")
    escolha = input("Escolha o seu jogo :")
    escolha = int(escolha)
    if(escolha == 1):
        main.jogar_adivinhacao()
    elif(escolha == 2):
        foca.jogar_foca()