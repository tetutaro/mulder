#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from itertools import chain
from random import shuffle


def mulder(script: str, max_mulder: int = 50):
    m: list[str] = list(
        chain.from_iterable(
            (x[: (len(x) + 1) // 2], x[(len(x) + 1) // 2 :])
            for x in script.split()
        )
    )
    real = m[:]
    while 1:
        shuffle(m)
        yield "".join(m[:2] + ["、"] + m[2:])
        if m == real:
            return


def main():
    parser: ArgumentParser = ArgumentParser(
        description="モルダーが疲れるか最大モルダー数に至るまでモルダーする",
    )
    parser.add_argument(
        "-m",
        "--max-mudler",
        type=int,
        default=50,
        help="最大モルダー数（default: 50）",
    )
    args: Namespace = parser.parse_args()
    max_mulder: int = args.max_mudler
    digits: int = len(str(max_mulder))
    if max_mulder < 1:
        max_mulder = -1
        digits = 5
    script: str = "モルダー あなた 疲れてる のよ"
    for i, m in enumerate(mulder(script)):
        print(f"{i + 1:0{digits}d}: {m}")
        if max_mulder > 0 and i + 1 >= max_mulder:
            break


if __name__ == "__main__":
    main()
