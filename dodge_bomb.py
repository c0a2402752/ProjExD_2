import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue, 外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    黒背景に「Game Over」と泣きこうかとん画像を5秒表示
    """
    # 黒いSurface半透明化
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(200)
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))

    # Game Over文字を生成
    font = pg.font.Font(None, 120)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(txt, txt_rct)

    # こうかとん画像
    kk_img = pg.image.load("fig/8.png")

    # 左側に配置
    kk_left_rct = kk_img.get_rect(midright=(txt_rct.left - 20, txt_rct.centery))
    screen.blit(kk_img, kk_left_rct)

    # 右側に配置
    kk_right_rct = kk_img.get_rect(midleft=(txt_rct.right + 20, txt_rct.centery))
    screen.blit(kk_img, kk_right_rct)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の大きさと加速倍率のリストを生成する
    戻り値: (爆弾Surfaceリスト, 加速度リスト)
    """
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):  # 1～10段階
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  # 黒背景を透明化
        bb_imgs.append(bb_img)
        bb_accs.append(r)
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # bb_img = pg.Surface((20,20)) #空のSurface
    # pg.draw.circle(bb_img, (255,0,0),(10,10),10) #赤い爆弾
    # bb_img.set_colorkey((0,0,0))
    # bb_rct = bb_img.get_rect()
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()

    bb_rct.centerx = random.randint(0, WIDTH) #爆弾横
    bb_rct.centery = random.randint(0,HEIGHT) #爆弾縦
    vx,vy = 5,5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return #ゲームオーバー
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5/
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,avy) #爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
