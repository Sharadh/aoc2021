import click


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    result = 0
    match = {
        ")": ("(", 1),
        "]": ("[", 2),
        "}": ("{", 3),
        ">": ("<", 4),
    }
    reverse_match = {v[0]: (k, v[1]) for k, v in match.items()}
    scores = []
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
                    break
        else:
            # Line is valid, but incomplete?
            if not ip:
                raise ValueError(f"Nothing incomplete in line: {l}")

            score = 0
            completion = ""
            while ip:
                c = ip.pop()
                need, points = reverse_match[c]
                score = score * 5 + points
                completion += need

            click.echo(f"Completed with string {completion} (score={score})")
            scores.append(score)

    scores.sort()
    middle = len(scores) // 2
    click.echo("")
    click.echo(f"Got {len(scores)} autocompletes; getting middle one at {middle}")
    click.secho(f"Answer is {scores[middle]}", fg="green")


if __name__ == "__main__":
    main()
