import random
import os
import game_config as gc

from pygame import image, transform

demons_count = dict((a, 0) for a in gc.ASSET_FILES)

back_card = image.load('other_assets/behind.png')

def available_demons():
    return [demon for demon, count in demons_count.items() if count < 2]

# หลังการ์ด , random
class Demon:
    def __init__(self, index):
        self.index = index
        self.name = random.choice(available_demons())
        self.image_path = os.path.join(gc.ASSET_DIR, self.name)
        self.row = index // gc.NUM_TILES_SIDE
        self.col = index % gc.NUM_TILES_SIDE
        self.skip = False
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (gc.IMAGE_SIZE - 2 * gc.MARGIN, gc.IMAGE_SIZE - 2 * gc.MARGIN))
        self.box = self.image.copy()
        self.box = transform.scale(back_card,(125 ,125))
        demons_count[self.name] += 1
        
