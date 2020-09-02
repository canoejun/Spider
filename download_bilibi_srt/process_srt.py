


def process():
    result = ""
    with open("./srt.txt","r") as f :
        for line in f.readlines():
            if len(line.strip()) == 0:
                line = "&" + line.replace("\n","")
            result += line

    result = result.split("&")

    fianl_result = []

    for single in result:
        singles = single.split("\n")
        for i in range(2, len(singles)):
            if len(singles[i].strip()) != 0 :
                fianl_result.append(singles[i])

    with open("./result.txt",'w') as f:
        result = "，".join(fianl_result)
        f.write(result)


if __name__ == '__main__':
    process()