import csv
import time
import os
import sys


from util.graphdb_base import GraphDBBase


class DRKGImporter(GraphDBBase):

    def __init__(self, argv):
        super().__init__(command=__file__, argv=argv)

    def import_all(self, file):
        with open(file, 'r+') as in_file:
            reader = csv.reader(in_file, delimiter='\t')
            next(reader, None)
            with self._driver.session(database=self.get_database()) as session:
                self.execute_without_exception("CREATE CONSTRAINT ON (u:DrkgNode) ASSERT u.id IS UNIQUE")

                tx = session.begin_transaction()
                j = 0
                query = """
                    MERGE (source:DrkgNode {id: $sourceId})
                    WITH source
                    CALL apoc.create.addLabels(source, [$sourceType])  YIELD node
                    MERGE (destination:DrkgNode {id: $destId})
                    WITH source, destination
                    CALL apoc.create.addLabels(destination, [$destinationType]) YIELD node
                    WITH source, destination
                    CALL apoc.merge.relationship(source,$relType,{}, {}, destination, {}) YIELD rel
                    RETURN id(source)
                """
                for row in reader:
                    try:
                        if row:
                            source_id = row[0]
                            rel_type = row[1].split("::")[1].replace(":", "_")
                            dest_id = row[2]
                            source_type = source_id.split("::")[0]
                            destination_type = dest_id.split("::")[0]
                            tx.run(query, {"sourceId": source_id, "destId": dest_id, "relType": rel_type, "sourceType": source_type, "destinationType": destination_type})
                            j += 1
                            if j % 1000 == 0:
                                tx.commit()
                                print(j, "lines processed")
                                tx = session.begin_transaction()
                    except Exception as e:
                        print(e, row, reader.line_num)
                tx.commit()
                print(j, "lines processed")


if __name__ == '__main__':
    start = time.time()
    importing = DRKGImporter(argv=sys.argv[1:])
    base_path = importing.source_dataset_path
    if not base_path:
        base_path = "./dataset/drkg/"
    file_path = os.path.join(base_path, "drkg.tsv")
    importing.import_all(file=file_path)
    end = time.time() - start
    print("Time to complete:", end)
