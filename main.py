import pygame
import random
import os
pygame.init()
pygame.font.init()

# SCREEN PARAMETERS
WIDTH = 800
HEIGHT = 800
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
SCREEN_COLOR = (171,219,227)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ping Pong")

# ! MAIN FONTS
score_font = pygame.font.SysFont("comicsans",20) 
game_over_font = pygame.font.SysFont("comicsans",50) 

# ! DISPLAYING OUR SCORE
def display_score(score1,score2):
    player1_score_label = score_font.render(f"Player 1: {score1}", True, (255,255,255))
    player2_score_label = score_font.render(f"Player 2:{score2}", True, (255,255,255))
    screen.blit(player1_score_label, ((WIDTH//2 - player1_score_label.get_width())/2,10))
    screen.blit(player2_score_label, ((3*WIDTH//2 - player2_score_label.get_width())/2,10))

class Object:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Rectangle(Object):
    def __init__(self, x, y,velocity):
        super().__init__(x, y)
        self.vel_Y = velocity

# RECTANGLE PARAMETERS 
RECT_COLOR = (250,122,235)
RECT_BREADTH = 20
RECT_HEIGHT = 100
# BALL PARAMETERS
BALL_COLOR = (0,0,0)
BALL_RADIUS = 20
choice_toGo = (-1,1)
BALL_VEL_X = 1*(random.choice(choice_toGo))
BALL_VEL_Y = 1

# * INSTANTANIZING OUR BALL WITH RANDOM Y SO TO DIFFERENT THROWS
ran = random.randrange(100,400)
ball = Object(WIDTH//2,HEIGHT//2 + ran)

# * INSTANTANIZING OUR PLAYERS
players_vel = .5
player1 = Rectangle(80 - RECT_BREADTH//2,(HEIGHT - RECT_HEIGHT)/2, players_vel)
player2 = Rectangle(WIDTH - 80 - RECT_BREADTH//2,(HEIGHT - RECT_HEIGHT)/2, players_vel)


def circle_show(x,y):
    pygame.draw.circle(screen, BALL_COLOR, (x,y), BALL_RADIUS)
    pass

def rect_show(x,y):
    pygame.draw.rect(screen, RECT_COLOR, [x,y,RECT_BREADTH,RECT_HEIGHT])

def isCollide(ball,rect):
    if (ball.x - BALL_RADIUS <= rect.x) and (ball.x)>=rect.x - RECT_BREADTH:
        if (ball.y)<=rect.y + RECT_HEIGHT and (ball.y + BALL_RADIUS) >= rect.y :
            return True
    return False

def lost_text(lost,score1,score2):
    if lost:
        # print("blitting game over")
        if (score1>score2):
            game_over_label = game_over_font.render("Player1 Wins!", True, (255,255,255))
        elif (score1<score2):
            game_over_label = game_over_font.render("Player2 Wins!", True, (255,255,255))
        else:
            game_over_label = game_over_font.render("Draw!", True, (255,255,255))

        screen.blit(game_over_label, ((WIDTH - game_over_label.get_width())//2,HEIGHT//2))
        
def main():
    global BALL_VEL_X,BALL_VEL_Y
# * GAME LOOP
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    clock.tick(FPS)
    lost = False
    lost_count = 0
    collide_flag_1 = False
    collide_flag_2 = False
    score1,score2 = 0,0
    ran = random.randrange(100,400)
    ball = Object(WIDTH//2,HEIGHT//2 + ran)
    while run:
        if lost:
            lost_count += 1
            # print("Incremented lost count")
            if lost_count > FPS*30:
                run = False
                # print("run is false")
                return
            else:
                lost_text(lost,score1,score2)
                pygame.display.update()
                # print("Inside else")
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # ! MOVING OUR PLAYERS IN Y DIRECTION
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player2.y > 0:
            player2.y -= player2.vel_Y
        if keys[pygame.K_DOWN] and player2.y < HEIGHT - RECT_HEIGHT:
            player2.y += player2.vel_Y
        if keys[pygame.K_w] and player1.y > 0:
            player1.y -= player1.vel_Y
        if keys[pygame.K_s] and player1.y < HEIGHT - RECT_HEIGHT:
            player1.y += player1.vel_Y

        
        
        # ! GIVING RANDOM VALUES OF VEL(X,Y) SO TO HAVE REAL LIFE COLLISIONS.
        screen.fill(SCREEN_COLOR)
        tmp_rand = random.random()
        ball.x += BALL_VEL_X*tmp_rand
        if tmp_rand < 0.5:
            tmp_rand = random.random()
        ball.y += BALL_VEL_Y*tmp_rand

        # ! CONDITION FOR BALL X COLLISION.
        if (ball.x > WIDTH - BALL_RADIUS):
            BALL_VEL_X = BALL_VEL_X * (-1)
        if (ball.y > HEIGHT - BALL_RADIUS):
            BALL_VEL_Y = BALL_VEL_Y * (-1)
        if (ball.y < BALL_RADIUS):
            BALL_VEL_Y = BALL_VEL_Y * (-1)
        if (ball.x < BALL_RADIUS):
            BALL_VEL_X = BALL_VEL_X * (-1)

        # print(ball.x,ball.y)

        # ! DISPLAYING OUR OBJECTS
        circle_show(ball.x,ball.y)
        rect_show(player1.x,player1.y)
        rect_show(player2.x,player2.y)

        # ! CHECKING OUR COLLIDE CONDITIONS
        if isCollide(ball,player1) and not collide_flag_1:
            BALL_VEL_X = BALL_VEL_X * (-1)
            collide_flag_1 = True   
            score1+=1     
            print("Collision1")
        
        if not isCollide(ball,player1):
            collide_flag_1 = False
            
        if isCollide(ball,player2) and not collide_flag_2:
            BALL_VEL_X = BALL_VEL_X * (-1)
            collide_flag_2 = True        
            score2+=1
            print("Collision2")
        
        if not isCollide(ball,player2):
            collide_flag_2 = False
            
        display_score(score1,score2)

        if ball.x < BALL_RADIUS or ball.x > WIDTH - BALL_RADIUS:
            print("game over")
            lost = True
            lost_count += 1
            print("Incremented lost count")
        pygame.display.update()


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True 
    while run:
        screen.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin", 1, (255,255,255))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()