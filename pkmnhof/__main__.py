import click
from PIL import Image, ImageShow

from pkmnhof import Pokedex, __version__


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-o", "--output", type=click.Path(dir_okay=False))
@click.option("-r", "--resize", type=click.FloatRange(1, 3), default=1)
@click.option("--no-frame", is_flag=True)
@click.version_option(version=__version__)
@click.argument("nums", type=int, nargs=6)
def main(output, resize, no_frame, nums):
    pokedex = Pokedex()

    pad = int(9 * resize)
    side = int(60 * resize)
    tmp = Image.new(mode="RGBA", size=(pad * 2 + side * 6, pad * 2 + side))
    for i, n in enumerate(nums):
        tmp.paste(
            Image.open(pokedex[n]).resize((side, side)), box=(pad + side * i, pad)
        )

    if no_frame:
        background = Image.new(
            mode="RGBA", size=(pad * 2 + side * 6, pad * 2 + side), color="#ffffff"
        )
    else:
        background = (
            Image.open(pokedex.frame)
            .convert("RGBA")
            .resize((pad * 2 + side * 6, pad * 2 + side))
        )

    final = Image.alpha_composite(background, tmp)

    if output is not None:
        final.save(output)
    else:
        ImageShow.register(ImageShow.EogViewer, 0)  # prefer `eog` over `display`
        ImageShow.show(final)


if __name__ == "__main__":
    main()
