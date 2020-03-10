#ifndef __DYNAVAR
#define __DYNAVAR

typedef enum
{
    false,
    true
} bool;

enum t_typenames 
{
    TYPENAME_BOOL,
    TYPENAME_STRING,
    TYPENAME_INT,
};

#define typename(x) _Generic((x),   \
    char* : TYPENAME_STRING,        \
    int*  : TYPENAME_INT,           \
    bool* : TYPENAME_BOOL)          \


typedef struct
{
    char *type;
    void *data;
    void *nxt;
} Var;


Var new_int_var(int x);
Var new_string_var(char *x);
Var new_bool_var(bool x);

#endif

/*
Var almacena la información que está almacenando (la variable dinámica)
y, al mismo tiempo, una dirección en memoria al siguiente eslabón del arreglo
(Si la dirección es NULL ahí acaba el arreglo).
*/
