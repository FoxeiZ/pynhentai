# pynhentai
*coom*
# Installation
```
git clone https://github.com/FoxeiZ/pynhentai
cd pynhentai
python setup.py install
```
> You might need to run the last command with `root` (or `Administrator` if you are a Windows user)
# Usage
```py
from pynhentai import nhentai

api = nhentai()

# Get info for the sauce
sauce = await api.getByID('177013')
# <nhentaiContainer(id=177013, media_id=987560, title='[ShindoLA] M...te) [English]')>

# Get pages
await api.getPageImage('177013')
# or
sauce.pages
# Same result tho
