#include <stdio.h>
#include <stdarg.h>
#include "../src/dynavar.h"

#define vtypeof(a) _Generic((a),    \
    int   : TYPE_INT,               \
    char* : TYPE_STRING,            \
    bool  : TYPE_BOOL,              \
    void* : TYPE_NONE,              \
    Var   : TYPE_VAR)

int func(int num_of_args, ...)
{
    va_list args;
    va_start(args, num_of_args);
    int total = 0;

    for (int i = 0; i < num_of_args; i++)
        total += va_arg(args, int);
    
    va_end(args);
    return total;
}

int main()
{
    printf("%d\n", func(3, 1, 2, 1));
}
