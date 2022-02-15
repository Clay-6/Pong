from random import randint
import sys
import pygame

# Setup
pygame.init()
SCORE_FONT = pygame.font.SysFont("century", 40)
WIN_FONT = pygame.font.SysFont("algerian", 100)
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()

# Constants
FPS = 60
PADDLE_SIZE = (5, 100)
BALL_RADIUS = 5
P1_START = (20, HEIGHT // 2 - PADDLE_SIZE[1] // 2)
P2_START = (WIDTH - 20, HEIGHT // 2 - PADDLE_SIZE[1] // 2)
MOVEMENT_SPEED = 10
POINTS_TO_WIN = 10


# Player classes
class Paddle:
    def __init__(self, start_pos: tuple, screen: pygame.Surface, size: tuple):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.screen = screen
        self.image = pygame.Surface(size)
        self.image.fill("purple")
        self.rect = self.image.get_rect()

    def Draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Player1(Paddle):
    def __init__(self, start_pos: tuple, screen: pygame.Surface, size: tuple):
        super().__init__(start_pos, screen, size)

    def Move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y - MOVEMENT_SPEED > 0:
            self.y -= MOVEMENT_SPEED
        if keys[pygame.K_s] and self.y + MOVEMENT_SPEED + PADDLE_SIZE[1] < HEIGHT:
            self.y += MOVEMENT_SPEED


class Player2(Paddle):
    def __init__(self, start_pos: tuple, screen: pygame.Surface, size: tuple):
        super().__init__(start_pos, screen, size)

    def Move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y - MOVEMENT_SPEED > 0:
            self.y -= MOVEMENT_SPEED
        if keys[pygame.K_DOWN] and self.y + MOVEMENT_SPEED + PADDLE_SIZE[1] < HEIGHT:
            self.y += MOVEMENT_SPEED


# Ball class
class Ball:
    COLOUR = (255, 0, 0)
    rng = randint(1, 50)
    if rng % 2 == 0:
        MAX_VEL = 5
    else:
        MAX_VEL = -5

    def __init__(self, x: int, y: int, radius: float, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.radius = radius
        self.screen = screen

    def Draw(
        self,
    ):
        pygame.draw.circle(self.screen, self.COLOUR, (self.x, self.y), self.radius)

    def Move(self):
        self.x += self.x_vel
        self.y += self.y_vel


# Collision function
def HandleCollision(ball: Ball, paddle1: Player1, paddle2: Player2):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= paddle1.y and ball.y <= paddle1.y + PADDLE_SIZE[1]:
            if ball.x - ball.radius <= paddle1.x + PADDLE_SIZE[0]:
                ball.x_vel *= -1
                middle_y = paddle1.y + PADDLE_SIZE[1] / 2
                y_diff = middle_y - ball.y
                reduct_factor = (PADDLE_SIZE[1] / 2) / ball.MAX_VEL
                y_vel = y_diff / reduct_factor
                ball.y_vel = y_vel * -1
    else:
        if ball.y >= paddle2.y and ball.y <= paddle2.y + PADDLE_SIZE[1]:
            if ball.x + ball.radius >= paddle2.x + PADDLE_SIZE[0]:
                ball.x_vel *= -1
                middle_y = paddle1.y + PADDLE_SIZE[1] / 2
                y_diff = middle_y - ball.y
                reduct_factor = (PADDLE_SIZE[1] / 2) / ball.MAX_VEL
                y_vel = y_diff / reduct_factor
                ball.y_vel = y_vel * -1


# Draw function
def Draw(player1: Player1, player2: Player2, ball: Ball, p1_score: int, p2_score: int):
    # Drawbackground & midline
    SCREEN.fill((0, 0, 0))
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(SCREEN, (255, 255, 255), (WIDTH // 2 - 5, i, 10, 15))
    # Draw points
    player1_score = SCORE_FONT.render(f"{p1_score}", 1, (255, 255, 255))
    player2_score = SCORE_FONT.render(f"{p2_score}", 1, (255, 255, 255))
    SCREEN.blit(
        player1_score, (WIDTH // 2 - WIDTH // 4 - player1_score.get_width(), 10)
    )
    SCREEN.blit(player2_score, (WIDTH - WIDTH // 4 - player2_score.get_width(), 10))
    # Draw players & ball
    player1.Draw()
    player2.Draw()
    ball.Draw()

    pygame.display.update()


def main():
    p1 = Player1(P1_START, SCREEN, PADDLE_SIZE)
    p2 = Player2(P2_START, SCREEN, PADDLE_SIZE)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, SCREEN)
    p1_score = 0
    p2_score = 0

    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Scoring
        if ball.x < 0:
            p2_score += 1
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball.y_vel = 0
            p1.x, p1.y = P1_START[0], P1_START[1]
            p2.x, p2.y = P2_START[0], P2_START[1]
            pygame.time.wait(500)
        elif ball.x > WIDTH:
            p1_score += 1
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball.y_vel = 0
            p1.x, p1.y = P1_START[0], P1_START[1]
            p2.x, p2.y = P2_START[0], P2_START[1]
            pygame.time.wait(500)
        if p1_score == 10:
            p1_win = WIN_FONT.render("Player 1 wins!", 1, (255, 255, 255))
            SCREEN.blit(
                p1_win,
                (
                    WIDTH // 2 - p1_win.get_width() // 2,
                    HEIGHT // 2 - p1_win.get_height() // 2,
                ),
            )
            pygame.display.update()
            pygame.time.wait(2000)
            main()
        elif p2_score == 10:
            p2_win = WIN_FONT.render("Player 2 wins!", 1, (255, 255, 255))
            SCREEN.blit(
                p2_win,
                (
                    WIDTH // 2 - p2_win.get_width() // 2,
                    HEIGHT // 2 - p2_win.get_height() // 2,
                ),
            )
            pygame.display.update()
            pygame.time.wait(2000)
            main()

        # Function calls
        p1.Move()
        p2.Move()
        ball.Move()
        HandleCollision(ball, p1, p2)
        Draw(p1, p2, ball, p1_score, p2_score)


if __name__ == "__main__":
    main()
