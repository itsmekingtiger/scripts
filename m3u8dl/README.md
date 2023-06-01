# m3u8dl

My IDM does not download encrypted m3u8 videos.

# Usage

1. Write list of urls on `m3u8_list.txt`.

   For example:

   ```txt
   https://lorem.com/ipsum.m3u8
   https://lorem.com/ipsum/dolor.m3u8
   https://lorem.ipsum.com/dolor.m3u8
   https://lorem.ipsum.com/2023/01/01/dolor.m3u8
   ```

2. Run
   ```bash
   $ poetry shell
   $ poetry install
   $ poetry run m3u8dl
   ```
