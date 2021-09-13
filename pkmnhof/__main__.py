import argparse

from PIL import Image, ImageShow

from pkmnhof import Pokedex, __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs=6, type=int, metavar="N")
    parser.add_argument("-o", "--output")
    parser.add_argument("-r", "--resize", default=1, type=float)
    parser.add_argument("--no-frame", action="store_true")
    parser.add_argument(
        "--version", action="version", version=f"pkmnhof, version {__version__}"
    )
    args = parser.parse_args()

    if args.resize is not None and not (1 <= args.resize <= 3):
        raise ValueError

    pokedex = Pokedex()

    pad = int(9 * args.resize)
    side = int(60 * args.resize)
    tmp = Image.new(mode="RGBA", size=(pad * 2 + side * 6, pad * 2 + side))
    for i, n in enumerate(args.numbers):
        tmp.paste(
            Image.open(pokedex[n]).resize((side, side)), box=(pad + side * i, pad)
        )

    if args.no_frame:
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

    if args.output is not None:
        final.save(args.output)
    else:
        ImageShow.register(ImageShow.EogViewer, 0)  # prefer `eog` over `display`
        ImageShow.show(final)


if __name__ == "__main__":
    main()
