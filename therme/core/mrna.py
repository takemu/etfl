# -*- coding: utf-8 -*-
"""
.. module:: thermome
   :platform: Unix, Windows
   :synopsis: Thermodynamics-based Flux Analysis

.. moduleauthor:: pyTFA team

ME-related Enzyme subclasses and methods definition


"""

from ..optim.variables import mRNAVariable
from cobra import Species, Metabolite, DictList
from Bio.SeqUtils import molecular_weight



class mRNA(Species):
    def __init__(self, id=None, kdeg=None, gene_id=None, *args, **kwargs):
        Species.__init__(self, id = id, *args, **kwargs)

        self.kdeg = kdeg
        self._gene_id = gene_id
        self._molecular_weight_override = 0

    @property
    def peptide(self):
        return self.gene.peptide

    @property
    def rna(self):
        return self.gene.rna

    @property
    def gene(self):
        return self.model.genes.get_by_id(self._gene_id)


    def init_variable(self, queue=False):
        """
        Attach an mRNAVariable object to the Species. Needs to have the object
        attached to a model

        :return:
        """
        self._mrna_variable = self.model.add_variable(mRNAVariable,
                                                        self,
                                                        queue=queue)

    @property
    def molecular_weight(self):
        if not self._molecular_weight_override:
            return molecular_weight(self.rna) / 1000 # g.mol^-1 -> kg.mol^-1 (SI) = g.mmol^-1
        else:
            return self._molecular_weight_override

    @molecular_weight.setter
    def molecular_weight(self, value):
        self._molecular_weight_override = value

    @property
    def variable(self):
        """
        For convenience in the equations of the constraints

        :return:
        """
        try:
            return self._mrna_variable.variable
        except AttributeError:
            self.model.logger.warning('''{} has no model attached - variable attribute
             is not available'''.format(self.id))