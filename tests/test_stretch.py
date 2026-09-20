"""Run: python tests/test_stretch.py   (or pytest). Fails if stretching changes anything but the length."""
import sys
sys.path[:0] = ["src", "examples"]
from demo import demo_part
from stretch import find_cut, section_area, stretch

def test_stretch_only_adds_length():
    m = demo_part(); cut = find_cut(m, 2); out, area = stretch(m, 2, cut, 40)
    assert cut > 12, "cut must land in the plain tube, not in the flange or cross-hole zone"
    assert out.is_watertight and len(out.split(only_watertight=False)) == 1   # one welded body, not two halves
    assert abs(out.extents[2] - (m.extents[2] + 40)) < 1e-6
    assert abs(out.volume - (m.volume + area * 40)) < 1e-3 * m.volume
    assert abs(section_area(out, 2, 8) - section_area(m, 2, 8)) < 1e-6      # cross hole untouched

if __name__ == "__main__":
    test_stretch_only_adds_length(); print("ok")
