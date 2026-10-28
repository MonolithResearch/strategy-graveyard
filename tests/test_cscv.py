"""Independent reference checks for the synthetic CSCV demonstration."""
from itertools import combinations
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import rankdata

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import demo_validation as dv


def reference(matrix, n_splits):
    blocks = np.split(np.arange(len(matrix)), n_splits)
    below = []
    for selected in combinations(range(n_splits), n_splits // 2):
        train = np.concatenate([blocks[i] for i in selected])
        test = np.concatenate([blocks[i] for i in range(n_splits) if i not in selected])
        sr_train = np.array([dv.sharpe(matrix[train, j]) for j in range(matrix.shape[1])])
        sr_test = np.array([dv.sharpe(matrix[test, j]) for j in range(matrix.shape[1])])
        # Average tied training winners; no first-column preference.
        winners = np.flatnonzero(sr_train == sr_train.max())
        relative = rankdata(sr_test, method="average") / (matrix.shape[1] + 1)
        below.append(np.mean(relative[winners] <= 0.5))
    return float(np.mean(below))


def test_uses_all_symmetric_half_block_combinations():
    matrix = np.random.default_rng(123).normal(size=(24, 5))
    assert dv.pbo_cscv(matrix, n_splits=4) == pytest.approx(reference(matrix, 4))


def test_ties_use_midrank_and_are_order_invariant():
    x = np.tile([-1.0, 1.0], 12)
    matrix = np.column_stack((x, x, x))
    assert dv.pbo_cscv(matrix, n_splits=4) == 1.0
    assert dv.pbo_cscv(matrix[:, ::-1], n_splits=4) == 1.0


@pytest.mark.parametrize("splits", [0, 3, True, 4.5, 24, 100])
def test_invalid_splits_fail_explicitly(splits):
    with pytest.raises(ValueError):
        dv.pbo_cscv(np.ones((24, 4)), n_splits=splits)


@pytest.mark.parametrize("matrix", [np.ones(20), np.ones((20, 1)),
    np.ones((23, 3)), np.full((24, 3), np.nan), np.full((24, 3), np.inf)])
def test_invalid_matrix_is_rejected(matrix):
    with pytest.raises(ValueError):
        dv.pbo_cscv(matrix, n_splits=4)


def test_no_information_is_not_fabricated_for_constant_returns():
    assert dv.psr(np.zeros(30)) == 0.0
    assert dv.dsr(np.zeros(30), 10, 0.1) == 0.0


@pytest.mark.parametrize("value", [0.1, -0.1, 0.3, 1e10])
def test_nonzero_constants_do_not_create_floating_point_sharpe(value):
    values = np.full(30, value)
    assert dv.sharpe(values) == 0.0
    assert dv.psr(values) == 0.0
    assert dv.dsr(values, 10, 0.1) == 0.0


def test_constant_columns_have_no_spurious_cscv_winner():
    matrix = np.tile([0.1, 0.2, 0.3], (24, 1))
    assert dv.pbo_cscv(matrix, n_splits=4) == 1.0


@pytest.mark.parametrize("returns", [[], [1.0], [0.1, np.nan], [[1, 2], [3, 4]]])
def test_invalid_returns_rejected(returns):
    with pytest.raises(ValueError):
        dv.psr(returns)
