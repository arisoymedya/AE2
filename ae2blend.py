bl_info = {
    "name": "AE2Blend",
    "author": "AE2Blend Contributors",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > AE2Blend",
    "description": "Paste keyframes and create objects from After Effects",
    "category": "Animation",
}

import bpy
import mathutils
import pyperclip
import math

class AE2BLEND_PT_Panel(bpy.types.Panel):
    bl_label = "AE2Blend"
    bl_idname = "AE2BLEND_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE2Blend"

    def draw(self, context):
        layout = self.layout
        layout.operator("ae2blend.paste_keyframes")
        layout.operator("ae2blend.create_empty")
        layout.operator("ae2blend.create_plane")
        layout.operator("ae2blend.create_camera")

class AE2BLEND_OT_PasteKeyframes(bpy.types.Operator):
    bl_label = "Paste Keyframes"
    bl_idname = "ae2blend.paste_keyframes"
    bl_description = "Paste keyframe data copied from After Effects"

    def execute(self, context):
        clipboard = pyperclip.paste()
        lines = clipboard.splitlines()

        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}

        for line in lines:
            parts = line.split('\t')
            if len(parts) < 4:
                continue
            frame = int(float(parts[0]))
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])

            obj.location = (x, y, z)
            obj.keyframe_insert(data_path="location", frame=frame)

        return {'FINISHED'}

class AE2BLEND_OT_CreateEmpty(bpy.types.Operator):
    bl_label = "Create Empty"
    bl_idname = "ae2blend.create_empty"
    bl_description = "Create an Empty object"

    def execute(self, context):
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        return {'FINISHED'}

class AE2BLEND_OT_CreatePlane(bpy.types.Operator):
    bl_label = "Create Plane"
    bl_idname = "ae2blend.create_plane"
    bl_description = "Create a Plane"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=2)
        return {'FINISHED'}

class AE2BLEND_OT_CreateCamera(bpy.types.Operator):
    bl_label = "Create Camera"
    bl_idname = "ae2blend.create_camera"
    bl_description = "Create a Camera"

    def execute(self, context):
        bpy.ops.object.camera_add()
        return {'FINISHED'}

classes = (
    AE2BLEND_PT_Panel,
    AE2BLEND_OT_PasteKeyframes,
    AE2BLEND_OT_CreateEmpty,
    AE2BLEND_OT_CreatePlane,
    AE2BLEND_OT_CreateCamera,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
