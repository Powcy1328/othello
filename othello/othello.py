"""
修正版 オセロゲーム
2026/06/22
"""

"""
定数定義
"""
# フォントパス
JAPANESE_FONT_PATH = r".\font\ipaexg.ttf"

# 画面サイズ
(WIDTH, HEIGHT) = (20+688+20,20+688+78+20)# 卓上(688, 766) 全体(728, 806)
DISPLAY_SIZE = (WIDTH, HEIGHT)

# 色指定
WHITE = (255, 255, 255) #白
BLACK = (  0,   0,   0) #黒
GREEN = (  0, 255,   0) #緑
RED   = (255,   0,   0) #赤
BLUE  = (  0,   0, 255) #青


TITLE = "オセロ"
TICK = 30

"""
path取得
"""

from pathlib import Path

cwd_path = Path.cwd()
image_directory_path = cwd_path.joinpath("image")
sound_directory_path = cwd_path.joinpath("sound")

"""
画像読み込み
"""

import pygame
sound_enabled = True

try:
    pygame.mixer.init()
except pygame.error as e:
    print("音声初期化失敗:", e)
    sound_enabled = False

# オセロ盤面画像
IMG_othello_bg = pygame.image.load(image_directory_path.joinpath("osero_bg_688.png"))
# 黒い石画像
IMG_stone_black = pygame.image.load(image_directory_path.joinpath("osero_black_78.png"))
# 白い石画像
IMG_stone_white = pygame.image.load(image_directory_path.joinpath("osero_white_78.png"))
# ハイライト石画像
IMG_stone_transparent = pygame.image.load(image_directory_path.joinpath("osero_transparent_78.png"))
# 背景の木画像
IMG_wood_bg = pygame.image.load(image_directory_path.joinpath("wood.png"))

# 石の画像のリスト
stone_collor_img_list = [IMG_stone_black, IMG_stone_white]

if sound_enabled:
    # 石を置く音
    SOUND_put_stone = pygame.mixer.Sound(sound_directory_path.joinpath("stone_setting.wav"))
    # パス
    SOUND_pass = pygame.mixer.Sound(sound_directory_path.joinpath("pass.wav"))
else:
    SOUND_put_stone = None
    SOUND_pass = None

"""
関数定義
"""
import time
from decimal import *

