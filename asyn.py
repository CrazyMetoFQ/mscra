"""
The main file to run asynchrounous requests
"""


import time
# complete_start = time.time()  

import asyncio
import aiohttp
import os

from bs4 import BeautifulSoup
import img2pdf

  
async def get_urls(urls, round_to = 20, debug_ = False):
  """
  urls -> list of links

  returns response, ok, content of urls.
  requests are sent asynchrously.
  """
  
  if debug_:print(urls)
  else:pass

  start = time.time()  
  async with aiohttp.ClientSession() as session:
    	   
    tasks = []
    for url in urls:
      tasks.append(asyncio.create_task(session.get(url, ssl=False)))

    responses = await asyncio.gather(*tasks)
      
    urls_result = {"res":responses,
                      "ok":[r.ok for r in responses],
                      "content":[await r.content.read() for r in responses]}

    end = time.time()
    total_time = end - start
    print("It took {} seconds to make {} calls".format(round(total_time, round_to),len(urls)))
    
    return urls_result


def find_imgs(cnt , base_link, ky = "src", strt=None,stp=None,step=None, round_to = 20, debug_ = False):
  """
  cnt -> html
  ky -> str, what is the key for src for imgs

  strt, stp, stp -> int

  finds all imgs in html
  returns list of links to imgs
  """
  start = time.time()  

  soup = BeautifulSoup(cnt, 'lxml')
  img_list = list(soup.findAll('img'))
  nl = '\n'
  if debug_:print(f"img_list = {img_list}{nl}{ky}{nl}{strt} {stp} {step} {round_to}{nl}")
  else:pass

  imli = []
  for im in img_list[strt:stp:step]:
    try:
      si = im[ky]
      si.replace("\n","")
      si.replace("\t","")

      if "." not in si[:-7] and "/" == si[0]:
        si = base_link + si
      else:
        pass

      if "http" not in si:
        si = "http:" + si
      else:pass

      if "w3.org" not in si:
        imli.append(si)  
      
      else: pass
      
    except:
      print("src invalid")
      try:
        si = im["data-src"]
        si.replace("\n","")
        si.replace("\t","")

        if "http" not in si:
          si = "http:" + si
        else:pass
        
        imli.append(si)

      except Exception() as e:
        print(e)
        print("eror ocured")
        print(im)
        print(ky)
        print(type(im))
        print(im['src'])


  end = time.time()
  total_time = end - start
  print("It took {} seconds to find {} images".format(round(total_time, round_to),len(imli)))

  return imli


def converr(imgs,path, save_as = "pdf", file_format = ".pdf",round_to = 20):
  """
  imgs -> list of binary imgs
  path - > str of path to files

  save_as --> image or pdf 
  """
  start = time.time()  

  # pdf
  if save_as == "pdf":
    with open(f"{path}{file_format}",'wb') as f:
      try:
        f.write(img2pdf.convert(imgs))
      
      except Exception() as e:
        print(e)

    end = time.time()
    total_time = end - start
    print("It took {} seconds to write a {} page pdf".format(round(total_time, round_to),len(imgs)))
  
  # Images
  elif save_as == "image" or save_as == "img":
    os.mkdir(path)

    for sno,img in enumerate(imgs):
      
      with open(f"{path}/img{sno}{file_format}",'wb') as f:
        try:
          f.write(img)
        
        except Exception() as e:
          print(e)

    end = time.time()
    total_time = end - start
    print("It took {} seconds to write {} images".format(round(total_time, round_to),len(imgs)))

    
    

def main_func(urls, path, base_link, save_info = ("pdf",".pdf"),round_to = 20,debug__ = False, iKy = 'src',imgs_kwargs ={'strt':None,'stp':None,'step':None}):
  """
  urls -> list of urls
  path -> path to pdfs
  """
  start = time.time()  

  pg_d = asyncio.run(get_urls(urls, round_to,debug_ = debug__)) # pages to find the imgs
  print("\n------------------------\n")

  all_imgs = [find_imgs(cnt, base_link,round_to = round_to,debug_=debug__,ky = iKy, **imgs_kwargs) for cnt in pg_d["content"]] # all image links in nested list
  print("------------------------\n")

  del pg_d

  for sno,imgs in enumerate(all_imgs, start = 1):
    

    print(f"getting ch {sno}")
    img_d = asyncio.run(get_urls(imgs, round_to,debug_ = debug__)) # dict of images, contains binary


    print(f"making ch {sno}")
    converr(img_d["content"],f"{path}/ch_{sno}", save_info[0], save_info[1],round_to)
    print("------------------\n")


  end = time.time()
  total_time = end - start
  print("It took {} seconds to make {} chapters.".format(round(total_time, round_to),len(urls)))
