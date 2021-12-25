from math import ceil, floor

import click
import re

import sys


@click.command()
@click.argument("input_file", type=click.File())
def main(input_file):
    ip = next(input_file).strip()

    m = re.match(r'target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)', ip)
    if not m:
        raise ValueError("Uh-oh - regex is hard!")
    click.echo(str(m.groups()))
    x_min, x_max, y_min, y_max = [int(x) for x in m.groups()]
    click.confirm(f"Target area: x=[{x_min},{x_max}], y=[{y_min},{y_max}]")

    # The maximum x velocity is the right-most edge of the target area, reached in 1 step
    # The minimum x velocity reaches x_min, left-most edge, when it stop moving horizontally.
    # x + (x - 1) + ... 1 >= x_min => (x)(x + 1)/2 = x_min => start searching from ceil(root(2 * x_min)) down
    vx_min = ceil(pow(2 * x_min, 0.5))
    dx = (vx_min * (vx_min + 1)) // 2
    while dx >= x_min:
        vx_min -= 1
        dx = (vx_min * (vx_min + 1)) // 2
    vx_min += 1
    vx_max = x_max + 1
    click.confirm(f"Valid range for vx: [{vx_min}, {vx_max})")

    # Since sometimes infinite steps solves for x, find max steps for y (from part one).
    n_max_y = get_max_steps_y(y_min)
    click.confirm(f"Max value for n: {n_max_y}")

    result = set()
    # For every valid value of x...
    for vx in range(vx_min, vx_max):
        # ...find the value(s) of N that put it in the target range...
        n_min, n_max = get_step_range(vx, x_min, x_max)
        n_max = min(n_max, n_max_y)
        click.echo(f"Valid range for n for vx={vx}: [{n_min}, {n_max})")
        for n in range(n_min, n_max):
            # ...and then find any valid values of y that match.
            for vy in range(y_min, -y_min + 1):
                dy = get_dy(vy, n)
                if y_min <= dy <= y_max:
                    click.echo(f"Found match: {vx},{vy}; n={n}")
                    result.add((vx, vy))

            # vy_min, vy_max = get_vy_range(n, y_min, y_max)
            # click.confirm(f"Valid range for vy for vx={vx},n={n}: [{vy_min}, {vy_max})")
            # for y in range(vy_min, vy_max + 1):

    click.secho(f"Answer found: {len(result)}! Exiting.", fg="green")


def get_max_steps_y(y_min):
    # The max steps is clamped at the number for when y = y_min
    # Go up: y, y - 1, ...., 0 = y + 1 steps
    # Go down: -1, -2, -3, ..., -y = y steps
    # Total: 2 * -y_min + 1
    return 2 * abs(y_min) + 1


def get_step_range(vx, x_min, x_max):
    dx = 0
    n_start = n_finish = None
    for i, vx_step in enumerate(range(vx, 0, -1)):
        dx += vx_step
        if (x_min <= dx <= x_max) and not n_start:
            # Entered the target area.
            n_start = i + 1
        elif dx > x_max:
            # Exited the target area; the previous step was the last.
            n_finish = i + 1
            break
    else:
        # We reached 0 velocity and never exit the target area.
        n_finish = sys.maxsize

    if not n_start:
        return 0, 0
    return n_start, n_finish


def dy(y, n):
    return y * n - (n * (n - 1)) // 2


def get_vy_range(n, y_min, y_max):
    y_start = y_min // n
    while True:
        if y_min <= dy(y_start, n):
            break
        y_start += 1

    y_end = (y_max + n // n) + (n + 1) // 2
    while True:
        if y_min <= dy(y_end, n):
            break
        y_end -= 1

    if y_start > y_end:
        return 0, 0
    return y_start, y_end + 1


def get_dy(vy, n):
    if vy <= 0 or vy >= n:
        return n * vy - (n * (n - 1)) // 2

    # We go up, then come down.
    return (vy * (vy + 1)) // 2 + get_dy(0, n - vy)


if __name__ == "__main__":
    main()
