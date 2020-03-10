#include <stdio.h>
#include <stdlib.h>
#include "dynavar.h"


Var new_int_var(int x)
{
    Var var;
    var.type = "int";
    var.nxt = NULL;

    var.data = (int*)malloc(sizeof(int));
    *(int*)var.data = x;
    return var;
}

// Lists
int main()
{
    Var a = new_int_var(10);
    printf("%d\n", *(int*)a.data);
    printf("%s\n", a.type);
    return 0;
}