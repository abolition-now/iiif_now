#!/usr/bin/env python3

from iiif_now.csvreader import DataReader
from iiif_now.manifest import ANManifest
import click
import yaml
from tqdm import tqdm

@click.group()
def cli() -> None:
    pass

@cli.command("use", help="Generate IIIF manifests from a AN! data files.")
@click.argument("config", required=True)
def use(config: str) -> None:
    settings = yaml.safe_load(open(config, "r"))
    reader = DataReader(
        settings['main_sheet'],
        artists_file=settings['artists_file'],
        metadata_file=settings['metadata_codes']
    )
    manifests = reader.build_hierarchy()
    for manifest in tqdm(manifests):
        x = ANManifest(
            manifest,
            image_server_path=settings['image_server_path'],
            video_location=settings['video_location'],
            manifest_bucket=settings['manifest_bucket'],
            extensions=settings['extensions']
        )
        x.write(
            settings['manifest_directory']
        )