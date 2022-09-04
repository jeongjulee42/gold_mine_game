# 기본 뼈대
from cProfile import run
import pygame
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")

# 캐릭터 움직임을 위한 fps값 설정
clock = pygame.time.Clock()


running = True
while running:
    clock.tick(30)  # fps값이 30으로 고정.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
