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
@click.argument("rounds", type=click.INT, default=10)
def main(input_file, rounds):
    state = next(input_file).strip()
    next(input_file)

    # Transform holds the rules for substituting one pair with two others.
    transform = {}
    for l in input_file:
        pair, insert = l.strip().split(" -> ")
        transform[pair] = pair[0] + insert, insert, insert + pair[1]

    # We start with the pairs and joins we have.
    # Joins are letters that are counted twice (once in each pair they belong to).
    pair_counts = Counter("".join(v) for v in zip(state, state[1:]))
    join_counts = Counter(state[1:-1])
    click.echo(f"Initially, counts are {pair_counts} and {join_counts}")

    for i in range(rounds):
        click.echo(f"Simulating round {i + 1}...")
        new_pair_counts = Counter()
        for k, v in list(pair_counts.items()):
            frequency = pair_counts[k]
            first, join, second = transform[k]

            new_pair_counts[first] += frequency
            new_pair_counts[second] += frequency
            join_counts[join] += frequency
        click.echo(f"After round {i + 1}, counts are {new_pair_counts} and {join_counts}")
        pair_counts = new_pair_counts

    counts = Counter()
    for (first, second), v in pair_counts.items():
        counts[first] += v
        counts[second] += v

    counts -= join_counts
    sorted_counts = counts.most_common()
    click.echo(str(sorted_counts))
    x, y = sorted_counts[0][1], sorted_counts[-1][1]
    click.secho(f"Answer found: {x - y}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
