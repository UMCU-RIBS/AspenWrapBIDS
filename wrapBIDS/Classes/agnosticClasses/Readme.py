import os
from typing import TYPE_CHECKING
from wrapBIDS.Classes.datasetModule import DatasetCore

if TYPE_CHECKING:
    from wrapBIDS.Classes.bidsDataset import BidsDataset

class Readme(DatasetCore):
    def __init__(self, parent:"BidsDataset"):
        self.path = os.path.join(parent.root, "Readme")
        fileExt = [".md", ".txt"]

    def updateVals(self):
        pass
