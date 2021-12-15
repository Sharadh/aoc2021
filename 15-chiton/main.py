import click

from dataclasses import dataclass, field

import sys
import typing

import heapq


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


def vertex_sift_down(pq, heaplen, i):
    """Given heap pq of length l, sift down from index i to maintain heap property."""
    current = i
    l, r = left(current), right(current)
    while l < heaplen:
        if r < heaplen:
            # Both children exist.
            if pq[r].distance < pq[l].distance:
                child = r
            else:
                child = l
        elif pq[l].distance < pq[current].distance:
            child = l
        else:
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


def vertex_insert(pq, heaplen, val):
    val.index = heaplen
    pq[heaplen], heaplen = val, heaplen + 1
    vertex_sift_up(pq, heaplen - 1)


def vertex_pop(pq, heaplen):
    result = pq[0]

    pq[0] = pq[heaplen - 1]
    pq[0].index = 0
    heaplen -= 1

    vertex_sift_down(pq, heaplen, 0)

    return result, heaplen


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    risk = {}
    for i, l in enumerate(input_file):
        for j, val in enumerate(l.strip()):
            risk[(i, j)] = int(val)

    M = N = (i + 1) * 5
    DESTINATION = (M - 1, N - 1)

    # Expand the map...
    for i in range(M):
        for j in range(N):
            risk_increase = (i // 10) + (j // 10)
            original_risk = risk[i % 10, j % 10]
            risk[i, j] = (original_risk + risk_increase)
            if risk[i, j] > 9:
                risk[i, j] -= 9

    vertices = {(i, j): Vertex(sys.maxsize, (i, j), 0) for i in range(M) for j in range(N)}
    vertices[0, 0].distance = 0

    pq = list(vertices.values())
    heapq.heapify(pq)
    assert vertices[0, 0] == pq[0]
    for i, n in enumerate(pq):
        n.index = i

    heaplen = len(pq)
    unseen = {(i, j) for i in range(M) for j in range(N)}
    # click.echo(f"Starting with {len(unseen)} unseen vertices...")

    while unseen:
        n, heaplen = vertex_pop(pq, heaplen)
        # click.echo(f"Removed element {n.position} (distance: {n.distance}) from the queue; heaplen={heaplen}")
        # click.echo(f"New min is: {pq[0]}")

        unseen.remove(n.position)
        if n == DESTINATION:
            break

        for x, y in neighbours(*n.position, M, N):
            if (x, y) not in unseen:
                continue

            # click.echo(f"{x, y} is an unseen neighbor of {n.position}")
            candidate = vertices[x, y]
            alt = n.distance + risk[x, y]
            if alt < candidate.distance:
                # click.echo(f"{candidate.position} has a shorter path thro' {n.position}")
                candidate.distance = alt
                vertex_sift_up(pq, candidate.index)

    click.secho(f"Answer found: {vertices[M-1, N-1].distance}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
