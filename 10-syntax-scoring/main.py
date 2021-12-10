import click


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    result = 0
    match = {
        ")": ("(", 3),
        "]": ("[", 57),
        "}": ("{", 1197),
        ">": ("<", 25137),
    }
    for l in input_file:
        ip = []
        for i, c in enumerate(l):
            if c in "([{<":
                ip.append(c)
            elif c in ")]}>":
                pair = ip.pop()
                need, points = match[c]
                if pair != need:
                    click.echo(f"Found illegal character {c} at position {i}")
                    result += points

    click.secho(f"Answer is {result}", fg="green")


if __name__ == "__main__":
    main()
