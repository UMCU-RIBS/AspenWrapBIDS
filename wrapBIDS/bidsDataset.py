import bidsschematools, bidsschematools.schema

from pathlib import Path

from wrapBIDS.modules import *
from wrapBIDS.util.util import checkPath, isDir, clearSchema
from wrapBIDS.util.datasetTree import FileTree
from wrapBIDS.modules.commonFiles import resolveCoreClassType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import MutableMapping 

class BidsDataset():
    initialised = False
    schema = bidsschematools.schema.load_schema()
    schema.pop("meta")

    def __init__(self, root:str = Path.cwd()):
        self.children = {}
        self.root = root
        self.tree = FileTree(_name=root, link=self, parent=None)
        DatasetCore.dataset = self
        
        self._make_skeletonBIDS()
        self._interpret_skeletonBIDS()

    def _make_skeletonBIDS(self):

        #Exceptions for scans, sessions and phenotype
        exceptions = ["scans", "sessions", "phenotype"]

        def _pop_from_schema(schema:'MutableMapping'):
            toPop = []
            for file in schema.keys():
                if file in exceptions:
                    continue
                is_dir = isDir(self.schema.rules.directories.raw, file)
                tObj = resolveCoreClassType(**schema[file]._properties, is_dir=is_dir)
                #NEED TO UPDATE IT TO GIVE THE NAME RATHER THAN THE STEM
                self.tree.addPath(tObj.name, tObj, is_dir)
                toPop.append(file)

            for key in toPop:
                schema.pop(key)
                
        _pop_from_schema(self.schema.rules.files.common.core)
        clearSchema(self.schema.rules.files.common, "core")

        _pop_from_schema(self.schema.rules.files.common.tables)
        clearSchema(self.schema.rules.files.common, "tables")

        print(self.tree.children)
            
        return

    def _interpret_skeletonBIDS(self):
        
        return

    def make(self, force=False):
        self._removeRedundant()
        
        exists, msg = checkPath(self.root)
        if not exists:
            raise FileExistsError(msg)
        
        for child in self.children:
            child.createBIDS()
        return
    
    def _removeRedundant(self):
        for child in self.children:
            if child:
                child._removeRedundant()
            else:
                child._deleteSelf()
                #consider using __del__ method in order to just call pop. Concerns around whether the garbage collection always occurs

                self.children.pop(child)



    def read(self, path:str = None):
        if path:
            self.root = path

        exists, msg = checkPath(self.root)
        if not exists():
            raise FileExistsError(msg)
        

        """
        do some stuff
        """

        self.initialised = True
        
    """"
    reading files
        -tsv
        -json

    data specific       -sql queries
        -mne.io.raw
    """

if __name__ == "__main__":
    test = BidsDataset()