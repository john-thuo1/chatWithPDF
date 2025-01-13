"""

This package provides an abstraction for users to easily access PDF processing functions 
via the `_module_lookup` dictionary.

"""

_module_lookup = {
    "extract_text_with_page_numbers": "modules.process_data",
    "process_text_with_splitter": "modules.process_data"
}


__all__ = ['_module_lookup']

