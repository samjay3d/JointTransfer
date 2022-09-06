from pprint import pprint
import maya.cmds as cmds
from .maya_data import scene_data
import json
import os 

class SceneHandler:
    
    def __init__(self, file_path, use_selection=False) -> None:
        self.file_path = file_path
        self.use_selection = use_selection

    def _file_exists(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"{self.file_path} does not exist")

    def _read(self):
        with open(self.file_path) as f:
            self.imported_data = json.load(f)

    def _write(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.exported_data, f, indent=2)

    def import_scene(self):
        self._file_exists()
        self._read()
        sd = scene_data.SceneData()
        sd.scene_joints = self.imported_data
        sd.set_scene()
    
    def export_scene(self):
        if self.use_selection:
            sel = cmds.ls(sl=True)
            sd = scene_data.SceneData(sel)
        else:
            sd = scene_data.SceneData()
        self.exported_data = sd.to_dict()
        self._write()

    