import click

from dataclasses import dataclass, field

import sys
import typing

import heapq


def print_grid(distances, M, N):
    lines = []
    for i in range(M):
        l = ""
        for j in range(N):
            d = distances.get((i, j), "*")
            l += f" {d}".rjust(4, " ")
        lines.append(l)
    click.echo("\n".join(lines))
    click.echo("")


def neighbours(i, j, M, N):
    if i > 0:
        yield i-1, j
    if i < M - 1:
        yield i+1, j
    if j > 0:
        yield i, j-1
    if j < N - 1:
        yield i, j+1


@dataclass(order=True)
class Vertex:
    distance: int
    position: typing.Tuple[int, int] = field(compare=False)

    def __str__(self):
        return f"{self.position}@d={self.distance}"

    def __repr__(self):
        return str(self)


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("expand", type=click.BOOL, default=False)
@click.argument("debug", type=click.BOOL, default=False)
def main(input_file, expand, debug):
    risk = {}
    for i, l in enumerate(input_file):
        for j, val in enumerate(l.strip()):
            risk[(i, j)] = int(val)

    M = N = (i + 1)

    if expand:
        m, n = M, N
        M = N = (i + 1) * 5
        # Expand the map...
        for i in range(M):
            for j in range(N):
                risk_increase = (i // m) + (j // m)
                original_risk = risk[i % m, j % n]
                risk[i, j] = (original_risk + risk_increase)
                if risk[i, j] > 9:
                    risk[i, j] -= 9

    DESTINATION = (M - 1, N - 1)
    click.confirm(f"Grid size: {M}x{N}; destination is {DESTINATION}")

    seen = {(0, 0): 0}
    pq = [Vertex(0, (0, 0))]
    while pq:
        if debug:
            # Diagnostics
            print_grid(seen, M, N)
            click.echo(f"Up next: {pq}")
            click.confirm("")

        n = heapq.heappop(pq)
        if n.position == DESTINATION:
            click.echo(f"Reached destination with {len(seen)} elements visited; exiting!")
            break

        for position in neighbours(*n.position, M, N):
            if position in seen:
                # If we've seen an element, we'll never better its distance.
                continue

            # If we've not seen an element, add it through us since we're the
            # shortest path adjacent to it.
            add = Vertex(n.distance + risk[position], position)
            seen[add.position] = add.distance
            heapq.heappush(pq, add)

    click.secho(f"Answer found: {seen[DESTINATION]}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
