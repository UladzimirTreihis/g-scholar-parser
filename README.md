# YSC2244_Challenge_2

## Running the test

```
> tox

.pkg: _optional_hooks> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: get_requires_for_build_sdist> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: get_requires_for_build_wheel> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: prepare_metadata_for_build_wheel> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: build_sdist> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
py311: install_package> python -I -m pip install --force-reinstall --no-deps /home/toky/yalenus/teaching/apython/2023-2024-S1/challenges/c2/package/.tox/.tmp/package/5/google-scholar-api-0.0.1.tar.gz
py311: commands[0]> pytest
============================================================================================================ test session starts =============================================================================================================
platform linux -- Python 3.11.5, pytest-7.4.2, pluggy-1.3.0
cachedir: .tox/py311/.pytest_cache
rootdir: /home/toky/yalenus/teaching/apython/2023-2024-S1/challenges/c2/package
collected 28 items                                                                                                                                                                                                                           

tests/test_GSCacheCopy.py ..                                                                                                                                                                                                           [  7%]
tests/test_GSCrawler.py .                                                                                                                                                                                                              [ 10%]
tests/test_GSDB.py ......                                                                                                                                                                                                              [ 32%]
tests/test_GSDBBuilder.py ....                                                                                                                                                                                                         [ 46%]
tests/test_GoogleScholarCache.py ssss........                                                                                                                                                                                          [ 89%]
tests/test_GoogleScholarParser.py ...                                                                                                                                                                                                  [100%]

======================================================================================================= 24 passed, 4 skipped in 7.93s ========================================================================================================
.pkg: _exit> python /home/toky/.local/lib/python3.11/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
  py311: OK (9.33=setup[1.09]+cmd[8.23] seconds)
  congratulations :) (9.37 seconds)
```


