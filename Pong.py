import pygame  # helps us make GUI games in python
import random  # help us define which direction the ball will start moving in

# Primera versio del projecte de xarxes neuronals aplicades al pong
# Aquest arxiu conte la part del codi que regula el joc, la xarxa
# es a un arxiu apart.
# Aquesta primera versio no inclou varies xarxes.

# Frame rate
FPS = 240

# Tamany de la finestra
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Tamany de la nostra paleta
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
# distancia del costat
PADDLE_BUFFER = 10

# Tamany de la pilota
BALL_WIDTH = 10
BALL_HEIGHT = 10

# Veliocitat de la pilota
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

# Colors de la pilota
WHITE = (255,  255,  255)
BLACK = (0, 0, 0)

# Inicialitza la nostra finestra
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# La Paleta dreta es una IA
# La Paleta esquerra el nostre agent

# Funcions per pintar
def drawBall(ballXpos, ballYpos):
    ball = pygame.Rect(ballXpos, ballYpos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)

def drawPaddle_left(paddleLYpos):
    paddle_right = pygame.Rect(PADDLE_BUFFER,paddleLYpos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle_right)

def drawPaddle_right(paddleRYpos):
    paddle_left = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddleRYpos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle_left)

def draw_Wall():
    paddle_left = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, 0, PADDLE_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle_left)

