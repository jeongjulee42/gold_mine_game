# 집게 중심점기준으로 약간 띄우기. 집게 위치를 주어진값만큼 옮기기
from cProfile import run
from cgitb import small
from email.mime import image
from turtle import position
import pygame
import os

# 작업을 위해 self.rect를 업데이트, rect 정보로 그리기때문!


class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(
            default_offset_x_claw, 0)  # x위치 100만큼 오른쪽으로 이미지를 이동
        self.position = position

    def update(self):
        # offset값을 통해 rect 업데이트 함수
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center=rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # 중심점확인을 위해 중심점 그리기
        pygame.draw.circle(screen, RED, self.position, 3)


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
default_offset_x_claw = 40  # 중심점으로부터 집게까지의 기본 x 간격
# 색깔 변수
RED = (255, 0, 0)


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

    # 업데이트 먼저하고 그리기
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
