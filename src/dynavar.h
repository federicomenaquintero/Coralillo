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
    TYPE_NONE
} var_types;

typedef struct
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




/*

Var contiene dos formas de datos:
- data: el dato inmediato (un número, un string, un booleano).
- asoc: aquel otro Var con tendrá algúna relación (principalmente para listas).

Tendrá un tipo específico de dato a menos que tenga un asociado, en cuyo caso
el tipo será: (data_types)TYPE + LIST

Una lista sencilla, al descomponerla sería así:

Var a = 10
Var b = "hola"
Var c = true

Var a.asoc = Var b
Var b.asoc = Var c

Eso es equivalente a: Var a = [10, "hola", true]

Una lista con listas adentro:

Var a = [Var1, Var2, Var3]          # una lista
Var b = [Var4, Var5]                # otra lista
Var c = [Var6, Var7, Var8, Var9]    # una lista más

# Var1.asoc = Var b
# Var2.asoc = Var c
# Var3.asoc = NULL

De esta forma:
Var a = [
    [Var4.data, Var5.data],                         # Esto sería Var1
    [Var6.data, Var7.data, Var8.data, Var9.data],   # Esto Var2
    Var3.data                                       # Y aquí Var3
]

*/
