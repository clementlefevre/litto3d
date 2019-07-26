import bpy
import sys
from os.path import isfile
import os

blender_tiles = '/content/drive/My Drive/blender/berlin_mitte_voyager.tiff'
blender_raster  ='/content/drive/My Drive/blender/berlin_mitte_no_na.tif'

o  = bpy.data.objects['Plane'] # Replace with your actual object's name
t  = o.active_material.node_tree
im = t.nodes['Image Texture'].image
im.filepath = blender_raster

im_color = t.nodes['Image Texture.001'].image
im_color.filepath = blender_tiles




# https://blender.stackexchange.com/questions/5281/blender-sets-compute-device-cuda-but-doesnt-use-it-for-actual-render-on-ec2
bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.user_preferences.addons['cycles'].preferences.devices[0].use = True

bpy.context.scene.cycles.device = 'GPU'

bpy.data.scenes["Scene"].render.filepath = "output.png"

for scene in bpy.data.scenes:
    scene.render.resolution_percentage = 100

# redirect output to log file
logfile = 'blender_render.log'
open(logfile, 'a').close()
old = os.dup(1)
sys.stdout.flush()
os.close(1)
os.open(logfile, os.O_WRONLY)


bpy.ops.render.render(write_still=True)



# disable output redirection
os.close(1)
os.dup(old)
os.close(old)





#~/blender-2.79b-linux-glibc219-x86_64/blender  berlin_humboldthain.blend -b -P config.py --render-output . --engine CYCLES --render-format PNG --use-#extension 1 --render-frame 1 -- image.jpg
