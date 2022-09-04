# 집게 흔들기
import pygame
import os


class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        # 추가
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(
            default_offset_x_claw, 0)
        self.position = position

        # 변수 추가
        self.direction = LEFT  # 집게의 이동 방향
        self.angle_speed = 2.5  # 집게의 각도 변경 폭( 좌우 이동 속도 )
        self.angle = 10  # 최초 각도 정의. 오른쪽 끝

    def update(self):
        # 추가. 매 프레임마다 호출되어 동작의 변경을 가함.
        if self.direction == LEFT:  # 왼쪽방향으로 이동하고있다면
            self.angle += self.angle_speed  # 이동 속도만큼 각도를 증가.
        elif self.direction == RIGHT:  # 오른쪽 방향으로 이동하고 있다면
            self.angle -= self.angle_speed

        # 10~170도 초과하면 방향 바꾸기
        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT

        self.rotate()  # 회전 처리

        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center=rect_center)

    # 집게 이미지를 각도에 따라 회전시키기.

    def rotate(self):
        # 원본이미지를 바꾸는게 아니라 새로운 이미지를 만드는 pygame
        # -는 위쪽방향이아닌 아래쪽 방향으로 움직이도록 하기 위함. 1->이미지 크기 변경은 없음.
        self.image = pygame.transform.rotozoom(
            self.original_image, -self.angle, 1)
        # 회전 대상 이미지, 회전시킬 각도, 이미지 크기를 명시
        # 새로운 rect 중심좌표를 업데이트 - 새로운 이미지를 만들기 때문에 해줘야한다.
        self.rect = self.image.get_rect(center=self.position)

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
