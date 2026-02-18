#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **forward reference proxy** (i.e., low-level objects created by the
:func:`beartype._check.forward.reference.fwdrefmake` submodule) data submodule.

This submodule predefines forward reference proxies that test known edge cases
on behalf of higher-level unit test submodules.
'''

# ....................{ IMPORTS                            }....................
from beartype._check.forward.reference.fwdrefmake import (
    make_forwardref_subbable_subtype)

# ....................{ CONSTANTS                          }....................
PACKAGE_NAME = 'beartype_test.a00_unit.data'
'''
Fully-qualified name of a subpackage defining an arbitrary submodule.
'''


MODULE_BASENAME = 'data_type'
'''
Unqualified basename of a submodule in that subpackage defining an arbitrary
class.
'''


MODULE_NAME = f'{PACKAGE_NAME}.{MODULE_BASENAME}'
'''
Fully-qualified name of the same submodule.
'''


CLASS_BASENAME = 'Class'
'''
Unqualified basename of that type in that module.
'''


CLASS_NAME = f'{MODULE_NAME}.{CLASS_BASENAME}'
'''
Fully-qualified name of that type.
'''


SCOPE_NAME = __name__
'''
Fully-qualified name of the current test module.
'''

# ....................{ FORWARDREFS ~ invalid              }....................
FORWARDREF_RELATIVE_CIRCULAR = make_forwardref_subbable_subtype(
    # Unqualified basename of this global currently being declared.
    hint_name='FORWARDREF_RELATIVE_CIRCULAR',
    # Fully-qualified name of the current test module.
    scope_name=SCOPE_NAME,
)
'''
**Circular forward reference proxy** (i.e., invalid proxy circularly and thus
recursively referring to the same forward reference proxy).

Since the only means of declaring a circular forward reference proxy is as a
global attribute, the declaration of this proxy is necessarily isolated to its
own data submodule.
'''

# ....................{ FORWARDREFS ~ valid                }....................
FORWARDREF_ABSOLUTE = make_forwardref_subbable_subtype(
    hint_name=CLASS_NAME,
    # Intentionally ignored fully-qualified name of this test submodule.
    scope_name=SCOPE_NAME,
)
'''
Forward reference proxy to an unsubscripted type referenced by an absolute
(i.e., fully-qualified) name.
'''


FORWARDREF_RELATIVE = make_forwardref_subbable_subtype(
    hint_name=CLASS_BASENAME, scope_name=MODULE_NAME)
'''
Forward reference proxy to an unsubscripted type referenced by a relative (i.e.,
unqualified) name.
'''


FORWARDREF_MODULE_ABSOLUTE = make_forwardref_subbable_subtype(
    hint_name=MODULE_NAME,

    # Intentionally ignored fully-qualified name of this test submodule.
    scope_name=SCOPE_NAME,
)
'''
Forward reference proxy to a submodule of a subpackage referenced with an
absolute (i.e., fully-qualified) name.
'''


FORWARDREF_MODULE_CLASS = FORWARDREF_MODULE_ABSOLUTE.Class
'''
Forward reference proxy to an unsubscripted class of that submodule, accessed by
``"."``-delimited attribute syntax from an existing forward reference proxy.
'''
