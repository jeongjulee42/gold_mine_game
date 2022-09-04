# 충돌처리 - 끌고오는동안은 충돌처리를 하지 않도록 정보를 저장해둬야한다
from turtle import pos
import pygame
import os
import math


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

    def update(self, to_x):
        if self.direction == LEFT:
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x

        self.rotate()

    def rotate(self):

        self.image = pygame.transform.rotozoom(
            self.original_image, -self.angle, 1)

        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

# 속도와 가치 정의


class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        # 각도를 호도법으로 변환
        rad_angle = math.radians(angle)  # 각도
        r = self.rect.size[0] // 2  # 반지름
        to_x = r * math.cos(rad_angle)  # 삼각형의 밑변
        to_y = r*math.sin(rad_angle)  # 삼각형의 높이

        self.rect.center = (position[0] + to_x, position[1] + to_y)  # 센터 보정


def setup_gemstone():
    # 정의
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7
    small_gold = Gemstone(
        gemstone_images[0], (200, 380), small_gold_price, small_gold_speed)
    gemstone_group.add(small_gold)
    gemstone_group.add(
        Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed))
    gemstone_group.add(
        Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed))
    gemstone_group.add(
        Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed))

    # 집게에 끌려가는 gemstone 업데이트


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")
clock = pygame.time.Clock()

# 게임 관련 변수
default_offset_x_claw = 40
to_x = 0  # x 좌표 기준으로 집게 이미지를 이동시킬 값을 저장하는 변수
caught_gemstone = None  # 집게를 뻗어 잡은 보석의 정보

# 속도 변수
move_speed = 12  # 발사할때 이동 스피드(x 좌표 기준으로 증가되는 값)
return_speed = 20  # 아무것도 없이 돌아올때 이동 스피드

# 방향 변수
LEFT = -1  # 왼쪽방향
RIGHT = 1  # 오른쪽방향
STOP = 0  # 멈춤
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)
            to_x = move_speed

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state()
        # 원위치에 오면 보석 없애기
        if caught_gemstone:  # 잡힌보석있으면
            # update_score(caught_gemstone.price) # 점수 업데이트 처리
            gemstone_group.remove(caught_gemstone)  # 그룹에서 잡힌 보석은 제외
            caught_gemstone = None

    if not caught_gemstone:  # 잡힌 보석이 없을때 충돌체크
        # 보석 그룹에서 집게이미지와 충돌한게 있는지 체크해보면 된다.
        for gemstone in gemstone_group:
            if claw.rect.colliderect(gemstone.rect):
                caught_gemstone = gemstone  # 잡힌 보석의 정보
                # 집게는 더이상 뻗어나가면 안된다.
                # 잡힌 보석의 종류에 따라 속도가 달라지도록 정의
                to_x = -gemstone.speed  # 잡힌보석의 속도에 - 를 설정
                break
    if caught_gemstone:  # 잡힌 보석있으면 보석 위치를 업데이트하는 매소드
        caught_gemstone.set_position(
            claw.rect.center, claw.angle)  # 집게이미지기준으로 따라가도록

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)

    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