# Actualitzam la posicio de la pilota amb les paletes
def updateBall(paddleLYPos, paddleRYPos, ballXPos, ballYPos, ballXDirection, ballYDirection):
    # Actualitzam la posicio X e Y de la pilota
    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED
    score = 0

    # Comproba les colisions de la xarxa.
    # Paralelizar en iteraciones posteriores
    if (
            ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddleLYPos and ballYPos - BALL_HEIGHT <= paddleLYPos + PADDLE_HEIGHT):
        # Cambia de direccio
        if(ballXDirection != 1):
            ballXDirection = 1
            score = 2
    # No colisiona
    elif (ballXPos <= 0):
        # Score negatiu
        ballXDirection = 1
        score = -1
        return [score, paddleLYPos, paddleRYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

    # Comproba les colisions de la IA
    if (
            ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= paddleRYPos and ballYPos - BALL_HEIGHT <= paddleRYPos + PADDLE_HEIGHT):
        # Cambia de direccio
        ballXDirection = -1
    # No Colisiona
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        # Score positiu
        if(ballXDirection != -1):
            ballXDirection = -1
            score = 1
        return [score, paddleLYPos, paddleRYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]


    # Colisiona amb la part superior
    # Mou abaix
    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    # Si colisiona amb la part d'abaix, rebota
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [score, paddleLYPos, paddleRYPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

# Actualitzam la posicio de la pilota amb les paletes
def updateBall_Wall(paddleLYPos, ballXPos, ballYPos, ballXDirection, ballYDirection, BALL_X_SPEED, BALL_Y_SPEED):
    # Actualitzam la posicio X e Y de la pilota
    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED
    score = 0

    # Comproba les colisions de la xarxa.
    # Paralelizar en iteraciones posteriores
    if (
            ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddleLYPos and ballYPos - BALL_HEIGHT <= paddleLYPos + PADDLE_HEIGHT):
        # Cambia de direccio
        if(ballXDirection != 1):
            ballXDirection = 1
            score = 2
    # No colisiona
    elif (ballXPos <= 0):
        # Score negatiu
        ballXDirection = 1
        score = -1
        return [score, paddleLYPos, ballXPos, ballYPos, ballXDirection, ballYDirection, BALL_X_SPEED, BALL_Y_SPEED]

    # Comproba les colisions de la IA
    if (ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER):
        # Cambia de direccio
        BALL_X_SPEED = random.randint(0, 9)
        BALL_Y_SPEED = random.randint(0, PADDLE_SPEED)
        num = random.randint(-1, 1)
        if(num != 0):
            ballYDirection = num
        ballXDirection = -1
    # No Colisiona
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        # Score positiu
        if(ballXDirection != -1):
            ballXDirection = -1
            score = 1
        return [score, paddleLYPos, ballXPos, ballYPos, ballXDirection, ballYDirection, BALL_X_SPEED, BALL_Y_SPEED]


    # Colisiona amb la part superior
    # Mou abaix
    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    # Si colisiona amb la part d'abaix, rebota
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [score, paddleLYPos, ballXPos, ballYPos, ballXDirection, ballYDirection, BALL_X_SPEED, BALL_Y_SPEED]

def updatePaddle_left(action, paddleLYPos):
    #Paralelitzar
    # Adalt
    if (action == 1):
        paddleLYPos = paddleLYPos - PADDLE_SPEED
    # Abaix
    if (action == 2):
        paddleLYPos = paddleLYPos + PADDLE_SPEED

    if (paddleLYPos < 0):
        paddleLYPos = 0
    if (paddleLYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddleLYPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddleLYPos


def updatePaddle_right(paddleRYPos, ballYPos):
    # Mou la paleta si la bola es adalt
    if (paddleRYPos + PADDLE_HEIGHT / 2 < ballYPos + BALL_HEIGHT / 2):
        paddleRYPos = paddleRYPos + PADDLE_SPEED
    # Mou la paleta si la bola es abaix
    if (paddleRYPos + PADDLE_HEIGHT / 2 > ballYPos + BALL_HEIGHT / 2):
        paddleRYPos = paddleRYPos - PADDLE_SPEED
    # Colisiona amb la part inferior
    if (paddleRYPos < 0):
        paddleRYPos = 0
        # Colisiona amb la part superior
    if (paddleRYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddleRYPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddleRYPos

class PongGame:
    def __init__(self):
        # Direccio de la pilota
        num = random.randint(0, 9)
        # Mantener el score
        self.tally = 0
        self.hit = False
        self.wall = False
        # iniciam la pala
        # Si tenim mes de una paleta(es pasara a l'init)
        # self.number_paddle = np
        # self.paddleLYPos = []
        # for i in range(self.number_paddle):
        #       self.paddleLYPos[i] = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddleLYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddleRYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        #  i la direccio de la pilota
        self.ballXDirection = 1
        self.ballYDirection = 1
        # punt de partida
        self.ballXPos = WINDOW_WIDTH / 2 - BALL_WIDTH / 2

        if (0 < num < 3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if (3 <= num < 5):
            self.ballXDirection = -1
            self.ballYDirection = 1
        if (5 <= num < 8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if (8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1

        num = random.randint(0, 9)
        # On Començara
        self.ballYPos = num * (WINDOW_HEIGHT - BALL_HEIGHT) / 9



    def getNextFrame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        self.hit = False
        # Actualitzam la nostra pala
        self.paddleLYPos = updatePaddle_left(action, self.paddleLYPos)
        drawPaddle_left(self.paddleLYPos)
        # Actualitzam la IA
        if(self.wall):
            draw_Wall()
            [score, self.paddleLYPos, self.ballXPos, self.ballYPos, self.ballXDirection,self.ballYDirection,
             self.BALL_X_SPEED, self.BALL_Y_SPEED] = updateBall_Wall(self.paddleLYPos, self.ballXPos, self.ballYPos,
                                                                     self.ballXDirection,self.ballYDirection,
                                                                     self.BALL_X_SPEED, self.BALL_Y_SPEED)
        else:
            # Actualitzam la pilota
            self.paddleRYPos = updatePaddle_right(self.paddleRYPos, self.ballYPos)
            drawPaddle_right(self.paddleRYPos)
            [score, self.paddleLYPos, self.paddleRYPos, self.ballXPos, self.ballYPos, self.ballXDirection,
             self.ballYDirection] = updateBall(self.paddleLYPos, self.paddleRYPos, self.ballXPos, self.ballYPos,
                                               self.ballXDirection, self.ballYDirection)

        # Pintam la pilota
        drawBall(self.ballXPos, self.ballYPos)
        # Copiam la data de imatge
        # image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        # Actualitzam la finestra
        pygame.display.flip()
        # Actualitzam la puntuacio total
        if(score == 2):
            score = 0
            self.hit = True
        self.tally = self.tally + score
        print
        "Tally is " + str(self.tally)
        # Retornam l'Score i la posicio de la pilota
        return [score, self.ballXPos, self.ballYPos]

    # Funcions de posicionament auxiliar per a la xarxa
    def getballXposition(self):
        return self.ballXPos

    def getballYposition(self):
        return self.ballYPos

    def getPaddlePos(self):
        return [self.paddleLYPos, PADDLE_BUFFER]

    def gethit(self):
        return self.hit

    def getFPS(self):
        return FPS

    def setWall(self):
        self.wall = True
        self.BALL_X_SPEED = BALL_X_SPEED
        self.BALL_Y_SPEED = BALL_Y_SPEED



