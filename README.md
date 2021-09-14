# pkmnhof

![project banner](assets/banner.png)

pkmnhof is a _Pokémon Hall of Fame_ image generator for Gen 1.

## Usage

```console
$ pkmnhof -h
Usage: pkmnhof [OPTIONS] NUMS...

Options:
  -o, --output FILE
  -r, --resize FLOAT RANGE  [1<=x<=3]
  --no-frame
  --version                 Show the version and exit.
  -h, --help                Show this message and exit.
```

For example, running `pkmnhof --no-frame 18 65 112 103 130 6` will display the following image:

![example image](assets/example.png)

## Disclaimer

© 1995–2021 Nintendo/Creatures Inc./GAME FREAK inc. Pokémon
are trademarks of Nintendo.
