"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def read_write_2(files_path: str):
    with (open(f"{files_path}/file1.txt", "w", encoding="utf-8") as file1,
          open(f"{files_path}/file2.txt", "w", encoding="CP1252") as file2):
        words_generated = generate_words()
        first = True

        for word in words_generated:
            if first:
                file1.write(word)
                first = False
            else:
                file1.write(f"\n{word}")

        first = True
        for word in reversed(words_generated):
            if first:
                file2.write(word)
                first = False
            else:
                file2.write(f", {word}")

        return words_generated
