import numpy as np
import pytest
from scipy.io import loadmat
from nibabel.freesurfer.io import read_geometry
import brainstat.tests.surstat_wrap as sw
from brainstat.mesh.utils import mesh_edges
from brainspace.datasets import load_conte69

sw.matlab_init_surfstat()


def dummy_test(surf):
    try:
        # wrap matlab functions
        Wrapped_edg = sw.matlab_Edg(surf)

    except:
        pytest.skip("original matlab code doesn't work with these inputs...")

    Python_edg = mesh_edges(surf) + 1  # +1 to match across implementations.

    # compare matlab-python outputs
    testout = np.allclose(Wrapped_edg, Python_edg, rtol=1e-05, equal_nan=True)
    assert testout


def test_01():
    # take ax3 random arrays for surf['tri']
    a = np.random.randint(4, 100)
    A = {}
    A['tri'] = np.random.rand(a, 3)
    dummy_test(A)


def test_02():
    # dummy 3D array for surf['lat']
    A = {}
    A['lat'] = np.ones((10, 10))
    dummy_test(A)


def test_03():
    # dummy 3D array for surf['lat']
    A = {}
    A['lat'] = np.ones((10, 10, 10))
    dummy_test(A)


def test_04():
    A = {}
    A['lat'] = np.random.choice([0, 1], size=(10, 10, 10))
    dummy_test(A)


def test_05():
    # load freesurfer data lh.white & rh.white
    SW_surf_L = read_geometry('./data_OFF/lh.white')
    SW_surf_R = read_geometry('./data_OFF/rh.white')
    SW = {}
    SW['tri'] = np.concatenate((SW_surf_L[1]+1, 10242 + SW_surf_R[1]+1))
    dummy_test(SW)


def test_06():
    # load freesurfer data lh.pial & rh.pial
    Pial_Mesh_Left = read_geometry('./data_OFF/lh.pial')
    Pial_Mesh_Right = read_geometry('./data_OFF/rh.pial')
    Pial_Mesh = {}
    Pial_Mesh['tri'] = np.concatenate((Pial_Mesh_Left[1]+1,
                                       10242 + Pial_Mesh_Right[1]+1))
    dummy_test(Pial_Mesh)


def test_07():
    fname = ('./data_OFF/surf_lsub.mat')
    f = loadmat(fname)
    subiculum_left = {}
    subiculum_left['tri'] = f['ave_lsub']['tri'][0, 0]
    dummy_test(subiculum_left)


def test_08():
    # Test BSPolyData.
    surf, _ = load_conte69()
    dummy_test(surf)