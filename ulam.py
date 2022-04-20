import numpy as np
import PIL
import sys
# https://scipython.com/blog/the-ulam-spiral/, Christian Hill, October 2016

def make_spiral(arr):
    nrows, ncols = arr.shape
    idx = np.arange(nrows*ncols).reshape(nrows, ncols)[::-1]
    spiral_idx = []
    while idx.size:
        spiral_idx.append(idx[0])
        idx = idx[1:] # Remove the first row (the one we've just appended to spiral)
        idx = idx.T[::-1] # Rotate the rest of the array anticlockwise
    spiral_idx = np.hstack(spiral_idx) # Make a flat array of indices spiralling into the array
    spiral = np.empty_like(arr) # Index into a flattened version of our target array with spiral indices
    spiral.flat[spiral_idx] = arr.flat[::-1]
    return spiral

w = 1000 if len(sys.argv) < 2 else int(sys.argv[1])
primes = np.array([n for n in range(2, w**2+1) if all((n % m) != 0 for m in range(2, int(np.sqrt(n))+1))])
arr = np.zeros(w**2, dtype='u1')
arr[primes-1] = 1
arr = make_spiral(arr.reshape((w, w)))

img = PIL.Image.fromarray(arr*255)
img.save(f'ulam/ulam{w}.png')

# ifftarr = np.fft.ifft2(arr)
# ifftarr -= ifftarr.min()
# ifftarr *= 255/ifftarr.max()
# ifftarr = ifftarr.astype(int)
# ifftimg = PIL.Image.fromarray(ifftarr, mode='L')
# ifftimg.save(f'ulamifft{w}.png')