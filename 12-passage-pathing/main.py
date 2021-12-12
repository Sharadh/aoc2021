import click

from collections import defaultdict


def paths_without_small_repeat(graph):
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

    return paths


def paths_with_single_small_repeat(graph, repeat):
    candidates = [('start', [], [], repeat)]
    paths = []
    while candidates:
        node, to_path, lower_seen, can_repeat = candidates.pop()
        if node == 'end':
            click.secho(f"Path found: {','.join(to_path + [node])}", fg="yellow")
            paths.append(to_path + [node])
            continue

        this_seen = lower_seen + [node] if node.islower() else lower_seen
        this_path = to_path + [node]
        for n in graph[node]:
            if n.isupper() or n not in this_seen:
                candidates.append((n, this_path, this_seen, can_repeat))
            elif can_repeat and n == can_repeat:
                candidates.append((n, this_path, this_seen, None))

        click.echo("\n".join([",".join(c[1] + [c[0]]) for c in candidates]))
        # click.confirm("?")

    return paths


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

    paths = paths_without_small_repeat(graph)
    click.echo("\n".join([",".join(p) for p in paths]))
    click.secho(f"Answer found: {len(paths)}! Exiting.", fg="green")

    # TODO:
    #   instead of looping entire logic for each small cave, modify inner
    #   algo so we greedily use up the small cave allowance if we need to.
    small_caves = [n for n in graph if n.islower() and n not in ["start", "end"]]
    paths = set()
    for c in small_caves:
        new_paths = [",".join(p) for p in paths_with_single_small_repeat(graph, c)]
        click.echo(f"With allowing repeat of {c}: ")
        click.echo("\n".join(new_paths))
        paths.update(new_paths)
    click.secho(f"Answer found: {len(paths)}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
