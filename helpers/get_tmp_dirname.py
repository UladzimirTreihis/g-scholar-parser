import tempfile


def get_tmp_dirname():
    # using tempfile we get an anonymous dir
    _temp_dir = tempfile.TemporaryDirectory()
    return _temp_dir.name
