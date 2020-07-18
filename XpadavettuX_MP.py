import pygame
from math import *
import time
import os

print("---------XpadavettuX----------")

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "assets\images")
snd_folder = os.path.join(game_folder, "assets\sounds")

# player 1 = True
# player 2 = False

# Screen constants
WIDTH = 900
HEIGHT = 650
FPS = 15

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# sizes and positions of icons and button
BUTTON_SIZE = (40, 40)

REMOVE = (WIDTH / 2 - 100, HEIGHT - 30)  # position of center of remove button
REMOVE_SIZE = (150, 50)
PASS = (WIDTH / 2 + 100, HEIGHT - 30)
PASS_SIZE = (150, 50)

CTRL_SIZE = (150, 60)

# padavettu board
dim = 480
center = (WIDTH / 2, 300)
step = dim / 6
start = ((center[0] - dim / 2), (center[1] - dim / 2))

# anchor points in board
anchor_points = [None for i in range(33)]  # pints in the noard. total 33 points
point_counter = 0
for i in range(0, 7):
    for j in range(0, 7):
        if i in [0, 1, 5, 6] and j in [0, 1, 5, 6]:
            pass
        else:
            anchor_points[point_counter] = [start[0] + j * step, start[1] + i * step]
            point_counter += 1

# length of lines in the board
SLL = step  # straight line length
DLL = sqrt(2) * step  # diagonal line length
ML = 0

# anchor_points connectivity data of the points on the playing board
conn_points = [[0, 30], [2, 32], [6, 12], [20, 26],
               [0, 2], [30, 32], [6, 20], [12, 26],
               [6, 32], [8, 24], [0, 26], [20, 2], [22, 10], [30, 12],
               [1, 31], [13, 19], [7, 21], [11, 25], [3, 5], [27, 29]]
conn_data = list()
for i in conn_points:
    entry = [anchor_points[i[0]], anchor_points[i[1]]]
    conn_data.append(entry)

# ------------fixed variables over---------------------------------------------


# ------------pygame and sprites----------------------------------------------------------

pygame.init()  # initialise pygame
pygame.mixer.init()  # initialize mixer for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PADAVETTU")  # Window caption
ICON = pygame.image.load(os.path.join(img_folder, "icon.png")).convert_alpha()  # Window icon
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()


class Controls(pygame.sprite.Sprite):  # Class of immovable objects
    # sprite for player
    def __init__(self, file, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, file)).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos


# load_images and control sprites--------------
BG = Controls("board.png", (WIDTH / 2, HEIGHT / 2))
BG_fp = Controls("first_page.png", (WIDTH / 2, HEIGHT / 2))
PLAY = Controls("play.png", (112.5, 550))
RULES = Controls("rules.png", (337.5, 550))
ABOUT = Controls("about.png", (562.5, 550))
QUIT = Controls("quit.png", (787.5, 550))
DUMMY = Controls("dummy.png", (1000, 1000))
remove_passive = Controls("remove_passive.png", REMOVE)
remove_active = Controls("remove_active.png", REMOVE)
blue_move = Controls("blue_move.png", (635, 480))
red_move = Controls("red_move.png", (265, 120))
rules_page = Controls("rules_page.png", (WIDTH / 2, 250))
about_page = Controls("about_page.png", (WIDTH / 2, 250))

quit = Controls("quit.png", (787.5, 600))
rules = Controls("rules.png", (112.5, 600))

select = Controls("select.png", (WIDTH / 2, 578))
selected = Controls("selected.png", (WIDTH / 2, 578))

CURSOR = pygame.image.load(os.path.join(img_folder, "cursor.png"))
pass_passive = Controls("passive_pass.png", PASS)
pass_active = Controls("active_pass.png", PASS)

# loading sounds ---------------------------

move_sound = pygame.mixer.Sound(os.path.join(snd_folder, "move.aiff"))
wrong_sound = pygame.mixer.Sound(os.path.join(snd_folder, "wrong_sound.aiff"))
remove_sound = pygame.mixer.Sound(os.path.join(snd_folder, "remove.aiff"))
turn_sound = pygame.mixer.Sound(os.path.join(snd_folder, "turn.aiff"))
select_sound = pygame.mixer.Sound(os.path.join(snd_folder, "select.aiff"))
win_sound = pygame.mixer.Sound(os.path.join(snd_folder, "win.aiff"))
begin_sound = pygame.mixer.Sound(os.path.join(snd_folder, "begin.aiff"))


