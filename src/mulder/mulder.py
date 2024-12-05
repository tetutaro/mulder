#!/usr/bin/env python3
import os
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
    RawTextHelpFormatter,
)
from itertools import chain, zip_longest
from random import randint, seed, shuffle

from fugashi import Tagger
from pydantic import BaseModel
from unidic_lite import DICDIR


class Node(BaseModel):
    surface: str  # 表層形
    pos1: str  # 品詞大分類
    pos2: str  # 品詞中分類
    pos3: str  # 品詞小分類
    pos4: str  # 品詞細分類
    ctype: str  # 活用型
    cform: str  # 活用形
    base: str  # 書字形基本形


def script2words(script: str) -> tuple[list[str], list[tuple[int, str]]]:
    mecabrc: str = os.path.dirname(__file__) + "/mecabrc"
    tagger: Tagger = Tagger(f"-d {DICDIR} -r {mecabrc}")
    nodes: list[Node] = [
        Node(**eval(x)) for x in tagger.parse(script).splitlines()
    ]
    words: list[str] = []
    marks: list[tuple[int, str]] = []
    prefix: str = ""
    for node in nodes:
        if node.pos1 in ["名詞", "代名詞"]:
            if prefix != "":
                words.append(prefix)
            prefix = ""
            words.append(node.surface)
        elif node.pos1 in ["記号", "補助記号"]:
            if prefix != "":
                words.append(prefix)
            prefix = ""
            marks.append((len(words) * 2, node.surface))
        elif node.surface != node.base:
            prefix += node.surface
        else:
            if len(prefix + node.surface) > 1:
                words.append(prefix + node.surface)
                prefix = ""
            else:
                prefix += node.surface
    return words, marks


def mulder(
    script: str,
    max_mulder: int,
    random_seed: int | None = None,
) -> None:
    if random_seed is not None:
        seed(random_seed)
    digit: int = len(str(max_mulder))
    if max_mulder < 1:
        max_mulder = -1
        digit = 4
    original: str = script.strip()
    words, marks = script2words(script=original)
    slices: list[list[str]] = [
        [x[: (len(x) + 1) // 2], x[(len(x) + 1) // 2 :]] for x in words
    ]
    i: int = 0
    while True:
        i += 1
        shuffle(slices)
        flatten: list[str] = []
        for x in zip_longest(*[iter(slices)] * 2):
            flat: list[str] = list(chain.from_iterable(filter(None, x)))
            assert len(flat) in [2, 4]
            if randint(0, 1) == 0:
                if len(flat) == 4:
                    flatten.extend([flat[2], flat[1], flat[0], flat[3]])
                else:
                    flatten.extend([flat[1], flat[0]])
            else:
                flatten.extend(flat)
        for pos, mark in sorted(marks, key=lambda x: x[0], reverse=True):
            flatten = flatten[:pos] + [mark] + flatten[pos:]
        muldered: str = "".join(flatten)
        print(f"{i:0{digit}d}: {muldered}")
        if original == muldered:
            return
        if max_mulder > 0 and i >= max_mulder:
            return


class MyHelpFormatter(
    RawTextHelpFormatter,
    RawDescriptionHelpFormatter,
    ArgumentDefaultsHelpFormatter,
):
    pass


def main():
    parser: ArgumentParser = ArgumentParser(
        description="モルダーが疲れるか最大モルダー数に至るまでモルダーする",
        formatter_class=MyHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--script",
        type=str,
        default="モルダー、あなた疲れてるのよ",
        help="モルダーする台詞\n",
    )
    parser.add_argument(
        "-m",
        "--max-mulder",
        type=int,
        default=50,
        help="最大モルダー数（０の場合は疲れるまでモルダーする）\n",
    )
    parser.add_argument(
        "-r",
        "--random-seed",
        type=int,
        default=None,
        help="乱数のシード値（指定しない場合はランダムにモルダーする）\n",
    )
    args: Namespace = parser.parse_args()
    mulder(**vars(args))
    return


if __name__ == "__main__":
    main()
