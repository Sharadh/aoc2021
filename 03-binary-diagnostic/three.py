import click
from collections import defaultdict, Counter


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    lines = [l.strip() for l in input_file]

    candidates = lines
    i = 0
    while len(candidates) > 1:
        counts = [Counter(i) for i in zip(*candidates)]
        need = '0' if counts[i]['0'] > counts[i]['1'] else '1'
        candidates = [l for l in candidates if l[i] == need]
        i += 1
        # click.secho(f"{candidates}", fg="green")
        # click.prompt("")
    ogen = int(candidates[0], 2)

    candidates = lines
    i = 0
    while len(candidates) > 1:
        counts = [Counter(i) for i in zip(*candidates)]
        need = '1' if counts[i]['0'] > counts[i]['1'] else '0'
        candidates = [l for l in candidates if l[i] == need]
        i += 1
        # click.secho(f"{candidates}", fg="green")
        # click.prompt("")
    co2 = int(candidates[0], 2)

    click.secho(f"ogen: {ogen}, co2: {co2}", fg="green")
    click.secho(f"{ogen * co2}", fg="green")


if __name__ == "__main__":
    main()
