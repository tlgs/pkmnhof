import argparse
import base64
import io

from PIL import Image

from dump import pokedex


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs=6, type=int, metavar="N")
    parser.add_argument("-r", "--resize", type=float)
    args = parser.parse_args()

    if not all(0 < x < 152 for x in args.numbers):
        raise ValueError

    if args.resize is not None and (args.resize < 1 or args.resize > 8):
        raise ValueError

    images = [
        Image.open(io.BytesIO(base64.b64decode(pokedex[n - 1]))) for n in args.numbers
    ]

    side = 60 if args.resize is None else int(60 * args.resize)

    if args.resize is not None:
        for j, im in enumerate(images):
            images[j] = im.resize(size=(side, side))

    tmp = Image.new(mode="RGBA", size=(side * 3, side * 2))
    tmp.paste(images[0], (0, 0))
    tmp.paste(images[1], (side, 0))
    tmp.paste(images[2], (side * 2, 0))
    tmp.paste(images[3], (0, side))
    tmp.paste(images[4], (side, side))
    tmp.paste(images[5], (side * 2, side))

    final = Image.new(mode="RGBA", size=(side * 3, side * 2), color="#fbfbf9")
    final.alpha_composite(tmp)
    final.show()
