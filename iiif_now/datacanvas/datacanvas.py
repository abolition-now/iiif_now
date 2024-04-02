from csv import DictReader

class DataCanvas:
    def __init__(self, canvas_data, artists_data, metadata_data):
        self.canvas_data = canvas_data
        self.artists_data = artists_data
        self.metadata_data = metadata_data
        self.artists = self.__find_canvas_artists()
        self.metadata = self.__build_metadata()
        self.label = self.canvas_data['canvas title']
        self.sequence = self.get_sequence(self.canvas_data['sequence'])
        self.parent = self.canvas_data['parent']
        self.type = self.canvas_data['type']
        self.thumbnail = self.__find_thumbnail_source()
        self.parent_title = self.canvas_data['title']
        self.as_dict = self.__build_dict()

    @staticmethod
    def get_sequence(value):
        try:
            return int(value)
        except ValueError:
            return 1

    def __find_canvas_artists(self):
        artists = []
        split_key =  self.canvas_data['key'].split('_')
        for value in split_key:
            if value in self.artists_data:
                artists.append(self.artists_data[value])
        return artists

    def __build_metadata(self):
        metadata = {}
        for k, v in self.canvas_data.items():
            if k.startswith('code_') and v and v in self.metadata_data:
                field = self.metadata_data[v]
                metadata.setdefault(field, []).append(v)
        return metadata

    def __find_thumbnail_source(self):
        if self.canvas_data['thumbnail source'] != '':
            return self.canvas_data['thumbnail source']
        else:
            return self.canvas_data['key']

    def __build_dict(self):
        return {
            'label': self.label,
            'sequence': self.sequence,
            'parent': self.parent,
            'type': self.type,
            'thumbnail': self.thumbnail,
            'metadata': self.metadata,
            'artists': self.artists,
            'key': self.canvas_data['key'],
            'duration': self.canvas_data['duration']
        }
