import sys
import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 16
PADDLE_SPEED = 6
BALL_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vx = BALL_SPEED * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
        self.vy = BALL_SPEED * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

    def update(self, left_paddle, right_paddle):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

        if self.rect.colliderect(left_paddle.rect):
            self.rect.left = left_paddle.rect.right
            self.vx = -self.vx

        if self.rect.colliderect(right_paddle.rect):
            self.rect.right = right_paddle.rect.left
            self.vx = -self.vx

        # Score check
        if self.rect.left <= 0:
            return 'right'
        if self.rect.right >= WIDTH:
            return 'left'
        return None

    def draw(self, surf):
        pygame.draw.ellipse(surf, WHITE, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()

    left = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    font = pygame.font.SysFont(None, 36)
    score_left = 0
    score_right = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            left.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            right.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right.move(PADDLE_SPEED)

        scorer = ball.update(left, right)
        if scorer == 'left':
            score_left += 1
            ball.reset()
        if scorer == 'right':
            score_right += 1
            ball.reset()

        screen.fill(BLACK)
        left.draw(screen)
        right.draw(screen)
        ball.draw(screen)

        score_surf = font.render(f"{score_left}  -  {score_right}", True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
