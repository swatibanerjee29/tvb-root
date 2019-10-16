import uuid

import typing
import os.path
import abc
import numpy

from tvb.core.entities.file.hdf5_storage_manager import HDF5StorageManager
from tvb.basic.neotraits.api import HasTraits, Attr, NArray


def is_scalar_type(t):
    return (
        t in [bool, ] or
        issubclass(t, basestring) or
        numpy.issubdtype(t, numpy.number)
    )


class Accessor(object):
    def __init__(self, trait_attribute, h5file):
        # type: (Attr, H5File) -> None
        """
        :param trait_attribute: A traited attribute declared in a HasTraits class
        :param h5file: the parent h5 file
        """
        self.owner = h5file
        self.trait_attribute = trait_attribute

    @abc.abstractmethod
    def load(self):
        pass

    @abc.abstractmethod
    def store(self, val):
        pass



class Scalar(Accessor):
    """
    A scalar in a h5 file that corresponds to a traited attribute.
    Serialized as a global h5 attribute
    """

    def store(self, val):
        # type: (typing.Union[str, int, float]) -> None
        self.trait_attribute._validate_set(None, val)
        self.owner.storage_manager.set_metadata({self.trait_attribute.field_name: val})

    def load(self):
        # type: () -> typing.Union[str, int, float]
        return self.owner.storage_manager.get_metadata()[self.trait_attribute.field_name]



class DataSet(Accessor):
    """
    A dataset in a h5 file that corresponds to a traited NArray.
    """
    def __init__(self, trait_attribute, h5file, expand_dimension=None):
        # type: (NArray, H5File, int) -> None
        """
        :param trait_attribute: A traited attribute declared in a HasTraits class
        :param h5file: the parent h5 file
        :param expand_dimension: An int designating a dimension of the array that may grow.
        """
        super(DataSet, self).__init__(trait_attribute, h5file)
        self.expand_dimension = expand_dimension

    def append(self, data, close_file=True):
        # type: (numpy.ndarray, bool) -> None
        self.owner.storage_manager.append_data(
            self.trait_attribute.field_name,
            data,
            grow_dimension=self.expand_dimension,
            close_file=close_file
        )

    def store(self, data):
        # type: (numpy.ndarray) -> None
        self.trait_attribute._validate_set(None, data)
        self.owner.storage_manager.store_data(self.trait_attribute.field_name, data)

    def load(self):
        # type: () -> numpy.ndarray
        return self.owner.storage_manager.get_data(self.trait_attribute.field_name)

    def __getitem__(self, data_slice):
        # type: (slice) -> numpy.ndarray
        return self.owner.storage_manager.get_data(self.trait_attribute.field_name, data_slice)

    @property
    def shape(self):
        # type: () -> int
        return self.owner.storage_manager.get_data_shape(self.trait_attribute.field_name)


class Reference(Scalar):
    """
    A reference to another h5 file
    Corresponds to a contained datatype
    """
    def store(self, val):
        # type: (HasTraits) -> None
        """
        The reference is stored as a gid in the metadata.
        :param val: a datatype
        todo: This is not consistent with load. Load will just return the gid.
        """
        if not isinstance(val, HasTraits):
            raise TypeError("expected HasTraits, got {}".format(type(val)))
        # urn is a standard encoding, that is obvious an uuid
        # str(gid) is more ambiguous
        val = val.gid.urn
        self.owner.storage_manager.set_metadata({self.trait_attribute.field_name: val})

    def load(self):
        urngid = super(Reference, self).load()
        return uuid.UUID(urngid)



class H5File(object):

    def __init__(self, path):
        # type: (str) -> None
        storage_path, file_name = os.path.split(path)
        self.storage_manager = HDF5StorageManager(storage_path, file_name)
        # would be nice to have an opened state for the chunked api instead of the close_file=False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # write_metadata  creation time, serializer class name, etc
        self.storage_manager.set_metadata({
            'written_by': self.__class__.__module__ + '.' + self.__class__.__name__,
        })
        self.storage_manager.close_file()


    def store(self, datatype):
        # type: (HasTraits) -> None
        for name, accessor in self.__dict__.iteritems():
            if isinstance(accessor, Accessor):
                f_name = accessor.trait_attribute.field_name
                if f_name is None:
                    # skipp attribute that does not seem to belong to a traited type
                    continue
                accessor.store(getattr(datatype, f_name))


    def load_into(self, datatype):
        # type: (HasTraits) -> None
        for name, accessor in self.__dict__.iteritems():
            if isinstance(accessor, Reference):
                pass
            elif isinstance(accessor, Accessor):
                f_name = accessor.trait_attribute.field_name
                if f_name is None:
                    # skipp attribute that does not seem to belong to a traited type
                    continue
                setattr(datatype,
                        accessor.trait_attribute.field_name,
                        accessor.load())