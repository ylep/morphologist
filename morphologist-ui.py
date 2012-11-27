import sys
import optparse

from morphologist.gui.qt_backend import QtGui

def create_main_window(study_file=None, mock=False):
    if study_file: print "load " + str(study_file)
    if not mock:
        from morphologist.gui.main_window import IntraAnalysisWindow
        return IntraAnalysisWindow(study_file)
    else:
        print "mock mode"
        from morphologist.tests.mocks.main_window import MockIntraAnalysisWindow
        return MockIntraAnalysisWindow(study_file) 

def option_parser():
    parser = optparse.OptionParser()

    parser.add_option('-f', '--file', 
                      dest="study_file", metavar="STUDY_FILE", default=None, 
                      help="Opens the interface with the study loaded.")
    parser.add_option('--mock', action="store_true", 
                      dest='mock', default=False,
                      help="Test mode, runs mock intra analysis") 
   
    return parser


def main():
    parser = option_parser()
    options, args = parser.parse_args(sys.argv)

    qApp = QtGui.QApplication(sys.argv)
    main_window = create_main_window(options.study_file, options.mock)
    main_window.ui.show()
    sys.exit(qApp.exec_())


if __name__ == '__main__' : main()
