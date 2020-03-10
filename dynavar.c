#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dynavar.h"


Var new_int_var(int x)
{
    Var var;
    var.type = "int";
    var.nxt = NULL;

    var.data = (int*)calloc(1, sizeof(int));
    *(int*)var.data = x;
    
    return var;
}

Var new_string_var(char *x)
{
    Var var;
    var.type = "string";
    var.nxt = NULL;

    var.data = (char*)calloc(strlen(x), sizeof(x)); //Test
    strcpy((char*)var.data, x);
    
    return var;
}

// Npi de si esto funciona
Var new_bool_var(bool x)
{
    Var var;
    var.type = "boolean";
    var.nxt = NULL;

    var.data = (bool*)calloc(1, sizeof(x));
    *(bool*)var.data = x;
    
    return var;
}


int main()
{
    int x = 1;
    printf("%ld\n", sizeof(x));
    
    Var s = new_string_var("holaaa");
    printf("%s -> %ld\n", (char*)s.data, strlen(s.data));

    Var b = new_bool_var(false);
    if (*(bool*)b.data == true) printf("true\n");
    else if(*(bool*)b.data == false) printf("false\n");

    return 0;
}