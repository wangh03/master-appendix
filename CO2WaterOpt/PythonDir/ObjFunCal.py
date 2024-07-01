# ------------------------------------------------------------------------------------
# This file is to calculate objective functon with an instance. Don't move the file
# and running the file with a simple model before you save change to the class section
# ------------------------------------------------------------------------------------

import sys
from resdata.summary import rd_sum
import numpy as np


# -------------------------------------------------------------------------------------
# Objective class and child class code for NPV calculation
# -------------------------------------------------------------------------------------

# objective function class
class ObjFunCla:
    # objective function value
    objfunval = 0
    # NPV value 
    NPV = 0
    # Well cost value
    wellcost = 0
    # new objective function term result
    newvari = 0

    def __init__(self, simsummary, npvcomponent, wellsimdata, wellcostdata, newvari):
        """
        initialize the objective function class. this is the prototype of the class, the third
        and behind parameter could be modified.
        :param simsummary: reservoir summary case.
        :param npvcomponent: all of the data needed for NPV calculation, tuple or list type.
        :param wellsimdata: simulation data that define the well (eg:toe-heel coordinates).
        :param wellcostdata: well cost data.
        :param newvari: other variables.
        """
        self.simsumdata = rd_sum.Summary(f'{simsummary}.UNSMRY')
        self.npvcomdata = npvcomponent
        self.wellsimdata = wellsimdata
        self.wellcostdata = wellcostdata
        self.newvari = newvari

    @classmethod
    # calculate the final result of the objective function value.
    def objfunvalcal(cls):
        cls.objfunval = cls.NPV  # + cls.wellcost + cls.newvari( wait for update to int)
        return cls.objfunval


# NPV class
class NPVCla(ObjFunCla):
    def __init__(self, simsummary, npvcomponent, wellsimdata, wellcostdata, initaldata):
        """
        child class of ObjFunCal define for NPV calculation(only fluid flow)
        :param simsummary:
        :param npvcomponent:
        :param wellsimdata:
        :param wellcostdata:
        :param initaldata:
        """
        super().__init__(simsummary, npvcomponent, wellsimdata, wellcostdata, initaldata)
        self.simsumdata = rd_sum.Summary(f'{simsummary}.UNSMRY')
        self.npvcomdata = npvcomponent
        self.NPVprolist = []  # NPV property list.eg:wellgasprod
        self.NPVprokeylist = []  # NPV property keyword list. eg: 'WGIT:INJ1'
        self.NPVintlist = []
        self.NPVfluprilist = []
        self.NPVdislist = []

    # NPV component data process for later calculation.
    def NPVcompro(self):

        self.NPVprolist = []  # NPV property list.eg:wellgasprod
        self.NPVprokeylist = []  # NPV property keyword list. eg: 'WGIT:INJ1'/'FGIT'
        self.NPVintlist = []
        self.NPVfluprilist = []
        self.NPVdislist = []

        for i in range(0, len(self.npvcomdata)):
            NPVpro = '{}_{}_{}'.format(self.npvcomdata[i]['wellname'].lower(), \
                                       self.npvcomdata[i]['fluidtype'].lower(), \
                                       self.npvcomdata[i]['flowtype'][:4].lower())
            if self.npvcomdata[i]['datatype'][0].upper() == 'W':
                NPVprokey = '{}{}{}T:{}'.format(self.npvcomdata[i]['datatype'][0].upper(), \
                                                self.npvcomdata[i]['fluidtype'][0].upper(), \
                                                self.npvcomdata[i]['flowtype'][0].upper(), \
                                                self.npvcomdata[i]['wellname'])
            else:
                NPVprokey = '{}{}{}T'.format(self.npvcomdata[i]['datatype'][0].upper(), \
                                             self.npvcomdata[i]['fluidtype'][0].upper(), \
                                             self.npvcomdata[i]['flowtype'][0].upper())

            NPVint = '1{}'.format(self.npvcomdata[i]['interval'][0].upper())
            NPVflupri = self.npvcomdata[i]['fluidprice']
            NPVdis = self.npvcomdata[i]['discountfactor']

            self.NPVprolist.append(NPVpro)
            self.NPVprokeylist.append(NPVprokey)
            self.NPVintlist.append(NPVint)
            self.NPVfluprilist.append(NPVflupri)
            self.NPVdislist.append(NPVdis)

        return self.NPVprolist, self.NPVprokeylist, self.NPVintlist, self.NPVfluprilist, self.NPVdislist

    @property
    def NPVsumcal(self):
        # NPV component processing method first to assign value to the list.
        NPVCla.NPVcompro(self)
        # note we assume that time interval and discount factor is consistent for all the NPV component.

        '''
        timerange = self.simsumdata.time_range(interval=self.NPVintlist[0])
        NPVvalue = 0
        for time in range(0, len(timerange)):
            cashflow = 0
            for NPVcomnum in range(0, len(self.NPVprolist)):
                NPVvolumvect = np.insert(self.simsumdata.numpy_vector(self.NPVprokeylist[NPVcomnum], timerange), 0, 0)
                NPVvolumdiff = NPVvolumvect[time+1] - NPVvolumvect[time]
                cashflow += NPVvolumdiff * self.NPVfluprilist[NPVcomnum]

            NPVvalue += cashflow / ((1 + self.NPVdislist[0]) ** time)
        # overwrite the parent class NPV value.
        ObjFunCla.NPV = np.format_float_scientific(NPVvalue,precision=4)
        return ObjFunCla.NPV
        '''

        NPVvalue = 0
        for numcomp in range(len(self.NPVprolist)):
            timerange = self.simsumdata.time_range(interval=self.NPVintlist[numcomp])
            NPVtimelist = []
            discoufactlist = []
            time_index = 1
            for t in range(len(timerange)-1):
                if timerange[t] <= self.simsumdata.end_date:
                    NPVtimelist.append(timerange[t])
                    print(timerange[t],t)
            while time_index < len(NPVtimelist):
                if self.NPVintlist[numcomp] == '1Y':
                    yeardiscountfactor = 1 / ((1 + self.NPVdislist[numcomp]) ** (time_index - 1))
                    discoufactlist.append(yeardiscountfactor)
                    time_index += 1

                elif self.NPVintlist[numcomp] == '1M':
                    monthdiscountfactor = ((1 + self.NPVdislist[numcomp]) ** 0.083333) - 1
                    discountfactor = 1 / ((1 + monthdiscountfactor) ** (time_index - 1))
                    discoufactlist.append(discountfactor)
                    time_index += 1

            flowvolume = self.simsumdata.numpy_vector(key=self.NPVprokeylist[numcomp], time_index=NPVtimelist)
            cashflow = 0
            for numoftime in range(1, len(NPVtimelist)):
                flowvolumediff = flowvolume[numoftime] - flowvolume[numoftime - 1]
                discount_rate = discoufactlist[numoftime - 1]
                cashflow += flowvolumediff * self.NPVfluprilist[numcomp] * discount_rate
                print(flowvolume[numoftime],"  ",flowvolume[numoftime - 1])
                print(f'the production diff at time NPV time step {numoftime} is {flowvolumediff} with {discount_rate}')
            NPVvalue += cashflow
        ObjFunCla.NPV = np.format_float_scientific(NPVvalue)
        return ObjFunCla.NPV


