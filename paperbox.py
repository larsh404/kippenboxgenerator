# requires https://pypi.org/project/dxfwrite/
from dxfwrite import DXFEngine as dxf

# Box size, filename
width = 90
height = 58
depth = 20

filename = 'paperbox_'+str(width)+'x'+str(height)+'x'+str(depth)+'.dxf'

# Special formats
# 90x58x20   --> my standard format
# 90x60x23   --> 60mm is too wide for my machine
# 98x58x25   --> 98mm long box fits only with some modifications to the machine,
#                i.e. the one-way flap needs to be removed, this also means the
#                machine will be less reliable

# Box settings
flap=8
depthflap=15 
break3=1

flapindentx = 0
flapindenty = 5

closurespacing = 15
closurelength1 = width-2*flap-2*closurespacing
closurelength2 = width-2*closurespacing
closureextension = 0.8


# colors, 0: black, 1: red, 2: yellow, 3: green, 4: cyan, 5: blue, 6: magenta, 7: black, 8: gray, 9: gray, 10: black
color_cut = 0
color_fold = 1

drawing = dxf.drawing(filename)

# Move start position so that the result will fit on an A4 sheet
x = 10 + depth + depthflap
y = 287

def line(dx, dy, color=color_cut):
  global x, y

  x1 = x + dx
  y1 = y - dy
  drawing.add(dxf.line((x, y), (x1, y1), color=color))
  x = x1
  y = y1

def notch(dx, dy, ox=0, oy=0, color=color_cut):
  global x, y
  x1 = x + dx + ox
  y1 = y - dy - oy
  drawing.add(dxf.line((x+ox, y-oy), (x1, y1), color=color))

def bend(dx, dy, ox=0, oy=0, color=color_fold):
  global x, y

  x1 = x + dx + ox
  y1 = y - dy - oy
  drawing.add(dxf.line((x+ox, y-oy), (x1, y1), color=color))


# Start on the upper left corner, first draw the side flap
line(flap, -flap)
line(width-2*flap, 0)
line(flap, flap)

# folding edge for side flap
bend(closurespacing, 0, -width, 0)
bend(closurespacing, 0, -closurespacing, 0)

# add the slot where the corresponding flap latches
notch(width-2*closurespacing, 0, -width+closurespacing, 0)

# top/bottom flap
line(0, height)

# side bend line
bend(-width, 0)
bend(0, depth)

# side stabilizer flap
line(depthflap, break3)
line(0, depth-2*break3)
line(-depthflap, break3)

# side bend line
bend(-width, 0)

# top/bottom flap
line(depth, 0)
notch(-flapindentx, flapindenty)
bend(0,height-2*flapindenty, -flapindentx, flapindenty)
line(flap, flap)
line(0, height-2*flap)
line(-flap, flap)
notch(-flapindentx, -flapindenty)
line(-depth, 0)

# top/bottom bend line
bend(0, -height)

# side bend line
bend(-width, 0)

# top/bottom stabilizer flap bend line
bend(0, depth)

# top/bottom stabilizer flap
line(depthflap, break3)
line(0, depth-2*break3)
line(-depthflap, break3)

# side closure flap
line(-closurespacing+flap/2, 0)
bend(-closurelength2-0*flap, 0, -flap, 0)

notch(-flap, 0)
line(-flap, flap)
line(-closurelength2+flap, 0)
line(-flap, -flap)
notch(flap, 0)


line(-closurespacing+flap/2, 0)


# top/bottom stabilizer flap bend line
bend(0, -depth)

# top/bottom stabilizer flap
line(-depthflap, -break3)
line(0, -depth+2*break3)
line(depthflap, -break3)

# top/bottom bend line
bend(0, -height)

# top/bottom flap
line(-depth, 0)
notch(flapindentx, -flapindenty)
bend(0,-height+2*flapindenty, flapindentx, -flapindenty)
line(-flap, -flap)
line(0, -height+2*flap)
line(+flap, -flap)
notch(flapindentx, flapindenty)
line(depth, 0)

# top/bottom stabilizer flap bend line
bend(0, -depth)

# top/bottom stabilizer flap
line(-depthflap, -break3)
line(0, -depth+2*break3)
line(depthflap, -break3)

# last cut line back to home position
line(0, -height)


drawing.save()
