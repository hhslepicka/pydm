from ..PyQt.QtDesigner import QExtensionFactory, QPyDesignerTaskMenuExtension
from ..PyQt import QtGui, QtCore

from ..widgets.base import PyDMPrimitiveWidget

from ..widgets.rules_editor import RulesEditor
from ..widgets.waveformplot_curve_editor import WaveformPlotCurveEditorDialog
from ..widgets.timeplot_curve_editor import TimePlotCurveEditorDialog
from ..widgets.scatterplot_curve_editor import ScatterPlotCurveEditorDialog

class PyDMExtensionFactory(QExtensionFactory):
    def __init__(self, parent=None, extensions=None):
        super(PyDMExtensionFactory, self).__init__(parent)
        self.extensions = extensions

    def createExtension(self, obj, iid, parent):
        if isinstance(obj, PyDMPrimitiveWidget):
            return PyDMTaskMenuExtension(obj, parent, self.extensions)
        return None


class PyDMTaskMenuExtension(QPyDesignerTaskMenuExtension):
    def __init__(self, widget, parent, extensions):
        super(PyDMTaskMenuExtension, self).__init__(parent)
        self.widget = widget
        self.__actions = None
        self.__extensions = []

        if extensions is None: extensions = []
        for ex in extensions:
            self.__extensions.append(ex(self.widget))


    def taskActions(self):
        if self.__actions is None:
            self.__actions = []
            for ex in self.__extensions:
                self.__actions.extend(ex.actions())

        return self.__actions

    def preferredEditAction(self):
        if self.__actions is None:
            self.taskActions()
        return self.__actions[0]


class PyDMExtension(object):
    def __init__(self, widget):
        self.widget = widget

    def actions(self):
        raise NotImplementedError


class RulesExtension(PyDMExtension):
    def __init__(self, widget):
        super(RulesExtension, self).__init__(widget)
        self.widget = widget
        self.edit_rules_action = QtGui.QAction("Edit Rules...", self.widget)
        self.edit_rules_action.triggered.connect(self.edit_rules)

    @QtCore.pyqtSlot()
    def edit_rules(self):
        edit_rules_dialog = RulesEditor(self.widget, parent=self.widget)
        edit_rules_dialog.exec_()

    def actions(self):
        return [self.edit_rules_action]


class BasePlotExtension(PyDMExtension):
    def __init__(self, widget, curve_editor_class):
        super(BasePlotExtension, self).__init__(widget)
        self.widget = widget
        self.curve_editor_class = curve_editor_class
        self.edit_curves_action = QtGui.QAction("Edit Curves...", self.widget)
        self.edit_curves_action.triggered.connect(self.edit_curves)

    @QtCore.pyqtSlot()
    def edit_curves(self):
        edit_curves_dialog = self.curve_editor_class(self.widget, parent=self.widget)
        edit_curves_dialog.exec_()

    def actions(self):
        return [self.edit_curves_action]


class WaveformCurveEditorExtension(BasePlotExtension):
    def __init__(self, widget):
        super(WaveformCurveEditorExtension, self).__init__(widget, WaveformPlotCurveEditorDialog)


class TimeCurveEditorExtension(BasePlotExtension):
    def __init__(self, widget):
        super(TimeCurveEditorExtension, self).__init__(widget, TimePlotCurveEditorDialog)


class ScatterCurveEditorExtension(BasePlotExtension):
    def __init__(self, widget):
        super(ScatterCurveEditorExtension, self).__init__(widget, ScatterPlotCurveEditorDialog)
