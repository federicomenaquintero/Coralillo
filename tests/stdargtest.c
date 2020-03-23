#include <stdio.h>
#include <stdarg.h>
#include "../src/dynavar.h"

/*
#define vtypeof(a) _Generic((a),    \
    int   : TYPE_INT,               \
    char* : TYPE_STRING,            \
    bool  : TYPE_BOOL,              \
    Var   : TYPE_VAR)
*/

int main()
{
    List list = NEW_LIST("biiis", false, 2, 3, 94, "Hola");
    print_list(&list);
    return 0;
}