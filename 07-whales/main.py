from dataclasses import dataclass
from collections import defaultdict

import click


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    positions = sorted([int(x) for x in input_file.read().strip().split(",")])
    click.secho(f"{positions[0]} --> {positions[-1]}", fg="green")
    click.confirm("")

    fuel, result = 0, positions[0]
    for y in positions:
        distance = abs(positions[0] - y)
        fuel += distance * (distance + 1) // 2

    for x in range(positions[1], positions[-1] + 1):
        sum_ = 0
        for y in positions:
            distance = abs(x - y)
            sum_ += distance * (distance + 1) // 2

        if sum_ < fuel:
            click.echo(f"Position {x} requires less fuel: {sum_} is less than {fuel}")
            fuel = sum_
            result = x

    click.secho(f"Position {result} requires {fuel} fuel", fg="green")


if __name__ == "__main__":
    main()
