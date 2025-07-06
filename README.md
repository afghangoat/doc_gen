#Documentation generator for C/C++

A python script which can be used for generating a html documentation for the comments in your code.

##Features

- Custom pointer, end of linked list notation,
- Static notation,
- Doxygen-like commenting,
- Comes with English and Hungarian example config.

##Usage

The script only picks up these comments:
- `//? Is defining what the file content is used for.`
- `//- Is struct documentation`
- `//! Is function/method documentation`

###Configurable values

- `def_value_label`="<b>(Default value)</b>"
- `def_ret_label`="<b>Returns:</b>"
- `def_linked_label`="<b>Next linked list element</b>"
- `def_param_label`="<b>Parameters:</b>"
- `def_no_ret_label`="<i>(Has no return value)</i>"
- `def_no_par_label`="<b>(Has no input parameters)</b>"
- `def_comment_label`="Integer";
- `pointer_label`="(Pointer)";
- `static_var_ids`=[]
- `static_comments`=[]

First, you need to tune the script to fit your needs.

Then, run:

`python doc_generator.py`

After that, you need to specify:

- Documentation project name
- Create document from header files? (y/n)
- Create document from source .c files? (y/n)