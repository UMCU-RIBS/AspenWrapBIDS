
from typing import TYPE_CHECKING
from bidsbuilder.modules.dataset_core import DatasetCore

if TYPE_CHECKING:
    from bidsbuilder.bidsDataset import BidsDataset

def schema():
    return notImplemented()

def dataset(core:'DatasetCore') -> 'BidsDataset':
    return core._dataset

def subject():
    return notImplemented()

def path(core:DatasetCore) -> str:
    return core._tree_link.relative_path

def entities(core:DatasetCore):
    return
    return notImplemented()

def datatype(core:DatasetCore):
    return
    return notImplemented()

def suffix(core:DatasetCore):
    return
    return notImplemented()

def extension(core:DatasetCore):
    return
    return notImplemented()

def modality():
    return notImplemented()

def sidecar():
    return notImplemented()

def associations():
    return notImplemented()

def columns():
    return notImplemented()

def json(core:DatasetCore):
    """   NOT YET COMPLETED NEED TO MAKE A MORE ROBUST METHOD
    WHICH TAKES INTO ACCOUNT THE INHERITANCE PRINCIPLE IN ORDER TO COLLECT ALL METADATA
    """
    from ..modules.json_files import JSONfile
    assert isinstance(core, JSONfile), f"given core: {core} was not a JSON\n update fields_funcs.json to use inheritance principle"
    return core

def gzip():
    return notImplemented()

def nifti_header():
    return notImplemented()

def ome():
    return notImplemented()

def tiff():
    return notImplemented() 

__all__ = ["schema","dataset","subject","path","entities","datatype","suffix","extension","modality",
           "sidecar","associations","columns","json","gzip","nifti_header","ome","tiff"]

def notImplemented(*args, **kwargs):
    raise NotImplementedError()

