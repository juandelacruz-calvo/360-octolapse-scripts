import sys

COMMENT_PREFIX = ";"


def tweak_gcode(input: str, output: str):
    line_count = 0

    # Count lines
    with open(input, "r") as input_file:
        for line in input_file:
            if not line.startswith(COMMENT_PREFIX):
                line_count += 1

    segment = int(line_count / 800)
    line_count = 0

    with open(input, "r") as input_file:
        with open(output, "w") as output:
            for line in input_file:
                output.write(line)
                if not line.startswith(COMMENT_PREFIX):
                    line_count += 1
                    if line_count == segment:
                        line_count = 0
                        output.write("@OCTOLAPSE TAKE-SNAPSHOT\n")


if __name__ == '__main__':

    arguments = sys.argv

    if len(arguments) != 3:
        print("Usage: python tweak-gcode-360.py input_file.gcode output_file.gcode")
        sys.exit(-1)
    tweak_gcode(input=sys.argv[1], output=sys.argv[2])
