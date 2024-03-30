
# QConfigList  
QConfigList is a single-file PySide6 custom QWidget representing a customizable list of QWidgets. It allows adding, removing, editing the content, the style, and verifying the QWidgets values easily.

## Installation
To use QConfigList, clone its repo or simply, download the QConfigList.py file. QConfigList need no more dependencies than PySide6.

## Getting started with QConfigList
The documentation is **as code** using reST: you fill find everything you want within the QConfigList.py file, but for the laziest among you, here's a quick summary of how to use QConfigList properly:

- **QConfigList**(**self**, **parent**: _typing.Optional[QWidget] = None_, **f**: _Qt.WindowType = Qt.WindowFlags_, **n**: _typing.Optional[int] = None_, **max_rows**: _typing.Optional[int] = None_, **header_texts**: _typing.Optional[typing.Tuple[str, ...]] = None_, **row_widgets**: _typing.Optional[typing.Tuple[typing.Type, ...]] = None_, **default_row_widget_texts**: _typing.Optional[typing.Tuple[str, ...]] = None_, **initial**: _typing.Optional[typing.List[typing.Tuple[QWidget, ...]]] = None_, **validity_function**: _typing.Optional[typing.Callable[..., bool]] = None_, **no_buttons**: _bool = False_, **no_verif**: _bool = False_, **style**: _typing.Optional[typing.Dict[str, typing.Union[str, typing.Dict[str, str]]]] = None_)
    - If parent is provided, set such a parent to the QConfigList.
    - If f is provided, set such WindowFlags to the QConfigList.
    - If n is provided, use such number of columns per row.
    - If max_rows is provided, use such a maximum number of rows. Headers are not taken into account for computing the current number of rows.
    - If header_texts is provided, create QLabel with such header_texts to the QConfigList.
    - If row_widgets is provided, use such widgets for each row of the QConfigList.
    - If default_row_widget_texts is provided, use such default row widget texts of the QConfigList.
    - If initial is provided, fill the QConfigList's grid layout with the given widgets.
    - If validity_function is provided, use such a function to validate the content of a row giving every row's QWidget as parameters.  
    - If style is provided, use such a style dictionary for the QConfigList.
  
 - **default_style**: typing.Dict[str, typing.Union[str, typing.Dict[str, str]]]_
     - Attribute returning the default style dictionary of the QConfigList.
   
 - **valid**: _bool_
     - Attribute returning the boolean validity of every row within the QConfigList.
  