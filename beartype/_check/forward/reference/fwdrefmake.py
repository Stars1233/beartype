#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **forward reference factories** (i.e.,  low-level callables creating
and returning forward reference proxy subclasses deferring the resolution of a
stringified type hint referencing an attribute that has yet to be defined and
annotating a class or callable decorated by the :func:`beartype.beartype`
decorator).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar import BeartypeDecorHintForwardRefException
from beartype._cave._cavefast import WeakrefCallableType
from beartype._cave._cavemap import NoneTypeOr
from beartype._data.typing.datatyping import (
    BeartypeForwardRef,
    BeartypeForwardRefArgs,
    FuncLocalParentCodeObjectWeakref,
    TupleTypes,
)
from beartype._check.forward.reference.fwdrefabc import (
    BeartypeForwardRefSubbableABC,
    BeartypeForwardRefSubbableABC_BASES,
    BeartypeForwardRefSubbedABC,
    BeartypeForwardRefSubbedABC_BASES,
)
from beartype._util.cls.utilclsmake import make_type
from beartype._util.text.utiltextidentifier import die_unless_identifier

# ....................{ FACTORIES                          }....................
def make_forwardref_subbable_subtype(
    # Mandatory parameters.
    hint_name: str,
    scope_name: str,

    # Optional parameters.
    func_local_parent_codeobj_weakref: FuncLocalParentCodeObjectWeakref = None,
) -> type[BeartypeForwardRefSubbableABC]:
    '''
    Create and return a new **subscriptable forward reference subclass** (i.e.,
    concrete subclass of the :class:`.BeartypeForwardRefSubbableABC` abstract
    base class (ABC) deferring the resolution of the unresolved type hint with
    the passed name, transparently permitting this type hint to be subscripted
    by any arbitrary child type hints).

    This factory is effectively memoized despite not being explicitly memoized
    (e.g., by the :func:`callable_cached` decorator), as the lower-level private
    :func:`._make_forwardref_subtype` factory called by this higher-level public
    factory is itself internally memoized.

    Parameters
    ----------
    hint_name : str
        Relative (i.e., unqualified) or absolute (i.e., fully-qualified) name of
        this unresolved type hint to be proxied.
    scope_name : str
        Possibly ignored fully-qualified name of the lexical scope in which this
        unresolved type hint was originally declared. For example:

        * ``"some_package.some_module"`` for a module scope (e.g., to
          resolve a global class or callable against this scope).
        * ``"some_package.some_module.SomeClass"`` for a class scope (e.g.,
          to resolve a nested class or callable against this scope).
    func_local_parent_codeobj_weakref : FuncLocalParentCodeObjectWeakref
        Proxy weakly referring to the code object underlying the lexical scope
        of the parent module, type, or callable whose body locally defines the
        locally decorated callable if this forward reference proxy subtype
        proxies a stringified forward reference annotating a locally decorated
        callable *or* :data:`None` otherwise. See also the
        :attr:`beartype._check.forward.reference.fwdrefabc.BeartypeForwardRefABC.__func_local_parent_codeobj_weakref_beartype__`
        class variable docstring for further details.

    Returns
    -------
    type[BeartypeForwardRefSubbableABC]
        Subscriptable forward reference proxy subclass proxying this type hint.

    Raises
    ------
    BeartypeDecorHintForwardRefException
        If either ``hint_name`` or ``scope_name`` are *not* syntactically valid
        ``"."``-delimited Python identifiers.
    '''

    # Subscriptable forward reference to be returned.
    return _make_forwardref_subtype(  # type: ignore[return-value]
        type_bases=BeartypeForwardRefSubbableABC_BASES,
        hint_name=hint_name,
        scope_name=scope_name,
        func_local_parent_codeobj_weakref=func_local_parent_codeobj_weakref,
    )


def make_forwardref_subbed_subtype(
    hint_name: str,
    scope_name: str,
    func_local_parent_codeobj_weakref: FuncLocalParentCodeObjectWeakref,
) -> type[BeartypeForwardRefSubbedABC]:
    '''
    Create and return a new **subscripted forward reference subclass** (i.e.,
    concrete subclass of the :class:`.BeartypeForwardRefSubbedABC` abstract
    base class (ABC) deferring the resolution of the unresolved type hint with
    the passed name, transparently prohibiting this type hint from being
    re-subscripted by any further child type hints).

    This factory is effectively memoized despite not being explicitly memoized
    (e.g., by the :func:`callable_cached` decorator), as the lower-level private
    :func:`._make_forwardref_subtype` factory called by this higher-level public
    factory is itself internally memoized.

    Parameters
    ----------
    hint_name : str
        Relative (i.e., unqualified) or absolute (i.e., fully-qualified) name of
        this unresolved type hint to be proxied.
    scope_name : str
        Possibly ignored fully-qualified name of the lexical scope in which this
        unresolved type hint was originally declared. See also
        :func:`.make_forwardref_subbable_subtype` docstring for further details.
    func_local_parent_codeobj_weakref : FuncLocalParentCodeObjectWeakref
        Proxy weakly referring to the code object underlying the lexical scope
        of the parent module, type, or callable whose body locally defines the
        locally decorated callable if this forward reference proxy subtype
        proxies a stringified forward reference annotating a locally decorated
        callable *or* :data:`None` otherwise. See also the
        :attr:`beartype._check.forward.reference.fwdrefabc.BeartypeForwardRefABC.__func_local_parent_codeobj_weakref_beartype__`
        class variable docstring for further details.

    Returns
    -------
    type[BeartypeForwardRefSubbedABC]
        Subscriptable forward reference proxy subclass proxying this type hint.

    Raises
    ------
    BeartypeDecorHintForwardRefException
        If either ``hint_name`` or ``scope_name`` are *not* syntactically valid
        ``"."``-delimited Python identifiers.
    '''

    # Subscriptable forward reference to be returned.
    return _make_forwardref_subtype(  # type: ignore[return-value]
        type_bases=BeartypeForwardRefSubbedABC_BASES,
        hint_name=hint_name,
        scope_name=scope_name,
        func_local_parent_codeobj_weakref=func_local_parent_codeobj_weakref,
    )

