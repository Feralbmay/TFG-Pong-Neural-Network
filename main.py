import Pong  # our class
import numpy as np  # math
import Neural
import random
import time
import pickle
# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS = 4 # Posicio de la pilota a les ultimes posicio actual de la paelata i la pilota
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

    #Inicialitzam el Joc
    game = Pong.PongGame()

    # Copiam la posicio inicial de e la pilota a les nostres variables de imput
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

    Net = pickle.load(open("../../Xarxes/xarxaAN_2.nn", "rb"))
    print(Net.sizes)

    game.setWall_angle_2()
    game.TestMode()
    x = 0
    h = 0
    while(x < 1000):
        start = time.time()
        # Copiam la posicio actual de la paleta de la qual decidim l'accio
        px, py = game.getPaddlePos()
        # Cream l'array(matriu (n,1)) de imputs de la xarxa
        if(Net.sizes[0] == 12):
            a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [bx3], [by3], [bx4], [by4], [px], [py]])
        elif(Net.sizes[0] == 8):
            a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [px], [py]])
        elif(Net.sizes[0] == 4):
            a = np.asarray([[bx], [by], [px], [py]])
        # Decidim l'accio cridant a la Xarxa
        Pa = Net.feedforward(a)
        action = getaction(Pa)
        # Actualitzam el Frame amb la nova accio
        score, Posx, Posy = game.getNextFrame(action)
        bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, Posx, Posy)
        # Si la pala ha pegat a la pilota, aumentam els hits de la xarxa
        #time.sleep(max(1. / game.getFPS() - (time.time() - start), 0))
        if(game.gethit()):
            x = x + 1
            h = h + 1
        if(score == -1):
            x = x + 1

    print(h/x * 100)










if __name__ == "__main__":
    main()