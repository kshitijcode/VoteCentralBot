def write_file(text):
    f = open('failure.txt', "a")
    f.write(text + '\n')
    f.close()


def get_lines(path):
    return open(path, "r")


def read_file(path):
    return open(path, "r").read()
