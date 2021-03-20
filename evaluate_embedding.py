import time
import os
import sys
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_fscore_support

from util.graphdb_base import GraphDBBase


class EvaluateEmbedding(GraphDBBase):

    def __init__(self, argv):
        super().__init__(command=__file__, argv=argv)

    def evaluate(self):
        with self._driver.session(database=self.get_database()) as session:
            query = """
             MATCH (node:DrkgNode)
             WITH node, rand() as rand
             order by rand 
             LIMIT 10000
             RETURN coalesce(node.symbol, node.id)  as nodeId, node.embeddingVectorFastRP as embedding, labels(node)[1] as category
         """
        result = session.run(query)
        df = pd.DataFrame([dict(record) for record in result])

        train, test = train_test_split(df, test_size=0.2)

        X = train.embedding.values.tolist()
        y = train.category.values.tolist()

        scaler = StandardScaler().fit(X)
        X_std = scaler.transform(X)

        clf = LogisticRegression(random_state=0, solver='liblinear', multi_class='ovr', max_iter=1000)
        model = clf.fit(X_std, y)

        X_test = test.embedding.values.tolist()
        y_test = test.category.values.tolist()
        X_test_std = scaler.transform(X_test)

        prediction = model.predict(X_test_std)
        gold = y_test
        print(list(prediction))
        print(gold)

        weighted = precision_recall_fscore_support(gold, prediction, average='weighted')
        print(weighted[2])


if __name__ == '__main__':
    start = time.time()
    importing = EvaluateEmbedding(argv=sys.argv[1:])
    importing.evaluate()
    end = time.time() - start
    print("Time to complete:", end)
