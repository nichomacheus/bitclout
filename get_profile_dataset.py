import argparse
import json

from networking.client import BitCloutBaseClient, IdentifierType
from profiles.profile_dataset_builder import ProfileDataSetBuilder, DEFAULT_MAX_ITEMS


def build_profile_dataset(
    profile_builder: ProfileDataSetBuilder,
    path_to_dataset_file: str,
    max_items: int,
    overwrite_file: bool = False,
) -> None:
    dataset = profile_builder.build(
        path_to_dataset_file,
        max_items,
        key_on=IdentifierType.USERNAME,
        overwrite_file=overwrite_file,
    )
    print("Writing collected dataset to dataset file...")
    with open(path_to_dataset_file, "w+") as dataset_file:
        json.dump(dataset, dataset_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get transaction stats for some public key"
    )
    parser.add_argument(
        "--path", type=str, help="path to dataset file to write to", required=True
    )
    parser.add_argument(
        "--maxItems",
        type=int,
        help="maximum number of profiles to collect. If not specified just keeps going.",
        required=False,
        default=DEFAULT_MAX_ITEMS
    )
    parser.add_argument(
        "--overwrite",
        help="should we overwrite the dataset file if it exists",
        action='store_true'
    )
    args = parser.parse_args()
    build_profile_dataset(
        profile_builder=ProfileDataSetBuilder(client=BitCloutBaseClient()),
        path_to_dataset_file=args.path,
        max_items=args.maxItems,
        overwrite_file=args.overwrite,
    )
