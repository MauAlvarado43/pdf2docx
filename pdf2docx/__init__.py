from pymupdf import Rect

def _rect_get_area(self) -> float:
    """Robust area computation for pymupdf.Rect."""
    try:
        x0 = float(self.x0)
        y0 = float(self.y0)
        x1 = float(self.x1)
        y1 = float(self.y1)
    except Exception:
        try:
            x0, y0, x1, y1 = map(float, tuple(self))
        except Exception:
            return 0.0

    w = max(0.0, x1 - x0)
    h = max(0.0, y1 - y0)
    return w * h

# add method if missing
if not hasattr(Rect, "get_area"):
    Rect.get_area = _rect_get_area

# add property `.area` for code that expects it
if not hasattr(Rect, "area"):
    Rect.area = property(_rect_get_area)

from .converter import Converter
from .page.Page import Page
from .main import parse