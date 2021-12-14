import click

from collections import defaultdict, Counter

import sys


def simulate(state, transform):
    new = ""
    for a, b in zip(state, state[1:] + " "):
        pair = a + b
        insert = transform.get(pair)
        if not insert:
            new += a
        else:
            new += a + insert
    return new


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    state = next(input_file).strip()
    next(input_file)

    transform = {}
    for l in input_file:
        pair, insert = l.strip().split(" -> ")
        transform[pair] = insert

    for i in range(10):
        new = simulate(state, transform)
        click.echo(f"Step {i + 1}")
        # click.echo(f"Step {i + 1}: {state} -> {new}")
        # click.confirm("?")
        state = new

    counts = Counter(state)
    x, y = -sys.maxsize, sys.maxsize
    for v in counts.values():
        if v > x:
            x = v
        if v < y:
            y = v

    click.secho(f"Answer found: {x - y}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
