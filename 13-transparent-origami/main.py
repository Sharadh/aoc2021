import click

from collections import defaultdict


def print_grid(grid, M, N):
    lines = []
    result = 0
    for i in range(M + 1):
        l = ""
        for j in range(N + 1):
            if i in grid and j in grid[i]:
                l += "#"
                result += 1
            else:
                l += "."
        lines.append(l)
    click.echo(f"Grid size: {M + 1} x {N + 1}")
    click.echo("\n".join(lines))
    click.echo(f"Total of {result} dots visible.")
    click.confirm("?")


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    grid = defaultdict(dict)
    M = N = 0
    for l in input_file:
        if not l.strip():
            break
        x, y = [int(i) for i in l.strip().split(",")]
        grid[y][x] = True

        M = max(M, y)
        N = max(N, x)

    print_grid(grid, M, N)

    folds = []
    for l in input_file:
        instruction = l.strip()[11:]
        axis, number = instruction.split("=")
        folds.append((axis, int(number)))

    for axis, number in folds:
        if axis == "y":
            for y in range(number):
                for x in list(grid[M - y].keys()):
                    if y > N:
                        continue
                    grid[y][x] = True
            M = number - 1
        elif axis == "x":
            for y in range(M + 1):
                for x in list(grid[y].keys()):
                    if x > number:
                        grid[y][N - x] = True
            N = number - 1
        print_grid(grid, M, N)

    # click.secho(f"Answer found: {result}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
