import click

M = N = 10


def print_grid(grid):
    lines = []
    for i in range(M):
        lines.append("  ".join(str(x).rjust(2, " ") for x in grid[i]))
    grid = "\n".join(lines)
    click.secho(grid, fg="yellow")
    # click.confirm("?")


def neighbours(i, j):
    if i > 0:
        if j > 0:
            yield i-1, j-1
        yield i-1, j
        if j < N - 1:
            yield i-1, j+1

    if j > 0:
        yield i, j-1
    if j < N - 1:
        yield i, j+1

    if i < M - 1:
        if j > 0:
            yield i+1, j-1
        yield i+1, j
        if j < N - 1:
            yield i+1, j+1


def simulate_step(grid):
    result = 0
    flashed = set()

    # Increment.
    for i in range(M):
        for j in range(N):
            grid[i][j] += 1

    # Cascade.
    candidates = [(M-i-1, N-j-1) for i in range(M) for j in range(N)]
    while candidates:
        i, j = candidates.pop()
        # click.echo(f"Evaluating {i},{j}")
        if grid[i][j] > 9:
            if (i, j) in flashed:
                continue

            # Flash!
            click.echo(f"Flashing at {i},{j}!")
            flashed.add((i, j))
            for x, y in neighbours(i, j):
                grid[x][y] += 1
                candidates.append((x, y))
            print_grid(grid)
        # print_grid(grid)

    # Reset!
    for i, j in flashed:
        grid[i][j] = 0
        result += 1
    return result


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    result = 0
    grid = {}
    for i, l in enumerate(input_file):
        grid[i] = [int(x) for x in l.strip()]

    # for i in range(100):
    #     flashes = simulate_step(grid)
    #     result += flashes
    #     click.echo(f"Step {i}: {flashes} => {result}")
    #     # click.confirm("?")
    #
    # click.secho(f"Answer after 100 steps is {result}", fg="green")

    i = 1
    while True:
        flashes = simulate_step(grid)
        click.echo(f"Step {i}: {flashes}")
        if flashes == 100:
            click.secho(f"Answer found! Exiting.", fg="green")
            break
        i += 1


if __name__ == "__main__":
    main()
