author = '__Rigardo__'

"""
Basic set of functions to implement inside Maya world.
"""

# System Imports.
import os, sys

# Maya Imports.
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from pymel.core.general import PyNode as pyNode

# Import Qt class object current version.
try:
  from PySide2.QtCore import * 
  from PySide2.QtGui import * 
  from PySide2.QtWidgets import *
  from PySide2.QtUiTools import *
  from shiboken2 import wrapInstance 

except ImportError:
  from PySide.QtCore import * 
  from PySide.QtGui import * 
  from PySide.QtUiTools import *
  from shiboken import wrapInstance 


# Custom Classes Related to Maya. --------------------------------------------
class MayaFunctions(object):
    """Main Maya utilities functions class"""
    def __init__(self):
        super( MayaFunctions, self ).__init__()
        self.mayaVersion = mc.about( version=True )
        print 'Initiliazing Maya functions class!'


    @staticmethod
    def unique_name(name):
        """
        Sinopsis:
            - Check if the name has a suffix to set the name whit it.
            - If not just rename whit index.
        SYNTAX:
            unique_name(<str(name)>)
        RETURN:
            New index name.
        """
   
        # Process.
        if '_' in name:
            name, suffix = name.rsplit('_', 1)
            counter      = 1
            newName = '{0}_0{1}_{2}'.format(name, counter, suffix)        

            while mc.objExists(newName):
                counter +=1
                newName = '{0}_0{1}_{2}'.format(name, counter, suffix)
            return str(newName)
                
        else:
            counter = 1
            newName = '{0}_0{1}'.format(name, counter)
            
            while mc.objExists(newName):
                counter +=1
                newName = '{0}_0{1}'.format(name, counter)
        
        return str(newName)


    @staticmethod
    def add_offset_transform(nodes=None, offsetGroups=1, suffix='offset'):
        """
        Sinopsis:
            Adds Zero Transformations to a given node.
        SYNTAX:
            addoffset (<nodes=String>)
        RETURN:
            offset=String :: A String containing the Zero Transform node name.
        """

        # Selection checks.
        if not nodes:
            nodes = pm.ls(selection=True)
            if not nodes:
                om.MGlobal.displayError('No selection.')
                return
                
        # For each selected node(s) create the offsets transform node(s).
        offsetNodes = []
        for node in nodes:
            nodeParent = node.getParent()
            nodesGrp = []
            for index in reversed(xrange(offsetGroups)):
                offsetNode = pm.createNode('transform', name=MayaFunctions.unique_name(node.name() + '_0{}_'.format(index) +suffix))
                offsetNode.setMatrix(node.getMatrix())
                offsetNodes.append(offsetNode)

                if len(nodesGrp) == 0:
                    if (nodeParent != None):
                        pm.parent(offsetNode, nodeParent)
                else:
                    pm.parent(offsetNode, nodesGrp[-1])
                    

                nodesGrp.append(offsetNode)

            # Parent the node to the last offset group
            pm.parent(node, nodesGrp[-1])

        return sorted(offsetNodes)


    @staticmethod
    def set_non_user_attributes(nodes=[], attributes=[]):
        """
        Sinopsis:
            - Lock for given node(s) the argument attributes.
            - If not just rename whit index.

        SYNTAX:
            set_non_user_attributes(['locator1', 'pSphere1'], attributes=['.tx', '.ty', '.tz'])

        """
        # Main loop to lock the given attributes.
        if len(nodes)>0:
            for node in nodes:
                node = pyNode(node)
                for attr in attributes:
                    pm.setAttr(node + attr, lock=True, channelBox=False, keyable=False)


    @staticmethod
    def color_to_curve(objects=None, color=4):
        """
        Sinopsis:
            Adds Zero Transformations to a given node.
        SYNTAX:
            addoffset (<nodes=String>)
        RETURN:
            offset=String :: A String containing the Zero Transform node name.
        """

        #Controls default color List.
        black  = 1
        blue   = 6
        red    = 13
        green  = 14
        yellow = 17

        # Selection checks.
        if not objects:
            objects = pm.ls(selection=True)
            if not objects:
                om.MGlobal.displayError('No object was specified or selected. Failed to continue.')
                return
        
        #Set the color to the shapes of the given object(s)
        for node in objects:
            if node.type() == 'transform':
                if node.getShape().type() == 'nurbsCurve':
                    node.getShape().overrideEnabled.set(True)
                    node.getShape().overrideColor.set(color)
                    continue

            elif node.type() == 'nurbsCurve':
                node.overrideEnabled.set(True)
                node.overrideColor.set(color)