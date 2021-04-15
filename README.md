# BitClout Experimentation Repo
I'm experimenting with BitClout's existing APIs. Shoutout to @HPaulson. His repo: https://github.com/HPaulson/BitClout saved me a lot of time and effort. 

## BitClout Base Client
- This is a base client to use for interacting with BitClout APIs. For now all it does is either get the current block or get transaction info. It uses cloudscraper to get around the CloudFlare Bot Protection.

## Transactions
- Wrapper of transaction data. Will improve and expand later

## Get Transaction Info
- Just an example of what you can do with Transactions / Client. Running get_transaction_info.py makes a get_transcription_info call to the base client and returns some stats about the transcriptions. Usage:
```bash
get_transaction_info.py [-h] --public_key PUBLIC_KEY [--is_mempool IS_MEMPOOL]
```

## Get Profile Dataset
- Just an example of what you can do with get-profiles API and base client. Running get_profile_dataset.py makes iterative calls to get-profiles API to construct a dataset of profile info. Will terminate when max number of (non-unique) items returned is hit. 
  Usage:
  ```bash
  get_profile_dataset.py [-h] --path PATH [--maxItems MAXITEMS] [--overwrite OVERWRITE]
  ```
  - path: path to dataset json file that will be created with the profiles
  - maxItems: Optional parameter specifying a max number of profiles to search. Default is 100
  - overwrite: Optional parameter indicating whether to overwrite dataset json file if it exists

# Daily Updates
- 4/13/21: Headed to bed. Pushed a starting point. Will expand tomorrow.
- 4/14/21: Added two more APIs to the base client: get-profiles and get-exchange-rate. Threw together a super basic "profile dataset builder" on top of the get-profiles API that builds a json dataset of profile info and saves it to a local json file. I haven't run the code long enough to reach termination yet. Will let this run overnight and see if it terminates. You can pass a maxItems param to make it terminate after a certain number of profiles are collected. 