from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from ..scene_handler import SceneHandler
from . import maya_window
import maya.cmds as cmds

class ExportDialog(QtWidgets.QDialog):
    FILE_FILTERS = "JSON Files (*.json);;All Files (*.*)"
    selected_filter = "JSON Files (*json)"

    def __init__(self, parent=maya_window.maya_main_window()):
        super().__init__(parent)
        self.file_name = ''

    def show_file_select_dialog(self):
        file_name, self.selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                                                "Export file", 
                                                                                "", 
                                                                                self.FILE_FILTERS, 
                                                                                self.selected_filter)
        if file_name:
            self.file_name = file_name
            return True

    def prepare(self):
        self.use_selection = bool(cmds.ls(sl=True))
        if self.use_selection:
            result = QtWidgets.QMessageBox.question(self, 
                                                   "Selection", 
                                                   "You have selected an object will you like to export your selection?")
            if result == QtWidgets.QMessageBox.StandardButton.No:
                self.use_selection = False
                QtWidgets.QMessageBox.information(self,
                                           "Export",
                                           "Exporting Entire Scene...")
            
                
    def start(self):
        self.prepare()
        success = self.show_file_select_dialog()
        if success:
            scn = SceneHandler(self.file_name, self.use_selection)
            scn.export_scene()

def export_scene():
    diag = ExportDialog()
    diag.start()