''' component tests '''

#############
## Imports ##
#############

import torch
import pytest
import photontorch as pt

from fixtures import det


###########
## Tests ##
###########

def test_photodetector(det):
    pass

def test_photodetector_with_normal_cutoff_too_big():
    det = pt.Photodetector(bitrate=50e9, bandwidth=1000e9)

def test_photodetector_a_parameter(det):
    a = det.a
    assert a in det._buffers.values()
    assert a.shape[0] == det.filter_order+1

def test_photodetector_b_parameter(det):
    b = det.b
    assert (b == det.conv.weight).all()
    assert b.shape[0] == 1
    assert b.shape[1] == 1
    assert b.shape[2] == det.filter_order+1

def test_photodetector_b_setter(det):
    with pytest.raises(TypeError):
        det.b = 4
    det.b = torch.rand(det.b.shape)

def test_photodetector_forward(det):
    with torch.no_grad():
        num_bits = 10
        bits = torch.rand(num_bits) > 0.5
        det = pt.Photodetector(bitrate=50e9, dt=1./(10*50e9))
        timesteps_per_bit = int(1./(det.bitrate*det.dt)+0.5)
        bitstream = torch.stack([bits]*timesteps_per_bit, -1).flatten().float()
        detected_bitstream = det(bitstream)


###############
## Run Tests ##
###############

if __name__ == '__main__': # pragma: no cover
    pytest.main([__file__])