from pathlib import Path


class Bitmap:
    def __init__(self, path: str) -> None:
        self.origin_bitmap = ""
        with open(path, mode="r") as file:
            self.origin_bitmap = file.read()

    def changeElement(self, phrase: str = "") -> str:
        if phrase == "":
            return self.origin_bitmap
        new_bitmap = ""
        for line in self.origin_bitmap.splitlines():
            for i in range(len(line)):
                if line[i] == " ":
                    new_bitmap += " "
                else:
                    new_bitmap += phrase[i % len(phrase)]
            new_bitmap += "\n"

        return new_bitmap


if __name__ == "__main__":
    path = str(Path(__file__).parent)

    pic = Bitmap(path=path + "/worldMap.txt")
    print(pic.changeElement("YOLO"))
