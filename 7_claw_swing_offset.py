# 집게 흔들기 - offset 적용
# 집게 각도가 변할때마다 offset 각도를 변경시켜 적용해주어야 한다.
import pygame
import os


class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image

        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(
            default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT
        self.angle_speed = 2.5
        self.angle = 10

    def update(self):
        if self.direction == LEFT:
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT

        self.rotate()

        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center=rect_center)

    def rotate(self):

        self.image = pygame.transform.rotozoom(
            self.original_image, -self.angle, 1)

        # 추가
        # 옵셋데이터를 각도에 맞춰 회전시킨 새 offset을 받아온다.
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)


class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)


def setup_gemstone():
    small_gold = Gemstone(gemstone_images[0], (200, 380))
    gemstone_group.add(small_gold)
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")
clock = pygame.time.Clock()

# 게임 관련 변수
default_offset_x_claw = 40
LEFT = -1  # 왼쪽방향
RIGHT = 1  # 오른쪽방향
# 색깔 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)


current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),
    pygame.image.load(os.path.join(current_path, "big_gold.png")),
    pygame.image.load(os.path.join(current_path, "stone.png")),
    pygame.image.load(os.path.join(current_path, "diamond.png"))]

gemstone_group = pygame.sprite.Group()

setup_gemstone()


claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width//2, 110))


running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)

    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
