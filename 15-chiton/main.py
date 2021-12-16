import click

from dataclasses import dataclass, field

import sys
import typing

import heapq


def print_grid(vertices, M, N):
    lines = []
    for i in range(M):
        l = ""
        for j in range(N):
            d = vertices[i, j].distance
            l += f" {d}".rjust(4, " ") if d < sys.maxsize else "   *"
        lines.append(l)
    click.echo("\n".join(lines))


def neighbours(i, j, M, N):
    if i > 0:
        yield i-1, j
    if i < M - 1:
        yield i+1, j
    if j > 0:
        yield i, j-1
    if j < N - 1:
        yield i, j+1


def left(i):
    return 2*i + 1


def right(i):
    return 2*i + 2


def parent(i):
    return (i - 1) // 2


@dataclass(order=True)
class Vertex:
    distance: int
    position: typing.Tuple[int, int] = field(compare=False)

    # Extra: store the index of the item in the heap so we can manipulate it.
    index: int = field(compare=False)


def vertex_swap(pq, i, j):
    pq[i], pq[j] = pq[j], pq[i]
    pq[i].index = i
    pq[j].index = j


def vertex_sift_down(pq: typing.List[Vertex], heaplen, i):
    """Given heap pq of length heaplen, sift down from index i to maintain heap property."""
    current = i
    l, r = left(current), right(current)
    while l < heaplen:
        if r < heaplen:
            # Both children exist.
            if pq[r].distance < pq[l].distance:
                child = r
            else:
                child = l
        else:
            child = l

        if pq[child].distance >= pq[current].distance:
            # Invariant maintained; exit.
            break

        # Swap current and child nodes.
        # # click.echo(f"Swap down: {pq[l]} <--> {pq[current]}")
        vertex_swap(pq, current, child)

        # Iterate downwards.
        current = child
        l, r = left(current), right(current)


def vertex_sift_up(pq, i):
    current = i
    while current > 0:
        p = parent(current)

        if pq[current] >= pq[p]:
            break

        vertex_swap(pq, current, p)
        current = p


def vertex_pop(pq, heaplen):
    result = pq[0]

    pq[0] = pq[heaplen - 1]
    pq[0].index = 0

    pq[heaplen - 1] = None
    heaplen -= 1

    vertex_sift_down(pq, heaplen, 0)

    return result, heaplen


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("expand", type=click.BOOL, default=False)
def main(input_file, expand):
    risk = {}
    for i, l in enumerate(input_file):
        for j, val in enumerate(l.strip()):
            risk[(i, j)] = int(val)

    M = N = (i + 1)

    if expand:
        M = N = (i + 1) * 5
        # Expand the map...
        for i in range(M):
            for j in range(N):
                risk_increase = (i // 10) + (j // 10)
                original_risk = risk[i % 10, j % 10]
                risk[i, j] = (original_risk + risk_increase)
                if risk[i, j] > 9:
                    risk[i, j] -= 9

    DESTINATION = (M - 1, N - 1)
    click.confirm(f"Grid size: {M}x{N}; destination is {DESTINATION}")

    vertices = {(i, j): Vertex(sys.maxsize, (i, j), 0) for i in range(M) for j in range(N)}
    vertices[0, 0].distance = 0

    pq = list(vertices.values())
    heapq.heapify(pq)
    assert vertices[0, 0] == pq[0]
    for i, n in enumerate(pq):
        n.index = i

    heaplen = len(pq)
    unseen = {(i, j) for i in range(M) for j in range(N)}

    click.confirm(f"Heap size: {heaplen}; Unseen size: {len(unseen)}")
    # click.echo(f"Starting with {len(unseen)} unseen vertices...")

    i = 0
    while unseen:
        # Diagnostics
        print_grid(vertices, M, N)
        click.echo(f"Visiting {pq[0].position} at distance={pq[0].distance}")
        click.confirm("")

        i += 1
        n, heaplen = vertex_pop(pq, heaplen)
        # click.echo(f"Removed element {n.position} (distance: {n.distance}) from the queue; heaplen={heaplen}")
        # click.echo(f"New min is: {pq[0]}")

        unseen.remove(n.position)

        if not i % 100:
            # click.echo(f"Visiting {n.position} at distance={n.distance}")
            # click.echo(str(pq[:5]))
            # click.echo(str(pq[heaplen-5:heaplen]))
            click.confirm(f"Round {i}")
        if n.position == DESTINATION:
            click.echo(f"Reached destination with {len(unseen)} unseen elements; exiting!")
            break

        for x, y in neighbours(*n.position, M, N):
            if (x, y) not in unseen:
                continue

            # click.echo(f"{x, y} is an unseen neighbor of {n.position}")
            candidate = vertices[x, y]
            alt = n.distance + risk[x, y]
            if alt < candidate.distance:
                click.echo(f"{candidate.position} has a shorter path thro' {n.position}")
                candidate.distance = alt
                vertex_sift_up(pq, candidate.index)

    click.secho(f"Answer found: {vertices[DESTINATION].distance}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
