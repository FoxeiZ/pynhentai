from pynhentai.nhentai import *
import aiohttp
import sys
import os
import asyncio

client = nhentai()

# https://stackoverflow.com/a/37630397
def progressBar(current, total):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * 35 - 1) + '>'
    spaces  = ' ' * (35 - len(arrow))

    print(f'Downloading page {current}: [{arrow + spaces}] {int(percent)}%', end = '\r')

async def download_image(id, path):
    pageId = 1
    img_list = await client.getPageImage(id=id)
    for pages in img_list:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=pages['url']) as r:
                with open(f'{path}\\{pages["url"].split("/")[-1]}', 'wb') as f:
                    f.write(await r.read())
                pageId += 1
            progressBar(pageId-1, len(img_list))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <id>'.format(sys.argv[0]))
        sys.exit(1)

    id = sys.argv[1]
    path = f'.\\{id}'

    if not os.path.exists(path):
        os.makedirs(path)

    asyncio.get_event_loop().run_until_complete(download_image(id, path))
    print('\nDone!')
    sys.exit(0)