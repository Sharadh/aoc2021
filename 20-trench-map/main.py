import typing
from copy import deepcopy
from functools import reduce

import click


class Parts:
    PART_ONE = "part-one"
    PART_TWO = "part-two"


# class Window:
#     x: int
#     y: int
#     size: int
#
#     M: int
#     N: int
#     image: dict[typing.Tuple[int, int], str]
#
#     def move_right(self):
#         pass
#
#     def move_down(self):
#         pass


def neighbours(i, j):
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            yield i + x, j + y


def enhance(grid: typing.Dict[typing.Tuple[int, int], str], key: str, x_start: int, x_end: int, y_start: int, y_end: int):
    new_grid = {}
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            k = "".join(grid.get((x, y), "0") for x, y in neighbours(i, j))
            n = int(k, 2)
            new_grid[i, j] = key[n]
    return new_grid


def print_grid(grid, x_start, x_end, y_start, y_end):
    lines = []
    result = 0
    for i in range(x_start, x_end):
        l = ""
        for j in range(y_start, y_end):
            c = grid[i, j]
            if c == "1":
                result += 1
            l += "." if c == "0" else "#"
        lines.append(l)

    click.echo("\n".join(lines))
    click.secho(f"{result} pixels switched on in grid {x_end - x_start}x{y_end - y_start}!", fg="green")
    click.confirm("")


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("part", type=click.Choice([Parts.PART_ONE, Parts.PART_TWO]))
def main(input_file, part):
    key = next(input_file).strip().replace("#", "1").replace(".", "0")
    click.echo(key)
    click.confirm(f"{len(key)} pixels.")
    next(input_file)

    grid = {}
    for i, l in enumerate(input_file):
        for j, c in enumerate(l.strip()):
            grid[(i, j)] = "1" if c == "#" else "0"

    x_start, x_end, y_start, y_end = 0, i + 1, 0, j + 1
    print_grid(grid, x_start, x_end, y_start, y_end)
    for i in range(2):
        x_start -= 2
        y_start -= 2
        x_end += 2
        y_end += 2
        grid = enhance(grid, key, x_start, x_end, y_start, y_end)
        print_grid(grid, x_start, x_end, y_start, y_end)

    click.secho(f"Done!", fg="green")


if __name__ == "__main__":
    main()
