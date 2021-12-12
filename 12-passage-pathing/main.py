import click

from collections import defaultdict


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    graph = defaultdict(list)
    for l in input_file:
        x, y = l.strip().split("-")
        if x.isupper() and y.isupper():
            raise ValueError("can't handle two big caves directly connected!")

        graph[x].append(y)
        graph[y].append(x)

    candidates = [('start', [], [])]
    paths = []
    while candidates:
        node, to_path, lower_seen = candidates.pop()
        if node == 'end':
            click.secho(f"Path found: {','.join(to_path + [node])}", fg="yellow")
            paths.append(to_path + [node])
            continue

        this_seen = lower_seen + [node] if node.islower() else lower_seen
        this_path = to_path + [node]
        for n in graph[node]:
            if n.isupper() or n not in this_seen:
                candidates.append((n, this_path, this_seen))

        click.echo("\n".join([",".join(c[1] + [c[0]]) for c in candidates]))
        # click.confirm("?")

    click.echo("\n".join([",".join(p) for p in paths]))
    click.secho(f"Answer found: {len(paths)}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
