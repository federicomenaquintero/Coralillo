#include <stdio.h>
#include <string.h>

typedef void(*voidfunc)();

typedef struct
{
    char *s;
    size_t len;
} str;

void replace(str *string, char *text)
{
    string->s = text;
    string->len = strlen(text);
}

void append(str *string, char *text)
{
    strcat(string->s, text);
    string->len = strlen(string->s);
}

int main()
{
    return 0;
}
