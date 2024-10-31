import cv2 as cv
from sudoku import Sudoku
from OCR import find_board
from pre_processing import find_cells


def solve_sudoku(board):
    puzzle = Sudoku(3, 3, board=board.tolist())
    #puzzle.show()
    #solution.show_full()
    solution = puzzle.solve()
    if solution:
        solution.show()
        return solution.board  # Return the solved board
    else:
        print("No solution found for the Sudoku puzzle.")
        return None


def main(img_path):
    try:
        img1 = cv.imread(img_path)
        if img1 is None:
            print("Error: Image not loaded. Check the file path or image file.")
            return

        cells, cell_coord, cell_size, img_ready = find_cells(img1)
        board = find_board(cells)
        solution_board = solve_sudoku(board)

        if solution_board is None:
            return  # Exit if no solution is found

        for i in range(9):
            for j in range(9):
                #fill empty cells
                digits = []
                if board[i][j] == 0:
                    num = solution_board[i][j]
                    coord = cell_coord[i][j]
                    cell_center_x = coord[0] + cell_size // 2
                    cell_center_y = coord[1] + cell_size // 2
                    #cv.circle(img_ready, (cell_center_x,cell_center_y), 5, (0, 0, 255), -1)

                    text_size,baseline = cv.getTextSize(str(num), cv.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)
                    text_x = cell_center_x - text_size[0] // 2
                    text_y = cell_center_y + text_size[1] // 2

                    text_y += baseline //2
                    solved = cv.putText(img_ready, str(num), (text_x,text_y), cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)

        output_path = 'solutions/sudokuSolution.jpg'
        cv.imwrite(output_path, solved)
        return output_path


    except Exception as e:
            print(f"An error occurred: {e}")

