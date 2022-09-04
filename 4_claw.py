# 집게 클래스 만들기
# 집게 중심점기준으로 약간 띄우기. 집게 위치를 주어진값만큼 옮기기
from cProfile import run
from cgitb import small
from email.mime import image
from turtle import position
import pygame
import os


# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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


current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),
    pygame.image.load(os.path.join(current_path, "big_gold.png")),
    pygame.image.load(os.path.join(current_path, "stone.png")),
    pygame.image.load(os.path.join(current_path, "diamond.png"))]

gemstone_group = pygame.sprite.Group()

setup_gemstone()

# 집게
# 하나이므로 함수 안만들고 처리
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width//2, 110))  # 가로 위치는 화면 절반, 위에서 110픽셀정도 위치


running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    # 객체 그리기, 스프라이트 각각은 draw함수가 없다. 따라서 클래스에 구현
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
