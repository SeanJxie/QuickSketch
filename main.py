import pygame as pg
import sys
import os
from tkinter import Tk, filedialog, messagebox

"""

TODO: Eraser

"""

pg.init()

ROOT = Tk()
ROOT.withdraw()

DISPLAY_SIZE = ROOT.winfo_screenwidth() // 2, ROOT.winfo_screenheight() // 2
WIN_NAME = "QuickSketch"

BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)
RED   = (255, 0  , 0  )

L_MOUSE  = 1
R_MOUSE  = 3
U_SCROLL = 4
D_SCROLL = 5

DELIMITER = 'e'
FILE_EXT = "quicksketch"

INTRO_DIALOGUE = """
Press "L" to load a file
Press "S" to save a file
Draw with leftclick
Erase with rightclick
Adjust size with scroll

Press "OK" to get started!
"""

M_SCROLL_INC = 5
MIN_ERASER_RAD = 5
MAX_ERASER_RAD = 100
LINE_WIDTH = 3

CURSOR_WIDTH = 1

MAIN_SURFACE = pg.display.set_mode(DISPLAY_SIZE, pg.RESIZABLE)
try:
    base_path = sys._MEIPASS  # May not exist
except Exception:
    base_path = os.path.abspath(".")
WIN_ICON = pg.image.load(os.path.join(base_path, 'assets//pencil_icon.ico'))


def save_file(pLst: list) -> None:
    #print("SAVE")
    path = filedialog.asksaveasfilename(
        defaultextension=FILE_EXT,
        filetypes=[(f"{FILE_EXT} Files", f"*.{FILE_EXT}")]
    )

    if not path:
        return

    with open(path, 'w') as oFile:
        for p in pLst:
            if p != DELIMITER:
                oFile.write(f"{p[0]} {p[1]}\n")
            else:
                oFile.write(DELIMITER + '\n')


def load_file() -> list:
    #print("LOAD")
    path = filedialog.askopenfilename(
        filetypes=[(f"{FILE_EXT} Files", f"*.{FILE_EXT}")]
    )

    if not path:
        return []

    with open(path, 'r') as iFile:
        pListStr = iFile.read().split('\n')

    pList = []
    # (x, y)
    for e in pListStr:
        if e != DELIMITER:
            pList.append(tuple(map(int, e.split())))
        else:
            pList.append(DELIMITER)

    return pList[:-1] # Omit terminating newline char


def dst(a: tuple, b: tuple) -> float:
    return ((b[0]- a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5


def draw_points(pLst: list, wt: int) -> None:
    i = 0
    while i < len(pLst) - 1:
        if pLst[i + 1] == DELIMITER or pLst[i] == DELIMITER: # Delimiter ahead! Skip index to disconnect line.
            i += 1
        else:
            pg.draw.line(MAIN_SURFACE, BLACK, pLst[i], pLst[i + 1], wt)

        i += 1

def draw_cursor(p: tuple, r: int, col: tuple):
    pg.draw.circle(MAIN_SURFACE, col, p, r, CURSOR_WIDTH)


# Main program loop
def main() -> None:
    pg.display.set_caption(WIN_NAME)
    pg.display.set_icon(WIN_ICON)
    pg.mouse.set_visible(False)

    pointList = []
    drawing = False
    erasing = False
    eraser_rad = 10

    while 1:
        mPos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    save_file(pointList)

                elif event.key == pg.K_l:
                    pointList = load_file()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == L_MOUSE:
                    drawing = True
                elif event.button == R_MOUSE:
                    erasing = True

                elif event.button == U_SCROLL:
                    if erasing and eraser_rad < MAX_ERASER_RAD:
                        eraser_rad += M_SCROLL_INC

                elif event.button == D_SCROLL:
                    if erasing and eraser_rad > MIN_ERASER_RAD:
                        eraser_rad -= M_SCROLL_INC
        
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == L_MOUSE:
                    drawing = False
                elif event.button == R_MOUSE:
                    erasing = False

        if drawing:
            if mPos not in pointList:
                pointList.append(mPos)

        elif erasing:
            for i in range(len(pointList)):
                if pointList[i] != DELIMITER:
                    if dst(pointList[i], mPos) < eraser_rad:
                        pointList[i] = DELIMITER


        else: # We've stopped drawing.
            if pointList and pointList[-1] != DELIMITER: # If a delimiter has not already been appended, do so.
                pointList.append(DELIMITER)

        # Render
        MAIN_SURFACE.fill(WHITE)
        draw_points(pointList, LINE_WIDTH)
        
        if erasing:
            draw_cursor(mPos, eraser_rad, RED)
        else:
            draw_cursor(mPos, 2 * LINE_WIDTH, BLACK)

        pg.display.update()


# Run
if __name__ == "__main__":
    messagebox.showinfo(title=f"Welcome to {WIN_NAME}!", message=INTRO_DIALOGUE)
    main()