#
# The context provides the namespaces available to rules.
# These namespaces are used by selectors to define the scope of application
# for a rule, as well as assertions, to determine whether the rule is satisfied.
#
# Not all components of the context will be defined; for example a NIfTI header
# will only be defined when examining a NIfTI file.
#
# The dataset namespace is constructed once and is available when visiting all
# files.
#
# The subject namespace is constructed once per subject, and is available when
# visiting all files within that subject.
#
# All other (current) namespaces are defined on individual files.
# Sidecar metadata and file associations are built according to the inheritance
# principle.
#
"""
type: object
required:
  - schema
  - dataset
  - path
  - size
  - sidecar
  - associations
additionalProperties: false
properties:
  schema:
    description: 'The BIDS specification schema'
    type: object
  dataset:
    description: 'Properties and contents of the entire dataset'
    type: object
    required:
      - dataset_description
      - tree
      - ignored
      - datatypes
      - modalities
      - subjects
    additionalProperties: false
    properties:
      dataset_description:
        description: 'Contents of /dataset_description.json'
        type: object
      tree:
        description: 'Tree view of all files in dataset'
        type: object
      ignored:
        description: 'Set of ignored files'
        type: array
        items:
          type: string
      datatypes:
        description: 'Data types present in the dataset'
        type: array
        items:
          type: string
      modalities:
        description: 'Modalities present in the dataset'
        type: array
        items:
          type: string
      subjects:
        description: 'Collections of subjects in dataset'
        type: object
        required:
          - sub_dirs
        additionalProperties: false
        properties:
          sub_dirs:
            description: 'Subjects as determined by sub-* directories'
            type: array
            items:
              type: string
          participant_id:
            description: 'The participant_id column of participants.tsv'
            type: array
            items:
              type: string
          phenotype:
            description: 'The union of participant_id columns in phenotype files'
            type: array
            items:
              type: string
  subject:
    description: 'Properties and contents of the current subject'
    type: object
    required:
      - sessions
    additionalProperties: false
    properties:
      sessions:
        description: 'Collections of sessions in subject'
        type: object
        required:
          - ses_dirs
        additionalProperties: false
        properties:
          ses_dirs:
            description: 'Sessions as determined by ses-* directories'
            type: array
            items:
              type: string
          session_id:
            description: 'The session_id column of sessions.tsv'
            type: array
            items:
              type: string
          phenotype:
            description: 'The union of session_id columns in phenotype files'
            type: array
            items:
              type: string

  # Properties of the current file
  path:
    description: 'Path of the current file'
    type: string
  size:
    description: 'Length of the current file in bytes'
    type: integer
  entities:
    description: 'Entities parsed from the current filename'
    type: object
    additionalProperties:
      type: string
  datatype:
    description: 'Datatype of current file, for examples, anat'
    type: string
  suffix:
    description: 'Suffix of current file'
    type: string
  extension:
    description: 'Extension of current file including initial dot'
    type: string
  modality:
    description: 'Modality of current file, for examples, MRI'
    type: string

  sidecar:
    description: 'Sidecar metadata constructed via the inheritance principle'
    type: object
  associations:
    # Note that this is not intended to be an exhaustive list of associated files
    # or to expose every attribute of those files. It is specifically those files
    # and attributes for which a rule needs to be applied from an originating file.
    description: |
      Associated files, indexed by suffix, selected according to the inheritance principle
    type: object
    additionalProperties: false
    properties:
      events:
        description: 'Events file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated events file'
            type: string
          onset:
            description: 'Contents of the onset column'
            type: array
            items:
              type: string
      aslcontext:
        description: 'ASL context file'
        type: object
        required: [path, n_rows]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated aslcontext file'
            type: string
          n_rows:
            description: 'Number of rows in aslcontext.tsv'
            type: integer
          volume_type:
            description: 'Contents of the volume_type column'
            type: array
            items:
              type: string
      m0scan:
        description: 'M0 scan file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated M0 scan file'
            type: string
      magnitude:
        description: 'Magnitude image file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated magnitude file'
            type: string
      magnitude1:
        description: 'Magnitude1 image file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated magnitude1 file'
            type: string
      bval:
        description: 'B value file'
        type: object
        required: [path, n_cols, n_rows, values]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated bval file'
            type: string
          n_cols:
            description: 'Number of columns in bval file'
            type: integer
          n_rows:
            description: 'Number of rows in bval file'
            type: integer
          values:
            description: 'B-values contained in bval file'
            type: array
            items:
              type: number
      bvec:
        description: 'B vector file'
        type: object
        required: [path, n_cols, n_rows]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated bvec file'
            type: string
          n_cols:
            description: 'Number of columns in bvec file'
            type: integer
          n_rows:
            description: 'Number of rows in bvec file'
            type: integer
      channels:
        description: 'Channels file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated channels file'
            type: string
          type:
            description: 'Contents of the type column'
            type: array
            items:
              type: string
          short_channel:
            description: 'Contents of the short_channel column'
            type: array
            items:
              type: string
          sampling_frequency:
            description: 'Contents of the sampling_frequency column'
            type: array
            items:
              type: string
      coordsystem:
        description: 'Coordinate system file'
        type: object
        required: [path]
        additionalProperties: false
        properties:
          path:
            description: 'Path to associated coordsystem file'
            type: string
  # The following properties are populated if the current file is of an appropriate type
  columns:
    description: 'TSV columns, indexed by column header, values are arrays with column contents'
    type: object
    additionalProperties:
      type: array
      items:
        type: string
  json:
    description: 'Contents of the current JSON file'
    type: object
  gzip:
    description: 'Parsed contents of gzip header'
    type: object
    required: [timestamp]
    additionalProperties: false
    properties:
      timestamp:
        description: 'Modification time, unix timestamp'
        type: number
      filename:
        description: 'Filename'
        type: string
      comment:
        description: 'Comment'
        type: string
  nifti_header:
    name: 'NIfTI Header'
    description: 'Parsed contents of NIfTI header referenced elsewhere in schema.'
    type: object
    required:
      - dim_info
      - dim
      - pixdim
      - shape
      - voxel_sizes
      - xyzt_units
      - qform_code
      - sform_code
    additionalProperties: false
    properties:
      dim_info:
        name: 'Dimension Information'
        description: 'Metadata about dimensions data.'
        type: object
        required: [freq, phase, slice]
        additionalProperties: false
        properties:
          freq:
            name: 'Frequency'
            description: 'These fields encode which spatial dimension (1, 2, or 3).'
            type: integer
          phase:
            name: 'Phase'
            description: 'Corresponds to which acquisition dimension for MRI data.'
            type: integer
          slice:
            name: 'Slice'
            description: 'Slice dimensions.'
            type: integer
      dim:
        name: 'Data Dimensions'
        description: 'Data seq dimensions.'
        type: array
        minItems: 8
        maxItems: 8
        items:
          type: integer
      pixdim:
        name: 'Pixel Dimension'
        description: 'Grid spacings (unit per dimension).'
        type: array
        minItems: 8
        maxItems: 8
        items:
          type: number
      shape:
        name: 'Data shape'
        description: 'Data array shape, equal to dim[1:dim[0] + 1]'
        type: array
        minItems: 0
        maxItems: 7
        items:
          type: integer
      voxel_sizes:
        name: 'Voxel sizes'
        description: 'Voxel sizes, equal to pixdim[1:dim[0] + 1]'
        type: array
        minItems: 0
        maxItems: 7
        items:
          type: number
      xyzt_units:
        name: 'XYZT Units'
        description: 'Units of pixdim[1..4]'
        type: object
        required: [xyz, t]
        additionalProperties: false
        properties:
          xyz:
            name: 'XYZ Units'
            description: 'String representing the unit of voxel spacing.'
            type: string
            enum:
              - $ref: objects.enums.unknown.value
              # TODO: Add definitions for these values. (perhaps don't specify)
              - 'meter'
              - 'mm'
              - 'um'
          t:
            name: 'Time Unit'
            description: 'String representing the unit of inter-volume intervals.'
            type: string
            enum:
              - $ref: objects.enums.unknown.value
              # TODO: Add definitions for these values. (perhaps don't specify)
              - 'sec'
              - 'msec'
              - 'usec'
      qform_code:
        name: 'qform code'
        description: 'Use of the quaternion fields.'
        type: integer
      sform_code:
        name: 'sform code'
        description: 'Use of the affine fields.'
        type: integer
      mrs:
        name: 'NIfTI-MRS extension'
        description: 'NIfTI-MRS JSON fields'
        type: object
  ome:
    name: 'Open Microscopy Environment fields'
    description: 'Parsed contents of OME-XML header, which may be found in OME-TIFF or OME-ZARR files'
    type: object
    additionalProperties: false
    properties:
      PhysicalSizeX:
        name: 'PhysicalSizeX'
        description: 'Pixels / @PhysicalSizeX'
        type: number
      PhysicalSizeY:
        name: 'PhysicalSizeY'
        description: 'Pixels / @PhysicalSizeY'
        type: number
      PhysicalSizeZ:
        name: 'PhysicalSizeZ'
        description: 'Pixels / @PhysicalSizeZ'
        type: number
      PhysicalSizeXUnit:
        name: 'PhysicalSizeXUnit'
        description: 'Pixels / @PhysicalSizeXUnit'
        type: string
      PhysicalSizeYUnit:
        name: 'PhysicalSizeYUnit'
        description: 'Pixels / @PhysicalSizeYUnit'
        type: string
      PhysicalSizeZUnit:
        name: 'PhysicalSizeZUnit'
        description: 'Pixels / @PhysicalSizeZUnit'
        type: string
  tiff:
    name: 'TIFF'
    description: 'TIFF file format metadata'
    type: object
    required:
      - version
    additionalProperties: false
    properties:
      version:
        name: 'Version'
        description: 'TIFF file format version (the second 2-byte block)'
        type: integer
"""