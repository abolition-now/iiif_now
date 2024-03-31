from csv import DictReader
from iiif_now.datacanvas import DataCanvas

class DataReader:
    def __init__(self, filename, artists_file, metadata_file):
        self.filename = filename
        self.artists = self.__dereference_artists(artists_file)
        self.metadata = self.__build_metadata(metadata_file)
        self.relevant_rows = self.__read(filename)

    def __repr__(self):
        return f"DataReader({self.filename})"

    def __str__(self):
        return f"DataReader for {self.filename}"

    @staticmethod
    def __dereference_artists(artists_sheet):
        with open(artists_sheet) as f:
            reader = DictReader(f)
            artists = {row['Artist Code']: row['Artist Name'] for row in reader}
        return artists

    @staticmethod
    def __build_metadata(metadata_sheet):
        with open(metadata_sheet) as f:
            reader = DictReader(f)
            metadata = {}
            for row in reader:
                for k, v in row.items():
                    if v != '':
                        metadata[v] = k
        return metadata

    def build_hierarchy(self):
        """
        Build a hierarchy of canvases based on the parent field in the CSV

        Returns:
            dict: A dictionary of canvases organized by parent

        Example:
            {
              '0001_newbeginnings': {
                'canvases': [
                   {'label': 'Original Image', 'sequence': '1', 'parent': '0001_newbeginnings', 'type': 'Image', 'thumbnail': '0001_newbeginnings_oo.jpg', 'metadata': {}, 'artists': ['Ricardo Levins Morales']},
                   {'label': 'Reuse', 'sequence': '2', 'parent': '0001_newbeginnings', 'type': 'Image', 'thumbnail': '0001_newbeginnings_ru.png', 'metadata': {'Visual Motif': ['Butterflies']}, 'artists': ['Ricardo Levins Morales']}
                ],
                'manifest_title': 'New Beginnings - Monarch Butterfly',
                'artists': ['Ricardo Levins Morales'],
                'metadata': {'Visual Motif': ['Butterflies']}
              }
            }
        """
        hierarchy = {}
        for row in self.relevant_rows:
            if row['parent'] not in hierarchy:
                hierarchy[row['parent']] = {
                    'canvases': [],
                    'manifest_title': '',
                    'artists': [],
                    'metadata': {}
                }
            canvas = DataCanvas(row, self.artists, self.metadata)
            if canvas.parent_title != '':
                hierarchy[row['parent']]['manifest_title'] = canvas.parent_title
            hierarchy[row['parent']]['canvases'].append(canvas.as_dict)
            for artist in canvas.artists:
                if artist not in hierarchy[row['parent']]['artists']:
                    hierarchy[row['parent']]['artists'].append(artist)
            if canvas.metadata:
                for k, v in canvas.metadata.items():
                    if k not in hierarchy[row['parent']]['metadata']:
                        hierarchy[row['parent']]['metadata'][k] = v
                    else:
                        hierarchy[row['parent']]['metadata'][k].extend(v)
        return hierarchy

    @staticmethod
    def __read(csv_file):
        relevant_rows = []
        with open(csv_file) as f:
            reader = DictReader(f)
            for row in reader:
                if row.get('parent') != "":
                    relevant_rows.append(row)
        return relevant_rows


if __name__ == '__main__':
    reader = DataReader(
        'data/march302024.csv',
        artists_file='data/artists_codes.csv',
        metadata_file='data/new_codes.csv'
    )
    x = reader.build_hierarchy()
    # for manifest, v in x.items():
    #     print(v['metadata'])
    print(x['0001_newbeginnings'])