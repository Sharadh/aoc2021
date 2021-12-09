from dataclasses import dataclass
from collections import defaultdict, Counter

import click


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    locations = [[int(c) for c in l.strip()] for l in input_file]
    click.echo(str(locations))
    result = 0
    M, N = len(locations), len(locations[0])
    for i in range(M):
        for j in range(N):
            candidates = []
            # if i > 0 and j > 0:
            #     candidates.append(locations[i-1][j-1])
            # if i > 0 and j < len(locations) - 1:
            #     candidates.append(locations[i-1][j+1])
            # if i < len(locations) - 1 and j > 0:
            #     candidates.append(locations[i+1][j-1])
            # if i < len(locations) - 1 and j < len(locations) - 1:
            #     candidates.append(locations[i+1][j+1])

            if i > 0:
                candidates.append(locations[i-1][j])
            if i < M - 1:
                candidates.append(locations[i+1][j])
            if j > 0:
                candidates.append(locations[i][j-1])
            if j < N - 1:
                candidates.append(locations[i][j+1])
            click.echo(f"{i},{j} -> {locations[i][j]} -> {candidates}")
            if all(locations[i][j] < l for l in candidates):
                click.echo(f"{i},{j} has a low point; value = {locations[i][j]}!")
                result += locations[i][j] + 1
            # click.confirm("?")

    click.secho(f"Answer is {result}", fg="green")


if __name__ == "__main__":
    main()
