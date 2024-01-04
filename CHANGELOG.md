# 20th Oct 2021

- Facilitate programming
  - Add a Jupyter Notebook with examples of the basic commands

- Facilitate testing
  - Split `fetch_authors` and `h_index` tests.
  - Add the Driver manager to facilitate Selenium usage.

- OS-Compatibility and Tool-Compatibility
  - Fix Unit tests for compatibility with Windows.
  - Add a `close()` method to `GoogleScholarDB` to facilitate testing on Windows.
  - Add a `close()` method to `GoogleScholarCacheSQLite` to facilitate testing on Windows.
  - Rename every test with `test_` to improve compatibility with PyCharm.
  - Add encoding when writing files.


# 10th Mar 2022

- Flake8 Compatibility

- Improve features
  - Detect more cluster ids during parsing.
  - Parse two element dates.
  - Beep for captcha.

-Questions
  - Add get_citation_graph


# 10th October 2023

- Update tests with most recent data
- Fix some typos
- Update requirements.txt
