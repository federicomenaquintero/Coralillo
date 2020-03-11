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

#define typename(t) _Generic((t),       \
    char* : TYPE_STRING,                \
    int*  : TYPE_INT,                   \
    bool* : TYPE_BOOL)                  \


typedef struct
{
    var_type type;
    void *data;
    void *nxt;
} Var;


Var new_int_var(int x);
Var new_string_var(char *x);
Var new_bool_var(bool x);

#define new_var(var) _Generic((var),    \
    char* : new_string_var,             \
    int   : new_int_var,                \
    bool  : new_bool_var) (var)


#endif

/*
Var almacena la información que está almacenando (la variable dinámica)
y, al mismo tiempo, una dirección en memoria al siguiente eslabón del arreglo
(Si la dirección es NULL ahí acaba el arreglo).
*/
