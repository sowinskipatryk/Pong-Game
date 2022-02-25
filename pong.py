import pygame
pygame.init()

WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
EDGE_DEVIATION = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 50
PADDLE_VELOCITY = 4
BALL_RADIUS = 5
BALL_VELOCITY = 5
BG_COLOR = (255, 255, 0)
OBJ_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont('Arial Black', 24)
FPS = 60
BEST_OF = 3


class Paddle:
    width = PADDLE_WIDTH
    height = PADDLE_HEIGHT
    vel = PADDLE_VELOCITY

    def __init__(self, orig_x, orig_y):
        self.orig_x = orig_x
        self.orig_y = orig_y
        self.x = self.orig_x
        self.y = self.orig_y

    def draw(self):
        pygame.draw.rect(SCREEN, OBJ_COLOR, (self.x, self.y, self.width, self.height))

    def move(self, key_press):
        if key_press == 'up':
            self.y -= self.vel
        if key_press == 'down':
            self.y += self.vel

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y

class Ball:
    width = PADDLE_WIDTH
    height = PADDLE_HEIGHT
    orig_x = WIDTH // 2
    orig_y = HEIGHT // 2
    x = orig_x
    y = orig_y
    orig_vel = BALL_VELOCITY
    vel_x = orig_vel
    vel_y = 0

    def draw(self):
        pygame.draw.circle(SCREEN, OBJ_COLOR, (self.x, self.y), BALL_RADIUS)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def reset(self):
        self.vel_x *= -1
        self.vel_y = 0
        self.x = self.orig_x
        self.y = self.orig_y

def pad_movement(keys, left_pad, right_pad):
    if keys[pygame.K_w] and left_pad.y - left_pad.vel >= 0:
        left_pad.move('up')
    if keys[pygame.K_s] and left_pad.y + PADDLE_HEIGHT + left_pad.vel <= HEIGHT:
        left_pad.move('down')
    if keys[pygame.K_UP] and right_pad.y - right_pad.vel >= 0:
        right_pad.move('up')
    if keys[pygame.K_DOWN] and right_pad.y + PADDLE_HEIGHT + right_pad.vel <= HEIGHT:
        right_pad.move('down')

def bounce(ball, left_paddle, right_paddle):
    if ball.y - BALL_RADIUS <= 0:
        ball.vel_y *= -1
    elif ball.y + BALL_RADIUS >= HEIGHT:
        ball.vel_y *= -1

    if ball.x < left_paddle.x + PADDLE_WIDTH:
        if left_paddle.y < ball.y + BALL_RADIUS and left_paddle.y + PADDLE_HEIGHT > ball.y:
            ball.vel_x *= -1
            diff_y = left_paddle.y + PADDLE_HEIGHT // 2 - ball.y
            coef_y = -diff_y / (PADDLE_HEIGHT // 2)
            ball.vel_y = coef_y * BALL_VELOCITY
    elif ball.x > right_paddle.x:
        if right_paddle.y < ball.y + BALL_RADIUS and right_paddle.y + PADDLE_HEIGHT > ball.y:
            ball.vel_x *= -1
            diff_y = right_paddle.y + PADDLE_HEIGHT // 2 - ball.y
            coef_y = -diff_y / (PADDLE_HEIGHT // 2)
            ball.vel_y = coef_y * BALL_VELOCITY


def show_scores(font, screen, score_left, score_right):
    scoreboard = font.render(f'{score_left}:{score_right}', True, (0, 0, 0))
    screen.blit(scoreboard, (WIDTH // 2 - scoreboard.get_width() // 2, EDGE_DEVIATION // 2))


def draw(win, left_paddle, right_paddle, ball, score_left, score_right):
    win.fill(BG_COLOR)

    show_scores(FONT, win, score_left, score_right)

    left_paddle.draw()
    right_paddle.draw()

    ball.draw()

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    pygame.display.set_caption('Pong')

    left_pad = Paddle(EDGE_DEVIATION, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_pad = Paddle(WIDTH - PADDLE_WIDTH - EDGE_DEVIATION, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    score_left, score_right = 0,0

    game_finished = False
    run = True
    while run:
        clock.tick(FPS)

        draw(SCREEN, left_pad, right_pad, ball, score_left, score_right)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_q]:
                run = False

        pad_movement(keys, left_pad, right_pad)
        ball.move()
        bounce(ball,left_pad,right_pad)

        if ball.x < 0:
            ball.reset()
            left_pad.reset()
            right_pad.reset()
            score_right += 1
        elif ball.x > WIDTH:
            ball.reset()
            left_pad.reset()
            right_pad.reset()
            score_left += 1

        SCREEN.fill(BG_COLOR)
        show_scores(FONT, SCREEN, score_left, score_right)

        if score_left == BEST_OF:
            win_msg = FONT.render('Left paddle wins!', True, (0, 0, 0))
            play_again_msg = FONT.render('Play again? Y/N', True, (0, 0, 0))
            SCREEN.blit(win_msg, (WIDTH // 2 - win_msg.get_width() // 2, HEIGHT // 2 - win_msg.get_height() // 2 - 10))
            SCREEN.blit(play_again_msg, (WIDTH // 2 - play_again_msg.get_width() // 2, HEIGHT // 2 + win_msg.get_height() // 2 - play_again_msg.get_height() // 2))
            pygame.display.flip()
            game_finished = True
        elif score_right == BEST_OF:
            win_msg = FONT.render('Right paddle wins!', True, (0, 0, 0))
            play_again_msg = FONT.render('Play again? Y/N', True, (0, 0, 0))
            SCREEN.blit(win_msg, (WIDTH // 2 - win_msg.get_width() // 2, HEIGHT // 2 - win_msg.get_height() // 2 - 10))
            SCREEN.blit(play_again_msg, (WIDTH // 2 - play_again_msg.get_width() // 2, HEIGHT // 2 + win_msg.get_height() // 2 - play_again_msg.get_height() // 2))
            pygame.display.flip()
            game_finished = True
        while game_finished:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        score_left = 0
                        score_right = 0
                        ball.reset()
                        left_pad.reset()
                        right_pad.reset()
                        game_finished = False
                    elif event.key == pygame.K_n:
                        run = False
                        game_finished = False
    pygame.quit()

if __name__ == '__main__':
    main()
