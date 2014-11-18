__author__ = 'lester'

import math
import os
from PIL import Image
from PIL import ImageChops

class dfrnt:
    def __init__(self, run_dir='run', gold_dir='gold', diff_dir='diff', mask_dir='mask', fuzzy=None):
        # This is the directory of screenshots from your run, aka 'actual screenshots'
        self.run_dir = run_dir
        # This is the directory of screenshots that are compared against, aka 'expected screenshots'
        self.gold_dir = gold_dir
        # This is the directory to output the visual diff images into
        self.diff_dir = diff_dir
        # This is the directory to contain images with highlighted areas you wish to ignore in the diff
        self.mask_dir = mask_dir
        # This is a "fuzziness" factor of how different images can be and still pass.
        # If you experience jitter you should experimentally determine the lowest acceptable number you can use.
        # Default is none, we are using 40 in our testing of 1024x768 images
        self.fuzzy = fuzzy

    def diff(self):
        self.run_ss = [run for run in os.listdir(self.run_dir)]
        self.gold_ss = [gold for gold in os.listdir(self.gold_dir)]
        self.mask_ss = [mask for mask in os.listdir(self.mask_dir)]

        if self.run_ss != self.gold_ss:
            print 'Missing screenshots: %s' % str(list(set(self.gold_ss).difference(self.run_ss)))
            print 'Extra screenshots: %s' % str(list(set(self.run_ss).difference(self.gold_ss)))

        # Diff all the images common to run and gold directories
        for ss in list(set(self.run_ss).intersection(self.gold_ss)):
            try:
                # Apply the mask, if it exists
                if ss in self.mask_ss:
                    base = Image.open(self.run_dir + ss)
                    mask = Image.open(self.mask_dir + ss)
                    Image.alpha_composite(base, mask).save(self.run_dir+ss)
                if not self.images_identical(self.gold_dir + ss, self.run_dir + ss):
                    rms = self.image_diff(self.gold_dir + ss, self.run_dir + ss, self.diff_dir + ss, (255, 0, 0))[0]
                    # Experimentally found value, "fuzziness factor"
                    if rms < self.fuzzy:
                        pass
                    else:
                        print 'Diff failed! %s is not identical enough.' % ss
            except AssertionError:
                print "Diff failed! %s. Images have different dimensions or pixel modes." % ss

    @classmethod
    def rmsdiff_rgba(cls, im1, im2):
        # Calculate the root-mean-square difference between two images
        diff = ImageChops.difference(im1, im2)
        h = diff.histogram()
        # Modulo 256, since this is a multiband (RGBA) image
        sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(im1.size[0] * im1.size[1]))
        return rms

    @classmethod
    def images_identical(cls, path1, path2):
        im1 = Image.open(path1)
        im2 = Image.open(path2)
        return ImageChops.difference(im1, im2).getbbox() is None

    @classmethod
    def image_diff(cls, path1, path2, outpath, diffcolor):
        im1 = Image.open(path1)
        im2 = Image.open(path2)

        rmsdiff = cls.rmsdiff_rgba(im1, im2)

        pix1 = im1.load()
        pix2 = im2.load()

        assert im1.mode == im2.mode, 'Different pixel modes between %r and %r' % (path1, path2)
        assert im1.size == im2.size, 'Different dimensions between %r (%r) and %r (%r)' % (path1, im1.size, path2, im2.size)

        mode = im1.mode

        if mode == '1':
            value = 255
        elif mode == 'L':
            value = 255
        elif mode == 'RGB':
            value = diffcolor
        elif mode == 'RGBA':
            value = diffcolor + (255,)
        elif mode == 'P':
            raise NotImplementedError('TODO: look up nearest palette color')
        else:
            raise NotImplementedError('Unexpected PNG mode')

        width, height = im1.size

        for y in xrange(height):
            for x in xrange(width):
                if pix1[x, y] != pix2[x, y]:
                    pix2[x, y] = value
        im2.save(outpath)

        return (rmsdiff, width, height)

    @classmethod
    def crop(cls, image, width, height, x=0, y=0):
        im = Image.open(image)
        im.crop((x,y,width,height)).save(image)
