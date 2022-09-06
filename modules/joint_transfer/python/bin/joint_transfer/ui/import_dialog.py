from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from ..scene_handler import SceneHandler
from . import maya_window
import maya.cmds as cmds

class ImportDialog:
    FILE_FILTERS = "JSON Files (*.json);;All Files (*.*)"
    selected_filter = "JSON Files (*json)"

    def __init__(self, parent=maya_window.maya_main_window()):
        super(ImportDialog, self).__init__(parent)
        self.file_name = ''

    def show_file_select_dialog(self):
        file_name, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                                "Select file", 
                                                                                "", 
                                                                                self.FILE_FILTERS, 
                                                                                self.selected_filter)
        if file_name:
            self.file_name
            return True

    def check_for_changes(self):
        if cmds.file(q=True, modified=True): #check if file is modified and not selected force
            result = QtWidgets.QMessageBox.warning(self, 
                                                   "Modified", 
                                                   "Importing into an existing scene could have issues\n Are you sure you wish to continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                return True


    def start(self):
        if self.check_for_changes():
            success = self.show_file_select_dialog()
            if success:
                scn = SceneHandler(self.file_name)
                scn.import_scene()


def import_scene():
    diag = ImportDialog()
    diag.start()