"""
Tests for `simplebbox` package.
"""

import numpy as np
import torch
from pytest import approx

from simplebbox.numpy_array import bbox_numpy
from simplebbox.torch_tensor import bbox_torch
import simplebbox.array as bbox_array


class equal_np_array:
    # Tell numpy to use our `__eq__` operator instead of its.
    __array_ufunc__ = None
    __array_priority__ = 100

    def __init__(self, *args, **kwargs):
        self.value = np.array(*args, **kwargs)

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if not isinstance(other, np.ndarray):
            return False
        return self.value.dtype == other.dtype and np.array_equal(self.value, other)


class equal_tensor:
    __array_ufunc__ = None
    __array_priority__ = 100

    def __init__(self, *args, **kwargs):
        self.value = torch.tensor(*args, **kwargs)

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if not isinstance(other, torch.Tensor):
            return False
        return torch.equal(self.value, other)


def test_x0y0wh_to_x0y0x1y1():
    in1 = [100, 200, 10, 20]
    out1 = [100, 200, 110, 220]
    in2 = [10, 20, 10, 20]
    out2 = [10, 20, 20, 40]

    assert bbox_array.x0y0wh_to_x0y0x1y1(in1) == out1
    assert bbox_array.x0y0wh_to_x0y0x1y1(in2) == out2

    assert bbox_numpy.x0y0wh_to_x0y0x1y1(np.array(in1)) == equal_np_array(out1, dtype='int')
    assert bbox_numpy.x0y0wh_to_x0y0x1y1(np.array([in1])) == equal_np_array([out1], dtype='int')
    assert bbox_numpy.x0y0wh_to_x0y0x1y1(np.array([in1, in2])) == equal_np_array([out1, out2], dtype='int')
    assert bbox_numpy.x0y0wh_to_x0y0x1y1(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='int')

    assert bbox_torch.x0y0wh_to_x0y0x1y1(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.long)
    assert bbox_torch.x0y0wh_to_x0y0x1y1(torch.tensor([in1])) == equal_tensor([out1], dtype=torch.long)
    assert bbox_torch.x0y0wh_to_x0y0x1y1(torch.tensor([in1, in2])) == equal_tensor([out1, out2], dtype=torch.long)
    assert bbox_torch.x0y0wh_to_x0y0x1y1(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]], dtype=torch.long)


def test_x0y0x1y1_to_x0y0wh():
    in1 = [100, 200, 110, 220]
    out1 = [100, 200, 10, 20]
    in2 = [10, 20, 20, 40]
    out2 = [10, 20, 10, 20]

    assert bbox_array.x0y0x1y1_to_x0y0wh(in1) == out1
    assert bbox_array.x0y0x1y1_to_x0y0wh(in2) == out2

    assert bbox_numpy.x0y0x1y1_to_x0y0wh(np.array(in1)) == equal_np_array(out1, dtype='int')
    assert bbox_numpy.x0y0x1y1_to_x0y0wh(np.array([in1])) == equal_np_array([out1], dtype='int')
    assert bbox_numpy.x0y0x1y1_to_x0y0wh(np.array([in1, in2])) == equal_np_array([out1, out2], dtype='int')
    assert bbox_numpy.x0y0x1y1_to_x0y0wh(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='int')

    assert bbox_torch.x0y0x1y1_to_x0y0wh(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.long)
    assert bbox_torch.x0y0x1y1_to_x0y0wh(torch.tensor([in1])) == equal_tensor([out1], dtype=torch.long)
    assert bbox_torch.x0y0x1y1_to_x0y0wh(torch.tensor([in1, in2])) == equal_tensor([out1, out2], dtype=torch.long)
    assert bbox_torch.x0y0x1y1_to_x0y0wh(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]], dtype=torch.long)


def test_cxcywh_to_x0y0wh__with_float_as_input():
    assert bbox_array.cxcywh_to_x0y0wh([100, 200, 10.9, 21.], int) == [94, 189, 10, 21]
    assert bbox_array.cxcywh_to_x0y0wh([100, 200, 10.9, 21.], round) == [95, 190, 11, 21]
    assert bbox_array.cxcywh_to_x0y0wh([100, 200, 11, 21]) == approx([94.5, 189.5, 11., 21.])
    assert bbox_array.cxcywh_to_x0y0wh([100., 200., 11., 21.]) == approx([94.5, 189.5, 11., 21.])
    assert bbox_array.cxcywh_to_x0y0wh([100, 200, 10.8, 20.8]) == approx([94.6, 189.6, 10.8, 20.8])


def test_cxcywh_to_x0y0wh():
    in1 = [100, 200, 10, 20]
    out1 = [95, 190, 10, 20]
    in2 = [100, 200, 11, 21]
    out2_int = [94, 189, 11, 21]
    out2 = [94.5, 189.5, 11, 21]

    assert bbox_array.cxcywh_to_x0y0wh(in1, float) == approx(out1)
    assert bbox_array.cxcywh_to_x0y0wh(in1, int) == out1
    assert bbox_array.cxcywh_to_x0y0wh(in2, int) == out2_int
    assert bbox_array.cxcywh_to_x0y0wh(tuple(in1), int) == tuple(out1)

    assert bbox_numpy.cxcywh_to_x0y0wh(np.array(in1)) == equal_np_array(out1, dtype='float')
    assert bbox_numpy.cxcywh_to_x0y0wh(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='float')

    assert bbox_torch.cxcywh_to_x0y0wh(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.float)
    assert bbox_torch.cxcywh_to_x0y0wh(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]], dtype=torch.float)


