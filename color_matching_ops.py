# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from bpy.utils import register_class, unregister_class
from .color_matching import ColorMatching
from .b3d_lib_int.rgb import RGB


class COLORMATCH_OT_add_node(Operator):
    bl_idname = 'colormatch.add_node'
    bl_label = 'Add RGB Node'
    bl_options = {'REGISTER', 'INTERNAL'}

    add_node_id: IntProperty(
        name='NodeId',
        min=0,
        subtype='UNSIGNED',
        default=0
    )

    def execute(self, context):
        # add RGB node to active object - active material
        for object in context.selected_objects[:]:
            if object.active_material:
                if not object.active_material.use_nodes:
                    object.active_material.use_nodes = True
                rgb_node = object.active_material.node_tree.nodes.new(type='ShaderNodeRGB')
                rgb_node.location = (0, 0)
                match_color = ColorMatching.matches()[self.add_node_id][0]
                rgb_match_color = RGB.fromlist(match_color).as_linear()
                rgb_node.outputs[0].default_value = (rgb_match_color[0], rgb_match_color[1], rgb_match_color[2], 1.0)
        return {'FINISHED'}


class COLORMATCH_OT_copy_matches_to_clipboard(Operator):
    bl_idname = 'colormatch.copy_matches_to_clipboard'
    bl_label = 'To Clipboard'
    bl_description = 'Copy search results to clipboard'
    bl_options = {'REGISTER', 'INTERNAL'}

    db: StringProperty(
        name='Db',
        default=''
    )

    def execute(self, context):
        matches_str = ColorMatching.matches_str(context, self.db)
        if matches_str:
            context.window_manager.clipboard = matches_str
        return {'FINISHED'}


class COLORMATCH_OT_color_match(Operator):
    bl_idname = 'colormatch.color_match'
    bl_label = 'Search for closest colors:'
    bl_options = {'REGISTER', 'INTERNAL'}

    db: StringProperty(
        name='Db',
        default=''
    )

    def execute(self, context):
        ColorMatching.clear(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.db:
            return '{CANCELLED}'
        ColorMatching.search_by_rgb(context,
                                    self.db,
                                    RGB.fromlist(context.window_manager.colormatching_vars.source_color),
                                    context.preferences.addons[__package__].preferences.matching_count)
        matches = ColorMatching.matches()
        for i, match in enumerate(matches):
            context.window_manager.colormatching_colors.add()
            matchcolor = RGB.fromlist(match[0]).as_linear()
            context.window_manager.colormatching_colors[i].dest_color[0] = matchcolor[0]
            context.window_manager.colormatching_colors[i].dest_color[1] = matchcolor[1]
            context.window_manager.colormatching_colors[i].dest_color[2] = matchcolor[2]
        # show window
        return context.window_manager.invoke_popup(self, width=700)

    def draw(self, context):
        matches = ColorMatching.matches()
        row = self.layout.split(factor=0.92)
        row.label(text=self.bl_label)
        row.operator('colormatch.copy_matches_to_clipboard', text='', icon='COPYDOWN').db = self.db
        row = self.layout.row().separator()
        row = self.layout.row()
        for i, match in enumerate(matches):
            col = row.column()
            col.label(text='{:<7.2%}'.format(match[2]))
            col.prop(context.window_manager.colormatching_colors[i], 'dest_color', text='')
            col.label(text=match[1][0])
            col.label(text='CMYK ' + match[1][1])
            col.operator('colormatch.add_node').add_node_id = i

    def check(self, context):
        return True

    def cancel(self, context):
        self.execute(context)


def register():
    register_class(COLORMATCH_OT_color_match)
    register_class(COLORMATCH_OT_add_node)
    register_class(COLORMATCH_OT_copy_matches_to_clipboard)


def unregister():
    unregister_class(COLORMATCH_OT_copy_matches_to_clipboard)
    unregister_class(COLORMATCH_OT_add_node)
    unregister_class(COLORMATCH_OT_color_match)
