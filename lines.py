import io
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy
import PIL.Image
from scipy.ndimage import convolve

xorder = 1
yorder = 1
minlength = 3
xoffsetstep = 0
yoffsetstep = 0.333
linewidth = 0.12
mean = True
#edge = True
#edgethreshold = 120

try:
    image = PIL.Image.open(sys.argv[1])
    arr = numpy.array(image)
except Exception as e:
    print(e); exit()
bandimgs = image.split()
bands = [numpy.array(_) for _ in bandimgs]
#directionvalues = []
#directions = []

# find all possible directions for the input size, limited by xorder and yorder
'''
for i in range(min(image.height, xorder+1)):
    for j in range(min(image.width, yorder+1)):
        r = -1 if j == 0 else round(i/j, 5)
        if r not in directionvalues and [i, j] != [0, 0]:
            directionvalues.append(r)
            directions.append([i, j])
'''
directions = [[1, 1]] # override
lines = [[], [], []]

threshold = [numpy.mean(_) for _ in bands] if mean else (127, 127, 127)

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
plt.figure(figsize=(10, 10*image.height/image.width), dpi=image.width)#, bbox_inches='tight')
plt.xlim(0, image.width)
plt.ylim(0, image.height)
plt.gca().set_aspect('equal')
plt.gca().invert_yaxis()
plt.gca().set_facecolor('black')
plt.axis('off')
plt.tight_layout(pad=0, h_pad=0, w_pad=0)
plt.gca().add_patch(patches.Rectangle((0, 0), image.width, image.height, linewidth=1, edgecolor='black', facecolor='black'))
for channel in range(len(lines)):
    match channel:
        case 0: color='black' if len(bands) == 1 else 'red'
        case 1: color='green'
        case 2: color='blue'
    xoffset = channel*xoffsetstep
    yoffset = channel*yoffsetstep
    for line in lines[channel]: plt.plot([line[0][1]+xoffset, line[1][1]+xoffset], [line[0][0]+yoffset, line[1][0]+yoffset], color=color, linewidth=linewidth)
output = 'lines/' + ('output.png' if len(sys.argv) < 3 else sys.argv[2])

# if edge:
#     edgearr = numpy.array([[[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [-8, -8, -8], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]]])
#     edgeimg = PIL.Image.fromarray(convolve(arr, edgearr)).convert("RGBA")
#     datas = edgeimg.getdata()
#     newData = []
#     for item in datas:
#         if item[0] > edgethreshold and item[1] > edgethreshold and item[2] > edgethreshold: newData.append((255, 255, 255, 0))
#         else: newData.append(item)
#     edgeimg.putdata(newData)
#     buf = io.BytesIO()
#     plt.savefig(buf)
#     buf.seek(0)
#     outimage = PIL.Image.open(buf).convert('RGBA')
#     edgeimg.thumbnail(outimage.size, PIL.Image.ANTIALIAS)
#     outimage.paste(edgeimg, (0, 0), edgeimg)
#     outimage.save(output)
# else:

plt.savefig(output)
