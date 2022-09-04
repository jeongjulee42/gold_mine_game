# 집게 발사
# 현재위치로부터 집게를 뻗는 동작
# 화면 밖으로 벗어나면 다시 돌아오도록 처리
# 뻗을때 속도, 돌아올때 속도 다르게 적용
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

        # 추가
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
        self.offset.x = default_offset_x_claw  # 초기화
        # 각도 초기화
        self.angle = 10
        self.direction = LEFT


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
to_x = 0  # x 좌표 기준으로 집게 이미지를 이동시킬 값을 저장하는 변수

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
        # 키 누르면 발사
        if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼 누를때 집게를 뻗음
            # 좌우로 움직이는거 멈춤
            claw.set_direction(STOP)
            to_x = move_speed  # 이만큼 빠르게 쭉 뻗음

    # 바깥 경계 처리
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    # 원상복구
    if claw.offset.x < default_offset_x_claw:  # 원위치에 오면
        to_x = 0
        # 초기화
        claw.set_init_state()  # 처음상태로 되돌림

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)

    # to_x 값에 따라 바뀌도록 전달인자로 넣어줘서 update함수에서 처리
    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
