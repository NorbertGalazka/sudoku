from flask import Flask, request, render_template, redirect, url_for, session
from sudoku import generator_sudoku
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey1234'


def create_sudoku_without_some_val(arg):
    new_dict_with_sudoku_without_values = arg

    for key, val in new_dict_with_sudoku_without_values.items():
        random_int = random.randint(1, 2)
        if random_int == 1:
            new_dict_with_sudoku_without_values[key] = ''
        else:
            new_dict_with_sudoku_without_values[key] = val

    return new_dict_with_sudoku_without_values


original_sudoku = generator_sudoku()
sudoku_without_val = create_sudoku_without_some_val(original_sudoku.copy())


@app.route('/', methods=['GET', 'POST'])
def index():
    bad_val_index = request.args.get('bad_val_index')
    if bad_val_index is not None:
        bad_val_index = int(bad_val_index)
    bad_val = request.args.get('bad_val')

    global original_sudoku, sudoku_without_val

    if request.method == 'POST':
        val_list = []
        for i in range(81):
            value = request.form.get(f'field{i}', '')
            val_list.append(value)
            sudoku_without_val[i] = value
            if value != str(original_sudoku[i]) and value != '':
                session['bad_val_index'] = i
                session['bad_val'] = value
                return redirect(url_for('index', bad_val_index=i,  bad_val=value)) #porazka
        if all(val_list):
            return render_template('sudoku_board.html', sudoku_without_val=sudoku_without_val, win=1) #win

        return render_template('sudoku_board.html', sudoku_without_val=sudoku_without_val) #dobre wprowadzenie

    elif bad_val:
        return render_template('sudoku_board.html', sudoku_without_val=sudoku_without_val, bad_val_index=bad_val_index, lost=1) #porazka z redirecta

    else:
        original_sudoku = generator_sudoku()
        sudoku_without_val = create_sudoku_without_some_val(original_sudoku.copy())
        return render_template('sudoku_board.html', sudoku_without_val=sudoku_without_val)  #start gry


if __name__ == "__main__":
    app.run()
