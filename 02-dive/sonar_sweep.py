import click


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("window_size", type=click.INT, default=1)
def main(input_file, window_size):
    click.echo(f"Working with window size of {window_size}")
    # Set up our window, and calculate initial window size.
    # We don't handle the case where number of inputs <= window_size.
    window = [int(next(input_file)) for _ in range(window_size)]
    current = sum(window)
    result = 0
    for i, l in enumerate(input_file):
        l = int(l)
        click.echo(f"{current}: {window} -> {l}")

        first, window = window[0], window[1:]
        window.append(l)

        prev = current
        current = prev - first + l
        # click.prompt("next?")
        if current > prev:
            result += 1

    click.secho(result, fg="green")


if __name__ == "__main__":
    main()
