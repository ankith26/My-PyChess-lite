import pygame
from chess import *
from gui import *

# Initialize regular pygame stuff.
pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('My-PyChess')

# Initialize chess variables
side = 0
board = (
    [[1, 7, "p"], [2, 7, "p"], [3, 7, "p"], [4, 7, "p"],
     [5, 7, "p"], [6, 7, "p"], [7, 7, "p"], [8, 7, "p"],
     [1, 8, "r"], [2, 8, "n"], [3, 8, "b"], [4, 8, "q"],
     [5, 8, "k"], [6, 8, "b"], [7, 8, "n"], [8, 8, "r"]
    ], [
     [1, 2, "p"], [2, 2, "p"], [3, 2, "p"], [4, 2, "p"],
     [5, 2, "p"], [6, 2, "p"], [7, 2, "p"], [8, 2, "p"],
     [1, 1, "r"], [2, 1, "n"], [3, 1, "b"], [4, 1, "q"],
     [5, 1, "k"], [6, 1, "b"], [7, 1, "n"], [8, 1, "r"]
    ])
flags = [[True for _ in range(4)], None]

sel = prevsel = [0, 0]

# Main function for showing the chess board. Call it once every game loop.
def showScreen(win, side, board, flags, pos):
    drawBoard(win)
    if isEnd(side, board, flags):
        if isChecked(side, board):
            win.blit(CHECKMATE,(120, 0))
            win.blit(PIECES[side]['k'], (270, 0))
        else:
            win.blit(STALEMATE, (150, 0))
    else:
        if isChecked(side, board):
            win.blit(CHECK, (180, 0))
            
        if isOccupied(side, board, pos):
            x, y = pos[0] * 50, pos[1] * 50
            pygame.draw.rect(win, (255, 255, 0), (x, y, 50, 50))
    drawPieces(win, board)

# return getChoice only if pawn has reached promotion state
def getPromote(win, side, board, fro, to):
    if getType(side, board, fro) == "p":
        if (side == 0 and to[1] == 1) or (side == 1 and to[1] == 8):
            return getChoice(win, side)
        
running = True        
while running:
    clock.tick(30)
    # Iterate over events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 < x < 450 and 50 < y < 450:
                x, y = x // 50, y // 50
                prevsel = sel
                sel = [x, y]
            # If move is legal, do the move - update chess variables
            if isValidMove(side, board, flags, prevsel, sel):
                promote = getPromote(win, side, board, prevsel, sel)
                side, board, flags = makeMove(
                    side, board, prevsel, sel, flags, promote)
    # Show screen                    
    showScreen(win, side, board, flags, sel)
    pygame.display.update()
    
# Quit pygame
pygame.quit()