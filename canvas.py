import os

class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = self.create()

    place = {
        'description': {'columns': 25, 'lines': 16, 'start_line': 8, 'start_column': 8},
        'name': {'columns': 25, 'lines': 1, 'start_line': 2, 'start_column': 8},
        'evo': {'columns': 80, 'lines': 4, 'start_line': 16, 'start_column': 0},
        'image': {'columns': 25, 'lines': 22, 'start_line': 0, 'start_column': 54}
    }

    def create(self):
        canvas = []
        for height in range(self.height):
            line = []
            for width in range(self.width):
                line.append([(0,0,0), " "])
            canvas.append(line)
        return canvas

    def add(self, place_name, text):
        text_or_color = 1 if isinstance(text[0], str) else 0
        placement = self.place[place_name]
        text = list(text)
        text_index = 0
        done = False
        # TODO: find better way to loop and break
        for line in range(placement['start_line'], placement['start_line']+placement['lines']):
            for column in range(placement['start_column'],placement['start_column']+placement['columns']):
                if text[text_index] == '\n':
                    text_index += 1
                    break
                self.content[line][column][text_or_color] = text[text_index]
                text_index += 1
                if text_index >= len(text):
                    done = True
                    break
            if done:
                break