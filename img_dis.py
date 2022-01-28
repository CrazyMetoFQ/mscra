"""
view image in ipython notebook
"""

from IPython.display import display,HTML,Image
from os import listdir

class ImageViewEr:
  
  """
  view images in IPython notebook
  
  run in order
  
  self.sort_ls()
  self.format_imgs()
  
  self.show_image()
  """
  
  def __init__(self,image_path):
    """
    image_path -> str to images
    """
    
    self.img_path = image_path
    self.img_list = [f"{self.img_path}/{img}" for img in listdir(self.img_path)]

  def sort_ls(self, x, y):
    """
    truly sorts image list

    x ->  stars wih
    y -> ends with
    """

    imd = {}
    for img in self.img_list:

      no = int(img[ img.find(x) + len(x) : img.find(y) ])
      imd[no] = img
          
    sorted_chs = [imd[k] for k in sorted(imd)]

    self.sorted_images = sorted_chs
    return sorted_chs 


  def format_imgs(self):
    """
    converts the image of path to img objs,
    and adds breaks between each image
    """

    imdi = []
    for im in self.sorted_images:

      imdi.append(Image(im))
      imdi.append(HTML('<div> <br>---------------------------<br> <br> </div>'))

    self.formated_images = imdi

  
  def show_images(self):

    display(HTML("""
    <style>
    #output-body {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    </style>
    """))
    display(*self.formated_images)
