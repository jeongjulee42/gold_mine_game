# 보석 클래스, 보석이미지 불러오기
from cProfile import run
from cgitb import small
import pygame
import os

# 보석 클래스


class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()  # 상속받았으니 초기화
        # sprite를 받아 쓰기 위해서는 두개의 맴버변수를 정의해주어야한다.
        self.image = image  # 이미지정보
        # 캐릭터정보, 객체를 만들때마다 포지션에 따라 위치가 달라진다. 즉 보석이 나타날 위치.
        self.rect = image.get_rect(center=position)


def setup_gemstone():
    # 작은 금 하나 만들어보기
    # 0번째 이미지를 해당 위치에 둔다.
    # 클래스로 객체 생성. 좌표는 임의로 넣음.
    small_gold = Gemstone(gemstone_images[0], (200, 380))
    # 객체를 그룹에 추가
    gemstone_group.add(small_gold)

    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # 다이아
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")
clock = pygame.time.Clock()


current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),
    pygame.image.load(os.path.join(current_path, "big_gold.png")),
    pygame.image.load(os.path.join(current_path, "stone.png")),
    pygame.image.load(os.path.join(current_path, "diamond.png"))]

# 하나씩 가져와서 캐릭터를 만들지않기.
# 파이게임이 제공해주는 sprite 클래스를 사용.
# 그룹을 사용하면 그룹에 모든 보석을 집어넣고 한번에 처리 (스크린에 그리는것도 반복작업을 하지 않아도 된다.)

# 보석 그룹 만들기
gemstone_group = pygame.sprite.Group()  # 여기에 보석 객체들을 추가해주자.

setup_gemstone()  # 게임에 원하는만큼의 보석을 정의

running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    # 화면에 그룹 한번에 그리기
    gemstone_group.draw(screen)  # 그룹 내 모든 스프라이트를 스크린에 그리기.

    pygame.display.update()

pygame.quit()
