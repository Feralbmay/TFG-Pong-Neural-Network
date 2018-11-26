import Pong  # our class
import numpy as np  # math
import Neural
import random
import time

# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS = 4 # Posicio de la pilota a les ultimes posicio actual de la paelata i la pilota
NUM_XARXES = 50 #Numero de xarxes
HITS_GOAL = 20 #Nombre de cops objectiu


#Actualitza els imputs de les pilotes, copiant les anteriors posicions de les pilotes i actualitzant l'actual.
def UpdateImputs( Px, Py):

    x = Px
    y = Py

    return [x, y]

# Transforma la matriu resultant de la xarxa en un array i retorna l'index del mayor component(accio mes probable)
def getaction(a):
    arr = a.ravel()
    return np.argmax(arr)
        

def main():
    #Inicialitzam la xarxa
    sizes = [IMPUTS, 8 ,ACTIONS]

    #Inicialitzam el Joc
    game = Pong.PongGame()

    #Copiam la posicio inicial de e la pilota a les nostres variables de imput
    bx = game.getballXposition()
    by = game.getballYposition()

    #Guarda el nombre maxim de cops de la ultima generacio.
    max_hit = 0

    #Cream les llistes on enmagatzamarem les millors xarxes amb el nombre de cops que han assolit
    best_nets = []
    best_hits = []

    #Cream els 2 arrays que emprarem per a les generacions
    nets = []
    n = 0

    while(n < NUM_XARXES):
        nets.append(Neural.Network(sizes))
        n = n+1

    hits = np.zeros(NUM_XARXES, dtype=np.int16)
    while(max_hit < HITS_GOAL):
        x = 0
        start = time.time()
        while(x < NUM_XARXES):
            if (x != 0):
                start = time.time()
            hits[x] = 0
            score = -2
            while(score != -1 and hits[x] < HITS_GOAL):
                if ((score != -2 and x != 0) or score != -2):
                    start = time.time()
                # Copiam la posicio actual de la paleta de la qual decidim l'accio
                px, py = game.getPaddlePos()
                #Cream l'array(matriu (n,1)) de imputs de la xarxa
                a = np.asarray([[bx], [by], [px],[py]])
                # Decidim l'accio cridant a la Xarxa
                Pa = nets[x].feedforward(a)
                action = getaction(Pa)
                # Actualitzam el Frame amb la nova accio
                score, Posx, Posy = game.getNextFrame(action)
                bx, by = UpdateImputs(Posx, Posy)
                #Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
                if(game.gethit()):
                    hits[x] = hits[x] + 1
                #time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))

            x = x + 1
        #Sort
        i = 0
        while(i < hits.__len__()):
            j = i
            while(j < hits.__len__()):
                if(hits[i] < hits[j]):
                    auxc = hits[i]
                    hits[i] = hits[j]
                    hits[j] = auxc
                    auxn = nets[i]
                    nets[i] = nets[j]
                    nets[j] = auxn
                j = j + 1
            i = i + 1
        #Emmagatzemam la xarxa i el nombre de cops
        best_hits.append(hits[0])
        best_nets.append(nets[0])
        print("/Length",best_hits.__len__(),"/ Hits cumu", best_hits)
        max_hit = hits[0]
        #Si cap xarxa a copetjat, generam noves aleatoriament
        if(hits[0] == 0):
            n = 0
            while (n < NUM_XARXES):
                nets[n] = Neural.Network(sizes)
                n = n + 1
        elif(max_hit < HITS_GOAL):
            #Copiam les xarxes
            copy_nets = nets
            #Recorreguem les xarxes
            for i, n in enumerate(nets):
                if (i < nets.__len__() * 0.8):
                    # Numero aleatori de 0 a la suma de tots el hits
                    num = random.randint(0, hits.sum())
                    aux = 0
                    # Seleccionam l'index de la xarxa corresponent
                    while (num > hits[aux]):
                        num = num - hits[aux]
                        aux = aux + 1
                    # Generam la nova xarxa filla de la xarxa de l'index
                    nets[i] = copy_nets[aux].generate_child()
                else:
                    # Numero aleatori de 0 a la suma de tots el hits
                    num = random.randint(0, nets.__len__())
                    aux = 1
                    # Seleccionam l'index de la xarxa corresponent
                    while (num > aux):
                        aux = aux + 1
                    # Generam la nova xarxa filla de la xarxa de l'index
                    nets[i] = copy_nets[aux - 1].generate_child()

        print("/ Hits", best_hits[-1])
    game.setWall()
    while(1):
        start = time.time()
        # Copiam la posicio actual de la paleta de la qual decidim l'accio
        px, py = game.getPaddlePos()
        # Cream l'array(matriu (n,1)) de imputs de la xarxa
        a = np.asarray([[bx], [by], [px], [py]])
        # Decidim l'accio cridant a la Xarxa
        Pa = best_nets[-1].feedforward(a)
        action = getaction(Pa)
        # Actualitzam el Frame amb la nova accio
        score, Posx, Posy = game.getNextFrame(action)
        bx, by = UpdateImputs(Posx, Posy)
        # Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
        time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))
        if(score == -1):
            print ("HIT!!!")








if __name__ == "__main__":
    main()