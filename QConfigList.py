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
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
"""

# =--------------= #
# Libraries import #
# =--------------= #

from typing            import Callable, Dict, List, Optional, Tuple, Type, Union
from PySide6.QtCore    import Qt, QEvent
from PySide6.QtGui     import QMouseEvent
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, \
    QWidget
import re

# =-------------------------------------------------------------------------------------------------------------= #


# =--------= #
# Authorship #
# =--------= #

__author__       = "Quentin Raimbaud"
__contact__      = "quentin.raimbaud.contact@gmail.com"
__date__         = "2024-03-23"
__license__      = "LGPL-2.1"
__maintainer__   = "Quentin Raimbaud"
__status__       = "Development"
__version__      = "1.0.2"

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
            parent: Optional[QWidget] = None,
            f: Qt.WindowType = Qt.WindowFlags,
            n: Optional[int] = None,
            max_rows: Optional[int] = None,
            header_texts: Optional[Union[Tuple[str, ...], List[str]]] = None,
            row_widgets: Optional[Union[Type[str, ...], List[Type]]] = None,
            default_row_widget_texts: Optional[Union[Tuple[str, ...], List[str]]] = None,
            initial: Optional[
                Union[
                    Tuple[Union[Tuple[QWidget, ...], List[QWidget]]],
                    List[Union[Tuple[QWidget, ...], List[QWidget]]]
                ]
            ] = None,
            validity_function: Optional[Callable[..., bool]] = None,
            no_buttons: bool = False,
            no_verif: bool = False,
            style: Optional[Dict[str, Union[str, Dict[str, str]]]] = None
    ) -> None:
        """
        Initializer method.
        If parent is provided, set such a parent to the QConfigList.
        If f is provided, set such WindowFlags to the QConfigList.
        If n is provided, use such number of columns per row.
        If max_rows is provided, use such a maximum number of rows. Headers are not taken into account for computing \
the current number of rows.
        If header_texts is provided, create QLabel with such header_texts to the QConfigList.
        If row_widgets is provided, use such widgets for each row of the QConfigList.
        If default_row_widget_texts is provided, use such default row widget texts of the QConfigList.
        If initial is provided, fill the QConfigList's grid layout with the given widgets.
        If validity_function is provided, use such a function to validate the content of a row giving every row's \
QWidget as parameters.
        If style is provided, use such a style dictionary for the QConfigList.

        :param parent: The optional parent of the QConfigList to instantiate. By default, None.
        :type parent: QWidget or None
        :param f: The optional WindowFlags of the QConfigList to instantiate. By default, None.
        :type f: Qt.WindowFlags
        :param n: The number of columns of the QConfigList to instantiate. By default, None. If None but header_texts \
or row_widgets or default_row_widget_texts are not None, use the length of such arguments in this order of priority: \
header_texts > row_widgets > default_row_widget_texts. If all of these 3 arguments are None, use 2.
        :type n: int or None
        :param max_rows: The optional maximum number of rows. By default, None.
        :type max_rows: int or None
        :param header_texts: The optional header texts of the QConfigList to instantiate. By default, None.
        :type header_texts: Tuple[str, ...] or List[str] or None
        :param row_widgets: The optional widgets of the QConfigList to instantiate. By default, None. If None, use one \
QLabel and QLineEdit for the rest of the rows if n <1, otherwise use a single QLineEdit.
        :type row_widgets: Tuple[Type, ...] or List[Type] or None
        :param default_row_widget_texts: The optional default row widget texts of the QConfigList to instantiate. By \
default, None. If None, use empty strings for the whole rows.
        :type default_row_widget_texts: Tuple[str, ...] or List[str] or None
        :param initial: The optional widgets to add to the QConfigList's grid layout. By default, None.
        :type initial: Tuple[Tuple[QWidget, ...] or List[QWidget]] or List[Tuple[QWidget, ...] or List[QWidget]] or None
        :param validity_function: The optional validity function used to validate the content of a row. It takes every \
