import Pong  # our class
import numpy as np  # math
import Neural
import random
import time

# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS1 = 12 # Posicio de la pilota a les ultimes 5 iteracions i posicio actual de la paelata
IMPUTS2 = 4 #Posicio Actual de la pilota y la pala
IMPUTS3 = 8 # 3 posicions de la pilota + pala
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
    #Preparam les mides de les xarxes
    Imputs = [IMPUTS1, IMPUTS2, IMPUTS3]
    HiddenLayer = [4, 8, 15, 45]

    #Cream la llista que emagetzamara el nombre de generacions de cada xaxa
    gen = []

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

    IM = 0
    while(IM < Imputs.__len__()):
        HL = 0
        while(HL < HiddenLayer.__len__()):
            d = 0
            while( d < 20 ):
                #Inicialitzam la xarxa
                sizes = [Imputs[IM], HiddenLayer[HL] ,ACTIONS]

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
                while(max_hit < HITS_GOAL and best_hits.__len__() < 3000):
                    x = 0
                    start = time.time()
                    while(x < NUM_XARXES and max_hit < HITS_GOAL):
                        if (x != 0):
                            start = time.time()
                        hits[x] = 0
                        score = -2
                        while(score != -1 and max_hit < HITS_GOAL):
                            if ((score != -2 and x != 0) or score != -2):
                                start = time.time()
                            # Copiam la posicio actual de la paleta de la qual decidim l'accio
                            px, py = game.getPaddlePos()
                            if(IM == 0):
                                #Cream l'array(matriu (n,1)) de imputs de la xarxa
                                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [bx3], [by3], [bx4], [by4],[px],[py]])
                            elif(IM == 1):
                                a = np.asarray([[bx], [by], [px], [py]])
                            else:
                                a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [px], [py]])
                            # Decidim l'accio cridant a la Xarxa
                            Pa = nets[x].feedforward(a)
                            action = getaction(Pa)
                            # Actualitzam el Frame amb la nova accio
                            score, Posx, Posy = game.getNextFrame(action)
                            bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx, Posy)
                            #Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
                            if(game.gethit()):
                                hits[x] = hits[x] + 1
                                if(hits[x]> max_hit):
                                    max_hit = hits[x]
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
                            if(i < nets.__len__()*0.8):
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
                                # Numero aleatori de 0 a la suma de tots el hits
                                num = random.randint(0, nets.__len__())
                                aux = 1
                                # Seleccionam l'index de la xarxa corresponent
                                while (num > aux):
                                    aux = aux + 1
                                # Generam la nova xarxa filla de la xarxa de l'index
                                nets[i] = copy_nets[aux-1].generate_child()

                if(best_hits.__len__() == 3000 and max_hit != 20):
                    print("/Case discarded, too much generacions","/Imputs:",Imputs[IM]," /Layer: ", HiddenLayer[HL]," /Length", best_hits.__len__())
                    gen.append(-1)
                else:
                    print("/Imputs:", Imputs[IM], " /Layer: ", HiddenLayer[HL], " /Length", best_hits.__len__(),
                     )
                    gen.append(best_hits.__len__())
                d = d + 1
            HL = HL + 1
        IM = IM + 1
    print(gen)






if __name__ == "__main__":
    main()