/*

struct Var is a container with the folowing structure:
Var {
    var_type    // Type of the data is storing.
    data        // Actual sored data. This can also be another Var.
    asoc        // Some other related Var called asociate.
}

Asociates are used to make lists. A Var can only have one asociate.

*/


#ifndef __DYNAVAR
#define __DYNAVAR

typedef enum
{
    false,
    true
} bool;

typedef enum var_types
{
    TYPE_INT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_VAR,
    TYPE_NONE
} var_types;

typedef struct Var
{
    var_types type;
    void *data;
    void *asoc;
} Var;

Var new_int_var(int x);
Var new_string_var(char *x);
Var new_bool_var(bool x);

#define NEW_VAR(var) _Generic((var),    \
    int   : new_int_var,                \
    char* : new_string_var,             \
    bool  : new_bool_var)(var)

Var *new_int_asoc(int x);
Var *new_string_asoc(char* x);
Var *new_bool_asoc(bool x);

void add_int_asoc(Var *var, int asoc_type);
void add_string_asoc(Var *var, char* asoc_type);
void add_bool_asoc(Var *var, bool asoc_type);

#define ADD_NEW_ASOC(varptr, asoc) _Generic((asoc), \
    int   : add_int_asoc,                           \
    char* : add_string_asoc,                        \
    bool  : add_bool_asoc)(varptr, asoc)

void del_var(Var *var);

var_types type(Var *var);

#endif
