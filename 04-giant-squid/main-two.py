import click


CROSS = 'x'


def mark(board, num):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == num:
                board[i][j] = CROSS


def check(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != CROSS:
                break
        else:
            return True

    for i in range(len(board)):
        for j in range(len(board[j])):
            if board[j][i] != CROSS:
                break
        else:
            return True


def win(board, num):
    sum_ = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != CROSS:
                sum_ += int(board[i][j])

    return sum_ * int(num)


def play(order, boards):
    for o in order:
        new_boards = []
        last = None
        for i, b in enumerate(boards):
            mark(b, o)
            if check(b):
                click.echo(f"Board {i} won with number {o}!")
                last = b
                continue
            else:
                new_boards.append(b)
        if len(new_boards) == 0:
            click.echo(f"Last one standing!")
            click.echo(str(last))
            return win(last, o)
        boards = new_boards


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    order = next(input_file).strip().split(",")
    click.echo(str(order))
    # click.prompt("")
    next(input_file)

    boards = []
    b = []
    for l in input_file:
        l = l.strip()
        if l:
            b.append(l.strip().split())
            continue

        click.echo(str(b))
        # click.prompt("")
        boards.append(b)
        b = []

    result = play(order, boards)

    click.echo(f"{result}")


if __name__ == "__main__":
    main()
