Produces a visualization of [OEIS A250001: Number of arrangements of n circles in the affine plane.](https://oeis.org/A250001).
Full credit goes to Jon Wild of McGill University for the layout of the circles, see the OEIS page for his images.

See output for the connected n=4 here:
[![Watch the video](https://img.youtube.com/vi/cTM2c9mWMhY/maxresdefault.jpg)](https://youtu.be/cTM2c9mWMhY)

## Building
Assuming `manim` is correctly installed, the below produces outputs in `media/2160p60/*.mp4`:
```
manim -qk main.py
```