def test_cxcywh_to_x0y0wh_int_div():
    in1 = [100, 200, 10, 20]
    out1 = [95, 190, 10, 20]
    in2 = [100, 200, 11, 21]
    out2 = [95, 190, 11, 21]

    assert bbox_array.cxcywh_to_x0y0wh_int_div(in1, float) == approx(out1)
    assert bbox_array.cxcywh_to_x0y0wh_int_div(in1, int) == out1
    assert bbox_array.cxcywh_to_x0y0wh_int_div(in2, int) == out2
    assert bbox_array.cxcywh_to_x0y0wh_int_div(tuple(in1), int) == tuple(out1)

    assert bbox_numpy.cxcywh_to_x0y0wh_int_div(np.array(in1)) == equal_np_array(out1, dtype='int')
    assert bbox_numpy.cxcywh_to_x0y0wh_int_div(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='int')

    assert bbox_torch.cxcywh_to_x0y0wh_int_div(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.long)
    assert bbox_torch.cxcywh_to_x0y0wh_int_div(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]],
                                                                                           dtype=torch.long)


def test_cxcywh_to_x0y0x1y1_float():
    assert bbox_array.cxcywh_to_x0y0x1y1([100, 200, 10, 20], float) == approx([95., 190., 105., 210.])
    assert bbox_array.cxcywh_to_x0y0x1y1([100, 200, 11, 21], float) == approx([94.5, 189.5, 105.5, 210.5])
    assert bbox_array.cxcywh_to_x0y0x1y1([100., 200., 11., 21.], float) == approx([94.5, 189.5, 105.5, 210.5])
    assert bbox_array.cxcywh_to_x0y0x1y1([100, 200, 10.8, 20.8], float) == approx(
        [95 - 0.4, 190 - 0.4, 105 + 0.4, 210 + 0.4])


def test_cxcywh_to_x0y0x1y1():
    in1 = [100, 200, 10, 20]
    out1 = [95, 190, 105, 210]
    in2 = [100, 200, 11, 21]
    out2_int = [94, 189, 105, 210]
    out2 = [94.5, 189.5, 105.5, 210.5]

    assert bbox_array.cxcywh_to_x0y0x1y1(in1, float) == approx(out1)
    assert bbox_array.cxcywh_to_x0y0x1y1(in1, int) == out1
    assert bbox_array.cxcywh_to_x0y0x1y1(in2, int) == out2_int
    assert bbox_array.cxcywh_to_x0y0x1y1(tuple(in1), int) == tuple(out1)

    assert bbox_numpy.cxcywh_to_x0y0x1y1(np.array(in1)) == equal_np_array(out1, dtype='float')
    assert bbox_numpy.cxcywh_to_x0y0x1y1(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='float')

    assert bbox_torch.cxcywh_to_x0y0x1y1(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.float)
    assert bbox_torch.cxcywh_to_x0y0x1y1(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]], dtype=torch.float)


def test_cxcywh_to_x0y0x1y1_int_div():
    in1 = [100, 200, 10, 20]
    out1 = [95, 190, 105, 210]
    in2 = [100, 200, 11, 21]
    out2 = [95, 190, 106, 211]

    assert bbox_array.cxcywh_to_x0y0x1y1_int_div(in1, float) == approx(out1)
    assert bbox_array.cxcywh_to_x0y0x1y1_int_div(in1, int) == out1
    assert bbox_array.cxcywh_to_x0y0x1y1_int_div(in2, int) == out2
    assert bbox_array.cxcywh_to_x0y0x1y1_int_div(tuple(in1), int) == tuple(out1)

    assert bbox_numpy.cxcywh_to_x0y0x1y1_int_div(np.array(in1)) == equal_np_array(out1, dtype='int')
    assert bbox_numpy.cxcywh_to_x0y0x1y1_int_div(np.array([[in1, in2]])) == equal_np_array([[out1, out2]], dtype='int')

    assert bbox_torch.cxcywh_to_x0y0x1y1_int_div(torch.tensor(in1)) == equal_tensor(out1, dtype=torch.long)
    assert bbox_torch.cxcywh_to_x0y0x1y1_int_div(torch.tensor([[in1, in2]])) == equal_tensor([[out1, out2]],
                                                                                             dtype=torch.long)


def test_xyxy_abs_to_rel():
    in_bbox = [100, 200, 200, 50]
    wh = [400, 200]
    assert bbox_numpy.xyxy_abs_to_rel(np.array(in_bbox), np.array(wh)) == equal_np_array([0.25, 1.0, 0.5, 0.25])
    assert bbox_torch.xyxy_abs_to_rel(torch.tensor(in_bbox), torch.tensor(wh)) == equal_tensor([0.25, 1.0, 0.5, 0.25])

    in_bbox2 = [0, 5, 5, 10]
    wh2 = [10, 10]
    assert bbox_numpy.xyxy_abs_to_rel(np.array([in_bbox, in_bbox2]), np.array([wh, wh2])) == \
           equal_np_array([
               [0.25, 1.0, 0.5, 0.25],
               [0., 0.5, 0.5, 1.]
           ])
    assert bbox_torch.xyxy_abs_to_rel(torch.tensor([in_bbox, in_bbox2]), torch.tensor([wh, wh2])) == \
           equal_tensor([
               [0.25, 1.0, 0.5, 0.25],
               [0., 0.5, 0.5, 1.]
           ])


def test_xyxy_rel_to_abs():
    in_bbox, wh = ([0.25, 1.0, 0.5, 0.25], [400, 200])

    assert bbox_numpy.xyxy_rel_to_abs(np.array(in_bbox), np.array(wh)) == equal_np_array([100., 200., 200., 50.])
    assert bbox_torch.xyxy_rel_to_abs(torch.tensor(in_bbox), torch.tensor(wh)) == equal_tensor([100., 200., 200., 50.])
