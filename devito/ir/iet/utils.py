from devito.ir.iet import IterationTree, FindSections, FindSymbols
from devito.symbolics import Keyword, Macro
from devito.tools import as_tuple, filter_ordered
from devito.types import Array, Global, LocalObject

__all__ = ['filter_iterations', 'retrieve_iteration_tree', 'derive_parameters',
           'diff_parameters']


def retrieve_iteration_tree(node, mode='normal'):
    """
    A list with all Iteration sub-trees within an IET.

    Examples
    --------
    Given the Iteration tree:

        .. code-block:: c

           Iteration i
             expr0
             Iteration j
               Iteration k
                 expr1
             Iteration p
               expr2

    Return the list: ::

        [(Iteration i, Iteration j, Iteration k), (Iteration i, Iteration p)]

    Parameters
    ----------
    iet : Node
        The searched Iteration/Expression tree.
    mode : str, optional
        - ``normal``
        - ``superset``: Iteration trees that are subset of larger iteration trees
                        are dropped.
    """
    assert mode in ('normal', 'superset')

    trees = [IterationTree(i) for i in FindSections().visit(node) if i]
    if mode == 'normal':
        return trees
    else:
        found = []
        for i in trees:
            if any(set(i).issubset(set(j)) for j in trees if i != j):
                continue
            found.append(i)
        return found


def filter_iterations(tree, key=lambda i: i):
    """
    Return the first sub-sequence of consecutive Iterations such that
    ``key(iteration)`` is True.
    """
    filtered = []
    for i in tree:
        if key(i):
            filtered.append(i)
        elif len(filtered) > 0:
            break
    return filtered


def derive_parameters(iet, drop_locals=False):
    """
    Derive all input parameters (function call arguments) from an IET
    by collecting all symbols not defined in the tree itself.
    """
    # Extract all candidate parameters
    candidates = FindSymbols().visit(iet)

    # Symbols, Objects, etc, become input parameters as well
    basics = FindSymbols('basics').visit(iet)
    candidates.extend(i.function for i in basics)

    # Filter off duplicates (e.g., `x_size` is extracted by both calls to FindSymbols)
    candidates = filter_ordered(candidates)

    # Filter off symbols which are defined somewhere within `iet`
    defines = [i._C_name for i in FindSymbols('defines').visit(iet)]
    parameters = [i for i in candidates if i._C_name not in defines]

    # Due to long-standing issue X, that is the presence of aliasing symbols in the
    # generated code (e.g., `ii_rec_0` being both a ConditionalDimension and a Symbol),
    # we also look at the name for symbols
    #weak_defines = [s.name for s in defines if s.is_Symbol]
    #from IPython import embed; embed()
    #parameters = [i for i in parameters
    #              if not (i.is_Symbol and i.name in weak_defines)]

    # Drop globally-visible objects
    parameters = [p for p in parameters if not isinstance(p, (Global, Keyword, Macro))]

    # Maybe filter out all other compiler-generated objects
    if drop_locals:
        parameters = [p for p in parameters if not isinstance(p, (Array, LocalObject))]

    return parameters


def diff_parameters(iet, root, indirectly_provided=None):
    """
    Derive the non-constant parameters of `iet`, a sub-IET within `root`, that is
    the parameters whose value changes at some point in `root`.

    The `indirectly_provided` are the parameters that are provided indirectly to
    `iet`, for example via a composite type (e.g., a C struct).
    """
    required = derive_parameters(iet)
    required = [i for i in required if i not in as_tuple(indirectly_provided)]

    known = set(root.parameters)
    known.update({i for i in required if i.is_AbstractFunction and not i._mem_external})
    known.update(set().union(*[i.bound_symbols for i in known]))

    dynamic_parameters = [i for i in required if i not in known]

    return dynamic_parameters
