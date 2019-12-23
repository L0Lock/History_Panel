# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.utils import register_class

bl_info = {
    "name": "History Panel",
    "description": "Brings back the «History» panel with all its history managment including the famous Undo & Redo buttons.",
    "author": "Loïc \"L0Lock\" Dautry",
    "version": (0, 0, 2),
    "blender": (2, 81, 0),
    "location": "3D Viewport > Sidebar > Tool tab.",
    "warning": "",
    "wiki_url": "https://github.com/L0Lock/History_Panel",
    "tracker_url": "https://github.com/L0Lock/History_Panel/issues",
    "category": "3D View"
}

class VIEW3D_PT_UndoRedo(bpy.types.Panel):
    bl_label = "History"
    bl_idname = "VIEW3D_PT_undo_redo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool' # 'Tool'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("ed.undo", icon='LOOP_BACK')
        row.operator("ed.redo", icon='LOOP_FORWARDS')
        col.operator("ed.undo_history", icon='BACK')

        col = layout.column(align=True)
        col.label(text="Repeat:")
        col.operator("screen.repeat_last", icon='FILE_REFRESH')
        col.operator("screen.repeat_history", text="History...", icon='SORTTIME')
        
# Prefs Addon

def update_category(self, context):
    is_panel = hasattr(bpy.types, 'VIEW3D_PT_UndoRedo')

    if is_panel:
        try:
            bpy.utils.unregister_class(VIEW3D_PT_UndoRedo)
        except:
            pass
    VIEW3D_PT_UndoRedo.bl_category = self.category
    bpy.utils.register_class(VIEW3D_PT_UndoRedo)

class AddonPrefs(AddonPreferences):
    bl_idname = __name__
    
#    PrefTab = StringProperty(
#        name = "Tab (default: \"Tool\")",
#        default = "Tooltest"
#    )
#    
#    pref_tab = PrefTab
#    
#    def draw(self, context):
#        layout = self.layout
#        layout.label(text="In which tab should the History panel be placed?")
#        layout.prop(self, "PrefTab")
    category : StringProperty(description="Choose the target tab for the panel.",default="Tool",update=update_category)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="In which tab should the History panel be placed in?")
        layout.prop(self, "category")

# Register

classes = (
    VIEW3D_PT_UndoRedo,
    AddonPrefs,
)

def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")
        
    # Update Category
    context = bpy.context
    prefs = context.preferences.addons[__name__].preferences
    update_category(prefs, context)

def unregister():
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)