from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from tvb.datatypes.spectral import FourierSpectrum, WaveletCoefficients, CoherenceSpectrum, ComplexCoherenceSpectrum

from tvb.core.entities.model.datatypes.time_series import TimeSeriesIndex
from tvb.core.neotraits.db import HasTraitsIndex, NArrayIndex


class FourierSpectrumIndex(HasTraitsIndex):
    id = Column(Integer, ForeignKey(HasTraitsIndex.id), primary_key=True)

    segment_length = Column(Float, nullable=False)
    windowing_function = Column(String, nullable=False)
    frequency_step = Column(Float, nullable=False)
    max_frequency = Column(Float, nullable=False)

    source_id = Column(Integer, ForeignKey(TimeSeriesIndex.id), nullable=not FourierSpectrum.source.required)
    source = relationship(TimeSeriesIndex, foreign_keys=source_id, primaryjoin=TimeSeriesIndex.id == source_id)

    def fill_from_has_traits(self, datatype):
        self.gid = datatype.gid.hex
        self.segment_length = datatype.segment_length
        self.windowing_function = datatype.windowing_function
        self.frequency_step = datatype.frequency_step
        self.max_frequency = datatype.max_frequency


class WaveletCoefficientsIndex(HasTraitsIndex):
    id = Column(Integer, ForeignKey(HasTraitsIndex.id), primary_key=True)

    source_id = Column(Integer, ForeignKey(TimeSeriesIndex.id), nullable=not WaveletCoefficients.source.required)
    source = relationship(TimeSeriesIndex, foreign_keys=source_id, primaryjoin=TimeSeriesIndex.id == source_id)

    mother = Column(String, nullable=False)
    normalisation = Column(String, nullable=False)
    q_ratio = Column(Float, nullable=False)
    sample_period = Column(Float, nullable=False)
    number_of_scales = Column(Integer, nullable=False)

    frequencies_id = Column(Integer, ForeignKey("narrays.id"), nullable=not WaveletCoefficients.frequencies.required)
    frequencies = relationship(NArrayIndex, foreign_keys=frequencies_id)

    def fill_from_has_traits(self, datatype):
        self.gid = datatype.gid.hex
        self.mother = datatype.mother
        self.normalisation = datatype.normalisation
        self.q_ratio = datatype.q_ratio
        self.sample_period = datatype.sample_period
        self.number_of_scales = datatype.frequencies.shape[0]
        self.frequencies = NArrayIndex.from_ndarray(datatype.frequencies)


class CoherenceSpectrumIndex(HasTraitsIndex):
    id = Column(Integer, ForeignKey(HasTraitsIndex.id), primary_key=True)

    source_id = Column(Integer, ForeignKey(TimeSeriesIndex.id), nullable=not CoherenceSpectrum.source.required)
    source = relationship(TimeSeriesIndex, foreign_keys=source_id, primaryjoin=TimeSeriesIndex.id == source_id)

    nfft = Column(Integer, nullable=False)
    frequencies_id = Column(Integer, ForeignKey("narrays.id"), nullable=not CoherenceSpectrum.frequency.required)
    frequencies = relationship(NArrayIndex, foreign_keys=frequencies_id)

    def fill_from_has_traits(self, datatype):
        self.gid = datatype.gid.hex
        self.nfft = datatype.nfft
        self.frequencies = NArrayIndex.from_ndarray(datatype.frequencies)


class ComplexCoherenceSpectrumIndex(HasTraitsIndex):
    id = Column(Integer, ForeignKey(HasTraitsIndex.id), primary_key=True)

    source_id = Column(Integer, ForeignKey(TimeSeriesIndex.id), nullable=not ComplexCoherenceSpectrum.source.required)
    source = relationship(TimeSeriesIndex, foreign_keys=source_id, primaryjoin=TimeSeriesIndex.id == source_id)

    epoch_length = Column(Float, nullable=False)
    segment_length = Column(Float, nullable=False)
    windowing_function = Column(String, nullable=False)
    frequency_step = Column(Float, nullable=False)
    max_frequency = Column(Float, nullable=False)

    def fill_from_has_traits(self, datatype):
        self.gid = datatype.gid.hex
        self.epoch_length = datatype.epoch_length
        self.segment_length = datatype.segment_length
        self.windowing_function = datatype.windowing_function
        self.frequency_step = datatype.freq_step
        self.max_frequency = datatype.max_freq