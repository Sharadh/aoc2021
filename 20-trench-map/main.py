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


def enhance(grid: typing.Dict[typing.Tuple[int, int], str], key: str, M: int, N: int):
    new_grid = {}
    for i in range(M):
        for j in range(N):
            k = "".join(grid.get((x, y), "0") for x, y in neighbours(i, j))
            n = int(k, 2)
            new_grid[i, j] = key[n]
    return new_grid


def print_grid(grid, M, N):
    lines = []
    result = 0
    for i in range(M):
        l = ""
        for j in range(N):
            c = grid[i, j]
            if c == "1":
                result += 1
            l += c
        lines.append(l)

    click.echo("\n".join(lines))
    click.echo(f"{result} pixels switched on!")
    click.confirm("")


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("part", type=click.Choice([Parts.PART_ONE, Parts.PART_TWO]))
def main(input_file, part):
    result = None

    key = next(input_file).strip().replace("#", "1").replace(".", "0")
    click.echo(key)
    click.confirm(f"{len(key)} pixels.")
    next(input_file)

    grid = {}
    for i, l in enumerate(input_file):
        for j, c in enumerate(l.strip()):
            grid[(i, j)] = "1" if c == "#" else "0"

    M, N = i, j
    print_grid(grid, M, N)
    for i in range(2):
        grid = enhance(grid, key, M, N)
        print_grid(grid, M, N)

    click.secho(f"Answer found! {result}", fg="green")


if __name__ == "__main__":
    main()
