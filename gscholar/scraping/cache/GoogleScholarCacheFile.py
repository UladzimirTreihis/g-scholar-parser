import os

from os import listdir
from os.path import isfile, join


from gscholar.scraping.cache.GoogleScholarCache import GoogleScholarCache, GSInvalidCacheException

AUTHOR_FILE_PREFIX = "author_"
PUBLICATIONS_FILE_PREFIX = "publications_"
CITATIONS_FILE_PREFIX = "citations_"
VERSIONS_FILE_PREFIX = "versions_"


def save_to_file(filename, text):
    fd = open(filename, "w", encoding='utf-8')
    fd.write(text)
    fd.close()


def read_from_file(filename):
    try:
        fd = open(filename, "r", encoding='utf-8')
        text = fd.read()
        fd.close()
        return text
    except FileNotFoundError:
        return None


class GoogleScholarCacheFile (GoogleScholarCache):

    def __init__(self, db_path):
        super().__init__()
        self.folder = db_path
        if not os.path.isdir(db_path):
            os.mkdir(db_path)

    def add_author_page(self, userid, source):
        return save_to_file(f"{self.folder}/{AUTHOR_FILE_PREFIX}{userid}", source)

    def get_author_page(self, userid):
        return read_from_file(f"{self.folder}/{AUTHOR_FILE_PREFIX}{userid}")

    def add_publication_page(self, userid, publication_id, source):
        return save_to_file(f"{self.folder}/{PUBLICATIONS_FILE_PREFIX}{userid}_{publication_id}", source)

    def get_publication_page(self, userid, publication_id):
        return read_from_file(f"{self.folder}/{PUBLICATIONS_FILE_PREFIX}{userid}_{publication_id}")

    def add_citations_page(self, cluster_id, start, source):
        return save_to_file(f"{self.folder}/{CITATIONS_FILE_PREFIX}{cluster_id}_{start}", source)

    def get_citations_page(self, cluster_id, start):
        return read_from_file(f"{self.folder}/{CITATIONS_FILE_PREFIX}{cluster_id}_{start}")

    def add_versions_page(self, cluster_id, start, source):
        return save_to_file(f"{self.folder}/{VERSIONS_FILE_PREFIX}{cluster_id}_{start}", source)

    def get_versions_page(self, cluster_id, start):
        return read_from_file(f"{self.folder}/{VERSIONS_FILE_PREFIX}{cluster_id}_{start}")

    def dump(self):
        print(f"GoogleScholarCacheFile({self.folder})")
        print([f for f in listdir(self.folder) if isfile(join(self.folder, f))])

    def clear(self):
        pass

    def copy_into(self, cache):
        """
        Copy the cache into a different cache object
        In case of error GSInvalidCacheException is raised.
        :param cache:
        :return: None
        """

        try:
            data = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
            authors = [value.split('_') for value in data if AUTHOR_FILE_PREFIX in value]
            for author in authors:
                author_id = author[1]
                cache.add_author_page(
                    author_id,
                    self.get_author_page(author_id)
                )

            publications = [value.split('_') for value in data if PUBLICATIONS_FILE_PREFIX in value]
            for publication in publications:
                author_id = publication[1]
                publication_id = publication[2]
                cache.add_publication_page(
                    author_id,
                    publication_id,
                    self.get_publication_page(author_id, publication_id)
                )

            citations = [value.split('_') for value in data if CITATIONS_FILE_PREFIX in value]
            for citation in citations:
                cluster_id = citation[1]
                start = citation[2]
                cache.add_citations_page(
                    cluster_id,
                    start,
                    self.get_citations_page(cluster_id, start)
                )

            versions = [value.split('_') for value in data if VERSIONS_FILE_PREFIX in value]
            for version in versions:
                cluster_id = version[1]
                start = version[2]
                cache.add_versions_page(
                    cluster_id,
                    start,
                    self.get_versions_page(cluster_id, start)
                )

        except GSInvalidCacheException("GSInvalidCacheException") as e:
            raise e

        return None

# End of file
