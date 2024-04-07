from slugify import slugify

class HomePage:
    def __init__(self, label):
        self.label = label
        self.uri = self.__process_label_for_uri(label)
        self.body = self.__build()

    @staticmethod
    def __process_label_for_uri(title):
        return f"https://abolition-now.github.io/an/works/{slugify(title)}"

    def __build(self):
        return {
            "id": self.uri,
            "type": "Text",
            "label": { "en": [ self.label ] },
            "format": "text/html",
            "language": [ "en" ]
        }