from dataclasses import dataclass
from collections import defaultdict, Counter

import click


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    result = 0
    for l in input_file:
        ip, op = l.strip().split("|")
        ip = [set(x) for x in ip.strip().split()]
        op = [set(x) for x in op.strip().split()]
        
        # Map of numbers to set of characters in them.
        numbers = {}
        
        # Map of panels to signals in this input that control them. 
        panels = {}
        
        # Count of times signals appear in this input.
        counts = Counter()

        # Note: this is the major part of solution to part one.
        for i in ip:
            counts.update(i)
            l = len(i)
            if l == 2:
                numbers[1] = i
            elif l == 3:
                numbers[7] = i
            elif l == 4:
                numbers[4] = i
            elif l == 7:
                numbers[8] = i

        # A appears in 7 but not 1.
        panels['A'] = (numbers[7] - numbers[1]).pop()

        # BC are in 1; B appears 8 times across all numbers and C appears 9 times.
        for p in numbers[1]:
            if counts[p] == 8:
                panels['B'] = p
            elif counts[p] == 9:
                panels['C'] = p
            else:
                raise RuntimeError("Uh-oh!")
        # click.echo(str(panels))
        # click.confirm("?")

        # FG are in 4 but not 1; F appears 6 times and G appears 7 times.
        for p in (numbers[4] - numbers[1]):
            if counts[p] == 6:
                panels['F'] = p
            elif counts[p] == 7:
                panels['G'] = p
            else:
                raise RuntimeError("Uh-oh!")
        # click.echo(str(panels))
        # click.confirm("?")

        # ED are remaining; E appears 4 times and D appears 7 times.
        for p in (numbers[8] - set(panels.values())):
            if counts[p] == 4:
                panels['E'] = p
            elif counts[p] == 7:
                panels['D'] = p
            else:
                raise RuntimeError("Uh-oh!")

        click.echo(f"Complete signal->panel mapping: {panels}")

        for n, p in {
            2: "ABDEG",
            3: "ABCDG",
            5: "ACDFG",
            6: "ACDEFG",
            9: "ABCDFG",
            0: "ABCDEF",
        }.items():
            numbers[n] = set(panels[x] for x in p)
        click.echo(f"Complete number->input mapping: {numbers}")
        click.echo(f"Found following numbers: {sorted(numbers.keys())}")

        # Create the mapping of output to digits
        answer = ""
        click.echo(f"{op}")
        for o in op:
            for d, i in numbers.items():
                if i == o:
                    answer += str(d)
                    break
            else:
                raise RuntimeError("Uh-oh!")

        click.echo(str(panels))
        # click.confirm(answer)

        result += int(answer)

    click.secho(f"Answer is {result}", fg="green")


if __name__ == "__main__":
    main()
