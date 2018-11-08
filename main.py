import Pong  # our class
import numpy as np  # math
import Neural

# hyper params
ACTIONS = 3  # up,down, stay
IMPUTS = 12 # Posicio de la pilota a les ultimes 5 iteracions i posicio actual de la paelata

#Actualitza els imputs de les pilotes, copiant les anteriors posicions de les pilotes i actualitzant l'actual.
def UpdateImputs(x, y, x1, y1, x2, y2, x3, y3, x4, y4, Px, Py):
    
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
    NL = Neural.Network(sizes)

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

    
    while(1):
        # Copiam la posicio actual de la paleta de la qual decidim l'accio
        px, py = game.getPaddlePos()
        #Cream l'array(matriu (n,1)) de imputs de la xarxa
        a = np.asarray([[bx], [by], [bx1], [by1], [bx2], [by2], [bx3], [by3], [bx4], [by4],[px],[py]])
        # Decidim l'accio cridant a la Xarxa
        Pa = NL.feedforward(a)
        action = getaction(Pa)
        # Actualitzam el Frame amb la nova accio
        score, Posx, Posy = game.getNextFrame(action)
        bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4 = UpdateImputs(bx, by, bx1, by1, bx2, by2, bx3, by3, bx4, by4, Posx, Posy)

        #Debug
        print( "/ ACTION", action, "/Array", Pa )


if __name__ == "__main__":
    main()