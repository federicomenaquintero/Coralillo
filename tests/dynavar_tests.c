// Compile with gcc tests/dynavar_tests.c src/dynavar.c -o dynavar_tests && ./dynavar_tests
// Or, run run_tests.sh

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

void test_add_int_asoc(void)
{
    Var i = NEW_VAR(10);
    add_int_asoc(&i, 10);

    int asoc_data = *(int*)((Var*)i.asoc)->data;
    TEST_ASSERT_EQUAL(10, asoc_data);
}

void test_add_string_asoc(void)
{
    Var s = NEW_VAR(10);
    add_string_asoc(&s, "hola");

    char* asoc_data = (char*)((Var*)s.asoc)->data;
    int asoc_cmp = strcmp("hola", asoc_data);
    TEST_ASSERT_EQUAL(0, asoc_cmp);
}

void test_add_bool_asoc(void)
{
    Var b = NEW_VAR("Hola");
    add_bool_asoc(&b, true);

    bool asoc_data = *(bool*)((Var*)b.asoc)->data;
    TEST_ASSERT_EQUAL(true, asoc_data);
}

void test_new_asoc_macro(void)
{
    Var i = NEW_VAR(10); /* INT */
    ADD_NEW_ASOC(&i, 10);

    int asoc_int = *(int*)((Var*)i.asoc)->data;
    TEST_ASSERT_EQUAL(10, asoc_int);

    Var s = NEW_VAR("Hola"); /* STRING */
    ADD_NEW_ASOC(&s, "Juanito");

    char* asoc_str = (char*)((Var*)s.asoc)->data;
    int asoc_cmp = strcmp("Juanito", asoc_str);
    TEST_ASSERT_EQUAL(0, asoc_cmp);

    Var b = NEW_VAR(true); /* INT */
    ADD_NEW_ASOC(&b, false);

    bool asoc_bool = *(bool*)((Var*)b.asoc)->data;
    TEST_ASSERT_EQUAL(false, asoc_bool);
}

int main()
{
    UnityBegin("tests/dynavar_tests.c");

    RUN_TEST(test_new_int_var_using);
    RUN_TEST(test_new_string_var);
    RUN_TEST(test_new_bool_var);
    RUN_TEST(test_new_var_macro);

    RUN_TEST(test_add_int_asoc);
    RUN_TEST(test_add_string_asoc);
    RUN_TEST(test_add_bool_asoc);
    RUN_TEST(test_new_asoc_macro);

    return UnityEnd();
}