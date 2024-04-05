# IIIF Now

## About

IIIF Manifest generation tools for the Abolition Now project.

![Example Manifest](https://github.com/abolition-now/iiif_now/blob/main/manifest_example.png?raw=true "Example Manifest")

## Installation

```bash
pip install iiif-now
```

## Configuration

Create a configuration file in YAML format. The configuration file should contain the following:

```yaml
main_sheet: 'path_to_main_sheet.csv'
artists_file: 'path_to_artists_codes.csv'
metadata_codes: 'path_to_metadata_codes.csv'
manifest_directory:  'path_to_where_you_want_manifests_to_go'
image_server_path: "https://strob6zro3bzklrulaqu2545sy0odbvz.lambda-url.us-east-2.on.aws/iiif/3/" # This is our default Image Server as of April 2, 2024.
video_location: "https://digital.lib.utk.edu/static/" # This is our default video location as of April 2, 2024. It will move in the future.
manifest_bucket: "https://aboltion-now-manifests.s3.us-east-2.amazonaws.com/" # This is a unique pattern for naming canvases. It should not be dereferenceable. 404 preferred.
extensions: ["extensions/navPlace.json"] # Path to navPlace extension
```

## Usage

```bash
iiifnow use config.yml
```