import click


class StringTrie:

    def __init__(self, value="", parent=None):
        self.value = value
        self.parent = parent
        self.children = {}
        self.count = 0

    def add(self, s):
        self.count += 1

        # Add subtrie as a child
        c = s[0]
        if c not in self.children:
            self.children[c] = StringTrie(c, self)

        # Termination case.
        if len(s) == 1:
            return

        self.children[c].add(s[1:])

    def add_many(self, *ss):
        for s in ss:
            self.add(s)

    def __repr__(self):
        return f'{self.__class__.__name__}<"{self.path}" x {self.count}>'

    def __getitem__(self, item):
        return self.children[item]

    @property
    def path(self):
        result = ""
        current = self
        while current.parent:
            result = current.value + result
            current = current.parent
        return result


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    t = StringTrie()
    for l in input_file:
        t.add(l)

    current = t
    while current.count > 1:
        click.echo(current)
        click.echo(current.children)
        if current['0'].count > current['1'].count:
            current = current['0']
        else:
            current = current['1']
        # click.prompt("")
    ogen = int(str(current.path), 2)
    click.echo(f"{current.path} --> {ogen}")

    current = t
    while current.count > 1:
        click.echo(current)
        click.echo(current.children)
        if current['0'].count > current['1'].count:
            current = current['1']
        else:
            current = current['0']
        # click.prompt("")
    co2 = int(str(current.path), 2)
    click.echo(f"{current.path} --> {co2}")

    click.secho(f"ogen: {ogen}, co2: {co2}", fg="green")
    click.secho(f"{ogen * co2}", fg="green")


if __name__ == "__main__":
    main()
