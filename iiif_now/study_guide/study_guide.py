class StudyGuide:
    def __init__(self, artists):
        self.guides = self.__known_guides()
        self.artists = artists
        self.body = self.__build()

    def __known_guides(self):
        return {
            "Josh MacPhee": {
                "url": "https://drive.google.com/file/d/1aWo1lORRVTQ0VveV3aP5Ym6hfVXUqr8_/view?usp=sharing",
                "label": 'Download "A study guide: Josh MacPhee"'
            }

        }

    def __build(self):
        for artist in self.artists:
            if artist in self.guides:
                return {
                    "id": self.guides[artist]["url"],
                    "type": "Text",
                    "label": { "en": [ self.guides[artist]["label"] ] },
                    "format": "application/pdf"
                }
        return None