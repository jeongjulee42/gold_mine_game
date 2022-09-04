# 배경이미지 집어넣기
from cProfile import run
import pygame
import os
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")
clock = pygame.time.Clock()

# 배경이미지 불러오기.
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))


running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경이미지 적용
    screen.blit(background, (0, 0))

    pygame.display.update()

pygame.quit()
