## TODO
automatically handle usb udev rules/ better errors, guide the user to add the appropriate udev rule

SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2042",MODE="0666"                  

```
2026-05-26 18:04:13.521 Uncaught app execution
Traceback (most recent call last):
  File "/home/wissotsky/Documents/development/stikka-factory/.venv/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
  File "/home/wissotsky/Documents/development/stikka-factory/.venv/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 669, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wissotsky/Documents/development/stikka-factory/printit.py", line 38, in <module>
    from printer_utils import (
  File "/home/wissotsky/Documents/development/stikka-factory/printer_utils.py", line 19, in <module>
    from job_queue import print_queue
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 701, in _load_unlocked
KeyError: 'job_queue'
```
## DONE

Remove PDF file support(not worth the external dependency)

Remove AI Image Gen related features

Fetch images from openverse

Replace cat and dog image apis with openverse

Got rid of secrets.toml and related code