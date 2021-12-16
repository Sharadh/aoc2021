import click


HEX_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def convert_to_bits(s):
    """Convert a Hexadecimal string to a BITS bit string"""
    for c in s:
        yield HEX_MAP[c]


def decode(s):
    return s


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    for l in input_file:
        click.echo(f"{l.strip()} --> {''.join(convert_to_bits(l.strip()))}")

    result = None

    click.secho(f"Answer found: {result}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
