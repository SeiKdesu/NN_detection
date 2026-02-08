"""
Hybrid objective patterns: 25D blocks summed into a 100D objective.

This file is intended to be the "easy to edit" configuration.

Each pattern consists of 4 blocks (25D each). A block is a dict:
  - func: one of BASE_FUNCS (see compute_objective.py)
  - transform: "none" | "shift" | "rot_shift"
  - seed: int | None  (used when transform != "none")
  - shift_range: float (optional, default 5.0)
  - weight: float (optional, default 1.0)

To change objectives:
  - Edit EX2_F_PATTERNS directly, or
  - Adjust the generator in _generate_ex2_patterns().
"""

from __future__ import annotations

from typing import Any

BLOCK_SIZE: int = 25
N_BLOCKS: int = 4
TOTAL_DIM: int = BLOCK_SIZE * N_BLOCKS


def _fixed_patterns() -> list[list[dict[str, Any]]]:
    # ex2_f1〜ex2_f7: 既存の f1〜f7 の意味に合わせた固定パターン
    return [
        # ex2_f1: Sphere + Rastrigin + Ellipsoid + (Rot+Shift)Rosenbrock
        [
            {"func": "sphere", "transform": "shift", "seed": 303},
            {"func": "rastrigin", "transform": "shift", "seed": 101},
            {"func": "ellipsoid", "transform": "shift", "seed": 202},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
        ],
        # ex2_f2: Sphere + Rastrigin + (Rot+Shift)Rosenbrock + (Rot+Shift)Rosenbrock
        [
            {"func": "sphere", "transform": "shift", "seed": 303},
            {"func": "rastrigin", "transform": "shift", "seed": 101},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
        ],
        # ex2_f3: Sphere + (Rot+Shift)Rosenbrock + (Rot+Shift)Rosenbrock + (Rot+Shift)Rosenbrock
        [
            {"func": "sphere", "transform": "shift", "seed": 303},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 101},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
        ],
        # ex2_f4: (Rot+Shift)Rosenbrock × 4
        [
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 303},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 101},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
        ],
        # ex2_f5: Sphere + Rastrigin + Ackley + (Rot+Shift)Rosenbrock
        [
            {"func": "sphere", "transform": "shift", "seed": 303},
            {"func": "rastrigin", "transform": "shift", "seed": 101},
            {"func": "ackley", "transform": "shift", "seed": 404},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 202},
        ],
        # ex2_f6: Rosenbrock × 4 (no shift/rotation)
        [
            {"func": "rosenbrock", "transform": "none", "seed": None},
            {"func": "rosenbrock", "transform": "none", "seed": None},
            {"func": "rosenbrock", "transform": "none", "seed": None},
            {"func": "rosenbrock", "transform": "none", "seed": None},
        ],
        # ex2_f7: (Rot+Shift)Sphere + (Rot+Shift)Rastrigin + (Rot+Shift)Ackley + (Rot+Shift)Rosenbrock
        [
            {"func": "sphere", "transform": "rot_shift", "seed": 701},
            {"func": "rastrigin", "transform": "rot_shift", "seed": 702},
            {"func": "ackley", "transform": "rot_shift", "seed": 703},
            {"func": "rosenbrock", "transform": "rot_shift", "seed": 704},
        ],
    ]


def _generate_ex2_patterns(total_patterns: int = 25) -> list[list[dict[str, Any]]]:
    """
    ex2_f8〜ex2_f{total_patterns} を生成します（決定論的・編集しやすい生成規則）。
    """
    fixed = _fixed_patterns()
    if total_patterns <= len(fixed):
        return fixed[:total_patterns]

    base_funcs = [
        "sphere",
        "rastrigin",
        "ackley",
        "rosenbrock",
        "ellipsoid",
        "griewank",
        "schwefel",
    ]
    transforms = ["shift", "rot_shift", "none"]

    patterns = list(fixed)
    for idx in range(len(fixed) + 1, total_patterns + 1):  # 1-based
        blocks: list[dict[str, Any]] = []
        for b in range(N_BLOCKS):
            func = base_funcs[(idx + b) % len(base_funcs)]
            transform = transforms[(idx + 2 * b) % len(transforms)]
            seed = None if transform == "none" else 1000 + idx * 10 + b
            blocks.append({"func": func, "transform": transform, "seed": seed})
        patterns.append(blocks)

    return patterns


# ex2_f1〜ex2_f25 のブロック定義（index 0 が f1）
EX2_F_PATTERNS: list[list[dict[str, Any]]] = _generate_ex2_patterns(total_patterns=25)

