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

Var *new_int_asoc(int x)
{
    // Asociate value = *(int*)((Var*)var.asoc)->data)

    Var asoc = new_int_var(x);
    Var* space = (Var*)calloc(1, sizeof(asoc));
    *space = asoc;

    return space;
}

Var *new_string_asoc(char* x)
{
    // Asociate value = (char*)((Var*)var.asoc)->data

    Var asoc = new_string_var(x);
    Var* space = (Var*)calloc(1, sizeof(asoc));
    *space = asoc;

    return space;
}

Var *new_bool_asoc(bool x)
{
    // Asociate value = *(bool*)((Var*)var.asoc)->data

    Var asoc = new_bool_var(x);
    Var* space = (Var*)calloc(1, sizeof(asoc));
    *space = asoc;

    return space;
}

void add_int_asoc(Var *var, int asoc_type)
{
    var->asoc = new_int_asoc(asoc_type);
}

void add_string_asoc(Var *var, char* asoc_type)
{
    var->asoc = new_string_asoc(asoc_type);
}

void add_bool_asoc(Var *var, bool asoc_type)
{
    var->asoc = new_bool_asoc(asoc_type);
}

void del_var(Var *var)
{
    free(var->asoc);
    free(var->data);
}

var_types type(Var *var)
{
    return var->type;
}

