# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


import bpy
from .color_matching import ColorMatching
from .color_matching import ColorMatchingStatic


class NCSMatchAddNode(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch_addnode'
    bl_label = 'Add RGB Node'
    bl_options = {'REGISTER', 'INTERNAL'}

    add_node_id = bpy.props.IntProperty(
        name='NodeId',
        min=0,
        max=ColorMatchingStatic.matching_count - 1,
        subtype='UNSIGNED',
        default=0
    )

    def execute(self, context):
        # add RGB node to active object - active material
        if context.selected_objects:
            added = []
            for object in context.selected_objects:
                if object.active_material and object.active_material not in added:
                    if not object.active_material.use_nodes:
                        object.active_material.use_nodes = True
                    rgb_node = object.active_material.node_tree.nodes.new(type='ShaderNodeRGB')
                    rgb_node.location = (0, 0)
                    matches = ColorMatching.matches()
                    rgb_node.outputs[0].default_value = (matches[self.add_node_id][0][0] / 255, matches[self.add_node_id][0][1] / 255, matches[self.add_node_id][0][2] / 255, 1.0)
                    added.append(object.active_material)
        return {'FINISHED'}


class NCSMatchCopyMatchesToClipboard(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch_toclipboard'
    bl_label = 'To Clipboard'
    bl_description = 'Copy search results to clipboard'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        # copy NCS matches string to clipboard
        matches_str = ColorMatching.matches_str()
        if matches_str:
            context.window_manager.clipboard = matches_str
        return {'FINISHED'}


class NCSMatch(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch'
    bl_label = 'Search for closest NCS:'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        ColorMatching.clear()
        return {'FINISHED'}

    def invoke(self, context, event):
        ColorMatching.search_nearest_ncs_by_rgb(context.window_manager.colormatching_vars.source_color, ColorMatchingStatic.matching_count)
        matches = ColorMatching.matches()
        for i, match in enumerate(matches):
            context.window_manager.colormatching_colors.add()
            context.window_manager.colormatching_colors[i].dest_color[0] = match[0][0] / 255
            context.window_manager.colormatching_colors[i].dest_color[1] = match[0][1] / 255
            context.window_manager.colormatching_colors[i].dest_color[2] = match[0][2] / 255
        # show window
        return context.window_manager.invoke_popup(self, width=700)

    def draw(self, context):
        matches = ColorMatching.matches()
        row = self.layout.split(0.92)
        row.label(self.bl_label)
        row.operator('colormatch.ncsmatch_toclipboard', text='', icon='COPYDOWN')
        row = self.layout.row().separator()
        row = self.layout.row()
        for i, match in enumerate(matches):
            col = row.column()
            col.label(str(round(match[2] * 100, 2)) + ' %')
            col.prop(context.window_manager.colormatching_colors[i], 'dest_color', text='')
            col.label(match[1][0])
            col.label('CMYK ' + match[1][1])
            col.operator('colormatch.ncsmatch_addnode').add_node_id = i

    def check(self, context):
        return True

    def cancel(self, context):
        self.execute(context)


def register():
    bpy.utils.register_class(NCSMatch)
    bpy.utils.register_class(NCSMatchAddNode)
    bpy.utils.register_class(NCSMatchCopyMatchesToClipboard)


def unregister():
    bpy.utils.unregister_class(NCSMatchCopyMatchesToClipboard)
    bpy.utils.unregister_class(NCSMatchAddNode)
    bpy.utils.unregister_class(NCSMatch)
