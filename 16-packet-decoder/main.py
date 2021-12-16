import typing
from dataclasses import dataclass
from io import StringIO

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
    val, i = s.getvalue(), s.tell()
    click.echo(f"Parsing {val[i:]}:")

    version = int(s.read(3), 2)
    pid = int(s.read(3), 2)
    root = Packet(version, pid, [])

    # Parse literal values.
    if root.pid == 4:
        click.echo(f" * is a literal value.")
        number = []
        while True:
            signal, *block = s.read(5)
            number.extend(block)
            if signal == "0":
                break
        click.echo(f" * is the number {int(''.join(number), 2)}")
        # while True:
        #     if s.read(1) != "0":
        #         break
    else:
        # Parse operators.
        click.echo(f" * is an operator.")
        length_type = s.read(1)
        if length_type == "0":
            sub_length = int(s.read(15), 2)
            click.echo(f" * defines subpacket length of {sub_length}")
            sub_stream = StringIO(s.read(sub_length))
            while sub_stream.tell() < sub_length:
                root.subpackets.append(decode(sub_stream))
        elif length_type == "1":
            subpackets_count = int(s.read(11), 2)
            click.echo(f" * defines subpacket count of {subpackets_count}")
            for i in range(subpackets_count):
                root.subpackets.append(decode(s))

    j = s.tell()
    click.confirm(f" * Parsed {root} from {val[i:j]}")
    return root


@dataclass
class Packet:
    version: int
    pid: int

    subpackets: typing.List["Packet"]


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    bstrings = []
    for l in input_file:
        bstrings.append(''.join(convert_to_bits(l.strip())))

    for s in bstrings:
        root = decode(StringIO(s))
        click.echo(str(root))
        click.confirm("Next line?")

    result = None
    click.secho(f"Answer found: {result}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
