from dataclasses import dataclass
from collections import defaultdict, Counter

import click

SEEN = 9


def basin_search(locations, M, N, i, j):
    click.echo(f"{i},{j} --> {locations[i][j]}")
    if locations[i][j] == SEEN:
        return 0

    locations[i][j] = SEEN
    result = 1
    # TODO: add the SEEN check here as well to avoid log spam.
    if i > 0:
        click.echo(f"{i},{j}: go up")
        result += basin_search(locations, M, N, i-1, j)
    if i < M - 1:
        click.echo(f"{i},{j}: go down")
        result += basin_search(locations, M, N, i+1, j)
    if j > 0:
        click.echo(f"{i},{j}: go left")
        result += basin_search(locations, M, N, i, j-1)
    if j < N - 1:
        click.echo(f"{i},{j}: go right")
        result += basin_search(locations, M, N, i, j+1)

    locations[i][j] = SEEN
    return result


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    locations = [[int(c) for c in l.strip()] for l in input_file]
    click.echo(str(locations))
    M, N = len(locations), len(locations[0])
    basins = []
    for i in range(M):
        for j in range(N):
            # Minor mod to prevent confirm annoyance.
            if locations[i][j] == SEEN:
                continue
            b = basin_search(locations, M, N, i, j)
            basins.append(b)
            # click.confirm(str(b))

    basins.sort()
    click.echo(f"Found following basins: {basins}")
    click.secho(f"Answer is {basins[-1] * basins[-2] * basins[-3]}", fg="green")


if __name__ == "__main__":
    main()
