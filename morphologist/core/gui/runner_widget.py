import os
import subprocess

from morphologist.core.gui.qt_backend import QtCore, QtGui, loadUi 
from morphologist.core.gui import ui_directory 
from morphologist.core.runner import MissingInputFileError, MissingModelsError
from morphologist.core.constants import ALL_SUBJECTS


class RunnerView(QtGui.QWidget):
    uifile = os.path.join(ui_directory, 'runner_widget.ui')
    
    def __init__(self, model, parent=None):
        super(RunnerView, self).__init__(parent)
        self.ui = loadUi(self.uifile, self)
        self._running_movie = QtGui.QMovie(":/icons/running.gif")
        self.ui.status_label.setMovie(self._running_movie)
        self._init_model(model)

    def _init_model(self, model):
        self._runner_model = model
        self._runner_model.runner_status_changed.connect(self.on_runner_status_changed)
        self._runner_model.changed.connect(self.on_model_changed)
        self._runner_model.subject_selection_changed.connect(self.on_subject_selection_changed)
        self.on_model_changed()

    @QtCore.Slot()
    def on_model_changed(self):
        self._set_not_running_state()
        self._set_all_subjects_state()
        
    @QtCore.Slot(bool)
    def on_runner_status_changed(self, running):
        if running:
            self._set_running_state()
        else:
            self._set_not_running_state()

    @QtCore.Slot(int)
    def on_subject_selection_changed(self, index):
        if self._runner_model.get_selected_subject_ids():
            self._set_selected_subjects_state()
        else:
            self._set_all_subjects_state()
        self._set_not_running_state()
            
    def _set_selected_subjects_state(self):
        self.ui.label.setText("For selected subjects of the current study :")
        
    def _set_all_subjects_state(self):
        self.ui.label.setText("For all subjects of the current study :")
        
    # this slot is automagically connected
    @QtCore.Slot()
    def on_run_button_clicked(self):
        assert(self._runner_model is not None)
        if self._run_analyses():
            self._set_running_state()
        else:
            self._set_not_running_state()

    def _run_analyses(self):
        run = False
        try:
            selected_subject_ids \
                = self._runner_model.get_selected_subject_ids()
            self._runner_model.runner.run(selected_subject_ids)
            run = self._runner_model.runner._workflow_id is not None
            if not run:
                QtGui.QMessageBox.warning(
                    self, "Already done",
                    "Nothing to do, processing is finished.")
        except MissingModelsError, e:
            res = QtGui.QMessageBox.question(
                self, "Missing sulci identification models",
                "Sulci statistical models (SPAMs) are not installed.\n"
                "Do you want to download and install them now ?",
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Ok)
            if res == QtGui.QMessageBox.Ok:
                self.install_spam_models()
        except MissingInputFileError, e:
            QtGui.QMessageBox.critical(
                self, "Run analysis error",
                "Some input files do not exist.\n%s" %(e))
        return run
 
    # this slot is automagically connected
    @QtCore.Slot()
    def on_stop_button_clicked(self):
        assert(self._runner_model is not None)
        self._runner_model.runner.stop()
        self._set_not_running_state()

    def install_spam_models(self):
        print 'install_spam_models'
        cmd = ['python', '-c', 'from brainvisa.axon import processes; '
               'processes.neuroConfig.gui=True; from PyQt4 import QtGui; '
               'qapp = QtGui.QApplication([]); '
               'processes.initializeProcesses(); '
               'from brainvisa.processing.qtgui.neuroProcessesGUI import showProcess; '
               'showProcess("spam_install_models"); qapp.exec_()']
        subprocess.check_call(cmd)

    # this slot is automagically connected
    @QtCore.Slot()
    def on_erase_button_clicked(self):
        assert(self._runner_model is not None)
        selected_subject_ids = self._runner_model.get_selected_subject_ids()
        if selected_subject_ids == ALL_SUBJECTS:
            msg = "All subjects results will be erased."
        else:
            msg = "The results will be erased for the %d selected subjects." \
                % len(selected_subject_ids)
        msg += "\nDo you really want to erase these results ?"
        answer = QtGui.QMessageBox.question(
            self, "Really erase results ?", msg,
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if answer == QtGui.QMessageBox.Ok:
            self._runner_model.study.clear_results(selected_subject_ids)
            # XXX: this buttun could remain enabled if some files are added
            # manually
            self._set_not_running_state()

    def _set_running_state(self):
        self.ui.run_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)
        self.ui.erase_button.setEnabled(False)
        self._running_movie.start()
        self.ui.status_label.setVisible(True)

    def _set_not_running_state(self):
        self._set_run_button_if_needed()
        self.ui.stop_button.setEnabled(False)
        self._set_erase_button_if_needed()
        self._running_movie.stop()
        self.ui.status_label.setVisible(False)

    def _set_run_button_if_needed(self):
        selected_subject_ids = self._runner_model.get_selected_subject_ids()
        has_subjects = self._runner_model.study.has_subjects()
        missing_results = \
            not self._runner_model.study.has_all_results(selected_subject_ids)
        enable_run_button = has_subjects and missing_results
        self.ui.run_button.setEnabled(enable_run_button)

    def _set_erase_button_if_needed(self):
        selected_subject_ids = self._runner_model.get_selected_subject_ids() 
        enable_erase_button \
            = self._runner_model.study.has_some_results(selected_subject_ids)
        self.ui.erase_button.setEnabled(enable_erase_button)


