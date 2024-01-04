import os
import tempfile


def get_tmp_filename():
    # using tempfile we get an anonymous file
    fd = tempfile.NamedTemporaryFile(delete=False)
    fd.close()
    db_file = fd.name
    # we remove any existing file
    if os.path.exists(db_file):
        os.remove(db_file)
    return db_file
