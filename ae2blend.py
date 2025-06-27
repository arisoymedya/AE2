bl_info = {
    "name": "AE2Blend",
    "author": "AE2Blend Contributors",
    "version": (1, 1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AE2Blend",
    "description": "Manually paste keyframes from After Effects",
    "category": "Animation",
}

import bpy

class AE2BlendProperties(bpy.types.PropertyGroup):
    ae2blend_text: bpy.props.StringProperty(
        name="Keyframe Data",
        description="Paste After Effects keyframe data here (tab-separated)",
        default=""
    )

class AE2BLEND_PT_Panel(bpy.types.Panel):
    bl_label = "AE2Blend"
    bl_idname = "AE2BLEND_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE2Blend"

    def draw(self, context):
        layout = self.layout
        props = context.scene.ae2blend_props
        layout.prop(props, "ae2blend_text", text="Keyframe Data")
        layout.operator("ae2blend.paste_keyframes")
        layout.operator("ae2blend.create_empty")
        layout.operator("ae2blend.create_plane")
        layout.operator("ae2blend.create_camera")

class AE2BLEND_OT_PasteKeyframes(bpy.types.Operator):
    bl_label = "Paste Keyframes"
    bl_idname = "ae2blend.paste_keyframes"
    bl_description = "Paste keyframe data manually"

    def execute(self, context):
        lines = context.scene.ae2blend_props.ae2blend_text.splitlines()
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
    AE2BlendProperties,
    AE2BLEND_PT_Panel,
    AE2BLEND_OT_PasteKeyframes,
    AE2BLEND_OT_CreateEmpty,
    AE2BLEND_OT_CreatePlane,
    AE2BLEND_OT_CreateCamera,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ae2blend_props = bpy.props.PointerProperty(type=AE2BlendProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ae2blend_props

if __name__ == "__main__":
    register()