# Well cost class
class WelCosCla(ObjFunCla):
    def __init__(self, simsummary, npvcomponent, wellsimdata, wellcostdata, initaldata):
        super().__init__(simsummary, npvcomponent, wellsimdata, wellcostdata, initaldata)
        pass


if __name__ == "__main__":
    optimal_model_dir = sys.argv[1]
    py_result_dir = sys.argv[2]
    unsmary_dir = '{}/CO2OPTMODEL'.format(optimal_model_dir)
    

    NPVcomponent = ({'datatype': 'Field', 'wellname': 'INJ1', 'fluidtype': 'Gas', 'flowtype': 'Injection', \
               'interval': 'yearly', 'fluidprice': 15, 'discountfactor': 0.08},
              {'datatype': 'Field', 'wellname': 'PROD1', 'fluidtype': 'Oil', 'flowtype': 'Production', \
               'interval': 'yearly', 'fluidprice': -10, 'discountfactor': 0.08}, \
              {'datatype': 'Field', 'wellname': 'PROD1', 'fluidtype': 'Gas', 'flowtype': 'Production', \
               'interval': 'yearly', 'fluidprice': -1e+3, 'discountfactor': 0.08})


    thipar = foupar = fifpar = 0
    NPVcase = NPVCla(unsmary_dir, NPVcomponent, thipar, foupar, fifpar)
    Objcase = ObjFunCla(unsmary_dir, NPVcomponent, thipar, foupar, fifpar)

    # call the NPV calculation property.
    NPVcase.NPVsumcal
    Objcase.objfunvalcal()

    objective_result = Objcase.objfunvalcal()

    # write out the objective function result to a txt file
    py_result_path = '{}/PythonObjeResult.txt'.format(py_result_dir)
    with open(py_result_path, 'w') as file:
        file.write(objective_result)



