#!/usr/bin/env python
# -*- coding: utf-8 *-*


"""
    QConfigList is a single-file PySide6 custom QWidget
    class representing a customizable list of QWidgets.
    It allows adding, removing, editing the content,
    the style, and verifying the QWidgets values easily.

     _____________________________________________________________________
    | VERSION | DATE YYYY-MM-DD |                 CONTENT                 |
    |=====================================================================|
    |  1.0.0  |      2024-03-23 | Initial and fully functional commit.    |
    |---------|-----------------|-----------------------------------------|
    |  1.0.1  |      2024-03-23 | Add missing annotations and 'f'         |
    |         |                 | parameter to the QConfigList class.     |
    |---------|-----------------|-----------------------------------------|
    |  1.0.2  |      2024-03-23 | Edit classe and method signatures to    |
    |         |                 | support both Tuple and List when        |
    |         |                 | when mutability is an option.           |
    |         |                 | Import typing utilities directly from   |
    |         |                 | typing for readability.                 |
    |---------|-----------------|-----------------------------------------|
    |  1.0.3  |      2024-03-23 | Fix the typing issues inducted by       |
    |         |                 | v1.0.2 and fix the QConfigList's        |
    |         |                 | __init__ method.                        |
    |---------|-----------------|-----------------------------------------|
    |  1.0.4  |      2024-03-24 | Remove the header's row stretch.        |
    |         |                 | Place the QConfigList's __init__ method |
    |         |                 | "parent" and 'f' argument to the end    |
    |         |                 | in order to follow Qt constructors     |
    |         |                 | conventions.                            |
    |         |                 | Fix the typing issues of the            |
    |         |                 | QConfigList's initial parameter.        |
    |         |                 | Fix some typing notations of the        |
    |         |                 | QConfigList's __init__ method.          |
    |---------|-----------------|-----------------------------------------|
    |  1.0.5  |      2024-03-24 | Add a widgets ad widgets_str attributes |
    |         |                 | to QConfigList.                         |
    |         |                 | Add an adjust_parent parameter to the   |
    |         |                 | QConfigList's __init__ method for       |
    |         |                 | adjusting the parent's widget when      |
    |         |                 | removing a row from the grid layout.    |
    |         |                 | Remove the default_row_widget_texts     |
    |         |                 | argument from the QConfigList's         |
    |         |                 | __init__ method and change the          |
    |         |                 | row_widget type: it is not the row      |
    |         |                 | widgets types anymore, but the function |
    |         |                 | to call to create a widget when adding  |
    |         |                 | a new row. This function takes the      |
    |         |                 | parent reference as an argument.        |
    |         |                 | Add an only_one_empty_row attribute to  |
    |         |                 | the QConfigList's __init__ method.      |
    |         |                 | Rework the way the _widget_interacted   |
    |         |                 | callback get connected to widgets.      |
    |---------|-----------------|-----------------------------------------|
    |  1.0.6  |      2024-03-25 | Add an only_one_empty_cell to the       |
    |         |                 | QConfigList's __init__ method.          |
    |         |                 | Add a content_function method to the    |
    |         |                 | QConfigList's __init__ method.          |
    |         |                 | Use the content_function to retrieve    |
    |         |                 | the widgets content instead of using    |
    |         |                 | the text method.                        |
    |         |                 | Use a QTimer to periodically check if   |
    |         |                 | any widget content has been modifier    |
    |         |                 | instead of hard coding connexion        |
    |         |                 | between some types of QWidgets and some |
    |         |                 | signals.                                |
    |---------|-----------------|-----------------------------------------|
    |  1.0.7  |      2024-03-27 | Add a set_stylesheets method.           |
    |---------|-----------------|-----------------------------------------|
    |  1.0.8  |      2024-03-30 | Add a widget_edited_callback argument   |
    |         |                 | to the QConfigList's __init__ method.   |
    |         |                 | Create the AddRemoveEditEnum enum.      |
    |         |                 | Add a no_duplicates argument to the     |
    |         |                 | QConfigList's __init__ method.          |
    |         |                 | Rename the valid pseudo getter method   |
    |         |                 | to is_valid.                            |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
"""

# =--------------= #
# Libraries import #
# =--------------= #

from typing            import Any, Callable, Dict, List, Optional, Tuple, Union
from PySide6.QtCore    import Qt, QEvent, QTimer
from PySide6.QtGui     import QCloseEvent, QMouseEvent
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLayoutItem, QLineEdit, QPushButton, QSizePolicy, \
    QVBoxLayout, QWidget
from enum              import Enum
import re

# =-------------------------------------------------------------------------------------------------------------= #


# =--------= #
# Authorship #
# =--------= #

__author__       = "Quentin Raimbaud"
__contact__      = "quentin.raimbaud.contact@gmail.com"
__date__         = "2024-03-30"
__license__      = "LGPL-2.1"
__maintainer__   = "Quentin Raimbaud"
__status__       = "Development"
__version__      = "1.0.8"

# =-------------------------------------------------= #


