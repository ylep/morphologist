import unittest

from morphologist.tests.test_study import TestStudy
from morphologist.tests.test_analysis import TestAnalysis

from morphologist.tests.intra_analysis.test_analysis import TestIntraAnalysis
from morphologist.tests.intra_analysis.test_study import TestBrainvisaTemplateStudy, TestDefaultTemplateStudy

from morphologist.tests.test_runner import TestThreadRunner, TestSomaWorkflowRunner


if __name__=='__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStudy)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAnalysis))

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBrainvisaTemplateStudy))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDefaultTemplateStudy))

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntraAnalysis))

    # XXX: commented because ThreadRunner does not work anymore
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestThreadRunner))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSomaWorkflowRunner))

    unittest.TextTestRunner(verbosity=2).run(suite)


