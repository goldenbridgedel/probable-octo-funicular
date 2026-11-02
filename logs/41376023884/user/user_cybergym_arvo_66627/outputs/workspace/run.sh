#!/bin/bash

export ASAN_OPTIONS=handle_segv=0:handle_sigbus=0:handle_abort=0:disable_coredump=0:abort_on_error=1
export UBSAN_OPTIONS=handle_segv=0:halt_on_error=1:abort_on_error=1

if nm /out/matio_fuzzer | grep -q __afl_area_ptr ; then
    exec /out/matio_fuzzer $@
else
    exec /out/matio_fuzzer -handle_segv=0 -handle_abrt=0 -verbosity=0 $@
fi