class Button(pygame.sprite.Sprite):  # Class of moving objects
    global button_obj_cp
    global button_obj_op

    def __init__(self, position, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        if self.player == True:
            self.image = pygame.image.load(os.path.join(img_folder, "redbutton.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(img_folder, "bluebutton.png")).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = position

    def move(self, new_pos):
        self.rect.center = new_pos
        return


class Initialize_dynamic_varaibles():  # Assigning first values of all global variable that change values later

    def __init__(self):
        global P1button_pos
        global P2button_pos
        global button_pos_cp
        global button_pos_op
        global P1stock_counter
        global P2stock_counter
        global P1button_obj
        global P2button_obj
        global button_obj_cp
        global button_obj_cp
        global obj_op
        global click_no
        global cplayer
        global present
        global tap1, tap2, tap
        global all_sprites
        global _pass
        global first_move

        P1button_pos = []
        P2button_pos = []

        for i in [6, 7, 13, 14, 15] + list(range(20, 25)) + list(range(27, 33)):
            P1button_pos.append(anchor_points[i])

        for i in list(range(0, 6)) + list(range(8, 13)) + list(range(17, 20)) + list(range(25, 27)):
            P2button_pos.append(anchor_points[i])

        button_pos_cp = P1button_pos
        button_pos_op = P2button_pos

        P1stock_counter = 0
        P2stock_counter = 0

        # making page main sprites
        P1button_obj = []
        P2button_obj = []
        # making sprite groups

        all_sprites = pygame.sprite.Group()

        for i in P1button_pos:
            obj = Button(i, True)
            P1button_obj.append(obj)
            all_sprites.add(obj)

        for i in P2button_pos:
            obj = Button(i, False)
            P2button_obj.append(obj)
            all_sprites.add(obj)

        button_obj_cp = P1button_obj
        button_obj_op = P1button_obj

        all_sprites.add(red_move)
        all_sprites.add(remove_passive)
        all_sprites.add(quit)
        all_sprites.add(select)
        all_sprites.add(pass_passive)
        all_sprites.add(rules)

        tap1 = False
        tap2 = False
        tap = False

        first_move = True

        _pass = False

        click_no = 0
        cplayer = True


# Varying variables----------------------------------------
P1button_pos = None
P2button_pos = None
button_pos_cp = None
button_pos_op = None

P1stock_counter = None
P2stock_counter = None

P1button_obj = None
P2button_obj = None
button_obj_cp = None
button_obj_op = None

click_no = None
cplayer = None
present = None

tap1 = False
tap2 = False
tap = False
first_move = True

all_sprites = None
_pass = None

idv = Initialize_dynamic_varaibles()

# stock points
P1stock = []
P2stock = []

for i, j in [[0, i] for i in range(8)] + [[1, i] for i in range(8)]:
    P1stock.append([25 + (i + 1) * 50, 100 + (j + 1) * 50])
    P2stock.append([WIDTH - 25 + (i + 1) * -50, 100 + (j + 1) * 50])

controls = []  # group of fpage sprites

# making sprite groups
BG_sprites = pygame.sprite.Group()
fpage_all_sprites = pygame.sprite.Group()
fpage_BG_sprites = pygame.sprite.Group()

# adding other objects
BG_sprites.add(BG)
fpage_BG_sprites.add(BG_fp)


def clicked(center, dim, mx, my):  # check if a button is clicked
    if center[0] - (dim[0] / 2) < mx < center[0] + (dim[0] / 2) and center[1] - (dim[1] / 2) < my < center[1] + (
            dim[1] / 2):
        return True
    else:
        return False


def valid_click(mx, my):  # #check if a click is valid and store to global click1 and click2 variables
    global click_no
    global cplayer
    global click1
    global click2
    global button_pos_cp
    global button_pos_op
    global present
    global all_sprites
    global tap

    present = "game"

    if clicked(PASS, PASS_SIZE, mx, my):
        if _pass == True:
            turn_sound.play()
            click1 = "pass"
            click2 = None
            main_game()
        else:
            wrong_sound.play()

    if clicked(quit.pos, CTRL_SIZE, mx, my):
        select_sound.play()
        time.sleep(0.2)
        first_page()
        return

    if clicked(rules.pos, CTRL_SIZE, mx, my):
        select_sound.play()
        if tap == False:
            all_sprites.add(rules_page)
            tap = True
        else:
            all_sprites.remove(rules_page)
            tap = False
        click_no = 0
        return

    if click_no == 0:  # varify first click is valid and set click1 data

        button_no = 0
        for pos in button_pos_cp:
            if clicked(pos, BUTTON_SIZE, mx, my):
                click1 = {"x": pos[0], "y": pos[1], "bn": button_no}
                click_no = 1
                return
            button_no += 1

        button_no = 0
        for pos in button_pos_op:
            if clicked(pos, BUTTON_SIZE, mx, my):
                if first_move:
                    all_sprites.remove(remove_passive)
                    all_sprites.add(remove_active)
                    click1 = {"x": pos[0], "y": pos[1], "bn": button_no}
                    click_no = 1
                    return
                else:
                    wrong_sound.play()
                    return
            button_no += 1

    elif click_no == 1:  # varify second click is valid and set click2 data

        point = 0
        for pos in anchor_points:
            if clicked(pos, BUTTON_SIZE, mx, my):
                click2 = {"x": pos[0], "y": pos[1], "point": point}
                main_game()
                return
            point += 1

        if clicked(REMOVE, REMOVE_SIZE, mx, my) and [click1["x"], click1[
            "y"]] in button_pos_op:  # check if second click is "remove" button
            click_no = 0
            click2 = "remove"
            main_game()
        else:
            click_no = 0
        try:
            all_sprites.add(remove_passive)
            all_sprites.remove(remove_active)
        except:
            pass
        return


def main_game():  # Performs logical and legal checks on the click inputs
    global click1
    global click2
    global button_pos_cp
    global button_pos_op
    global button_obj_cp
    global button_obj_op
    global click_no
    global cplayer
    global P1stock_counter
    global P2stock_counter
    global present
    global _pass

    def didplayerwin():

        if P1stock_counter == 16:
            endgame(False)
        elif P2stock_counter == 16:
            endgame(True)
        else:
            return

    def change_cp():  # change current player
        global cplayer
        global button_pos_cp
        global button_pos_op
        global button_obj_cp
        global button_obj_op
        global click_no
        global _pass
        global first_move

        time.sleep(0.6)

        if cplayer == True:
            cplayer = False
            all_sprites.remove(red_move)
            all_sprites.add(blue_move)
        elif cplayer == False:
            cplayer = True
            all_sprites.add(red_move)
            all_sprites.remove(blue_move)
        if cplayer == True:  # assign variable values based on current player status
            button_pos_cp = P1button_pos
            button_pos_op = P2button_pos
            button_obj_cp = P1button_obj
            button_obj_op = P2button_obj

        elif cplayer == False:
            button_pos_cp = P2button_pos
            button_pos_op = P1button_pos
            button_obj_cp = P2button_obj
            button_obj_op = P1button_obj

        click_no = 0
        first_move = True

        _pass = False
        try:
            all_sprites.remove(pass_active)
        except:
            pass
        return

    def make_move(button_no, destn):
        global button_pos_cp
        global button_obj_cp
        global first_move

        button_pos_cp[button_no] = anchor_points[destn]
        button_obj_cp[button_no].move(anchor_points[destn])
        first_move = False
        move_sound.play()
        return

    def remove_button(button_no):
        global button_pos_op
        global button_obj_op
        global P1stock_counter
        global P2stock_counter

        if cplayer == True:
            button_pos_op[button_no] = P2stock[P2stock_counter]
            button_obj_op[button_no].move(P2stock[P2stock_counter])
            P2stock_counter += 1
        else:
            button_pos_op[button_no] = P1stock[P1stock_counter]
            button_obj_op[button_no].move(P1stock[P1stock_counter])
            P1stock_counter += 1

        remove_sound.play()
        didplayerwin()
        return

    def check_removable(click1):

        global click2
        global button_pos_op
        value = False
        temp = button_pos_op
        button_pos_op = button_pos_cp
        for i in range(33):
            click2 = {"x": anchor_points[i][0], "y": anchor_points[i][1], "point": i}
            result = check_rules()
            if result not in [False, -1]:
                value = True
                break

        button_pos_op = temp
        return value

    # rules of the game......................................................

    def rule0():   # motion in defined line
        # y=mx+c
        try:
            m = (click1["y"] - click2["y"]) / (click1["x"] - click2["x"])
            c = click1["y"] - m * click1["x"]
        except:
            m = "inf"
            c = None

        for i, j in conn_points:
            try:
                m1 = (anchor_points[i][1] - anchor_points[j][1]) / (anchor_points[i][0] - anchor_points[j][0])
                c1 = anchor_points[i][1] - m1 * anchor_points[i][0]
            except:
                m1 = "inf"
                c1 = None

            if m1 == m and c1 == c:
                return True
        else:
            return False

    def rule1():  # validate movement to neighbouring point exclusively

        ML = sqrt(pow(click2["y"] - click1["y"], 2) + pow(click2["x"] - click1["x"], 2))

        if ML in [SLL, DLL]:
            return True
        else:
            return False

    def rule2():  # invalidate movement to all occupied points

        if [click2["x"], click2["y"]] not in (button_pos_cp + button_pos_op):
            return True
        else:
            return False

    def rule3():  # validate jump over opposite team

        ML = sqrt(pow(click2["y"] - click1["y"], 2) + pow(click2["x"] - click1["x"], 2))

        if ML in [2 * SLL, 2 * DLL]:
            i = [click1["x"] + (click2["x"] - click1["x"]) / 2, click1["y"] + (click2["y"] - click1["y"]) / 2]
            for j in range(0, 16):
                if button_pos_op[j] == i:
                    return j + 1
            else:
                return False

        else:
            return False

    def check_rules(): #check various combinations of rules are satisfied

        if rule0() and rule2():
            if rule1() and _pass == False:
                return -1
            elif rule3():
                return rule3()

        return False

    # ............................................................
    if click1 == "pass":
        change_cp()
        return

    elif click2 == "remove":
        if [click1["x"], click1["y"]] in button_pos_op:
            if check_removable(click1) == True:
                remove_button(click1["bn"])
                click_no = 0
            else:
                wrong_sound.play()
        click_no = 0
        return

    elif ([click1["x"], click1["y"]] in button_pos_cp) and ([click2["x"], click2["y"]] in anchor_points):
        result = check_rules()

        if result != False:

            if result == -1:
                make_move(click1["bn"], click2["point"])
                change_cp()

            else:
                make_move(click1["bn"], click2["point"])
                remove_button(rule3() - 1)
                _pass = True
                all_sprites.add(pass_active)

            click_no = 0
            return

    all_sprites.remove(remove_active)
    all_sprites.add(remove_passive)
    try:
        if [click1["x"], click1["y"]] == [click2["x"], click2["y"]]:
            click_no = 0
            return
    except:
        pass

    wrong_sound.play()
    click_no = 0


def first_page(mx=None, my=None):
    global present
    global controls
    global tap1, tap2
    global running
    global initialize_dynamic_varaibles

    time.sleep(0.2)

    present = "first_page"

    def construct_first_page():
        global controls

        controls = [PLAY, RULES, ABOUT, QUIT]

        for i in [0, 1, 2, 3]:
            fpage_all_sprites.add(controls[i])
        return

    def execute_inp(mx, my):
        for i in range(len(controls)):
            if clicked(controls[i].rect.center, (200, 60), mx, my):
                next_action(i)
                return
        else:
            return

    def next_action(i):
        time.sleep(0.1)
        global present
        global fpage_all_sprites
        global tap1, tap2
        global running
        global initialize_dynamic_varaibles

        def display(page, tap):
            global tap1
            global tap2
            global fpage_all_sprites

            if tap == True:
                fpage_all_sprites.add(page)
            else:
                fpage_all_sprites.remove(page)
            return

        if i == 0:
            idv = Initialize_dynamic_varaibles()
            begin_sound.play()
            time.sleep(0.4)
            present = "game"
        elif i == 1:
            tap1 = not tap1
            select_sound.play()
            display(rules_page, tap1)
        elif i == 2:
            tap2 = not tap2
            select_sound.play()
            display(about_page, tap2)
        elif i == 3:
            time.sleep(0.3)
            select_sound.play()
            running = False
        elif i == 4:
            select_sound.play()
            construct_first_page()

    if mx != None and my != None:
        execute_inp(mx, my)
        return

    construct_first_page()


def endgame(winner):
    global present
    time.sleep(1)

    if winner == True:
        red_won = Controls("redwon.png", (WIDTH / 2, HEIGHT / 2))
        all_sprites.remove(red_move, remove_active, remove_passive, pass_active, pass_passive)
        all_sprites.add(red_won)

    else:
        blue_won = Controls("bluewon.png", (WIDTH / 2, HEIGHT / 2))
        all_sprites.remove(blue_move, remove_active, remove_passive, pass_active, pass_passive)
        all_sprites.add(blue_won)
    win_sound.play()
    present = "game_over"
    return


def game_over():  # disables all other options after game over except quit.
    if clicked(quit.pos, (200, 60), mx, my):
        select_sound.play()
        first_page()
        return
    return


running = True
first_page()
present = "first_page"

while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if present == "first_page":
                first_page(mx, my)
            elif present == "game":
                valid_click(mx, my)

    if click_no == 1:
        all_sprites.add(selected)
    else:
        try:
            all_sprites.remove(selected)
        except:
            pass

    if present == "game":
        BG_sprites.draw(screen)
        all_sprites.draw(screen)
    elif present == "first_page":
        fpage_BG_sprites.draw(screen)
        fpage_all_sprites.draw(screen)
    elif present == "game_over":
        all_sprites.draw(screen)
        game_over()

    # after drawing flip (double buffering)
    pygame.display.flip()

pygame.quit()
