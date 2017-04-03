#!/home/reyzeer/anaconda2/bin/python

import numpy as np
from skimage import data, io, morphology, filters, color
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from math import sqrt

cleft = io.imread('left.jpg')
cright = io.imread('right.jpg')

# Monochromatic images
oleft = cleft[:,:,1]
oright = cright[:,:,1]

#
#selem = morphology.disk(40)
#selem = morphology.octagon(30, 36)
#selem = morphology.diamond(20)

# przeksztalcenie morfologiczne na podstawie okna prostokatnego (w stosunku do rozdzielczosci obrazu)
#selem = morphology.rectangle(7*8, 7*6)
#left = filters.median(oleft, selem)
#right = filters.median(oright, selem)

# przeksztalcenie morfoligczne z oknem "okraglym"
selem = morphology.disk(20)
left = filters.median(oleft, selem)
right = filters.median(oright, selem)

lmarkers = filters.rank.gradient(left, morphology.rectangle(8, 6)) < 10
lmarkers = ndi.label(lmarkers)[0]
lgradient = filters.rank.gradient(left, morphology.rectangle(4, 3))
llabels = morphology.watershed(lgradient, lmarkers)

rmarkers = filters.rank.gradient(right, morphology.rectangle(8, 6)) < 10
rmarkers = ndi.label(rmarkers)[0]
rgradient = filters.rank.gradient(right, morphology.rectangle(4, 3))
rlabels = morphology.watershed(rgradient, rmarkers)

listOfLabelForTheLeftImageWhichILove = np.unique(llabels)
listOfLabelForTheRightImageWhichILove = np.unique(rlabels)

#print(listOfLabelForTheLeftImageWhichILove)
#print(listOfLabelForTheRightImageWhichILove)

for cluster in listOfLabelForTheLeftImageWhichILove:
	mask = llabels == cluster
	elements = np.sum(mask)
	##print('Current cluster is %i [%i elements]' %
	#(
	#	cluster,
	#	elements
	#))
	if elements < 1000:
		llabels[mask] = 0

for cluster in listOfLabelForTheRightImageWhichILove:
		mask = rlabels == cluster
		elements = np.sum(mask)
		##print('Current cluster is %i [%i elements]' %
		#(
		#       cluster,
		#       elements
		#))
		if elements < 1000:
				rlabels[mask] = 0

#print(np.unique(llabels))
#print(np.unique(rlabels))

for o in np.unique(llabels):
	mask = llabels == o
	source = rlabels[mask]
	counts = np.bincount(source)
	#print(counts)
	o2 = np.argmax(counts)
	# print('cluster %i gives %i' %(o, o2))
	llabels[mask] = o2

for o in np.unique(rlabels):
		mask = rlabels == o
		source = llabels[mask]
		counts = np.bincount(source)
		#print(counts)
		o2 = np.argmax(counts)
		# print('cluster %i gives %i' %(o, o2))
		rlabels[mask] = o2

print(np.unique(llabels))
print(np.unique(rlabels))

for o in np.unique(rlabels):
	left_area = llabels == o
	right_area = rlabels == o
	
	left_center_of_mass = ndi.measurements.center_of_mass(left, labels = left_area)
	right_center_of_mass = ndi.measurements.center_of_mass(right, labels = right_area)
	xe = abs(left_center_of_mass[0] - right_center_of_mass[0])
	ye = abs(left_center_of_mass[1] - right_center_of_mass[1])

	distance = sqrt(xe*xe + ye*ye)

	print('Object %i\n\t%s\n\t%s\n\t%i' % (o, left_center_of_mass, right_center_of_mass, distance))



plt.subplots(figsize=(8,8))
plt.subplot(4,2,1)
plt.imshow(cleft)
plt.subplot(4,2,2)
plt.imshow(cright)
plt.subplot(4,2,3)
plt.imshow(oleft, cmap = plt.cm.gray)
plt.subplot(4,2,4)
plt.imshow(oright, cmap = plt.cm.gray)
plt.subplot(4,2,5)
plt.imshow(left, cmap = plt.cm.gray)
plt.subplot(4,2,6)
plt.imshow(right, cmap = plt.cm.gray)
plt.subplot(4,2,7)
plt.imshow(llabels)
plt.subplot(4,2,8)
plt.imshow(rlabels)

plt.savefig('entuzjazm.png')

# Zadanie
# Policzenie lepszej odlegosci miedyz obiektami kod z srodkiem ciezkosic
#
# Lepeij rozpoznac ksztalt obiektu - kod z gradientami


