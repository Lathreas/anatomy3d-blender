import bpy

class ARF_OT_Armature_Mode(bpy.types.Operator):
    bl_label = "Armature Mode"
    bl_idname = "arf.armature_mode"

    def execute(self, context):
        for obj in context.scene.objects:
            if (obj.type == "ARMATURE"):
                obj.hide_set(False)
            else:
                obj.hide_set(True)
        return {'FINISHED'}


class ARF_OT_Skeleton_Mode(bpy.types.Operator):
    bl_label = "Skeleton Mode"
    bl_idname = "arf.skeleton_mode"

    def execute(self, context):
        for obj in context.scene.objects:
            if (obj.ARF.object_type == "BONE"):
                obj.hide_set(False)
            elif (obj.ARF.object_type != "NONE"):
                obj.hide_set(True)
        return {'FINISHED'}


class ARF_OT_Smart_Object_Mode(bpy.types.Operator):
    bl_label = "Smart Object Mode"
    bl_idname = "arf.smart_object_mode"

    def execute(self, context):
        # First check if we selected at least one object.
        # To not hide all objects by mistake.
        if context.selected_objects == []:
            return {'FINISHED'}

        selected = context.selected_objects
        # Then, hide all objects
        for obj in context.scene.objects:
            obj.hide_set(True)

        # Now get all objects tied to geom nodes tied to the selected object to unhide those
        for selection in selected:
            for modifier in selection.modifiers:
                if modifier.type != 'NODES':
                    continue
                # Disabled geom node modifiers sometimes do not contain a node_group
                if (modifier.node_group == None):
                    continue

                for input in modifier.node_group.inputs:
                    if not (isinstance(input, bpy.types.NodeSocketInterfaceObject)):
                        continue

                    # For some reason input.default_value is a copy of the object and not the actual
                    # object in the scene, so we need to get the actual object in the scene.
                    inputobj = bpy.context.scene.objects.get(input.default_value.name)
                    inputobj.hide_set(False)
                    # We also need to set every parent to also be visible
                    parent = inputobj.parent
                    while (parent != None):
                        parent.hide_set(False)
                        parent = parent.parent

            # Now unhide the object itself
            selection.hide_set(False)
            # If the selection has any parents they must also be made visible to undo
            # hiding all objects so the selection can be seen
            parent = selection.parent
            while (parent != None):
                parent.hide_set(False)
                parent = parent.parent
        return {'FINISHED'}


class ARF_OT_Muscle_Mode(bpy.types.Operator):
    bl_label = "Muscle Mode"
    bl_idname = "arf.muscle_mode"

    def execute(self, context):
        for obj in context.scene.objects:
            if (obj.ARF.object_type == "MUSCLE" or obj.ARF.object_type == "BONE"):
                obj.hide_set(False)
            elif (obj.ARF.object_type != "NONE"):
                obj.hide_set(True)
        return {'FINISHED'}


class ARF_OT_Skin_Mode(bpy.types.Operator):
    bl_label = "Skin Mode"
    bl_idname = "arf.skin_mode"

    def execute(self, context):
        for obj in context.scene.objects:
            if (obj.ARF.object_type == "SKIN"):
                obj.hide_set(False)
            elif (obj.ARF.object_type != "NONE"):
                obj.hide_set(True)
        return {'FINISHED'}


# A submenu with just the mode select options.
# In case this is needed by any other classes.
class ARF_MT_Mode_Select_Submenu(bpy.types.Menu):
    bl_label = "Mode Select Submenu"
    bl_idname = "ARF_MT_Mode_Select_Submenu"

    def draw(self, context):
        layout = self.layout
        layout.operator("arf.smart_object_mode")
        layout.operator("arf.armature_mode")
        layout.operator("arf.skeleton_mode")
        layout.operator("arf.muscle_mode")
        layout.operator("arf.skin_mode")


# The core ARF menu. When more options besides
# mode selection are desired this should be moved to its own class
# probably
class ARF_MT_ARF_Menu(bpy.types.Menu):
    bl_label = "ARF"
    bl_idname = "ARF_MT_ARF_Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("arf.smart_object_mode")
        layout.operator("arf.armature_mode")
        layout.operator("arf.skeleton_mode")
        layout.operator("arf.muscle_mode")
        layout.operator("arf.skin_mode")
        # If mode options are desired in a submenu instead this can be uncommented
        # layout.menu("ARF_MT_Mode_Select_Submenu", icon="COLLAPSEMENU")

    def execute(self, context):
        print("Executing context ")

        return {'FINISHED'}


def draw_item(self, context):
    layout = self.layout
    layout.menu(ARF_MT_ARF_Menu.bl_idname)


def register():
    bpy.utils.register_class(ARF_OT_Armature_Mode)
    bpy.utils.register_class(ARF_OT_Skeleton_Mode)
    bpy.utils.register_class(ARF_OT_Smart_Object_Mode)
    bpy.utils.register_class(ARF_OT_Muscle_Mode)
    bpy.utils.register_class(ARF_OT_Skin_Mode)
    bpy.utils.register_class(ARF_MT_Mode_Select_Submenu)
    bpy.utils.register_class(ARF_MT_ARF_Menu)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_item)


def unregister():
    bpy.utils.unregister_class(ARF_OT_Armature_Mode)
    bpy.utils.unregister_class(ARF_OT_Skeleton_Mode)
    bpy.utils.unregister_class(ARF_OT_Smart_Object_Mode)
    bpy.utils.unregister_class(ARF_OT_Muscle_Mode)
    bpy.utils.unregister_class(ARF_OT_Skin_Mode)
    bpy.utils.unregister_class(ARF_MT_Mode_Select_Submenu)
    bpy.utils.unregister_class(ARF_MT_ARF_Menu)
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_item)


if __name__ == "__main__":
    register()