# ....................{ PRIVATE ~ factories                }....................
def _make_forwardref_subtype(
    type_bases: TupleTypes,
    hint_name: str,
    scope_name: str,
    func_local_parent_codeobj_weakref: FuncLocalParentCodeObjectWeakref,
) -> BeartypeForwardRef:
    '''
    Create and return a new **forward reference subclass** (i.e., concrete
    subclass of the passed abstract base class (ABC) transparently deferring the
    resolution of the type hint with the passed name).

    This factory is internally memoized for efficiency.

    Caveats
    -------
    **There is an unresolvable syntactic disambiguity between the following two
    competing use cases:**

    * When ``hint_name`` is an absolute forward reference (e.g.,
      ``"muh_package.muh_submodule.MuhType"``). In this case, the
      ``type_module_name`` local variable internally defined in the body of
      this factory is a valid module name.
    * When ``hint_name`` is a relative forward reference to a nested type (e.g.,
      ``"MuhOuterType.MuhInnerType"``). In this case, ``type_module_name`` is
      non-empty but *not* a valid module name.

      Thankfully, nested types are entirely useless in Python and thus
      *extremely* uncommon in real-world code. The latter use case is thus
      largely ignorable (but still regrettable).

      In theory, these two cases could be disambiguated in the body of this
      factory by calling the :func:`.is_module` tester below like so:

      .. code-block:: python

         if not (
             type_module_name and
             is_module(type_module_name)
         ):

      In practice, doing so would be ill-advised. The whole point of forward
      references is to defer module importation until *after* this early
      decoration time. Importing arbitrary third-party modules at this early
      decoration time would increase the likelihood of real-world issues in
      production code *far* more severe than this syntactic ambiguity.

      Lastly, note that third-party downstream consumers do have options here.
      To avoid this syntactic ambiguity, users intending to create forward
      references to nested types should either prefer unquoted forward
      references under Python >= 3.14 *or* instantiate
      :class:`.typing.ForwardRef` objects passed the ``module`` parameter: e.g.,

      .. code-block:: python

         # Instead of this ambiguous awfulness...
         is_bearable(['ok'], list['MuhInnerType.MuhOuterType'])

         # ...users should do this under Python >= 3.14:
         from typing import ForwardRef
         is_bearable(['ok'], list[MuhInnerType.MuhOuterType])

         # ...or this under Python <= 3.14:
         from typing import ForwardRef
         is_bearable(['ok'], list[ForwardRef(
             'MuhInnerType.MuhOuterType', module=__name__])

    Parameters
    ----------
    type_bases : Tuple[type, ...]
        Tuple of all base classes to be inherited by this forward reference
        subclass. For simplicity, this *must* be a 1-tuple ``(type_base,)``
        where ``type_base`` is a :class:`.BeartypeForwardRefSubbableABC`
        subclass.
    hint_name : str
        Absolute (i.e., fully-qualified) or relative (i.e., unqualified) name of
        this unresolved type hint to be proxied.
    scope_name : str
        Possibly ignored fully-qualified name of the lexical scope in which this
        unresolved type hint was originally declared. See also the
        :func:`.make_forwardref_subbable_subtype` docstring for further details.
    func_local_parent_codeobj_weakref : FuncLocalParentCodeObjectWeakref
        Proxy weakly referring to the code object underlying the lexical scope
        of the parent module, type, or callable whose body locally defines the
        locally decorated callable if this forward reference proxy subtype
        proxies a stringified forward reference annotating a locally decorated
        callable *or* :data:`None` otherwise. See also the
        :attr:`beartype._check.forward.reference.fwdrefabc.BeartypeForwardRefABC.__func_local_parent_codeobj_weakref_beartype__`
        class variable docstring for further details.

    Returns
    -------
    BeartypeForwardRef
        Forward reference proxy subclass proxying this type hint.

    Raises
    ------
    BeartypeDecorHintForwardRefException
        If either ``hint_name`` or ``scope_name`` are *not* syntactically valid
        ``"."``-delimited Python identifiers.
    '''

    # ....................{ MEMOIZE                        }....................
    # Memoization of forward references is guaranteed to be safe despite the
    # commonality of relative forward references that are contextually relative
    # to the current module and possibly current nested class hierarchy being
    # decorated in that module. Why? Because the caller is already guaranteed to
    # have passed a fully-qualified "hint_name" and/or "scope_name". The caller
    # has thus effectively passed the absolute name of a fully-qualified module
    # to which this forward reference is relative. Altogether, this pair of
    # "hint_name" and "scope_name" parameters uniquely refers to an absolute
    # (rather than relative) module attribute. From the low-level perspective of
    # this factory, relative forward references are high-level syntactic sugar
    # the caller has already reduced on our behalf to equivalent absolute
    # forward references and are thus of no interest or concern to this factory.
    # Since memoization of absolute forward references is guaranteed to be safe,
    # memoization is guaranteed to be safe here. So say we all.

    # Tuple of all passed parameters (in arbitrary order).
    args: BeartypeForwardRefArgs = (
        type_bases, hint_name, scope_name, func_local_parent_codeobj_weakref)

    # Forward reference proxy previously created and returned by a prior call to
    # this function passed these parameters if any *OR* "None" otherwise (i.e.,
    # if this is the first call to this function passed these parameters).
    forwardref_subtype = _forwardref_args_to_forwardref_get(args, None)

    # If this proxy has already been created, reuse and return this proxy as is.
    if forwardref_subtype is not None:
        return forwardref_subtype
    # Else, this proxy has yet to be created.

    # ....................{ VALIDATE                       }....................
    # Validate all passed parameters *AFTER* attempting to reuse a previously
    # memoized forward reference, for efficiency.
    assert len(type_bases) == 1, (
        f'{repr(type_bases)} not 1-tuple of a single superclass.')
    assert isinstance(hint_name, str), f'{repr(hint_name)} not string.'
    assert isinstance(scope_name, str), f'{repr(scope_name)} not string.'
    assert isinstance(
        func_local_parent_codeobj_weakref, NoneTypeOr[WeakrefCallableType]), (
        f'{repr(func_local_parent_codeobj_weakref)} neither weak reference '
        f'nor "None".')

    # If this attribute name is *NOT* a syntactically valid Python identifier,
    # raise an exception.
    die_unless_identifier(
        text=hint_name,
        exception_cls=BeartypeDecorHintForwardRefException,
        exception_prefix='Forward reference ',
    )
    # Else, this attribute name is a syntactically valid Python identifier.

    # ....................{ LOCALS                         }....................
    # Possibly empty fully-qualified module name and unqualified basename of the
    # unresolved hint referred to by this forward reference.
    type_module_name, _, type_name = hint_name.rpartition('.')

    # If this module name is empty, fallback to the passed module name if any.
    if not type_module_name:
        type_module_name = scope_name
    # Else, this module name is non-empty.

    # ....................{ PROXY                          }....................
    # Forward reference proxy to be returned.
    forwardref_subtype = make_type(
        type_name=type_name,
        type_module_name=type_module_name,
        type_bases=type_bases,
        exception_cls=BeartypeDecorHintForwardRefException,
        exception_prefix='Forward reference ',
    )

    # Classify passed parameters with this proxy.
    forwardref_subtype.__name_beartype__ = hint_name  # pyright: ignore
    forwardref_subtype.__scope_name_beartype__ = scope_name  # pyright: ignore
    forwardref_subtype.__func_local_parent_codeobj_weakref_beartype__ = (
        func_local_parent_codeobj_weakref)

    # Cache this proxy for reuse by subsequent calls to this factory function
    # passed the same parameters.
    _forwardref_args_to_forwardref[args] = forwardref_subtype

    # Return this proxy.
    return forwardref_subtype

# ....................{ PRIVATE ~ globals                  }....................
_forwardref_args_to_forwardref: dict[
    BeartypeForwardRefArgs, BeartypeForwardRef] = {}
'''
**Forward reference proxy cache** (i.e., dictionary mapping from the tuple of
all parameters passed to each prior call of the
:func:`._make_forwardref_subtype` factory function to the forward reference
proxy dynamically created and returned by that call).

This cache serves a dual purpose. Notably, this cache both enables:

* External callers to iterate over all previously instantiated forward reference
  proxies. This is particularly useful when responding to module reloading,
  which requires that *all* previously cached types be uncached.
* :func:`._make_forwardref_subtype` to internally memoize itself over its
  passed parameters. Since the existing ``callable_cached`` decorator could
  trivially do so as well, however, this is only a negligible side effect.
'''


_forwardref_args_to_forwardref_get = _forwardref_args_to_forwardref.get
'''
:meth:`dict.get` method bound to the :data:`._forwardref_args_to_forwardref`
dictionary global (as a negligible micro-optimization).
'''
