import pygame
import sys
import asyncio
import time

# Initialize Pygame
pygame.init()

# Set up the variables for our display
WINDOW_SIZE = (810, 810)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CELL_SIZE = 90
GRID_SIZE = 8

# Set up the display screen where we will draw everything we need
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku")

# The font we will use when we display the numbers
num_font = pygame.font.SysFont("arial", 45)

# This is the solvable Sudoku puzzle we will use as our example. The '.' is a simple placeholder for the
# entries that we have to solve for.

board = [["5","3",".",".","7",".",".",".","."],
         ["6",".",".","1","9","5",".",".","."],
         [".","9","8",".",".",".",".","6","."],
         ["8",".",".",".","6",".",".",".","3"],
         ["4",".",".","8",".","3",".",".","1"],
         ["7",".",".",".","2",".",".",".","6"],
         [".","6",".",".",".",".","2","8","."],
         [".",".",".","4","1","9",".",".","5"],
         [".",".",".",".","8",".",".","7","9"]]


# Function to draw our grid -- we draw lines along the x and y axis
def draw_grid(grid = []):

    x_count = 0
    y_count = 0

    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):

        # We want the borders of the 3x3 boxes to be thicker than the other lines.
        # We do this by keeping track of where we are on the board with the 'x_count' and 
        # 'y_count' variables
        if x_count % 3 == 0:
            pygame.draw.line(screen, BLACK, (x,0), (x, WINDOW_SIZE[1]), 5)

        else:
            pygame.draw.line(screen, BLACK, (x,0), (x, WINDOW_SIZE[1]))
        x_count += 1

    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        if y_count % 3 == 0:
            pygame.draw.line(screen, BLACK, (0,y), (WINDOW_SIZE[0], y), 5)

        else:
            pygame.draw.line(screen, BLACK, (0,y), (WINDOW_SIZE[0], y))
        y_count += 1
    

# Function to determine if the Sudoku board is valid
def isValid(row, col, number, board):

    for i in range(9):

        # Check the row
        if board[i][col] == number:
            return False
        
        # Check the column
        if board[row][i] == number:
            return False
        
        # Formula to check the appropriate 3x3 box 
        if board[3*(row//3) + i//3][3*(col//3) + i%3] == number:
            return False
        
    return True

n = 9

# Function to solve our Sudoku puzzle. We define it as an async function because we want to delay
# the process of displaying the numbers on the board. This allows us to visualize the code.
async def solve(row, col, board):
    # If we've completed the last row (n-1), then we are done.
    if row == n:
        return True
    # If we've reached the last column on a given row, attempt to solve the next row.
    if col == n:
        return await solve(row+1, 0, board)
    
    # If we encounter an 'empty' entry, begin the solving process.
    if board[row][col] == ".":
        for i in range(1, 10):
            if isValid(row, col, str(i), board):
                board[row][col] = str(i)
                num = pygame.font.Font.render(num_font, str(i), True, (0,0,0))
                screen.blit(num, (33+(CELL_SIZE * col),20+(CELL_SIZE*row)) )
                pygame.display.flip()
                await asyncio.sleep(0.01)
                
                # Recursively call the function. If we continue to have valid entries, we will see 
                # the board display the numbers on the board. If we correctly solved the puzzle (i.e. 
                # completed the last row) then this will return 'True'.
                if await solve(row, col + 1, board):
                    return True
                
                # If we encounter an invalid move at some point in the recursion, we backtrack.
                # In this case, we simply change the value on our board and draw a white box that 
                # covers the previous number, which basically erases it from the board.
                else:
                    board[row][col] = "."
                    surf = pygame.Surface((CELL_SIZE-50, CELL_SIZE-30))
                    surf.fill(WHITE)
                    screen.blit(surf, (33+(CELL_SIZE * col),20+(CELL_SIZE*row)) )

        return False
    
    # When we encounter a space with a prefilled entry, skip it and go to the next column. 
    else:
        return await solve(row, col + 1, board)
    


# Main game loop
async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
        await asyncio.sleep(3)

        # Display our board with the prefilled entries
        board = [["5","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]]
        for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    num = pygame.font.Font.render(num_font, board[i][j], True, (0,0,0))
                    screen.blit(num, (33+(CELL_SIZE * j),20+(CELL_SIZE*i)) )
        pygame.display.flip()
        await asyncio.sleep(5)
                    
        row = 0
        col = 0
        
        time.sleep(1)

        # Solve the Sudoku Puzzle!
        await solve(0,0, board)
        await asyncio.sleep(5)
        #break 


if __name__ == "__main__":
    asyncio.run(main())
