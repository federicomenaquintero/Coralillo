// READ THE UNITY DOCS AND EXAMPLES

#include "unity/unity.c"

void setUp(){}
void tearDown(){}

void test_Cris_es_puto(void)
{
    TEST_ASSERT_MESSAGE(1, "Claro que es puto.");
}

int main()
{
    UnityBegin("tests/run_tests.c");
    RUN_TEST(test_Cris_es_puto, 3);
    return (UnityEnd());
}
