import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy
import PIL.Image

minlength = 3
dpifactor = 4
mean = True

try:
    image = PIL.Image.open(sys.argv[1])
    arr = numpy.array(image)
except Exception as e: print(e); exit()
bandimgs = image.split()
bands = [numpy.array(_) for _ in bandimgs]
threshold = [numpy.mean(_) for _ in bands] if mean else (127, 127, 127)

'''
# find all possible directions for the input size, limited by xorder and yorder
xorder = 1
yorder = 1
directionvalues = []
directions = []
for i in range(min(image.height, xorder+1)):
    for j in range(min(image.width, yorder+1)):
        r = -1 if j == 0 else round(i/j, 5)
        if r not in directionvalues and [i, j] != [0, 0]:
            directionvalues.append(r)
            directions.append([i, j])
'''

directions = [[1, 1]]
lines = [[], [], []]

# identify all lines to be drawn for each band
def checklines(x, y, i, j):
    xstart = x; ystart = y
    for channel in range(len(bands)):
        linestart = []
        linelength = 0
        x = xstart; y = ystart
        while x < image.height and y < image.width:
            if bands[channel][x][y] > threshold[channel]:
                if len(linestart) == 0: linestart = [x, y]
                else: linelength += 1
            elif len(linestart) > 0:
                if linelength >= minlength: lines[channel].append([linestart, [x-i, y-j]])
                linestart = []; linelength = 0
            x += i; y += j
        if linelength >= minlength: lines[channel].append([linestart, [x-i, y-j]])

for [i, j] in directions:
    if i == 0:
        for x in range(image.height): checklines(x, 0, i, j)
    elif j == 0:
        for y in range(image.width): checklines(0, y, i, j)
    elif i >= j:
        xstart = -int(image.width/j+1)*i
        for x in range(xstart, image.height):
            y = 0
            while x < 0:
                x += i; y += j
            if y < image.width: checklines(x, y, i, j)
    else:
        ystart = -int(image.height/i+1)*j
        for y in range(ystart, image.width):
            x = 0
            while y < 0:
                x += i; y += j
            if x < image.height: checklines(x, y, i, j)  

# draw lines
plt.figure(figsize=(dpifactor, dpifactor*image.height/image.width), dpi=image.width)
plt.gca().set_aspect('equal')
plt.gca().invert_yaxis()
plt.gca().set_facecolor('black')
plt.axis('off')
plt.tight_layout(pad=0, h_pad=0, w_pad=0)
plt.gca().add_patch(patches.Rectangle((0, 0), image.width, image.height, linewidth=0.01, edgecolor='black', facecolor='black'))
for _ in range(len(lines)):
    match _:
        case 0: color='black' if len(bands) == 1 else 'red'
        case 1: color='green'
        case 2: color='blue'
    for __ in lines[_]: plt.plot([__[0][1], __[1][1]], [__[0][0]+_*0.333, __[1][0]+_*0.333], color=color, linewidth=72/image.width)
output = 'lines/' + ('output.png' if len(sys.argv) < 3 else sys.argv[2])

plt.savefig(output)
