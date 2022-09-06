import sys
import traceback
import maya.api.OpenMaya as om
import joint_transfer 

import importlib
importlib.reload(joint_transfer)

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

def import_dialog():
    try:
        joint_transfer.ui.import_dialog.import_scene()
    except:
        print(traceback.format_exc(), file=sys.stderr)
def export_dialog():
    try:
        joint_transfer.ui.export_dialog.export_scene()
    except:
        print(traceback.format_exc(), file=sys.stderr)

def command_scene_handler(file_path, type, use_selection=False):
    try:
        handler = joint_transfer.scene_handler.SceneHandler(file_path, use_selection)
        if type in 'import':
            handler.import_scene()
        if type in 'export':
            handler.export_scene()
    except:
        print(traceback.format_exc(), file=sys.stderr)
    
class JointImport(om.MPxCommand):
    kPluginCmdName = "jointImport"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return JointImport()

    def doIt(self, arg_list):
        import_dialog()

class JointExport(om.MPxCommand):
    kPluginCmdName = "jointExport"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return JointExport()

    def doIt(self, arg_list):
        export_dialog()


class JointTransfer(om.MPxCommand):
    kPluginCmdName = "jointTransfer"
    kFilePathFlag = "-f"
    kFilePathLongFlag = "-filepath"
    kTypeFlag = "-t"
    kTypeLongFlag = "-type"
    kSelectionFlag = "-sl"
    kSelectionLongFlag = "-selection"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return JointTransfer()

    @staticmethod
    def createSyntax():
        syntax = om.MSyntax()
        syntax.addFlag(JointTransfer.kFilePathFlag, JointTransfer.kFilePathLongFlag, om.MSyntax.kString)
        syntax.addFlag(JointTransfer.kTypeFlag, JointTransfer.kTypeLongFlag, om.MSyntax.kString)
        syntax.addFlag(JointTransfer.kSelectionFlag, JointTransfer.kSelectionLongFlag, om.MSyntax.kBoolean)
        return syntax


    def doIt(self, arg_list):
        try:
            arg_data = om.MArgDatabase(self.syntax(), arg_list)
        except RuntimeError:
            om.MGlobal.displayError('Error while parsing arguments:\n#\t# If passing in list of nodes, also check that node names exist in scene.')
            raise
        
        if arg_data.isFlagSet(JointTransfer.kFilePathFlag):
            file_path =arg_data.flagArgumentString(JointTransfer.kFilePathFlag, 0)
        if arg_data.isFlagSet(JointTransfer.kTypeFlag):
            type = arg_data.flagArgumentString(JointTransfer.kTypeFlag, 0)
        if arg_data.isFlagSet(JointTransfer.kSelectionFlag):
            use_selection = arg_data.flagArgumentBool(JointTransfer.kSelectionFlag, 0)

        command_scene_handler(file_path, type, use_selection)




def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addFlag(JointTransfer.kFilePathFlag, JointTransfer.kFilePathLongFlag, om.MSyntax.kString)
    syntax.addFlag(JointTransfer.kTypeFlag, JointTransfer.kTypeLongFlag, om.MSyntax.kString)
    syntax.addFlag(JointTransfer.kSelectionFlag, JointTransfer.kSelectionFlag, om.MSyntax.kBoolean)
    return syntax

# Initialize the script plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            JointTransfer.kPluginCmdName, JointTransfer.creator, JointTransfer.createSyntax
        )
    except:
        print(f"Failed to register command: {JointTransfer.kPluginCmdName}", file=sys.stderr)
        raise
    try:
        pluginFn.registerCommand(
            JointImport.kPluginCmdName, JointImport.creator
        )
    except:
        print(f"Failed to register command: {JointImport.kPluginCmdName}", file=sys.stderr)
        raise
    try:
        pluginFn.registerCommand(
            JointExport.kPluginCmdName, JointExport.creator
        )
    except:
        print(f"Failed to register command: {JointExport.kPluginCmdName}", file=sys.stderr)
        raise

# Uninitialize the script plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(JointTransfer.kPluginCmdName)
    except:
        print(f"Failed to unregister command: {JointTransfer.kPluginCmdName}", file=sys.stderr)
        raise
    try:
        pluginFn.deregisterCommand(JointImport.kPluginCmdName)
    except:
        print(f"Failed to unregister command: {JointImport.kPluginCmdName}", file=sys.stderr)
        raise
    try:
        pluginFn.deregisterCommand(JointExport.kPluginCmdName)
    except:
        print(f"Failed to unregister command: {JointExport.kPluginCmdName}", file=sys.stderr)
        raise
    