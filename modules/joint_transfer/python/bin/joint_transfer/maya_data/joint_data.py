from __future__ import annotations
from dataclasses import dataclass
from typing import List
import maya.cmds as cmds


@dataclass
class JointData:
    name: str
    _index_order : str = None
    _world_position : List[float] = None
    _orientation : List[float] = None
    _children: List[JointData] = None
    _parent: JointData = None

    @property
    def index_order(self):
        if self._index_order is None:
            self._index_order = cmds.joint(self.name, q=True, roo=True)
        return self._index_order
    
    @index_order.setter
    def index_order(self, value):
        self._index_order = value

    @property
    def world_position(self):
        if self._world_position is None:
            self._world_position = cmds.joint(self.name, q=True, a=True)
        return self._world_position
    
    @world_position.setter
    def world_position(self, value):
        self._world_position = value

    @property
    def orientation(self):
        if self._orientation is None:
            self._orientation = cmds.joint(self.name, q=True, o=True)
        return self._orientation
    
    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    @property
    def children(self):
        if self._children is None:
            tmp = cmds.listRelatives(self.name, type='joint', c=True)
            if tmp:
               self._children = [JointData(j) for j in tmp]
        return self._children

    @children.setter
    def children(self, value: List[JointData]):
        self._children = value

    @property       
    def parent(self):
        if self._parent is None:
            tmp = cmds.listRelatives(self.name, type='joint', p=True)
            self._parent = JointData(tmp[0]) if tmp else None 
        return self._parent
    
    @parent.setter
    def parent(self, value: JointData):
        self._parent = value
        
    def _get_all_parents(self, 
                         parent: JointData, 
                         joints: List[JointData]) -> List[JointData]:
        if parent:
            joints.append(parent)
        if parent.parent:
            self._get_all_parents(parent.parent, joints)
        return joints

    def _get_all_children(self, 
                          children: List[JointData], 
                          joints: List[JointData]) -> List[JointData]:
        for c in children:
            if c:
                joints.append(c)
            if c.children:
                self._get_all_children(c.children, joints)
        return joints


    def get_all_joints(self) -> List[JointData]:
        """
        Recursively search the JointData and collect all parents and children
        """
        joints = [self]
        if self.parent:
            self._get_all_parents(self.parent, joints)
        if self.children:
            self._get_all_children(self.children, joints)
        return joints
    
    @classmethod
    def from_dict(cls, jnt_dict: dict, parent=None) -> JointData:
        """
        Applies Dictionary to Joint data
        """
        children_jnt = []
        for k, v in jnt_dict.items():
            jnt = JointData(k)
            jnt.parent = parent
            jnt.index_order = v.get('index_order')
            jnt.world_position = v.get('world_position')
            jnt.orientation = v.get('orientation')
            if v.get('children'):
                children = cls.from_dict(v.get('children'), parent=jnt)
                jnt.children = children
            if jnt.parent is None:
                return jnt # end the loop and return the top node 
            else:
                children_jnt.append(jnt)
        return children_jnt # return the children to add to the top node

    def _find_item(self, obj, key):
        if key in obj: return obj
        for k, v in obj.items():
            if isinstance(v,dict):
                item = self._find_item(v, key)
                if item is not None:
                    return item

    def to_dict(self) -> dict:
        jnts = self.get_all_joints() 
        jnt_dict = {}
        for j in jnts:
            if j.parent:
                relative_dict = self._find_item(jnt_dict, j.parent.name)
                parent_dict = relative_dict[j.parent.name]
                if 'children' not in parent_dict.keys():
                    parent_dict['children'] = {}

                parent_dict['children'][j.name] = {
                    "index_order" : j.index_order,
                    "world_position" : j.world_position,
                    "orientation" : j.orientation
                }

            else:
                jnt_dict[self.name] = {
                    "index_order" : j.index_order,
                    "world_position" : j.world_position,
                    "orientation" : j.orientation
                }
        return jnt_dict

    def _check_exists(self, name):
        """
        Check if object already exists and update name if it does.
        """
        if cmds.objExists(name):
            return self._check_exists(name + '_1')
        return name

    def set_joints(self):
        jnts = self.get_all_joints() 
        for j in jnts:
            cmds.select(d=True)
            j.name = self._check_exists(j.name)
            cmds.joint(n=j.name, roo=j.index_order, 
                       a=True, p=j.world_position, 
                       o=j.orientation)
            if j.parent:
                cmds.parent(j.name, j.parent.name, a=True)