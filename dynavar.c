#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dynavar.h"

Var new_int_var(int x)
{
    Var var;
    var.type = TYPE_INT;
    var.asoc = NULL;

    var.data = (int*)calloc(1, sizeof(int));
    *(int*)var.data = x;
    
    return var;
}

Var new_string_var(char *x)
{
    Var var;
    var.type = TYPE_STRING;
    var.asoc = NULL;

    var.data = (char*)calloc(strlen(x), sizeof(char));
    strcpy((char*)var.data, x);
    
    return var;
}

Var new_bool_var(bool x)
{
    Var var;
    var.type = TYPE_BOOL;
    var.asoc = NULL;

    var.data = (bool*)calloc(1, sizeof(bool));
    *(bool*)var.data = x;
    
    return var;
}

int main()
{
    Var a = new_var("Hola");
    printf("%s\n", (char*)a.data);

    return 0;
}
