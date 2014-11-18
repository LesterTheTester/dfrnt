dfrnt is a library for comparing PNG screenshots during automated testing and producing visual diffs.

dfrnt will compare images with identical names from automation and produce a result "diff" image that red-highlights regions
in the image that differ.

dfrnt requires a minimum of 3 folders to be specified:

run_dir is the directory of screenshots from your run, aka 'actual screenshots'
gold_dir directory of screenshots that are compared against, aka 'expected screenshots'
diff_dir is the directory to output the visual diff images into

Invoking:

1. You have a directory of images from your latest test run in "run" (1.png, 2.png, 3.png)
2. You have a directory of the expected images in "gold" (1.png, 2.png, 3.png)
3. You want the output of visual diffs to be placed in directory "diff"

import dfrnt

visual_diffs = dfrnt(run_dir="run", gold_dir="gold", diff_dir="diff")

visual_diffs.diff()

Output:
Diff failed! 2.png is not identical enough

A red-lined image showing the differences between run/2.png and gold/2.png is generated in diff/2.png

Optional Features:
mask_dir is the directory to contain images with highlighted areas you wish to ignore in the diff.
This is useful for ignoring portions of an image that always change, like date / time.
These mask images should be transparent background PNGs

fuzzy is a "fuzziness" factor of how different images can be and still pass.
If you experience jitter you should experimentally determine the lowest acceptable number you can use.
Default is None, starting your binary search around '40' is recommended

visual_diffs = visual_diffs = dfrnt(run_dir="run", gold_dir="gold", diff_dir="diff", mask_dir="mask", fuzzy=40)

Why is this project called 'dfrnt'?
To mock the modern practice of dropping vowels in software names to sound unique. Be glad I didn't name it dfrntzlyr.