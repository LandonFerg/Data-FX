# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "DataFX",
    "author" : "Landon-Ferguson",
    "description" : "",
    "blender" : (2, 90, 2),
    "version" : (0, 0, 3),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
)

from . scatter_op import OT_Scatter
from . scatter_panel import Scatter_Panel
from . updatevals_op import OT_UpdateVals
from . map_panel import Map_Panel, PlaceholderProperties
classes = (OT_Scatter, Scatter_Panel, Map_Panel, PlaceholderProperties, OT_UpdateVals)


#unregister = bpy.utils.register_classes_factory(classes)

def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    Scene.placeholder = PointerProperty(type=PlaceholderProperties) # register map property (put in op later?)
    #Scene.scatter_dropdown = PointerProperty(type=HeaderProperties)

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.placeholder

if __name__ == "__main__":
    register()