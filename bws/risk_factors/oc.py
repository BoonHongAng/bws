'''
Ovarian cancer risk factors.
'''

from bws.risk_factors.rfs import RiskFactor, RiskFactors
from collections import OrderedDict


class Parity(RiskFactor):
    cats = ['-', '0', '1', '>1']
    help_text = 'Number of Children'


class OralContraception(RiskFactor):
    cats = ['-', 'never or <1', '1-4', '5-9', '10-14', '>=15']
    help_text = 'Duration of Oral Contraception Use'
    synonyms = ['oc_use']

    @classmethod
    def get_category(cls, val, isreal=False):
        if val == '-':
            return 0
        if val == 'N' or val.lower() == 'never' or val.lower() == '<1':
            return 1
        if ':' not in val:
            return 0
        val = val.split(':')[1]

        if val.strip() == '<1' or val.strip() == '< 1':
            return 1
        try:
            val = cls.get_num(val, True)
            if val < 1.:
                return 1
        except Exception as e:
            print(e)

        return super(OralContraception, cls).get_category(val, isreal)


class MHT(RiskFactor):
    ''' Menopause hormone replacement '''
    cats = ['-', 'never', 'ever']
    help_text = 'Hormone Replacement Therapy'
    synonyms = ['mht_use']

    @classmethod
    def get_category(cls, val):
        if val == 'N' or val == 'never':
            return 1
        elif val == 'E' or val == 'F' or val == 'C' or val == 'ever':
            return 2
        return 0


class TubalLigation(RiskFactor):
    ''' Tubal ligation surgical procedure for sterilization '''
    cats = ['-', 'no', 'yes']
    help_text = 'Tubal Ligation'
    synonyms = ['TL', 'tl']

    @classmethod
    def get_category(cls, val):
        alt = ['na', 'n', 'y']
        val = val.lower().strip()
        for idx, cat in enumerate(TubalLigation.cats):
            if val == cat or val == alt[idx]:
                return idx
        return 0


class Endometriosis(RiskFactor):
    ''' Endometriosis '''
    cats = ['-', 'no', 'yes']
    help_text = 'Endometriosis'
    synonyms = ['Endo', 'endo']

    @classmethod
    def get_category(cls, val):
        alt = ['na', 'n', 'y']
        val = val.lower().strip()
        for idx, cat in enumerate(Endometriosis.cats):
            if val == cat or val == alt[idx]:
                return idx
        return 0


class BMI(RiskFactor):
    cats = ['-', '<22.5', '22.5-<30', '>=30']
    help_text = 'Body Mass Index'

    @classmethod
    def get_category(cls, val, isreal=True):
        return super(BMI, cls).get_category(val, isreal)


class Height(RiskFactor):
    cats = ['-', '<152.91', '152.91-<159.65', '159.65-<165.96', '165.96-<172.70', '>=172.70']
    help_text = 'Height (cm)'

    @classmethod
    def get_category(cls, val, isreal=True):
        return super(Height, cls).get_category(val, isreal)


class OCRiskFactors(RiskFactors):
    ''' Each risk factor for an individual is defined in terms of a category they are in.
        If a factor is unobserved, missing or not applicable, it is assigned category 0,
        and is not taken into account in the calculation. Otherwise a non-zero number is given
        depending on which group they belong to. These are then combined into a single
        risk factor code (see encode() function) that is used by the BOADICEA risk calculation. '''

    # list of risk factor classes
    risk_factors = [
        Parity,
        OralContraception,
        MHT,
        TubalLigation,
        Endometriosis,
        BMI,
        Height
    ]

    # dictionary of risk factor name and number of categories
    categories = OrderedDict(
        (rf.snake_name(), len(rf.cats)-1) for rf in risk_factors
    )

    # dictionary of risk factor name and the categories
    risk_factors_categories = OrderedDict(
        (rf.snake_name(), rf.cats) for rf in risk_factors
    )
