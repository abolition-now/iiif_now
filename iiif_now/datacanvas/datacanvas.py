from csv import DictReader

class DataCanvas:
    def __init__(self, canvas_data, artists_data, metadata_data):
        self.canvas_data = canvas_data
        self.artists_data = artists_data
        self.metadata_data = metadata_data
        self.artists = self.__find_canvas_artists()
        self.metadata = self.__build_metadata()

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
