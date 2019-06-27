# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
sys.path.append('../include')

import _predict

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt, QObject, QThreadPool, QRunnable, QTimer, QString, QVariant, pyqtSignal, pyqtSlot
from canvas import DeleteStroke, DeleteGroup, GroupStrokes, PaintScene, PaintView
from layers import LayerPanel, Layer, Folder
from delegate import TreeDelegate
import traceback

class PredictSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Predict(QRunnable):
    '''
    Predict thread

    Inherits from QRunnable to handler predict thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(Predict, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = PredictSignals()    

        # Add the callback to our kwargs
        ## self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result
        finally:
            self.signals.finished.emit()  # Done


class PyQtPaint(QtGui.QWidget):
    """
    Canvas based painting ui w/ brush control, layers, undo functionality

    Attributes:
        color_dialog (QColorDialog): Color Picker
        file_dialog (QFileDialog): Filepath picker for saving img externally
        layers_tree (QTreeWidgetItem): Tree widget acting as a layers panel
        paint_scene (QGraphicsScene): graphics scene storing/maintaing stroke
                                      information
    Args:
        width (int): width of PyQtPaint
        height (int): height of PyQtPaint
    """
    def __init__(self, width, height, *args, **kwargs):
        super(PyQtPaint, self).__init__(*args, **kwargs)
        uic.loadUi('../ui/pyqtpaint.ui', self)

        self._paint_view = PaintView()
        self._paint_view.setRenderHints(QtGui.QPainter.HighQualityAntialiasing)

        self.paint_scene = PaintScene(0, 0, width, height, None)
        self._paint_view.setScene(self.paint_scene)

        # Numbers of layers
        self.num_layers = 0
        self.old_layers = -1

        # Timer to save images
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()

        # Path to save imgs
        self.tmpFilepath = "../img/tmp/tmp.png"

        # Timer to predict shapes
        self.timer_predict = QTimer()
        self.timer_predict.setInterval(1000)
        self.timer_predict.start()

        # The app is not working on predict shapes
        self.working = False

        # Thread to run in background of paint
        self.threadpool = QThreadPool()

        # Setup all UI, and make the connctions between Signals & Slots
        self._setup_ui()
        self._create_actions()
        self._make_connections()

    def __del__(self):
        self.threadpool.deleteLater()

    def _setup_ui(self):
        self.viewport_widget.layout().addWidget(self._paint_view)
        self.layers_tree = LayerPanel(dragToggleColumns=[0], columns=['', ''])
        self.layers_tree.setItemDelegate(TreeDelegate())
        self.layers_widget.layout().addWidget(self.layers_tree)

        self.file_dialog = QtGui.QFileDialog(self)
        self.color_dialog = QtGui.QColorDialog()

        self._update_brush_ui()

    def _create_actions(self):
        self.undo_action = QtGui.QAction('Undo', self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.addAction(self.undo_action)

        self.redo_action = QtGui.QAction('Redo', self)
        self.redo_action.setShortcut('Shift+Ctrl+Z')
        self.addAction(self.redo_action)

        self.delete_action = QtGui.QAction('Delete', self)
        self.delete_action.setShortcut('Backspace')
        self.addAction(self.delete_action)

        self.group_action = QtGui.QAction('Group', self)
        self.group_action.setShortcut('Ctrl+G')
        self.addAction(self.group_action)

        self.save_action = QtGui.QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.addAction(self.save_action)

        self.increase_size_action = QtGui.QAction('Increase Size', self)
        self.increase_size_action.setShortcut(']')
        self.addAction(self.increase_size_action)

        self.decrease_size_action = QtGui.QAction('Decrease Size', self)
        self.decrease_size_action.setShortcut('[')
        self.addAction(self.decrease_size_action)

###        self.brush_softer_action = QtGui.QAction('Brush Softer', self)
###        self.brush_softer_action.setShortcut('{')
###        self.addAction(self.brush_softer_action)

###        self.brush_harder_action = QtGui.QAction('Brush Harder', self)
###        self.brush_harder_action.setShortcut('}')
###        self.addAction(self.brush_harder_action)

    def _make_connections(self):
        self.paint_scene.strokeAdded.connect(self.create_layer_item)
        self.paint_scene.strokeRemoved.connect(self.remove_layer_item)

        self.paint_scene.brushChanged.connect(self._update_brush_ui)
        self.size_SLD.valueChanged.connect(lambda: self.set_pen_size(self.size_SLD.value()))
###        self.blur_SLD.valueChanged.connect(lambda: self.set_pen_blur(self.blur_SLD.value()))

        self.increase_size_action.triggered.connect(lambda: self.paint_scene.increment_pen_size(10))
        self.decrease_size_action.triggered.connect(lambda: self.paint_scene.increment_pen_size(-10))
###        self.brush_softer_action.triggered.connect(lambda: self.paint_scene.increment_pen_blur(1))
###        self.brush_harder_action.triggered.connect(lambda: self.paint_scene.increment_pen_blur(-1))

        self.redo_action.triggered.connect(self.paint_scene.undo_stack.redo)
        self.undo_action.triggered.connect(self.paint_scene.undo_stack.undo)

        self.delete_action.triggered.connect(self.delete_layer)
        self.group_action.triggered.connect(self.group_layers)

        self.save_action.triggered.connect(self.save_img)

        self.layers_tree.itemChanged.connect(self.layer_change)
        self.layers_tree.layerOrderChanged.connect(self.update_layer_index)

        self.color_BTN.clicked.connect(self.update_pen_color)

        self.timer.timeout.connect(self.on_timer)
        self.timer_predict.timeout.connect(self.predict)

        self.connect(self, QtCore.SIGNAL('triggered'),self.closeEvent)

    def _update_brush_ui(self):
        self.size_SLD.setValue(self.paint_scene.pen_size)
###        self.blur_SLD.setValue(self.paint_scene.pen_blur)

        style = QString("QPushButton { border-style: none; \
                                              border-radius: 10px; \
                                              min-width: 3em; \
                                              height: 3em; \
                                              background-color: " +
                               self.paint_scene.pen_color.name() + "}")
        self.color_BTN.setStyleSheet(style)

    def create_layer_item(self, stroke_id, layer_name):
        """
        Creates layer item in layer panel using stroke data

        Args:
            stroke_id (int): unique index of stroke
            layer_name (str): name of stroke layer

        """
        stroke_info = ['', layer_name]
        layer = Layer(stroke_info, stroke_index=stroke_id)

        self.num_layers += 1 
        highest_group = None
        if self.layers_tree.selectedItems():
            iterator = QtGui.QTreeWidgetItemIterator(self.layers_tree)
            while iterator.value():
                item = iterator.value()
                if isinstance(item, Folder) and item in self.layers_tree.selectedItems():
                    highest_group = item
                    break
                iterator += 1
        if highest_group:
            highest_group.insertChild(0, layer)
        else:
            self.layers_tree.insertTopLevelItem(0, layer)
        self.update_layer_index()

    def remove_layer_item(self, stroke_id):
        """
        deletes layer item in layer panel

        Args:
            stroke_id (int): unique index of stroke to be removed

        """
        iterator = QtGui.QTreeWidgetItemIterator(self.layers_tree)
        self.num_layers -= 1

        while iterator.value():
            item = iterator.value()
            if isinstance(item, Layer):
                layer_data = item.data(1, Qt.UserRole).toPyObject()[0]
                if layer_data['stroke_index'] == stroke_id:
                    parent = item.parent()
                    if parent:
                        idx = parent.indexOfChild(item)
                        parent.takeChild(idx)
                    else:
                        idx = self.layers_tree.indexOfTopLevelItem(item)
                        self.layers_tree.takeTopLevelItem(idx)
            if isinstance(item, Folder):
                layer_data = item.data(1, Qt.UserRole).toPyObject()[0]

                if item.group_index == stroke_id:
                    parent = item.parent()
                    if parent:
                        idx = parent.indexOfChild(item)
                        parent.takeChild(idx)
                    else:
                        idx = self.layers_tree.indexOfTopLevelItem(item)
                        self.layers_tree.takeTopLevelItem(idx)
            iterator += 1

    def layer_change(self, item, column):
        """
        updates stroke information, used when updating visibility or layer name

        Args:
            item (QTreeWidgetItem): item associated with stroke
            column (int): column to change
        """
        if column == 0:
            if isinstance(item, Layer):
                self.paint_scene.toggle_layer_visibility(item.stroke_index,
                                                         item.visible)

            elif isinstance(item, Folder):
                for i in range(item.childCount()):
                    if item.visible is True:
                        item.child(i).setFlags(Qt.ItemIsSelectable |
                                               Qt.ItemIsEditable |
                                               Qt.ItemIsEnabled |
                                               Qt.ItemIsDragEnabled)
                    else:
                        item.child(i).setFlags(Qt.NoItemFlags)
                    self.paint_scene.toggle_layer_visibility(item.child(i).stroke_index, item.visible)

        elif column == 1:
            if isinstance(item, Layer):
                self.paint_scene.update_layer_name(item.stroke_index,
                                                   item.text(1))

    def delete_layer(self):
        """
        Deletes selected layers
        """
        for item in self.layers_tree.selectedItems():
            # remove item.stroke_index
            if isinstance(item, Layer):
                if item.parent():
                    command = DeleteStroke(self, item, group=item.parent())
                    self.paint_scene.undo_stack.push(command)
                else:
                    command = DeleteStroke(self, item)
                    self.paint_scene.undo_stack.push(command)

            if isinstance(item, Folder):
                command = DeleteGroup(self, item)
                self.paint_scene.undo_stack.push(command)

    def group_layers(self):
        """
        groups seleted layers

        """
        if self.layers_tree.selectedItems():
            grab_items = []
            for item in self.layers_tree.selectedItems():
                if isinstance(item, Layer):
                    grab_items.append(item.stroke_index)

            command = GroupStrokes(self, grab_items)
            self.paint_scene.undo_stack.push(command)

    def update_layer_index(self):
        """
        iterates through layer panel & updates stacking order of strokes

        """
        iterator = QtGui.QTreeWidgetItemIterator(self.layers_tree)
        while iterator.value():
            item = iterator.value()
            target_index = self.layers_tree.indexFromItem(item).row()
            try:
                new_indx = len(self.paint_scene.strokes) - target_index
                self.paint_scene.set_stroke_zindex(item._stroke_index, new_indx)
            except AttributeError:
                pass

            if isinstance(item, Layer):
                layer_data = item.data(1, Qt.UserRole).toPyObject()[0]
                parent = item.parent()
                if not parent:
                    layer_data['layerType'] = 0
                else:
                    layer_data['layerType'] = 2

                varient = QVariant((layer_data,))
                item.setData(1, Qt.UserRole, varient)

            elif isinstance(item, Folder):
                for i in range(item.childCount()):
                    if item.visible is True:
                        item.child(i).setFlags(Qt.ItemIsSelectable |
                                               Qt.ItemIsEditable |
                                               Qt.ItemIsEnabled |
                                               Qt.ItemIsDragEnabled)
                    else:
                        item.child(i).setFlags(Qt.NoItemFlags)
                    self.paint_scene.toggle_layer_visibility(item.child(i).stroke_index, item.visible)
            iterator += 1

    def set_pen_size(self, size):
        """
        Sets pen size from slider input

        Args:
            size (int): diameter of pen
        """
        self.paint_scene.set_pen_size(size)
        self._update_brush_ui()

    def set_pen_blur(self, blur):
        """
        Sets pen blur

        Args:
            blur (int): level of blur
        """
        self.paint_scene.set_pen_blur(blur)
        self._update_brush_ui()

    def set_pen_color(self, color):
        """
        sets pen color

        Args:
            color (QColor): color to set
        """
        self.paint_scene.set_pen_color(color)
        self._update_brush_ui()

    def update_pen_color(self):
        """
        updates pen color from color picker
        """
        color = self.color_dialog.getColor(self.paint_scene.pen_color,
                                           self, QString('Color'),
                                           QtGui.QColorDialog.ShowAlphaChannel)
        self.paint_scene.set_pen_color(color)

        style = QString("QPushButton { border-style: none; \
                                              border-radius: 10px; \
                                              min-width: 3em; \
                                              height: 3em; \
                                              background-color: " +
                               color.name() + "}")
        self.color_BTN.setStyleSheet(style)

    def on_timer(self):
        """
        saves image to temporary file
        
        if self.num_layers != self.old_layers :
            self.old_layers = self.num_layers
            """
        img = self.get_img()
        img.save(self.tmpFilepath)

    def save_img(self):
        """
        saves image to file
        """
        filepath = self.file_dialog.getSaveFileName(self, "Save Canvas",
                                                    "Render",
                                                    "Images (*.png *.jpg)")
        if filepath:
            img = self.get_img()
            img.save(filepath)

    def get_img(self):
        """
        gets image from PyQtPaint

        Returns:
            img: returns QImage data from canvas
        """
        img = QtGui.QImage(self.paint_scene.width, self.paint_scene.height,
                           QtGui.QImage.Format_RGB32)
        paint = QtGui.QPainter(img)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        self.paint_scene.render(paint)
        paint.end()
        return img

    """
    HFNet function by Hebb rule
    """
    def predict(self):
        if not self.working :
            self.working = True
            predict = Predict(_predict.predict)
            predict.signals.result.connect(self.print_output)
            predict.signals.finished.connect(self.thread_complete)

            # Execute
            self.threadpool.start(predict) 

    def thread_complete(self):
        self.working = False
        print("THREAD COMPLETE!")

    def print_output(self, s):
        ##self.resulted = int(s)
        if s == 0:
            self.results.setText(u"É um retângulo.")
        elif s == 1:
            self.results.setText(u"Catetos, catetos, catetos...")
        elif s == 2:
            self.results.setText(u"Catetos, catetos, catetos...")
        elif s == 3:
            self.results.setText(u"Catetos, catetos, catetos...")
        elif s == 4:
            self.results.setText(u"É círculo")
        else :
            self.results.setText(u"Sei lá")
        ##print(s)

    def progress_fn(self, n):
        print("%d%% done" % n)