# =------------------= #
# GridActionEnum Enum #
# =------------------= #

class AddRemoveEditEnum(Enum):
    """Add / Remove / Edit enum."""
    ADD    = 0
    REMOVE = 1
    EDIT   = 2

# =-------------------------------------------------= #


# =---------------= #
# QConfigList class #
# =---------------= #

class QConfigList(QWidget):
    """QConfigList class representing a customizable list of QWidgets."""

    # =================== #
    # Initializer methods #
    # =================== #

    def __init__(
            self,
            n: Optional[int] = None,
            max_rows: Optional[int] = None,
            no_duplicates: Union[Tuple[int, ...], List[int]] = (),
            header_texts: Optional[Union[Tuple[str, ...], List[str]]] = None,
            row_widgets: Optional[Union[Tuple[Callable[..., Any], ...], List[Callable[..., Any]]]] = None,
            initial: Optional[
                Union[
                    Tuple[Union[Tuple[QWidget, ...], List[QWidget]], ...],
                    List[Union[Tuple[QWidget, ...], List[QWidget]]]
                ]
            ] = None,
            content_function: Optional[Callable[..., Any]] = None,
            validity_function: Optional[Callable[[Tuple[QWidget, ...]], bool]] = None,
            widget_edited_callback: Optional[Callable[..., Any]] = None,
            only_one_empty_row: bool = False,
            only_one_empty_cell: bool = False,
            adjust_parent: bool = True,
            no_buttons: bool = False,
            no_verif: bool = False,
            style: Optional[Dict[str, Union[str, Dict[str, str]]]] = None,
            parent: Optional[QWidget] = None,
            f : Optional[Qt.WindowType] = None,
    ) -> None:
        """
        Initializer method.
        If n is provided, use such number of columns per row.
        If max_rows is provided, use such a maximum number of rows. Headers are not taken into account for computing \
the current number of rows.
        If no_duplicates is provided, make every rows invalid if the given column numbers have duplicates. To be \
aligned with PySide6's row/columns mechanism, the columns start at index 1.
        If header_texts is provided, create QLabel with such header_texts to the QConfigList.
        If row_widgets is provided, use such widgets for each row of the QConfigList.
        If initial is provided, fill the QConfigList's grid layout with the given widgets.
        If validity_function is provided, use such a function to validate the content of a row giving every row's \
QWidget as parameters.
        If widget_edited_callback is provided, call such a callback function when any QWidget gets edited, passing the \
corresponding action AddRemoveEditEnum enum as well as this QWidget's row content as a parameter.
        If style is provided, use such a style dictionary for the QConfigList.
        If parent is provided, set such a parent to the QConfigList.
        If f is provided, set such WindowType to the QConfigList.

        :param n: The number of columns of the QConfigList to instantiate. By default, None. If None but header_texts \
or row_widgets are not None, use the length of such arguments in this order of priority: \
header_texts > row_widgets. If all of these 2 arguments are None, use 2.
        :type n: int or None
        :param max_rows: The optional column numbers to check the duplicates. By default, [].
        :type max_rows: int or None
        :param max_rows: The optional maximum number of rows. By default, None.
        :type max_rows: List[int]
        :param header_texts: The optional header texts of the QConfigList to instantiate. By default, None.
        :type header_texts: Tuple[str, ...] or List[str] or None
        :param row_widgets: The optional widgets of the QConfigList to instantiate. By default, None. If None, use one \
QLabel("Column 1") and QLineEdit("Column X") for the rest of the rows if n <1, otherwise use a single \
QLineEdit("Column").
        :type row_widgets: Tuple[Callable[..., Any], ...] or List[Callable[..., Any]] or None
        :param initial: The optional widgets to add to the QConfigList's grid layout. By default, None.
        :type initial: Tuple[Tuple[QWidget, ...] or List[QWidget], ...] or List[Tuple[QWidget, ...] or List[QWidget]] \
or None
        :param content_function: The optional content function used to retrieve the content of a widget. It takes a \
QWidget as parameters. By Default, None. If None, return the widget's text.
        :type content_function: Callable[..., Any] or None
        :param validity_function: The optional validity function used to validate the content of a row. It takes every \
row's QWidget as parameters. By Default, None. If None, return True anyway.
        :type validity_function: Callable[[Tuple[QWidget, ...]], bool] or None
        :param widget_edited_callback: The optional callback function to call when any QWidget get edited. By default, \
None.
        :type widget_edited_callback: Callable[..., Any] or None
        :param only_one_empty_row: If True, only one empty row can be present on the grid layout as the same time, \
meaning the Add ('+') button will be disabled while an empty row exist. If only_one_empty_row: and only_one_empty_cell \
are True, only_one_empty_cell will be taken into account.
        :type only_one_empty_row: bool
        :param only_one_empty_cell: Similar to only_one_empty_row, but row with a single empty column will count. By \
default, False
        :type only_one_empty_cell: bool
        :param adjust_parent: If True, adjust the parent's size using adjustSize when a row get removed. By default, \
True.
        :type adjust_parent: bool
        :param no_buttons: If True, don't create the add/remove ('+'/'-') buttons. By default, False.
        :type no_buttons: bool
        :param no_verif: If True, performs no verification on the provided arguments. By default, False.
        :type no_verif: bool
        :param style: The optional style dictionary used for the QConfigList. This style dictionary should match the \
style format introduced by the HotClick software. By default, None. If None, use the QConfigList's default style \
dictionary
        :type style: Dict[str, Union[str, Dict[str, str]]] or None
        :param parent: The optional parent of the QConfigList to instantiate. By default, None.
        :type parent: QWidget or None
        :param f: The optional WindowType of the QConfigList to instantiate. By default, None.
        :type f: Qt.WindowType or None
        """

        # Call the super class's initializer method.
        if f is not None:
            if parent is not None:
                super().__init__(parent=parent, f=f)
            else:
                super().__init__(f=f)
        else:
            if parent is not None:
                super().__init__(parent=parent)
            else:
                super().__init__()

        # Set default arguments for the mutable arguments.
        if n is None:
            if header_texts is not None:
                n = len(header_texts)
            elif row_widgets is not None:
                n = len(row_widgets)
        if row_widgets is None:
            if n > 1:
                row_widgets = (
                    lambda parent_: QLabel("Column 1"),
                    *tuple(lambda parent_: QLineEdit("Column X") for _ in range(n - 1))
                )
            else:
                row_widgets = (lambda parent_: QLineEdit("Column"),)
        if only_one_empty_row and only_one_empty_cell:
            only_one_empty_row = False
        if content_function is None:
            def content_function(widget: QWidget) -> Any:
                """Default content function: return the widget's text."""
                if hasattr(widget, "text"):
                    return widget.text()
                return None
        if validity_function is None:
            def validity_function(*_args: QWidget) -> bool:
                """Default validity function: return True anyway."""
                return True
        if no_duplicates:
            old_validity_function: Callable[[Tuple[QWidget, ...]], bool] = validity_function

            def validity_function(*_args: QWidget) -> bool:
                """Default validity function: return True anyway."""
                for column in self._no_duplicates:
                    column = column-1
                    widget: QWidget = _args[column]
                    for row_widgets_ in self.widgets:
                        widget_: QWidget = row_widgets_[column]
                        if widget != widget_ and self._content_function(widget) == self._content_function(widget_):
                            return False
                return old_validity_function(*_args)
        if style is None:
            style = self.default_style

        # Ensure the validity of the provided arguments.
        if not no_verif:
            if n < 0:
                raise ValueError(f"Invalid number of columns. A QConfigList cannot have a negative number of columns.")
            if n == 0:
                raise ValueError(f"Invalid number of columns. A QConfigList should have at least 1 column.")
            if max_rows is not None and max_rows < 0:
                raise ValueError(
                    f"Invalid number of columns. A QConfigList cannot have a negative maximum number of rows."
                )
            if max_rows is not None and max_rows == 0:
                raise ValueError(f"Invalid number of columns. A QConfigList should have at least 1 row.")
            if header_texts is not None and len(header_texts) != n:
                raise ValueError(f"Invalid number of header texts. Expected {n} but got {len(header_texts)}.")
            if len(row_widgets) != n:
                raise ValueError(f"Invalid number of row widgets. Expected {n} but got {len(row_widgets)}.")
            if initial is not None:
                if not len(initial):
                    raise ValueError(f"Invalid number of initial widgets per row to fill. List is empty.")
                if any((len(initial[i]) != len(initial[i-1]) for i in range(len(initial)))):
                    raise ValueError(
                        f"Inconsistent number of initial widgets per row to fill. "
                        f"Expected only {n} but got {list(set(len(e) for e in initial))}."
                    )
                if len(initial[0]) != n:
                    raise ValueError(
                        f"Invalid number of initial widgets per row to fill. Expected {n} but got {len(initial[0])}."
                    )
                if max_rows is not None and len(initial) > max_rows:
                    raise ValueError(
                        f"Invalid number of rows to fill. Maximum is {max_rows} but got {len(initial)}."
                    )

        # Set the straight-forward attributes.
        self._n: int = n
        self._max_rows: int = max_rows
        self._no_duplicates: List[int] = no_duplicates
        self._first_row_index: int = 0 if header_texts is None else n
        self._selected_row: int = -1
        self._header_texts: Optional[Union[Tuple[str, ...], List[str]]] = header_texts
        self._row_widgets: Union[Tuple[Callable[..., Any], ...], List[Callable[..., Any]]] = row_widgets
        self._initial: Optional[
                Union[
                    Tuple[Union[Tuple[QWidget, ...], List[QWidget]], ...],
                    List[Union[Tuple[QWidget, ...], List[QWidget]]]
                ]
            ] = initial
        self._content_function: Callable[..., Any] = content_function
        self._validity_function: Callable[..., bool] = validity_function
        self._widget_edited_callback: Optional[Callable[..., Any]] = widget_edited_callback
        self._valid_grid_layout_pattern: str = r"color\s*:\s*" + style["Custom"]["invalid-color"] + r"\s*;"
        self._only_one_empty_row: bool = only_one_empty_row
        self._only_one_empty_cell: bool = only_one_empty_cell
        self._adjust_parent: bool = adjust_parent
        self._no_buttons: bool = no_buttons
        self._style: Dict[str, Union[str, Dict[str, str]]] = style
        self._widgets_content: List[Tuple[Any, ...]] = []

        # Initialize the QConfigList UI.
        self._init_ui()

        # Initialize the QTimer for periodically
        # check if a widget got modified.
        self._timer: QTimer = QTimer(self)
        # For typing issues.
        if hasattr(self._timer.timeout, "connect"):
            self._timer.timeout.connect(self._check_modified_widgets)
        self._timer.start(100)

        # If self._initial is not None, fill the
        # QConfigList's grid layout with such row widgets.
        self._initial_grid_layout_rows()

    def _init_ui(self) -> None:
        """Initialize the QConfigList UI."""

        # Set the QConfigList's background-color.
        self._set_config_list_stylesheet()

        # Initialize the main layout.
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize and configure the buttons container widget
        # and its horizontal layout for the add/remove ('+'/'-') buttons.
        self._buttons_container: Optional[QWidget] = None
        self._add_button: Optional[QWidget] = None
        self._remove_button: Optional[QWidget] = None
        if not self._no_buttons:
            self._buttons_container = QWidget()
            self._set_buttons_container_stylesheet()
            buttons_layout: QHBoxLayout = QHBoxLayout(self._buttons_container)
            buttons_layout.setSpacing(0)
            buttons_layout.setContentsMargins(0, 0, 0, 0)

            # Initialize, configure and connect the add ('+') button.
            # Then, add it to the buttons container widget.
            self._add_button = QPushButton("+")
            self._add_button.clicked.connect(self._add_grid_layout_row)
            self._set_add_button_stylesheet()
            buttons_layout.addWidget(self._add_button)

            # Initialize, configure and connect the remove ('-') button.
            # Disable it assuming the grid layout is initially empty.
            # Then, add it to the buttons container widget.
            self._remove_button = QPushButton("−")
            self._remove_button.setDisabled(True)
            self._remove_button.clicked.connect(self._remove_grid_layout_selected_row)
            self._set_remove_button_stylesheet()
            buttons_layout.addWidget(self._remove_button)

            # Add a stretchable space to pack the buttons to the left
            # and add the buttons container widget to the main layout.
            buttons_layout.addStretch()
            main_layout.addWidget(self._buttons_container)

            # Add the buttons container widget to the main layout.
            main_layout.addLayout(buttons_layout)

        # Initialize the grid layout and
        # add it the potential headers.
        self._grid_layout = QGridLayout()
        self._grid_layout.setSpacing(0)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        for i in range(self._n):
            self._grid_layout.setColumnStretch(i, 1)
        if self._header_texts is not None:
            self._add_grid_layout_headers(self._header_texts)

        # Add the gri layout to the main layout.
        main_layout.addLayout(self._grid_layout)

        # Set the main layout as the QConfigList's layout.
        self.setLayout(main_layout)

    # ================== #
    # Overridden methods #
    # ================== #

    def closeEvent(self, event: QCloseEvent):
        """
        Overridden closeEvent method.
        This method is called when the QConfigList get closed.

        :param PySide6.QtGui.QCloseEvent event: The QCloseEvent received.
        """

        # Stop the timer.
        self._timer.stop()
        
        # Call the super class's closeEvent method.
        super().closeEvent(event)

    def eventFilter(self, watched: QWidget, event: QEvent) -> bool:
        """
        Overridden eventFilter method.
        This method is called when any widget which have called
        installEventFilter with the QConfigList itself receive an event.

        :param watched: The QWidget concerned by the received event.
        :type watched: QWidget
        :param event: The event received by the QConfigList.
        :type watched: QEvent
        """

        # If the event is a MouseButtonPress, call
        # the widget_clicked callback method.
        if event.type() == QMouseEvent.Type.MouseButtonPress:
            self._widget_interacted(watched)

        """
        # If the watched widget is among the grid layout,
        # call the widget_interacted method on such a widget.
        if event.type() not in (
                #QEvent.Type.Enter,
                QEvent.Type.FocusAboutToChange,
                QEvent.Type.FocusIn,
                QEvent.Type.FocusOut,
                QEvent.Type.Hide,
                QEvent.Type.HoverEnter,
                QEvent.Type.HoverLeave,
                QEvent.Type.HoverMove,
                QEvent.Type.Leave,
                QEvent.Type.Move,
                QEvent.Type.Paint,
                QEvent.Type.PaletteChange,
                QEvent.Type.Polish,
                QEvent.Type.PolishRequest,
                QEvent.Type.Resize,
                QEvent.Type.Show,
                QEvent.Type.ShowToParent,
                QEvent.Type.StyleChange,
                QEvent.Type.UpdateLater,
                QEvent.Type.WindowActivate,
                QEvent.Type.WindowBlocked,
                QEvent.Type.WindowDeactivate,
                QEvent.Type.WindowUnblocked
        ):
            for i in range(self._grid_layout.count()):
                if self._grid_layout.itemAt(i) is not None:
                    widget: QWidget = self._grid_layout.itemAt(i).widget()
                    if watched == widget:
                        self._widget_interacted(watched)
                        break
        """

        # Return without filtering the handled event.
        return super().eventFilter(watched, event)

    # ========================== #
    # Private high-level methods #
    # ========================== #

    def _add_grid_layout_headers(self, header_texts: Union[Tuple[str, ...], List[str]]) -> None:
        """
        Add headers to the grid layout.
        The provided header_texts is a tuple containing at least one string element.
        This method is a wrapper to add_grid_layout_row with some hardcoded arguments.

        :param header_texts: The QLabel's header texts to add to the grid layout.
        :type header_texts: Tuple[str, ...] orList[str]
        """

        # Initialize the QLabels to use as headers.
        labels: List[QLabel] = []
        for header_text in header_texts:
            label: QLabel = QLabel(header_text)
            self._set_grid_layout_header_stylesheet(label)
            labels.append(label)

        # Call _add_grid_layout_widgets with the unpacked initialized labels list.
        self._add_grid_layout_widgets(*labels, no_stretch=True)

    def _initial_grid_layout_rows(self) -> None:
        """
        Add a list of rows to the grid layout.
        This list contains the widgets to directly add.
        The list used is the initial attribute.
        """

        # If initial is None, return here.
        if self._initial is None:
            return

        # Add each row one by one.
        for widgets in self._initial:
            for widget in widgets:
                widget.installEventFilter(self)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Determine the validity of the widgets list to set their stylesheets correctly.
            validity: bool = self._validity_function(*widgets)
            for widget in widgets:
                self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

            # Call _add_grid_layout_widgets with the unpacked initialized widgets list.
            self._add_grid_layout_widgets(*widgets)

        # Update the widgets_content attribute.
        self._widgets_content = self.widgets_content

    def _any_empty_rows(self) -> bool:
        """
        Check if there are any empty rows within the grid layout.

        :returns: The boolean result.
        :rtype: bool
        """

        for i in range(int(self._header_texts is not None) + 1, self._grid_layout.rowCount()):
            if self._grid_layout.rowStretch(i):
                flag: bool = False
                for j in range(self._n):
                    widget: QLayoutItem = self._grid_layout.itemAtPosition(i, j)
                    if widget is not None:
                        if self._content_function(widget.widget()):
                            flag = True
                    else:
                        pass
                if not flag:
                    return True
        return False

    def _any_empty_cell(self) -> bool:
        """
        Check if there are any empty cells within the grid layout.

        :returns: The boolean result.
        :rtype: bool
        """

        for i in range(int(self._header_texts is not None) + 1, self._grid_layout.rowCount()):
            if self._grid_layout.rowStretch(i):
                for j in range(self._n):
                    widget: QLayoutItem = self._grid_layout.itemAtPosition(i, j)
                    if widget is not None:
                        if not self._content_function(widget.widget()):
                            return True
        return False

    # ================ #
    # Callback methods #
    # ================ #

    def _add_grid_layout_row(self) -> None:
        """
        Add a row to the grid layout.
        The row widgets used will be the one from the row_widgets attribute.
        The default row widget content used will be the one from the default_row_widgets attribute.
        This method is a wrapper to add_grid_layout_row with some hardcoded arguments.
        """

        # Initialize the QWidgets list.
        widgets: List[QWidget] = []
        for func in self._row_widgets:
            widget: QWidget = func(self)
            widget.installEventFilter(self)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widgets.append(widget)

        # Determine the validity of the widgets list to set their stylesheets correctly.
        validity: bool = self._validity_function(*widgets)
        for widget in widgets:
            self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

        # Call _add_grid_layout_widgets with the unpacked initialized widgets list.
        self._add_grid_layout_widgets(*widgets)

        tmp: int = self._grid_layout.count()
        self._widget_edited_callback(
            AddRemoveEditEnum.ADD,
            *tuple(self._content_function(self._grid_layout.itemAt(i).widget()) for i in range(tmp-self._n, tmp))
        )

    def _remove_grid_layout_selected_row(self):
        """
        Remove the selected row from the grid layout.
        If no row is selected, do nothing.
        """

        # If no row has been selected, return here.
        if self._selected_row == -1:
            return

        # Remove the selected row and
        # Update the grid layout row stretch.
        i: int = self._n*self._selected_row
        self._grid_layout.setRowStretch(self._grid_layout.getItemPosition(i)[0], 0)
        self._widget_edited_callback(
            AddRemoveEditEnum.REMOVE,
            *tuple(self._content_function(self._grid_layout.itemAt(i).widget()) for i in range(i, i+self._n))
        )
        for _ in range(i, i+self._n):
            widget: QWidget = self._grid_layout.itemAt(i).widget()
            self._grid_layout.removeWidget(widget)
            widget.deleteLater()

        # Unselect the row.
        self._unselect_row()

        # If the only_one_empty_row attribute is True,
        # disable the Add ('+') button if there is an empty row.
        if not self._only_one_empty_row or not self._any_empty_rows():
            self._add_button.setDisabled(False)
        # Same for only_one_empty_cell.
        if not self._only_one_empty_cell or not self._any_empty_cell():
            self._add_button.setDisabled(False)

        # Resize the QConfigList.
        self._grid_layout.activate()
        self.adjustSize()
        self.update()

        # Adjust the parent size if such a parent exist
        # and if the adjust_parent attribute is True.
        if self.parent() is not None and self._adjust_parent:
            self.parent().layout().activate()
            self.parent().adjustSize()
            self.parent().update()

    def _widget_clicked(self, widget: QWidget, no_select: bool = False) -> None:
        """
        This method override the rows widgets "mousePressEvent" method.
        If no_select is True, select no widgets.

        :param widget: The widget that got clicked.
        :type widget: QWidget
        """

        # Retrieve the widget's index within the grid layout.
        index: int = self._grid_layout.indexOf(widget)

        # Unselect every widget within the grid layout.
        for i in range(self._n if self._header_texts is not None else 0, self._grid_layout.count(), self._n):
            # Determine the validity of each row to set their widget stylesheets correctly.
            row_widgets: Tuple[QWidget, ...] = tuple(
                self._grid_layout.itemAt(j).widget() for j in range(i, i+self._n)
            )
            validity: bool = self._validity_function(*row_widgets)
            for widget in row_widgets:
                self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

        # If no_select is True, return here.
        if no_select:
            return

        # Select the whole clicked row widgets and determine its
        # validity to set their stylesheets correctly.
        row_nbr: int = self._n * int(index / self._n)
        row_widgets: Tuple[QWidget, ...] = tuple(
            self._grid_layout.itemAt(j).widget() for j in range(row_nbr, row_nbr + self._n)
        )
        validity: bool = self._validity_function(*row_widgets)
        for widget in row_widgets:
            self._set_grid_layout_widget_selected_stylesheet(widget, validity)

        # Select the row.
        self._select_row(int(row_nbr/self._n))

    def _widget_interacted(self, widget: QWidget) -> None:
        """
        This method is connected to every widget of a row capable of being interacted.

        :param widget: The widget that got interacted.
        :type widget: QWidget
        """

        # Retrieve the widget's index within the grid layout.
        index: int = self._grid_layout.indexOf(widget)

        # Retrieve the every widget of the concerned row.
        tmp: int = self._n*int(index/self._n)
        widgets: Tuple[QWidget, ...] = tuple(
            self._grid_layout.itemAt(i).widget() for i in range(tmp, tmp+self._n)
        )

        # Call the widget_clicked callback method.
        self._widget_clicked(widget)

        # If the only_one_empty_row attribute is True,
        # disable the Add ('+') button if there is an empty row.
        if self._only_one_empty_row and not self._any_empty_rows():
            self._add_button.setDisabled(False)
        # Same for only_one_empty_cell.
        if self._only_one_empty_cell and not self._any_empty_cell():
            self._add_button.setDisabled(False)

        # Ensure the validity of the row and edit the widget stylesheets.
        validity: bool = self._validity_function(*widgets)
        for widget in widgets:
            self._set_grid_layout_widget_selected_stylesheet(widget, validity)

    def _check_modified_widgets(self) -> None:
        """
        Check periodically if any widget got modified
        for calling the _widget_interacted callback method.
        """

        # If any widget's content has changed since last iteration,
        # apply the _widget_interacted callback method on such a widget.
        i: int = 0
        offset: int = int(self._header_texts is not None) + 1
        while i < self._grid_layout.rowCount():
            if self._grid_layout.rowStretch(i):
                for j in range(self._n):
                    widget_item: QLayoutItem = self._grid_layout.itemAtPosition(i, j)
                    if self._grid_layout.itemAtPosition(i, j) is not None:
                        widget: QWidget = widget_item.widget()
                        widget_content: Any = self._content_function(widget)
                        try:
                            if widget_content != self._widgets_content[i-offset][j]:
                                self._widget_interacted(widget)
                                if self._widget_edited_callback is not None:
                                    self._widget_edited_callback(
                                        AddRemoveEditEnum.EDIT,
                                        *tuple(
                                            self._content_function(
                                                self._grid_layout.itemAtPosition(i, j).widget()
                                            ) for j in range(self._n)
                                        )
                                    )
                        except IndexError:
                            pass
            i += 1
        # Update the row_count and widgets_content attribute.
        self._row_count = self._grid_layout.rowCount()
        self._widgets_content = self.widgets_content

    # ========================= #
    # Private low-level methods #
    # ========================= #

    def _add_grid_layout_widgets(self, *widgets: QWidget, no_stretch: bool = False) -> None:
        """
        Add the provided widgets to the grid layout.

        :param *widgets: The widgets to add to the grid layout.
        :type *widgets: QWidget
        :param no_stretch: If True, set thew newly created gris layout row stretch to 0 instead of 1.
        :type no_stretch: bool
        """

        # Retrieve the current grid layout's row number.
        row_number: int = self._grid_layout.rowCount()

        # Add the every element of the provided row to the grid layout.
        for column_nbr in range(len(widgets)):
            self._grid_layout.addWidget(widgets[column_nbr], row_number, column_nbr)

        # If the maximum number of rows is
        # reached, disable the add ('+') button.
        if self._max_rows is not None and (row_number - int(self._header_texts is not None)) == self._max_rows:
            self._add_button.setDisabled(True)

        # Update the grid layout row stretch and
        # the row stretch mapping dictionary.
        if no_stretch:
            self._grid_layout.setRowStretch(row_number, 0)
        else:
            self._grid_layout.setRowStretch(row_number, 1)

        # If the only_one_empty_row attribute is True,
        # disable the Add ('+') button if there is an empty row.
        if self._only_one_empty_row and self._any_empty_rows():
            self._add_button.setDisabled(True)
        # Same for only_one_empty_cell.
        if self._only_one_empty_cell and self._any_empty_cell():
            self._add_button.setDisabled(True)

    # ================== #
    # StyleSheet methods #
    # ================== #

    def _set_config_list_stylesheet(self) -> None:
        """Set the QConfigList stylesheet."""

        # Set the QConfigList stylesheet.
        self.setStyleSheet(f"""
            background-color: {self._style["background-color"]}
        """)

    def _set_buttons_container_stylesheet(self) -> None:
        """Set the button container stylesheet."""

        # Set the buttons container stylesheet if it exists.
        if self._buttons_container is not None:
            self._buttons_container.setStyleSheet("""
                QWidget {
                    border: 1px solid white;
                }
            """)

    def _set_add_button_stylesheet(self) -> None:
        """Set the add button stylesheet."""

        # Set the add button stylesheet if it exists.
        if self._add_button is not None:
            self._add_button.setStyleSheet(f"""
                QPushButton {{
                    min-width: 25px;
                    min-height: 25px;
                    font-size: 25px;
                    color: {self._style["color"]};
                    border: 0px;
                    max-width: 25px;
                    max-height: 25px;
                    margin-top: 2px;
                    margin-bottom: 2px;
                    margin-left: 2px;
                    padding-top: -5px;
                }}
                QPushButton:hover {{
                    border: 2px solid {self._style["QPushButton:hover"]["border-color"]};
                }}
                QPushButton:disabled {{
                    background-color: {self._style["QPushButton:disabled"]["background-color"]};
               }}
            """)

    def _set_remove_button_stylesheet(self) -> None:
        """Set the remove button stylesheet."""

        # Set the remove button stylesheet if it exists.
        if self._remove_button is not None:
            self._remove_button.setStyleSheet(f"""
                QPushButton {{
                    min-width: 25px;
                    min-height: 25px;
                    font-size: 25px;
                    color: {self._style["color"]};
                    border: 0px;
                    max-width: 25px;
                    max-height: 25px;
                    margin-top: 2px;
                    margin-bottom: 2px;
                    padding-top: -5px;
                }}
                QPushButton:hover {{
                    border: 2px solid {self._style["QPushButton:hover"]["border-color"]};
                }}
                QPushButton:disabled {{
                    background-color: {self._style["QPushButton:disabled"]["background-color"]};
               }}
            """)

    def _set_grid_layout_header_stylesheet(self, label: QLabel) -> None:
        """
        Set the provided grid layout header stylesheet.

        :param label: The grid layout header to set the stylesheet.
        :type label: QLabel
        """

        # Set the provided grid layout header stylesheet.
        label.setStyleSheet(f"""
            QLabel {{
                property-alignment: AlignCenter;
                font-size: 16px;
                color: {self._style["color"]}; border: 1px solid white;
            }}
        """)

    def _set_grid_layout_widget_unselected_stylesheet(self, widget: QWidget, valid: bool = True) -> None:
        """
        Set the provided grid layout widget unselected stylesheet.
        If valid is False, color the widget border in red.

        :param widget: The grid layout widget to set the unselected stylesheet.
        :type widget: QWidget
        :param valid: If True, color the widget border in red.
        :type valid: bool
        """

        # Set the provided grid layout widget unselected stylesheet.
        widget.setStyleSheet(f"""
            property-alignment: AlignCenter;
            color: {self._style["color"] if valid else self._style["Custom"]["invalid-color"]};
            border: 2px solid {"white" if valid else self._style["Custom"]["invalid-color"]};
        """)

    def _set_grid_layout_widget_selected_stylesheet(self, widget: QWidget, valid: bool = True) -> None:
        """
        Set the provided grid layout widget selected stylesheet.
        If valid is False, color the widget border in red.

        :param widget: The grid layout widget to set the selected stylesheet.
        :type widget: QWidget
        :param valid: If True, color the widget border in red.
        :type valid: bool
        """

        # Set the provided grid layout widget selected stylesheet.
        widget.setStyleSheet(f"""
            property-alignment: AlignCenter;
            color: {self._style["color"] if valid else self._style["Custom"]["invalid-color"]};
            background-color: {self._style["Custom"]["selected-background-color"]};
            border: 2px solid {"white" if valid else self._style["Custom"]["invalid-color"]};
        """)

    def set_stylesheets(self) -> None:
        """Call every set_stylesheet method."""

        # Set the QConfigList StyleSheets.
        self._set_config_list_stylesheet()
        self._set_buttons_container_stylesheet()
        self._set_add_button_stylesheet()
        self._set_remove_button_stylesheet()
        if self._header_texts:
            for i in range(self._n):
                self._set_grid_layout_header_stylesheet(self._grid_layout.itemAt(i).widget())
        for i in range(self._n if self._header_texts is not None else 0, self._grid_layout.count(), self._n):
            row_widgets: Tuple[QWidget, ...] = tuple(self._grid_layout.itemAt(j).widget() for j in range(i, i+self._n))
            validity: bool = self._validity_function(*row_widgets)
            #print("ROW =", [r.text() for r in row_widgets])
            #print("VALIDITY =", validity)
            if i == self._selected_row:
                for widget in row_widgets:
                    self._set_grid_layout_widget_selected_stylesheet(widget, validity)
            else:
                for widget in row_widgets:
                    self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

    # =============================== #
    # Attributes manipulation methods #
    # =============================== #

    def _unselect_row(self) -> None:
        """
        Update the selected_row attribute for unselecting the (potentially)
        already selected row and disable the remove ('-') button.
        """

        # Update the selected_row attribute.
        self._selected_row = -1

        # Disable the remove ('-') button.
        self._remove_button.setDisabled(True)

        # Clear the remove ('-') button focus
        # that just got transferred to a widget.
        if focused_widget := next(
            (
                self._grid_layout.itemAt(i).widget() for i in range(self._grid_layout.count())
                if self._grid_layout.itemAt(i).widget().hasFocus()
            ),
            None
        ):
            focused_widget.clearFocus()

    def _select_row(self, row_number: int) -> None:
        """
        Update the selected_row attribute for selecting the
        provided row number row and enable the remove ('-') button.
        """

        # Update the selected_row attribute.
        self._selected_row = row_number

        # Enable the remove ('-') button.
        if not self._no_buttons:
            self._remove_button.setDisabled(False)

    # ===================== #
    # Pseudo getter methods #
    # ===================== #

    @property
    def default_style(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """
        Pseudo getter method for the default QConfigList style dictionary.

        :returns: The default QConfigList style dictionary.
        :rtype: Dict[str, Union[str, Dict[str, str]]]
        """

        # Return the default QConfigList style dictionary.
        return {
            "color"                : "#FFFFFF",
            "background-color"     : "#000000",
            "QPushButton:disabled" : {
                "background-color"          : "#333333",
            },
            "QPushButton:hover"    : {
                "border-color"              : "#4488BB",
            },
            "Custom"               : {
                "invalid-color"             : "#FF0000",
                "selected-background-color" : "#6688BB"
            }
        }

    @property
    def widgets(self) -> List[Tuple[QWidget, ...]]:
        """
        Pseudo getter method for the row widgets within the QConfigList.
        Headers are not part of the returned row widgets list.

        :returns: The row widgets within the QConfigList.
        :rtype: List[Tuple[QWidget, ...]]
        """

        # Return the row widgets within the QConfigList.
        return [
            tuple(
                self._grid_layout.itemAtPosition(i, j).widget() for j in range(self._n)
                if self._grid_layout.itemAtPosition(i, j) is not None
            )
            for i in range(int(self._header_texts is not None)+1, self._grid_layout.rowCount())
                if self._grid_layout.rowStretch(i)
        ]

    @property
    def widgets_content(self) -> List[Tuple[Any, ...]]:
        """
        Pseudo getter method for the content of the row widgets within the QConfigList.
        Headers are not part of the returned row widgets list.

        :returns: The content of the row widgets within the QConfigList.
        :rtype: List[Tuple[Any, ...]]
        """
        return [
            tuple(self._content_function(widget) for widget in row_widgets)
            for row_widgets in self.widgets
        ]

    @property
    def is_valid(self) -> bool:
        """
        Pseudo getter method for the validity of every grid layout rows.

        :returns: The validity of every grid layout rows.
        :rtype: bool
        """

        # Use regex to match any occurrence of the Custom{invalid-color}
        # within the grid layout widgets stylesheets.
        for i in range(self._n if self._header_texts is not None else 0, self._grid_layout.count(), self._n):
            if re.search(
                self._valid_grid_layout_pattern,
                self._grid_layout.itemAt(i).widget().styleSheet(),
                re.IGNORECASE
            ) is not None:
                return False

        # Return True if no occurrence has been found.
        return True

# =------------------------------------------------------------------------------------------------------------------= #
