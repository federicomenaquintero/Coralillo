#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
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


List NEW_LIST(char *fmt, ...)
{
    /*
    Format(fmt) types:
    'i'  ->  int
    's'  ->  string
    'b'  ->  bool
    'l'  ->  List
    */
    va_list args;
    va_start(args, fmt);

    Var list_head;
    Var *last_Var_parent = &list_head;

    if (*fmt == 'i')
        list_head = NEW_VAR(va_arg(args, int));
    else if (*fmt == 's')
        list_head = NEW_VAR(va_arg(args, char*));
    else if (*fmt == 'b')
        list_head = NEW_VAR(va_arg(args, bool));
    else if (*fmt == 'l')
        list_head = NEW_VAR(-1);
    // In this case, i'll have to call this same function again
    // to make the other list first, then resume the creation
    // of the first list.

    *fmt++;

    while(*fmt)
    {
        switch(*fmt++)
        {
        case 'i':
            ADD_NEW_ASOC(last_Var_parent, va_arg(args, int));
            last_Var_parent->in_list = true;
            last_Var_parent = (Var*)last_Var_parent->asoc;
            break;

        case 's':
            ADD_NEW_ASOC(last_Var_parent, va_arg(args, char*));
            last_Var_parent->in_list = true;
            last_Var_parent = (Var*)last_Var_parent->asoc;
            break;

        case 'b':
            ADD_NEW_ASOC(last_Var_parent, va_arg(args, bool));
            last_Var_parent->in_list = true;
            last_Var_parent = (Var*)last_Var_parent->asoc;
            break;

        case 'l':

            break;

        default:
            continue;
            break;
        }

        // Call function to add 1 to var value
    }

    va_end(args);
    
    Var *list_space = (Var*)calloc(1, sizeof(list_head));
    *list_space = list_head;

    List new_list;
    new_list.first_elem = list_space;
    
    return new_list;
}

// List CREATE_NEW_LIST(char *fmt, char *data)
// {
//     /*
//     Format(fmt) types:
//     'i'  ->  int
//     's'  ->  string
//     'b'  ->  bool
//     'l'  ->  List

//     Data:
//     int     ->  i[...]
//     string  ->  s[...]
//     bool    ->  b[...]
//     list    ->  l[...]
//     */

//     Var list_head;
//     Var *last_Var_parent = &list_head;

// }

// Add case for nested list
void print_var_data(Var *v)
{
    switch (v->type)
    {
    case TYPE_INT:
        printf("%d ", *(int*)v->data);
        break;

    case TYPE_STRING:
        printf("%s ", (char*)v->data);
        break;

    case TYPE_BOOL:
        printf((*(bool*)v->data == true) ? "True " : "False ");
        break;

    default:
        break;
    }
}

void print_list(List *list)
{
    Var *last_parent = list->first_elem;
    while(last_parent->asoc != NULL)
    {
        print_var_data(last_parent);
        last_parent = (Var*)last_parent->asoc;
    }
    print_var_data(last_parent);
}