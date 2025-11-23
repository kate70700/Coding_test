"""
강아지 마법사의 꿈 (Dream of the Dog Wizard)
기억 잃은 강아지 마법사가 꿈 속에서 잃어버린 기억 조각들을 모으며
자신의 아픈 과거를 치유하고, 결국 주인과 행복하게 재회하는 게임입니다.
"""

import pygame
import sys
import math

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("강아지 마법사의 꿈")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (138, 115, 166)
DARK_PURPLE = (90, 70, 130)
LIGHT_PURPLE = (200, 180, 220)
PINK = (255, 200, 220)
YELLOW = (255, 220, 100)
GOLD = (255, 215, 0)
DARK_GRAY = (60, 60, 60)
LIGHT_GRAY = (180, 180, 180)
NAVY = (20, 40, 80)
SOFT_BLUE = (150, 180, 220)

# 폰트 설정
try:
    # 한글 폰트 시도
    font_large = pygame.font.Font("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 48)
    font_medium = pygame.font.Font("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 28)
    font_small = pygame.font.Font("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 20)
    font_tiny = pygame.font.Font("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 16)
except:
    try:
        font_large = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_medium = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_small = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_tiny = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = pygame.font.SysFont("malgun gothic", 48)
        font_medium = pygame.font.SysFont("malgun gothic", 28)
        font_small = pygame.font.SysFont("malgun gothic", 20)
        font_tiny = pygame.font.SysFont("malgun gothic", 16)

# 게임 상태
class GameState:
    TITLE = "title"
    MEMORY_SELECT = "memory_select"
    STORY = "story"
    INPUT = "input"
    RESULT = "result"
    ENDING = "ending"

# 기억 조각 데이터
memory_fragments = {
    "neglect": {
        "name": "방치",
        "completed": False,
        "story": [
            "어느 추운 겨울 밤이었어요...",
            "",
            "작은 강아지 하나가 텅 빈 집에 홀로 남겨졌어요.",
            "주인은 몇 날 며칠째 돌아오지 않았고,",
            "물그릇은 바닥나고 배는 고파왔어요.",
            "",
            "강아지는 창문 너머로 지나가는 사람들을 바라보며",
            "언젠가 누군가 자신을 찾아와 주길 기다렸어요.",
            "",
            "\"왜 나를 잊어버린 걸까...\"",
            "강아지는 조용히 눈물을 흘렸어요."
        ],
        "keywords": ["괜찮", "사랑", "혼자", "함께", "잘", "응원", "힘내", "행복", "소중", "미안"],
        "success_message": "따뜻한 위로가 강아지의 마음에 닿았어요..."
    },
    "abuse": {
        "name": "학대",
        "completed": False,
        "story": [
            "그 집의 강아지는 항상 무서웠어요...",
            "",
            "조금만 실수해도 큰 소리가 들려왔고,",
            "아픈 곳이 하나둘 늘어만 갔어요.",
            "",
            "강아지는 사람의 손길이 무서워졌어요.",
            "한때는 그 손이 따뜻했었는데...",
            "",
            "구석에 웅크린 채 작은 몸을 떨면서",
            "강아지는 생각했어요.",
            "",
            "\"나도 사랑받을 수 있을까...?\""
        ],
        "keywords": ["괜찮", "사랑", "아프", "치료", "안전", "보호", "용기", "희망", "극복", "회복"],
        "success_message": "당신의 따뜻한 말이 상처받은 마음을 어루만져 주었어요..."
    },
    "abandon": {
        "name": "유기",
        "completed": False,
        "story": [
            "그날은 드라이브를 가는 줄 알았어요...",
            "",
            "창밖으로 스쳐가는 풍경이 설레었죠.",
            "하지만 차가 멈춘 곳은 낯선 곳이었어요.",
            "",
            "주인은 강아지를 내려놓고",
            "아무 말 없이 떠나버렸어요.",
            "",
            "강아지는 멀어지는 차를 바라보며",
            "있는 힘껏 뛰어갔지만...",
            "결국 지쳐 쓰러지고 말았어요.",
            "",
            "\"내가 뭘 잘못한 걸까...\""
        ],
        "keywords": ["사랑", "가족", "집", "새로운", "희망", "행복", "따뜻", "안녕", "괜찮", "함께"],
        "success_message": "당신의 진심 어린 응원이 새로운 희망이 되었어요..."
    }
}

# 게임 클래스
class Game:
    def __init__(self):
        self.state = GameState.TITLE
        self.current_memory = None
        self.story_index = 0
        self.input_text = ""
        self.result_success = False
        self.animation_time = 0
        self.particles = []
        self.message_display_time = 0
        self.show_instruction = True

    def draw_gradient_background(self, color1, color2):
        """그라데이션 배경 그리기"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_thought_bubble(self, x, y, width, height, text):
        """말풍선 그리기"""
        # 메인 구름 모양
        pygame.draw.ellipse(screen, PURPLE, (x, y, width, height))
        pygame.draw.ellipse(screen, PURPLE, (x - 20, y + 20, width * 0.3, height * 0.6))
        pygame.draw.ellipse(screen, PURPLE, (x + width - 30, y + 15, width * 0.25, height * 0.5))
        pygame.draw.ellipse(screen, PURPLE, (x + 20, y - 15, width * 0.4, height * 0.4))
        pygame.draw.ellipse(screen, PURPLE, (x + width - 60, y - 10, width * 0.3, height * 0.35))

        # 말풍선 꼬리 (작은 원들)
        pygame.draw.circle(screen, PURPLE, (x + width - 50, y + height + 10), 15)
        pygame.draw.circle(screen, PURPLE, (x + width - 20, y + height + 30), 10)
        pygame.draw.circle(screen, PURPLE, (x + width, y + height + 45), 6)

        # 텍스트
        text_surface = font_large.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def draw_dog_wizard(self, x, y, scale=1.0):
        """강아지 마법사 그리기 (픽셀 아트 스타일)"""
        s = scale

        # 별 이펙트
        for i in range(5):
            offset_x = math.sin(self.animation_time * 2 + i) * 30
            offset_y = math.cos(self.animation_time * 2 + i) * 20
            star_size = 3 + math.sin(self.animation_time * 3 + i) * 2
            self.draw_star(x + offset_x + i * 25, y - 30 + offset_y, int(star_size * s), YELLOW)

        # 마법사 모자
        hat_color = DARK_PURPLE
        pygame.draw.polygon(screen, hat_color, [
            (x + 40 * s, y - 60 * s),  # 꼭대기
            (x - 10 * s, y + 10 * s),   # 왼쪽
            (x + 90 * s, y + 10 * s)    # 오른쪽
        ])
        # 모자 밴드
        pygame.draw.rect(screen, GOLD, (x - 10 * s, y + 5 * s, 100 * s, 10 * s))
        # 모자 별
        self.draw_star(x + 40 * s, y - 30 * s, int(8 * s), YELLOW)

        # 몸통 (크림색)
        body_color = (255, 220, 180)
        pygame.draw.ellipse(screen, body_color, (x, y + 20 * s, 80 * s, 100 * s))

        # 얼굴
        pygame.draw.ellipse(screen, body_color, (x + 5 * s, y + 10 * s, 70 * s, 60 * s))

        # 귀
        pygame.draw.ellipse(screen, (220, 180, 140), (x - 15 * s, y + 5 * s, 30 * s, 45 * s))
        pygame.draw.ellipse(screen, (220, 180, 140), (x + 65 * s, y + 5 * s, 30 * s, 45 * s))

        # 눈
        pygame.draw.ellipse(screen, BLACK, (x + 18 * s, y + 30 * s, 12 * s, 14 * s))
        pygame.draw.ellipse(screen, BLACK, (x + 50 * s, y + 30 * s, 12 * s, 14 * s))
        # 눈 하이라이트
        pygame.draw.circle(screen, WHITE, (int(x + 22 * s), int(y + 34 * s)), int(3 * s))
        pygame.draw.circle(screen, WHITE, (int(x + 54 * s), int(y + 34 * s)), int(3 * s))

        # 코
        pygame.draw.ellipse(screen, (60, 40, 30), (x + 33 * s, y + 45 * s, 14 * s, 10 * s))

        # 입 (미소)
        pygame.draw.arc(screen, (60, 40, 30), (x + 25 * s, y + 48 * s, 30 * s, 15 * s),
                       3.14, 0, 2)

        # 목걸이
        pygame.draw.ellipse(screen, (200, 50, 50), (x + 30 * s, y + 68 * s, 20 * s, 15 * s))

        # 마법 지팡이
        wand_x = x + 85 * s
        wand_y = y + 50 * s
        pygame.draw.line(screen, (139, 90, 43), (wand_x, wand_y),
                        (wand_x + 30 * s, wand_y - 40 * s), int(4 * s))
        # 지팡이 끝 별
        star_glow = abs(math.sin(self.animation_time * 4)) * 50
        self.draw_star(wand_x + 30 * s, wand_y - 45 * s, int(12 * s),
                      (255, 255, int(150 + star_glow)))

    def draw_star(self, x, y, size, color):
        """별 그리기"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            if i % 2 == 0:
                r = size
            else:
                r = size / 2
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)

    def draw_diamond(self, x, y, size, color, text, completed=False, hover=False):
        """다이아몬드 모양 기억 조각 그리기"""
        # 3D 효과를 위한 그림자
        shadow_offset = 5
        shadow_points = [
            (x + shadow_offset, y - size + shadow_offset),
            (x + size + shadow_offset, y + shadow_offset),
            (x + shadow_offset, y + size + shadow_offset),
            (x - size + shadow_offset, y + shadow_offset)
        ]
        pygame.draw.polygon(screen, (30, 30, 30), shadow_points)

        # 메인 다이아몬드
        points = [
            (x, y - size),      # 상단
            (x + size, y),      # 우측
            (x, y + size),      # 하단
            (x - size, y)       # 좌측
        ]

        if completed:
            # 완료된 조각 - 빛나는 효과
            glow = abs(math.sin(self.animation_time * 2)) * 30
            glow_color = (min(255, color[0] + glow), min(255, color[1] + glow), min(255, color[2] + glow))
            pygame.draw.polygon(screen, glow_color, points)
            pygame.draw.polygon(screen, GOLD, points, 3)
        elif hover:
            # 호버 상태
            pygame.draw.polygon(screen, tuple(min(255, c + 30) for c in color), points)
            pygame.draw.polygon(screen, WHITE, points, 2)
        else:
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, LIGHT_GRAY, points, 2)

        # 테두리 (3D 효과)
        pygame.draw.line(screen, (80, 80, 80), points[0], points[1], 2)
        pygame.draw.line(screen, (80, 80, 80), points[1], points[2], 2)
        pygame.draw.line(screen, (100, 100, 100), points[2], points[3], 2)
        pygame.draw.line(screen, (100, 100, 100), points[3], points[0], 2)

        # 텍스트
        text_surface = font_small.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def draw_title_screen(self):
        """타이틀 화면"""
        self.draw_gradient_background(LIGHT_PURPLE, PURPLE)

        # 말풍선과 제목
        self.draw_thought_bubble(80, 60, 400, 120, "강아지 마법사의 꿈")

        # 강아지 마법사
        self.draw_dog_wizard(580, 280, 1.5)

        # 시작 안내 (깜빡임 효과)
        if int(self.animation_time * 2) % 2 == 0:
            start_text = font_medium.render("터치하여 시작하기", True, WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            screen.blit(start_text, start_rect)

        # 파티클 효과
        self.update_particles()
        self.draw_particles()

    def draw_memory_select_screen(self):
        """기억 조각 선택 화면"""
        # 그라데이션 배경 (위: 밝은 하늘색, 아래: 진한 남색)
        self.draw_gradient_background(SOFT_BLUE, NAVY)

        # 안내 텍스트
        guide_text = font_medium.render("기억 조각을 선택하세요", True, WHITE)
        guide_rect = guide_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(guide_text, guide_rect)

        # 진행 상황 표시
        completed_count = sum(1 for m in memory_fragments.values() if m["completed"])
        progress_text = font_small.render(f"회복된 기억: {completed_count} / 3", True, YELLOW)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 90))
        screen.blit(progress_text, progress_rect)

        # 마우스 위치
        mouse_pos = pygame.mouse.get_pos()

        # 세 개의 기억 조각
        diamond_positions = [
            (160, 320, "neglect"),
            (400, 320, "abuse"),
            (640, 320, "abandon")
        ]

        for x, y, key in diamond_positions:
            fragment = memory_fragments[key]
            # 호버 체크
            hover = self.check_diamond_hover(x, y, 70, mouse_pos)
            self.draw_diamond(x, y, 70, DARK_GRAY, fragment["name"],
                            fragment["completed"], hover and not fragment["completed"])

        # 모든 조각 완료 시 엔딩 버튼
        if completed_count == 3:
            # 버튼 배경
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 480, 240, 50)
            pygame.draw.rect(screen, GOLD, button_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)

            ending_text = font_medium.render("꿈에서 깨어나기", True, BLACK)
            ending_rect = ending_text.get_rect(center=button_rect.center)
            screen.blit(ending_text, ending_rect)

    def check_diamond_hover(self, x, y, size, mouse_pos):
        """다이아몬드 호버 체크"""
        mx, my = mouse_pos
        # 간단한 사각형 체크
        return abs(mx - x) < size and abs(my - y) < size

    def draw_story_screen(self):
        """스토리 화면"""
        self.draw_gradient_background(DARK_PURPLE, BLACK)

        fragment = memory_fragments[self.current_memory]

        # 제목
        title_text = font_large.render(f"[ {fragment['name']} ]", True, LIGHT_PURPLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # 스토리 텍스트
        y_offset = 120
        for i, line in enumerate(fragment["story"]):
            if i <= self.story_index:
                alpha = 255 if i < self.story_index else min(255, int((self.animation_time % 1) * 255))
                text_surface = font_small.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 35))
                screen.blit(text_surface, text_rect)

        # 진행 안내
        if self.story_index >= len(fragment["story"]) - 1:
            if int(self.animation_time * 2) % 2 == 0:
                continue_text = font_small.render("클릭하여 계속하기...", True, YELLOW)
                continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                screen.blit(continue_text, continue_rect)

    def draw_input_screen(self):
        """위로 문장 입력 화면"""
        self.draw_gradient_background(NAVY, DARK_PURPLE)

        fragment = memory_fragments[self.current_memory]

        # 안내 텍스트
        guide1 = font_medium.render("이 강아지에게 위로와 응원의 말을 전해주세요", True, WHITE)
        guide1_rect = guide1.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(guide1, guide1_rect)

        # 강아지 이미지 (작게)
        self.draw_dog_wizard(320, 120, 0.8)

        # 힌트
        hint_text = font_tiny.render("(진심을 담아 따뜻한 말을 적어주세요)", True, LIGHT_GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(hint_text, hint_rect)

        # 입력 박스
        input_box = pygame.Rect(100, 320, 600, 50)
        pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(screen, PURPLE, input_box, 3, border_radius=10)

        # 입력된 텍스트
        if self.input_text:
            input_surface = font_medium.render(self.input_text, True, BLACK)
        else:
            input_surface = font_medium.render("여기에 입력하세요...", True, LIGHT_GRAY)
        input_rect = input_surface.get_rect(midleft=(input_box.left + 15, input_box.centery))
        screen.blit(input_surface, input_rect)

        # 커서 (깜빡임)
        if int(self.animation_time * 2) % 2 == 0 and self.input_text:
            cursor_x = input_rect.right + 2
            pygame.draw.line(screen, BLACK, (cursor_x, input_box.top + 10),
                           (cursor_x, input_box.bottom - 10), 2)

        # 제출 버튼
        submit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 400, 160, 45)
        pygame.draw.rect(screen, PURPLE, submit_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, submit_rect, 2, border_radius=10)

        submit_text = font_medium.render("전달하기", True, WHITE)
        submit_text_rect = submit_text.get_rect(center=submit_rect.center)
        screen.blit(submit_text, submit_text_rect)

        # 입력 안내
        info_text = font_tiny.render("Enter 키를 눌러 전달할 수도 있습니다", True, LIGHT_GRAY)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, 470))
        screen.blit(info_text, info_rect)

    def draw_result_screen(self):
        """결과 화면"""
        if self.result_success:
            self.draw_gradient_background(LIGHT_PURPLE, PURPLE)

            # 성공 메시지
            fragment = memory_fragments[self.current_memory]

            # 별 이펙트
            for i in range(8):
                angle = i * math.pi / 4 + self.animation_time
                x = SCREEN_WIDTH // 2 + math.cos(angle) * 150
                y = 200 + math.sin(angle) * 80
                size = 10 + math.sin(self.animation_time * 3 + i) * 5
                self.draw_star(x, y, int(size), YELLOW)

            success_text = font_large.render("기억 회복 성공!", True, GOLD)
            success_rect = success_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(success_text, success_rect)

            # 메시지
            message_surface = font_medium.render(fragment["success_message"], True, WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(message_surface, message_rect)

            # 강아지 (행복한 모습)
            self.draw_dog_wizard(320, 350, 1.0)

        else:
            self.draw_gradient_background(DARK_GRAY, BLACK)

            # 실패 메시지
            fail_text = font_large.render("마음이 전해지지 않았어요...", True, LIGHT_GRAY)
            fail_rect = fail_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(fail_text, fail_rect)

            hint_text = font_medium.render("더 따뜻한 마음을 담아 다시 시도해보세요", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(hint_text, hint_rect)

        # 계속 버튼
        if int(self.animation_time * 2) % 2 == 0:
            continue_text = font_small.render("클릭하여 계속하기...", True,
                                              YELLOW if self.result_success else WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(continue_text, continue_rect)

    def draw_ending_screen(self):
        """엔딩 화면"""
        # 따뜻한 배경
        self.draw_gradient_background(PINK, LIGHT_PURPLE)

        # 별 이펙트
        for i in range(15):
            angle = i * math.pi / 7.5 + self.animation_time * 0.5
            dist = 200 + math.sin(self.animation_time + i) * 50
            x = SCREEN_WIDTH // 2 + math.cos(angle) * dist
            y = 300 + math.sin(angle) * dist * 0.5
            size = 8 + math.sin(self.animation_time * 2 + i) * 4
            self.draw_star(x, y, int(size), YELLOW)

        # 엔딩 텍스트
        ending_texts = [
            "모든 기억을 되찾은 강아지 마법사는",
            "마침내 꿈에서 깨어났습니다.",
            "",
            "그리고...",
            "",
            "따뜻한 새 가족을 만나",
            "행복한 나날을 보내게 되었답니다."
        ]

        y_offset = 80
        for i, text in enumerate(ending_texts):
            text_surface = font_medium.render(text, True, DARK_PURPLE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 40))
            screen.blit(text_surface, text_rect)

        # 행복한 강아지
        self.draw_dog_wizard(320, 350, 1.2)

        # 하트 이펙트
        for i in range(5):
            x = 200 + i * 100
            y = 420 + math.sin(self.animation_time * 2 + i) * 20
            self.draw_heart(x, y, 15, (255, 100, 150))

        # 메시지
        message_box = pygame.Rect(100, 500, 600, 80)
        pygame.draw.rect(screen, WHITE, message_box, border_radius=15)
        pygame.draw.rect(screen, GOLD, message_box, 3, border_radius=15)

        msg1 = font_small.render("당신의 따뜻한 마음이 기적을 만들었습니다", True, DARK_PURPLE)
        msg1_rect = msg1.get_rect(center=(SCREEN_WIDTH // 2, 525))
        screen.blit(msg1, msg1_rect)

        msg2 = font_tiny.render("유기동물 입양에 관심을 가져주세요 - 포인핸드 앱", True, PURPLE)
        msg2_rect = msg2.get_rect(center=(SCREEN_WIDTH // 2, 555))
        screen.blit(msg2, msg2_rect)

    def draw_heart(self, x, y, size, color):
        """하트 그리기"""
        # 두 원과 삼각형으로 하트 모양 만들기
        pygame.draw.circle(screen, color, (int(x - size * 0.3), int(y - size * 0.2)), int(size * 0.5))
        pygame.draw.circle(screen, color, (int(x + size * 0.3), int(y - size * 0.2)), int(size * 0.5))
        pygame.draw.polygon(screen, color, [
            (x - size * 0.7, y),
            (x + size * 0.7, y),
            (x, y + size * 0.8)
        ])

    def update_particles(self):
        """파티클 업데이트"""
        # 새 파티클 추가
        if len(self.particles) < 20 and pygame.time.get_ticks() % 10 == 0:
            import random
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT + 10,
                'speed': random.uniform(1, 3),
                'size': random.randint(2, 5),
                'color': random.choice([YELLOW, WHITE, LIGHT_PURPLE])
            })

        # 파티클 이동
        for p in self.particles[:]:
            p['y'] -= p['speed']
            p['x'] += math.sin(p['y'] * 0.02) * 0.5
            if p['y'] < -10:
                self.particles.remove(p)

    def draw_particles(self):
        """파티클 그리기"""
        for p in self.particles:
            self.draw_star(p['x'], p['y'], p['size'], p['color'])

    def check_input_validation(self, text, keywords):
        """입력 문장 검증"""
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                return True
        # 최소 글자 수 체크 (5자 이상)
        if len(text) >= 5:
            return True
        return False

    def handle_click(self, pos):
        """클릭 이벤트 처리"""
        if self.state == GameState.TITLE:
            self.state = GameState.MEMORY_SELECT

        elif self.state == GameState.MEMORY_SELECT:
            # 다이아몬드 클릭 체크
            diamond_positions = [
                (160, 320, "neglect"),
                (400, 320, "abuse"),
                (640, 320, "abandon")
            ]

            for x, y, key in diamond_positions:
                if self.check_diamond_hover(x, y, 70, pos):
                    if not memory_fragments[key]["completed"]:
                        self.current_memory = key
                        self.story_index = 0
                        self.state = GameState.STORY
                        return

            # 엔딩 버튼 체크
            completed_count = sum(1 for m in memory_fragments.values() if m["completed"])
            if completed_count == 3:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 480, 240, 50)
                if button_rect.collidepoint(pos):
                    self.state = GameState.ENDING

        elif self.state == GameState.STORY:
            fragment = memory_fragments[self.current_memory]
            if self.story_index < len(fragment["story"]) - 1:
                self.story_index += 1
            else:
                self.state = GameState.INPUT
                self.input_text = ""

        elif self.state == GameState.INPUT:
            # 제출 버튼 체크
            submit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 400, 160, 45)
            if submit_rect.collidepoint(pos):
                self.submit_input()

        elif self.state == GameState.RESULT:
            if self.result_success:
                self.state = GameState.MEMORY_SELECT
            else:
                self.state = GameState.INPUT
                self.input_text = ""

        elif self.state == GameState.ENDING:
            # 게임 재시작
            for key in memory_fragments:
                memory_fragments[key]["completed"] = False
            self.state = GameState.TITLE

    def submit_input(self):
        """입력 제출"""
        if not self.input_text.strip():
            return

        fragment = memory_fragments[self.current_memory]
        self.result_success = self.check_input_validation(
            self.input_text,
            fragment["keywords"]
        )

        if self.result_success:
            memory_fragments[self.current_memory]["completed"] = True

        self.state = GameState.RESULT

    def handle_keydown(self, event):
        """키 입력 처리"""
        if self.state == GameState.INPUT:
            if event.key == pygame.K_RETURN:
                self.submit_input()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if event.unicode and len(self.input_text) < 50:
                    self.input_text += event.unicode

    def update(self, dt):
        """게임 업데이트"""
        self.animation_time += dt

    def draw(self):
        """화면 그리기"""
        if self.state == GameState.TITLE:
            self.draw_title_screen()
        elif self.state == GameState.MEMORY_SELECT:
            self.draw_memory_select_screen()
        elif self.state == GameState.STORY:
            self.draw_story_screen()
        elif self.state == GameState.INPUT:
            self.draw_input_screen()
        elif self.state == GameState.RESULT:
            self.draw_result_screen()
        elif self.state == GameState.ENDING:
            self.draw_ending_screen()

def main():
    """메인 함수"""
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # 델타 타임 (초 단위)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 좌클릭
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                game.handle_keydown(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
