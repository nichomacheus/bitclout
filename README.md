# BitClout Experimentation Repo
I'm experimenting with BitClout's existing APIs. Shoutout to @HPaulson. His repo: https://github.com/HPaulson/BitClout saved me a lot of time and effort. 

## BitClout Base Client
- This is a base client to use for interacting with BitClout APIs. For now all it does is either get the current block or get transaction info. It uses cloudscraper to get around the CloudFlare Bot Protection.

## Transactions
- Wrapper of transaction data. Will improve and expand later

## Main
- Just an example of what you can do with Transactions / Client. Running main.py makes a get_transcription_info call to the base client and returns some stats about the transcriptions. Usage:
```bash
main.py [-h] --public_key PUBLIC_KEY [--is_mempool IS_MEMPOOL]
```

# Daily Updates
4/13/21: Headed to bed. Pushed a starting point. Will expand tomorrow.
