def write_data(content, filename):
    _file = open(filename, "a+")
    _file.write(content)
    _file.write('\n')
    _file.close()

def write_dict(content):
    _file = open("query.txt", "a+")
    _file.write(content)
    _file.write(',\n')
    _file.close()