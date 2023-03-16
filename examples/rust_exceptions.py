from fapolicy_analyzer.rust import throw_exception
from fapolicy_analyzer.rust import MalformedMarkerError

try:
    throw_exception("boom")
except MalformedMarkerError as e:
    print(f"caught: {e}")
