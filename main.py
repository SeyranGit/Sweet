from parser import Parser
import sys


def commandline(arguments: list) -> str:
    if len(arguments) > 1:
        return arguments[1]


def main(source_file: str):
    with open(source_file, "r") as source_file:
        codelines = source_file.read()
        parser = Parser(codelines)
        result = parser.run()


if __name__ == '__main__':
    arguments = sys.argv
    source_file = commandline(arguments)
    main(source_file)
