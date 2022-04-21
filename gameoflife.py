import numpy
import PIL.Image
from scipy.ndimage import convolve
import time

start_time = time.time()
iterations = 10
height = width = 1000
trail = 20
circular = False
fast = True # ignores trail

images = []

def fancymode():
    arr = (numpy.random.rand(height+2, width+2)*2).astype('uint8')*255
    if circular:
        for i in range(height):
            arr[i+1, 0] = arr[i+1, height]
            arr[i+1, height+1] = arr[i+1, 1]
        for i in range(width):
            arr[0, i+1] = arr[width, i+1]
            arr[width+1, i+1] = arr [1, i+1]
    images.append(PIL.Image.fromarray(arr[1:-1, 1:-1]).convert('L'))
    for i in range(iterations):
        nextarr = numpy.zeros((height+2, width+2)).astype('uint8')
        for j in range(1, height+1):
            for k in range(1, width+1):
                sum = -1 if arr[j][k] == 255 else 0
                subarr = arr[j-1:j+2, k-1:k+2]
                for l in range(3):
                    for m in range(3):
                        if subarr[l][m] == 255: sum += 1
                        if sum == 4: break
                    else: continue
                    break
                if sum == 3 or (sum == 2 and arr[j][k] == 255): nextarr[j][k] = 255
                elif arr[j][k] != 0: nextarr[j][k] = max(0, arr[j][k] - trail)
                if circular and (j in (1, height) or k in (1, width)):
                    j1 = j; k1 = k
                    if j == 1: j1 = height+1
                    elif j == height: j1 = 0
                    if k == 1: k1 = width+1
                    elif k == width: k1 = 0
                    nextarr[j1][k1] = nextarr[j][k]
        arr = nextarr
        images.append(PIL.Image.fromarray(nextarr[1:-1, 1:-1]).convert('L'))
        print(i)

def fastmode(): # ignores trail
    arr = (numpy.random.rand(height, width)*2).astype('uint8')
    images.append(PIL.Image.fromarray(arr*255).convert('L'))
    for i in range(iterations):
        convarr = numpy.array(convolve(arr, numpy.ones((3, 3)), mode=('wrap' if circular else 'constant'), cval = 0).astype('uint8') - arr.astype('uint8'))
        arr = numpy.logical_or((convarr == 3), numpy.logical_and((arr == 1), numpy.logical_and((1 < convarr), (convarr < 4)))).astype('uint8')
        images.append(PIL.Image.fromarray(arr*255).convert('L'))

if fast: fastmode()
else: fancymode()

images[0].save(f'gol/h{height}w{width}x{iterations}+{trail}_{fast*"fast"+circular*"circ"}.gif', save_all=True, append_images=images[1:], optimize=True, duration=40, loop=0, palette='L')
print(time.time() - start_time)