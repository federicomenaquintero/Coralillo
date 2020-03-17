#!/bin/bash
gcc tests/dynavar_tests.c src/dynavar.c -o dynavar_tests && ./dynavar_tests
rm dynavar_tests