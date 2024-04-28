import random


def generate_groups():
    return {f'group{num}': [1, 2, 3, 4, 5, 6, 7, 8, 9] for num in range(9)}


def get_free_numbers(row, columns, row_index, groups, group_number):
    return [free_num for free_num in row if free_num in columns[f'column{str(row_index)}']
            and free_num in groups[f'group{str(group_number)}']]


def generator_sudoku():
    rows_list = []
    while len(rows_list) != 9:
        row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        columns = {f'column{num}': [1, 2, 3, 4, 5, 6, 7, 8, 9] for num in range(9)}
        groups = generate_groups()
        for column_index in range(9):
            sequence_of_num_in_row = []
            for row_index in range(9):
                group_number = (row_index // 3) * 3 + (column_index // 3)
                row_starting_group_index = (group_number // 3) * 3

                free_numbers = get_free_numbers(row, columns, row_index, groups, group_number)
                while not free_numbers:
                    for index1, element in enumerate(sequence_of_num_in_row):
                        columns[f'column{str(index1)}'].append(element)
                    counter = 0  # if it reaches 3 it means we are in the next row of groups
                    jump = 0  # this tells you how much to the right the group index should move from the level
                    for element in sequence_of_num_in_row:
                        groups[f'group{str(row_starting_group_index + jump)}'].append(element)
                        counter += 1
                        if counter == 3:
                            jump = 1
                        if counter == 6:
                            jump = 2
                    groups = generate_groups()
                    sequence_of_num_in_row.clear()
                    row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    free_numbers = get_free_numbers(row, columns, row_index, groups, group_number)
                element = random.choice(free_numbers)
                sequence_of_num_in_row.append(element)
                columns[f'column{str(row_index)}'].remove(element)
                groups[f'group{str(group_number)}'].remove(element)
                row.remove(element)
            if len(sequence_of_num_in_row) == 9:
                rows_list.append(sequence_of_num_in_row)
            else:
                rows_list.clear()

            row = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    flattened_list_of_sudoku_numbers = [result for element in rows_list for result in element]
    dict_with_sudoku_numbers = {f'field{index}': element_from_list
                                for index, element_from_list in enumerate(flattened_list_of_sudoku_numbers)}

    return dict_with_sudoku_numbers
