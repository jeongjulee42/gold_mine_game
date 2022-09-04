# 게임 오버 처리. 60초 타임아웃. 시간 0 일때 목표점수와 현재점수 비교하여 성공, 실패 처리
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


class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        rad_angle = math.radians(angle)
        r = self.rect.size[0] // 2
        to_x = r * math.cos(rad_angle)
        to_y = r*math.sin(rad_angle)

        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_gemstone():
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


def update_score(score):
    global curr_score
    curr_score += score


def display_score():
    txt_curr_score = game_font.render(
        f"Curr Score : {curr_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 20))

    txt_goal_score = game_font.render(
        f"Goal Score : {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80))

# 정의


def display_time(time):
    txt_timer = game_font.render(f"Time:{time}", True, BLACK)
    screen.blit(txt_timer, (1100, 50))


def display_game_over():
    game_font = pygame.font.SysFont("applesymbols", 60)  # 큰 폰트 적용
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(
        center=(screen_width / 2, screen_height/2))  # 화면 중앙에 표시
    screen.blit(txt_game_over, rect_game_over)


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("gold miner")
clock = pygame.time.Clock()

# 게임 폰트 정의
game_font = pygame.font.SysFont("applesymbols", 30)
# pc 설치 폰트정보 확인
# print(pygame.font.get_fonts())

# 점수 관련 변수
goal_score = 1500  # 목표점수
curr_score = 0  # 현재점수

# 게임 오버 관련 변수
game_result = None  # 게임 결과
total_time = 40  # 총 시간
start_ticks = pygame.time.get_ticks()


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
    pygame.image.load(os.path.join(
        current_path, "small_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(
        current_path, "big_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "diamond.png")).convert_alpha()]

gemstone_group = pygame.sprite.Group()

setup_gemstone()


claw_image = pygame.image.load(os.path.join(
    current_path, "claw.png")).convert_alpha()
claw = Claw(claw_image, (screen_width//2, 110))


running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if claw.direction != STOP:  # 조건 추가 : 집게가 좌우로 이동중일 때만 마우스 이벤트 처리
                claw.set_direction(STOP)
                to_x = move_speed

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state()
        if caught_gemstone:
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    if not caught_gemstone:
        for gemstone in gemstone_group:
            if pygame.sprite.collide_mask(claw, gemstone):
                caught_gemstone = gemstone
                to_x = -gemstone.speed
                break
    if caught_gemstone:
        caught_gemstone.set_position(
            claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)

    claw.update(to_x)
    claw.draw(screen)

    display_score()

    # 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # ms -> s
    display_time(total_time - elapsed_time)  # 시간 표시

    # 게임 종료 처리
    if total_time - int(elapsed_time) <= 0:
        running = False
        if curr_score >= goal_score:
            game_result = "mission complete".upper()
        else:
            game_result = "game over".upper()

        # 게임 종료 메시지 표시
        display_game_over()

    pygame.display.update()

pygame.time.delay(2000)  # 2초 대기
pygame.quit()
