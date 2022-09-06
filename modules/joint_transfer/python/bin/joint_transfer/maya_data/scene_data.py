from . import joint_data
from typing import List
import maya.cmds as cmds

class SceneData:
    """
    Used to query and edit selection or entire scene for specific maya types

    This is used as place holder if any other data would be necessary to store in the future.
    eg.
    get_shape_data
    get_curve_data
    ...
    etc
    """
    def __init__(self, active_selection=None) -> None:
        self.active_selection = active_selection    
        self._scene_joints = None

    def get_top_node(self, node: str, type: str) -> str:
        """
        Cycle through node until the top node is found
        If no parent is found return passed node.
        """
        parent = cmds.listRelatives(node, p=True, typ=type)
        if parent:
            return self.get_top_node(parent[0], type)
        if parent is None:
            return node

    @property
    def scene_joints(self) -> List[joint_data.JointData]:
        if self._scene_joints is None:
            self._scene_joints = self._get_joint_data()
        return self._scene_joints

    @scene_joints.setter
    def scene_joints(self, scene_dict: dict):
        self._scene_joints = self._set_joint_data(scene_dict)

    def _get_joint_data(self) -> List[joint_data.JointData]:
        """
        Based on selection or Entire Scene find joint hierachies at the root.
        """
        nodes = []
        if self.active_selection:
            nodes.extend(self.active_selection)
        else:
            nodes.extend(cmds.ls(type='joint'))
        parent_joints = set()
        for n in nodes:
            parent_joints.add(self.get_top_node(n, 'joint'))

        joints = []
        for p in parent_joints:
            joints.append(joint_data.JointData(p))
        
        return joints

    def _set_joint_data(self, scene_dict) -> List[joint_data.JointData]:
        jnt_data = []
        if 'Scene' in scene_dict:
            if 'Joints' in scene_dict['Scene']:
                jnt_data = scene_dict['Scene']['Joints']
        if not jnt_data:
            return
        jnt_instances = []
        for jnt in jnt_data:
            jnt_instances.append(joint_data.JointData.from_dict(jnt))
        return jnt_instances


    def to_dict(self) -> dict:
        jnts = self.scene_joints
        scene = {'Scene' : {'Joints' : []}}
        for j in jnts:
            scene['Scene']['Joints'].append(j.to_dict())
        
        return scene

    def set_scene(self):
        """
        Will Apply Scene Data to Maya Scene
        """
        for jnt in self.scene_joints:
            jnt.set_joints()