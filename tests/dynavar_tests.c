// Compile with gcc tests/dynavar_tests.c src/dynavar.c -o dynavar_tests && ./dynavar_tests

#include <string.h>
#include "unity/unity.c"
#include "../src/dynavar.h"

void setUp() {}
void tearDown() {}

void test_new_int_var_using(void)
{
    Var v = new_int_var(10);
    TEST_ASSERT_EQUAL(10, *(int*)v.data);
}

void test_new_string_var(void)
{
    Var v = new_string_var("testing");
    int cmp = strcmp("testing", (char*)v.data);
    TEST_ASSERT_EQUAL(0, cmp);
}

void test_new_bool_var(void)
{
    Var v = new_bool_var(true);
    TEST_ASSERT_EQUAL(true, *(bool*)v.data);
}

void test_new_var_macro(void)
{
    Var i = NEW_VAR(5);       /* INT */
    TEST_ASSERT_EQUAL(5, *(int*)i.data);

    Var s = NEW_VAR("s");   /* STRING */
    int cmp = strcmp("s", (char*)s.data);
    TEST_ASSERT_EQUAL(0, cmp);

    Var b = NEW_VAR(false);  /* BOOL */
    TEST_ASSERT_EQUAL(false, *(bool*)b.data);
}

void test_new_int_asoc(void)
{
    Var a = NEW_VAR(10);
    a.asoc = add_int_asoc(202);

    int asoc_data = *(int*)((Var*)a.asoc)->data;
    TEST_ASSERT_EQUAL(202, asoc_data);
}

void test_new_string_asoc(void)
{
    Var a = NEW_VAR(10);
    a.asoc = add_string_asoc("hola");

    char* asoc_data = (char*)((Var*)a.asoc)->data;
    int cmp = strcmp("hola", asoc_data);
    TEST_ASSERT_EQUAL(0, cmp);
}

void test_new_bool_asoc(void)
{
    Var a = NEW_VAR(10);
    a.asoc = add_bool_asoc(true);

    bool asoc_data = *(bool*)((Var*)a.asoc)->data;
    TEST_ASSERT_EQUAL(true, asoc_data);
}

int main()
{
    UnityBegin("tests/dynavar_tests.c");

    RUN_TEST(test_new_int_var_using);
    RUN_TEST(test_new_string_var);
    RUN_TEST(test_new_bool_var);
    RUN_TEST(test_new_var_macro);

    RUN_TEST(test_new_int_asoc);
    RUN_TEST(test_new_string_asoc);
    RUN_TEST(test_new_bool_asoc);

    return UnityEnd();
}