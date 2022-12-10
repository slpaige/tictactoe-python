import re


def check_matrix(matrix_to_check):
    global x_three_row
    global o_three_row

    for group in matrix_to_check:
        x_count = 0
        o_count = 0

        for win in group:
            coords = [int(x) for x in win.split(":")]
            if placement_matrix[coords[0]][coords[1]] == "X":
                x_count += 1
            elif placement_matrix[coords[0]][coords[1]] == "O":
                o_count += 1

        if x_count == 3 and not x_three_row:
            x_three_row = True

        if o_count == 3 and not o_three_row:
            o_three_row = True

    return x_three_row or o_three_row


def check_game_state():
    found_winner = check_matrix(win_row_matrix)

    if not found_winner:
        found_winner = check_matrix(win_col_matrix)

    if not found_winner:
        found_winner = check_matrix(win_dia_matrix)

    count_each_entry()


def count_each_entry():
    global count_x
    global count_o

    count_x = 0
    count_o = 0

    for row in placement_matrix:
        for col in row:
            if col == "X":
                count_x += 1
            elif col == "O":
                count_o += 1


def generate_matrix():
    global played_coords
    placement_matrix.clear()

    for x, row in enumerate(grid_build):
        # build matrix row
        row_split = [*row]
        placement_matrix.append([])

        # set row:col value
        y_count = 0
        for col in row_split:
            placement_matrix[x].append(col)
            if col == "X" or col == "O":
                played_coords.add(f"{x} {y_count}")
            y_count += 1


def render_game_grid():
    print("---------")
    for row in placement_matrix:
        print(f"| {' '.join(row)} |")
    print("---------")


def player_turn():
    while True:
        placement = input()
        regex_coords = re.search("^[1-3] [1-3]$", placement)
        regex_text = re.search("^[^0-9]+\s?[^0-9]", placement)

        if regex_text:
            print("You should enter numbers")
            continue

        if not regex_coords:
            print("Coordinates should be from 1 to 3!")
            continue

        if regex_coords:
            player_coords = placement.split(' ')
            player_row = int(player_coords[0]) - 1
            player_col = int(player_coords[1]) - 1

            # check already played coords
            if f"{player_row} {player_col}" in played_coords:
                print("This cell is occupied! Choose another one!")
            else:
                # update game grid
                temp_list = list(grid_build[player_row])
                temp_list[player_col] = "X" if player_one else "O"
                grid_build[player_row] = "".join(temp_list)
                break


# row:col
win_row_matrix = [["0:0", "0:1", "0:2"], ["1:0", "1:1", "1:2"], ["2:0", "2:1", "2:2"]]
win_col_matrix = [["0:0", "1:0", "2:0"], ["0:1", "1:1", "2:1"], ["0:2", "1:2", "2:2"]]
win_dia_matrix = [["0:0", "1:1", "2:2"], ["0:2", "1:1", "2:0"]]
placement_matrix = []
played_coords = set()

# if count > 1 from either other, impossible
# if count x and count y != 9, game not finished
count_x = 0
count_o = 0

# if either have three in row that letter wins
# if both have 3 in row, impossible
x_three_row = False
o_three_row = False

# grid_build = re.findall("...", input())
grid_build = ["   ", "   ", "   "]
player_one = True

generate_matrix()
render_game_grid()

# game loop
while True:
    player_turn()
    generate_matrix()
    render_game_grid()
    check_game_state()

    if abs(count_x - count_o) > 1:
        print("Impossible")
        break
    elif x_three_row and o_three_row:
        print("Impossible")
        break
    elif x_three_row:
        print("X wins")
        break
    elif o_three_row:
        print("O wins")
        break
    elif count_x + count_o == 9:
        print("Draw")
        break
    # elif count_x + count_o < 9:
    #     print("Game not finished")

    player_one = not player_one
