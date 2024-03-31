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
            for key in reader.fieldnames:
                metadata[key] = []
            for row in reader:
                for key in row:
                    if row[key] != '':
                        metadata[key].append(row[key])
        print(metadata)
        return metadata

    def build_hierarchy(self):
        hierarchy = {}
        for row in self.relevant_rows:
            if row['parent'] not in hierarchy:
                hierarchy[row['parent']] = {
                    'canvases': [],
                    'manifest_title': '',
                    'artists': []
                }
            #canvas = DataCanvas(row, self.artists, self.metadata)
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
    reader.build_hierarchy()
    # print(reader.relevant_rows)