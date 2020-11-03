# mypy-extras

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![test](https://github.com/wemake-services/mypy-extras/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/mypy-extras/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/wemake-services/mypy-extras/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/mypy-extras)
[![Python Version](https://img.shields.io/pypi/pyversions/mypy-extras.svg)](https://pypi.org/project/mypy-extras/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Features

- Provides a custom `mypy` plugin to enhance its possibilities
- Provides new types that can be used in your programs with our plugin
- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)


## Installation

```bash
pip install mypy-extras
```

You also need to [configure](https://mypy.readthedocs.io/en/stable/config_file.html)
`mypy` correctly and install our custom plugin:

```ini
# In setup.cfg or mypy.ini:
[mypy]
plugins =
  mypy_extras.plugin.entrypoint
```

We also recommend to use the same `mypy` settings [we use](https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/mypy.toml).


## Usage

### AttrOf

We provide a special type to get named attributes of other types, like so:

```python
from typing_extensions import Literal  # or typing on python3.8+
from mypy_extras import AttrOf

class User(object):
    def auth(self, username: str, password: str) -> bool:
        return False  # Just an example

def get_callback(user: User) -> AttrOf[User, Literal['auth']]:
    return user.auth

user: User
reveal_type(get_callback(user))
# Revealed type is 'def (username: builtins.str, password: builtins.str) -> builtins.bool'
```


### ensure_attr

We can ensure that some `str` attribute exists on a object:

```python
from mypy_extras import ensure_attr


class User(object):
    policy = 'update'


reveal_type(ensure_attr(User, 'policy'))  # Revealed type is 'Literal['policy']'
reveal_type(ensure_attr(User, 'missing'))  # Error: attribute "missing" does not exist on type "User"
```

It is useful when we do any manipulations with objects based on a string field:

```python
DEFAULT_POLICY_FIELD: Final = ensure_attr(User, 'policy')  # typesafe
# vs
DEFAULT_POLICY_FIELD: Final = 'policy'  
# User can rename the field, and this will blow now!
```


## License

[MIT](https://github.com/wemake.services/mypy-extras/blob/master/LICENSE)
