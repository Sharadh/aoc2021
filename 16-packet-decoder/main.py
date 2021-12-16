import typing
from dataclasses import dataclass
from functools import reduce
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
    root = Packet(version, pid, None, [])

    # Parse literal values.
    if root.pid == 4:
        click.echo(f" * is a literal value.")
        number = []
        while True:
            signal, *block = s.read(5)
            number.extend(block)
            if signal == "0":
                break
        root._value = int(''.join(number), 2)
        click.echo(f" * is the number {root._value}")
        # while True:
        #     if s.read(1) != "0":
        #         break
    else:
        # Parse operators.
        click.echo(f" * is an operator ({root.pid}).")
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
    click.echo(f" * Parsed {root} from {val[i:j]}")
    return root


@dataclass
class Packet:
    version: int
    pid: int

    _value: typing.Optional[int]
    subpackets: typing.List["Packet"]

    def __str__(self):
        return f"v={self.version} ({','.join(str(sub) for sub in self.subpackets)})"

    def version_sum(self):
        return self.version + sum(sub.version_sum() for sub in self.subpackets)

    def value(self):
        if self.pid == 0:
            return sum(sub.value() for sub in self.subpackets)
        if self.pid == 1:
            return reduce(lambda x, y: x * y.value(), self.subpackets, 1)
        if self.pid == 2:
            return min(sub.value() for sub in self.subpackets)
        if self.pid == 3:
            return max(sub.value() for sub in self.subpackets)

        if self.pid == 4:
            return self._value

        a, b = self.subpackets
        if self.pid == 5:
            conditional = a.value() > b.value()
        elif self.pid == 6:
            conditional = a.value() < b.value()
        elif self.pid == 7:
            conditional = a.value() == b.value()
        return int(conditional)


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    bstrings = []
    for l in input_file:
        bstrings.append(''.join(convert_to_bits(l.strip())))

    for s in bstrings:
        root = decode(StringIO(s))
        click.secho(f"{root} has total version sum {root.version_sum()} and value {root.value()}", fg="yellow")
        click.confirm("Next line?")

    result = None
    click.secho(f"Answer found: {result}! Exiting.", fg="green")


if __name__ == "__main__":
    main()
