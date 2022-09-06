# JointTransfer
Tool to Simplify Import and Export of Skeletons in Maya.

## Table of Contents
1. [About the tool](#about)
2. [Prerequisites](#prereq)
3. [How to Install](#install)
4. [How to Use](#use)
5. [For Developers](#dev)


## 1. About the tool <a name="about"></a>
This tool will export or import joint information within the scene or your selection. 
Data we export is index order, world position, orientation, and hierarchy.

## 2. Prerequisites <a name="prereq"></a>
* Maya Version
  * Maya 2022 and Up

## 3. How to Install <a name="install"></a>
1. Download newest release from github.
2. Export Zip files contents to your module folder. 
   * Example location : C:\Users\USER_NAME\Documents\maya\2022\modules
3. If maya is open restart the software.
4. Once maya is opened a new shelf should be added called "Joint_Transfer"

## 4. How to Use <a name="use"></a>

<img style="float: right;" src="/modules/joint_transfer/maya/icons/icon_import-01.svg" width="200">

### i. How to Import

   1. If you haven't already install the module.
   2. Select the custom shelf "Joint_Transfer"
   3. Select the the import button. 
   4. If changes exists in the scene a warning will appear. Recommended workflow is to use a new scene or save scene first.
   5. A window will pop up choose your json file containing exported data.
   
<img style="float: right;" src="/modules/joint_transfer/maya/icons/icon_export-01.svg" width="200">

### ii. How to Export

   1. If you haven't already install the module.
   2. Select the custom shelf "Joint_Transfer"
   3. Select the the export button. 
   4. If Joint is selected option will pop up to export only selection. If you select no the entire scene will be exported.
   5. A window will pop up choose your json file location. 
   6. Export will be saved to your specified location.

## 5. For Developers <a name="dev"></a>
This tool was made in mind if we wish to automate it. While the option to choose your selection or warn the user if changes exists is helpful. It makes it hard to batch through existing files. 

To handle this the entire tool is accessed through custom maya commands.

1. Import Command
   ```python
   cmds.jointImport() # this is the user version where we get the pop ups
   ```
2. Export Command
   ```python
   cmds.jointExport() # this is the user version where we get the pop ups
   ```
3. JointTransfer 
   ```python
   """
   Args: 
     filepath or f (str) - specify location to export or import
     type or t (str) - takes either import or export to specify type of operation.
     selection or sl (bool) - specify if you wish to use selection or use the entire scene.
   """
   cmds.jointTransfer(filepath="\dev\export.json", type="import", selection=True)
   ```

