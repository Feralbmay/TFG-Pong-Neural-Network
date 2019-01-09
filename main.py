import Pong  # our class
import numpy as np  # math
import Neural
import random
import time
import pickle

# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS = 8 # Posicio de la pilota a les ultimes 5 iteracions i posicio actual de la paelata
NUM_XARXES = 50 #Numero de xarxes
HITS_GOAL = 20 #Nombre de cops objectiu


#Actualitza els imputs de les pilotes, copiant les anteriors posicions de les pilotes i actualitzant l'actual.
def UpdateImputs(x, y, x1, y1, x2, y2, x3, y3, Px, Py):
    
    x4 = x3
    y4 = y3
    
    x3 = x2
    y3 = y2
    
    x2 = x1
    y2 = y1
    
    x1 = x
    y1 = y

    x = Px
    y = Py

    return [x, y, x1, y1, x2, y2, x3, y3, x4, y4]

# Transforma la matriu resultant de la xarxa en un array i retorna l'index del mayor component(accio mes probable)
def getaction(a):
    arr = a.ravel()
    return np.argmax(arr)
        

def main():
    #Inicialitzam la xarxa
    sizes = [IMPUTS, 8,ACTIONS]

    #Inicialitzam el Joc
    game = Pong.PongGame()

    #Copiam la posicio inicial de e la pilota a les nostres variables de imput
    bx = game.getballXposition()
    by = game.getballYposition()
    bx1 = bx
    by1 = by
    bx2 = bx
    by2 = by
    bx3 = bx
    by3 = by
    bx4 = bx
    by4 = by

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
    distances = np.zeros(NUM_XARXES, dtype= np.float32)
    Move = False
    while(max_hit < HITS_GOAL):
        x = 0
        start = time.time()
        while(x < NUM_XARXES):
            if (x != 0):
                start = time.time()
            hits[x] = 0
            distances[x] = 0
            score = -2
            while(score != -1 and hits[x] < HITS_GOAL):
                if ((score != -2 and x != 0) or score != -2):
                    start = time.time()
                # Copiam la posicio actual de la paleta de la qual decidim l'accio
                px, py = game.getPaddlePos()
                #Cream l'array(matriu (n,1)) de imputs de la xarxa
                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [px],[py]])
                # Decidim l'accio cridant a la Xarxa
                Pa = nets[x].feedforward(a)
                action = getaction(Pa)
                # Actualitzam el Frame amb la nova accio
                score, Posx, Posy = game.getNextFrame(action)
                bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx, Posy)
                #Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
                if(game.gethit()):
                    hits[x] = hits[x] + 1
                if(not game.getTop() and action != 0):
                    Move = True
                #
                # time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))

            if(Move and game.getDistancia() != 0):
                distances[x] = 100/ game.getDistancia()
            else:
                distances[x] = 0
            Move = False
            x = x + 1

        copy_nets_dist = nets.copy()
        #Sort hits
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
        #Sort distances
        i = 0
        while (i < distances.__len__()):
            j = i
            while (j < distances.__len__()):
                if (distances[i] < distances[j]):
                    auxc = distances[i]
                    distances[i] = distances[j]
                    distances[j] = auxc
                    auxn = copy_nets_dist[i]
                    copy_nets_dist[i] = copy_nets_dist[j]
                    copy_nets_dist[j] = auxn
                j = j + 1
            i = i + 1
        #Emmagatzemam la xarxa i el nombre de cops
        best_hits.append(hits[0])
        best_nets.append(nets[0])
        print("/Length",best_hits.__len__(),"/ Hits cumu", best_hits)
        max_hit = hits[0]
        #Si cap xarxa a copetjat, generam noves aleatoriament
        if(max_hit == HITS_GOAL):
            game.testTop()
            bx = game.getballXposition()
            by = game.getballYposition()
            bx1 = bx
            by1 = by
            bx2 = bx
            by2 = by
            score = 0
            while(not game.gethit() and score != -1):
                start = time.time()
                # Copiam la posicio actual de la paleta de la qual decidim l'accio
                px, py = game.getPaddlePos()
                # Cream l'array(matriu (n,1)) de imputs de la xarxa
                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [px], [py]])
                # Decidim l'accio cridant a la Xarxa
                Pa = nets[0].feedforward(a)
                action = getaction(Pa)
                # Actualitzam el Frame amb la nova accio
                score, Posx, Posy = game.getNextFrame(action)
                bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx,
                                                                          Posy)
                #time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))

            game.testBotton()
            bx = game.getballXposition()
            by = game.getballYposition()
            bx1 = bx
            by1 = by
            bx2 = bx
            by2 = by
            while(not game.gethit() and score != -1):
                start = time.time()
                # Copiam la posicio actual de la paleta de la qual decidim l'accio
                px, py = game.getPaddlePos()
                # Cream l'array(matriu (n,1)) de imputs de la xarxa
                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [px], [py]])
                # Decidim l'accio cridant a la Xarxa
                Pa = nets[0].feedforward(a)
                action = getaction(Pa)
                # Actualitzam el Frame amb la nova accio
                score, Posx, Posy = game.getNextFrame(action)
                bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx,
                                                                          Posy)
                print(score)
                #time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))
            if(score == -1):
                max_hit = 0

        if(hits[0] == 0):
            n = 0
            while (n < NUM_XARXES):
                nets[n] = Neural.Network(sizes)
                n = n + 1
        elif(max_hit < HITS_GOAL):
            #Copiam les xarxes
            copy_nets = nets.copy()
            #Recorreguem les xarxes
            for i, n in enumerate(nets):
                if(i< NUM_XARXES * 0.8):
                    #Numero aleatori de 0 a la suma de tots el hits
                    num = random.randint(0, hits.sum())
                    aux = 0
                    # Seleccionam l'index de la xarxa corresponent
                    while (num > hits[aux]):
                        num = num - hits[aux]
                        aux = aux + 1
                    #Generam la nova xarxa filla de la xarxa de l'index
                    nets[i] =  copy_nets[aux].generate_child()
                else:
                    num = random.random() * distances.sum()
                    aux = 0
                    # Seleccionam l'index de la xarxa corresponent
                    while (num > distances[aux]):
                        num = num - distances[aux]
                        aux = aux + 1
                    # Generam la nova xarxa filla de la xarxa de l'index
                    nets[i] = copy_nets_dist[aux].generate_child()

        print("/ Hits", best_hits[-1])

    pickle.dump(nets[0],open( "../../Xarxes/xarxa2.nn", "wb"), pickle.HIGHEST_PROTOCOL)




if __name__ == "__main__":
    main()