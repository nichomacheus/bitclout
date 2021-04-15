import os
from pathlib import Path
from typing import Dict

from networking.client import BitCloutBaseClient, IdentifierType

DEFAULT_MAX_ITEMS = 100


class ProfileDataSetBuilder:
    def __init__(self, client: BitCloutBaseClient):
        self.baseClient = client

    def build(
            self,
            path_to_dataset_file: str,
            max_items: int = DEFAULT_MAX_ITEMS,
            key_on: IdentifierType = IdentifierType.USERNAME,
            overwrite_file: bool = False,
    ) -> Dict[str, dict]:
        dataset = {}
        profiles_collected = 0
        next_public_key = None
        if os.path.isfile(path_to_dataset_file) and not overwrite_file:
            raise RuntimeError(
                "Error, dataset file already exists and overwrite flag is false!"
            )
        if key_on == IdentifierType.USERNAME:
            key_tag = "Username"
        elif key_on == IdentifierType.PUBLIC_KEY:
            key_tag = "PublicKeyBase58Check"
        else:
            raise RuntimeError("Bad Identifier Type encountered!")
        Path(path_to_dataset_file).touch()
        while True:
            response_json = self.baseClient.get_profiles(
                tag_type=IdentifierType.PUBLIC_KEY, tag=next_public_key
            ).json()
            next_public_key = response_json["NextPublicKey"]
            profiles = response_json["ProfilesFound"]
            profiles_collected += len(profiles)
            for profile in profiles:
                dataset[profile[key_tag]] = profile
            if profiles_collected > max_items:
                print("Reached max profiles to collect!")
                break
            print(chr(27) + "[2J")
            print(
                "Collected {} profiles. Next Public Key is: {}. The most recent profiles we grabbed are:\n{}".format(
                    profiles_collected,
                    next_public_key,
                    "\n".join([profile["Username"] for profile in profiles]),
                ),
            )
        return dataset
