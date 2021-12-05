from dataclasses import dataclass
from collections import defaultdict

import click


@dataclass
class Interval:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def points(self):
        for i in range(self.x1, self.x2 + 1):
            for j in range(self.y1, self.y2 + 1):
                yield i, j


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    ints = []
    for l in input_file:
        l = l.strip()
        start, end = l.split("->")
        x1, y1 = [int(i) for i in start.strip().split(",")]
        x2, y2 = [int(i) for i in end.strip().split(",")]
        if x1 == x2:
            if y2 < y1:
                y1, y2 = y2, y1
        elif y1 == y2:
            if x2 < x1:
                x1, x2 = x2, x1
        else:
            # Diagonal line; skip
            continue

        i = Interval(x1, y1, x2, y2)
        ints.append(i)
        click.echo(f"{str(i)} --> {list(i.points)}")

    click.echo("Starting overlaps...")

    graph = defaultdict(lambda: defaultdict(int))
    result = 0
    seen = set()
    for it in ints:
        for x, y in it.points:
            graph[x][y] += 1
            if graph[x][y] > 1 and (x, y) not in seen:
                result += 1
                seen.add((x, y))

    click.secho(str(result), fg="green")


if __name__ == "__main__":
    main()
