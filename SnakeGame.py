import random
import pygame
import time

class Renderer:
    def __init__(self, boardHeight, boardWidth, cellSize = 20):
        pygame.init()
        self.cellSize = cellSize
        self.screen = pygame.display.set_mode((boardWidth * cellSize, boardHeight * cellSize))
        pygame.display.set_caption("Snake Game")
        self.colors = {
            "background": (124,252,0),
            "snake": (30, 144, 255),
            "food": (255, 0, 0),
            "grid": (50, 50, 50)
        }

    def draw(self, gameState):
        self.screen.fill(self.colors["background"])
        self.drawGrid(gameState.board)
        self.drawSnake(gameState.snake)
        self.drawFood(gameState.board)
        pygame.display.flip()       # updates the screen

    def drawGrid(self, board):
        for y in range(board.boardHeight):
            for x in range(board.boardWidth):
                rect = pygame.Rect(x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize)
                pygame.draw.rect(self.screen, self.colors["grid"], rect, 1)

    def drawSnake(self, snake):
        for (row, col) in snake.body:
            rect = pygame.Rect(col * self.cellSize, row * self.cellSize, self.cellSize, self.cellSize)
            pygame.draw.rect(self.screen, self.colors["snake"], rect)
    
    def drawFood(self, board):
        if board.food:
            row, col = board.food
            rect = pygame.Rect(col * self.cellSize, row * self.cellSize, self.cellSize, self.cellSize)
            pygame.draw.rect(self.screen, self.colors["food"], rect)

class GameState:
    def __init__(self, boardHeight, boardWidth):
        self.score = 0
        self.board = Board(boardHeight, boardWidth)
        self.snake = Snake(boardHeight // 2, boardWidth // 2)
        self.gameOver = False
        self.waitingForInput = True
        self.board.spawnFood(self.snake.body)
    
    def update(self):
        if self.waitingForInput:
            return
        food = self.board.food
        self.snake.moveSnake(food)
        head = self.snake.head()

        if not self.board.inBounds(head) or head in self.snake.body[1:]:
            self.gameOver = True
            return
        
        print(head)
        print(food)
        if head == food:
            self.board.spawnFood(self.snake.body)

class Snake:
    def __init__(self, startPositionRow, startPositionCol):
        self.body = []
        self.snakeDirection = 0
        self.initializeSnake(startPositionRow, startPositionCol)
    
    def initializeSnake(self, startPositionRow, startPositionCol):
        # initialize snake position on board
        self.body.append((startPositionRow, startPositionCol))
        self.body.append((startPositionRow, startPositionCol - 1))
        self.body.append((startPositionRow, startPositionCol - 2))
    
    def moveSnake(self, food):
        nextCell = self.head()
        if (self.snakeDirection == 0):      # left
            nextCell = (nextCell[0], nextCell[1] - 1)
        elif (self.snakeDirection == 1):    # up
            nextCell = (nextCell[0] - 1, nextCell[1])
        elif (self.snakeDirection == 2):    # right
            nextCell = (nextCell[0], nextCell[1] + 1)
        else:                               # down
            nextCell = (nextCell[0] + 1, nextCell[1])
        self.body.insert(0, nextCell)
        if nextCell != food:
            self.body.pop()

    def head(self):
        return self.body[0]

    def setDirection(self, direction):
        self.snakeDirection = direction


class Board:
    def __init__(self, boardHeight, boardWidth):
        self.boardHeight = boardHeight
        self.boardWidth = boardWidth
        self.food = None
    
    def spawnFood(self, snakeCells):
        while True:
            pos = (random.randint(0, self.boardHeight - 1), random.randint(0, self.boardWidth - 1))
            if pos not in snakeCells:
                self.food = pos
                break

    def inBounds(self, pos):
        return 0 <= pos[0] < self.boardHeight and 0 <= pos[1] < self.boardWidth

def main():
    # initialize snake and board
    boardHeight = 15
    boardWidth = 15
    gameState = GameState(boardHeight, boardWidth)
    renderer = Renderer(boardWidth, boardHeight, 25)

    clock = pygame.time.Clock()

    directionMap = {
        pygame.K_LEFT: 0,
        pygame.K_UP: 1, 
        pygame.K_RIGHT: 2,
        pygame.K_DOWN: 3
    }

    while not gameState.gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in directionMap:
                if directionMap[event.key] != gameState.snake.snakeDirection:
                    gameState.snake.setDirection(directionMap[event.key])
                
                if gameState.waitingForInput:
                    gameState.waitingForInput = False

        gameState.update()
        renderer.draw(gameState)
        clock.tick(10)

    print("Game Over!")
    time.sleep(2)
    return 




if __name__ == "__main__":
    main()