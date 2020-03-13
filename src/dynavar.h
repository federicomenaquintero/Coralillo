#ifndef __DYNAVAR
#define __DYNAVAR

typedef enum
{
    false,
    true
} bool;

typedef enum 
{
    TYPE_STRING,
    TYPE_INT,
    TYPE_BOOL
} var_type;

/* Probably useless */
#define typename(t) _Generic((t),       \
    char* : TYPE_STRING,                \
    int*  : TYPE_INT,                   \
    bool* : TYPE_BOOL)                  \

typedef struct
{
    var_type type;
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

Var *add_int_asoc(int x);
Var *add_string_asoc(char* x);
Var *add_bool_asoc(bool x);

#define NEW_ASOC(asoc) _Generic((asoc), \
    int   : *add_int_asoc,              \
    char* : *add_string_asoc,           \
    bool  : *add_bool_asoc)(asoc)

#endif

/*
Var almacena la información que está almacenando (la variable dinámica)
y, al mismo tiempo, una dirección en memoria al siguiente eslabón del arreglo
(Si la dirección es NULL ahí acaba el arreglo).
*/
