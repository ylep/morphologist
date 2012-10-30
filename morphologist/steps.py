import os

class Step(object):
    ''' Abstract class '''

    def __init__(self):
      pass

    def run(self):
        separator = " "
        to_execute = separator.join(self.get_command())
        print "run the command: \n" + to_execute + "\n"
        os.system(to_execute)

class MockStep(Step):

    def __init__(self):
        super(MockStep, self).__init__()

        self.input_1 = None
        self.input_2 = None
        self.input_3 = None

        #outputs
        self.output_1 = None
        self.output_2 = None

    def get_command(self):
        message = "MockStep "
        message += "inputs: %s %s %s outputs: %s %s" %(self.input_1, 
                                                       self.input_2, 
                                                       self.input_3, 
                                                       self.output_1, 
                                                       self.output_2)
        command = ["echo", "'" + message + "' ;", "sleep", "20"]
        return command

class SpatialNormalization(Step):

    def __init__(self):
        super(SpatialNormalization, self).__init__()
        
        self.mri = None
        
        #outputs
        self.commissure_coordinates = None
        self.talairach_transform = None

    def get_command(self):
        # TODO 
        command = ['echo', "TO DO : Spatial Normalization !!!"]
        return command
 

class BiasCorrection(Step):
 

    def __init__(self):
        super(BiasCorrection, self).__init__()

        self.mri = None
        self.commissure_coordinates = None 
        #outputs
        self.hfiltered = None
        self.white_ridges = None
        self.edges = None
        self.variance = None
        self.mri_corrected = None
    
    def get_command(self):
        command = ['VipT1BiasCorrection', 
                   '-i', self.mri, 
                   '-o', self.mri_corrected, 
                   '-wridge', self.white_ridges, 
                   '-ename', self.edges, 
                   '-vname', self.variance, 
                   '-hname', self.hfiltered, 
                   '-Points', self.commissure_coordinates,
                   '-Kregul', "20.0",
                   '-sampling', "16.0",
                   '-Kcrest', "20.0",
                   '-Grid', "2",
                   '-ZregulTuning', "0.5",
                   '-vp', "75",
                   '-e', "3",
                   '-Last', "auto"]                  

        # TODO referentials
        return command
   
 
class HistogramAnalysis(Step):

    def __init__(self):
        super(HistogramAnalysis, self).__init__()

        self.mri_corrected = None
        self.hfiltered = None
        self.white_ridges = None
        # output
        self.histo_analysis = None 

   
    def get_command(self):
        command = ['VipHistoAnalysis', 
                   '-i', self.mri_corrected, 
                   '-o', self.histo_analysis, 
                   '-Save', 'y',
                   '-Mask', self.hfiltered,
                   '-Ridge', self.white_ridges,
                   '-mode', 'i']
        return command

class BrainSegmentation(Step):

    def __init__(self):
        super(BrainSegmentation, self).__init__()

        self.mri_corrected = None
        self.commissure_coordinates = None
        self.white_ridges = None
        self.edges = None
        self.variance = None
        self.histo_analysis = None
        self.erosion_size = 1.8
        # output
        brain_mask = None
         

    def get_command(self):
        command = ['VipGetBrain',
                   '-berosion', str(self.erosion_size),
                   '-i', self.mri_corrected,
                   '-analyse', 'r', 
                   '-hname',  self.histo_analysis,
                   '-bname', self.brain_mask,
                   '-First', "0",
                   '-Last', "0", 
                   '-layer', "0",
                   '-Points', self.commissure_coordinates,
                   '-m', "V",
                   '-Variancename', self.variance,
                   '-Edgesname', self.edges,
                   '-Ridge', self.white_ridges,
                   ]
        # TODO referentials
        return command


class SplitBrain(Step):

    def __init__(self):
        super(SplitBrain, self).__init__()

        self.mri_corrected = None
        self.brain_mask = None
        self.white_ridges = None
        self.histo_analysis = None
        self.commissure_coordinates = None
        self.bary_factor = 0.6
        # output
        self.split_mask = None
   
    def get_command(self):
        command = ['VipSplitBrain',
                   '-input',  self.mri_corrected,
                   '-brain', self.brain_mask,
                   '-analyse', 'r', 
                   '-hname', self.histo_analysis,
                   '-output', self.split_mask,
                   '-mode', "'Watershed (2011)'",
                   '-erosion', "2.0",
                   '-ccsize', "500",
                   '-Ridge', self.white_ridges,
                   '-Bary', str(self.bary_factor),
                   '-walgo','b',
                   '-Points', self.commissure_coordinates]

        # TODO:
        # useful option ?? 
        # "-template", "share/brainvisa-share-4.4/hemitemplate/closedvoronoi.ima"
        # "-TemplateUse", "y" 

        # TODO referencials
        return command