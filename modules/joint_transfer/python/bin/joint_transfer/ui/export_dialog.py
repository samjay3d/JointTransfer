from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from ..scene_handler import SceneHandler
from . import maya_window
import maya.cmds as cmds

class ExportDialog:
    FILE_FILTERS = "JSON Files (*.json);;All Files (*.*)"
    selected_filter = "JSON Files (*json)"

    def __init__(self, parent=maya_window.maya_main_window()):
        super(ExportDialog, self).__init__(parent)
        self.file_name = ''

    def show_file_select_dialog(self):
        file_name, self.selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                                                "Export file", 
                                                                                "", 
                                                                                self.FILE_FILTERS, 
                                                                                self.selected_filter)
        if file_name:
            self.file_name
            return True

    def prepare(self):
        if cmds.ls(sl=True):
            self.use_selection = bool(cmds.ls(sl=True))


    def start(self):
        if self.prepare():
            success = self.show_file_select_dialog()
            if success:
                scn = SceneHandler(self.file_name, self.use_selection)
                scn.export_scene()

def export_scene():
    diag = ExportDialog()
    diag.start()