import typing
from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from io import StringIO

import click


EXPLODE_TEST_CASES = {
    "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
    "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
}

SPLIT_TEST_CASES = {
    "[[[[0,7],4],[15,[0,13]]],[1,1]]": "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
    "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]": "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
}


# Do not add tuple eq since we need id matching
# Tuple eq causes infinite recursion when comparing current to current.parent
@dataclass(eq=False)
class Pair:
    value: typing.Optional[int] = None
    children: typing.List["Pair"] = field(default_factory=list)
    parent: typing.Optional["Pair"] = None

    @property
    def is_number(self):
        return self.value is not None

    def __str__(self):
        if self.is_number:
            return str(self.value)

        return "[" + ",".join(str(c) for c in self.children) + "]"

    def __repr__(self):
        return str(self)

    def left(self):
        current = self
        # Go up as long as we are the left child.
        while current.parent and current == current.parent.children[0]:
            current = current.parent

        if not current.parent:
            # Reached the root; no left sibling.
            return None

        # Move one step left, then keep moving right.
        current = current.parent.children[0]
        while not current.is_number:
            current = current.children[1]
        return current

    def right(self):
        current = self
        # Go up as long as we are the right child.
        while current.parent and current == current.parent.children[1]:
            current = current.parent

        if not current.parent:
            # Reached the root; no right sibling.
            return None

        # Move one step right, then keep moving left.
        current = current.parent.children[1]
        while not current.is_number:
            current = current.children[0]
        return current

    def explode_step(self, level):
        if level == 4 and not self.is_number:
            # Explode!
            left = self.left()
            if left:
                left.value += self.children[0].value

            right = self.right()
            if right:
                right.value += self.children[1].value

            self.children = []
            self.value = 0
            return True

        # Depth First Search: Check our children.
        return any(c.explode_step(level + 1) for c in self.children)

    def split_step(self, level):
        if self.is_number and self.value > 9:
            a = self.value // 2
            b = self.value - a
            self.value = None
            self.children = [Pair(a, parent=self), Pair(b, parent=self)]
            return True

        # Depth First Search: Check our children.
        return any(c.split_step(level + 1) for c in self.children)

    def magnitude(self):
        if self.is_number:
            return self.value

        left, right = self.children
        return 3 * left.magnitude() + 2 * right.magnitude()


def encode_pair_tree(p: typing.Optional[Pair], indent: int):
    if p.is_number:
        return f"--{p.value}"

    children = [
        " " * indent + encode_pair_tree(c, indent + 2)
        for c in p.children
    ]
    children = [" " * indent + "|"] + children
    return "\n".join(children)


def parse_line(l: str):
    # Parse the string character at a time.
    s = StringIO(l)

    # Create the root.
    current = result = Pair()
    assert s.read(1) == "["

    # Iterate until the EOF.
    c = s.read(1)
    while c:
        # If this is a number, read until the "," or "]".
        num = ""
        while c.isnumeric():
            num += c
            c = s.read(1)
        if num:
            current.children.append(Pair(value=int(num), parent=current))
        if not c:
            continue

        # We've read the character after the number ended.
        if c == ",":
            # Move on.
            pass
        elif c == "[":
            # Start parsing a child.
            child = Pair(parent=current)
            current.children.append(child)
            current = child
        elif c == "]":
            # Finish parsing a node.
            current = current.parent

        # Read the next character.
        c = s.read(1)

    return result


def add_pairs(a: Pair, b: Pair):
    click.echo(f"\n  {a}\n+ {b}")
    c = Pair()
    a.parent = c
    b.parent = c
    c.children = [a, b]
    # click.echo(f"-> {c}")
    reduce_pair(c)
    click.echo(f"=> {c} ({c.magnitude()})")
    return c


def reduce_pair(p: Pair):
    while p.explode_step(0) or p.split_step(0):
        # click.echo(f"-> {p}")
        pass


class Parts:
    PART_ONE = "part-one"
    PART_TWO = "part-two"


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("part", type=click.Choice([Parts.PART_ONE, Parts.PART_TWO]))
def main(input_file, part):
    examples = []
    numbers = []
    for l in input_file:
        if not l.strip():
            examples.append(numbers)
            numbers = []
        else:
            p = parse_line(l.strip())
            # click.confirm(f"Parsed out:\n{p}")
            numbers.append(p)

    # for ip, expected in EXPLODE_TEST_CASES.items():
    #     x = parse_line(ip)
    #     x.reduce_step(0)
    #     passed = str(x) == expected
    #     click.echo(f"   {ip}\n-> {x}: {passed}")

    # for ip, expected in SPLIT_TEST_CASES.items():
    #     x = parse_line(ip)
    #     x.reduce_step(0)
    #     passed = str(x) == expected
    #     click.echo(f"   {ip}\n-> {x}: {passed}")

    if part == Parts.PART_ONE:
        click.echo("Part one!")
        for eg in examples:
            result = reduce(add_pairs, eg)
            click.secho(f"Answer found! {result} --> {result.magnitude()}", fg="green")
            click.confirm("")
        return

    if part == Parts.PART_TWO:
        click.echo("Part two!")
        for eg in examples:
            all_pairs = [
                (deepcopy(eg[i]), deepcopy(eg[j]))
                for i in range(len(eg))
                for j in range(len(eg))
                if i != j
            ]
            click.echo(f"Found {len(all_pairs)} candidates; evaluating...")
            click.confirm("")
            largest = 0
            for a, b in all_pairs:
                c = add_pairs(a, b)
                if c.magnitude() > largest:
                    largest = c.magnitude()
            click.secho(f"Answer found! {largest}", fg="green")
        return


if __name__ == "__main__":
    main()
