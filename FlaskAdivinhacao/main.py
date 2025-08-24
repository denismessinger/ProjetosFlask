# This is a sample Python script.
import random


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def jogar_adivinhacao():
    numero_secreto = random.randrange(1, 101, 1)
    total_de_tentativas = 0
    pontos = 100
    print("Qual o nivel de dificuldade?")
    print("{1} Facil {2}Medio {3} Dificil")
    nivel = int(input("Defina o nivel: "))
    if (nivel == 1):
        total_de_tentativas = 20
    elif (nivel == 2):
        total_de_tentativas = 10
    else:
        total_de_tentativas = 5

    laco_for = True
    if (laco_for):
        for tentativa in range(1, total_de_tentativas + 1):
            print("Tentativa {} de {}".format(tentativa, total_de_tentativas))
            valor = input("Digite o seu numero entre 1 e 100: ")
            numero = int(valor)
            if (numero < 1 or numero > 100):
                print("Digite um numero entre 1 e 100")
                continue
            acertou = numero == numero_secreto
            maior = numero_secreto < numero
            menor = numero_secreto > numero
            if (acertou):
                print("Parabens voce fez {} pontos".format(pontos))
                break
            else:
                if (maior):
                    print("Voce errou, o seu chute foi maior")
                elif (menor):
                    print("Voce errou, o seu chute foi menor")
                pontos_perdidos = numero_secreto - int(valor)
                abs(pontos_perdidos)
                pontos = pontos - pontos_perdidos
    else:
        while (tentativa <= total_de_tentativas):
            print("Tentativa {} de {}".format(tentativa, total_de_tentativas))
            valor = input("Digite o seu numero: ")
            numero = int(valor)
            acertou = numero == numero_secreto
            maior = numero_secreto < numero
            menor = numero_secreto > numero
            if (acertou):
                print("Parabens")
                break
            else:
                if (maior):
                    print("Voce errou, o seu chute foi maior")
                elif (menor):
                    print("Voce errou, o seu chute foi menor")
                tentativa = tentativa + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jogar_adivinhacao()
