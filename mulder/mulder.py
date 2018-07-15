#!/usr/bin/env python
# -*- coding:utf-8 -*-

from itertools import chain
from random import shuffle


def mulder(script):
    m = list(
        chain.from_iterable(
            (
                x[:(len(x)+1)//2],
                x[(len(x)+1)//2:]
            ) for x in script.split()
        )
    )
    real = m[:]
    while 1:
        shuffle(m)
        yield ''.join(m[:2]+["、"]+m[2:])
        if m == real:
            return


def main():
    script = "モルダー あなた 疲れてる のよ"
    for i, m in enumerate(mulder(script)):
        print(i, m)


if __name__ == "__main__":
    main()
