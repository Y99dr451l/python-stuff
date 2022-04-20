import numpy
import PIL.Image
import time
import sys

start_time = time.time()
images = []
iterations = 200
height = 200
width = 200
trail = 20
circular = True
# if len(sys.argv) < 2 else bool(sys.argv[1])

arr = (numpy.random.rand(height+2, width+2) * 2).astype('uint8') * 255
if not circular: arr[:, [0, -1]] = arr[[0, -1], :] = 0 # if not circular
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
            if circular and (j in (1, height) or k in (1, width)): # if circular
                j1 = j; k1 = k
                if j == 1: j1 = height+1
                elif j == height: j1 = 0
                if k == 1: k1 = width+1
                elif k == width: k1 = 0
                nextarr[j1][k1] = nextarr[j][k]
            # print(f'{j},{k}')
    arr = nextarr
    images.append(PIL.Image.fromarray(nextarr[1:-1, 1:-1]).convert('L'))
    print(i)
images[0].save(f'gol/gol{height}x{width}-{iterations}+{trail}-{circular*"circ"}.gif', save_all=True, append_images=images[1:], optimize=True, duration=40, loop=0, palette='L')
print(time.time() - start_time)