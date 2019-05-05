import os
import cv2
import numpy
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from urllib.request import urlopen
from PIL import Image

class ImageEngine:
    def __init__(self):
        self.msg = None
    
    def request(self, item):
        raise NotImplementedError
    
 #   def iterate(self, idx):
 #       return self.images[idx]
 #   
 #   def length(self):
 #       return len(self.images)
    
class BingImageEngine(ImageEngine):
    def __init__(self, key):
        super(BingImageEngine, self).__init__()
        self.key = key
        self.client = ImageSearchAPI(CognitiveServicesCredentials(self.key))
    
    def request(self, item):
        image_results = self.client.images.search(query=item)
        images = list()
        if image_results.value:
            print("Total number of images returned: {}".format(len(image_results.value)))
            self.msg = "Successfully requested!"
            for i in range(int(len(image_results.value)/10)):
                image_result = image_results.value[i]
                print("image thumbnail url: {}".format(image_result.thumbnail_url))
                print("image content url: {}".format(image_result.content_url))
                img = Image.open(urlopen(image_result.thumbnail_url))
                images.append(cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR))
        else:
            self.msg = "No image results returned!"
            print("No image results returned!")
        return images


if __name__ == "__main__":
    key = "3e49862cde1443c3b88b0538bb42b6cd"
    bie = BingImageEngine(key)
    bie.request("obama")
