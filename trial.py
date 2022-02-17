import json
import os

from pprint import pprint

# with open(r"C:\Users\Ali Hussain\Downloads\flaskwtf_tri/stuff.json") as f:

# 	st = json.load(f)


# # pprint(st)

# class Tri:

# 	attr1 = "something"

# tri = Tri()


# for k in st:

# 	setattr(tri, k, st[k])
# 	# print(getattr(tri, "attr2"))

# for atr in dir(tri):

# 	if not atr.startswith("_"):

# 		print(atr, ":  ", getattr(tri, atr))

# 	else:
# 		pass


# class confirur:

# 	def __init__(self, path = None):

# 		if path == None:
# 			self.path = "C:/Users/Ali Hussain/Downloads/flaskwtf_tri/stuff.json" 
# 		else:
# 			self.path = path

# 		with open(self.path) as f:
# 			st = json.load(f)

# 		for k in st:
# 			setattr(self, k, st[k])


# trial = confirur()

# for atr in dir(trial):

# 	if not atr.startswith("_"):
# 		print(atr, ":  ", getattr(trial, atr))

# 	else:
# 		pass



class tri:

	a1 = 1


tria = tri()

print(tria.a2)
