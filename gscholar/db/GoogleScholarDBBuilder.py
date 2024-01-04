from gscholar.GoogleScholarDB import GoogleScholarDB
from gscholar.scraping.GoogleScholar import GoogleScholar
from gscholar.utils.logger import info_log


class GoogleScholarDBBuilder:
    def __init__(self, source: GoogleScholar, target: GoogleScholarDB):
        """
        When you initialize a GoogleScholarDBBuilder, you need to provide
        two things. The source, that is a `GoogleScholar` API used to query data
        and the target where the data will be stored.
        :param source: GoogleScholar This is the `GoogleScholar` object used to collect the data
        :param target: GoogleScholarDB
        """
        self.db = target
        self.gs = source

    def fetch_citations(self, publication_cluster_id):
        """
        Collect every citation to a particular publication cluster id.
        As the object already contain a GoogleScholar API and a GoogleScholarDB,
        the role of this function is the move each citation information
        from the GoogleScholar to the GoogleScholarDB
        :param publication_cluster_id: cluster id of the publication to collect citations
        :return: None
        """

        gs = self.gs
        db = self.db

        citations = gs.get_citations(publication_cluster_id)
        citations.apply(lambda x: db.add_publication(x["clusters"][0], x["title"], x["year"], x["authors"]) if len(
            x["clusters"]) else None, axis=1)
        citations.apply(
            lambda x: db.add_citation(publication_cluster_id, x["clusters"][0]) if len(x["clusters"]) else None, axis=1)

        return citations

    def fetch_authors(self, author_list, depth=1):
        """
        Collect every publication of an author, and every direct citation to each publication.
        As the object already contain a GoogleScholar API and a GoogleScholarDB,
        the role of this function is the move each author information
        from the GoogleScholar to the GoogleScholarDB
        :param author_list: List of author to process
        :param depth: Crawling depth (by default 1 means no crawling, 0 is infinity)
        :return: None
        """

        gs = self.gs
        db = self.db

        # Authors : add_author (author_id, name)
        # Publications : add_publication (publication_cluster_id, title, year, authors)
        # Citations : add_citation (publication_cluster_id, cited_by)
        # Authorship : add_authorship (author_id, author_pub_id, publication_cluster_id)

        author_publications_dict = {}
        for author_id in author_list:
            author_details = gs.get_author_details(author_id)
            db.add_author(author_id, author_details["name"])
            author_publications_dict[author_id] = gs.get_author_publication_ids(author_id)
            publications = gs.get_author_publications(author_id).to_dict(orient='records')

            for publication in publications:
                author_publication_id = publication["pid"]
                publication_details = gs.get_publication_details(author_id, author_publication_id)
                if publication_details["cites"]:
                    publication_id = publication_details["cites"][0]
                else:
                    continue

                db.add_publication(
                    publication_id,
                    publication["title"],
                    publication["year"],
                    publication_details["authors"]
                )

                db.add_authorship(author_id, author_publication_id, publication_id)
                citations = gs.get_citations(publication_id).to_dict(orient='records')

                for citation in citations:
                    for cluster_id in citation["clusters"]:
                        db.add_citation(publication_id, cluster_id)

                        db.add_publication(
                            cluster_id,
                            citation["title"],
                            citation["year"],
                            citation["authors"]
                        )

        return None

    def crawl_publication(self, publication_cluster_id, max_level=0):
        """
        Crawl every citation from a particular publication cluster id.
        As the object already contain a GoogleScholar API and a GoogleScholarDB,
        the role of this function is the move each citation information
        from the GoogleScholar to the GoogleScholarDB
        :param publication_cluster_id: Root of the crawl
        :param max_level: How many level the crawl goes to
        :return: None
        """
        # TODO: publication_cluster_id is not necessarily inside the publications!!!!!
        from gscholar.utils.logger import error_log

        old_cluster_ids = []
        next_cluster_ids = [publication_cluster_id]
        level = 0
        while next_cluster_ids:
            info_log(f"Crawling level {level} : {len(next_cluster_ids)} publications")
            new_cluster_ids = []
            for p in next_cluster_ids:
                try:

                    ret_fetch = self.fetch_citations(p)
                    if len(ret_fetch):
                        citations = ret_fetch["clusters"].sum()
                    else:
                        citations = []
                    new_cluster_ids += citations
                except KeyError:
                    error_log(f"Error with citation {p}")
            next_cluster_ids = [x for x in set(new_cluster_ids) if x not in old_cluster_ids]
            old_cluster_ids += new_cluster_ids
            level += 1
            if level == max_level:
                info_log(f"End the crawl at level {level}.")
                break
        return

    def crawl_publications(self, cluster_ids, max_level=0):
        for p in cluster_ids:
            self.crawl_publication(p, max_level)
        return

# End of file