class othello:
    def __init__(self, screen):
        self.screen = screen
    
    def init(self):
        self.Lboard_for_judge = []
        self.Lboard_for_display = []
        self.stone_clr = 0
        self.Lmouse_pos_mass = []
        self.Lcanput_pos = []
        self.Fput = False
        self.s_time = time.time()
        self.Fhighlight = False
        self.count_pass = 0
        self.Fgamefinish = False
        self.finish_time = 0
        self.Fskip = False
        self.count_put = 0

    # ボードの初期化
    def init_boad(self):
        # リスト作成(すべて9=空白)
        for i in range(8):
            self.Lboard_for_judge.append([9, 9, 9, 9, 9, 9, 9, 9]) 

        # 初期設定 中央に石を設置
        self.Lboard_for_judge[3][3] = 1
        self.Lboard_for_judge[4][4] = 1
        self.Lboard_for_judge[4][3] = 0
        self.Lboard_for_judge[3][4] = 0

        self.Lboard_for_display = self.Lboard_for_judge.copy()

        # self.Lboard_for_judge = [  # デバッグ用(終了)
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 1, 1, 1, 1, 1, 1, 0],
        #     [0, 1, 0, 0, 0, 0, 1, 0],
        #     [0, 1, 0, 1, 1, 0, 1, 0],
        #     [0, 1, 0, 1, 1, 0, 1, 0],
        #     [0, 1, 0, 0, 0, 0, 1, 0],
        #     [0, 1, 1, 1, 1, 1, 1, 0],
        #     [0, 0, 0, 9, 9, 9, 0, 0]  # ← 残り3マス（黒→白→黒で埋まる）
        # ]

        # self.Lboard_for_judge = [  # デバッグ用(skip)
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 9, 9, 9, 0, 0],
        #     [0, 0, 0, 9, 9, 9, 0, 0],
        #     [0, 0, 0, 9, 9, 9, 0, 0],
        #     [0, 0, 0, 0, 0, 1, 0, 0],
        #     [0, 0, 9, 1, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0]
        # ]


    # 背景の木とオセロ盤面の描写
    def blit_bg(self):

        # 木の背景とオセロの盤面の描写
        self.screen.blit(IMG_wood_bg, [0, 0])
        self.screen.blit(IMG_othello_bg, [20, 20])

    # スタート画面描写(index=0)
    def start_surface(self):
        font = pygame.font.Font(JAPANESE_FONT_PATH, 54)

        # タイトル文字定義
        title_txt = font.render("オセロゲーム", True, BLACK)
        title_txt_poss = title_txt.get_rect(center=(WIDTH//2, 100))
        # スタートボタン文字定義
        start_btn_txt = font.render("start", True, BLACK)
        start_btn_txt_poss = start_btn_txt.get_rect(center=(WIDTH//2, HEIGHT//2+90))

        # スタートボタン背景座標定義
        start_draw_rect_poss = [WIDTH//2-150, HEIGHT//2+90-50, 300, 100]

        # 背景描写
        self.blit_bg()
        # タイトル描写
        pygame.draw.rect(self.screen, WHITE, [164, 50, 400, 100])
        pygame.draw.rect(self.screen, BLACK, [164, 50, 400, 100], 2)
        self.screen.blit(title_txt, [title_txt_poss.x, title_txt_poss.y])
        # スタートボタン描写
        pygame.draw.rect(self.screen, WHITE, start_draw_rect_poss)
        pygame.draw.rect(self.screen, BLACK, start_draw_rect_poss, 2)
        self.screen.blit(start_btn_txt, [start_btn_txt_poss.x, start_btn_txt_poss.y])

    # スタートボタン判定
    def start_btn_judge(self, mX, mY):
        if WIDTH//2-150 < mX and mX < WIDTH//2+150 and HEIGHT//2+90-50 < mY and mY < HEIGHT//2+90+50:
            return 1
        else:
            return 0

    # 石の描写
    def blit_stone(self):

        self.Lboard_for_judge
        # リストに沿って石を描写
        for y in range(8):
            for x in range(8):
                if self.Lboard_for_judge[y][x] == 0:
                    self.screen.blit(IMG_stone_black, [20+7+7*x+78*x,20+7+7*y+78*y])
                elif self.Lboard_for_judge[y][x] == 1:
                    self.screen.blit(IMG_stone_white, [20+7+7*x+78*x,20+7+7*y+78*y])
                elif self.Lboard_for_judge[y][x] == 7:
                    self.screen.blit(IMG_stone_transparent, [20+7+7*x+78*x,20+7+7*y+78*y])

    # ゲーム中のオセロ盤面と置かれた石の描写
    def game_surface(self):

        self.blit_bg()
        self.blit_stone()
        self.screen.blit(stone_collor_img_list[self.stone_clr], [0+20,688+20])

    # マウスの座標がどのマスの上なのかの計算
    def pos_stone(self, mX, mY, e):
        
        # マウスがどこのボードのマスの上か判定
        # ボードのマスの判定を左上に設定
        OmX = mX-20-3
        OmY = mY-20-3
        # 85(1マスの大きさ)で割る
        Boad_OmX = int(OmX/85)
        Boad_OmY = int(OmY/85)

        self.Lmouse_pos_mass = [Boad_OmX, Boad_OmY]
        # return Boad_OmX, Boad_OmY
    
    def press_key(self, e):
        if e.key == pygame.K_1:
            self.Fskip = True
    
    def highlight_delete(self):
        self.Fhighlight = False
        for y in range(8):
            for x in range(8):
                if self.Lboard_for_judge[y][x] == 7:
                    self.Lboard_for_judge[y][x] = 9
    
    def highlight(self):
        # self.highlight_delete()
        # 変数定義
        opposite_clr = (self.stone_clr+1)%2
        # 判定用リスト
        Ljudge_y = [-1, -1, 0, 1, 1, 1, 0, -1] # 上から時計周り
        Ljudge_x = [0, 1, 1, 1, 0, -1, -1, -1]

        # ハイライト判定
        for y in range(8):
            for x in range(8):
                if self.Lboard_for_judge[y][x] != 9:
                    continue
                # 何も置いていない場合
                # else:
                for judge_around in range(len(Ljudge_y)):
                    # リスト外対策
                    if y+Ljudge_y[judge_around] < 0 or y+Ljudge_y[judge_around] >= 8:
                        continue
                    elif x+Ljudge_x[judge_around] < 0 or x+Ljudge_x[judge_around] >= 8:
                        continue
                    # 違う色がある場合
                    elif self.Lboard_for_judge[y+Ljudge_y[judge_around]][x+Ljudge_x[judge_around]] == opposite_clr:
                        for i in range(2, 9, 1):
                            serch_y = y+Ljudge_y[judge_around]*i
                            serch_x = x+Ljudge_x[judge_around]*i
                            # リスト外対策
                            if serch_y < 0 or serch_y >= 8:
                                continue
                            elif serch_x < 0 or serch_x >= 8:
                                continue
                            # 石がない場合
                            elif self.Lboard_for_judge[serch_y][serch_x] in [9, 7]:
                                break
                            # 反対の色の石の場合
                            elif self.Lboard_for_judge[serch_y][serch_x] == (self.stone_clr+1)%2:
                                pass
                            # 反対に今の色の石がある場合
                            elif self.Lboard_for_judge[serch_y][serch_x] == self.stone_clr:
                                self.Lboard_for_judge[y][x] = 7
                                self.Lcanput_pos.append([(x, y), Ljudge_y[judge_around], Ljudge_x[judge_around]])
                                self.Fhighlight = True
                                break

    # 石を置いて更新する
    def put_stone(self):
        Fput = False
        if self.Lmouse_pos_mass != []:
            massX = self.Lmouse_pos_mass[0]
            massY = self.Lmouse_pos_mass[1]
            for pos, arrowy, arrowx in self.Lcanput_pos:
                if pos == (massX, massY):
                    self.Lboard_for_judge[massY][massX] = self.stone_clr
                    for i in range(1, 8):
                        if self.Lboard_for_judge[massY+arrowy*i][massX+arrowx*i] == self.stone_clr:
                            break
                        elif self.Lboard_for_judge[massY+arrowy*i][massX+arrowx*i] == (self.stone_clr+1)%2:
                            if SOUND_put_stone:
                                SOUND_put_stone.play()
                            self.Lboard_for_judge[massY+arrowy*i][massX+arrowx*i] = self.stone_clr
                            Fput = True
            if Fput:
                self.turn_over()
                self.count_put += 1
        self.Lmouse_pos_mass = []
    
    # ターン終了
    def turn_over(self):
        self.stone_clr = (self.stone_clr+1)%2
        self.highlight_delete()
        self.Lcanput_pos = []

    # 途中経過タイマー
    def blit_during_game_timer(self):
        # pygame font 定義
        font = pygame.font.Font(JAPANESE_FONT_PATH, 40)

        # 小数点定義
        exp = Decimal("0.01")

        # 今の時間を取得
        now_time = time.time()

        # タイマーの秒数
        if now_time - self.s_time > 9999.99:
            timer_output_num = 9999.99
        else:
            timer_output_num = now_time - self.s_time

        # タイマーの描写用変数定義
        timer_output_num_decimal = str(Decimal(timer_output_num).quantize(exp, ROUND_UP))
        timer_txt = font.render(timer_output_num_decimal, True, WHITE)
        timer_txt_pos = timer_txt.get_rect(midright = (700, 730))
        # タイマー描写
        self.screen.blit(timer_txt, (timer_txt_pos.x, timer_txt_pos.y))

        self.finish_time = Decimal(timer_output_num).quantize(exp, ROUND_UP)


    # 終わったか判断　結果の描写　ホームボタンの描写
    def judge_end(self):
        # 変数定義
        if self.Fhighlight:
            self.count_pass = 0
        elif self.Fgamefinish == False: # ハイライトがなかったら
            if self.count_pass == 0 and self.count_put != 60:
                font = pygame.font.Font(JAPANESE_FONT_PATH, 54)
                if SOUND_pass:
                    SOUND_pass.play()
                text_pass = font.render("パス", True, BLACK)
                text_pass_rect = text_pass.get_rect(center=(WIDTH//2, HEIGHT//2))
                pygame.draw.rect(self.screen, WHITE, [WIDTH//2-60, HEIGHT//2-30, 120, 60])
                pygame.draw.rect(self.screen, BLACK,[WIDTH//2-60, HEIGHT//2-30, 120, 60], 2)
                self.screen.blit(text_pass, (text_pass_rect.x, text_pass_rect.y))

                pygame.display.flip()
                time.sleep(0.5)
            
            self.count_pass += 1
            self.turn_over()
            self.Fhighlight = False
        
        if self.Fskip:
            self.count_pass += 1
            self.turn_over()
            self.Fhighlight = False
            self.Fskip = False
        
        # 2回パスをしたら
        if self.count_pass == 2:
            self.Fgamefinish = True
            return 2 # index

        return 1 # index

    # 試合結果の判別
    def end(self):
        num_black_stone = 0
        num_white_stone = 0
        # カウント
        for i in range(8):
            for j in range(8):
                if self.Lboard_for_judge[i][j] == 0:
                    num_black_stone += 1
                elif self.Lboard_for_judge[i][j] == 1:
                    num_white_stone += 1

        # 変数定義
        much_result = ""

        # ゲーム結果判定
        if num_black_stone > num_white_stone:
            much_result = "black"
        elif num_black_stone < num_white_stone:
            much_result = "white"
        elif num_black_stone == num_white_stone:
            much_result = "drow"

        font = pygame.font.Font(JAPANESE_FONT_PATH, 54)
        font_es = pygame.font.Font(JAPANESE_FONT_PATH, 18)

        # 宣言
        # 黒が勝った場合
        if much_result == "black":
            winner_txt = font.render("winner Black !!", True, BLACK)
            winner_txt_poss = winner_txt.get_rect(center=(WIDTH//2, 100))

        # 白が勝った場合
        elif much_result == "white":
            winner_txt = font.render("winner White !!", True, BLACK)
            winner_txt_poss = winner_txt.get_rect(center=(WIDTH//2, 100))

        # ドローの場合
        elif much_result == "drow":
            winner_txt = font.render("Drow !!", True, BLACK)
            winner_txt_poss = winner_txt.get_rect(center=(WIDTH//2, 100))

        # バックホームボタンテキスト宣言
        back_home_btn_txt = font.render("back home", True, BLACK)
        back_home_btn_txt_poss = back_home_btn_txt.get_rect(center=(WIDTH//2, HEIGHT//2+90))

        # 背景の座標宣言
        back_home_draw_rect_poss = [WIDTH//2-200, HEIGHT//2+90-50, 400, 100]

        # timeテキスト宣言
        # pygame font 定義
        font_time = pygame.font.Font(JAPANESE_FONT_PATH, 40)

        # finish_time テキスト定義
        finish_time_txt = font_time.render("TIME:"+str(self.finish_time), True, BLACK)
        finish_time_txt_pos = finish_time_txt.get_rect(center=(WIDTH//2, 150))

        # 石の数の宣言
        # pygame font 定義
        font_num_stone = pygame.font.Font(JAPANESE_FONT_PATH, 30)
        # 石の数のテキスト宣言
        num_stone_txt = font_num_stone.render(f"black:{num_black_stone}個 white:{num_white_stone}個", True, BLACK)
        num_stone_txt_pos = num_stone_txt.get_rect(center=(WIDTH//2, 200))

        # winnerテキスト背景座標
        draw_rect_pos = [114, 50, 500, 200]

        # エスケープで非表示
        escape_text = font_es.render("escapeで非表示", True, WHITE)
        escape_text_pos = escape_text.get_rect(midright = (700, 750))

        # 描写
        # 背景描写
        self.blit_bg()
        self.blit_stone()

        Fescape = pygame.key.get_pressed()[K_ESCAPE]
        

        # 結果表示背景
        if not Fescape:
            pygame.draw.rect(self.screen, WHITE, draw_rect_pos) 
            pygame.draw.rect(self.screen, BLACK, draw_rect_pos, 2)

            # ゲーム結果文字表示
            self.screen.blit(winner_txt, (winner_txt_poss.x, winner_txt_poss.y))

            # 終わりのタイム描写
            self.screen.blit(finish_time_txt, (finish_time_txt_pos.x, finish_time_txt_pos.y))

            # 石の数の描写
            self.screen.blit(num_stone_txt, (num_stone_txt_pos.x, num_stone_txt_pos.y))

            # エスケープで非表示
            self.screen.blit(escape_text, (escape_text_pos.x, escape_text_pos.y))

            # バックホームボタン描写
            pygame.draw.rect(self.screen, WHITE, back_home_draw_rect_poss)
            pygame.draw.rect(self.screen, BLACK,back_home_draw_rect_poss, 2)
            self.screen.blit(back_home_btn_txt, [back_home_btn_txt_poss.x, back_home_btn_txt_poss.y])

        # ゲーム終わりのホームボタンの押された判定
    def back_home_btn(self, mouseX, mouseY):

        # バックホームボタン押された判定
        if WIDTH // 2 - 200 < mouseX < WIDTH // 2 + 200 and HEIGHT // 2 + 90 - 50 < mouseY < HEIGHT // 2 + 90 + 50:
            return 0
        else:
            return 2

"""
メイン関数定義
"""

import sys
from pygame.locals import *

def main():
    pygame.init()
    pygame.display.set_caption(TITLE) # 上のバーのタイトル
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()
    index = 0
    otl = othello(screen)

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            if index == 0: # start
                if event.type == MOUSEBUTTONDOWN:
                    index = otl.start_btn_judge(mouseX, mouseY)
            elif index == 1: # playing
                if event.type == MOUSEBUTTONDOWN:
                    otl.pos_stone(mouseX, mouseY, event)
                elif event.type == KEYDOWN:
                    otl.press_key(event)
            elif index == 2: # result
                if event.type == MOUSEBUTTONDOWN:
                    index = otl.back_home_btn(mouseX, mouseY)
        
        if index == 0: # start
            otl.init()
            otl.init_boad()
            otl.start_surface()
        elif index == 1: # game
            otl.highlight()
            index = otl.judge_end()
            otl.put_stone()
            otl.game_surface()
            otl.blit_during_game_timer()
        elif index == 2: # result
            otl.end()

        # 画面更新
        pygame.display.flip()
        clock.tick(TICK)

if __name__ == "__main__":
    main()