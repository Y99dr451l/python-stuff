import numpy
import PIL.Image
from scipy.ndimage import convolve
import time

start_time = time.time()
iterations = 100
height = width = 100
trail = 20
circular = True
fast = True # ignores trail

def fancymode():
    arr = numpy.random.randint(2, size=(height+2, width+2), dtype='uint8')*255
    if circular:
        arr[:, 0] = arr[:, width]
        arr[:, width+1] = arr[:, 1]
        arr[0, :] = arr[height, :]
        arr[height+1, :] = arr[1, :]
    else: arr[:, 0] = arr[:, width+1] = arr[0, :] = arr[height+1, :] = 0
    images = [PIL.Image.fromarray(arr[1:-1, 1:-1]).convert('L')]
    for i in range(iterations):
        nextarr = numpy.zeros((height+2, width+2)).astype('uint8')
        for j in range(1, height+1): # use numpy iteration?
            for k in range(1, width+1):
                sum = (arr[j-1:j+2, k-1:k+2]/255).astype('uint8').sum() - int(arr[j][k]/255)
                if sum == 3 or (sum == 2 and arr[j][k] == 255): nextarr[j][k] = 255
                elif arr[j][k]: nextarr[j][k] = max(0, arr[j][k] - trail)
                if circular and (j in (1, height) or k in (1, width)):
                    nextarr[height+1 if j == 1 else (0 if j == height else j)][width+1 if k == 1 else (0 if k == width else k)] = nextarr[j][k]
        arr = nextarr
        images.append(PIL.Image.fromarray(nextarr[1:-1, 1:-1]).convert('L'))
        print(i)
    return images

def fastmode(): # ignores trail
    arr = (numpy.random.rand(height, width)*2).astype('uint8')
    images = [PIL.Image.fromarray(arr*255).convert('L')]
    for i in range(iterations):
        convarr = numpy.array(convolve(arr, numpy.ones((3, 3)), mode=('wrap' if circular else 'constant'), cval = 0).astype('uint8') - arr.astype('uint8'))
        arr = numpy.logical_or((convarr == 3), numpy.logical_and((arr == 1), (convarr == 2))).astype('uint8')
        images.append(PIL.Image.fromarray(arr*255).convert('L'))
    return images

images = fastmode() if fast else fancymode()
images[0].save(f'gol/{height}x{width}x{iterations}' + (not fast)*f'+{trail}' + fast*"f" + circular*"c" + '.gif',
                save_all=True, append_images=images[1:], optimize=True, duration=40, loop=0, palette='L')
print(time.time() - start_time)