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
            list: A list of dictionaries of canvases organized by parent

        Example:
            [
              {
                'id': '0001_newbeginnings',
                'canvases': [
                   {'label': 'Original Image', 'sequence': '1', 'parent': '0001_newbeginnings', 'type': 'Image', 'thumbnail': '0001_newbeginnings_oo.jpg', 'metadata': {}, 'artists': ['Ricardo Levins Morales']},
                   {'label': 'Reuse', 'sequence': '2', 'parent': '0001_newbeginnings', 'type': 'Image', 'thumbnail': '0001_newbeginnings_ru.png', 'metadata': {'Visual Motif': ['Butterflies']}, 'artists': ['Ricardo Levins Morales']}
                ],
                'manifest_title': 'New Beginnings - Monarch Butterfly',
                'artists': ['Ricardo Levins Morales'],
                'metadata': {'Visual Motif': ['Butterflies']}
              }
            ]
        """
        hierarchy = []
        for row in self.relevant_rows:
            canvas_id = row['parent']
            canvas_dict = next((item for item in hierarchy if item['id'] == canvas_id), None)
            if canvas_dict is None:
                canvas_dict = {
                    'id': canvas_id,
                    'canvases': [],
                    'manifest_title': '',
                    'artists': [],
                    'metadata': {}
                }
                hierarchy.append(canvas_dict)

            canvas = DataCanvas(row, self.artists, self.metadata)
            if canvas.parent_title != '':
                canvas_dict['manifest_title'] = canvas.parent_title
            canvas_dict['canvases'].append(canvas.as_dict)
            # @Todo: Does this need to be here with below?
            for artist in canvas.artists:
                if artist not in canvas_dict['artists']:
                    canvas_dict['artists'].append(artist)
            # @Todo: Break this into separate method
            if canvas.metadata:
                for k, v in canvas.metadata.items():
                    if k not in canvas_dict['metadata']:
                        canvas_dict['metadata'][k] = v
                    else:
                        for value in v:
                            if value not in canvas_dict['metadata'][k]:
                                canvas_dict['metadata'][k].append(value)
            # @Todo: Break this into separate method
            # Add artists to metadata if not already present
            if len(canvas_dict['artists']) > 0:
                if 'Artist' not in canvas_dict['metadata']:
                    canvas_dict['metadata']['Artist'] = canvas_dict['artists']
                else:
                    for artist in canvas_dict['artists']:
                        if artist not in canvas_dict['metadata']['Artist']:
                            canvas_dict['metadata']['Artist'].append(artist)
        for canvas_dict in hierarchy:
            canvas_dict['canvases'] = sorted(canvas_dict['canvases'], key=lambda x: int(x['sequence']))
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
