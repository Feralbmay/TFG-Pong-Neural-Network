import Pong  # our class
import numpy as np  # math
import Neural
import random
# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS = 12 # Posicio de la pilota a les ultimes 5 iteracions i posicio actual de la paelata
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
    sizes = [IMPUTS, 15 ,ACTIONS]

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

    
    while(max_hit < HITS_GOAL):
        x = 0
        while(x < NUM_XARXES):
            hits[x] = 0
            score = 0
            while(score != -1 and hits[x] < HITS_GOAL):
                # Copiam la posicio actual de la paleta de la qual decidim l'accio
                px, py = game.getPaddlePos()
                #Cream l'array(matriu (n,1)) de imputs de la xarxa
                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [bx3], [by3], [bx4], [by4],[px],[py]])
                # Decidim l'accio cridant a la Xarxa
                Pa = nets[x].feedforward(a)
                action = getaction(Pa)
                # Actualitzam el Frame amb la nova accio
                score, Posx, Posy = game.getNextFrame(action)
                bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx, Posy)
                #Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
                if(game.gethit()):
                    hits[x] = hits[x] + 1
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
        print("/ Hits cumu", best_hits)
        max_hit = hits[0]
        #Si cap xarxa a copetjat, generam noves aleatoriament
        if(hits[0] == 0):
            n = 0
            while (n < NUM_XARXES):
                nets[n] = Neural.Network(sizes)
                n = n + 1
        else:
            #Copiam les xarxes
            copy_nets = nets
            #Recorreguem les xarxes
            for i, n in enumerate(nets):
                #Numero aleatori de 0 a la suma de tots el hits
                num = random.randint(0, hits.sum())
                aux = 0
                # Seleccionam l'index de la xarxa corresponent
                while (num > hits[aux]):
                    num = num - hits[aux]
                    aux = aux + 1
                #Generam la nova xarxa filla de la xarxa de l'index    
                nets[i] =  copy_nets[aux].generate_child()
        print("/ Hits", best_hits[-1])



if __name__ == "__main__":
    main()