row's QWidget as parameters. By Default, None. If None, return True anyway.
        :type validity_function: Optional[Callable[..., bool]]
        :param no_buttons: If True, don't create the add/remove ('+'/'-') buttons. By default, False.
        :type no_buttons: bool
        :param no_verif: If True, performs no verification on the provided arguments. By default, False.
        :type no_verif: bool
        :param style: The optional style dictionary used for the QConfigList. This style dictionary should match the \
style format introduced by the HotClick software. By default, None. If None, use the QConfigList's default style \
dictionary
        :type style: Optional[Dict[str, Union[str, Dict[str, str]]]]
        """

        # Calling the super class's initializer method.
        super().__init__(parent=parent, f=f)

        # Set default arguments for the mutable arguments.
        if n is None:
            if header_texts is not None:
                n = len(header_texts)
            elif row_widgets is not None:
                n = len(row_widgets)
            elif default_row_widget_texts is not None:
                n = len(default_row_widget_texts)
        if row_widgets is None:
            if n > 1:
                row_widgets = (QLabel, *tuple(QLineEdit for _ in range(n - 1)))
            else:
                row_widgets = QLineEdit,
        if default_row_widget_texts is None:
            default_row_widget_texts = tuple("" for _ in range(n))
        if validity_function is None:
            def validity_function(*_args: QWidget) -> bool:
                """Default validity function: return True anyway."""
                return True
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
                if any((tuple(type(widget) for widget in widgets) != row_widgets for widgets in initial)):
                    raise ValueError(
                        f"Inconsistent type of initial widgets per row to fill. "
                        f"Expected {row_widgets} but got "
                        f"{list(set(tuple(type(widget) for widget in widgets) for widgets in initial))}."
                    )

        # Set the straight-forward attributes.
        self._n: int = n
        self._max_rows: int = max_rows
        self._first_row_index: int = 0 if header_texts is None else n
        self._selected_row: int = -1
        self._header_texts: Optional[Union[Tuple[str, ...], List[str]]] = header_texts
        self._row_widgets: Union[Tuple[Type, ...], List[Type]] = row_widgets
        self._default_row_widget_texts: Union[Tuple[str, ...], List[str]] = default_row_widget_texts
        self._initial: Optional[
                Union[
                    Tuple[Union[Tuple[QWidget, ...], List[QWidget]]],
                    List[Union[Tuple[QWidget, ...], List[QWidget]]]
                ]
            ] = initial
        self._validity_function: Callable[..., bool] = validity_function
        self._valid_grid_layout_pattern: str = r"color\s*:\s*" + style["Custom"]["invalid-color"] + r"\s*;"
        self._no_buttons: bool = no_buttons
        self._style: Dict[str, Union[str, Dict[str, str]]] = style

        # Initialize the QConfigList UI.
        self._init_ui()

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
        if not self._no_buttons:
            self._buttons_container: QWidget = QWidget()
            self._set_buttons_container_stylesheet()
            buttons_layout: QHBoxLayout = QHBoxLayout(self._buttons_container)
            buttons_layout.setSpacing(0)
            buttons_layout.setContentsMargins(0, 0, 0, 0)

            # Initialize, configure and connect the add ('+') button.
            # Then, add it to the buttons container widget.
            self._add_button: QPushButton = QPushButton("+")
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
            self._widget_clicked(watched)

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
        self._add_grid_layout_widgets(*labels)

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
                if isinstance(widget, QLineEdit):
                    widget.textChanged.connect(lambda _event, widget_=widget: self._widget_interacted(widget_))

            # Determine the validity of the widgets list to set their stylesheets correctly.
            validity: bool = self._validity_function(*widgets)
            for widget in widgets:
                self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

            # Call _add_grid_layout_widgets with the unpacked initialized widgets list.
            self._add_grid_layout_widgets(*widgets)

    # ================ #
    # Callback methods #
    # ================ #

    def _add_grid_layout_row(self) -> None:
        """
        Add a row to the grid layout.
        The row widgets used will be the one from the row_widgets attribute.
        The default row widget texts used will be the one from the default_row_widgets attribute.
        This method is a wrapper to add_grid_layout_row with some hardcoded arguments.
        """

        # Initialize the QWidgets list.
        widgets: List[QWidget] = []
        for i in range(len(self._default_row_widget_texts)):
            widget: QWidget = self._row_widgets[i](
                self._default_row_widget_texts[i]
            )
            widget.installEventFilter(self)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda _event, widget_=widget: self._widget_interacted(widget_))
            widgets.append(widget)

        # Determine the validity of the widgets list to set their stylesheets correctly.
        validity: bool = self._validity_function(*widgets)
        for widget in widgets:
            self._set_grid_layout_widget_unselected_stylesheet(widget, validity)

        # Call _add_grid_layout_widgets with the unpacked initialized widgets list.
        self._add_grid_layout_widgets(*widgets)

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
        for _ in range(i, i+self._n):
            widget: QWidget = self._grid_layout.itemAt(i).widget()
            self._grid_layout.removeWidget(widget)
            widget.deleteLater()

        # Unselect the row.
        self._unselect_row()

        # If the add ('+') button is
        # disabled, enable it.
        self._add_button.setDisabled(False)

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
        self._widget_clicked(widget, no_select=True)

        # Ensure the validity of the row and edit the widget stylesheets.
        validity: bool = self._validity_function(*widgets)
        for widget in widgets:
            self._set_grid_layout_widget_selected_stylesheet(widget, validity)

    # ========================= #
    # Private low-level methods #
    # ========================= #

    def _add_grid_layout_widgets(self, *widgets: QWidget) -> None:
        """
        Add the provided widgets to the grid layout.

        :param *widgets: The widgets to add to the grid layout.
        :type *widgets: QWidget
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
        self._grid_layout.setRowStretch(row_number, 1)

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

        # Set the buttons container stylesheet.
        self._buttons_container.setStyleSheet("""
            QWidget {
                border: 1px solid white;
            }
        """)

    def _set_add_button_stylesheet(self) -> None:
        """Set the add button stylesheet."""

        # Set the add button stylesheet.
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

        # Set the remove button stylesheet.
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
            color: {self._style["color"]}; border: 1px solid white;
        """)

    def _set_grid_layout_widget_unselected_stylesheet(self, widget: QWidget, valid: bool = True) -> None:
        """
        Set the provided grid layout widget unselected stylesheet.
        If valid is False, color the widget text in red.

        :param widget: The grid layout widget to set the unselected stylesheet.
        :type widget: QWidget
        :param valid: If True, color the widget text in red.
        :type valid: bool
        """

        # Set the provided grid layout widget unselected stylesheet.
        widget.setStyleSheet(f"""
            color: {self._style["color"] if valid else self._style["Custom"]["invalid-color"]};
            border: 1px solid white;
        """)

    def _set_grid_layout_widget_selected_stylesheet(self, widget: QWidget, valid: bool = True) -> None:
        """
        Set the provided grid layout widget selected stylesheet.
        If valid is False, color the widget text in red.

        :param widget: The grid layout widget to set the selected stylesheet.
        :type widget: QWidget
        :param valid: If True, color the widget text in red.
        :type valid: bool
        """

        # Set the provided grid layout widget selected stylesheet.
        widget.setStyleSheet(f"""
            background-color: {self._style["Custom"]["selected-background-color"]};
            color: {self._style["color"] if valid else self._style["Custom"]["invalid-color"]};
            border: 1px solid white;
        """)

    # ============================== #
    # Attribute manipulation methods #
    # ============================== #

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
    def valid(self) -> bool:
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
